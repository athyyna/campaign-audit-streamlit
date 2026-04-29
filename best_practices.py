"""
Campaign Best Practice Auditor — Best Practices Knowledge Base
7 channels: Google Search, YouTube, Performance Max, DV360, LinkedIn, Meta, Demand Gen
Source: Google Ads Help, Meta Business, LinkedIn Marketing Solutions, industry benchmarks 2024-2025
"""

from dataclasses import dataclass, field
from typing import Optional

# ─── Data Structures ──────────────────────────────────────────────────────────

@dataclass
class AuditRule:
    id: str
    channel: str
    category: str
    name: str
    description: str
    metric: Optional[str]
    check_type: str  # 'threshold' | 'presence'
    threshold: Optional[float] = None
    threshold_direction: Optional[str] = None  # 'below' | 'above'
    benchmark_label: Optional[str] = None
    severity: str = 'warning'  # 'critical' | 'warning' | 'pass'
    recommendation: str = ''
    quick_win: bool = False


@dataclass
class ChannelConfig:
    id: str
    name: str
    icon: str
    color: str
    metrics: list = field(default_factory=list)


# ─── Channel Definitions ──────────────────────────────────────────────────────

CHANNELS = [
    ChannelConfig('google_search', 'Google Search',      '🔍', '#4285F4', ['CTR','CPC','CPM','CPA','CVR','Quality Score','Impressions','Clicks','Conversions','Cost','ROAS']),
    ChannelConfig('youtube',       'YouTube Ads',         '▶️',  '#FF0000', ['CTR','CPM','CPC','VTR','CPV','Impressions','Views','Clicks','Cost','Frequency']),
    ChannelConfig('pmax',          'Performance Max',     '⚡',  '#34A853', ['CTR','CPC','CPM','CPA','ROAS','Conversions','Cost','Impressions']),
    ChannelConfig('dv360',         'DV360 Programmatic',  '📡',  '#FBBC04', ['CTR','CPM','CPC','VTR','Viewability','Impressions','Clicks','Cost','Frequency']),
    ChannelConfig('linkedin',      'LinkedIn Ads',        '💼',  '#0A66C2', ['CTR','CPM','CPC','CPL','Impressions','Clicks','Leads','Cost','Frequency']),
    ChannelConfig('meta',          'Meta (Facebook/IG)',  '📘',  '#1877F2', ['CTR','CPM','CPC','CPL','ROAS','Frequency','Reach','Impressions','Clicks','Conversions','Cost','VTR','CPA']),
    ChannelConfig('demand_gen',    'Demand Gen',          '🎯',  '#9C27B0', ['CTR','CPM','CPC','CPL','VTR','Impressions','Clicks','Conversions','Cost','Frequency']),
]

CHANNEL_MAP = {c.id: c for c in CHANNELS}

# ─── Severity Config ──────────────────────────────────────────────────────────

SEVERITY_CONFIG = {
    'critical':    {'label': '🔴 Critical',    'color': '#EF4444'},
    'warning':     {'label': '🟡 Warning',     'color': '#F59E0B'},
    'pass':        {'label': '🟢 Pass',        'color': '#10B981'},
    'opportunity': {'label': '🔵 Opportunity', 'color': '#3B82F6'},
}

# ─── Audit Rules ──────────────────────────────────────────────────────────────

