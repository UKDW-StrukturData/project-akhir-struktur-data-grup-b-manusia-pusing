import streamlit as st
import os

st.set_page_config(page_title="NeuvaMoneda", layout="wide")

#mengeksekusi file css dengan batuuan CHAT GPT
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

# Fungsi GUARD dibantu untuk CHAT GPT
def login_guard():
    if not st.session_state.logged_in:
        st.warning("Silakan login terlebih dahulu.")
        st.session_state.page = "login"
        st.rerun()

def pindahhalaman(page):
    st.session_state.page = page
    st.rerun()

def LoginPages():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="logo-box">LOGO</div>', unsafe_allow_html=True)
    st.markdown('<div class="title">Selamat Datang Kembali!</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Masuk"):
        if username in st.session_state.CREDENTIALS and st.session_state.CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.switch_page("pages/Home.py")
        else:
            st.error("Username atau password salah.")

    if st.button("Belum punya akun? Daftar"):
        pindahhalaman("signup")

    st.markdown("</div>", unsafe_allow_html=True)

def SignUpPages():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="logo-box">LOGO</div>', unsafe_allow_html=True)
    st.markdown('<div class="title">Buat Akun Baru</div>', unsafe_allow_html=True)

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    confirm = st.text_input("Konfirmasi Password", type="password")

    if st.button("Daftar"):
        if new_user == "" or new_pass == "":
            st.error("Semua kolom wajib diisi.")
        elif new_user in st.session_state.CREDENTIALS:
            st.error("Username sudah digunakan.")
        elif new_pass != confirm:
            st.error("Password tidak cocok.")
        else:
            st.session_state.CREDENTIALS[new_user] = new_pass
            st.success("Akun berhasil dibuat! Silakan login.")
            pindahhalaman("login")

    if st.button("Kembali ke Login"):
        pindahhalaman("login")

    st.markdown("</div>", unsafe_allow_html=True)

def page_dashboard():
    login_guard()

    st.sidebar.title("NeuvaMoneda — Admin Panel")
    st.sidebar.write("Pilih menu aplikasi.")

    st.title(f"Halo, {st.session_state.username} 👋")
    st.success("Selamat datang di Dashboard NeuvaMoneda!")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

if not st.session_state.logged_in and st.session_state.page not in ["login", "signup"]:
    st.session_state.page = "signup"

if st.session_state.page == "login":
    LoginPages()
elif st.session_state.page == "signup":
    SignUpPages()
else:
    page_dashboard()
