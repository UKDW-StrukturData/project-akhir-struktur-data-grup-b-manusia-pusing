import streamlit as st
import os
from LoginPages import login_page
from SignUpPages import signup_page

st.set_page_config(page_title="NeuvaMoneda", layout="wide")

def load_css():
    css_file = "styles.css"
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

if "page" not in st.session_state:
    st.session_state.page = "signup"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "CREDENTIALS" not in st.session_state:
    st.session_state.CREDENTIALS = {}

def login_guard():
    if not st.session_state.logged_in:
        st.warning("Silakan login terlebih dahulu.")
        st.session_state.page = "login"
        st.rerun()

def page_dashboard():
    login_guard()

    st.sidebar.title("NeuvaMoneda — Admin Panel")
    st.sidebar.write("Pilih menu aplikasi.")

    st.title(f"Halo, {st.session_state.username} !")
    st.success("Selamat datang di Dashboard NeuvaMoneda!")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

if not st.session_state.logged_in and st.session_state.page not in ["login", "signup"]:
    st.session_state.page = "signup"

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
else:
    page_dashboard()