AUDIT_RULES = [

    # ── GOOGLE SEARCH ──────────────────────────────────────────────────────────
    AuditRule(
        id='gs_ctr_critical', channel='google_search', category='Performance',
        name='Critical CTR Drop',
        description='CTR is below 1.5% — severe creative fatigue or targeting mismatch.',
        metric='CTR', check_type='threshold', threshold=1.5, threshold_direction='below',
        benchmark_label='Benchmark: 3–6%', severity='critical',
        recommendation='Pause underperforming ads. Refresh ad copy and headlines. Audit negative keyword list.',
        quick_win=False,
    ),
    AuditRule(
        id='gs_ctr_low', channel='google_search', category='Performance',
        name='Low Search CTR',
        description='CTR is below 3% — below recommended minimum for Search campaigns.',
        metric='CTR', check_type='threshold', threshold=3.0, threshold_direction='below',
        benchmark_label='3–6% (Search)', severity='warning',
        recommendation='Review ad copy relevance, improve headline-keyword alignment, test stronger CTAs. Aim for Ad Strength "Good" or "Excellent".',
        quick_win=True,
    ),
    AuditRule(
        id='gs_cpa_spike', channel='google_search', category='Efficiency',
        name='CPA Spike',
        description='CPA exceeds $50 — significantly above the $20–40 benchmark.',
        metric='CPA', check_type='threshold', threshold=50.0, threshold_direction='above',
        benchmark_label='$20–40 (avg)', severity='critical',
        recommendation='Switch to Target CPA bidding. Check landing page CVR. Audit negative keywords.',
        quick_win=False,
    ),
    AuditRule(
        id='gs_cvr_low', channel='google_search', category='Efficiency',
        name='Low Conversion Rate',
        description='CVR is below 2.8% — landing page or targeting issues likely.',
        metric='CVR', check_type='threshold', threshold=2.8, threshold_direction='below',
        benchmark_label='2.8–7% (Search)', severity='warning',
        recommendation='Audit landing page speed (<3s), relevance to ad copy, and CTA clarity. A/B test landing pages.',
        quick_win=True,
    ),
    AuditRule(
        id='gs_quality_score', channel='google_search', category='Quality',
        name='Low Quality Score',
        description='Quality Score below 6 — poor ad relevance, CTR, or landing page experience.',
        metric='Quality Score', check_type='threshold', threshold=6.0, threshold_direction='below',
        benchmark_label='7–10 (target)', severity='warning',
        recommendation='Improve keyword-to-ad-copy alignment. Add keyword in at least one headline. Optimize landing page relevance.',
        quick_win=True,
    ),

    # ── YOUTUBE ────────────────────────────────────────────────────────────────
    AuditRule(
        id='yt_vtr_low', channel='youtube', category='Creative',
        name='Low View-Through Rate',
        description='VTR below 15% — viewers are skipping early. Hook is not compelling.',
        metric='VTR', check_type='threshold', threshold=15.0, threshold_direction='below',
        benchmark_label='>15% (skippable)', severity='warning',
        recommendation='Strengthen the first 5 seconds. Lead with a problem, bold visual, or direct question. Avoid logo-first openings.',
        quick_win=False,
    ),
    AuditRule(
        id='yt_frequency_high', channel='youtube', category='Audience',
        name='High Ad Frequency',
        description='Frequency exceeds 5/week — significant ad fatigue risk.',
        metric='Frequency', check_type='threshold', threshold=5.0, threshold_direction='above',
        benchmark_label='2–5/week (target)', severity='warning',
        recommendation='Apply frequency caps (3–5/week). Expand audience or refresh creative.',
        quick_win=True,
    ),
    AuditRule(
        id='yt_ctr_low', channel='youtube', category='Performance',
        name='Low YouTube CTR',
        description='CTR below 0.5% — viewers are not clicking through.',
        metric='CTR', check_type='threshold', threshold=0.5, threshold_direction='below',
        benchmark_label='0.5–2% (YouTube)', severity='warning',
        recommendation='Add stronger CTAs in video and as overlay cards. Review targeting for high-intent audiences.',
        quick_win=True,
    ),
    AuditRule(
        id='yt_cpm_high', channel='youtube', category='Efficiency',
        name='High CPM',
        description='CPM exceeds $15 — above YouTube average.',
        metric='CPM', check_type='threshold', threshold=15.0, threshold_direction='above',
        benchmark_label='$5–12 (YouTube avg)', severity='warning',
        recommendation='Broaden audience targeting. Test bumper vs. skippable formats. Review placement targeting.',
        quick_win=True,
    ),

    # ── PERFORMANCE MAX ────────────────────────────────────────────────────────
    AuditRule(
        id='pmax_low_roas', channel='pmax', category='Efficiency',
        name='Low ROAS',
        description='ROAS below 3x — PMax is not generating sufficient return.',
        metric='ROAS', check_type='threshold', threshold=3.0, threshold_direction='below',
        benchmark_label='3–8x (target)', severity='critical',
        recommendation='Review audience signals — add customer match lists and high-intent remarketing. Ensure conversion tracking is set to bottom-funnel events.',
        quick_win=False,
    ),
    AuditRule(
        id='pmax_learning', channel='pmax', category='Setup',
        name='Insufficient Conversions for Learning',
        description='Fewer than 50 conversions in 30 days — Smart Bidding cannot optimize.',
        metric='Conversions', check_type='threshold', threshold=50.0, threshold_direction='below',
        benchmark_label='50+ conv/month (min)', severity='warning',
        recommendation='Start with Maximize Conversions (no Target CPA) until 50+ conversions. Avoid frequent changes during learning phase.',
        quick_win=False,
    ),
    AuditRule(
        id='pmax_ctr_low', channel='pmax', category='Performance',
        name='Low PMax CTR',
        description='CTR below 1% — asset groups may lack relevance or variety.',
        metric='CTR', check_type='threshold', threshold=1.0, threshold_direction='below',
        benchmark_label='1–3% (PMax)', severity='warning',
        recommendation='Add more headline and description variations. Ensure assets include lifestyle images, not just product shots.',
        quick_win=True,
    ),

    # ── DV360 ──────────────────────────────────────────────────────────────────
    AuditRule(
        id='dv360_viewability_low', channel='dv360', category='Quality',
        name='Low Viewability Rate',
        description='Viewability below 70% — ads are not being seen, wasting budget.',
        metric='Viewability', check_type='threshold', threshold=70.0, threshold_direction='below',
        benchmark_label='70–90% (MRC standard)', severity='critical',
        recommendation='Apply Active View targeting. Use PMP deals for premium inventory. Review placement exclusions.',
        quick_win=False,
    ),
    AuditRule(
        id='dv360_ctr_low', channel='dv360', category='Performance',
        name='Low Display CTR',
        description='CTR below 0.1% — display ads are not driving engagement.',
        metric='CTR', check_type='threshold', threshold=0.1, threshold_direction='below',
        benchmark_label='0.1–0.35% (display)', severity='warning',
        recommendation='Refresh creative assets. Test animated vs. static. Review audience segments — use in-market or custom intent.',
        quick_win=True,
    ),
    AuditRule(
        id='dv360_frequency_high', channel='dv360', category='Audience',
        name='High Programmatic Frequency',
        description='Frequency exceeds 7/week — significant ad fatigue risk.',
        metric='Frequency', check_type='threshold', threshold=7.0, threshold_direction='above',
        benchmark_label='3–7/week (programmatic)', severity='warning',
        recommendation='Set frequency caps at insertion order or line item level. Expand audience pool or rotate creatives.',
        quick_win=True,
    ),
    AuditRule(
        id='dv360_cpm_high', channel='dv360', category='Efficiency',
        name='High Programmatic CPM',
        description='CPM exceeds $8 — above efficient range for programmatic display.',
        metric='CPM', check_type='threshold', threshold=8.0, threshold_direction='above',
        benchmark_label='$2–8 (programmatic display)', severity='warning',
        recommendation='Review bid strategies. Test open auction vs. PMP pricing. Broaden geo or audience targeting.',
        quick_win=True,
    ),

    # ── LINKEDIN ───────────────────────────────────────────────────────────────
    AuditRule(
        id='li_ctr_low', channel='linkedin', category='Performance',
        name='Low LinkedIn CTR',
        description='CTR below 0.4% — below LinkedIn benchmark for Sponsored Content.',
        metric='CTR', check_type='threshold', threshold=0.4, threshold_direction='below',
        benchmark_label='0.4–1.0% (LinkedIn)', severity='warning',
        recommendation='Test different ad formats (Single Image vs. Carousel vs. Video). Personalize copy for the target audience. Use strong value propositions in the first line.',
        quick_win=True,
    ),
    AuditRule(
        id='li_cpl_high', channel='linkedin', category='Efficiency',
        name='High Cost Per Lead',
        description='CPL exceeds $150 — above efficient range for LinkedIn.',
        metric='CPL', check_type='threshold', threshold=150.0, threshold_direction='above',
        benchmark_label='$50–150 (B2B LinkedIn)', severity='warning',
        recommendation='Narrow to highest-intent segments. Test Lead Gen Forms vs. landing page. Review offer — gated content outperforms generic CTAs.',
        quick_win=False,
    ),
    AuditRule(
        id='li_frequency_high', channel='linkedin', category='Audience',
        name='High LinkedIn Frequency',
        description='Frequency exceeds 4 — LinkedIn audiences are smaller, fatigue sets in faster.',
        metric='Frequency', check_type='threshold', threshold=4.0, threshold_direction='above',
        benchmark_label='1–4 (LinkedIn)', severity='warning',
        recommendation='Expand audience (broaden job titles, industries, seniority). Rotate creatives every 2–3 weeks.',
        quick_win=True,
    ),
    AuditRule(
        id='li_cpm_high', channel='linkedin', category='Efficiency',
        name='High LinkedIn CPM',
        description='CPM exceeds $50 — significantly above efficient range.',
        metric='CPM', check_type='threshold', threshold=50.0, threshold_direction='above',
        benchmark_label='$20–50 (LinkedIn)', severity='warning',
        recommendation='Broaden audience targeting. Test Max Delivery vs. Cost Cap bidding. Review audience overlap.',
        quick_win=True,
    ),

    # ── META ───────────────────────────────────────────────────────────────────
    AuditRule(
        id='meta_frequency_critical', channel='meta', category='Audience',
        name='Critical Ad Frequency',
        description='Frequency exceeds 4.0 — severe creative fatigue on Meta.',
        metric='Frequency', check_type='threshold', threshold=4.0, threshold_direction='above',
        benchmark_label='1–3 (Meta target)', severity='critical',
        recommendation='Pause and refresh creative immediately. Expand audience size. Rotate between 3–5 creative variants per ad set.',
        quick_win=True,
    ),
    AuditRule(
        id='meta_frequency_warning', channel='meta', category='Audience',
        name='Elevated Ad Frequency',
        description='Frequency exceeds 3.0 — early signal of creative fatigue on Meta.',
        metric='Frequency', check_type='threshold', threshold=3.0, threshold_direction='above',
        benchmark_label='1–3 (Meta target)', severity='warning',
        recommendation='Plan creative refresh. Implement frequency caps. Rotate between creative variants.',
        quick_win=True,
    ),
    AuditRule(
        id='meta_ctr_low', channel='meta', category='Performance',
        name='Low Meta CTR',
        description='CTR (Link) below 1% — ads are not compelling enough to drive clicks.',
        metric='CTR', check_type='threshold', threshold=1.0, threshold_direction='below',
        benchmark_label='1–3% (Meta Link CTR)', severity='warning',
        recommendation='Test different creative formats (video vs. static vs. carousel). Improve hook in first 3 seconds. Align copy with audience pain points.',
        quick_win=True,
    ),
    AuditRule(
        id='meta_cpm_high', channel='meta', category='Efficiency',
        name='High Meta CPM',
        description='CPM exceeds $20 — audience saturation or competitive pressure.',
        metric='CPM', check_type='threshold', threshold=20.0, threshold_direction='above',
        benchmark_label='$8–20 (Meta avg)', severity='warning',
        recommendation='Broaden audience targeting. Test Advantage+ audience. Review campaign objective.',
        quick_win=True,
    ),
    AuditRule(
        id='meta_roas_low', channel='meta', category='Efficiency',
        name='Low ROAS',
        description='ROAS below 2x — Meta campaigns not generating sufficient return.',
        metric='ROAS', check_type='threshold', threshold=2.0, threshold_direction='below',
        benchmark_label='2–6x (Meta target)', severity='critical',
        recommendation='Review audience quality and creative relevance. Ensure pixel fires correctly on all conversion events. Test Advantage+ Shopping.',
        quick_win=False,
    ),
    AuditRule(
        id='meta_cpl_high', channel='meta', category='Efficiency',
        name='High Cost Per Lead',
        description='CPL exceeds $50 — above efficient range for Meta lead generation.',
        metric='CPL', check_type='threshold', threshold=50.0, threshold_direction='above',
        benchmark_label='$10–50 (Meta leads)', severity='warning',
        recommendation='Test Instant Forms vs. landing page. Simplify lead form (fewer fields). Use Lookalike audiences based on existing customers.',
        quick_win=True,
    ),

    # ── DEMAND GEN ─────────────────────────────────────────────────────────────
    AuditRule(
        id='dg_ctr_low', channel='demand_gen', category='Performance',
        name='Low Demand Gen CTR',
        description='CTR below 0.5% — Demand Gen ads not driving sufficient engagement.',
        metric='CTR', check_type='threshold', threshold=0.5, threshold_direction='below',
        benchmark_label='0.5–2% (Demand Gen)', severity='warning',
        recommendation='Test different creative formats (video vs. image). Ensure audience signals include high-intent custom segments. Refresh creative every 3–4 weeks.',
        quick_win=True,
    ),
    AuditRule(
        id='dg_frequency_high', channel='demand_gen', category='Audience',
        name='High Demand Gen Frequency',
        description='Frequency exceeds 5 — audiences are seeing the same ad too often.',
        metric='Frequency', check_type='threshold', threshold=5.0, threshold_direction='above',
        benchmark_label='2–5 (Demand Gen)', severity='warning',
        recommendation='Expand audience signals. Use lookalike segments (transitioning to signal mode in 2026). Rotate creative assets.',
        quick_win=True,
    ),
    AuditRule(
        id='dg_cpl_high', channel='demand_gen', category='Efficiency',
        name='High Demand Gen CPL',
        description='CPL exceeds $80 — Demand Gen not efficiently generating leads.',
        metric='CPL', check_type='threshold', threshold=80.0, threshold_direction='above',
        benchmark_label='$20–80 (Demand Gen)', severity='warning',
        recommendation='Prioritize custom intent audiences over broad interest targeting. Test different landing pages. Verify conversion tracking.',
        quick_win=False,
    ),
    AuditRule(
        id='dg_vtr_low', channel='demand_gen', category='Creative',
        name='Low Video View Rate',
        description='VTR below 20% — creative is not retaining viewers.',
        metric='VTR', check_type='threshold', threshold=20.0, threshold_direction='below',
        benchmark_label='20–40% (Demand Gen video)', severity='warning',
        recommendation='Lead with a strong hook in the first 3 seconds. Use native-feeling content. Test shorter formats (15s vs. 30s).',
        quick_win=False,
    ),
]

