import streamlit as st
from database import update_password

def forgot_password_page():
    st.markdown("""
        <style>
            .title {
                text-align: center;
                color: #ff9800;
                font-size: 2.2em;
                margin-bottom: 30px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">Reset Password</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    new_password = st.text_input("Password Baru", type="password")
    confirm_password = st.text_input("Konfirmasi Password", type="password")

    if st.button("Reset Password"):
        if not username or not new_password:
            st.error("❌ Semua field wajib diisi")
        elif new_password != confirm_password:
            st.error("❌ Password tidak sama")
        elif len(new_password) < 4:
            st.error("❌ Password minimal 4 karakter")
        else:
            if update_password(username, new_password):
                st.success("✅ Password berhasil direset")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("❌ Username tidak ditemukan")

    if st.button("Kembali ke Login"):
        st.session_state.page = "login"
        st.rerun()
