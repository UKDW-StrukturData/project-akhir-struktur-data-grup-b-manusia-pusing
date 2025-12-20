import sys
import os
import streamlit as st

# Penggunaan database dibantu GPT
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from database import delete_user, update_username


st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(ellipse at center, #240b36 0%, #000000 100%);
            color: #e0f7fa;
            font-family: 'Segoe UI', Roboto, sans-serif;
        }
        h1, h2, h3, h4 {
            color: #875aff; /* Neon Ungu */
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(135, 90, 255, 0.6);
        }
        
        /* Glassmorphism Card Settings */
        .card {
            background: rgba(46, 17, 71, 0.65); /* Ungu tua transparan */
            padding: 40px;
            border-radius: 30px;
            color: white;
            width: 95%;
            margin: 30px auto;
            box-shadow: 0 15px 40px 0 rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(25px); /* Sedikit lebih buram */
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(135, 90, 255, 0.35); /* Border neon ungu */
        }
        
        .round-img {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid #875aff;
            box-shadow: 0 0 25px rgba(135, 90, 255, 0.7);
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #875aff, #b196ff);
            color: #000000;
            font-weight: bold;
            border-radius: 12px;
            margin-top: 10px;
            transition: all 0.3s;
            border: none;
            box-shadow: 0 0 10px rgba(135, 90, 255, 0.4);
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #b196ff, #875aff);
            box-shadow: 0 0 20px rgba(177, 150, 255, 0.8);
            transform: scale(1.02);
        }
        
        /* Primary Danger Button (LOGOUT & Hapus) */
        .stButton button[kind="primary"] {
            background: linear-gradient(90deg, #ff4b4b, #c62828) !important;
            box-shadow: 0 0 10px rgba(255, 75, 75, 0.4) !important;
        }
        
        /* Inputs inside card */
        .stTextInput>div>div>input, .stSelectbox>div>div>div>div>div {
            background-color: rgba(0, 0, 0, 0.5) !important;
            border: 1px solid #875aff;
            color: #e0f7fa;
            border-radius: 10px;
            padding: 12px;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.3), 0 0 5px rgba(135, 90, 255, 0.2);
        }

        /* Sidebar styling */
        .stSidebar > div:first-child {
            background: rgba(46, 17, 71, 0.5); /* Sidebar Glassmorphism */
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(135, 90, 255, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# GUARD LOGIN DIBANTU GPT DAN ASDOS
def require_login_page():
    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("App.py")

require_login_page()

if "username" not in st.session_state:
    st.session_state.username = "ADMIN"
if "show_change_username" not in st.session_state:
    st.session_state.show_change_username = False

st.markdown(
    "<h1 style='text-align:center;'>PENGATURAN AKUN</h1>",
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        "<img class='round-img' src='https://img.icons8.com/lollipop/1200/test-account.jpg'>",
        unsafe_allow_html=True
    )

with col2:
    st.subheader("Username Aktif")
    st.markdown(
        f"<h2 style='color:white;'>{st.session_state.username}</h2>",
        unsafe_allow_html=True
    )

st.divider()

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
            old_username = st.session_state.username

            if new_username.strip() == "":
                st.warning("Username tidak boleh kosong.")
            else:
                success = update_username(old_username, new_username)

                if success:
                    st.session_state.username = new_username
                    st.session_state.show_change_username = False
                    st.success("Username berhasil diperbarui di database!")
                else:
                    st.error("Username sudah digunakan. Silakan pilih yang lain.")

    with col_cancel:
        if st.button("Batal", use_container_width=True):
            st.session_state.show_change_username = False

st.divider()
st.subheader("Manajemen Akun")

if st.button("LOGOUT", type="primary"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("App.py")

if st.button("⚠️ Hapus Akun Permanen", type="primary"):
    delete_user(st.session_state.username)

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.error("Akun berhasil dihapus permanen.")
    st.switch_page("LoginPages.py")
