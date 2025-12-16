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
            background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%);
            color: #e0f7fa;
        }
        h1, h2, h3, h4 {
            color: #00bcd4;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(0, 188, 212, 0.6);
        }
        .round-img {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            border: 4px solid #00bcd4;
        }
    </style>
""", unsafe_allow_html=True)

# GUARD LOGIN DIBANTU GPT DAN ASDOS
def require_login_page():
    if not st.session_state.get("logged_in"):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("LoginPages.py")

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
        "<img class='round-img' src='https://i.ibb.co/680385F/avatar-futuristic.png'>",
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

if st.button("LOGOUT", type="primary"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("LoginPages.py")

st.subheader("Manajemen Akun Permanen")

if st.button("⚠️ Hapus Akun Permanen", type="primary"):
    delete_user(st.session_state.username)

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.error("Akun berhasil dihapus permanen.")
    st.switch_page("LoginPages.py")
