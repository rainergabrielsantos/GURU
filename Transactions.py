import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils import apply_custom_theme

apply_custom_theme()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Soda Store Transactions",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- MOCK SODA TRANSACTIONS DATA ----------
@st.cache_data
def generate_mock_transactions(n_days: int = 90):
    np.random.seed(123)

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=n_days - 1)
    dates = pd.date_range(start_date, end_date, freq="D")

    channels = ["Web", "Mobile App", "In-Store POS"]
    payment_methods = ["Credit Card", "PayPal", "Apple Pay", "Google Pay"]
    statuses = ["Completed", "Refunded", "Pending", "Failed", "Chargeback"]
    shipping_methods = ["Standard", "Express", "Local Delivery", "Pickup"]

    customers = [f"Customer #{i:04d}" for i in range(1, 201)]

    # Soda SKUs – all mock but soda-specific
    soda_skus = [
        {
            "sku": "CC-12C-24",
            "product_name": "Coca-Cola Classic 12oz Cans (24-pack)",
            "brand": "Coca-Cola",
            "flavor": "Cola",
            "category": "Regular Soda",
            "pack_size": 24,
            "unit_price": 1.10,   # per can
        },
        {
            "sku": "CC-20B-12",
            "product_name": "Coca-Cola Classic 20oz Bottles (12-pack)",
            "brand": "Coca-Cola",
            "flavor": "Cola",
            "category": "Regular Soda",
            "pack_size": 12,
            "unit_price": 1.80,
        },
        {
            "sku": "SP-20B-12",
            "product_name": "Sprite Lemon-Lime 20oz Bottles (12-pack)",
            "brand": "Sprite",
            "flavor": "Lemon-Lime",
            "category": "Citrus Soda",
            "pack_size": 12,
            "unit_price": 1.79,
        },
        {
            "sku": "FA-12C-12",
            "product_name": "Fanta Orange 12oz Cans (12-pack)",
            "brand": "Fanta",
            "flavor": "Orange",
            "category": "Fruit Soda",
            "pack_size": 12,
            "unit_price": 1.29,
        },
        {
            "sku": "DP-12C-6",
            "product_name": "Dr Pepper 12oz Cans (6-pack)",
            "brand": "Dr Pepper",
            "flavor": "Cola",
            "category": "Specialty Cola",
            "pack_size": 6,
            "unit_price": 1.39,
        },
        {
            "sku": "MD-16B-6",
            "product_name": "Mountain Dew 16oz Bottles (6-pack)",
            "brand": "Mountain Dew",
            "flavor": "Citrus",
            "category": "Citrus Soda",
            "pack_size": 6,
            "unit_price": 1.59,
        },
        {
            "sku": "CCZ-12C-12",
            "product_name": "Coke Zero 12oz Cans (12-pack)",
            "brand": "Coca-Cola",
            "flavor": "Cola",
            "category": "Zero Sugar",
            "pack_size": 12,
            "unit_price": 1.35,
        },
        {
            "sku": "EN-MON-16",
            "product_name": "Monster Energy 16oz Cans (4-pack)",
            "brand": "Monster",
            "flavor": "Energy",
            "category": "Energy Drink",
            "pack_size": 4,
            "unit_price": 2.99,
        },
    ]

    rows = []
    order_counter = 10000

    for date in dates:
        # more weekend orders
        day_factor = 1.3 if date.weekday() in [4, 5] else 1.0
        num_orders = np.random.poisson(35 * day_factor)

        for _ in range(num_orders):
            order_id = f"ORD-{order_counter}"
            order_counter += 1

            customer = np.random.choice(customers)
            channel = np.random.choice(channels, p=[0.5, 0.25, 0.25])
            payment_method = np.random.choice(payment_methods)

            # choose a primary soda SKU for this order
            sku_info = np.random.choice(soda_skus)
            pack_qty = np.random.randint(1, 6)  # 1–5 packs of that SKU

            units = pack_qty * sku_info["pack_size"]
            base_price_per_unit = sku_info["unit_price"]

            subtotal = units * base_price_per_unit

            # Discounts & fees
            discount = np.random.choice([0, 0, 0, 5, 10])  # mostly no discount
            shipping = np.random.choice(
                [0, 3.99, 6.99, 9.99],
                p=[0.25, 0.45, 0.2, 0.1],
            )
            tax = subtotal * 0.09

            total = subtotal + tax + shipping - discount
            total = max(1, total)

            # Status
            status = np.random.choice(
                statuses,
                p=[0.83, 0.06, 0.05, 0.04, 0.02],
            )

            is_refund = status in ["Refunded", "Chargeback"]

            # Fulfilment timeliness
            fulfillment_days = np.random.choice(
                [1, 2, 3, 4, 5, 7],
                p=[0.25, 0.3, 0.25, 0.1, 0.07, 0.03],
            )
            fulfillment_status = "Late" if fulfillment_days > 3 else "On-Time"

            new_vs_returning = np.random.choice(["New", "Returning"], p=[0.3, 0.7])
            shipping_method = np.random.choice(
                shipping_methods,
                p=[0.5, 0.2, 0.2, 0.1],
            )

            rows.append(
                {
                    "order_id": order_id,
                    "date": date.date(),
                    "customer_name": customer,
                    "channel": channel,
                    "payment_method": payment_method,
                    "status": status,
                    "items_count": units,              # total cans/bottles
                    "packs": pack_qty,                 # number of packs
                    "primary_sku": sku_info["sku"],
                    "product_name": sku_info["product_name"],
                    "brand": sku_info["brand"],
                    "flavor": sku_info["flavor"],
                    "category": sku_info["category"],
                    "pack_size": sku_info["pack_size"],
                    "subtotal": round(subtotal, 2),
                    "discount": round(discount, 2),
                    "shipping": round(shipping, 2),
                    "tax": round(tax, 2),
                    "total": round(total, 2),
                    "is_refund": is_refund,
                    "fulfillment_status": fulfillment_status,
                    "fulfillment_days": fulfillment_days,
                    "customer_type": new_vs_returning,
                    "shipping_method": shipping_method,
                }
            )

    df = pd.DataFrame(rows)
    return df


