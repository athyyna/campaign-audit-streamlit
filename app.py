"""
Campaign Best Practice Auditor — Streamlit App
=================================================
How to use:
  1. Upload a CSV or XLSX campaign report export from any supported platform
  2. Select the channel (auto-detected, but you can override)
  3. Click "Run Audit" to see findings, score, and recommendations
  4. Use the sidebar filters to focus on Critical issues, Quick Wins, etc.

Supported channels: Google Search, YouTube, Performance Max, DV360, LinkedIn, Meta, Demand Gen
"""

import re
import io
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from best_practices import CHANNELS, CHANNEL_MAP, DEMO_DATA, SEVERITY_CONFIG
from audit_engine import run_audit, detect_channel, AuditResult, AuditFinding


def md_to_html(text: str) -> str:
    """Convert **bold** markdown to <strong> tags for safe HTML injection."""
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Campaign Best Practice Auditor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
  /* Dark navy background */
  .stApp { background-color: #0F172A; color: #E2E8F0; }
  .stApp header { background-color: #0F172A; }

  /* Sidebar */
  section[data-testid="stSidebar"] { background-color: #111827; border-right: 1px solid rgba(255,255,255,0.06); }
  section[data-testid="stSidebar"] * { color: #CBD5E1 !important; }

  /* Cards */
  .metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
  }
  .metric-card .value { font-size: 2rem; font-weight: 700; font-family: 'Courier New', monospace; }
  .metric-card .label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.4); margin-top: 4px; }

  /* Finding rows */
  .finding-critical { border-left: 3px solid #EF4444; padding: 12px 16px; border-radius: 0 8px 8px 0; background: rgba(239,68,68,0.06); margin-bottom: 8px; }
  .finding-warning  { border-left: 3px solid #F59E0B; padding: 12px 16px; border-radius: 0 8px 8px 0; background: rgba(245,158,11,0.06); margin-bottom: 8px; }
  .finding-pass     { border-left: 3px solid #10B981; padding: 12px 16px; border-radius: 0 8px 8px 0; background: rgba(16,185,129,0.06); margin-bottom: 8px; }
  .finding-na       { border-left: 3px solid rgba(255,255,255,0.15); padding: 12px 16px; border-radius: 0 8px 8px 0; background: rgba(255,255,255,0.02); margin-bottom: 8px; }

  /* Badge */
  .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-right: 6px; }
  .badge-critical    { background: rgba(239,68,68,0.15);  color: #EF4444; border: 1px solid rgba(239,68,68,0.3); }
  .badge-warning     { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.3); }
  .badge-pass        { background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.3); }
  .badge-quickwin    { background: rgba(59,130,246,0.15); color: #60A5FA; border: 1px solid rgba(59,130,246,0.3); }
  .badge-na          { background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.35); }

  /* Section headers */
  .section-header { font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: rgba(255,255,255,0.3); margin-bottom: 12px; margin-top: 24px; }

  /* Score number */
  .score-number { font-size: 3.5rem; font-weight: 800; font-family: 'Courier New', monospace; }

  /* Divider */
  hr { border-color: rgba(255,255,255,0.08); }

  /* ── Streamlit widget overrides ── */
  .stButton > button { background: rgba(59,130,246,0.2); border: 1px solid rgba(59,130,246,0.4); color: #93C5FD; border-radius: 8px; font-weight: 600; }
  .stButton > button:hover { background: rgba(59,130,246,0.35); border-color: rgba(59,130,246,0.6); }
  div[data-testid="stMetricValue"] { color: #E2E8F0; }
  .stTabs [data-baseweb="tab"] { color: rgba(255,255,255,0.5); }
  .stTabs [aria-selected="true"] { color: #60A5FA; }
  .stExpander { border: 1px solid rgba(255,255,255,0.08) !important; background: rgba(255,255,255,0.02) !important; border-radius: 8px !important; }

  /* ── File uploader — dark themed ── */
  [data-testid="stFileUploader"] section,
  [data-testid="stFileUploaderDropzone"],
  [data-testid="stFileUploaderDropzoneInstructions"] {
    background-color: rgba(59,130,246,0.05) !important;
    border: 1px dashed rgba(59,130,246,0.3) !important;
    border-radius: 8px !important;
    color: #94A3B8 !important;
  }
  [data-testid="stFileUploader"] section:hover,
  [data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(59,130,246,0.6) !important;
    background-color: rgba(59,130,246,0.1) !important;
  }
  [data-testid="stFileUploaderDropzoneInstructions"] span,
  [data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #64748B !important;
  }
  /* The "Browse files" button inside uploader */
  [data-testid="stFileUploaderDropzone"] button,
  [data-testid="stFileUploader"] button {
    background-color: rgba(59,130,246,0.18) !important;
    border: 1px solid rgba(59,130,246,0.4) !important;
    color: #93C5FD !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
  }
  [data-testid="stFileUploaderDropzone"] button:hover,
  [data-testid="stFileUploader"] button:hover {
    background-color: rgba(59,130,246,0.3) !important;
    border-color: rgba(59,130,246,0.6) !important;
  }
  /* Uploaded file pill */
  [data-testid="stFileUploaderFile"],
  [data-testid="stFileUploaderFileName"] {
    background-color: rgba(16,185,129,0.08) !important;
    border: 1px solid rgba(16,185,129,0.2) !important;
    border-radius: 6px !important;
    color: #6EE7B7 !important;
  }
  [data-testid="stFileUploaderDeleteBtn"] button {
    color: #64748B !important;
    background: transparent !important;
    border: none !important;
  }

  /* ── Radio buttons ── */
  [data-testid="stRadio"] > div { gap: 6px; }
  [data-testid="stRadio"] label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 6px !important;
    padding: 6px 12px !important;
    color: #CBD5E1 !important;
    transition: all 0.15s;
  }
  [data-testid="stRadio"] label:hover {
    background: rgba(59,130,246,0.1) !important;
    border-color: rgba(59,130,246,0.35) !important;
  }
  /* Hide the raw radio circle — use styled label instead */
  [data-testid="stRadio"] input[type="radio"] { accent-color: #3B82F6; }

  /* ── Selectbox / dropdown ── */
  [data-testid="stSelectbox"] > div > div,
  div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
  }
  div[data-baseweb="select"] span { color: #E2E8F0 !important; }
  /* Dropdown popover + menu list */
  div[data-baseweb="popover"],
  div[data-baseweb="popover"] ul,
  div[data-baseweb="menu"] {
    background-color: #1E293B !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
  }
  /* Every list item — force light text */
  div[data-baseweb="menu"] li,
  div[data-baseweb="menu"] li *,
  div[data-baseweb="menu"] [role="option"],
  div[data-baseweb="menu"] [role="option"] * {
    color: #CBD5E1 !important;
    background-color: transparent !important;
  }
  /* Hover state */
  div[data-baseweb="menu"] li:hover,
  div[data-baseweb="menu"] [role="option"]:hover {
    background-color: rgba(59,130,246,0.18) !important;
    color: #E2E8F0 !important;
  }
  /* Selected / highlighted item */
  div[data-baseweb="menu"] [aria-selected="true"],
  div[data-baseweb="menu"] [data-highlighted="true"] {
    background-color: rgba(59,130,246,0.25) !important;
    color: #93C5FD !important;
  }

  /* ── Success / info / warning alert boxes ── */
  [data-testid="stAlert"] {
    background-color: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #CBD5E1 !important;
  }
  div[data-testid="stNotification"] { background-color: rgba(16,185,129,0.12) !important; border-color: rgba(16,185,129,0.3) !important; }

  /* ── Caption / small text ── */
  .stCaption, [data-testid="stCaptionContainer"] { color: rgba(255,255,255,0.35) !important; }

  /* ── Download button ── */
  [data-testid="stDownloadButton"] button {
    background: rgba(16,185,129,0.15) !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    color: #6EE7B7 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
  }
  [data-testid="stDownloadButton"] button:hover {
    background: rgba(16,185,129,0.25) !important;
  }

  /* ── Dataframe ── */
  [data-testid="stDataFrame"] { border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 8px !important; overflow: hidden; }

  /* ── Labels ── */
  .stSelectbox label, .stFileUploader label, .stRadio label {
    color: rgba(255,255,255,0.45) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def score_color(score: int) -> str:
    if score >= 75: return '#10B981'
    if score >= 50: return '#F59E0B'
    return '#EF4444'


def score_label(score: int) -> str:
    if score >= 75: return 'Healthy'
    if score >= 50: return 'Needs Work'
    return 'At Risk'


def make_gauge(score: int) -> go.Figure:
    color = score_color(score)
    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': score_label(score), 'font': {'size': 14, 'color': 'rgba(255,255,255,0.5)'}},
        number={'font': {'size': 48, 'color': color, 'family': 'Courier New'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'rgba(255,255,255,0.2)', 'tickfont': {'color': 'rgba(255,255,255,0.3)'}},
            'bar': {'color': color, 'thickness': 0.25},
            'bgcolor': 'rgba(255,255,255,0.04)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50],  'color': 'rgba(239,68,68,0.08)'},
                {'range': [50, 75], 'color': 'rgba(245,158,11,0.08)'},
                {'range': [75, 100],'color': 'rgba(16,185,129,0.08)'},
            ],
            'threshold': {'line': {'color': color, 'width': 3}, 'thickness': 0.8, 'value': score},
        }
    ))
    fig.update_layout(
        height=220, margin=dict(t=20, b=0, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#E2E8F0'},
    )
    return fig


def make_findings_bar(result: AuditResult) -> go.Figure:
    categories = {}
    for f in result.findings:
        if f.status == 'not_applicable':
            continue
        cat = f.category
        if cat not in categories:
            categories[cat] = {'critical': 0, 'warning': 0, 'pass': 0}
        if f.status == 'fail':
            categories[cat][f.severity] = categories[cat].get(f.severity, 0) + 1
        else:
            categories[cat]['pass'] += 1

    cats = list(categories.keys())
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Critical', x=cats, y=[categories[c]['critical'] for c in cats], marker_color='#EF4444'))
    fig.add_trace(go.Bar(name='Warning',  x=cats, y=[categories[c]['warning']  for c in cats], marker_color='#F59E0B'))
    fig.add_trace(go.Bar(name='Pass',     x=cats, y=[categories[c]['pass']     for c in cats], marker_color='#10B981'))
    fig.update_layout(
        barmode='stack', height=200,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#E2E8F0', 'size': 11},
        margin=dict(t=10, b=30, l=0, r=0),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, font={'size': 10}),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont={'size': 10}),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont={'size': 10}),
    )
    return fig


# Shared CSS for finding cards (injected once per render_finding call via components.html)
_FINDING_CSS = """
<style>
  body { margin:0; padding:0; background:transparent; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
  .finding-critical { border-left:3px solid #EF4444; padding:12px 16px; border-radius:0 8px 8px 0; background:rgba(239,68,68,0.08); margin-bottom:0; }
  .finding-warning  { border-left:3px solid #F59E0B; padding:12px 16px; border-radius:0 8px 8px 0; background:rgba(245,158,11,0.08); margin-bottom:0; }
  .finding-pass     { border-left:3px solid #10B981; padding:12px 16px; border-radius:0 8px 8px 0; background:rgba(16,185,129,0.08); margin-bottom:0; }
  .finding-na       { border-left:3px solid rgba(255,255,255,0.12); padding:12px 16px; border-radius:0 8px 8px 0; background:rgba(255,255,255,0.02); margin-bottom:0; }
  .badge { display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.68rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-right:6px; }
  .badge-critical { background:rgba(239,68,68,0.15); color:#EF4444; border:1px solid rgba(239,68,68,0.3); }
  .badge-warning  { background:rgba(245,158,11,0.15); color:#F59E0B; border:1px solid rgba(245,158,11,0.3); }
  .badge-pass     { background:rgba(16,185,129,0.15); color:#10B981; border:1px solid rgba(16,185,129,0.3); }
  .badge-quickwin { background:rgba(59,130,246,0.15); color:#60A5FA; border:1px solid rgba(59,130,246,0.3); }
  .badge-na       { background:rgba(255,255,255,0.06); color:rgba(255,255,255,0.3); }
  .cat-label { font-size:0.65rem; color:rgba(255,255,255,0.3); text-transform:uppercase; letter-spacing:0.1em; }
  .rule-name { font-weight:600; margin-top:4px; font-size:0.9rem; color:#E2E8F0; }
  .evidence  { font-size:0.78rem; color:rgba(255,255,255,0.5); margin-top:3px; line-height:1.5; }
  .rec-block { margin-top:8px; font-size:0.78rem; color:rgba(255,255,255,0.5); line-height:1.5; }
  .rec-block strong { color:#60A5FA; }
  .val-block { text-align:right; min-width:70px; font-family:'Courier New',monospace; font-weight:700; font-size:0.95rem; white-space:nowrap; }
  .row { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }
</style>
"""


def render_finding(f: AuditFinding):
    sev_key = f.severity if f.status != 'not_applicable' else 'na'
    css_class   = {'critical':'finding-critical','warning':'finding-warning','pass':'finding-pass'}.get(sev_key,'finding-na')
    badge_class = {'critical':'badge-critical','warning':'badge-warning','pass':'badge-pass'}.get(sev_key,'badge-na')
    badge_label = {'critical':'🔴 Critical','warning':'🟡 Warning','pass':'🟢 Pass'}.get(sev_key,'⚪ N/A')
    val_color   = SEVERITY_CONFIG.get(f.severity, {}).get('color', '#888')

    qw_badge  = '<span class="badge badge-quickwin">⚡ Quick Win</span>' if f.quick_win and f.status == 'fail' else ''
    value_str = f'<div class="val-block" style="color:{val_color}">{f.formatted_value}</div>' if f.formatted_value else '<div></div>'
    evidence_html = md_to_html(f.evidence)
    rec_html = ''
    if f.status == 'fail' and f.recommendation:
        rec_html = f'<div class="rec-block"><strong>→ Recommendation:</strong> {f.recommendation}</div>'

    html = f"""{_FINDING_CSS}
<div class="{css_class}">
  <div class="row">
    <div style="flex:1;min-width:0">
      <span class="badge {badge_class}">{badge_label}</span>{qw_badge}
      <span class="cat-label">{f.category}</span>
      <div class="rule-name">{f.rule_name}</div>
      <div class="evidence">{evidence_html}</div>
      {rec_html}
    </div>
    {value_str}
  </div>
</div>"""
    # height auto-sizes: ~90px base + ~20px for recommendation
    height = 115 if (f.status == 'fail' and f.recommendation) else 85
    components.html(html, height=height, scrolling=False)


def load_demo(channel_id: str) -> pd.DataFrame:
    data = DEMO_DATA[channel_id]
    return pd.DataFrame(data['rows'], columns=data['headers'])


def export_findings_csv(result: AuditResult) -> bytes:
    rows = []
    for f in result.findings:
        rows.append({
            'Channel': result.channel_name,
            'Category': f.category,
            'Check': f.rule_name,
            'Status': f.status.upper(),
            'Severity': f.severity.upper() if f.status != 'not_applicable' else 'N/A',
            'Metric': f.metric or '',
            'Actual Value': f.formatted_value or '',
            'Benchmark': f.benchmark_label or '',
            'Evidence': f.evidence,
            'Recommendation': f.recommendation,
            'Quick Win': 'Yes' if f.quick_win and f.status == 'fail' else '',
        })
    df = pd.DataFrame(rows)
    return df.to_csv(index=False).encode('utf-8')


# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📊 Campaign Auditor")
    st.markdown('<div style="font-size:0.7rem;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px">Best Practice Engine</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Data Source</div>', unsafe_allow_html=True)

    data_source = st.radio("", ["Upload CSV/XLSX", "Use Demo Data"], label_visibility="collapsed")

    df_input = None
    channel_id = None

    if data_source == "Upload CSV/XLSX":
        uploaded = st.file_uploader("Upload report", type=['csv', 'xlsx', 'xls'], label_visibility="collapsed")
        if uploaded:
            try:
                if uploaded.name.endswith('.csv'):
                    df_input = pd.read_csv(uploaded)
                else:
                    df_input = pd.read_excel(uploaded)
                st.success(f"✓ {len(df_input)} rows loaded")
            except Exception as e:
                st.error(f"Error reading file: {e}")
    else:
        demo_channel = st.selectbox(
            "Select channel",
            options=[c.id for c in CHANNELS],
            format_func=lambda x: CHANNEL_MAP[x].icon + ' ' + CHANNEL_MAP[x].name,
        )
        df_input = load_demo(demo_channel)
        st.info(f"Demo data loaded: {len(df_input)} rows")

    if df_input is not None:
        st.markdown("---")
        st.markdown('<div class="section-header">Channel Override</div>', unsafe_allow_html=True)
        auto_detected = detect_channel(list(df_input.columns))
        channel_id = st.selectbox(
            "Channel",
            options=[c.id for c in CHANNELS],
            index=[c.id for c in CHANNELS].index(auto_detected),
            format_func=lambda x: CHANNEL_MAP[x].icon + ' ' + CHANNEL_MAP[x].name,
            label_visibility="collapsed",
        )
        st.caption(f"Auto-detected: {CHANNEL_MAP[auto_detected].name}")

    st.markdown("---")
    st.markdown('<div style="font-size:0.68rem;color:rgba(255,255,255,0.2);text-align:center">Co-built by Athena & Manus<br>Best practices: 2024–2025</div>', unsafe_allow_html=True)


# ─── Main Content ─────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div style="padding:24px 0 8px 0">
  <div style="font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.15em;color:#3B82F6;margin-bottom:8px">Campaign Intelligence Engine</div>
  <h1 style="font-size:2rem;font-weight:800;margin:0;color:#F1F5F9">Campaign Best Practice <span style="color:#3B82F6">Auditor</span></h1>
  <p style="color:rgba(255,255,255,0.4);font-size:0.85rem;margin-top:8px">Upload any campaign report and instantly surface anomalies, quick wins, and what's working — across 7 channels.</p>
</div>
""", unsafe_allow_html=True)

if df_input is None:
    # Landing state
    st.markdown("---")
    cols = st.columns(len(CHANNELS))
    for i, ch in enumerate(CHANNELS):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align:center;padding:12px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:8px">
              <div style="font-size:1.4rem">{ch.icon}</div>
              <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);margin-top:4px">{ch.name}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Upload a CSV/XLSX export or select demo data from the sidebar to begin your audit.")

    with st.expander("📋 How to use this tool"):
        st.markdown("""
        **Step 1 — Get your data**
        Export your campaign report from any platform:
        - **Google Ads**: Reports → Download as CSV
        - **Meta Ads Manager**: Export → CSV
        - **LinkedIn Campaign Manager**: Export → CSV
        - **YouTube / DV360**: Standard performance report export

        **Step 2 — Upload & detect**
        The tool auto-detects the channel from your column headers. You can override this in the sidebar.

        **Step 3 — Review findings**
        Findings are sorted by severity. Use the filter tabs to focus on:
        - 🔴 **Critical** — fix immediately
        - 🟡 **Warning** — address soon
        - ⚡ **Quick Wins** — high impact, low effort
        - 🟢 **Passing** — what's working well

        **Step 4 — Export**
        Download the full audit as CSV to share with your agency or XFN partners.
        """)

    with st.expander("📊 KPI Benchmarks Reference"):
        benchmark_data = {
            'Channel': ['Google Search', 'YouTube', 'Performance Max', 'DV360', 'LinkedIn', 'Meta', 'Demand Gen'],
            'CTR': ['3–6%', '0.5–2%', '1–3%', '0.1–0.35%', '0.4–1.0%', '1–3%', '0.5–2%'],
            'CPM': ['$10–15', '$5–12', '$8–15', '$2–8', '$20–50', '$8–20', '$10–18'],
            'CPC': ['$1–5', '$0.10–0.30', '$1–4', '$0.50–2', '$5–15', '$0.50–3', '$1–4'],
            'CPA/CPL': ['$20–40', '—', '$25–50', '—', '$50–150', '$10–50', '$20–80'],
            'Frequency': ['—', '2–5/wk', '—', '3–7/wk', '1–4', '1–3', '2–5'],
        }
        st.dataframe(pd.DataFrame(benchmark_data), use_container_width=True, hide_index=True)

else:
    # ── Run Audit ──────────────────────────────────────────────────────────────
    result = run_audit(df_input, channel_id)
    channel = CHANNEL_MAP[channel_id]

    # ── Top Bar ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
      <span style="font-size:1.2rem">{channel.icon}</span>
      <span style="font-size:1.1rem;font-weight:700;color:#F1F5F9">{channel.name} Audit</span>
      <span style="font-size:0.75rem;color:rgba(255,255,255,0.35)">{result.data_rows} rows · {len(result.detected_metrics)} metrics detected</span>
    </div>
    <div style="font-size:0.72rem;color:rgba(255,255,255,0.3);margin-bottom:16px">Detected: {', '.join(result.detected_metrics) or 'None'}</div>
    """, unsafe_allow_html=True)

    # ── Score + Stats Row ──────────────────────────────────────────────────────
    col_gauge, col_stats = st.columns([1, 2])

    with col_gauge:
        st.plotly_chart(make_gauge(result.score), use_container_width=True, config={'displayModeBar': False})

    with col_stats:
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.markdown(f'<div class="metric-card"><div class="value" style="color:#EF4444">{result.critical_count}</div><div class="label">Critical</div></div>', unsafe_allow_html=True)
        with r2:
            st.markdown(f'<div class="metric-card"><div class="value" style="color:#F59E0B">{result.warning_count}</div><div class="label">Warnings</div></div>', unsafe_allow_html=True)
        with r3:
            st.markdown(f'<div class="metric-card"><div class="value" style="color:#10B981">{result.pass_count}</div><div class="label">Passing</div></div>', unsafe_allow_html=True)
        with r4:
            st.markdown(f'<div class="metric-card"><div class="value" style="color:#60A5FA">{result.quick_win_count}</div><div class="label">Quick Wins</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(make_findings_bar(result), use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # ── Tabs ───────────────────────────────────────────────────────────────────
    manual_checks = [f for f in result.findings if f.status == 'not_applicable']
    manual_badge = f" ({len(manual_checks)})" if manual_checks else ""
    tab_findings, tab_summary, tab_manual, tab_data = st.tabs(["🔍 Findings", "📋 Summary", f"👁 Manual Checks{manual_badge}", "📄 Raw Data"])

    with tab_findings:
        # Filter bar
        filter_col1, filter_col2 = st.columns([3, 1])
        with filter_col1:
            filter_opt = st.radio(
                "Filter",
                ["All", "🔴 Critical", "🟡 Warning", "🟢 Pass", "⚡ Quick Wins"],
                horizontal=True,
                label_visibility="collapsed",
            )
        with filter_col2:
            csv_bytes = export_findings_csv(result)
            st.download_button(
                "⬇ Export CSV",
                data=csv_bytes,
                file_name=f"audit_{channel_id}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime='text/csv',
            )

        # Apply filter
        filtered = []
        for f in result.findings:
            if filter_opt == "All" and f.status != 'not_applicable':
                filtered.append(f)
            elif filter_opt == "🔴 Critical" and f.status == 'fail' and f.severity == 'critical':
                filtered.append(f)
            elif filter_opt == "🟡 Warning" and f.status == 'fail' and f.severity == 'warning':
                filtered.append(f)
            elif filter_opt == "🟢 Pass" and f.status == 'pass':
                filtered.append(f)
            elif filter_opt == "⚡ Quick Wins" and f.status == 'fail' and f.quick_win:
                filtered.append(f)

        if not filtered:
            st.info("No findings match this filter.")
        else:
            # Sort: critical first, then warning, then pass
            order = {'critical': 0, 'warning': 1, 'pass': 2, 'not_applicable': 3}
            filtered.sort(key=lambda f: order.get(f.severity if f.status != 'not_applicable' else 'not_applicable', 3))
            for f in filtered:
                render_finding(f)

    with tab_summary:
        s1, s2 = st.columns(2)

        with s1:
            if result.summary_anomalies:
                st.markdown('<div class="section-header">🔴 Anomalies & Critical Issues</div>', unsafe_allow_html=True)
                for item in result.summary_anomalies:
                    st.markdown(f'<div style="font-size:0.82rem;color:rgba(255,255,255,0.65);padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)">⚠ {item}</div>', unsafe_allow_html=True)
            else:
                st.success("No critical anomalies detected.")

            st.markdown("<br>", unsafe_allow_html=True)

            if result.summary_quick_wins:
                st.markdown('<div class="section-header">⚡ Low-Hanging Fruit (Quick Wins)</div>', unsafe_allow_html=True)
                for item in result.summary_quick_wins:
                    st.markdown(f'<div style="font-size:0.82rem;color:rgba(255,255,255,0.65);padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)">⚡ {item}</div>', unsafe_allow_html=True)

        with s2:
            if result.summary_worked:
                st.markdown('<div class="section-header">🟢 What\'s Working Well</div>', unsafe_allow_html=True)
                for item in result.summary_worked:
                    st.markdown(f'<div style="font-size:0.82rem;color:rgba(255,255,255,0.65);padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)">✓ {item}</div>', unsafe_allow_html=True)
            else:
                st.warning("No passing checks detected — review your data columns.")

            st.markdown("<br>", unsafe_allow_html=True)

            if result.summary_improvements:
                st.markdown('<div class="section-header">🟡 Areas to Improve</div>', unsafe_allow_html=True)
                for item in result.summary_improvements[:6]:  # Top 6
                    st.markdown(f'<div style="font-size:0.82rem;color:rgba(255,255,255,0.65);padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)">→ {item}</div>', unsafe_allow_html=True)

    with tab_manual:
        st.markdown("""
        <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);border-radius:10px;padding:16px;margin-bottom:16px">
            <div style="font-size:0.9rem;font-weight:700;color:#F59E0B;margin-bottom:6px">👁 Platform-Level Checks — Cannot Be Auto-Verified</div>
            <div style="font-size:0.78rem;color:rgba(255,255,255,0.55);line-height:1.6">
                These checks <strong>require you to log into the ad platform directly</strong>. They cannot be assessed from a CSV export alone.<br>
                Work through each item below and tick it off as you verify it inside the platform.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not manual_checks:
            st.success("No manual checks required for this channel.")
        else:
            # Group by category
            from collections import defaultdict
            by_cat = defaultdict(list)
            for f in manual_checks:
                by_cat[f.category].append(f)

            total = len(manual_checks)
            done_count = 0

            for cat, items in by_cat.items():
                st.markdown(f'<div class="section-header">{cat}</div>', unsafe_allow_html=True)
                for f in items:
                    sev_color = '#EF4444' if f.severity == 'critical' else '#F59E0B'
                    sev_label = '🔴 Critical' if f.severity == 'critical' else '🟡 Warning'
                    checked = st.checkbox(
                        f"{sev_label} — **{f.rule.name}**",
                        key=f"manual_{f.rule_id}",
                        help=f.rule.recommendation,
                    )
                    if checked:
                        done_count += 1
                    if not checked:
                        st.markdown(
                            f'<div style="margin:-8px 0 10px 28px;font-size:0.76rem;color:rgba(255,255,255,0.45);line-height:1.5">'
                            f'{f.rule.description}<br>'
                            f'<span style="color:#60A5FA">→ {f.rule.recommendation}</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

            st.markdown("<br>", unsafe_allow_html=True)
            progress = done_count / total if total > 0 else 0
            st.progress(progress, text=f"Platform review progress: {done_count} of {total} checks completed")

    with tab_data:
        st.markdown('<div class="section-header">Uploaded Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df_input, use_container_width=True)
        st.caption(f"{len(df_input)} rows × {len(df_input.columns)} columns")
