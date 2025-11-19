import streamlit as st

def require_login():
    if "logged_in" not in st.session_state or st.session_state.logged_in is False:
        st.warning("Anda harus login untuk mengakses halaman ini.")
        st.switch_page("LoginPages.py")
require_login()
username = st.session_state.get("username", "User")

st.title(f"Selamat datang {username} di Halaman Home!")
st.write("proses pengembangan")
