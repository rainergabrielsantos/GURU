from fpdf import FPDF
from io import BytesIO
import datetime

import pandas as pd
from numpy.random import default_rng
import streamlit as st

from utils import apply_custom_theme


# ---------- PAGE SETUP ----------
st.set_page_config(layout="wide")
apply_custom_theme()

# Global styling to mimic Figma
st.markdown(
    """
<style>
/* Overall page padding tweak */
.main {
    padding-top: 1.5rem;
}

/* Tabs -> pill style */
.stTabs [role="tablist"] {
    gap: 0.5rem;
}

.stTabs [role="tab"] {
    padding: 0.4rem 1.2rem;
    border-radius: 999px;
    background-color: #222;
    color: #eee;
    border: 1px solid #444;
    font-weight: 500;
}

.stTabs [role="tab"][aria-selected="true"] {
    background-color: #fff;
    color: #000;
    border-color: #fff;
}

/* Quick report container */
.quick-card {
    background-color: #050505;
    border-radius: 18px;
    padding: 1.5rem 1.75rem;
    border: 1px solid #333;
}

/* Report cards */
.report-card {
    background-color: #151515;
    border-radius: 18px;
    padding: 1.5rem 1.75rem;
    border: 1px solid #333;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.report-icon {
    width: 44px;
    height: 44px;
    border-radius: 14px;
    background-color: #222;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}

.report-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.1rem;
}

.report-subtitle {
    color: #aaaaaa;
    font-size: 0.9rem;
}

.report-meta-label {
    color: #888;
    font-size: 0.85rem;
}

.report-meta-value {
    font-size: 0.9rem;
}

/* Make buttons a bit more like the mock */
.stButton > button {
    border-radius: 999px;
    font-weight: 500;
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------- HEADER ----------
st.title("Reports & Analytics")
st.caption("Generate comprehensive business reports and schedule automated analytics.")


# ---------- PDF GENERATION ----------
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(
        0,
        10,
        txt="This is a dynamically generated sample report!",
        ln=True,
        align="C",
    )
    pdf_bytes = pdf.output(dest="S")
    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode("latin-1")
    return BytesIO(pdf_bytes)


# ---------- TABS ----------
tab_generate, tab_recent, tab_scheduled = st.tabs(
    ["Generate Reports", "Recent Reports", "Scheduled Reports"]
)

# ===========================
# TAB 1: GENERATE REPORTS
# ===========================
with tab_generate:
    # ---- Quick Report Generation block ----
    st.markdown('<div class="quick-card">', unsafe_allow_html=True)

    st.subheader("Quick Report Generation")
    st.caption("Generate instant reports with customizable parameters")

    c1, c2, c3, c4 = st.columns([1.1, 1.1, 1.1, 1.2])

    with c1:
        date_range = st.selectbox(
            "Date Range",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Today", "Yesterday", "Custom"],
            index=1,
        )

    with c2:
        report_format = st.selectbox(
            "Format",
            ["PDF Document", "Excel Spreadsheet", "CSV File"],
            index=0,
        )

    with c3:
        custom_date = st.date_input(
            "Custom Date",
            datetime.date.today(),
        )

    with c4:
        generate_all = st.button("📊  Generate All Reports", width='stretch')

    if generate_all:
        pdf_data = create_pdf()
        st.success(
            f"Reports generated for **{date_range}** "
            f"in **{report_format}** format."
        )
        st.download_button(
            "⬇️ Download Sample Combined Report",
            data=pdf_data,
            file_name="Combined_Report.pdf",
            mime="application/pdf",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")  # spacing

    # ---- Individual Report Cards ----
    row1_col1, row1_col2 = st.columns(2)

    # Sales Summary Report
    with row1_col1:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)

        top_row = st.columns([0.18, 0.82])
        with top_row[0]:
            st.markdown('<div class="report-icon">📈</div>', unsafe_allow_html=True)
        with top_row[1]:
            st.markdown('<div class="report-title">Sales Summary Report</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="report-subtitle">'
                'Overview of sales performance, revenue trends, and key metrics'
                "</div>",
                unsafe_allow_html=True,
            )

        meta_left, meta_right = st.columns([0.5, 0.5])
        with meta_left:
            st.markdown('<span class="report-meta-label">Frequency:</span>', unsafe_allow_html=True)
            st.markdown('<div class="report-meta-value">Daily, Weekly, Monthly</div>', unsafe_allow_html=True)
        with meta_right:
            st.markdown('<span class="report-meta-label">Est. Time:</span>', unsafe_allow_html=True)
            st.markdown('<div class="report-meta-value">2 mins</div>', unsafe_allow_html=True)

        st.button("Generate Report", key="sales_report_btn", width='stretch')

        st.markdown("</div>", unsafe_allow_html=True)

    # Inventory Status Report
    with row1_col2:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)

        top_row = st.columns([0.18, 0.82])
        with top_row[0]:
            st.markdown('<div class="report-icon">📦</div>', unsafe_allow_html=True)
        with top_row[1]:
            st.markdown('<div class="report-title">Inventory Status Report</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="report-subtitle">'
                'Current stock levels, low stock alerts, and inventory valuation'
                "</div>",
                unsafe_allow_html=True,
            )

        meta_left, meta_right = st.columns([0.5, 0.5])
        with meta_left:
            st.markdown('<span class="report-meta-label">Frequency:</span>', unsafe_allow_html=True)
            st.markdown('<div class="report-meta-value">Daily, Weekly</div>', unsafe_allow_html=True)
        with meta_right:
            st.markdown('<span class="report-meta-label">Est. Time:</span>', unsafe_allow_html=True)
            st.markdown('<div class="report-meta-value">1 min</div>', unsafe_allow_html=True)

        st.button("Generate Report", key="inventory_report_btn", width='stretch')

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")  # spacing between rows

    row2_col1, row2_col2 = st.columns(2)

    # Financial Summary Report
    with row2_col1:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)

        top_row = st.columns([0.18, 0.82])
        with top_row[0]:
            st.markdown('<div class="report-icon">💰</div>', unsafe_allow_html=True)
        with top_row[1]:
            st.markdown('<div class="report-title">Financial Summary Report</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="report-subtitle">'
                'Revenue, expenses, profit margins, and financial KPIs'
                "</div>",
                unsafe_allow_html=True,
            )

        meta_left, meta_right = st.columns([0.5, 0.5])
        with meta_left:
            st.markdown('<span class="report-meta-label">Frequency:</span>', unsafe_allow_html=True)
            st.markdown('<div class="report-meta-value">Weekly, Monthly, Quarterly</div>', unsafe_allow_html=True)
        with meta_right:
            st.markdown('<span class="report-meta-label">Est. Time:</span>', unsafe_allow_html=True)
            st.markdown('<div class="report-meta-value">3 mins</div>', unsafe_allow_html=True)

        st.button("Generate Report", key="financial_report_btn", width='stretch')

        st.markdown("</div>", unsafe_allow_html=True)

    # Customer Analytics Report
    with row2_col2:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)

        top_row = st.columns([0.18, 0.82])
        with top_row[0]:
            st.markdown('<div class="report-icon">👥</div>', unsafe_allow_html=True)
        with top_row[1]:
            st.markdown('<div class="report-title">Customer Analytics Report</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="report-subtitle">'
                'Customer behavior, purchase patterns, and loyalty metrics'
                "</div>",
                unsafe_allow_html=True,
            )

        meta_left, meta_right = st.columns([0.5, 0.5])
        with meta_left:
            st.markdown('<span class="report-meta-label">Frequency:</span>', unsafe_allow_html=True)
            st.markdown('<div class="report-meta-value">Weekly, Monthly</div>', unsafe_allow_html=True)
        with meta_right:
            st.markdown('<span class="report-meta-label">Est. Time:</span>', unsafe_allow_html=True)
            st.markdown('<div class="report-meta-value">2 mins</div>', unsafe_allow_html=True)

        st.button("Generate Report", key="customer_report_btn", width='stretch')

        st.markdown("</div>", unsafe_allow_html=True)


# ===========================
# TAB 2: RECENT REPORTS
# ===========================
with tab_recent:
    st.subheader("Recent Reports")
    st.caption("View your most recently generated reports and quick performance trends.")

    # simple dummy trend chart
    rng = default_rng(0)
    df_recent = pd.DataFrame(
        rng.standard_normal((20, 3)),
        columns=["Sales", "Inventory", "Customers"],
    )
    st.line_chart(df_recent)

    recent_df = pd.DataFrame(
        [
            ["Sales Summary Report", "PDF", "Last 7 Days", "2025-11-25 14:10"],
            ["Inventory Status Report", "PDF", "Today", "2025-11-25 13:02"],
            ["Financial Summary Report", "Excel", "Last 30 Days", "2025-11-24 17:21"],
        ],
        columns=["Report", "Format", "Date Range", "Generated At"],
    )
    st.table(recent_df)


# ===========================
# TAB 3: SCHEDULED REPORTS
# ===========================
with tab_scheduled:
    st.subheader("Scheduled Reports")
    st.caption("Manage automated report schedules and delivery preferences.")

    scheduled_df = pd.DataFrame(
        [
            ["Sales Summary Report", "Daily at 08:00", "Email"],
            ["Inventory Status Report", "Daily at 07:30", "Slack"],
            ["Financial Summary Report", "Monthly on 1st", "Email"],
        ],
        columns=["Report", "Schedule", "Delivery Channel"],
    )
    st.table(scheduled_df)
