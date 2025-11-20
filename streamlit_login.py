import streamlit as st

#st.title("Authentication")
#if st.button("Authenticate"):
 #   st.login("google")



st.title("Welcome to the App login page")
if not st.user.is_logged_in:
    if st.button("Log in with Google", type="primary", icon=":material/login:"):
        st.login()
        st.switch_page("pages/Dashboard.py")
else:
    st.html(f"Hello, <span style='color: orange; font-weight: bold;'>{st.user.name}</span>!")
    if st.button("Log out", type="secondary", icon=":material/logout:"):
        st.logout()