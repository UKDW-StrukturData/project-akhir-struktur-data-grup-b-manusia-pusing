import streamlit as st
from database import validate_user

def login_page():
    st.markdown("""
    <style>
    .stApp {
        /* Gradasi Ungu Gelap ke Hitam Pekat */
        background: radial-gradient(ellipse at center, #240b36 0%, #000000 100%);
        color: #e0f7fa;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    /* Container Card Glassmorphism untuk Form Login/Signup */
    .login-container {
        background: rgba(46, 17, 71, 0.4); /* Ungu tua transparan */
        border-radius: 20px;
        padding: 40px;
        margin-top: 50px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(135, 90, 255, 0.3); /* Border neon ungu */
    }

    .title {
        text-align: center;
        color: #875aff; /* Warna Neon Ungu Terang */
        font-size: 2.5em;
        margin-top: 20px;
        margin-bottom: 40px;
        text-shadow: 0 0 10px #875aff, 0 0 20px #875aff;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .stTextInput>div>div>input {
        background-color: rgba(0, 0, 0, 0.6); /* Hitam transparan */
        border: 1px solid #875aff;
        color: #e0f7fa;
        border-radius: 10px;
        padding: 12px;
        box-shadow: 0 0 5px #875aff;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #875aff, #b196ff); /* Gradasi Ungu */
        color: #000000;
        font-weight: bold;
        border-radius: 10px;
        margin-top: 15px;
        transition: all 0.3s;
        border: none;
        box-shadow: 0 0 10px #875aff;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #b196ff, #875aff);
        box-shadow: 0 0 15px #b196ff, 0 0 30px #b196ff;
        transform: translateY(-2px);
    }

    @keyframes glowPulse {
        0% { box-shadow: 0 0 5px #b196ff; }
        50% { box-shadow: 0 0 25px #b196ff; }
        100% { box-shadow: 0 0 5px #b196ff; }
    }

    @keyframes slideFade {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .futuristic-success {
        background: linear-gradient(135deg, #b196ff, #5e35b1);
        color: #000000;
        padding: 18px;
        border-radius: 16px;
        font-weight: bold;
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 25px;
        animation: slideFade 0.8s ease-out, glowPulse 2s infinite;
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
