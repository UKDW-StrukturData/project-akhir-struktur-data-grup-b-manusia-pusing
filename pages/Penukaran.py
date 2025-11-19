import streamlit as st

def require_login():
    if "logged_in" not in st.session_state or st.session_state.logged_in is False:
        st.warning("Anda harus login untuk mengakses halaman ini.")
        st.switch_page("LoginPages.py")
require_login()

st.title("Penukaran Uang")
st.write("proses pengembangan")

