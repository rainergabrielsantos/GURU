import streamlit as st
import pandas as pd
from utils import apply_custom_theme
from datetime import date, timedelta

# ---------- PAGE SETUP ----------
st.set_page_config(layout="wide")
apply_custom_theme()

# ===== PAGE SETUP =====
st.title("Sales & Analytics")

st.caption(
    "Deep-dive into revenue, volume, and category performance. "
    "This layout follows the structure of your React SalesAnalytics component: "
    "summary KPIs, time filters, trend chart, and category breakdown."
)

# ===== FILTER BAR (similar to your timeframe / compare controls) =====
col_time, col_compare = st.columns([2, 1])

with col_time:
    period = st.selectbox(
        "Time period",
        ["This week", "This month", "Last month", "Last 90 days", "Year to date"],
        index=1,
    )

with col_compare:
    comparison = st.selectbox(
        "Compare against",
        ["Previous period", "Same period last year", "No comparison"],
        index=0,
    )

st.markdown("")

# ===== MOCK DATA (adapted from your analytics mock data) =====
sales_summary = {
    "revenue": 125_420,
    "revenue_change": 12.5,
    "orders": 1247,
    "orders_change": 8.3,
    "avg_order_value": 100.6,
    "aov_change": 3.1,
    "repeat_customers": 34.7,  # %
    "repeat_change": 4.2,
}

daily_sales = pd.DataFrame(
    {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Revenue": [18_200, 19_450, 17_800, 20_100, 21_300, 22_800, 25_770],
        "Orders": [165, 178, 160, 182, 195, 210, 225],
    }
).set_index("Day")

category_sales = pd.DataFrame(
    {
        "Category": [
            "Cola",
            "Lemon-Lime",
            "Citrus",
            "Specialty Cola",
            "Energy Drinks",
        ],
        "Revenue": [37_100, 18_450, 12_800, 9_600, 7_470],
        "Units": [450, 260, 180, 140, 95],
    }
).set_index("Category")

# ===== KPI CARDS ROW (mirrors your top Card row) =====
st.markdown("### Key sales metrics")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Total Revenue",
        f"${sales_summary['revenue']:,}",
        f"{sales_summary['revenue_change']}% vs {comparison.lower()}",
    )

with k2:
    st.metric(
        "Total Orders",
        f"{sales_summary['orders']:,}",
        f"{sales_summary['orders_change']}% vs {comparison.lower()}",
    )

with k3:
    st.metric(
        "Avg Order Value",
        f"${sales_summary['avg_order_value']:.2f}",
        f"{sales_summary['aov_change']}% vs {comparison.lower()}",
    )

with k4:
    st.metric(
        "Repeat Customers",
        f"{sales_summary['repeat_customers']:.1f}%",
        f"{sales_summary['repeat_change']}% vs {comparison.lower()}",
    )

st.markdown("---")

# ===== MAIN CHART + CATEGORY BREAKDOWN (similar to your line + pie/side panel) =====
left, right = st.columns([2, 1])

with left:
    st.subheader("Revenue & orders trend")
    st.caption("Line chart equivalent of your combined revenue/orders chart in React.")
    st.line_chart(daily_sales[["Revenue", "Orders"]])

with right:
    st.subheader("Category performance")
    st.caption("Top revenue by category, similar to your category chart section.")
    st.bar_chart(category_sales["Revenue"])

    st.markdown("#### Category snapshot")
    top_cat = category_sales["Revenue"].idxmax()
    st.write(
        f"• **Top category:** {top_cat}  \n"
        f"• **Revenue:** ${category_sales.loc[top_cat, 'Revenue']:,}  \n"
        f"• **Units sold:** {category_sales.loc[top_cat, 'Units']:,}"
    )

st.markdown("---")

# ===== ADDITIONAL INSIGHTS SECTION (like the bottom cards in SalesAnalytics) =====
st.markdown("### Sales insights")

c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Momentum & growth")
    st.write(
        "- Revenue is trending upward across the selected period.\n"
        "- Orders are increasing toward the weekend, matching convenience-buying behavior.\n"
        "- Consider staffing and stock levels accordingly."
    )

with c2:
    st.markdown("#### Category strategy")
    st.write(
        "- Cola dominates your revenue mix — good for stability but risky for dependency.\n"
        "- Lemon-Lime and Citrus are strong secondary categories.\n"
        "- Energy Drinks have lower volume but likely higher margin — good for targeted promos."
    )

st.caption(
    "Later, you can replace these text insights with AI-generated commentary based on real data, "
    "similar to how your React view uses more advanced analytics."
)
