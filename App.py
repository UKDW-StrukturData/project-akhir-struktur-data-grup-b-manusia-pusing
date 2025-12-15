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
    st.session_state.page = "home"

left, center, right = st.columns([1, 2, 1])

with center:
    st.image("LogoNuevaMoneda.png", width=400)

    st.markdown("""
    <p style="text-align:center; font-size:20px; font-style:italic;">
        “Money is a tool. Used properly it makes something beautiful,
        used wrong it makes a mess.”
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
