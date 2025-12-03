import streamlit as st

st.set_page_config(
    page_title="GURU · AI Business Advisor",
    page_icon="🧠",
    layout="wide",
)


# ---------- SIDEBAR / NAV STYLES ----------
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: #050608;
    color: #E5E7EB;
    border-right: 1px solid #111827;
}

section[data-testid="stSidebar"] nav a {
    border-radius: 10px;
    padding: 0.38rem 0.55rem;
    font-size: 0.9rem;
    color: #E5E7EB;
}
section[data-testid="stSidebar"] nav a:hover {
    background: rgba(148,163,184,0.15);
}
section[data-testid="stSidebar"] nav a[aria-current="page"] {
    background: rgba(22,163,74,0.18);
    border: 1px solid rgba(34,197,94,0.65);
    color: #BBF7D0;
}
#MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    /* Sidebar base look */
    section[data-testid="stSidebar"] {
        background: #050608;
        color: #E5E7EB;
        border-right: 1px solid #111827;
    }

    /* Header area where st.logo lives */
    [data-testid="stSidebarHeader"] {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 14px 8px 14px;
        border-bottom: 1px solid #111827;
    }

    /* Logo image inside header – make sure it doesn’t look huge */
    [data-testid="stSidebarHeader"] img {
        width: 32px;
        height: 32px;
        object-fit: contain;
    }

    /* Text container next to logo */
    [data-testid="stSidebarHeader"]::after {
        content: "GURU\\A";
        white-space: pre;
        font-weight: 700;
        font-size: 0.86rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-left: 4px;
        color: #E5E7EB;
    }

    /* Navigation links */
    section[data-testid="stSidebar"] nav a {
        border-radius: 10px;
        padding: 0.38rem 0.55rem;
        font-size: 0.9rem;
        color: #E5E7EB;
    }
    section[data-testid="stSidebar"] nav a:hover {
        background: rgba(148,163,184,0.15);
    }
    section[data-testid="stSidebar"] nav a[aria-current="page"] {
        background: rgba(22,163,74,0.18);
        border: 1px solid rgba(34,197,94,0.65);
        color: #BBF7D0;
    }

    #MainMenu, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)
# ---------- LOGO + BRAND TEXT ----------
with st.sidebar:
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("assets/guru_logo.png", use_container_width=True)

    with col2:
        st.markdown(
            """
            <div style="padding-top: 4px;">
                <div style="
                    font-weight: 700;
                    font-size: 1.05rem;
                    letter-spacing: 0.03em;
                ">
                    GURU
                </div>
                <div style="
                    font-size: 0.74rem;
                    color: #9CA3AF;
                    letter-spacing: 0.13em;
                    margin-top: -2px;
                    text-transform: uppercase;
                ">
                    AI Business Advisor
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border-color: #111827;'>", unsafe_allow_html=True)

# ---------- NAVIGATION ----------
pages = {
    "Navigation Bar": [
        st.Page("Dashboard.py", title="Dashboard Home"),
        st.Page("Sales_Analytics.py", title="Sales and Analytics"),
        st.Page("Trends_and_Analysis.py", title="Trends and Analysis"),
        st.Page("Inventory_Overview.py", title="Inventory Overview"),
        st.Page("Transactions.py", title="Transactions and Inventory"),
        st.Page("Reports.py", title="Reports"),
        st.Page("Agent.py", title="AI Insights"),
        st.Page("AIAgent.py", title="GURU"),
        
    ],
}

pg = st.navigation(pages)
pg.run()
