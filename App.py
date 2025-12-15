import streamlit as st
import os

st.set_page_config(
    page_title="NeuvaMoneda",
    layout="wide"
)

def load_css():
    css_file = "styles.css"
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

left, center, right = st.columns([1, 2, 1])

with center:
    st.image("LogoNuevaMoneda.png", width=400)
    st.markdown("""
    <p style="
        text-align:center;
        font-size:20px;
        font-style:italic;
        color: #dddddd;
        margin-top: 15px;
    ">
        “Money is a tool. Used properly it makes something beautiful,  
        used wrong it makes a mess.”
    </p>
    """, unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login", use_container_width=True):
            st.switch_page("LoginPages.py")

    with col2:
        if st.button("Sign Up", use_container_width=True):
            st.switch_page("SignUpPages.py")

