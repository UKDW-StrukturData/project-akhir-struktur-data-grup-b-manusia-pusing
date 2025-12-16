import streamlit as st
from database import validate_user

def login_page():
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #0f1c2c, #0d0d0d);
                color: #e0f7fa;
            }
            .title {
                text-align: center;
                color: #00bcd4;
                font-size: 2.5em;
                margin-top: 20px;
                margin-bottom: 40px;
                text-shadow: 0 0 10px #00bcd4, 0 0 20px #00bcd4;
            }
        </style>
    """, unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with b:
        st.image("LogoNuevaMoneda.png", width=750)

    st.markdown('<div class="title">Selamat Datang di NuevaMoneda</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Masuk"):
        if validate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.switch_page("pages/Home.py")
        else:
            st.error("❌ Username atau password salah")

    if st.button("Belum punya akun? Daftar"):
        st.session_state.page = "signup"
        st.rerun()
