import streamlit as st

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
                text-shadow: 0 0 15px rgba(0, 188, 212, 0.8), 0 0 30px rgba(0, 188, 212, 0.4);
            }
            .stTextInput>div>div>input {
                background-color: rgba(0, 0, 0, 0.5) !important;
                border: 1px solid #00bcd4 !important;
                color: #00e5ff !important;
                border-radius: 12px;
                padding: 12px;
                box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
            }
            .stTextInput>div>div>input:focus {
                box-shadow: 0 0 15px rgba(0, 188, 212, 0.6), inset 0 0 10px rgba(0,0,0,0.5);
            }
            .stButton>button {
                width: 100%;
                background: linear-gradient(90deg, #00bcd4, #008ba3);
                color: #0f1c2c;
                font-weight: bold;
                border-radius: 14px;
                margin-top: 15px;
                padding: 12px ;
                transition: all 0.3s ease-in-out;
                border: none;
                box-shadow: 0 0 10px rgba(0, 188, 212, 0.5);
            }
            .stButton>button:hover {
                background: linear-gradient(90deg, #00e5ff, #00bcd4);
                box-shadow: 0 0 20px rgba(0, 229, 255, 0.8);
                transform: scale(1.02);
            }
            .signup-card {
                background: rgba(15, 28, 44, 0.6);
                border-radius: 25px;
                padding: 50px;
                backdrop-filter: blur(25px);
                -webkit-backdrop-filter: blur(25px);
                border: 1px solid rgba(0, 188, 212, 0.2);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
                margin: auto;
                max-width: 450px;
            }
        </style>
    """, unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with b:
        st.image("LogoNuevaMoneda.png", width=750)

    st.markdown('<div class="title">Silahkan Membuat Akun Baru</div>', unsafe_allow_html=True)

    with st.container():
        new_user = st.text_input("Username", key="signup_username")
        new_pass = st.text_input("Password", type="password", key="signup_password")
        confirm = st.text_input("Konfirmasi Password", type="password", key="signup_confirm")

        if st.button("Daftar", key="signup_action"):
            if new_user == "" or new_pass == "":
                st.error("Semua kolom wajib diisi.")
            elif new_user in st.session_state.CREDENTIALS:
                st.error("Username sudah digunakan.")
            elif new_pass != confirm:
                st.error("Password tidak cocok.")
            else:
                st.session_state.CREDENTIALS[new_user] = new_pass
                st.success("Akun berhasil dibuat! Silakan login.")
                st.session_state.page = "login"
                st.rerun()

        if st.button("Kembali ke Login", key="back_to_login"):
            st.session_state.page = "login"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# Inisialisasi state
if "page" not in st.session_state:
    st.session_state.page = "signup"

if "CREDENTIALS" not in st.session_state:
    st.session_state.CREDENTIALS = {"admin": "admin"}

signup_page()