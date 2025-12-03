# utils.py
import streamlit as st


def apply_custom_theme() -> None:
    """Apply global dark theme and layout for the entire app."""
    st.markdown(
        """
<style>
/* Global app background + text */
.stApp {
    background-color: #050608;
    color: #f5f5f5;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Main content padding (so top bar doesn't overlap) */
.block-container {
    padding-top: 3.5rem;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #050608;
    border-right: 1px solid #222;
}

/* Tables */
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

/* Buttons - optional subtle rounding */
.stButton > button {
    border-radius: 999px;
    font-weight: 500;
}

/* You can add more global styles here later (cards, headings, etc.) */
</style>
""",
        unsafe_allow_html=True,
    )
