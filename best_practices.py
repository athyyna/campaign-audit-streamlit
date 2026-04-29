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
    ChannelConfig('tiktok',         'TikTok Ads',          '🎵',  '#010101', ['CTR','CPM','CPC','CPL','VTR','Impressions','Clicks','Conversions','Cost','Frequency']),
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

    # ── GOOGLE ADS — Account & Structural Checks (from ACB Google Ads Audit Checklist) ──
    AuditRule(
        id='gs_auto_tagging', channel='google_search', category='Account Settings',
        name='Auto-Tagging',
        description='Auto-tagging should be enabled so Google Ads can pass gclid parameters to GA4/analytics for accurate attribution.',
        metric=None, check_type='checklist', severity='critical',
        recommendation='Enable auto-tagging in Google Ads account settings. Verify gclid is being captured in GA4.',
        quick_win=True,
    ),
    AuditRule(
        id='gs_enhanced_conversions_leads', channel='google_search', category='Account Settings',
        name='Enhanced Conversions for Leads',
        description='Enhanced Conversions for Leads is OFF. This reduces match rates and attribution accuracy for lead-based campaigns.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Enable Enhanced Conversions for Leads in Google Ads conversion settings. Requires first-party data (email/phone) to be passed at conversion.',
        quick_win=True,
    ),
    AuditRule(
        id='gs_negative_keywords', channel='google_search', category='Targeting & Bidding',
        name='Campaign Negative Keywords',
        description='No negative keywords are applied at the campaign level. Without negatives, budget is wasted on irrelevant queries.',
        metric=None, check_type='checklist', severity='critical',
        recommendation='Add a minimum of 20–50 negative keywords per campaign. Build a shared negative keyword list at account level. Review Search Terms report weekly.',
        quick_win=True,
    ),
    AuditRule(
        id='gs_shared_negative_lists', channel='google_search', category='Targeting & Bidding',
        name='Shared Negative Keyword Lists',
        description='No shared negative keyword lists applied at account level. Account-level negatives prevent wasted spend across all campaigns.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Create shared negative keyword lists in the Shared Library. Apply to all relevant campaigns. Include brand protection, competitor, and irrelevant intent terms.',
        quick_win=True,
    ),
    AuditRule(
        id='gs_ip_exclusions', channel='google_search', category='Targeting & Bidding',
        name='IP Exclusion Lists',
        description='No IP exclusion lists applied. Without IP exclusions, internal traffic and known bot IPs inflate metrics.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Add your office/internal IP addresses to the IP exclusion list. Consider excluding known competitor IPs if identifiable.',
        quick_win=True,
    ),
    AuditRule(
        id='gs_placement_exclusions', channel='google_search', category='Targeting & Bidding',
        name='Placement Exclusion Lists',
        description='No placement exclusion lists applied at account level. Irrelevant or low-quality placements waste budget on Display/PMax.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Build a placement exclusion list in the Shared Library. Exclude mobile apps (Games, Kids), parked domains, and low-quality sites. Apply to all Display/PMax campaigns.',
        quick_win=True,
    ),
    AuditRule(
        id='gs_mobile_app_exclusions', channel='google_search', category='Targeting & Bidding',
        name='Mobile App Exclusion List',
        description='No mobile app exclusion list applied. Mobile app placements (especially games) often generate accidental clicks with no conversion value.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Exclude all mobile app categories under Display Network placements. Use the mobileappcategory:: exclusion in shared placement lists.',
        quick_win=True,
    ),
    AuditRule(
        id='gs_location_targeting', channel='google_search', category='Targeting & Bidding',
        name='Location Targeting Settings',
        description='Campaigns are using interest-based location targeting instead of physical presence. This can serve ads to users outside your target geography.',
        metric=None, check_type='checklist', severity='critical',
        recommendation='Switch location targeting to "Presence: People in or regularly in your targeted locations" — not "Presence or interest". Audit all campaigns.',
        quick_win=True,
    ),
    AuditRule(
        id='gs_customer_list_audience', channel='google_search', category='Targeting & Bidding',
        name='Customer List Audiences',
        description='No customer list audiences are active. Customer Match enables targeting/exclusion of known customers for more efficient spend.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Upload a customer email list via Customer Match. Use for bid adjustments (+20–30% for high-value segments) or exclusions (existing customers from acquisition campaigns).',
        quick_win=False,
    ),
    AuditRule(
        id='gs_sitelinks_minimum', channel='google_search', category='Ads',
        name='Minimum 4 Sitelinks per Campaign',
        description='One or more campaigns have fewer than 4 sitelinks. Google recommends at least 4 sitelinks to maximize ad real estate and CTR.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Add at least 4 sitelinks per campaign. Use distinct destination URLs. Include high-intent pages (Pricing, Contact, Case Studies, Free Trial).',
        quick_win=True,
    ),
    AuditRule(
        id='gs_conversion_tracking', channel='google_search', category='Conversion Tracking',
        name='Conversion Tracking Health',
        description='Verify that conversion tracking is active, primary conversion actions are set, and attribution model is Data-Driven (DDC).',
        metric=None, check_type='checklist', severity='critical',
        recommendation='Audit conversion actions in Google Ads. Ensure at least one primary conversion action fires. Switch attribution model to Data-Driven where eligible (500+ conversions/month).',
        quick_win=False,
    ),
    AuditRule(
        id='gs_bidding_strategy_review', channel='google_search', category='Targeting & Bidding',
        name='Bidding Strategy Diversification',
        description='Only one bidding strategy in use across all campaigns. Consider diversifying strategies to match different campaign goals (awareness vs. conversion).',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Use Target CPA or Target ROAS for conversion campaigns. Use Maximize Clicks or Target Impression Share for brand/awareness. Avoid mixing objectives within a single strategy.',
        quick_win=False,
    ),

    # ── META — Structural Checks (from ACB Meta Ads Audit Checklist) ──────────────
    AuditRule(
        id='meta_advanced_matching', channel='meta', category='Tracking & Attribution',
        name='Advanced Matching Enabled',
        description='Advanced Matching is OFF. This reduces pixel match rates and attribution accuracy. Enabling it improves event matching and reduces CPA.',
        metric=None, check_type='checklist', severity='critical',
        recommendation='Enable Advanced Matching in Events Manager → Pixel Settings. Pass hashed customer data (email, phone, name) via the pixel or CAPI to improve match rates by 10–30%.',
        quick_win=True,
    ),
    AuditRule(
        id='meta_capi', channel='meta', category='Tracking & Attribution',
        name='Conversion API (CAPI) Enabled',
        description='No server-side events detected. CAPI appears inactive. Without CAPI, iOS14+ signal loss significantly underreports conversions.',
        metric=None, check_type='checklist', severity='critical',
        recommendation='Implement Meta Conversions API (CAPI) via direct integration or a partner (Shopify, GTM server-side). Aim for Event Match Quality score of 6+. Deduplicate browser + server events.',
        quick_win=False,
    ),
    AuditRule(
        id='meta_custom_audiences', channel='meta', category='Targeting & Audience',
        name='Custom Audience Targeting',
        description='Less than 75% of ad sets use Custom Audiences. Custom Audiences (website visitors, customer lists, video viewers) are your highest-intent targeting layer.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Build Custom Audiences from: website visitors (30/60/90d), customer email list, video viewers (25%/50%/75%), and Instagram engagers. Apply to at least 75% of ad sets.',
        quick_win=False,
    ),
    AuditRule(
        id='meta_language_targeting', channel='meta', category='Targeting & Audience',
        name='Language Targeting Specified',
        description='One or more ad sets have no language targeting set. Without language targeting, ads may serve to users in the wrong language, reducing relevance and CTR.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Set language targeting on all ad sets to match your ad creative language. For multilingual markets, create separate ad sets per language with tailored copy.',
        quick_win=True,
    ),
    AuditRule(
        id='meta_learning_phase', channel='meta', category='Budget & Bidding',
        name='Learning Phase Health',
        description='One or more ad sets are failing the learning phase (fewer than 50 optimization events in 7 days). Campaigns stuck in learning have unstable CPAs and poor delivery.',
        metric=None, check_type='checklist', severity='critical',
        recommendation='Consolidate ad sets to concentrate conversion volume. Raise budgets to at least 1–2x your target CPA per day. Avoid edits during the first 7 days after launch. Use CBO.',
        quick_win=False,
    ),
    AuditRule(
        id='meta_cost_per_result_goal', channel='meta', category='Budget & Bidding',
        name='Cost per Result Goal',
        description='No ad sets are using a Cost-Per-Result Goal (bid cap or cost cap). Without a goal, Meta optimizes for volume only, which can cause CPA to spike.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Set a Cost Cap or Bid Cap on conversion-focused ad sets. Start at 1.5–2x your historical CPA, then tighten as the algorithm learns. Avoid setting caps too aggressively at launch.',
        quick_win=True,
    ),
    AuditRule(
        id='meta_budget_adequacy', channel='meta', category='Budget & Bidding',
        name='Budget Adequacy vs. Cost Per Result',
        description='One or more campaigns are underfunded relative to their cost per result. If daily spend < CPR, Meta cannot generate even one conversion per day, keeping learning unstable.',
        metric=None, check_type='checklist', severity='critical',
        recommendation='Ensure each campaign daily budget is at least 2-3x the target CPA. Consolidate underfunded campaigns or pause them until budget is available.',
        quick_win=False,
    ),
    AuditRule(
        id='meta_naming_convention', channel='meta', category='Campaign Structure',
        name='Naming Convention Health',
        description='Verify campaign, ad set, and ad naming conventions are consistent and encode key attributes (objective, audience, format, date) for clean reporting.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Adopt a naming convention: [Market]-[Objective]-[Audience]-[Format]-[Date]. Enforce across all campaigns. Use consistent delimiters (hyphens or underscores, not both).',
        quick_win=True,
    ),
    AuditRule(
        id='meta_cbo', channel='meta', category='Budget & Bidding',
        name='Advantage+ Campaign Budget (CBO)',
        description='Verify all conversion campaigns use Advantage+ Campaign Budget (CBO). CBO allocates spend to best-performing ad sets automatically, reducing learning fragmentation.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Switch all conversion campaigns to CBO. Set a campaign-level daily budget. Allow at least 7 days before evaluating performance post-switch.',
        quick_win=True,
    ),
    AuditRule(
        id='meta_ads_per_adset', channel='meta', category='Ads & Creative',
        name='Minimum 5 Ads per Ad Set',
        description='Verify each active ad set has at least 5 ads. Meta needs creative variety to optimize delivery and avoid fatigue.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Maintain 5–10 active ads per ad set across different formats (static, video, carousel). Refresh lowest-performing ads every 2–3 weeks.',
        quick_win=True,
    ),
    AuditRule(
        id='meta_utm_tags', channel='meta', category='Ads & Creative',
        name='URL Tags / UTM Parameters',
        description='Verify all ads have UTM parameters (utm_source, utm_medium, utm_campaign) for GA4/analytics attribution.',
        metric=None, check_type='checklist', severity='critical',
        recommendation='Add UTM parameters to all ad destination URLs. Use a consistent UTM taxonomy. Automate via URL Parameters field in Meta Ads Manager.',
        quick_win=True,
    ),
    AuditRule(
        id='meta_publisher_blocklist', channel='meta', category='Targeting & Audience',
        name='Publisher Block Lists',
        description='Verify publisher block lists are applied to prevent ads from appearing on brand-unsafe content.',
        metric=None, check_type='checklist', severity='warning',
        recommendation='Apply at least one publisher block list in Brand Safety settings. Include known low-quality or brand-unsafe domains. Review quarterly.',
        quick_win=True,
    ),
    # ─── META ENHANCED ────────────────────────────────────────────────────────
    AuditRule(
        id='meta_reels_vtr', channel='meta', category='Creative',
        name='Low Reels VTR',
        description='Reels VTR is below 15% — hook is not retaining viewers past the first 3 seconds.',
        metric='VTR', check_type='threshold',
        threshold=15.0, threshold_direction='below',
        benchmark_label='15–35% (Meta Reels)',
        severity='warning',
        recommendation='Lead with motion, text overlay, or a direct question in the first 3 seconds. Ensure safe zone compliance — keep key content in center 80% of frame. Sound-on strategy required.',
        quick_win=False,
    ),
    AuditRule(
        id='meta_cpa_high', channel='meta', category='Efficiency',
        name='High Meta CPA',
        description='CPA exceeds $60 — above efficient range for Meta conversion campaigns.',
        metric='CPA', check_type='threshold',
        threshold=60.0, threshold_direction='above',
        benchmark_label='$15–60 (Meta conversions)',
        severity='warning',
        recommendation='Review pixel health and attribution window. Enable Advantage+ audience. Ensure ad set has min 50 conversions/week for algorithm stability. Check landing page CVR.',
        quick_win=False,
    ),
    # ─── PMAX ENHANCED ────────────────────────────────────────────────────────
    AuditRule(
        id='pmax_cpa_high', channel='pmax', category='Efficiency',
        name='High PMax CPA',
        description='CPA exceeds $80 — PMax is not converting efficiently. May indicate poor audience signals or asset quality.',
        metric='CPA', check_type='threshold',
        threshold=80.0, threshold_direction='above',
        benchmark_label='$20–80 (PMax avg)',
        severity='warning',
        recommendation='Add Customer Match lists as audience signals. Review asset group ad strength — aim for Excellent. Ensure primary conversion goal is bottom-funnel only.',
        quick_win=False,
    ),
    AuditRule(
        id='pmax_ctr_low', channel='pmax', category='Performance',
        name='Low PMax CTR',
        description='CTR is below 1% — asset groups are not generating compelling ads.',
        metric='CTR', check_type='threshold',
        threshold=1.0, threshold_direction='below',
        benchmark_label='1–4% (PMax)',
        severity='warning',
        recommendation='Diversify headlines — add more unique value propositions. Include a vertical 9:16 video for Shorts/Discovery. Review search themes — add intent-based keywords.',
        quick_win=True,
    ),
    # ─── DEMAND GEN ENHANCED ──────────────────────────────────────────────────
    AuditRule(
        id='dg_new_customer_rate', channel='demand_gen', category='Efficiency',
        name='New Customer Rate Below Benchmark',
        description='Demand Gen should drive 18%+ higher new customer conversions vs. paid media average. If new customer rate is low, existing customers are not being excluded.',
        metric=None, check_type='checklist',
        severity='warning',
        recommendation='Exclude existing customers from acquisition campaigns. Add converter exclusion list (90 day). Demand Gen drives 18% higher new customer share when exclusions are properly configured.',
        quick_win=True,
    ),
    AuditRule(
        id='dg_placement_mix', channel='demand_gen', category='Setup',
        name='Single Placement Only',
        description='Demand Gen value comes from cross-placement coverage (YouTube + Discover + Gmail). Single placement limits reach.',
        metric=None, check_type='checklist',
        severity='warning',
        recommendation='Ensure creative assets cover all 3 placements: horizontal video (YouTube), square image (Discover), and Gmail-compatible format. Include vertical 9:16 for Shorts.',
        quick_win=True,
    ),
    # ─── ACCOUNT-LEVEL ────────────────────────────────────────────────────────
    AuditRule(
        id='acct_smart_bidding_data', channel='google_search', category='Setup',
        name='Insufficient Conversions for Smart Bidding',
        description='Target CPA/ROAS requires min 30–50 conversions/month. Below this threshold, Smart Bidding cannot optimize effectively.',
        metric='Conversions', check_type='threshold',
        threshold=30.0, threshold_direction='below',
        benchmark_label='Min 30–50 conv/month for Target CPA/ROAS',
        severity='critical',
        recommendation='Switch to Maximize Conversions (no target) until 30+ conversions/month are achieved. Do not set Target CPA/ROAS prematurely — it throttles delivery.',
        quick_win=False,
    ),
    AuditRule(
        id='acct_pmax_smart_bidding_data', channel='pmax', category='Setup',
        name='Insufficient Conversions for PMax Target ROAS',
        description='PMax Target ROAS requires min 50 conversions/month. Below this, the algorithm cannot optimize effectively.',
        metric='Conversions', check_type='threshold',
        threshold=50.0, threshold_direction='below',
        benchmark_label='Min 50 conv/month for Target ROAS (PMax)',
        severity='warning',
        recommendation='Use Maximize Conversion Value without a ROAS target until 50+ conversions/month. Avoid changing bid strategy during learning phase (first 2–4 weeks).',
        quick_win=False,
    ),
    # ─── TIKTOK ───────────────────────────────────────────────────────────────
    AuditRule(
        id='tt_ctr_low', channel='tiktok', category='Performance',
        name='Low TikTok CTR',
        description='CTR is below 0.8% — below TikTok benchmark for In-Feed ads.',
        metric='CTR', check_type='threshold',
        threshold=0.8, threshold_direction='below',
        benchmark_label='0.8–1.5% (TikTok In-Feed)',
        severity='warning',
        recommendation='Hook must land in first 2 seconds. Check Creative Center for trending formats in your market. Ensure creative looks native — indistinguishable from organic TikTok content.',
        quick_win=True,
    ),
    AuditRule(
        id='tt_cpm_high', channel='tiktok', category='Efficiency',
        name='High TikTok CPM',
        description='CPM exceeds $12 — above efficient range for TikTok In-Feed ads.',
        metric='CPM', check_type='threshold',
        threshold=12.0, threshold_direction='above',
        benchmark_label='$6–12 (TikTok avg)',
        severity='warning',
        recommendation='Broaden audience targeting (min 5M). Switch to Max Delivery bidding. Review audience overlap between ad groups.',
        quick_win=True,
    ),
    AuditRule(
        id='tt_vvr_low', channel='tiktok', category='Creative',
        name='Low 6s Video View Rate',
        description='VVR (6s) is below 30% — viewers are swiping past before the hook lands.',
        metric='VTR', check_type='threshold',
        threshold=30.0, threshold_direction='below',
        benchmark_label='30–50% (TikTok 6s VVR)',
        severity='critical',
        recommendation='Rework the first 2 seconds. Use text overlay, trending audio, or a bold visual statement. Check TikTok Creative Center for top-performing hooks in your category.',
        quick_win=False,
    ),
    AuditRule(
        id='tt_frequency_high', channel='tiktok', category='Audience',
        name='High TikTok Frequency',
        description='Frequency exceeds 3x/week — TikTok audiences fatigue faster than other platforms.',
        metric='Frequency', check_type='threshold',
        threshold=3.0, threshold_direction='above',
        benchmark_label='2–3x/week (TikTok)',
        severity='warning',
        recommendation='Introduce 5–10 new creatives per month. Expand audience to minimum 5M. Kill creatives with CTR below 0.5%.',
        quick_win=True,
    ),
    AuditRule(
        id='tt_cpl_high', channel='tiktok', category='Efficiency',
        name='High TikTok CPL',
        description='CPL exceeds $25 — above efficient range for TikTok lead generation.',
        metric='CPL', check_type='threshold',
        threshold=25.0, threshold_direction='above',
        benchmark_label='$8–25 (TikTok leads)',
        severity='warning',
        recommendation='Test Spark Ads (boosted organic) vs. standard In-Feed. Review landing page mobile experience. Simplify the conversion flow.',
        quick_win=False,
    ),
    AuditRule(
        id='tt_native_aesthetic', channel='tiktok', category='Creative',
        name='Native Aesthetic Check',
        description='TikTok ads that look like ads (polished, branded, non-native) consistently underperform vs. content that mimics organic TikTok style.',
        metric=None, check_type='checklist',
        severity='warning',
        recommendation='Check TikTok Creative Center weekly for trending formats in your market. Ads should use trending audio, vertical 9:16, text overlays, and creator-style filming. Avoid overly polished brand videos.',
        quick_win=True,
    ),
    AuditRule(
        id='tt_safe_zones', channel='tiktok', category='Creative',
        name='Safe Zone Compliance',
        description='TikTok UI overlays (right-side icons, bottom caption stack) eat ~25% of the visible area. Key content placed outside the center 70% will be obscured.',
        metric=None, check_type='checklist',
        severity='critical',
        recommendation='Keep all key visuals, text, and CTAs within the center 70% of the frame. Avoid bottom 15% (UI overlay) and right side (share/like/comment icons). Test on mobile before launch.',
        quick_win=True,
    ),
    AuditRule(
        id='tt_spark_ads', channel='tiktok', category='Setup',
        name='Spark Ads Not Enabled',
        description='Spark Ads (boosting organic TikTok posts) consistently outperform standard In-Feed ads on CTR and VVR due to social proof (likes, comments, shares).',
        metric=None, check_type='checklist',
        severity='warning',
        recommendation='Identify top-performing organic posts. Authorize them as Spark Ads. Prioritize creator content over brand-produced assets for Spark Ads.',
        quick_win=True,
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
    'tiktok': {
        'headers': ['Campaign Name', 'Impressions', 'Clicks', 'CTR', 'CPM', 'CPC', 'Cost', 'Conversions', 'CPL', 'VTR', 'Frequency'],
        'rows': [
            ['TikTok - Awareness',   1200000, 7200, 0.6,  7.50, 1.25, 9000, 144, 62.50, 22.0, 2.4],
            ['TikTok - Conversion',   280000, 1120, 0.4, 14.00, 3.50, 3920,  56, 70.00, 18.0, 4.2],
            ['TikTok - Spark Ads',    650000, 6500, 1.0,  9.00, 0.90, 5850, 195, 30.00, 35.0, 2.8],
        ]
    },
}
