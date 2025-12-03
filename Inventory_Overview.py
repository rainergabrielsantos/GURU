import streamlit as st
import pandas as pd
from datetime import date, timedelta

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Inventory Overview",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",  # optional
)
# ---------- STATE ----------
if "inventory_view" not in st.session_state:
    # "overview" or "manage"
    st.session_state.inventory_view = "overview"

if "inventory_filter" not in st.session_state:
    # "all", "critical", or "low"
    st.session_state.inventory_filter = "all"

# products added during this session
if "new_products" not in st.session_state:
    st.session_state.new_products = []

# ---------- GLOBAL STYLES ----------
st.markdown(
    """
<style>
.stApp {
    background-color: #050608;
    color: #f5f5f5;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 3.5rem;   /* more space so top bar doesn't cover content */
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}

/* You can leave sidebar styles here if you like how the default nav looks */
section[data-testid="stSidebar"] {
    background-color: #050608;
    border-right: 1px solid #222;
}

.card-row {
    display: flex;
    gap: 1.25rem;
    margin-top: 0.75rem;
}

.metric-card {
    flex: 1;
    background: #111827;
    border-radius: 0.75rem;
    padding: 1rem 1.25rem;
    border: 1px solid #1f2937;
    position: relative;
}
.metric-title {
    font-size: 0.8rem;
    color: #9ca3af;
    margin-bottom: 0.75rem;
}

.metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}

.metric-subtext {
    font-size: 0.7rem;
    color: #6b7280;
}

.metric-alert {
    color: #f97373;
    font-size: 1.6rem;
    font-weight: 700;
}

.metric-low {
    color: #facc15;
    font-size: 1.6rem;
    font-weight: 700;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.page-title {
    font-size: 1.1rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.page-subtitle {
    font-size: 0.8rem;
    color: #9ca3af;
    margin-bottom: 0.75rem;
}

.inventory-header-row {
    margin-top: 1.8rem;
    margin-bottom: 0.75rem;
}

.inventory-header-title {
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 0.15rem;
}

.inventory-header-subtitle {
    font-size: 0.75rem;
    color: #9ca3af;
}


.tab-button {
    background: #111827;
    border-radius: 999px;
    border: 1px solid #1f2937;
    padding: 0.35rem 0.9rem;
    font-size: 0.75rem;
    color: #e5e7eb;
    cursor: pointer;
    margin-right: 0.25rem;
}

.tab-button.active {
    background: #10b981;
    border-color: #10b981;
    color: #022c22;
    font-weight: 600;
}

.dataframe tbody tr td {
    font-size: 0.78rem;
    padding: 0.35rem 0.25rem;
}

.dataframe thead tr th {
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    border-bottom: 1px solid #1f2937;
}

.chat-bubble {
    position: fixed;
    right: 1.5rem;
    bottom: 1.5rem;
    background: #10b981;
    color: #022c22;
    border-radius: 999px;
    padding: 0.55rem 0.9rem;
    font-size: 0.78rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
    box-shadow: 0 14px 40px rgba(0,0,0,0.6);
    z-index: 999;
}

.chat-bubble-subtext {
    font-size: 0.65rem;
    color: #022c22;
    opacity: 0.8;
    margin-top: -2px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
col_left, col_right = st.columns([4, 1])

with col_left:
    st.markdown(
        """
<div class="page-header">
  <div>
    <div class="page-title">Inventory Overview</div>
    <div class="page-subtitle">
      Monitor stock levels, track inventory value, and manage product availability.
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

with col_right:
    st.write("")
    st.write("")
    if st.button("➕  Add Product", width='stretch'):
        st.session_state.inventory_view = "manage"


# ---------- METRIC CARDS ----------
st.markdown(
    """
<div class="card-row">
  <div class="metric-card">
    <div class="metric-title">Total Inventory Value</div>
    <div class="metric-value">$1,504</div>
    <div class="metric-subtext">View top contributors · Click to view</div>
  </div>

  <div class="metric-card">
    <div class="metric-title">Critical Stock</div>
    <div class="metric-alert">1</div>
    <div class="metric-subtext">Items need immediate attention · Click to view</div>
  </div>

  <div class="metric-card">
    <div class="metric-title">Low Stock</div>
    <div class="metric-low">1</div>
    <div class="metric-subtext">Items below minimum threshold · Click to view</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- INVENTORY HEADER ----------
st.markdown(
    """
<div class="inventory-header-row">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <div>
      <div class="inventory-header-title">Product Inventory</div>
      <div class="inventory-header-subtitle">
        Manage your product stock levels and details.
      </div>
    </div>
    <div>
      <button class="tab-button active">Full Inventory</button>
      <button class="tab-button">Alerts & Visuals</button>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- MANAGE / ADD PRODUCT VIEW ----------
if st.session_state.inventory_view == "manage":
    st.markdown("### Add / Manage Product")

    with st.form("add_product_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Product name *")
            pid = st.text_input("Product ID / SKU")
            category = st.text_input("Category")
        with col2:
            stock = st.number_input("Current stock", min_value=0, step=1, value=0)
            min_stock = st.number_input("Minimum stock", min_value=0, step=1, value=0)
            value = st.number_input("Inventory value ($)", min_value=0.0, step=1.0, value=0.0)
            status = st.selectbox("Status", ["good", "low", "critical"])

        submitted = st.form_submit_button("Save product")

    if submitted:
        if not name:
            st.error("Please enter at least a product name.")
        else:
            st.session_state.new_products.append(
                {
                    "Product": name,
                    "ID": pid or f"NEW{len(st.session_state.new_products)+1}",
                    "Category": category or "Uncategorized",
                    "Stock": stock,
                    "Min Stock": min_stock,
                    "Value": value,
                    "Status": status,
                    "Actions": "Restock  ·  ✏️  ·  🗑",
                }
            )
            st.success(f"✅ Added **{name}** to inventory (this session).")

    st.markdown("---")
    if st.button("⬅️ Back to inventory overview"):
        st.session_state.inventory_view = "overview"

    # Stop here so the overview layout doesn't render at the same time
    st.stop()


# ---------- SEARCH + FILTER ----------
search_col, filter_col, _ = st.columns([3, 1.3, 2])

with search_col:
    search_query = st.text_input(
        "Search products",
        value="",
        placeholder="Search products...",
        label_visibility="collapsed",
    )

with filter_col:
    selected_category = st.selectbox(
        "All Categories",
        ["All Categories", "Citrus", "Lemon-Lime", "Cola", "Specialty Cola", "Fruit Soda", "Uncategorized"],
        index=0,
        label_visibility="collapsed",
    )

# ---------- DATA ----------
data = [
    {
        "Product": "Mountain Dew 16oz Bottles",
        "ID": "P005",
        "Category": "Citrus",
        "Stock": 72,
        "Min Stock": 30,
        "Value": 129,
        "Status": "good",
        "Actions": "Restock  ·  ✏️  ·  🗑",
    },
    {
        "Product": "Sprite 20oz Bottles",
        "ID": "P003",
        "Category": "Lemon-Lime",
        "Stock": 58,
        "Min Stock": 25,
        "Value": 110,
        "Status": "good",
        "Actions": "Restock  ·  ✏️  ·  🗑",
    },
    {
        "Product": "Coca-Cola Classic 12oz Cans (24-pack)",
        "ID": "P001",
        "Category": "Cola",
        "Stock": 45,
        "Min Stock": 20,
        "Value": 855,
        "Status": "good",
        "Actions": "Restock  ·  ✏️  ·  🗑",
    },
    {
        "Product": "Pepsi 2-Liter Bottles",
        "ID": "P002",
        "Category": "Cola",
        "Stock": 32,
        "Min Stock": 15,
        "Value": 80,
        "Status": "good",
        "Actions": "Restock  ·  ✏️  ·  🗑",
    },
    {
        "Product": "Dr Pepper 12oz Cans (6-pack)",
        "ID": "P004",
        "Category": "Specialty Cola",
        "Stock": 28,
        "Min Stock": 15,
        "Value": 140,
        "Status": "good",
        "Actions": "Restock  ·  ✏️  ·  🗑",
    },
    {
        "Product": "Fanta Orange 12oz Cans (12-pack)",
        "ID": "P006",
        "Category": "Fruit Soda",
        "Stock": 22,
        "Min Stock": 20,
        "Value": 154,
        "Status": "low",
        "Actions": "Restock  ·  ✏️  ·  🗑",
    },
]

df = pd.DataFrame(data)

# include any products added via the Add Product form this session
if st.session_state.new_products:
    df = pd.concat([df, pd.DataFrame(st.session_state.new_products)], ignore_index=True)


# apply search & category filters
if search_query:
    df = df[df["Product"].str.contains(search_query, case=False, na=False)]

if selected_category != "All Categories":
    df = df[df["Category"] == selected_category]

# apply metric-card filter
if st.session_state.inventory_filter == "critical":
    df = df[df["Status"] == "critical"]
elif st.session_state.inventory_filter == "low":
    df = df[df["Status"] == "low"]
# "all" = no extra filter



# ---------- METRICS (based on ALL inventory) ----------
total_value = float(df["Value"].sum()) if not df.empty else 0.0
critical_count = int((df["Status"] == "critical").sum())
low_count = int((df["Status"] == "low").sum())
total_products = len(df)

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    if st.button(
        f"💰 Total Inventory Value\n${total_value:,.0f} · {total_products} products",
        key="filter_all",
        width='stretch',
    ):
        st.session_state.inventory_filter = "all"

with metric_col2:
    if st.button(
        f"🚨 Critical Stock\n{critical_count} products · Click to view",
        key="filter_critical",
        width='stretch',
    ):
        st.session_state.inventory_filter = "critical"

with metric_col3:
    if st.button(
        f"⚠️ Low Stock\n{low_count} products · Click to view",
        key="filter_low",
        width='stretch',
    ):
        st.session_state.inventory_filter = "low"

st.markdown("")  # small spacing

# filters
if search_query:
    df = df[df["Product"].str.contains(search_query, case=False, na=False)]

if selected_category != "All Categories":
    df = df[df["Category"] == selected_category]


def status_color(val):
    if val == "good":
        color = "#16a34a"
        bg = "#052e16"
    elif val == "low":
        color = "#facc15"
        bg = "#3f3f0e"
    else:
        color = "#d1d5db"
        bg = "#111827"
    return (
        f"background-color: {bg}; color: {color}; "
        "border-radius: 999px; text-align:center;"
    )


df_filtered = df.copy()
if st.session_state.inventory_filter == "critical":
    df_filtered = df_filtered[df_filtered["Status"] == "critical"]
elif st.session_state.inventory_filter == "low":
    df_filtered = df_filtered[df_filtered["Status"] == "low"]

styled_df = (
    df_filtered.style
    .format({"Value": "${:,.0f}", "Stock": "{:,.0f} units", "Min Stock": "{:,.0f}"})
    .map(status_color, subset=["Status"])
)

# View selector: Full table or Alerts & Visuals
view_mode = st.radio(
    "View",
    ["Full Inventory", "Alerts & Visuals"],
    horizontal=True,
    label_visibility="collapsed",
)

if view_mode == "Full Inventory":
    st.dataframe(styled_df, width='stretch', hide_index=True)
else:
    alerts_df = df[df["Status"] != "good"].copy()
    st.subheader("Inventory alerts")
    st.dataframe(alerts_df, width='stretch', hide_index=True)

    # Example: simple bar chart of stock vs min
    chart_df = alerts_df[["Product", "Stock", "Min Stock"]].set_index("Product")
    st.bar_chart(chart_df)

# ---------- CHAT BUBBLE ----------
st.markdown(
    """
<div class="chat-bubble">
  <div>💬</div>
  <div>
    <div>Ask GURU!</div>
    <div class="chat-bubble-subtext">AI insights</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
