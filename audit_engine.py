"""
Campaign Audit Engine
Processes uploaded CSV/XLSX data against best practice rules.
Supports check_type: 'threshold' (metric vs. benchmark) and 'checklist' (column presence/value check).
"""

import re
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional
from best_practices import AUDIT_RULES, CHANNELS, CHANNEL_MAP, METRIC_ALIASES


# ─── Data Structures ──────────────────────────────────────────────────────────

@dataclass
class AuditFinding:
    rule_id: str
    rule_name: str
    channel: str
    category: str
    severity: str           # 'critical' | 'warning' | 'pass' | 'not_applicable'
    status: str             # 'fail' | 'pass' | 'not_applicable'
    metric: Optional[str]
    actual_value: Optional[float]
    formatted_value: Optional[str]
    benchmark_label: Optional[str]
    evidence: str
    recommendation: str
    quick_win: bool
    description: str


@dataclass
class AuditResult:
    channel_id: str
    channel_name: str
    data_rows: int
    detected_metrics: list
    findings: list
    critical_count: int
    warning_count: int
    pass_count: int
    quick_win_count: int
    score: int
    summary_worked: list
    summary_improvements: list
    summary_quick_wins: list
    summary_anomalies: list


# ─── Helpers ──────────────────────────────────────────────────────────────────

def normalize_header(h: str) -> str:
    return re.sub(r'[^a-z0-9]', '_', h.lower()).strip('_')


def build_metric_map(columns: list) -> dict:
    """Map canonical metric names → actual DataFrame column names."""
    result = {}
    for col in columns:
        norm = normalize_header(col)
        canonical = METRIC_ALIASES.get(norm)
        if canonical:
            result[canonical] = col
    return result


def parse_numeric(val) -> Optional[float]:
    """Parse a value that may contain $, %, commas."""
    if pd.isna(val):
        return None
    s = str(val).replace('$', '').replace('%', '').replace(',', '').strip()
    try:
        return float(s)
    except ValueError:
        return None


def format_metric(metric: str, value: float) -> str:
    pct_metrics = {'CTR', 'VTR', 'CVR', 'Viewability'}
    currency_metrics = {'CPC', 'CPM', 'CPA', 'CPL', 'CPV', 'Cost'}
    if metric in pct_metrics:
        return f"{value:.2f}%"
    if metric in currency_metrics:
        return f"${value:.2f}"
    if metric in {'ROAS', 'Frequency'}:
        return f"{value:.2f}x" if metric == 'ROAS' else f"{value:.2f}"
    return f"{value:.2f}"


def detect_channel(columns: list) -> str:
    """Heuristically detect channel from column names."""
    h = ' '.join(normalize_header(c) for c in columns)
    if 'quality_score' in h or 'search_impression_share' in h:
        return 'google_search'
    if 'view_rate' in h or 'video_view' in h or 'cpv' in h:
        return 'youtube'
    if 'asset_group' in h or 'pmax' in h:
        return 'pmax'
    if 'viewability' in h or 'dv360' in h or 'insertion_order' in h:
        return 'dv360'
    if 'linkedin' in h or 'sponsored_content' in h or 'lead_gen_form' in h:
        return 'linkedin'
    if 'demand_gen' in h or 'discovery' in h:
        return 'demand_gen'
    if 'frequency' in h and 'reach' in h:
        return 'meta'
    return 'meta'


def _check_column_value(df: pd.DataFrame, col: str, expected_value: Optional[str]) -> tuple:
    """
    For checklist rules: check if a column exists and optionally matches expected_value.
    Returns (found: bool, actual_str: str)
    """
    if col not in df.columns:
        return False, None
    if expected_value is None:
        # Just presence check — column exists and has non-empty values
        non_empty = df[col].dropna().astype(str).str.strip()
        non_empty = non_empty[non_empty != '']
        return len(non_empty) > 0, str(df[col].iloc[0]) if len(df) > 0 else None
    # Value match check
    vals = df[col].astype(str).str.strip().str.lower()
    match = (vals == expected_value.lower()).any()
    actual = str(df[col].iloc[0]) if len(df) > 0 else None
    return match, actual


# ─── Core Audit Function ──────────────────────────────────────────────────────

