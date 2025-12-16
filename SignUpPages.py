import streamlit as st
import time
from database import add_user, user_exists

def signup_page():
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

    st.markdown('<div class="title">Silahkan Membuat Akun Baru</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm  = st.text_input("Konfirmasi Password", type="password")

    if st.button("Daftar"):
        if not username or not password or not confirm:
            st.warning("⚠️ Semua kolom wajib diisi.")
            return

        if password != confirm:
            st.warning("⚠️ Password dan konfirmasi tidak sama.")
            return

        if user_exists(username):
            st.warning("⚠️ Username sudah digunakan.")
            return

        if add_user(username, password):
            st.success("✅ Akun berhasil dibuat!")
            time.sleep(1.5)
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("❌ Gagal membuat akun.")

    if st.button("Kembali ke Login"):
        st.session_state.page = "login"
        st.rerun()
