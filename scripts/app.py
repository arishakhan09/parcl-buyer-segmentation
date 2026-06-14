import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Parcl Buyer Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Responsive CSS Injection ──────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Root tokens ── */
    :root {
        --sidebar-bg:      #0F172A;
        --sidebar-accent:  #3B82F6;
        --sidebar-text:    #CBD5E1;
        --sidebar-label:   #64748B;
        --sidebar-border:  #1E293B;
        --sidebar-hover:   #1E293B;
        --sidebar-width:   260px;
        --header-blue:     #1E3A8A;
        --body-font:       'Inter', sans-serif;
        --radius:          10px;
    }

    /* ── Global font ── */
    html, body, [class*="css"] {
        font-family: var(--body-font) !important;
    }

    /* ── Main content area ── */
    .main .block-container {
        padding: 1.5rem 2rem 3rem 2rem;
        max-width: 1400px;
    }

    /* ══════════════════════════════════════
       SIDEBAR — full restyle
    ══════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: var(--sidebar-bg) !important;
        border-right: 1px solid var(--sidebar-border);
        min-width: var(--sidebar-width) !important;
        max-width: var(--sidebar-width) !important;
        transition: transform 0.3s ease, width 0.3s ease;
    }

    /* Sidebar inner padding */
    section[data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1.25rem 2rem 1.25rem;
    }

    /* Sidebar header text (🔍 Filter Data) */
    section[data-testid="stSidebar"] h2 {
        color: #F1F5F9 !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 1.25rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid var(--sidebar-border);
    }

    /* Sidebar filter labels */
    section[data-testid="stSidebar"] label {
        color: var(--sidebar-label) !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Multiselect container */
    section[data-testid="stSidebar"] .stMultiSelect > div > div {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: var(--radius) !important;
        color: var(--sidebar-text) !important;
        font-size: 0.82rem !important;
        transition: border-color 0.2s;
    }
    section[data-testid="stSidebar"] .stMultiSelect > div > div:focus-within {
        border-color: var(--sidebar-accent) !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    }

    /* Multiselect tags (selected items) */
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background: #1D4ED8 !important;
        border-radius: 6px !important;
        color: #EFF6FF !important;
        font-size: 0.75rem !important;
    }

    /* Multiselect tag × button */
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] svg {
        color: #BFDBFE !important;
    }

    /* Multiselect dropdown list */
    ul[data-testid="stMultiSelectOptionsList"] {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: var(--radius) !important;
    }
    ul[data-testid="stMultiSelectOptionsList"] li {
        color: #CBD5E1 !important;
        font-size: 0.82rem !important;
    }
    ul[data-testid="stMultiSelectOptionsList"] li:hover {
        background: #334155 !important;
    }

    /* Divider inside sidebar */
    section[data-testid="stSidebar"] hr {
        border-color: var(--sidebar-border) !important;
        margin: 1rem 0;
    }

    /* Sidebar collapse button */
    button[data-testid="collapsedControl"],
    button[kind="header"] {
        background: var(--sidebar-bg) !important;
        border: none !important;
        color: var(--sidebar-text) !important;
    }

    /* ══════════════════════════════════════
       TABS — cleaner look
    ══════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 0;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-radius: 8px 8px 0 0;
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 0.55rem 1.1rem;
        transition: color 0.2s, background 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: #EFF6FF !important;
        color: var(--header-blue) !important;
        font-weight: 700;
        border-bottom: 2px solid var(--header-blue) !important;
    }

    /* ══════════════════════════════════════
       METRIC CARDS
    ══════════════════════════════════════ */
    div[data-testid="metric-container"] {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: var(--radius);
        padding: 1rem 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="metric-container"] label {
        color: #64748B !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: var(--header-blue) !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }

    /* ══════════════════════════════════════
       SUBHEADERS
    ══════════════════════════════════════ */
    h2 { color: #1E293B !important; }
    h3 { color: #334155 !important; font-size: 1rem !important; }

    /* ══════════════════════════════════════
       DATAFRAME
    ══════════════════════════════════════ */
    .stDataFrame {
        border-radius: var(--radius);
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }

    /* ══════════════════════════════════════
       SELECTBOX & TEXT INPUT (Tab 4)
    ══════════════════════════════════════ */
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        border-radius: var(--radius) !important;
        border-color: #CBD5E1 !important;
        font-size: 0.85rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--sidebar-accent) !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
    }

    /* ══════════════════════════════════════
       RESPONSIVE — Tablet (≤900px)
    ══════════════════════════════════════ */
    @media (max-width: 900px) {
        .main .block-container {
            padding: 1rem 1.25rem 2rem 1.25rem;
        }

        /* Stack Streamlit columns */
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        .stTabs [data-baseweb="tab"] {
            font-size: 0.78rem;
            padding: 0.45rem 0.7rem;
        }
    }

    /* ══════════════════════════════════════
       RESPONSIVE — Mobile (≤640px)
       Sidebar becomes an overlay drawer
    ══════════════════════════════════════ */
    @media (max-width: 640px) {

        /* Full-width main content when sidebar is collapsed */
        .main .block-container {
            padding: 0.75rem 0.85rem 2rem 0.85rem !important;
        }

        /* Sidebar slides in as a drawer over content */
        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100vh !important;
            z-index: 9999 !important;
            box-shadow: 4px 0 24px rgba(0,0,0,0.4) !important;
            min-width: 85vw !important;
            max-width: 85vw !important;
        }

        /* Collapse sidebar completely when closed on mobile */
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-100%) !important;
            min-width: 0 !important;
            max-width: 0 !important;
        }

        /* Give main content full width on mobile */
        section.main {
            margin-left: 0 !important;
        }

        /* Stack all columns */
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        /* Tighten tabs on mobile */
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap;
            gap: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.72rem;
            padding: 0.4rem 0.55rem;
        }

        /* Metric cards full width */
        div[data-testid="metric-container"] {
            margin-bottom: 0.6rem;
        }

        /* Charts — cap height on mobile */
        .js-plotly-plot {
            max-height: 320px;
        }

        /* Header font size */
        h1 { font-size: 1.4rem !important; }
    }

    /* ══════════════════════════════════════
       MOBILE HINT BANNER (shows only on small screens)
    ══════════════════════════════════════ */
    .mobile-hint {
        display: none;
    }
    @media (max-width: 640px) {
        .mobile-hint {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: #EFF6FF;
            border: 1px solid #BFDBFE;
            border-radius: 8px;
            padding: 0.55rem 0.9rem;
            font-size: 0.78rem;
            color: #1D4ED8;
            font-weight: 500;
            margin-bottom: 1rem;
        }
    }

    /* ══════════════════════════════════════
       SCROLLBAR (sidebar)
    ══════════════════════════════════════ */
    section[data-testid="stSidebar"] ::-webkit-scrollbar {
        width: 4px;
    }
    section[data-testid="stSidebar"] ::-webkit-scrollbar-track {
        background: transparent;
    }
    section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ── Data Loading ──────────────────────────────────────────────
