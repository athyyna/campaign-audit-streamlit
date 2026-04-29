# Campaign Best Practice Auditor — Streamlit App

> Upload any campaign report CSV/XLSX and instantly surface anomalies, quick wins, and what's working — across 7 ad channels.

## Channels Supported

| Channel | Auto-detected from |
|---|---|
| 🔍 Google Search | `Quality Score`, `Search Impression Share` columns |
| ▶️ YouTube Ads | `View Rate`, `CPV`, `Video Views` columns |
| ⚡ Performance Max | `Asset Group`, `ROAS`, `Conversions` columns |
| 📡 DV360 Programmatic | `Viewability`, `Insertion Order` columns |
| 💼 LinkedIn Ads | `CPL`, `Leads`, `Sponsored Content` columns |
| 📘 Meta (Facebook/IG) | `Frequency` + `Reach` columns |
| 🎯 Demand Gen | `Demand Gen`, `Discovery` columns |

## What the Audit Checks

- **Performance**: CTR, VTR, View Rate vs. channel benchmarks
- **Efficiency**: CPC, CPM, CPA, CPL, ROAS vs. industry benchmarks
- **Audience**: Frequency caps and fatigue signals
- **Quality**: Viewability (DV360), Quality Score (Google Search)
- **Setup**: Conversion volume for Smart Bidding learning phase

## Severity Levels

| Level | Meaning |
|---|---|
| 🔴 Critical | Fix immediately — significant budget waste or performance risk |
| 🟡 Warning | Address soon — below benchmark but not urgent |
| 🟢 Pass | Within acceptable range |
| ⚡ Quick Win | High-impact, low-effort fix |

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploying to Streamlit Cloud

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as the entry point
4. Deploy — no secrets or API keys required

## File Structure

```
app.py               # Main Streamlit UI
audit_engine.py      # CSV parser, metric aggregation, scoring logic
best_practices.py    # All audit rules, benchmarks, channel configs, demo data
requirements.txt     # Python dependencies
README.md            # This file
```

## KPI Benchmarks Used

| Channel | CTR | CPM | CPA/CPL | Frequency |
|---|---|---|---|---|
| Google Search | 3–6% | $10–15 | $20–40 | — |
| YouTube | 0.5–2% | $5–12 | — | 2–5/wk |
| Performance Max | 1–3% | $8–15 | $25–50 | — |
| DV360 | 0.1–0.35% | $2–8 | — | 3–7/wk |
| LinkedIn | 0.4–1.0% | $20–50 | $50–150 | 1–4 |
| Meta | 1–3% | $8–20 | $10–50 | 1–3 |
| Demand Gen | 0.5–2% | $10–18 | $20–80 | 2–5 |

*Sources: Google Ads Help, Meta Business, LinkedIn Marketing Solutions, industry benchmarks 2024–2025*

---
*Co-built by Athena & Manus · Best practices: 2024–2025*
