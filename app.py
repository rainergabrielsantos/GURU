import streamlit as st

st.set_page_config(
    page_title="GURU • Sidebar Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",  # opens after login when nav renders
)

# ---------- LOGIN GATE ----------
# Works with your custom auth (st.user / st.login()).
# If you're not using that, swap this condition for your own.
is_logged_in = getattr(st.user, "is_logged_in", False)

if not is_logged_in:
    st.title("Welcome to the App login page")
    st.write("Please sign in to continue.")

    if st.button("Log in with Google", type="primary"):
        st.login()            # your environment's Google auth
        st.rerun()            # refresh to reflect logged-in state

    st.stop()  # <- CRUCIAL: prevents the sidebar/nav from rendering

# ---------- NAV ONLY AFTER LOGIN ----------
pages = {
    "Navigation Bar": [
        st.Page("app_pages/Dashboard.py",           title="Dashboard Home"),
        st.Page("app_pages/Sales_Analytics.py",     title="Sales and Analytics"),
        st.Page("app_pages/Trends_and_Analysis.py", title="Trends and Analysis"),
        st.Page("app_pages/Inventory_Overview.py",  title="Inventory Overview"),
        st.Page("app_pages/Transactions.py",        title="Transactions and Inventory"),
        st.Page("app_pages/Agent.py",               title="AI Insights"),
        st.Page("app_pages/Reports.py",             title="Reports"),
        st.Page("app_pages/AIAgent.py",             title="Another Agent"),
    ]
}

st.navigation(pages).run()