@st.cache_data
def load_data():
    csv_path = Path("clustured/clustered_clients.csv")

    if not csv_path.exists():
        st.error(f"CSV file not found: {csv_path}")
        st.stop()

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
        st.stop()

    required_columns = [
        "Cluster",
        "country",
        "region",
        "acquisition_purpose",
        "client_type",
        "client_id",
        "Age",
        "satisfaction_score"
    ]

    missing_cols = [c for c in required_columns if c not in df.columns]

    if missing_cols:
        st.error(
            f"Missing columns in CSV: {', '.join(missing_cols)}\n\n"
            f"Available columns:\n{list(df.columns)}"
        )
        st.stop()

    cluster_names = {
        0: "Global Investors",
        1: "First-Time Buyers",
        2: "Corporate Buyers",
        3: "Luxury Investors"
    }

    df["Segment"] = df["Cluster"].map(cluster_names).fillna("Unknown")

    return df


df = load_data()

# ── Header ────────────────────────────────────────────────────
st.markdown(
    """
    <h1 style='text-align:center; color:#1E3A8A; font-family:Inter,sans-serif; font-weight:700; letter-spacing:-0.02em;'>
        AI-Driven Buyer Segmentation
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center; color:#94A3B8; font-family:Inter,sans-serif; font-size:0.9rem; margin-top:-0.4rem;'>
        Parcl Co. Limited — Market Intelligence Dashboard
    </p>
    """,
    unsafe_allow_html=True
)