# ─── Metric Column Aliases ────────────────────────────────────────────────────
# Maps common CSV column names → our canonical metric names

METRIC_ALIASES = {
    'ctr': 'CTR', 'click_through_rate': 'CTR', 'click_thru_rate': 'CTR',
    'cpc': 'CPC', 'cost_per_click': 'CPC', 'avg_cpc': 'CPC', 'average_cpc': 'CPC',
    'cpm': 'CPM', 'cost_per_thousand': 'CPM', 'cost_per_mille': 'CPM',
    'cpa': 'CPA', 'cost_per_acquisition': 'CPA', 'cost_per_conversion': 'CPA',
    'cpl': 'CPL', 'cost_per_lead': 'CPL',
    'cvr': 'CVR', 'conversion_rate': 'CVR', 'conv_rate': 'CVR',
    'roas': 'ROAS', 'return_on_ad_spend': 'ROAS',
    'vtr': 'VTR', 'view_through_rate': 'VTR', 'view_rate': 'VTR', 'video_view_rate': 'VTR',
    'frequency': 'Frequency', 'avg_frequency': 'Frequency',
    'viewability': 'Viewability', 'viewable_rate': 'Viewability',
    'quality_score': 'Quality Score',
    'impressions': 'Impressions', 'clicks': 'Clicks',
    'conversions': 'Conversions', 'cost': 'Cost', 'spend': 'Cost', 'amount_spent': 'Cost',
    'views': 'Views', 'video_views': 'Views',
    'cpv': 'CPV', 'cost_per_view': 'CPV',
    'reach': 'Reach',
    'campaign_name': 'Campaign Name', 'campaign': 'Campaign Name',
    'ad_set_name': 'Ad Set Name', 'adset_name': 'Ad Set Name', 'ad_group': 'Ad Set Name',
}

