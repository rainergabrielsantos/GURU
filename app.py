import streamlit as st
from utils import apply_custom_theme

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="GURU · AI Business Guru",
    page_icon="🧠",
    layout="wide",
)

apply_custom_theme()

# ---------- LOGO IN SIDEBAR HEADER ----------
# This puts the logo in the special sidebar header area (always ABOVE nav)
st.logo("assets/guru_logo.png")

# ---------- SIDEBAR / NAV STYLES ----------
st.markdown(
    """
    <style>
    /* Sidebar base */
    section[data-testid="stSidebar"] {
        background: #050608;
        color: #E5E7EB;
        border-right: 1px solid #111827;
    }

    /* Header where st.logo is rendered */
    [data-testid="stSidebarHeader"] {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px 8px 14px;
        border-bottom: 1px solid #111827;
    }

    /* Make the logo look like a rounded green badge */
    [data-testid="stSidebarHeader"] img {
        width: 34px;
        height: 34px;
        border-radius: 12px;
        background: #16a34a;
        padding: 6px;
        box-shadow: 0 8px 20px rgba(22,163,74,0.7);
        object-fit: contain;
    }

    /* GURU text next to logo */
    [data-testid="stSidebarHeader"]::after {
        content: "GURU\\A AI BUSINESS GURU";
        white-space: pre;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #F9FAFB;
    }

    /* Hide the default section label "Navigation Bar" */
    section[data-testid="stSidebar"] h2 {
        display: none;
    }

    /* NAV LIST: soften spacing */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        padding: 6px 8px 12px 8px;
    }

    /* Base style for each nav item (button or link) */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] [role="listitem"] > * {
        border-radius: 16px;
        padding: 0.46rem 0.9rem;
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
        transition: background 120ms ease, box-shadow 120ms ease, color 120ms ease;
    }

    /* Hover state */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] [role="listitem"] > *:hover {
        background: rgba(75,85,99,0.4);
        text-decoration: none;
    }

    /* ACTIVE PAGE: bright green pill */
    section[data-testid="stSidebar"] [aria-current="page"] {
        background: #16a34a !important;
        color: #020617 !important;
        font-weight: 600;
        box-shadow: 0 14px 30px rgba(22,163,74,0.7);
    }

    /* Ensure any icon inside the active item also turns dark */
    section[data-testid="stSidebar"] [aria-current="page"] span, 
    section[data-testid="stSidebar"] [aria-current="page"] svg {
        color: #020617 !important;
        fill: #020617 !important;
    }

    #MainMenu, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- DEFINE PAGES ----------
pages = {
    "Navigation Bar": [
        st.Page("Dashboard.py",            title="Dashboard",          icon=":material/dashboard:"),
        st.Page("Sales_Analytics.py",      title="Sales Analytics",    icon=":material/trending_up:"),
        st.Page("Trends_and_Analysis.py",  title="Trends & Analysis",  icon=":material/stacked_line_chart:"),
        st.Page("Inventory_Overview.py",   title="Inventory Overview", icon=":material/inventory_2:"),
        st.Page("Transactions.py",         title="Transactions",       icon=":material/payments:"),
        st.Page("Agent.py",                title="AI Insights",        icon=":material/psychology:"),
        st.Page("AIAgent.py",              title="Chat with GURU",     icon=":material/chat:"),
        st.Page("Reports.py",              title="Reports",            icon=":material/description:"),
    ],
}

# ---------- NAVIGATION ROUTER ----------
pg = st.navigation(pages)   # still uses sidebar position by default
pg.run()
