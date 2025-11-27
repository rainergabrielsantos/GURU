import streamlit as st
import pandas as pd




if not st.user.is_logged_in:
    st.title("Welcome to the Dashboard")
else:
    st.html(f"Hello, <span style='color: orange; font-weight: bold;'>{st.user.name}</span>! Welcome to the Dashboard.")
    if st.button("Log out", type="secondary", icon=":material/logout:"):
        st.logout()

#st.title("Welcome to the Dashboard")


#if st.button("Log out", type="secondary", icon=":material/logout:"):
 #       st.logout()
        