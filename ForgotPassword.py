import streamlit as st
from database import update_password

def forgot_password_page():
    st.markdown("""
        <style>
            .stApp {
                background: radial-gradient(ellipse at center, #240b36 0%, #000000 100%);
                color: #e0f7fa;
            }
            
            .title {
                text-align: center;
                color: #b196ff;
                font-size: 2.5em;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 40px;
                text-transform: uppercase;
                letter-spacing: 3px;
                text-shadow: 0 0 15px rgba(177, 150, 255, 0.8);
            }
            
            .stTextInput>div>div>input {
                background-color: rgba(0, 0, 0, 0.5) !important;
                border: 1px solid #b196ff !important;
                color: #e0f7fa !important;
                border-radius: 10px !important;
                padding: 12px !important;
                box-shadow: 0 0 5px rgba(177, 150, 255, 0.3) !important;
            }
            
            .stButton>button {
                width: 100%;
                background: linear-gradient(90deg, #875aff, #b196ff);
                color: #000000;
                font-weight: bold;
                border-radius: 10px;
                margin-top: 10px;
                transition: all 0.3s;
                border: none;
                box-shadow: 0 0 10px #875aff;
            }

            .stButton>button:hover {
                background: linear-gradient(90deg, #b196ff, #875aff);
                box-shadow: 0 0 15px #b196ff, 0 0 30px #b196ff;
            }
            
        </style>
    """, unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with b:
        st.image("LogoNuevaMoneda.png", width=750)
    st.markdown('<div class="title">Reset Password</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    new_password = st.text_input("Password Baru", type="password")
    confirm_password = st.text_input("Konfirmasi Password", type="password")

    if st.button("Reset Password"):
        if not username or not new_password:
            st.error("Semua field wajib diisi")
        elif new_password != confirm_password:
            st.error("Password tidak sama")
        elif len(new_password) < 4:
            st.error("Password minimal 4 karakter")
        else:
            if update_password(username, new_password):
                st.success("Password berhasil direset")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Username tidak ditemukan")

    if st.button("Kembali ke Login"):
        st.session_state.page = "login"
        st.rerun()
