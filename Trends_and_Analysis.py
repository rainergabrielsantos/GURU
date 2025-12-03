import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from utils import apply_custom_theme

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Trends & Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_theme()

# ---------- DATA GENERATION (MOCK – SODA BUSINESS) ----------
@st.cache_data
def generate_mock_data():
    np.random.seed(42)

    # Last 365 days
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=364)
    dates = pd.date_range(start_date, end_date, freq="D")

    # Soda-focused categories
    categories = [
        "Cola",
        "Lemon-Lime",
        "Citrus",
        "Fruit Soda",
        "Specialty Cola",
        "Energy Drinks",
    ]

    traffic_sources = ["Organic Search", "Paid Ads", "Social", "Email", "Direct"]

    # Soda products (SKUs / names)
    products = [
        "Coca-Cola Classic 12oz Cans (24-pack)",
        "Coca-Cola Classic 20oz Bottles (12-pack)",
        "Coke Zero 12oz Cans (12-pack)",
        "Pepsi Cola 12oz Cans (12-pack)",
        "Sprite Lemon-Lime 20oz Bottles (12-pack)",
        "Fanta Orange 12oz Cans (12-pack)",
        "Dr Pepper 12oz Cans (6-pack)",
        "Mountain Dew 16oz Bottles (6-pack)",
        "Monster Energy 16oz Cans (4-pack)",
        "Red Bull 8.4oz Cans (4-pack)",
    ]

    rows = []
    for date in dates:
        for src in traffic_sources:
            # Baseline demand by traffic source
            if src == "Paid Ads":
                base_sessions = 130
            elif src == "Organic Search":
                base_sessions = 110
            elif src == "Social":
                base_sessions = 85
            elif src == "Email":
                base_sessions = 60
            else:  # Direct
                base_sessions = 75

            # Weekly seasonality: small early-week boost
            weekday_boost = 1.1 if date.weekday() in [0, 1] else 0.95
            # Weekend bump for soda runs
            weekend_boost = 1.2 if date.weekday() in [4, 5] else 1.0

            sessions = np.random.poisson(base_sessions * weekday_boost * weekend_boost)

            # Conversion rate varies by source (typical ecommerce behavior)
            if src == "Email":
                base_cr = 0.055
            elif src == "Paid Ads":
                base_cr = 0.04
            elif src == "Organic Search":
                base_cr = 0.032
            elif src == "Direct":
                base_cr = 0.03
            else:  # Social
                base_cr = 0.024

            cr = base_cr + np.random.normal(0, 0.004)
            cr = max(0.006, min(cr, 0.13))  # clamp

            orders = np.random.binomial(sessions, cr) if sessions > 0 else 0

            # Pick a soda category & drive average ticket from that
            category = np.random.choice(categories)

            # Approximate cart values by category (multi-pack soda orders)
            if category == "Energy Drinks":
                avg_ticket = np.random.normal(45, 10)
            elif category in ["Specialty Cola", "Fruit Soda"]:
                avg_ticket = np.random.normal(38, 8)
            elif category in ["Cola", "Lemon-Lime", "Citrus"]:
                avg_ticket = np.random.normal(32, 7)
            else:
                avg_ticket = np.random.normal(30, 6)

            avg_ticket = max(8, avg_ticket)
            revenue = orders * avg_ticket

            product_name = np.random.choice(products)

            rows.append(
                {
                    "date": date.date(),
                    "traffic_source": src,
                    "category": category,
                    "product_name": product_name,
                    "sessions": sessions,
                    "orders": orders,
                    "revenue": revenue,
                }
            )

    df = pd.DataFrame(rows)
    df["conversion_rate"] = np.where(
        df["sessions"] > 0, df["orders"] / df["sessions"], 0
    )
    df["aov"] = np.where(df["orders"] > 0, df["revenue"] / df["orders"], 0)

    return df


df = generate_mock_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.title("Trends Filters")

min_date = df["date"].min()
max_date = df["date"].max()

