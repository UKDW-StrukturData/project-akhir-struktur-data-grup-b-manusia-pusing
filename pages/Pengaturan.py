import sys
import os
import streamlit as st

# ===== FIX IMPORT DATABASE (WAJIB UNTUK FILE DI /pages) =====
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from database import delete_user
# ===========================================================

st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%);
            color: #e0f7fa;
        }
        h1, h2, h3, h4 {
            color: #00bcd4;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(0, 188, 212, 0.6);
        }
        
        /* Glassmorphism Card Settings */
        .card {
            background: rgba(15, 28, 44, 0.65);
            padding: 40px;
            border-radius: 30px;
            color: white;
            width: 95%;
            margin: 30px auto;
            box-shadow: 0 15px 40px 0 rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 1px solid rgba(0, 188, 212, 0.25);
        }
        
        .round-img {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid #00bcd4;
            box-shadow: 0 0 25px rgba(0, 188, 212, 0.5);
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #00bcd4, #008ba3);
            color: #0f1c2c;
            font-weight: bold;
            border-radius: 12px;
            margin-top: 10px;
            transition: all 0.3s;
            border: none;
            box-shadow: 0 0 10px rgba(0, 188, 212, 0.3);
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #00e5ff, #00bcd4);
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.6);
            transform: scale(1.02);
        }
        
        /* Primary Danger Button */
        .stButton button[kind="primary"] {
            background: linear-gradient(90deg, #ff4b4b, #c62828) !important;
            box-shadow: 0 0 10px rgba(255, 75, 75, 0.4);
        }
        
        /* Inputs inside card */
        .stTextInput>div>div>input, .stSelectbox>div>div>div>div>div {
            background-color: rgba(0, 0, 0, 0.4) !important;
            border: 1px solid #00bcd4;
            color: #e0f7fa;
            border-radius: 10px;
            padding: 12px;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)


# Fungsi GUARD
def require_login_page():
    if not st.session_state.get("logged_in"):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("LoginPages.py")
require_login_page()

if "username" not in st.session_state:
    st.session_state.username = "ADMIN"
if "user_id" not in st.session_state:
    st.session_state.user_id = "12345678"
if "show_change_username" not in st.session_state:
    st.session_state.show_change_username = False
if "bahasa" not in st.session_state:
    st.session_state.bahasa = "Indonesia"

st.markdown("""
    <h1 style='text-align:center; color:#00bcd4; margin-bottom: 0px;'>PENGATURAN AKUN</h1>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        "<img class='round-img' src='https://i.ibb.co/680385F/avatar-futuristic.png'>", 
        unsafe_allow_html=True
    )

with col2:
    st.subheader("Username Aktif")
    st.markdown(
        f"<h2 style='color:white;'>{st.session_state.username}</h2>",
        unsafe_allow_html=True
    )

st.write("---")

# FITUR GANTI USERNAME
st.subheader("Ganti Username")

if not st.session_state.show_change_username:
    if st.button("Ganti Username"):
        st.session_state.show_change_username = True
else:
    new_username = st.text_input(
        "Masukkan Username Baru",
        value=st.session_state.username
    )
    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("Simpan Username", use_container_width=True):
            st.session_state.username = new_username
            st.session_state.show_change_username = False
            st.success("Username berhasil diperbarui!")
    with col_cancel:
        if st.button("Batal", use_container_width=True):
            st.session_state.show_change_username = False

st.write("---")

# LOGOUT
if st.button("LOGOUT", type="primary"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "login"

    st.success("Berhasil logout")
    st.switch_page("LoginPages.py")

# HAPUS AKUN
st.subheader("Manajemen Akun Permanen")

if st.button("⚠️ Hapus Akun Permanen", type="primary"):
    delete_user(st.session_state.username)

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "login"

    st.error("Akun berhasil dihapus permanen.")
    st.switch_page("LoginPages.py")

st.markdown("</div>", unsafe_allow_html=True)
