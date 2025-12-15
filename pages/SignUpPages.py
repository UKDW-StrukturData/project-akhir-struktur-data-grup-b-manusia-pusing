import streamlit as st

def signup_page():
    # pembuatan markdown dibantu oleh GPT
    a,b,c = st.columns(3)
    
    with b:
        st.image("LogoNuevaMoneda.png", width=750 )
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
            st.session_state.page = "login"
            st.rerun()

    if st.button("Kembali ke Login"):
        st.session_state.page = "login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
