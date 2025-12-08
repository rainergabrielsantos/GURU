import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils import apply_custom_theme

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Sales Analytics", layout="wide")
apply_custom_theme()

# ---------- STYLES ----------
st.markdown(
    """
    <style>
    .guru-section-card {
        background: #050b16;
        border-radius: 18px;
        border: 1px solid #111827;
        padding: 1.0rem 1.1rem 0.9rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 14px 40px rgba(0,0,0,0.55);
    }
    .guru-kpi-card {
        background: #050b16;
        border-radius: 16px;
        border: 1px solid #111827;
        padding: 0.8rem 1.0rem;
        box-shadow: 0 10px 26px rgba(0,0,0,0.45);
    }
    .guru-kpi-label {
        font-size: 0.78rem;
        color: #9ca3af;
        margin-bottom: 0.15rem;
    }
    .guru-kpi-value {
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .guru-kpi-delta-pos {
        font-size: 0.78rem;
        color: #4ade80;
    }
    .guru-kpi-delta-neg {
        font-size: 0.78rem;
        color: #f97373;
    }
    .guru-quarter-meta {
        font-size: 0.75rem;
        color: #9ca3af;
        margin-top: 0.25rem;
    }
    .badge-actual {
        display: inline-block;
        font-size: 0.72rem;
        padding: 0.15rem 0.45rem;
        border-radius: 999px;
        background: rgba(55,65,81,0.9);
        color: #e5e7eb;
        margin-left: 0.4rem;
    }
    .badge-predicted {
        display: inline-block;
        font-size: 0.72rem;
        padding: 0.15rem 0.45rem;
        border-radius: 999px;
        background: rgba(22,163,74,0.12);
        color: #4ade80;
        border: 1px solid rgba(34,197,94,0.7);
        margin-left: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- DATA ----------
@st.cache_data
def generate_mock_sales():
    # Monthly dates for 2024
    dates = pd.date_range("2024-01-01", "2024-12-01", freq="MS")
    df = pd.DataFrame({"month": dates})
    df["month_name"] = df["month"].dt.strftime("%b")
    df["quarter"] = "Q" + df["month"].dt.quarter.astype(str) + " 2024"

    # Base trend: gently rising revenue
    base = np.linspace(8200, 15000, len(df))
    noise = np.random.normal(0, 550, len(df))
    df["current_revenue"] = np.round(base + noise, -1)

    # Previous year slightly lower
    df["prev_year_revenue"] = np.round(
        df["current_revenue"] * np.random.uniform(0.86, 0.94, len(df)),
        -1,
    )

    # Target line ~ 5–8% above previous year
    df["target"] = np.round(df["prev_year_revenue"] * 1.07, -1)

    # Forecast extension (for future quarters)
    df["forecast"] = np.round(
        df["current_revenue"] * np.random.uniform(1.03, 1.09, len(df)),
        -1,
    )

    # Mark Q1 + Q2 as actual, Q3 + Q4 as predicted
    df["is_actual"] = df["quarter"].isin(["Q1 2024", "Q2 2024"])

    # Category breakdown per quarter
    categories = ["Cola", "Lemon-Lime", "Citrus", "Energy Drinks", "Specialty Cola"]
    rows = []
    for q in ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]:
        q_mask = df["quarter"] == q
        q_total = df.loc[q_mask, "current_revenue"].sum()
        # Shares vary a bit by quarter
        if q in ["Q1 2024", "Q2 2024"]:
            weights = np.array([0.38, 0.22, 0.18, 0.12, 0.10])
        else:
            weights = np.array([0.34, 0.20, 0.20, 0.16, 0.10])
        weights = weights / weights.sum()
        cat_revs = np.round(q_total * weights, -1)
        for cat, rev in zip(categories, cat_revs):
            rows.append({"quarter": q, "category": cat, "revenue": rev})

    cat_df = pd.DataFrame(rows)
    return df, cat_df


sales_df, cat_df = generate_mock_sales()
quarters = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]

# ---------- HEADER ----------
st.markdown("### Sales Analytics")
st.caption(
    "Detailed insights into your soda sales performance, trends, and AI-powered forecasts."
)

# ---------- QUARTER SELECTION ----------
_, top_right = st.columns([3, 2])

with top_right:
    quarter_idx = st.session_state.get("selected_quarter_idx", 1)  # default Q2
    selected_quarter = st.radio(
        "Quarter",
        quarters,
        index=quarter_idx,
        horizontal=True,
        key="quarter_radio",
    )
    st.session_state["selected_quarter_idx"] = quarters.index(selected_quarter)

    q_status = (
        "Actual" if selected_quarter in ["Q1 2024", "Q2 2024"] else "AI Predicted"
    )
    badge_class = "badge-actual" if q_status == "Actual" else "badge-predicted"

    st.markdown(
        f"""
        <div class="guru-quarter-meta">
            Viewing <strong>{selected_quarter}</strong>
            <span class="{badge_class}">{q_status}</span><br/>
            Past quarters use historical data; future quarters use AI-style projections based on the trend.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Filter for quarter
q_mask = sales_df["quarter"] == selected_quarter
q_df = sales_df[q_mask].copy()

# For YTD we take all months up to end of quarter
q_end_month = q_df["month"].max()
ytd_mask = sales_df["month"] <= q_end_month
ytd_df = sales_df[ytd_mask]

# ---------- KPI CALCULATIONS ----------
q_total_revenue = q_df["current_revenue"].sum()
# crude prev quarter logic just for demo
q_prev = (
    "Q1 2024"
    if selected_quarter == "Q2 2024"
    else "Q2 2024"
    if selected_quarter == "Q3 2024"
    else "Q3 2024"
)
if selected_quarter == "Q1 2024":
    prev_q_total = q_total_revenue * 0.9
else:
    prev_q_total = sales_df.loc[
        sales_df["quarter"] == q_prev, "current_revenue"
    ].sum()

month_revenue = q_df.iloc[-1]["current_revenue"]
month_prev = prev_q_total / len(q_df) if len(q_df) else 0
monthly_delta = (month_revenue - month_prev) / month_prev * 100 if month_prev else 0

ytd_revenue = ytd_df["current_revenue"].sum()

# Target achievement
q_target = q_df["target"].sum()
target_ach = (q_total_revenue / q_target * 100) if q_target else 0

# Projected growth vs previous year same quarter
prev_year_q = q_df["prev_year_revenue"].sum()
proj_growth = (
    (q_total_revenue - prev_year_q) / prev_year_q * 100 if prev_year_q else 0
)

# ---------- KPI ROW ----------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown('<div class="guru-kpi-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="guru-kpi-label">$ Monthly Revenue</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="guru-kpi-value">${month_revenue:,.0f}</div>',
        unsafe_allow_html=True,
    )
    cls = "guru-kpi-delta-pos" if monthly_delta >= 0 else "guru-kpi-delta-neg"
    st.markdown(
        f'<div class="{cls}">{monthly_delta:+.1f}% vs previous quarter</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with k2:
    st.markdown('<div class="guru-kpi-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="guru-kpi-label">Target Achievement</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="guru-kpi-value">{target_ach:.1f}%</div>',
        unsafe_allow_html=True,
    )
    label = (
        "Achieved"
        if target_ach >= 100
        else "On track"
        if target_ach >= 95
        else "Below target"
    )
    st.markdown(
        f'<span style="font-size:0.75rem;padding:2px 8px;border-radius:999px;'
        f'background:#f9fafb;color:#020617;">{label}</span>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with k3:
    st.markdown('<div class="guru-kpi-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="guru-kpi-label">YTD Revenue</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="guru-kpi-value">${ytd_revenue:,.0f}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="guru-kpi-delta-pos">Cumulative through quarter end</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with k4:
    st.markdown('<div class="guru-kpi-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="guru-kpi-label">Projected Growth</div>',
        unsafe_allow_html=True,
    )
    cls = "guru-kpi-delta-pos" if proj_growth >= 0 else "guru-kpi-delta-neg"
    st.markdown(
        f'<div class="guru-kpi-value">{proj_growth:+.1f}%</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="{cls}">vs same quarter last year</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("")

# ---------- REVENUE PERFORMANCE ANALYSIS ----------
st.markdown("#### Revenue Performance Analysis")
st.caption(
    "Monthly revenue with targets, year-over-year comparison, and forecast. "
    "Hover to see exact values; future quarters blend historical trend with AI-style projections."
)

fig = go.Figure()

# Area for current revenue (selected quarter)
fig.add_trace(
    go.Scatter(
        x=q_df["month_name"],
        y=q_df["current_revenue"],
        mode="lines+markers",
        name="Current Revenue",
        line=dict(color="#22c55e", width=3),
        fill="tozeroy",
        hovertemplate="Month: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>",
    )
)

# Forecast
fig.add_trace(
    go.Scatter(
        x=q_df["month_name"],
        y=q_df["forecast"],
        mode="lines+markers",
        name="Forecast",
        line=dict(color="#0ea5e9", width=2, dash="dot"),
        hovertemplate="Month: %{x}<br>Forecast: $%{y:,.0f}<extra></extra>",
    )
)

# Target
fig.add_trace(
    go.Scatter(
        x=q_df["month_name"],
        y=q_df["target"],
        mode="lines",
        name="Monthly Target",
        line=dict(color="#22c55e", width=2, dash="dash"),
        hovertemplate="Month: %{x}<br>Target: $%{y:,.0f}<extra></extra>",
    )
)

# Previous year
fig.add_trace(
    go.Scatter(
        x=q_df["month_name"],
        y=q_df["prev_year_revenue"],
        mode="lines",
        name="Previous Year",
        line=dict(color="#38bdf8", width=2),
        hovertemplate="Month: %{x}<br>Prev year: $%{y:,.0f}<extra></extra>",
    )
)

fig.update_layout(
    margin=dict(l=0, r=0, t=8, b=0),
    height=340,
    plot_bgcolor="#020617",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="", showgrid=False),
    yaxis=dict(
        title="",
        showgrid=True,
        gridcolor="rgba(148,163,184,0.2)",
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
    ),
)

st.plotly_chart(fig, use_container_width=True)

# ---------- QUARTERLY CATEGORY BREAKDOWN ----------
st.markdown("#### Quarterly Sales by Category")
st.caption(
    f"Soda category mix for {selected_quarter}. Use hover to explore revenue by flavor segment."
)

q_cat = cat_df[cat_df["quarter"] == selected_quarter].copy()
q_cat = q_cat.sort_values("revenue", ascending=True)

fig_bar = px.bar(
    q_cat,
    x="revenue",
    y="category",
    orientation="h",
    color="category",
    color_discrete_sequence=[
        "#16a34a",
        "#22c55e",
        "#38bdf8",
        "#0ea5e9",
        "#6366f1",
    ],
    labels={"revenue": "Revenue ($)", "category": "Category"},
    height=320,
)

fig_bar.update_layout(
    margin=dict(l=0, r=0, t=10, b=0),
    plot_bgcolor="#020617",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
)
fig_bar.update_xaxes(gridcolor="rgba(148,163,184,0.2)")

st.plotly_chart(fig_bar, use_container_width=True)

# ---------- INSIGHTS ----------
left_i, right_i = st.columns([2, 1])

with left_i:
    st.markdown("#### 💡 Quarter highlights")
    if selected_quarter in ["Q1 2024", "Q2 2024"]:
        st.write(
            "- Revenue is trending upward quarter-over-quarter with solid growth vs last year.\n"
            "- Targets are mostly on track; watch for any months where revenue dips below the dashed target line.\n"
            "- Category mix is cola-heavy — good for stability but watch for growing demand in energy drinks."
        )
    else:
        st.write(
            "- Forecast suggests continued growth if current momentum continues.\n"
            "- Consider testing price or promo changes on high-margin categories like Energy Drinks.\n"
            "- Use these projections to pre-plan inventory and staffing for upcoming peaks."
        )

with right_i:
    st.markdown("#### 📌 Quick actions")
    st.write(
        "- Check low-stock SKUs in top categories.\n"
        "- Align promos with the strongest growth months.\n"
        "- Compare actuals vs forecast after each month to refine predictions."
    )
