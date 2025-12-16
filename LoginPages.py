import streamlit as st
from database import validate_user

def login_page():
    st.markdown("""
        <style>
            .stApp {
                background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%);
                color: #e0f7fa;
            }
            .title {
                text-align: center;
                color: #00bcd4;
                font-size: 2.5em;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 40px;
                text-transform: uppercase;
                letter-spacing: 3px;
                text-shadow: 0 0 15px rgba(0, 188, 212, 0.8);
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
            st.switch_page("pages/Home.py")  # ⬅ HOME DI FOLDER pages
        else:
            st.error("❌ Username atau password salah")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Lupa Password?"):
            st.session_state.page = "forgot"
            st.rerun()

    with col2:
        if st.button("Belum punya akun? Daftar"):
            st.session_state.page = "signup"
            st.rerun()