# Mobile hint banner
st.markdown(
    """
    <div class="mobile-hint">
        ☰ Tap the arrow at top-left to open filters
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ── Sidebar Filters ───────────────────────────────────────────
st.sidebar.header("🔍 Filter Data")

selected_country = st.sidebar.multiselect(
    "Country",
    options=sorted(df["country"].dropna().unique()),
    default=sorted(df["country"].dropna().unique())
)

selected_region = st.sidebar.multiselect(
    "Region",
    options=sorted(df["region"].dropna().unique()),
    default=sorted(df["region"].dropna().unique())
)

selected_purpose = st.sidebar.multiselect(
    "Acquisition Purpose",
    options=sorted(df["acquisition_purpose"].dropna().unique()),
    default=sorted(df["acquisition_purpose"].dropna().unique())
)

selected_client = st.sidebar.multiselect(
    "Client Type",
    options=sorted(df["client_type"].dropna().unique()),
    default=sorted(df["client_type"].dropna().unique())
)

# ── Apply Filters ─────────────────────────────────────────────
filtered_df = df[
    df["country"].isin(selected_country)
    & df["region"].isin(selected_region)
    & df["acquisition_purpose"].isin(selected_purpose)
    & df["client_type"].isin(selected_client)
]

if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Market Overview",
    "🌍 Geographic Analysis",
    "💡 Segment Insights",
    "📋 Client Directory"
])

# ── Tab 1 ─────────────────────────────────────────────────────
with tab1:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Buyer Segmentation Overview")

        segment_counts = (
            filtered_df["Segment"]
            .value_counts()
            .reset_index()
        )

        segment_counts.columns = ["Segment", "Count"]

        fig1 = px.pie(
            segment_counts,
            names="Segment",
            values="Count",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig1.update_layout(
            margin=dict(t=30, b=10, l=10, r=10),
            autosize=True
        )

        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Investor Behavior")

        behavior_data = (
            filtered_df
            .groupby(["Segment", "acquisition_purpose"])
            .size()
            .reset_index(name="Count")
        )

        fig2 = px.bar(
            behavior_data,
            x="Segment",
            y="Count",
            color="acquisition_purpose",
            barmode="group"
        )
        fig2.update_layout(
            margin=dict(t=30, b=30, l=10, r=10),
            autosize=True,
            legend=dict(orientation="h", y=-0.25)
        )

        st.plotly_chart(fig2, use_container_width=True)

# ── Tab 2 ─────────────────────────────────────────────────────
with tab2:

    st.subheader("Geographic Buyer Analysis")

    geo_data = (
        filtered_df
        .groupby(["region", "Segment"])
        .size()
        .reset_index(name="Count")
    )

    fig3 = px.bar(
        geo_data,
        x="region",
        y="Count",
        color="Segment"
    )

    fig3.update_layout(
        height=550,
        xaxis_tickangle=-45,
        xaxis_title="Region",
        yaxis_title="Number of Buyers",
        margin=dict(t=30, b=80, l=10, r=10),
        legend=dict(orientation="h", y=-0.3)
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Region × Segment Heatmap")

    pivot = (
        filtered_df
        .groupby(["region", "Segment"])
        .size()
        .unstack(fill_value=0)
    )

    fig4 = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale="Blues"
        )
    )

    fig4.update_layout(
        height=450,
        xaxis_title="Segment",
        yaxis_title="Region",
        margin=dict(t=30, b=30, l=10, r=10)
    )

    st.plotly_chart(fig4, use_container_width=True)

# ── Tab 3 ─────────────────────────────────────────────────────
with tab3:

    st.subheader("Key Segment Insights")

    insights = (
        filtered_df
        .groupby("Segment")
        .agg(
            Total_Clients=("client_id", "count"),
            Average_Age=("Age", "mean"),
            Average_Satisfaction=("satisfaction_score", "mean")
        )
        .reset_index()
    )

    for _, row in insights.iterrows():

        st.markdown(f"### {row['Segment']}")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total Clients",
            int(row["Total_Clients"])
        )

        c2.metric(
            "Average Age",
            f"{row['Average_Age']:.1f} yrs"
        )

        c3.metric(
            "Average Satisfaction",
            f"{row['Average_Satisfaction']:.2f}"
        )

        st.divider()

# ── Tab 4 ─────────────────────────────────────────────────────
with tab4:

    st.subheader("Client Directory")

    col1, col2 = st.columns(2)

    with col1:
        segment_options = ["All Segments"] + sorted(
            filtered_df["Segment"].dropna().unique().tolist()
        )

        dir_segment = st.selectbox(
            "Filter by Segment",
            segment_options
        )

    with col2:
        dir_search = st.text_input(
            "Search by Client ID",
            placeholder="e.g. C0015"
        )

    dir_df = filtered_df.copy()

    if dir_segment != "All Segments":
        dir_df = dir_df[
            dir_df["Segment"] == dir_segment
        ]

    if dir_search.strip():
        dir_df = dir_df[
            dir_df["client_id"]
            .astype(str)
            .str.upper()
            == dir_search.strip().upper()
        ]

    display_cols = [
        "client_id",
        "client_type",
        "country",
        "region",
        "Age",
        "acquisition_purpose",
        "Segment"
    ]

    available_cols = [
        c for c in display_cols
        if c in dir_df.columns
    ]

    st.dataframe(
        dir_df[available_cols],
        hide_index=True,
        use_container_width=True
    )
