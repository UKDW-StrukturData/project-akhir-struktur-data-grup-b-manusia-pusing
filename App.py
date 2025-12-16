import streamlit as st
from database import init_db
from LoginPages import login_page
from SignUpPages import signup_page

st.set_page_config(page_title="NuevaMoneda", layout="wide")
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"

def require_login_app():
    if not st.session_state.logged_in:
        if st.session_state.page not in ["login", "signup"]:
            st.session_state.page = "login"
            st.warning("Silakan login terlebih dahulu.")
            st.rerun()

require_login_app()

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
else:
    st.title(f"Halo, {st.session_state.username}")
    st.success("Selamat datang di NuevaMoneda")