df = generate_mock_transactions()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.title("Soda Transaction Filters")

min_date = df["date"].min()
max_date = df["date"].max()
default_start = max_date - timedelta(days=29)

start_date, end_date = st.sidebar.date_input(
    "Date range",
    value=(default_start, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(start_date, (tuple, list)):
    start_date, end_date = start_date[0], start_date[1]

status_options = sorted(df["status"].unique())
channel_options = sorted(df["channel"].unique())
category_options = sorted(df["category"].unique())

selected_status = st.sidebar.multiselect(
    "Order Status",
    status_options,
    default=status_options,
)

selected_channels = st.sidebar.multiselect(
    "Sales Channel",
    channel_options,
    default=channel_options,
)

selected_categories = st.sidebar.multiselect(
    "Soda Category",
    category_options,
    default=category_options,
)

min_value = st.sidebar.slider(
    "Min Order Total ($)",
    min_value=float(df["total"].min()),
    max_value=float(df["total"].max()),
    value=float(df["total"].quantile(0.1)),
    step=1.0,
)

# Filtered dataframe
mask = (
    (df["date"] >= start_date)
    & (df["date"] <= end_date)
    & (df["status"].isin(selected_status))
    & (df["channel"].isin(selected_channels))
    & (df["category"].isin(selected_categories))
    & (df["total"] >= min_value)
)

filtered = df[mask].copy()

# ---------- PAGE HEADER ----------
st.title("Transactions")
st.caption(
    "View and analyze orders, high-value customers, and stock pressure from recent sales."
)

if filtered.empty:
    st.warning("No transactions for the selected filters. Try adjusting the date range or filters.")
    st.stop()

# ---------- KPIs ----------
completed = filtered[filtered["status"] == "Completed"]
refunded = filtered[filtered["is_refund"]]

gross_revenue = completed["total"].sum()
refund_amount = refunded["total"].sum()
net_revenue = gross_revenue - refund_amount

total_orders = len(filtered)
completed_orders = len(completed)
refund_orders = len(refunded)

refund_rate = refund_orders / completed_orders if completed_orders > 0 else 0
avg_order_value = completed["total"].mean() if completed_orders > 0 else 0

late_shipments = filtered[filtered["fulfillment_status"] == "Late"]
late_rate = len(late_shipments) / len(filtered) if len(filtered) > 0 else 0

new_customers_orders = filtered[filtered["customer_type"] == "New"]
returning_customers_orders = filtered[filtered["customer_type"] == "Returning"]

total_units_sold = completed["items_count"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Net Revenue (Completed - Refunds)", f"${net_revenue:,.2f}")

with col2:
    st.metric("Total Orders", f"{total_orders:,}")

with col3:
    st.metric("Avg Order Value (Completed)", f"${avg_order_value:,.2f}")

with col4:
    st.metric("Total Units Sold (Cans/Bottles)", f"{int(total_units_sold):,}")

st.markdown("---")

# ---------- SUMMARY STRIP ----------
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.write(
        f"**Completed Orders:** {completed_orders:,} | "
        f"Refunded / Chargeback Orders: {refund_orders:,}"
    )

with col_b:
    st.write(
        f"**Late Shipments:** {len(late_shipments):,} "
        f"({late_rate*100:.1f}% of filtered orders)"
    )

with col_c:
    new_share = (
        len(new_customers_orders) / len(filtered) * 100 if len(filtered) > 0 else 0
    )
    st.write(
        f"**New vs Returning:** {new_share:.1f}% new / {100 - new_share:.1f}% returning"
    )

st.markdown("### Recent Soda Transactions")

# ---------- TRANSACTIONS TABLE ----------
# Show newest first
filtered_display = filtered.sort_values("date", ascending=False)

# Format money columns
for col in ["subtotal", "discount", "shipping", "tax", "total"]:
    filtered_display[col] = filtered_display[col].map(lambda x: f"${x:,.2f}")

st.dataframe(
    filtered_display[
        [
            "order_id",
            "date",
            "customer_name",
            "status",
            "channel",
            "product_name",
            "category",
            "flavor",
            "packs",
            "items_count",
            "subtotal",
            "discount",
            "shipping",
            "tax",
            "total",
            "fulfillment_status",
            "fulfillment_days",
            "customer_type",
            "shipping_method",
        ]
    ].head(300),
    width='stretch',
    height=420,
)

# ---------- TOP CUSTOMERS ----------
st.markdown("### Top Customers (by Net Spend on Soda)")

customer_summary = (
    filtered.assign(
        effective_total=lambda d: np.where(
            d["is_refund"], -d["total"], d["total"]
        )
    )
    .groupby("customer_name", as_index=False)
    .agg(
        {
            "order_id": "nunique",
            "effective_total": "sum",
            "items_count": "sum",
        }
    )
    .rename(
        columns={
            "order_id": "orders",
            "effective_total": "net_spend",
            "items_count": "units_purchased",
        }
    )
    .sort_values("net_spend", ascending=False)
)

top_customers = customer_summary.head(10).copy()
top_customers["net_spend"] = top_customers["net_spend"].map(lambda x: f"${x:,.2f}")

st.dataframe(
    top_customers.reset_index(drop=True),
    width='stretch',
)

# ---------- TOP SODA SKUs (Sales Pressure on Inventory) ----------
st.markdown("### Top Soda SKUs by Units Sold (Inventory Pressure)")

sku_summary = (
    completed.groupby(
        ["primary_sku", "product_name", "brand", "flavor", "category", "pack_size"],
        as_index=False,
    )
    .agg(
        {
            "packs": "sum",
            "items_count": "sum",
            "total": "sum",
        }
    )
    .rename(
        columns={
            "packs": "total_packs_sold",
            "items_count": "units_sold",
            "total": "revenue",
        }
    )
    .sort_values("units_sold", ascending=False)
)

sku_summary_display = sku_summary.copy()
sku_summary_display["revenue"] = sku_summary_display["revenue"].map(
    lambda x: f"${x:,.2f}"
)

st.dataframe(
    sku_summary_display.head(10).reset_index(drop=True),
    width='stretch',
)

# ---------- RECOMMENDED ACTIONS ----------
st.markdown("### 💡 Recommended Actions Based on Soda Sales & Inventory Signals")

actions = []

# Refund rate
if refund_rate > 0.08:
    actions.append(
        f"- **Refund rate is {refund_rate*100:.1f}%**, which is relatively high. "
        "Review which soda SKUs are driving refunds (damaged cans, incorrect flavor, warm deliveries) "
        "and tighten packaging, handling, or product descriptions."
    )
else:
    actions.append(
        f"- **Refund rate is {refund_rate*100:.1f}%**, which is within a healthy range. "
        "Keep current quality and handling standards, and continue monitoring by flavor and brand."
    )

# Late shipments
if late_rate > 0.1:
    actions.append(
        f"- **{late_rate*100:.1f}% of orders are shipping late.** "
        "Check peak times for warehouse picks, cooler restocking, and courier pickup windows. "
        "Consider adjusting same-day / next-day promises on the storefront."
    )
elif late_rate > 0:
    actions.append(
        f"- **Some orders ({late_rate*100:.1f}%) are shipping late.** "
        "Pay attention to SKUs stored in coolers or backroom shelves that slow down picking "
        "and reorganize to keep best-sellers closest."
    )
else:
    actions.append(
        "- **All orders in this view shipped on time.** "
        "Use this slice as a benchmark when adding new soda SKUs or changing fulfillment partners."
    )

# High-value customers
high_value_threshold = (
    customer_summary["net_spend"].quantile(0.9) if len(customer_summary) > 0 else 0
)
high_value_count = (customer_summary["net_spend"].str.replace("[$,]", "", regex=True).astype(float)
                    if isinstance(customer_summary["net_spend"].iloc[0], str)
                    else (customer_summary["net_spend"] > high_value_threshold).sum())

if isinstance(high_value_count, int) and high_value_count > 0:
    actions.append(
        f"- **Top-spend soda fans** exceed the 90th percentile net spend. "
        "Consider a VIP tier: free case upgrades, early access to new flavors, or mix-and-match bundles."
    )

# New vs returning
if new_share < 30:
    actions.append(
        f"- Only **{new_share:.1f}% of orders are from new soda customers.** "
        "Invest in awareness (front-of-store displays, social promos, food-bundle deals) to bring in more first-time buyers."
    )
elif new_share > 60:
    actions.append(
        f"- **{new_share:.1f}% of orders are from new customers.** "
        "Acquisition is strong—now push loyalty: refill reminders, multi-case discounts, and subscribe-and-save on favorite flavors."
    )
else:
    actions.append(
        f"- **Balanced mix of new ({new_share:.1f}%) and returning customers.** "
        "A good base to test different promotions for classic vs. limited-time soda flavors."
    )

# Units sold – inventory pressure
if total_units_sold > 0:
    actions.append(
        f"- You sold **{int(total_units_sold):,} total cans/bottles** in this period. "
        "Cross-check this with your inventory overview to ensure high-velocity SKUs (Cola & Citrus especially) "
        "are reordered before hitting low-stock thresholds."
    )

for a in actions:
    st.markdown(a)

