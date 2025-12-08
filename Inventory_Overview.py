import streamlit as st
import pandas as pd
from utils import apply_custom_theme

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Inventory Overview",
    page_icon="📦",
    layout="wide",
)

apply_custom_theme()

# ---------- HELPERS & INITIAL DATA ----------

def compute_status_label(stock: float, min_stock: float) -> str:
    """Return a human-readable status label based on stock vs minimum."""
    try:
        stock = float(stock)
        min_stock = float(min_stock)
    except (TypeError, ValueError):
        stock = 0
        min_stock = 0

    if stock < min_stock:
        return "🔴 Critical"
    elif stock <= min_stock * 1.5:
        return "🟠 Low"
    else:
        return "🟢 Good"


INITIAL_DATA = [
    {
        "Product": "Coca-Cola Classic 12oz Cans (24-pack)",
        "ID": "CC-12C-24",
        "Category": "Cola",
        "Stock": 45,
        "Min Stock": 20,
        "Value": 855,
    },
    {
        "Product": "Sprite Lemon-Lime 20oz Bottles (12-pack)",
        "ID": "SP-20B-12",
        "Category": "Lemon-Lime",
        "Stock": 58,
        "Min Stock": 25,
        "Value": 110,
    },
    {
        "Product": "Fanta Orange 12oz Cans (12-pack)",
        "ID": "FA-12C-12",
        "Category": "Fruit Soda",
        "Stock": 22,
        "Min Stock": 20,
        "Value": 154,
    },
    {
        "Product": "Dr Pepper 12oz Cans (6-pack)",
        "ID": "DP-12C-6",
        "Category": "Specialty Cola",
        "Stock": 28,
        "Min Stock": 15,
        "Value": 140,
    },
    {
        "Product": "Mountain Dew 16oz Bottles (6-pack)",
        "ID": "MD-16B-6",
        "Category": "Citrus",
        "Stock": 72,
        "Min Stock": 30,
        "Value": 129,
    },
]

# ---------- SESSION STATE BOOTSTRAP ----------

if "inventory_df" not in st.session_state:
    base_df = pd.DataFrame(INITIAL_DATA)
    base_df["Status"] = base_df.apply(
        lambda r: compute_status_label(r["Stock"], r["Min Stock"]), axis=1
    )
    st.session_state.inventory_df = base_df

if "inventory_history" not in st.session_state:
    st.session_state.inventory_history = []

if "inventory_mode" not in st.session_state:
    st.session_state.inventory_mode = "view"  # "view" | "add" | "manage"

df = st.session_state.inventory_df

