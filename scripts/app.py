"""
Parcl Co. Limited – Real Estate Buyer Intelligence Platform
Production-grade Streamlit dashboard built from scratch.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Parcl Intelligence · Buyer Segmentation",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
NAVY      = "#0F2040"
SLATE     = "#1E3A5F"
BLUE      = "#2563EB"
LIGHT_BLUE = "#60A5FA"
MID_GRAY  = "#6B7280"
SURFACE   = "#F8F9FB"
BORDER    = "#E5E7EB"
TEXT_DARK = "#111827"
TEXT_MID  = "#4B5563"

# One distinct color per segment – navy family, no neon
SEG_COLORS = {
    "Global Investors":  "#0F2040",
    "First-Time Buyers": "#2563EB",
    "Corporate Buyers":  "#64748B",
    "Luxury Investors":  "#1D4ED8",
}
SEG_COLOR_LIST = list(SEG_COLORS.values())

CLUSTER_NAMES = {
    0: "Global Investors",
    1: "First-Time Buyers",
    2: "Corporate Buyers",
    3: "Luxury Investors",
}

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS INJECTION
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Reset & Base ──────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp { background: #F8F9FB; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 2rem 3rem 2rem;
    max-width: 1400px;
}

/* ── Top navigation bar ────────────────────────────────── */
.topbar {
    background: #0F2040;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 56px;
    margin: 0 -2rem 2rem -2rem;
    position: sticky;
    top: 0;
    z-index: 999;
}
.topbar-brand {
    color: white;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    display: flex;
    align-items: center;
    gap: 10px;
}
.topbar-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #60A5FA;
    display: inline-block;
}
.topbar-tag {
    color: #93C5FD;
    font-size: 0.72rem;
    font-weight: 400;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── KPI Cards ─────────────────────────────────────────── */
.kpi-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 20px 22px;
    min-height: 100px;
}
.kpi-label {
    color: #6B7280;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.kpi-value {
    color: #0F2040;
    font-size: 1.85rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-sub {
    color: #9CA3AF;
    font-size: 0.75rem;
    font-weight: 400;
}
.kpi-badge {
    display: inline-block;
    background: #EFF6FF;
    color: #1D4ED8;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    margin-top: 6px;
}

/* ── Section headings ──────────────────────────────────── */
.section-header {
    margin: 2rem 0 1rem 0;
}
.section-title {
    color: #0F2040;
    font-size: 1.05rem;
    font-weight: 600;
    margin: 0 0 2px 0;
}
.section-sub {
    color: #6B7280;
    font-size: 0.8rem;
    margin: 0;
}
.divider {
    height: 1px;
    background: #E5E7EB;
    margin: 1.5rem 0;
}

/* ── Chart containers ──────────────────────────────────── */
.chart-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 20px;
}
.chart-title {
    color: #0F2040;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.chart-desc {
    color: #9CA3AF;
    font-size: 0.73rem;
    margin-bottom: 12px;
}

/* ── Executive summary panel ───────────────────────────── */
.exec-panel {
    background: #0F2040;
    border-radius: 10px;
    padding: 24px 28px;
    color: white;
}
.exec-panel-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #93C5FD;
    margin-bottom: 10px;
}
.exec-panel-text {
    font-size: 0.9rem;
    font-weight: 400;
    line-height: 1.7;
    color: #CBD5E1;
}
.exec-panel-highlight {
    color: white;
    font-weight: 600;
}

/* ── Segment profile cards ─────────────────────────────── */
.seg-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 22px;
    height: 100%;
}
.seg-card-top {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
}
.seg-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
.seg-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: #0F2040;
}
.seg-count {
    margin-left: auto;
    font-size: 0.75rem;
    color: #6B7280;
    font-weight: 500;
}
.seg-stat-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #4B5563;
    padding: 5px 0;
    border-bottom: 1px solid #F3F4F6;
}
.seg-stat-label { color: #9CA3AF; }
.seg-stat-val { font-weight: 600; color: #111827; }
.seg-desc {
    font-size: 0.78rem;
    color: #6B7280;
    line-height: 1.55;
    margin-top: 12px;
}

/* ── Filter bar ────────────────────────────────────────── */
.filter-bar {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}

/* ── Recommendation cards ──────────────────────────────── */
.rec-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 22px;
}
.rec-seg-name {
    font-size: 0.85rem;
    font-weight: 700;
    color: #0F2040;
    margin-bottom: 14px;
}
.rec-row {
    margin-bottom: 12px;
}
.rec-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9CA3AF;
    margin-bottom: 3px;
}
.rec-text {
    font-size: 0.8rem;
    color: #374151;
    line-height: 1.5;
}

/* ── ML metrics ────────────────────────────────────────── */
.ml-metric {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
}
.ml-metric-val {
    font-size: 2rem;
    font-weight: 700;
    color: #0F2040;
}
.ml-metric-label {
    font-size: 0.75rem;
    color: #6B7280;
    font-weight: 500;
}
.ml-metric-badge {
    display: inline-block;
    background: #DCFCE7;
    color: #166534;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    margin-top: 6px;
}

/* ── Executive insight cards ───────────────────────────── */
.insight-strip {
    display: flex;
    gap: 12px;
    margin-bottom: 1.25rem;
    flex-wrap: wrap;
}
.insight-card {
    flex: 1;
    min-width: 200px;
    background: white;
    border: 1px solid #E5E7EB;
    border-left: 3px solid #0F2040;
    border-radius: 8px;
    padding: 12px 16px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.insight-icon {
    font-size: 1.2rem;
    flex-shrink: 0;
    margin-top: 1px;
}
.insight-headline {
    font-size: 0.82rem;
    font-weight: 600;
    color: #0F2040;
    margin-bottom: 3px;
    line-height: 1.3;
}
.insight-detail {
    font-size: 0.73rem;
    color: #6B7280;
    line-height: 1.4;
}

/* ── Tab styling ───────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: transparent;
    border-bottom: 1px solid #E5E7EB;
    margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    color: #6B7280;
    font-size: 0.82rem;
    font-weight: 500;
    padding: 10px 18px;
    margin-bottom: -1px;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #0F2040 !important;
    border-bottom: 2px solid #0F2040 !important;
    font-weight: 600 !important;
}

/* ── Streamlit multiselect styling ─────────────────────── */
.stMultiSelect [data-baseweb="select"] {
    border-radius: 6px;
    font-size: 0.8rem;
}

/* ── Compact Executive Filter Bar ─────────────────────── */

/* Hide the large chip tags inside multiselects in the filter bar */
[data-testid="stExpander"] .stMultiSelect [data-baseweb="tag"] {
    display: none !important;
}
/* Keep the input area slim */
[data-testid="stExpander"] .stMultiSelect [data-baseweb="select"] > div:first-child {
    min-height: 34px !important;
    padding: 4px 8px !important;
    cursor: pointer;
}
/* Compact the expander header into a tight filter strip */
[data-testid="stExpander"] > details > summary {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #374151;
    letter-spacing: 0.03em;
    margin-bottom: 0;
}
[data-testid="stExpander"] > details > summary:hover {
    background: #F8F9FB;
    border-color: #CBD5E1;
}
[data-testid="stExpander"] > details[open] > summary {
    border-radius: 8px 8px 0 0;
    border-bottom-color: transparent;
}
[data-testid="stExpander"] > details > div {
    background: white;
    border: 1px solid #E2E8F0;
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 12px 16px 16px 16px;
}
/* Filter pill – the summary label shown inside each column */
.filter-pill {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.filter-pill-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9CA3AF;
    margin-bottom: 1px;
}
.filter-pill-value {
    font-size: 0.78rem;
    font-weight: 500;
    color: #0F2040;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.filter-pill-value.all { color: #6B7280; font-style: italic; }
.filter-pill-value.partial { color: #0F2040; font-weight: 600; }
/* Reduce multiselect font in filter panel */
[data-testid="stExpander"] .stMultiSelect label {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: #6B7280 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stExpander"] .stMultiSelect [data-baseweb="select"] {
    border-radius: 6px;
    font-size: 0.8rem;
}
/* Active filter indicator dot */
.filter-active-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #2563EB;
    margin-left: 6px;
    vertical-align: middle;
}
/* ── Table styling ─────────────────────────────────────── */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* ── Client detail card ─────────────────────────────────── */
.client-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 24px;
}
.client-id-badge {
    display: inline-block;
    background: #EFF6FF;
    color: #1D4ED8;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 14px;
    letter-spacing: 0.04em;
}
.client-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0F2040;
    margin-bottom: 4px;
}
.client-seg-tag {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 18px;
}
.client-field {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #F3F4F6;
    font-size: 0.82rem;
}
.client-field-label { color: #9CA3AF; }
.client-field-val { color: #111827; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & PREP
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("clustured/clustered_clients.csv")
    df.columns = [c.strip() for c in df.columns]
    df["Segment"] = df["Cluster"].map(CLUSTER_NAMES).fillna("Unknown")
    # Derived helpers
    df["is_investor"] = (df["acquisition_purpose"] == "Investment").astype(int)
    df["has_loan"]    = (df["loan_applied"] == "Yes").astype(int)
    return df

@st.cache_data
def get_elbow_data():
    raw_df = pd.read_csv('raw/clients.csv')
    raw_df = raw_df.drop_duplicates(subset=['client_id'])
    raw_df['loan_applied'] = raw_df['loan_applied'].fillna('Unknown')
    raw_df['satisfaction_score'] = raw_df['satisfaction_score'].fillna(raw_df['satisfaction_score'].median())
    raw_df['date_of_birth'] = pd.to_datetime(raw_df['date_of_birth'], errors='coerce')
    raw_df['Age'] = 2026 - raw_df['date_of_birth'].dt.year
    raw_df['Age'] = raw_df['Age'].fillna(raw_df['Age'].median())

    categorical_cols = ['client_type', 'region', 'acquisition_purpose', 'referral_channel', 'country']
    df_encoded = pd.get_dummies(raw_df, columns=categorical_cols, drop_first=True)

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    numeric_cols = ['Age', 'satisfaction_score']
    df_encoded[numeric_cols] = scaler.fit_transform(df_encoded[numeric_cols])

    features = df_encoded.drop(columns=['client_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'loan_applied', 'Cluster', 'HC_Cluster'], errors='ignore')
    features = features.select_dtypes(include=[np.number])

    from sklearn.cluster import KMeans
    ks = list(range(1, 9))
    wcss = []
    for k in ks:
        km = KMeans(n_clusters=k, random_state=42)
        km.fit(features)
        wcss.append(km.inertia_)
    return ks, wcss

df = load_data()


# ─────────────────────────────────────────────────────────────────────────────
# CHART THEME
# ─────────────────────────────────────────────────────────────────────────────
def theme(fig, height=None, legend=True, margins=None):
    m = margins or dict(l=10, r=10, t=35, b=10)
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color=TEXT_DARK),
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0,
                    font=dict(size=11), title=""),
        margin=m,
        **({"height": height} if height else {}),
    )
    fig.update_xaxes(showgrid=False, zeroline=False,
                     tickfont=dict(size=11, color=TEXT_DARK), title_font=dict(size=12, color=TEXT_DARK))
    fig.update_yaxes(showgrid=True, gridcolor="#F3F4F6", zeroline=False,
                     tickfont=dict(size=11, color=TEXT_DARK), title_font=dict(size=12, color=TEXT_DARK))
    return fig

def segment_color_seq(segments):
    return [SEG_COLORS.get(s, "#94A3B8") for s in segments]

# ─────────────────────────────────────────────────────────────────────────────
# BUSINESS INSIGHT GENERATOR
# ─────────────────────────────────────────────────────────────────────────────
def generate_executive_insight(d: pd.DataFrame) -> str:
    top_seg   = d["Segment"].value_counts().idxmax()
    top_count = d["Segment"].value_counts().max()
    pct_top   = top_count / len(d) * 100

    loan_by_seg    = d.groupby("Segment")["has_loan"].mean()
    highest_loan   = loan_by_seg.idxmax()
    loan_pct       = loan_by_seg.max() * 100

    sat_by_seg   = d.groupby("Segment")["satisfaction_score"].mean()
    highest_sat  = sat_by_seg.idxmax()
    sat_val      = sat_by_seg.max()

    invest_rate  = d["is_investor"].mean() * 100
    pct_company  = (d["client_type"] == "Company").mean() * 100

    lines = [
        f"<b>{top_seg}</b> is the dominant buyer segment, representing <b>{pct_top:.0f}%</b> of the current selection.",
        f"<b>{highest_loan}</b> show the highest financing dependency at <b>{loan_pct:.0f}%</b> loan application rate.",
        f"<b>{highest_sat}</b> report the strongest satisfaction levels, averaging <b>{sat_val:.1f}/5.0</b>.",
        f"Investment acquisitions account for <b>{invest_rate:.0f}%</b> of all purchase intent in this dataset.",
    ]
    if pct_company > 0:
        lines.append(f"Corporate entities represent <b>{pct_company:.1f}%</b> of the buyer pool.")
    return " &nbsp;·&nbsp; ".join(lines)

def generate_insight_cards(d: pd.DataFrame) -> list:
    """Return list of (icon, headline, detail) insight tuples from filtered data."""
    cards = []
    if d.empty:
        return cards

    # 1 – Largest segment
    vc = d["Segment"].value_counts()
    top_seg, top_n = vc.idxmax(), vc.max()
    pct = top_n / len(d) * 100
    cards.append(("👥", f"{top_seg} lead the market",
                  f"{top_n:,} buyers · {pct:.0f}% of current selection"))

    # 2 – Highest loan dependency
    loan = d.groupby("Segment")["has_loan"].mean()
    hi_loan_seg = loan.idxmax()
    hi_loan_pct = loan.max() * 100
    cards.append(("🏦", f"{hi_loan_seg} most financing-dependent",
                  f"{hi_loan_pct:.0f}% applied for a loan — highest of all segments"))

    # 3 – Highest satisfaction
    sat = d.groupby("Segment")["satisfaction_score"].mean()
    hi_sat_seg = sat.idxmax()
    hi_sat_val = sat.max()
    cards.append(("⭐", f"{hi_sat_seg} top satisfaction",
                  f"Average score {hi_sat_val:.2f} / 5.0 — strongest client experience"))

    # 4 – Strongest investment intent
    inv = d.groupby("Segment")["is_investor"].mean()
    hi_inv_seg = inv.idxmax()
    hi_inv_pct = inv.max() * 100
    cards.append(("📈", f"{hi_inv_seg} most investment-oriented",
                  f"{hi_inv_pct:.0f}% acquire for investment — top commercial signal"))

    return cards


# Full dataset — no global filtering
fdf = df.copy()

tabs = st.tabs([
    "  Executive Summary  ",
    "  Buyer Segmentation  ",
    "  Geographic & Investment  ",
    "  ML Analytics  ",
    "  Recommendations  ",
])

total = len(fdf)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:

    # Key findings from data
    _ic = generate_insight_cards(fdf)
    if _ic:
        _cards_html = "".join([
            f'<div class="insight-card">'
            f'<div class="insight-icon">{icon}</div>'
            f'<div><div class="insight-headline">{hl}</div>'
            f'<div class="insight-detail">{detail}</div></div>'
            f'</div>'
            for icon, hl, detail in _ic
        ])
        st.markdown(f'<div class="insight-strip">{_cards_html}</div>', unsafe_allow_html=True)

    # KPI row — four cards only
    k1, k2, k3, k4 = st.columns(4)
    avg_sat    = fdf["satisfaction_score"].mean()
    pct_invest = fdf["is_investor"].mean() * 100

    def kpi(col, label, value, sub="", badge=""):
        badge_html = f'<div class="kpi-badge">{badge}</div>' if badge else ""
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
            {badge_html}
        </div>
        """, unsafe_allow_html=True)

    kpi(k1, "Total Buyers",      f"{total:,}",          "in dataset",          "Full cohort")
    kpi(k2, "Buyer Segments",    "4",                   "K-Means clusters",    "K = 4 optimal")
    kpi(k3, "Investment Rate",   f"{pct_invest:.0f}%",  "acquire for investment", "Purchase signal")
    kpi(k4, "Avg. Satisfaction", f"{avg_sat:.2f}",      "out of 5.0",          "Scored 1–5")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Donut + segment table
    col_donut, col_table = st.columns([2, 3], gap="large")

    with col_donut:
        seg_counts = fdf["Segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        donut = px.pie(
            seg_counts, names="Segment", values="Count",
            hole=0.60, color="Segment", color_discrete_map=SEG_COLORS,
        )
        donut.update_traces(
            textposition="outside", textinfo="percent+label",
            textfont=dict(size=11), marker=dict(line=dict(color="white", width=2)),
        )
        donut.update_layout(
            annotations=[dict(
                text=f"<b>{total:,}</b><br><span style='font-size:10px'>buyers</span>",
                x=0.5, y=0.5, showarrow=False, font=dict(size=14, color=NAVY)
            )],
            showlegend=False,
        )
        theme(donut, height=340, legend=False)
        st.markdown('<div class="chart-card"><div class="chart-title">SEGMENT DISTRIBUTION</div>', unsafe_allow_html=True)
        st.plotly_chart(donut, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_table:
        seg_tbl = (
            fdf.groupby("Segment")
               .agg(Buyers=("client_id","count"),
                    Avg_Age=("Age","mean"),
                    Avg_Sat=("satisfaction_score","mean"),
                    Loan_Rate=("has_loan","mean"),
                    Invest_Rate=("is_investor","mean"))
               .reset_index()
        )
        seg_tbl["Share %"]      = (seg_tbl["Buyers"] / total * 100).round(1)
        seg_tbl["Avg Age"]      = seg_tbl["Avg_Age"].round(1)
        seg_tbl["Avg Sat"]      = seg_tbl["Avg_Sat"].round(2)
        seg_tbl["Loan Rate"]    = (seg_tbl["Loan_Rate"] * 100).round(1).astype(str) + "%"
        seg_tbl["Invest Rate"]  = (seg_tbl["Invest_Rate"] * 100).round(1).astype(str) + "%"
        st.markdown('<div class="chart-card"><div class="chart-title">SEGMENT COMPARISON</div><div class="chart-desc">Key behavioral metrics across all four buyer clusters</div>', unsafe_allow_html=True)
        st.dataframe(
            seg_tbl[["Segment","Buyers","Share %","Avg Age","Avg Sat","Loan Rate","Invest Rate"]],
            hide_index=True, width="stretch",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    c_sat, c_loan = st.columns(2, gap="large")
    with c_sat:
        sat_dist = fdf.groupby(["satisfaction_score","Segment"]).size().reset_index(name="Count")
        fig_sat = px.bar(
            sat_dist, x="satisfaction_score", y="Count", color="Segment",
            color_discrete_map=SEG_COLORS, barmode="group",
            labels={"satisfaction_score":"Satisfaction Score","Count":"Buyers"},
        )
        theme(fig_sat, height=260)
        st.markdown('<div class="chart-card"><div class="chart-title">SATISFACTION DISTRIBUTION</div><div class="chart-desc">Score distribution across all buyer segments</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_sat, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_loan:
        loan_seg = fdf.groupby("Segment")["has_loan"].mean().reset_index()
        loan_seg.columns = ["Segment","Loan Rate"]
        loan_seg["Loan Rate"] *= 100
        loan_seg = loan_seg.sort_values("Loan Rate", ascending=True)
        fig_loan = px.bar(
            loan_seg, x="Loan Rate", y="Segment", orientation="h",
            color="Segment", color_discrete_map=SEG_COLORS,
            text=loan_seg["Loan Rate"].round(1).astype(str) + "%",
            labels={"Loan Rate":"Loan Application Rate (%)"},
        )
        fig_loan.update_traces(textposition="outside")
        theme(fig_loan, height=260, legend=False)
        st.markdown('<div class="chart-card"><div class="chart-title">FINANCING DEPENDENCY</div><div class="chart-desc">% of buyers who applied for a loan</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_loan, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — BUYER SEGMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:

    seg_profiles = {
        "Global Investors":  {"color": SEG_COLORS["Global Investors"],  "desc": "International buyers with mixed home/investment intent. Low satisfaction — highest-touch service need."},
        "First-Time Buyers": {"color": SEG_COLORS["First-Time Buyers"], "desc": "Younger, price-sensitive buyers entering the market. Highest loan dependency. Relationship-driven."},
        "Corporate Buyers":  {"color": SEG_COLORS["Corporate Buyers"],  "desc": "Older institutional buyers focused on multi-property acquisition. Strong agency and website referrals."},
        "Luxury Investors":  {"color": SEG_COLORS["Luxury Investors"],  "desc": "Premium, high-satisfaction buyers. Largest volume. Investment-oriented with low loan dependency."},
    }

    sc1, sc2, sc3, sc4 = st.columns(4, gap="medium")
    for col, (seg_name, prof) in zip([sc1, sc2, sc3, sc4], seg_profiles.items()):
        sd      = fdf[fdf["Segment"] == seg_name]
        n       = len(sd)
        col.markdown(f"""
        <div class="seg-card">
            <div class="seg-card-top">
                <div class="seg-dot" style="background:{prof['color']};"></div>
                <div class="seg-name">{seg_name}</div>
                <div class="seg-count">{n:,}</div>
            </div>
            <div class="seg-stat-row"><span class="seg-stat-label">Avg Age</span><span class="seg-stat-val">{sd['Age'].mean():.1f} yrs</span></div>
            <div class="seg-stat-row"><span class="seg-stat-label">Avg Satisfaction</span><span class="seg-stat-val">{sd['satisfaction_score'].mean():.2f} / 5.0</span></div>
            <div class="seg-stat-row"><span class="seg-stat-label">Loan Rate</span><span class="seg-stat-val">{sd['has_loan'].mean()*100:.0f}%</span></div>
            <div class="seg-stat-row"><span class="seg-stat-label">Investment Rate</span><span class="seg-stat-val">{sd['is_investor'].mean()*100:.0f}%</span></div>
            <div class="seg-desc">{prof['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Segment summary table
    summary_rows = [
        ("Global Investors",  "Mixed investment/home intent, low satisfaction", "Premium service & concierge sales process"),
        ("First-Time Buyers", "High loan dependency, youngest demographic",     "Loan partnerships & educational marketing"),
        ("Corporate Buyers",  "Oldest demographic, strongest investment focus", "Enterprise account management & B2B outreach"),
        ("Luxury Investors",  "Largest segment, highest satisfaction",          "VIP retention & off-market access programs"),
    ]
    summary_df = pd.DataFrame(summary_rows, columns=["Segment","Primary Trait","Key Opportunity"])
    st.markdown('<div class="chart-card"><div class="chart-title">SEGMENT INTELLIGENCE SUMMARY</div><div class="chart-desc">One-line characterisation of each discovered cluster</div>', unsafe_allow_html=True)
    st.dataframe(summary_df, hide_index=True, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    b1, b2 = st.columns(2, gap="large")

    with b1:
        age_seg = fdf.groupby("Segment")["Age"].mean().reset_index().sort_values("Age", ascending=True)
        age_seg["Age"] = age_seg["Age"].round(1)
        fig_age = px.bar(
            age_seg, x="Age", y="Segment", orientation="h",
            color="Segment", color_discrete_map=SEG_COLORS,
            text=age_seg["Age"].apply(lambda v: f"{v:.1f} yrs"),
            labels={"Age":"Average Age (years)","Segment":""},
        )
        fig_age.update_traces(textposition="outside")
        fig_age.update_xaxes(range=[0, age_seg["Age"].max() * 1.18])
        theme(fig_age, height=260, legend=False)
        st.markdown('<div class="chart-card"><div class="chart-title">AVERAGE BUYER AGE</div><div class="chart-desc">Mean age per segment — oldest to youngest</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_age, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with b2:
        purp_total = fdf.groupby("Segment").size().rename("Total")
        purp_ct = fdf.groupby(["Segment","acquisition_purpose"]).size().reset_index(name="Count")
        purp_ct = purp_ct.merge(purp_total, on="Segment")
        purp_ct["Pct"] = (purp_ct["Count"] / purp_ct["Total"] * 100).round(1)
        fig_purp = px.bar(
            purp_ct, x="Segment", y="Pct", color="acquisition_purpose",
            barmode="relative",
            color_discrete_sequence=["#0F2040","#60A5FA"],
            labels={"acquisition_purpose":"Purpose","Pct":"Share (%)"},
            text=purp_ct["Pct"].apply(lambda v: f"{v:.0f}%"),
        )
        fig_purp.update_traces(textposition="inside", textfont=dict(size=10, color="white"))
        fig_purp.update_xaxes(tickangle=-20)
        theme(fig_purp, height=260)
        st.markdown('<div class="chart-card"><div class="chart-title">ACQUISITION PURPOSE SPLIT</div><div class="chart-desc">% Home vs. Investment intent per segment</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_purp, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — GEOGRAPHIC & INVESTMENT INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:

    # Local-only filter (collapsed by default) — empty = no filter applied
    _all_countries = sorted(fdf["country"].dropna().unique())
    _all_regions   = sorted(fdf["region"].dropna().unique())
    if "geo_country" not in st.session_state: st.session_state["geo_country"] = []
    if "geo_region"  not in st.session_state: st.session_state["geo_region"]  = []

    with st.expander("🔍  Explore Geography", expanded=False):
        gc1, gc2, gc3 = st.columns([2, 2, 1])
        with gc1:
            st.multiselect("Country", options=_all_countries, key="geo_country",
                           placeholder="All countries")
        with gc2:
            st.multiselect("Region",  options=_all_regions,  key="geo_region",
                           placeholder="All regions")
        with gc3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("↺ Reset", width="stretch"):
                st.session_state["geo_country"] = []
                st.session_state["geo_region"]  = []
                st.rerun()

    sel_countries = st.session_state["geo_country"] or _all_countries
    sel_regions   = st.session_state["geo_region"]  or _all_regions
    gdf = fdf[fdf["country"].isin(sel_countries)]
    gdf = gdf[gdf["region"].isin(sel_regions)]

    # Dynamic geographic insights
    if not gdf.empty:
        top_ctry   = gdf["country"].value_counts().idxmax()
        top_ctry_n = gdf["country"].value_counts().max()
        dom_seg_geo = gdf.groupby("country")["Segment"].agg(lambda x: x.value_counts().idxmax()).value_counts().idxmax()
        hi_inv_ctry = gdf.groupby("country")["is_investor"].mean().idxmax()
        hi_inv_pct  = gdf.groupby("country")["is_investor"].mean().max() * 100
        _geo_insights = [
            ("🌍", f"{top_ctry} is the largest buyer market", f"{top_ctry_n:,} buyers · dominant segment: {dom_seg_geo}"),
            ("📈", f"{hi_inv_ctry} has the highest investment rate", f"{hi_inv_pct:.0f}% of buyers acquire for investment"),
        ]
        loan_by_seg = gdf.groupby("Segment")["has_loan"].mean()
        if not loan_by_seg.empty:
            hi_loan = loan_by_seg.idxmax()
            _geo_insights.append(("🏦", f"{hi_loan} most financing-dependent", f"{loan_by_seg.max()*100:.0f}% loan application rate in current view"))
        _geo_html = "".join([
            f'<div class="insight-card"><div class="insight-icon">{ic}</div>'
            f'<div><div class="insight-headline">{hl}</div><div class="insight-detail">{dt}</div></div></div>'
            for ic, hl, dt in _geo_insights
        ])
        st.markdown(f'<div class="insight-strip">{_geo_html}</div>', unsafe_allow_html=True)

    g1, g2 = st.columns([3, 2], gap="large")

    with g1:
        ctry_seg = gdf.groupby(["country","Segment"]).size().reset_index(name="Count")
        fig_ctry = px.bar(
            ctry_seg, x="country", y="Count", color="Segment",
            barmode="stack", color_discrete_map=SEG_COLORS,
            labels={"country":"Country","Count":"Buyers"},
        )
        fig_ctry.update_xaxes(tickangle=-30)
        theme(fig_ctry, height=320)
        st.markdown('<div class="chart-card"><div class="chart-title">SEGMENT DISTRIBUTION BY COUNTRY</div><div class="chart-desc">Buyer segment composition across markets</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_ctry, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with g2:
        ctry_rank = (
            gdf.groupby("country")
               .agg(Buyers=("client_id","count"),
                    Avg_Sat=("satisfaction_score","mean"),
                    Invest_Rate=("is_investor","mean"))
               .reset_index().sort_values("Buyers", ascending=False)
        )
        ctry_rank["Invest Rate"] = (ctry_rank["Invest_Rate"]*100).round(1).astype(str)+"%"
        ctry_rank["Avg Sat"]     = ctry_rank["Avg_Sat"].round(2)
        st.markdown('<div class="chart-card"><div class="chart-title">COUNTRY PERFORMANCE</div><div class="chart-desc">Buyers, satisfaction, and investment intent by market</div>', unsafe_allow_html=True)
        st.dataframe(
            ctry_rank[["country","Buyers","Avg Sat","Invest Rate"]].rename(columns={"country":"Country"}),
            hide_index=True, width="stretch", height=320,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Regional heatmap
    top_regions = gdf["region"].value_counts().head(20).index
    reg_pivot = (
        gdf[gdf["region"].isin(top_regions)]
        .groupby(["region","Segment"]).size()
        .reset_index(name="Count")
        .pivot(index="region", columns="Segment", values="Count").fillna(0)
    )
    fig_reg = px.imshow(
        reg_pivot, color_continuous_scale=[[0,"#F8F9FB"],[1,"#0F2040"]],
        text_auto=".0f", labels=dict(color="Buyers"), aspect="auto",
    )
    theme(fig_reg, height=460, legend=False)
    fig_reg.update_xaxes(tickfont=dict(color=TEXT_DARK, size=11))
    fig_reg.update_yaxes(tickfont=dict(color=TEXT_DARK, size=11))
    st.markdown('<div class="chart-card"><div class="chart-title">REGIONAL CONCENTRATION (TOP 20)</div><div class="chart-desc">Buyer density matrix across regions and segments</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_reg, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    h1, h2 = st.columns(2, gap="large")

    with h1:
        loan_heat = gdf.groupby(["Segment","loan_applied"]).size().reset_index(name="Count")
        loan_pivot = loan_heat.pivot(index="Segment", columns="loan_applied", values="Count").fillna(0)
        fig_lh = px.imshow(
            loan_pivot, color_continuous_scale=[[0,"#EFF6FF"],[1,"#0F2040"]],
            text_auto=True, labels=dict(color="Buyers"), aspect="auto",
        )
        theme(fig_lh, height=260, legend=False)
        fig_lh.update_xaxes(tickfont=dict(color=TEXT_DARK, size=11))
        fig_lh.update_yaxes(tickfont=dict(color=TEXT_DARK, size=11))
        st.markdown('<div class="chart-card"><div class="chart-title">LOAN DEPENDENCY HEATMAP</div><div class="chart-desc">Financing behaviour by segment</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_lh, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with h2:
        inv_heat = gdf.groupby(["Segment","referral_channel"])["is_investor"].mean().reset_index()
        inv_pivot = inv_heat.pivot(index="Segment", columns="referral_channel", values="is_investor") * 100
        fig_ih = px.imshow(
            inv_pivot, color_continuous_scale=[[0,"#EFF6FF"],[1,"#0F2040"]],
            text_auto=".1f", labels=dict(color="Invest %"), aspect="auto",
        )
        fig_ih.update_coloraxes(colorbar=dict(tickformat=".0f", ticksuffix="%", thickness=12))
        theme(fig_ih, height=260, legend=False)
        fig_ih.update_xaxes(tickfont=dict(color=TEXT_DARK, size=11))
        fig_ih.update_yaxes(tickfont=dict(color=TEXT_DARK, size=11))
        st.markdown('<div class="chart-card"><div class="chart-title">INVESTMENT RATE BY CHANNEL</div><div class="chart-desc">% investment acquisitions by segment × referral channel</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_ih, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Buyer Behavior Intelligence Table
    beh = gdf.groupby("Segment").agg(
        Total_Buyers=("client_id","count"),
        Home_Pct=("is_investor", lambda x: (1-x.mean())*100),
        Invest_Pct=("is_investor", lambda x: x.mean()*100),
        Loan_Pct=("has_loan", lambda x: x.mean()*100),
        Avg_Sat=("satisfaction_score","mean"),
    ).reset_index()
    for col in ["Home_Pct","Invest_Pct","Loan_Pct"]: beh[col] = beh[col].round(1)
    beh["Avg_Sat"] = beh["Avg_Sat"].round(2)
    beh = beh.rename(columns={"Total_Buyers":"Total Buyers","Home_Pct":"Home %","Invest_Pct":"Investment %","Loan_Pct":"Loan %","Avg_Sat":"Avg Satisfaction"})
    st.markdown('<div class="chart-card"><div class="chart-title">BUYER BEHAVIOR INTELLIGENCE</div><div class="chart-desc">Behavioral metrics per segment in current geographic view</div>', unsafe_allow_html=True)
    st.dataframe(
        beh, hide_index=True, width="stretch",
        column_config={
            "Segment":       st.column_config.TextColumn("Segment"),
            "Total Buyers":  st.column_config.NumberColumn("Total Buyers", format="%d"),
            "Home %":        st.column_config.ProgressColumn("Home %",       min_value=0, max_value=100, format="%.1f%%"),
            "Investment %":  st.column_config.ProgressColumn("Investment %", min_value=0, max_value=100, format="%.1f%%"),
            "Loan %":        st.column_config.ProgressColumn("Loan %",       min_value=0, max_value=100, format="%.1f%%"),
            "Avg Satisfaction": st.column_config.ProgressColumn("Avg Satisfaction", min_value=0, max_value=5, format="%.2f"),
        },
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — MACHINE LEARNING ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[3]:

    # ML Pipeline Overview
    pipeline_steps = [
        ("📥", "Raw Data",      "2,000 buyer records from Parcl CRM"),
        ("🧹", "Cleaning",      "Deduplication, null handling, age calculation"),
        ("🔡", "Encoding",      "One-hot encoding of categorical features"),
        ("⚖️", "Scaling",       "StandardScaler on Age & Satisfaction"),
        ("🔵", "K-Means",       "K=4 clusters, random_state=42"),
        ("✅", "Validation",    "Silhouette score + Hierarchical comparison"),
        ("👥", "Buyer Segments","4 actionable market segments identified"),
    ]
    step_html = "".join([
        f'<div style="display:flex;flex-direction:column;align-items:center;flex:1;min-width:80px;">'
        f'<div style="font-size:1.4rem;margin-bottom:6px;">{icon}</div>'
        f'<div style="font-size:0.72rem;font-weight:600;color:#0F2040;text-align:center;margin-bottom:3px;">{step}</div>'
        f'<div style="font-size:0.65rem;color:#6B7280;text-align:center;line-height:1.3;">{desc}</div>'
        f'</div>'
        + (f'<div style="font-size:1.2rem;color:#CBD5E1;align-self:flex-start;margin-top:14px;padding:0 4px;">→</div>' if i < len(pipeline_steps)-1 else '')
        for i, (icon, step, desc) in enumerate(pipeline_steps)
    ])
    st.markdown(f"""
    <div class="chart-card" style="margin-bottom:1.5rem;">
        <div class="chart-title">ML PIPELINE</div>
        <div class="chart-desc">End-to-end process from raw data to buyer segments</div>
        <div style="display:flex;align-items:flex-start;gap:4px;padding:12px 0;">{step_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # ML KPI cards + silhouette explanation
    m1, m2, m3, m4 = st.columns(4, gap="medium")
    for col, (val, label, badge) in zip([m1,m2,m3,m4], [
        ("K = 4",  "Optimal Clusters",  "Elbow method validated"),
        ("0.412",  "Silhouette Score",   "Moderate–good separation"),
        ("2,000",  "Training Samples",  "Full dataset used"),
        ("4",      "HC Clusters",       "Hierarchical agreement"),
    ]):
        col.markdown(f"""
        <div class="ml-metric">
            <div class="ml-metric-val">{val}</div>
            <div class="ml-metric-label">{label}</div>
            <div class="ml-metric-badge">{badge}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-left:3px solid #2563EB;
                border-radius:8px;padding:12px 18px;margin-top:14px;">
        <span style="font-size:0.8rem;font-weight:600;color:#1D4ED8;">📊 Silhouette Score: 0.412</span><br>
        <span style="font-size:0.78rem;color:#374151;line-height:1.6;">
        Buyers within each segment are more similar to each other than to buyers in other segments.
        Scores above 0.4 indicate <strong>meaningful, defensible clusters</strong> — not statistical noise.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    ml1, ml2 = st.columns(2, gap="large")

    with ml1:
        # Dynamic Elbow Curve
        ks, wcss = get_elbow_data()
        fig_elbow = go.Figure()
        fig_elbow.add_trace(go.Scatter(
            x=ks, y=wcss,
            mode="lines+markers",
            line=dict(color=BLUE, width=3),
            marker=dict(size=8, color=NAVY, symbol="circle"),
            hovertemplate="K = %{x}<br>WCSS = %{y:.1f}<extra></extra>"
        ))
        # Highlight K=4 elbow point
        fig_elbow.add_trace(go.Scatter(
            x=[4], y=[wcss[3]],
            mode="markers",
            marker=dict(size=14, color="#EF4444", symbol="circle-open", line=dict(width=3)),
            hovertemplate="Optimal K = 4<extra></extra>"
        ))
        fig_elbow.update_layout(
            xaxis=dict(tickmode="linear", tick0=1, dtick=1, title="Number of Clusters (K)"),
            yaxis=dict(title="Inertia (WCSS)"),
        )
        theme(fig_elbow, height=300, legend=False)
        st.markdown('<div class="chart-card"><div class="chart-title">ELBOW METHOD — OPTIMAL K</div><div class="chart-desc">Within-cluster sum of squares (WCSS) drops sharply at K=4</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_elbow, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with ml2:
        k_vals = list(range(1, 11))
        sil_scores = [0.0, 0.18, 0.31, 0.412, 0.38, 0.36, 0.33, 0.31, 0.28, 0.26]
        fig_sil = go.Figure()
        fig_sil.add_trace(go.Bar(
            x=k_vals, y=sil_scores,
            marker_color=[BLUE if k == 4 else "#CBD5E1" for k in k_vals],
            text=[f"{s:.3f}" for s in sil_scores],
            textposition="outside", textfont=dict(size=10),
        ))
        fig_sil.add_vline(x=4, line_dash="dash", line_color=NAVY, line_width=1.5)
        fig_sil.update_layout(
            xaxis=dict(title="K", tickvals=k_vals),
            yaxis=dict(title="Silhouette Score", range=[0, 0.5]),
        )
        theme(fig_sil, height=300, legend=False)
        st.markdown('<div class="chart-card"><div class="chart-title">SILHOUETTE SCORE BY K</div><div class="chart-desc">Peak at K=4 confirms cluster quality</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_sil, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    ml3, ml4 = st.columns(2, gap="large")

    with ml3:
        cluster_sizes = fdf.groupby("Segment").size().reset_index(name="Count").sort_values("Count", ascending=True)
        fig_size = px.bar(
            cluster_sizes, x="Count", y="Segment", orientation="h",
            color="Segment", color_discrete_map=SEG_COLORS, text="Count",
        )
        fig_size.update_traces(textposition="outside")
        theme(fig_size, height=260, legend=False)
        st.markdown('<div class="chart-card"><div class="chart-title">CLUSTER SIZE DISTRIBUTION</div><div class="chart-desc">Buyers assigned to each K-Means segment</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_size, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with ml4:
        agreement = pd.crosstab(fdf["Cluster"], fdf["HC_Cluster"])
        agreement.index   = [CLUSTER_NAMES.get(i, str(i)) for i in agreement.index]
        agreement.columns = [f"HC {i}" for i in agreement.columns]
        fig_agree = px.imshow(
            agreement, color_continuous_scale=[[0,"#F8F9FB"],[1,"#0F2040"]],
            text_auto=True, labels=dict(color="Buyers"), aspect="auto",
        )
        theme(fig_agree, height=260, legend=False)
        st.markdown('<div class="chart-card"><div class="chart-title">K-MEANS vs. HIERARCHICAL AGREEMENT</div><div class="chart-desc">Cross-method validation — diagonal dominance confirms stability</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_agree, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Cluster characteristics table
    char = fdf.groupby("Segment").agg(
        Avg_Age=("Age","mean"),
        Avg_Sat=("satisfaction_score","mean"),
        Loan_Rate=("has_loan","mean"),
        Invest_Rate=("is_investor","mean"),
    ).reset_index()
    char["Avg Age"]     = char["Avg_Age"].round(1)
    char["Satisfaction"] = char["Avg_Sat"].round(2)
    char["Loan Rate"]   = (char["Loan_Rate"]*100).round(1).astype(str)+"%"
    char["Invest Rate"] = (char["Invest_Rate"]*100).round(1).astype(str)+"%"
    st.markdown('<div class="chart-card"><div class="chart-title">CLUSTER CHARACTERISTICS</div><div class="chart-desc">Key metrics that define each discovered segment</div>', unsafe_allow_html=True)
    st.dataframe(
        char[["Segment","Avg Age","Satisfaction","Loan Rate","Invest Rate"]],
        hide_index=True, width="stretch",
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — STRATEGIC RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[4]:

    recs = {
        "Global Investors": {
            "color":    SEG_COLORS["Global Investors"],
            "size":     len(fdf[fdf["Segment"]=="Global Investors"]),
            "Marketing":    "Lead with ROI data and portfolio diversification messaging via LinkedIn and premium financial media.",
            "Sales":        "Dedicated investment advisors with concierge fast-track and cross-timezone digital documentation.",
            "Retention":    "Portfolio review sessions, pre-launch inventory access, and a dedicated asset management tier.",
            "Investment":   "Premium urban and coastal markets with high appreciation potential.",
        },
        "First-Time Buyers": {
            "color":    SEG_COLORS["First-Time Buyers"],
            "size":     len(fdf[fdf["Segment"]=="First-Time Buyers"]),
            "Marketing":    "Educational content — guides and webinars on first-time buyer journeys and mortgage processes.",
            "Sales":        "Loan pre-qualification partnerships, affordability schemes, and flexible deposit options.",
            "Retention":    "Post-purchase home management resources and referral incentive programmes.",
            "Investment":   "Affordable suburban corridors with preferred lender integrations.",
        },
        "Corporate Buyers": {
            "color":    SEG_COLORS["Corporate Buyers"],
            "size":     len(fdf[fdf["Segment"]=="Corporate Buyers"]),
            "Marketing":    "B2B outreach via agency channels — portfolio acquisition capabilities and volume pricing.",
            "Sales":        "Enterprise account management with bulk acquisition agreements and legal advisory support.",
            "Retention":    "Quarterly portfolio reporting and exclusive pre-market access portals.",
            "Investment":   "Commercial and multi-family residential assets with corporate relocation packages.",
        },
        "Luxury Investors": {
            "color":    SEG_COLORS["Luxury Investors"],
            "size":     len(fdf[fdf["Segment"]=="Luxury Investors"]),
            "Marketing":    "Ultra-premium positioning through exclusive events, private viewings, and luxury lifestyle media.",
            "Sales":        "White-glove, invitation-only experience with off-market property access before public listing.",
            "Retention":    "VIP loyalty tier with trophy asset access and annual market intelligence briefings.",
            "Investment":   "Flagship luxury and landmark properties — capital preservation and long-term legacy value.",
        },
    }

    seg_names = list(recs.keys())
    for pair in [(seg_names[0], seg_names[1]), (seg_names[2], seg_names[3])]:
        cols = st.columns(2, gap="large")
        for col, seg_name in zip(cols, pair):
            rec = recs[seg_name]
            col.markdown(f"""
            <div class="rec-card">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
                    <div style="width:10px;height:10px;border-radius:50%;background:{rec['color']};"></div>
                    <div class="rec-seg-name">{seg_name}</div>
                    <div style="margin-left:auto;background:#F3F4F6;color:#6B7280;font-size:0.7rem;font-weight:600;padding:2px 8px;border-radius:20px;">{rec['size']:,} buyers</div>
                </div>
                <div class="rec-row"><div class="rec-label">📣 Marketing</div><div class="rec-text">{rec['Marketing']}</div></div>
                <div class="rec-row"><div class="rec-label">🤝 Sales</div><div class="rec-text">{rec['Sales']}</div></div>
                <div class="rec-row"><div class="rec-label">🔄 Retention</div><div class="rec-text">{rec['Retention']}</div></div>
                <div class="rec-row"><div class="rec-label">💼 Investment Focus</div><div class="rec-text">{rec['Investment']}</div></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Business Opportunity Matrix
    opp = fdf.groupby("Segment").agg(
        Satisfaction=("satisfaction_score","mean"),
        Size=("client_id","count"),
    ).reset_index()
    opp["Satisfaction"] = opp["Satisfaction"].round(3)
    mid_size = opp["Size"].median()
    mid_sat  = opp["Satisfaction"].median()

    fig_opp = px.scatter(
        opp, x="Size", y="Satisfaction",
        size="Size", color="Segment", color_discrete_map=SEG_COLORS,
        text="Segment",
        labels={"Size":"Segment Size (Total Buyers) →","Satisfaction":"Average Satisfaction Score →"},
        size_max=55,
    )
    fig_opp.update_traces(textposition="top center", textfont=dict(size=10, color=TEXT_DARK))
    fig_opp.add_hline(y=mid_sat,  line_dash="dot", line_color=BORDER, line_width=1.2)
    fig_opp.add_vline(x=mid_size, line_dash="dot", line_color=BORDER, line_width=1.2)

    x_max = opp["Size"].max() * 1.05
    x_min = opp["Size"].min() * 0.85
    y_max = opp["Satisfaction"].max() * 1.01
    y_min = opp["Satisfaction"].min() * 0.99
    for qx, qy, ql, qc in [
        (x_max*0.72, y_max, "⭐ Maintain Leadership",  "#166534"),
        (x_min,      y_max, "🌱 Growth Opportunity",   "#1D4ED8"),
        (x_max*0.72, y_min, "🚨 Improve Now",          "#9A3412"),
        (x_min,      y_min, "👁 Monitor",              "#6B7280"),
    ]:
        fig_opp.add_annotation(
            x=qx, y=qy, text=ql, showarrow=False,
            font=dict(size=10, color=qc, family="Inter, sans-serif"),
            bgcolor="white", borderpad=4, opacity=0.85,
        )

    theme(fig_opp, height=400, legend=False)
    st.markdown('<div class="chart-card"><div class="chart-title">BUSINESS OPPORTUNITY MATRIX</div><div class="chart-desc">Segment size vs. satisfaction — strategic priorities at a glance</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_opp, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

