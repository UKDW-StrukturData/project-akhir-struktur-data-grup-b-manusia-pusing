import streamlit as st
from database import init_db
from LoginPages import login_page
from SignUpPages import signup_page
from ForgotPassword import forgot_password_page

st.set_page_config(page_title="NuevaMoneda", layout="wide")
init_db()

st.markdown("""
    <style>
        .stApp {
            /* Gradasi Ungu Gelap ke Hitam Pekat */
            background: radial-gradient(ellipse at center, #240b36 0%, #000000 100%);
            color: #e0f7fa;
            font-family: 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Sidebar container utama (latar belakang) */
        [data-testid="stSidebar"] {
            background-color: rgba(13, 5, 20, 0.95) !important; /* Ungu sangat gelap, hampir hitam */
        }
        
        /* Item navigasi yang TIDAK DIPILIH */
        [data-testid="stSidebarNav"] li a {
            color: #b196ff !important; /* Teks neon ungu */
            border-radius: 10px;
            padding: 10px 15px;
            transition: all 0.2s;
        }
        [data-testid="stSidebarNav"] li a:hover {
            background-color: rgba(94, 53, 177, 0.3) !important; /* Hover effect */
            color: #ffffff !important;
        }
        
        /* Item navigasi yang SEDANG DIPILIH (Active/Selected Page) */
        /* Selector kuat untuk memastikan perubahan */
        [data-testid="stSidebarNav"] li .st-emotion-cache-1ft9w09, 
        [data-testid="stSidebarNav"] li .st-emotion-cache-1ft9w09 div { 
            background-color: #5e35b1 !important; /* Ungu Solid untuk highlight */
            color: #ffffff !important;
            border-radius: 10px;
        }

        h1, h2, h3, h4, h5, h6, .title {
            color: #b196ff !important; /* Neon Ungu Muda */
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(177, 150, 255, 0.7);
        }
    </style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "login"

def require_login_app():
    if not st.session_state.logged_in:
        if st.session_state.page not in ["login", "signup", "forgot"]:
            st.session_state.page = "login"
            st.warning("Silakan login terlebih dahulu.")
            st.rerun()

require_login_app()

if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "signup":
    signup_page()

elif st.session_state.page == "forgot":
    forgot_password_page()
