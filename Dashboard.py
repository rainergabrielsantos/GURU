import streamlit as st
import pandas as pd
from utils import apply_custom_theme


# ---------- PAGE SETUP ----------
st.set_page_config(layout="wide")
apply_custom_theme()

# ========= PAGE SETUP =========
st.title("Dashboard")

st.caption(
    "High-level overview of your business performance — revenue, sales, products, "
    "customers, and key trends."
)

# ========= MOCK DATA (similar to your React mockDashboardData) =========
mock_dashboard_data = {
    "totalRevenue": 125_420,
    "totalSales": 1247,
    "totalProducts": 342,
    "totalCustomers": 856,
    "revenueChange": 12.5,
    "salesChange": 8.3,
    "productsChange": -2.1,
    "customersChange": 5.7,
}

revenue_trend = pd.DataFrame(
    {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Revenue": [18_200, 19_450, 17_800, 20_100, 21_300, 22_800, 25_770],
    }
)

top_products = [
    {"name": "Coca-Cola 2-Liter", "sales": 320, "revenue": 1_920, "growth": 14},
    {"name": "Pepsi 2-Liter", "sales": 280, "revenue": 1_680, "growth": 11},
    {"name": "Sprite 20oz Bottles", "sales": 210, "revenue": 1_260, "growth": 9},
    {"name": "Fanta Orange 12-Pack", "sales": 180, "revenue": 1_440, "growth": 7},
    {"name": "Monster Energy 16oz", "sales": 110, "revenue": 990, "growth": 5},
]

# ========= HERO / OVERVIEW CARD =========
with st.container():
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # A “hero card” similar to your Figma gradient card
        st.markdown(
            """
            <div style="
                padding: 18px 18px 16px;
                border-radius: 16px;
                background: linear-gradient(135deg, #020617, #0f172a);
                color: white;
                border: 1px solid rgba(148, 163, 184, 0.4);
            ">
                <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 8px;">
                    <span style="
                        font-size: 11px;
                        padding: 2px 10px;
                        border-radius: 999px;
                        background: rgba(15, 118, 110, 0.2);
                        border: 1px solid rgba(45, 212, 191, 0.7);
                    ">
                        Live overview
                    </span>
                    <span style="font-size: 11px; opacity: 0.8;">
                        Updated with latest sales & inventory
                    </span>
                </div>
                <h3 style="margin: 0 0 4px; font-size: 20px;">Business performance overview</h3>
                <p style="margin: 0; font-size: 13px; opacity: 0.85;">
                    Track revenue, orders, active products, and customer activity at a glance. 
                    This section mirrors the hero summary from your React dashboard.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown("")

# ========= SUMMARY KPI CARDS =========
st.markdown("### Key metrics")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Total Revenue",
        f"${mock_dashboard_data['totalRevenue']:,}",
        f"{mock_dashboard_data['revenueChange']}% vs last month",
    )

with m2:
    st.metric(
        "Total Sales",
        f"{mock_dashboard_data['totalSales']:,}",
        f"{mock_dashboard_data['salesChange']}% vs last month",
    )

with m3:
    st.metric(
        "Products in Catalog",
        f"{mock_dashboard_data['totalProducts']:,}",
        f"{mock_dashboard_data['productsChange']}% vs last month",
    )

with m4:
    st.metric(
        "Customers",
        f"{mock_dashboard_data['totalCustomers']:,}",
        f"{mock_dashboard_data['customersChange']}% vs last month",
    )

st.markdown("---")

# ========= REVENUE TREND + SNAPSHOT =========
st.markdown("### Revenue & activity")

left, right = st.columns([2, 1])

with left:
    st.subheader("Weekly revenue")
    st.caption("Line chart version of your main performance chart from the React dashboard.")
    st.line_chart(revenue_trend.set_index("Day")["Revenue"])

with right:
    st.subheader("This week at a glance")
    avg_per_sale = mock_dashboard_data["totalRevenue"] / mock_dashboard_data["totalSales"]
    st.write(
        f"- **Total revenue:** `${mock_dashboard_data['totalRevenue']:,}`  \n"
        f"- **Total sales:** `{mock_dashboard_data['totalSales']:,}` orders  \n"
        f"- **Avg revenue per sale:** `~${avg_per_sale:.2f}`  \n"
    )

    st.markdown("#### Example category split")
    cat_df = pd.DataFrame(
        {
            "Category": [
                "Cola",
                "Lemon-Lime",
                "Citrus",
                "Specialty Cola",
                "Energy Drinks",
            ],
            "Share": [45, 25, 15, 10, 5],
        }
    )
    st.bar_chart(cat_df.set_index("Category")["Share"])

st.markdown("---")

# ========= TOP PRODUCTS LIST =========
st.markdown("### Top products this month")

for idx, product in enumerate(top_products, start=1):
    with st.container():
        c_main, c_stats = st.columns([3, 1])

        with c_main:
            st.markdown(
                f"**{idx}. {product['name']}**  \n"
                f"{product['sales']} sales · ${product['revenue']:,} revenue"
            )
            # progress bar as a simple “performance bar”
            st.progress(min(int(product["growth"]) + 20, 100))

        with c_stats:
            st.markdown(
                f"<div style='text-align:right;'>"
                f"<span style='font-size:13px; color:#16a34a;'>▲ "
                f"{product['growth']}% </span><br>"
                f"<span style='font-size:11px; opacity:0.7;'>vs last month</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

st.caption(
    "This ranked list with growth indicators mirrors the ‘Top Products’ style card "
    "from your Figma/React dashboard, adapted to Streamlit components."
)

# ========= RECENT ACTIVITY (SIMPLE PLACEHOLDER) =========
st.markdown("---")
st.markdown("### Recent activity")

st.info(
    "Here you can later show recent transactions, low-stock alerts, or AI-generated "
    "insights, just like the bottom sections of your original dashboard."
)
