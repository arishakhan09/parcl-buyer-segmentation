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
    <h1 style='text-align:center; color:#1E3A8A;'>
        AI-Driven Buyer Segmentation Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center; color:#6B7280;'>
        Parcl Co. Limited — Market Intelligence
    </p>
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
        yaxis_title="Number of Buyers"
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
        yaxis_title="Region"
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