# ─── Demo Data ────────────────────────────────────────────────────────────────

DEMO_DATA = {
    'google_search': {
        'headers': ['Campaign Name', 'Impressions', 'Clicks', 'CTR', 'CPC', 'Cost', 'Conversions', 'CVR', 'CPA', 'Quality Score'],
        'rows': [
            ['Brand - Search',       45000,  2250, 5.0,  1.20,  2700,  180, 8.0,  15.00, 9],
            ['Non-Brand - Search',  120000,  1800, 1.5,  3.80,  6840,   45, 2.5, 152.00, 5],
            ['Competitor - Search',  30000,   300, 1.0,  5.20,  1560,   12, 4.0, 130.00, 4],
        ]
    },
    'meta': {
        'headers': ['Campaign Name', 'Impressions', 'Reach', 'Clicks', 'CTR', 'CPM', 'CPC', 'Cost', 'Frequency', 'Conversions', 'CPA', 'ROAS'],
        'rows': [
            ['Awareness - Q1',   500000, 180000, 3500, 0.7,  8.50, 1.21, 4250, 2.8,  85,  50.00, 3.2],
            ['Retargeting - Q1', 120000,  25000, 2400, 2.0, 22.00, 1.10, 2640, 4.8, 120,  22.00, 5.8],
            ['Conversion - Q1',  250000,  95000, 1250, 0.5, 25.00, 5.00, 6250, 2.6,  62, 100.80, 1.8],
        ]
    },
    'youtube': {
        'headers': ['Campaign Name', 'Impressions', 'Views', 'CTR', 'CPM', 'CPV', 'VTR', 'Cost', 'Frequency'],
        'rows': [
            ['YouTube - Awareness',   800000, 200000, 0.8,  9.50, 0.038, 25.0, 7600, 3.2],
            ['YouTube - Retargeting', 150000,  30000, 1.5, 14.00, 0.070, 20.0, 2100, 6.2],
        ]
    },
    'linkedin': {
        'headers': ['Campaign Name', 'Impressions', 'Clicks', 'CTR', 'CPM', 'CPC', 'Cost', 'Leads', 'CPL', 'Frequency'],
        'rows': [
            ['Lead Gen - IT DMs',     85000, 255, 0.3, 45.00, 15.00, 3825, 22, 173.86, 3.5],
            ['Awareness - C-Suite',  120000, 600, 0.5, 38.00,  7.60, 4560, 18, 253.33, 5.2],
        ]
    },
    'dv360': {
        'headers': ['Campaign Name', 'Impressions', 'Clicks', 'CTR', 'CPM', 'Cost', 'Viewability', 'Frequency'],
        'rows': [
            ['DV360 - Display', 2000000, 1800, 0.09, 3.20, 6400, 65.0, 8.5],
            ['DV360 - Video',    500000,  750, 0.15, 7.50, 3750, 72.0, 4.2],
        ]
    },
    'pmax': {
        'headers': ['Campaign Name', 'Impressions', 'Clicks', 'CTR', 'CPC', 'Cost', 'Conversions', 'ROAS', 'CPA'],
        'rows': [
            ['PMax - All Products', 350000, 5250, 1.5, 1.80, 9450, 315, 4.2, 30.00],
            ['PMax - New Products', 120000,  840, 0.7, 3.50, 2940,  18, 1.8, 163.33],
        ]
    },
    'demand_gen': {
        'headers': ['Campaign Name', 'Impressions', 'Clicks', 'CTR', 'CPM', 'CPC', 'Cost', 'Conversions', 'CPL', 'VTR', 'Frequency'],
        'rows': [
            ['Demand Gen - Q1',        420000, 1680, 0.4, 12.00, 3.00, 5040, 42, 120.00, 18.0, 3.8],
            ['Demand Gen - Retarget',   95000,  760, 0.8, 18.00, 2.25, 1710, 38,  45.00, 28.0, 4.5],
        ]
    },
}