def run_audit(df: pd.DataFrame, channel_id: str) -> AuditResult:
    channel = CHANNEL_MAP.get(channel_id)
    channel_name = channel.name if channel else channel_id
    columns = list(df.columns)
    metric_map = build_metric_map(columns)
    detected_metrics = list(metric_map.keys())

    channel_rules = [r for r in AUDIT_RULES if r.channel == channel_id]
    findings = []

    for rule in channel_rules:

        # ── Checklist rules (no metric needed, always shown) ──────────────────
        if rule.check_type == 'checklist':
            # checklist rules always surface — they represent structural best practices
            # that can't be auto-verified from a CSV, so we surface them as advisory checks
            findings.append(AuditFinding(
                rule_id=rule.id, rule_name=rule.name, channel=channel_id,
                category=rule.category, severity=rule.severity, status='fail',
                metric=None, actual_value=None, formatted_value=None,
                benchmark_label=rule.benchmark_label,
                evidence=rule.description,
                recommendation=rule.recommendation, quick_win=rule.quick_win,
                description=rule.description,
            ))
            continue

        # ── Threshold rules (metric-based) ────────────────────────────────────
        if not rule.metric:
            continue

        col = metric_map.get(rule.metric)

        if col is None:
            findings.append(AuditFinding(
                rule_id=rule.id, rule_name=rule.name, channel=channel_id,
                category=rule.category, severity='not_applicable', status='not_applicable',
                metric=rule.metric, actual_value=None, formatted_value=None,
                benchmark_label=rule.benchmark_label,
                evidence=f'Metric "{rule.metric}" not found in uploaded data.',
                recommendation=rule.recommendation, quick_win=rule.quick_win,
                description=rule.description,
            ))
            continue

        values = [parse_numeric(v) for v in df[col] if parse_numeric(v) is not None]
        if not values:
            findings.append(AuditFinding(
                rule_id=rule.id, rule_name=rule.name, channel=channel_id,
                category=rule.category, severity='not_applicable', status='not_applicable',
                metric=rule.metric, actual_value=None, formatted_value=None,
                benchmark_label=rule.benchmark_label,
                evidence=f'No valid numeric data found for "{rule.metric}".',
                recommendation=rule.recommendation, quick_win=rule.quick_win,
                description=rule.description,
            ))
            continue

        avg_val = sum(values) / len(values)
        fmt_val = format_metric(rule.metric, avg_val)

        if rule.check_type == 'threshold' and rule.threshold is not None:
            is_bad = (avg_val < rule.threshold) if rule.threshold_direction == 'below' else (avg_val > rule.threshold)
            if is_bad:
                direction_word = 'below' if rule.threshold_direction == 'below' else 'above'
                threshold_fmt = format_metric(rule.metric, rule.threshold)
                evidence = (
                    f"{rule.metric} is **{fmt_val}** — {direction_word} the {threshold_fmt} threshold. "
                    f"Benchmark: {rule.benchmark_label or 'N/A'}."
                )
                findings.append(AuditFinding(
                    rule_id=rule.id, rule_name=rule.name, channel=channel_id,
                    category=rule.category, severity=rule.severity, status='fail',
                    metric=rule.metric, actual_value=avg_val, formatted_value=fmt_val,
                    benchmark_label=rule.benchmark_label, evidence=evidence,
                    recommendation=rule.recommendation, quick_win=rule.quick_win,
                    description=rule.description,
                ))
            else:
                evidence = (
                    f"{rule.metric} is **{fmt_val}** — within acceptable range. "
                    f"Benchmark: {rule.benchmark_label or 'N/A'}."
                )
                findings.append(AuditFinding(
                    rule_id=rule.id, rule_name=rule.name, channel=channel_id,
                    category=rule.category, severity='pass', status='pass',
                    metric=rule.metric, actual_value=avg_val, formatted_value=fmt_val,
                    benchmark_label=rule.benchmark_label, evidence=evidence,
                    recommendation='', quick_win=False,
                    description=rule.description,
                ))

    # Counts — use rule lookup to exclude checklist from critical score impact
    rule_map = {r.id: r for r in channel_rules}
    def is_checklist(f): return rule_map.get(f.rule_id) and rule_map[f.rule_id].check_type == 'checklist'
    critical_count  = sum(1 for f in findings if f.status == 'fail' and f.severity == 'critical' and not is_checklist(f))
    warning_count   = sum(1 for f in findings if f.status == 'fail' and f.severity == 'warning')
    pass_count      = sum(1 for f in findings if f.status == 'pass')
    quick_win_count = sum(1 for f in findings if f.status == 'fail' and f.quick_win)

    score = max(0, min(100, 100 - (critical_count * 20) - (warning_count * 8)))

    summary_worked = [
        f"**{f.rule_name}**: {f.formatted_value} — within benchmark ({f.benchmark_label})"
        for f in findings if f.status == 'pass' and f.formatted_value
    ]
    summary_improvements = [
        f"**{f.rule_name}**: {f.evidence}"
        for f in findings if f.status == 'fail'
    ]
    summary_quick_wins = [
        f.rule_name for f in findings if f.status == 'fail' and f.quick_win
    ]
    summary_anomalies = [
        f.evidence for f in findings if f.status == 'fail' and f.severity == 'critical'
    ]

    return AuditResult(
        channel_id=channel_id,
        channel_name=channel_name,
        data_rows=len(df),
        detected_metrics=detected_metrics,
        findings=findings,
        critical_count=critical_count,
        warning_count=warning_count,
        pass_count=pass_count,
        quick_win_count=quick_win_count,
        score=score,
        summary_worked=summary_worked,
        summary_improvements=summary_improvements,
        summary_quick_wins=summary_quick_wins,
        summary_anomalies=summary_anomalies,
    )