# ---------- STYLES ----------
st.markdown(
    """
<style>
.block-container {
    padding-top: 1.0rem;
}

/* Metric cards */
.inv-card-row {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}
.inv-metric-card {
    background: #050b16;
    border-radius: 16px;
    border: 1px solid #111827;
    padding: 0.8rem 1.0rem;
    box-shadow: 0 14px 30px rgba(0,0,0,0.55);
}
.inv-metric-title {
    font-size: 0.8rem;
    color: #9ca3af;
    margin-bottom: 0.1rem;
}
.inv-metric-value {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.1rem;
}
.inv-metric-sub {
    font-size: 0.75rem;
    color: #6b7280;
}

/* Action buttons row */
.inv-actions-row {
    display: flex;
    justify-content: flex-end;
    gap: 0.4rem;
    margin-bottom: 0.4rem;
}

/* Table wrapper */
.inv-table-card {
    background: #050b16;
    border-radius: 18px;
    border: 1px solid #111827;
    padding: 0.7rem 0.8rem 0.5rem;
    box-shadow: 0 18px 40px rgba(0,0,0,0.65);
}

/* Add / manage sections */
.inv-section-card {
    background: #050b16;
    border-radius: 18px;
    border: 1px solid #111827;
    padding: 1.0rem 1.1rem 1.0rem;
    box-shadow: 0 18px 40px rgba(0,0,0,0.65);
    margin-top: 0.5rem;
}

</style>
""",
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
st.markdown("### 📦 Inventory Overview")
st.caption("Track soda inventory levels, low-stock alerts, and product performance.")

# ---------- ACTIONS & FILTERS ----------
col_filters, col_actions = st.columns([2, 2])

with col_filters:
    search_query = st.text_input("Search products", placeholder="Search by name or ID...")
    categories = ["All Categories"] + sorted(df["Category"].unique().tolist())
    selected_category = st.selectbox("Category filter", categories, index=0)

with col_actions:
    st.markdown('<div class="inv-actions-row">', unsafe_allow_html=True)
    add_clicked = st.button("➕  Add Product")
    manage_clicked = st.button("🛠  Manage Inventory")
    view_clicked = st.button("👁  Back to Overview")
    st.markdown("</div>", unsafe_allow_html=True)

    if add_clicked:
        st.session_state.inventory_mode = "add"
    elif manage_clicked:
        st.session_state.inventory_mode = "manage"
    elif view_clicked:
        st.session_state.inventory_mode = "view"

mode = st.session_state.inventory_mode

# ---------- METRICS (always from full inventory) ----------
total_value = df["Value"].sum() if "Value" in df.columns else 0
critical_count = (df["Status"].str.contains("Critical")).sum()
low_count = (df["Status"].str.contains("Low")).sum()

st.markdown(
    f"""
<div class="inv-card-row">
  <div class="inv-metric-card">
    <div class="inv-metric-title">Total Inventory Value</div>
    <div class="inv-metric-value">${total_value:,.0f}</div>
    <div class="inv-metric-sub">Across all soda SKUs in stock.</div>
  </div>
  <div class="inv-metric-card">
    <div class="inv-metric-title">Critical Stock Items</div>
    <div class="inv-metric-value">{critical_count}</div>
    <div class="inv-metric-sub">Stock below minimum level.</div>
  </div>
  <div class="inv-metric-card">
    <div class="inv-metric-title">Low Stock Items</div>
    <div class="inv-metric-value">{low_count}</div>
    <div class="inv-metric-sub">Approaching minimum threshold.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================
#   VIEW MODE (READ-ONLY)
# =========================
if mode == "view":
    view_df = df.copy()

    if search_query:
        view_df = view_df[
            view_df["Product"].str.contains(search_query, case=False, na=False)
            | view_df["ID"].str.contains(search_query, case=False, na=False)
        ]

    if selected_category != "All Categories":
        view_df = view_df[view_df["Category"] == selected_category]

    st.markdown("#### Current Inventory")

    st.markdown('<div class="inv-table-card">', unsafe_allow_html=True)
    styled = view_df.style.hide(axis="index")
    st.dataframe(styled, use_container_width=True, height=400)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
#   ADD PRODUCT MODE
# =========================
elif mode == "add":
    st.markdown("#### ➕ Add a New Product")
    st.markdown(
        "Use this form to quickly add a new soda SKU to your inventory. "
        "Status is calculated automatically from stock levels."
    )

    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("Product name*", placeholder="e.g., Coca-Cola Cherry 12oz Cans")
            sku_id = st.text_input("Product ID / SKU", placeholder="e.g., CC-CH-12C-12")
            category = st.selectbox(
                "Category",
                ["Cola", "Lemon-Lime", "Citrus", "Fruit Soda", "Specialty Cola", "Energy Drink"],
            )
        with col2:
            stock = st.number_input("Current stock", min_value=0, step=1, value=0)
            min_stock = st.number_input("Minimum stock threshold", min_value=0, step=1, value=10)
            value = st.number_input("Inventory value ($)", min_value=0.0, step=1.0, value=0.0)

        submitted = st.form_submit_button("Save Product")

    if submitted:
        if not product_name.strip():
            st.error("Please enter a product name.")
        else:
            new_row = {
                "Product": product_name.strip(),
                "ID": sku_id.strip(),
                "Category": category,
                "Stock": int(stock),
                "Min Stock": int(min_stock),
                "Value": float(value),
            }
            new_row["Status"] = compute_status_label(new_row["Stock"], new_row["Min Stock"])

            # Save snapshot for undo before modifying
            st.session_state.inventory_history.append(df.to_dict("records"))

            st.session_state.inventory_df = pd.concat(
                [df, pd.DataFrame([new_row])],
                ignore_index=True,
            )
            st.success(f"Added product: {new_row['Product']}")
            st.session_state.inventory_mode = "view"
            st.rerun()

# =========================
#   MANAGE INVENTORY MODE
# =========================
elif mode == "manage":
    st.markdown("#### 🛠 Manage Inventory")
    st.markdown(
        "Use this view for **bulk edits and removals**. Edits apply immediately. "
        "Use **Undo last change** if you remove or edit items by mistake."
    )

    # Undo button
    if st.session_state.inventory_history:
        if st.button("↩️ Undo last change"):
            last_snapshot = st.session_state.inventory_history.pop()
            st.session_state.inventory_df = pd.DataFrame(last_snapshot)
            st.rerun()

    work_df = st.session_state.inventory_df.copy()
    work_df["Remove"] = False  # delete flags for this render only

    edited = st.data_editor(
        work_df,
        hide_index=False,
        num_rows="fixed",  # adding is done via Add Product form
        column_config={
            "Product": st.column_config.TextColumn("Product", required=True),
            "ID": st.column_config.TextColumn("ID / SKU"),
            "Category": st.column_config.SelectboxColumn(
                "Category",
                options=["Cola", "Lemon-Lime", "Citrus", "Fruit Soda", "Specialty Cola", "Energy Drink"],
            ),
            "Stock": st.column_config.NumberColumn("Stock", min_value=0, step=1),
            "Min Stock": st.column_config.NumberColumn("Min Stock", min_value=0, step=1),
            "Value": st.column_config.NumberColumn("Value ($)", min_value=0, step=1),
            "Status": st.column_config.TextColumn("Status", disabled=True),
            "Remove": st.column_config.CheckboxColumn("Remove", default=False),
        },
        key="inventory_manage_editor",
    )

    # Build new df and collect removals
    new_df = pd.DataFrame(
        columns=["Product", "ID", "Category", "Stock", "Min Stock", "Value", "Status"]
    )
    to_remove_idxs = []
    for idx, row in edited.iterrows():
        if row.get("Remove", False):
            to_remove_idxs.append(idx)

        if pd.isna(row.get("Product", "")):
            continue

        rd = {
            "Product": row["Product"],
            "ID": row.get("ID", ""),
            "Category": row.get("Category", ""),
            "Stock": int(row.get("Stock", 0) or 0),
            "Min Stock": int(row.get("Min Stock", 0) or 0),
            "Value": float(row.get("Value", 0) or 0.0),
        }
        rd["Status"] = compute_status_label(rd["Stock"], rd["Min Stock"])
        new_df.loc[idx] = rd

    st.session_state.inventory_df = new_df

    if to_remove_idxs:
        names = new_df.loc[to_remove_idxs, "Product"].astype(str).tolist()
        st.warning(
            f"You're about to permanently remove **{len(to_remove_idxs)}** product(s): "
            + ", ".join(names)
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Confirm delete"):
                # Save snapshot for undo, then drop
                st.session_state.inventory_history.append(new_df.to_dict("records"))
                st.session_state.inventory_df = new_df.drop(index=to_remove_idxs)
                st.success("Selected products removed.")
                st.rerun()
        with c2:
            if st.button("❌ Cancel"):
                st.rerun()
