import streamlit as st
import time

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
            .stTextInput>div>div>input {
                background-color: rgba(0, 0, 0, 0.5);
                border: 1px solid #00bcd4;
                color: #00e5ff;
                border-radius: 12px;
                padding: 12px;
            }
            .stButton>button {
                width: 100%;
                background: linear-gradient(90deg, #00bcd4, #008ba3);
                color: #0f1c2c;
                font-weight: bold;
                border-radius: 14px;
                margin-top: 15px;
                padding: 12px;
                border: none;
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
        elif username in st.session_state.CREDENTIALS:
            st.warning("⚠️ Username sudah digunakan.")
        elif password != confirm:
            st.warning("⚠️ Password dan konfirmasi tidak sama.")
        else:
            st.session_state.CREDENTIALS[username] = password
            st.success("✅ Akun berhasil dibuat! Mengalihkan ke halaman login...")
            time.sleep(1.5)
            st.session_state.page = "login"

    if st.button("Kembali ke Login"):
        st.session_state.page = "login"
        st.rerun()

if "CREDENTIALS" not in st.session_state:
    st.session_state.CREDENTIALS = {
        "admin": "admin"
    }
