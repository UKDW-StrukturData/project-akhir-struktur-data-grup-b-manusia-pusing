import streamlit as st

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
            .stTextInput>div>div>input {
                background-color: rgba(30, 40, 50, 0.7);
                border: 1px solid #00bcd4;
                color: #e0f7fa;
                border-radius: 8px;
                padding: 10px;
            }
            .stButton>button {
                width: 100%;
                background: #00bcd4;
                color: #0f1c2c;
                font-weight: bold;
                border-radius: 10px;
                margin-top: 10px;
                transition: all 0.3s;
                border: none;
                box-shadow: 0 0 5px #00bcd4, 0 0 15px #00bcd4;
            }
            .stButton>button:hover {
                background: #00e5ff;
                box-shadow: 0 0 10px #00e5ff, 0 0 25px #00e5ff;
            }
        </style>
    """, unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with b:
        st.image("LogoNuevaMoneda.png", width=750)

    st.markdown('<div class="title">Selamat Datang di NuevaMoneda</div>', unsafe_allow_html=True)

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Masuk", key="login_btn"):
        if (
            username in st.session_state.CREDENTIALS
            and st.session_state.CREDENTIALS[username] == password
        ):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.switch_page("pages/Home.py")
        else:
            st.error("Username atau password salah.")

    if st.button("Belum punya akun? Daftar", key="signup_btn"):
        st.session_state.page = "signup"
        st.rerun()

# Inisialisasi state (AMAN)
if "CREDENTIALS" not in st.session_state:
    st.session_state.CREDENTIALS = {"admin": "admin"}