default_start = max_date - timedelta(days=29)  # last 30 days by default
start_date, end_date = st.sidebar.date_input(
    "Date range",
    value=(default_start, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(start_date, tuple) or isinstance(start_date, list):
    # Normalize tuple input
    start_date, end_date = start_date[0], start_date[1]

traffic_options = sorted(df["traffic_source"].unique())
category_options = sorted(df["category"].unique())

selected_sources = st.sidebar.multiselect(
    "Traffic sources",
    traffic_options,
    default=traffic_options,
)

selected_categories = st.sidebar.multiselect(
    "Soda categories",
    category_options,
    default=category_options,
)

# Filtered dataframe
mask = (
    (df["date"] >= start_date)
    & (df["date"] <= end_date)
    & (df["traffic_source"].isin(selected_sources))
    & (df["category"].isin(selected_categories))
)

filtered = df[mask]

# ---------- HELPER: PREVIOUS PERIOD FOR KPI DELTAS ----------
def compute_previous_period_metrics():
    current_len = (end_date - start_date).days + 1
    prev_end = start_date - timedelta(days=1)
    prev_start = prev_end - timedelta(days=current_len - 1)

    prev_mask = (
        (df["date"] >= prev_start)
        & (df["date"] <= prev_end)
        & (df["traffic_source"].isin(selected_sources))
        & (df["category"].isin(selected_categories))
    )

    prev = df[prev_mask]

    prev_rev = prev["revenue"].sum()
    prev_orders = prev["orders"].sum()
    prev_sessions = prev["sessions"].sum()

    prev_cr = prev_orders / prev_sessions if prev_sessions > 0 else 0
    prev_aov = prev_rev / prev_orders if prev_orders > 0 else 0

    return {
        "revenue": prev_rev,
        "orders": prev_orders,
        "sessions": prev_sessions,
        "conversion_rate": prev_cr,
        "aov": prev_aov,
    }


prev_metrics = compute_previous_period_metrics()

# ---------- METRICS (KPI CARDS) ----------
st.title("Trends & Analysis")
st.caption(
    "Track traffic, orders, and revenue trends across flavors, categories, and channels."
)

if filtered.empty:
    st.warning(
        "No data for the selected filters. Try expanding the date range or adjusting sources/categories."
    )
    st.stop()

total_revenue = filtered["revenue"].sum()
total_orders = filtered["orders"].sum()
total_sessions = filtered["sessions"].sum()

conversion_rate = total_orders / total_sessions if total_sessions > 0 else 0
aov = total_revenue / total_orders if total_orders > 0 else 0


def pct_delta(current, previous):
    if previous <= 0:
        return 0.0
    return (current - previous) / previous * 100


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Soda Revenue",
        f"${total_revenue:,.0f}",
        f"{pct_delta(total_revenue, prev_metrics['revenue']):+.1f}% vs prev.",
    )

with col2:
    st.metric(
        "Soda Orders",
        f"{total_orders:,}",
        f"{pct_delta(total_orders, prev_metrics['orders']):+.1f}% vs prev.",
    )

with col3:
    st.metric(
        "Conversion Rate",
        f"{conversion_rate*100:.2f}%",
        f"{pct_delta(conversion_rate, prev_metrics['conversion_rate']):+.1f} pts vs prev.",
    )

with col4:
    st.metric(
        "Avg Order Value",
        f"${aov:,.2f}",
        f"{pct_delta(aov, prev_metrics['aov']):+.1f}% vs prev.",
    )

st.markdown("---")

# ---------- TOP SECTION: TIME SERIES + CATEGORY REVENUE ----------
left_col, right_col = st.columns((2, 1))

with left_col:
    st.subheader("Revenue Trend")
    daily = (
        filtered.groupby("date", as_index=False)
        .agg({"revenue": "sum", "orders": "sum"})
        .sort_values("date")
    )
    fig_revenue = px.line(
        daily,
        x="date",
        y="revenue",
        markers=True,
        labels={"date": "Date", "revenue": "Revenue (USD)"},
        title="Daily Soda Revenue",
    )
    fig_revenue.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=320)
    st.plotly_chart(fig_revenue, width='stretch')

with right_col:
    st.subheader("Revenue by Soda Category")
    by_cat = (
        filtered.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
    fig_cat = px.bar(
        by_cat,
        x="category",
        y="revenue",
        labels={"category": "Soda Category", "revenue": "Revenue (USD)"},
        title="Category Mix (Cola vs Citrus, Energy, etc.)",
    )
    fig_cat.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=320)
    st.plotly_chart(fig_cat, width='stretch')

# ---------- MIDDLE SECTION: TRAFFIC SOURCES ----------
st.subheader("Traffic Source Breakdown (Soda Shoppers)")

by_source = (
    filtered.groupby("traffic_source", as_index=False)["sessions"]
    .sum()
    .sort_values("sessions", ascending=False)
)
fig_source = px.pie(
    by_source,
    names="traffic_source",
    values="sessions",
    hole=0.5,
    title="Where Soda Traffic Comes From",
)
fig_source.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=320)
st.plotly_chart(fig_source, width='stretch')

# ---------- BOTTOM SECTION: TOP PRODUCTS ----------
st.subheader("Top Soda Products by Revenue")

product_perf = (
    filtered.groupby("product_name", as_index=False)
    .agg(
        {
            "orders": "sum",
            "revenue": "sum",
            "sessions": "sum",
        }
    )
)
product_perf["conversion_rate"] = np.where(
    product_perf["sessions"] > 0,
    product_perf["orders"] / product_perf["sessions"],
    0,
)
product_perf["aov"] = np.where(
    product_perf["orders"] > 0,
    product_perf["revenue"] / product_perf["orders"],
    0,
)

top_products = product_perf.sort_values("revenue", ascending=False).head(10)
top_products_display = top_products.assign(
    revenue=top_products["revenue"].map(lambda x: f"${x:,.0f}"),
    conversion_rate=(top_products["conversion_rate"] * 100).map(
        lambda x: f"{x:.2f}%"
    ),
    aov=top_products["aov"].map(lambda x: f"${x:,.2f}"),
)

st.dataframe(
    top_products_display[
        ["product_name", "orders", "revenue", "conversion_rate", "aov"]
    ].reset_index(drop=True),
    width='stretch',
)


