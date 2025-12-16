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

    new_user = st.text_input("Username", key="signup_username")
    new_pass = st.text_input("Password", type="password", key="signup_password")
    confirm  = st.text_input("Konfirmasi Password", type="password", key="signup_confirm")

    if st.button("Daftar", key="signup_action"):
        if not new_user or not new_pass or not confirm:
            st.error("Semua kolom wajib diisi.")
        elif new_user in st.session_state.CREDENTIALS:
            st.warning("Username sudah digunakan. Silakan gunakan username lain.")
        elif new_pass != confirm:
            st.error("Password tidak cocok.")
        else:
            st.session_state.CREDENTIALS[new_user] = new_pass
            st.toast("🎉 Akun berhasil dibuat! Silakan login.", icon="✅")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Kembali ke Login", key="back_to_login"):
        st.session_state.page = "login"
        st.rerun()

if "CREDENTIALS" not in st.session_state:
    st.session_state.CREDENTIALS = {
        "admin": "admin"
    }
