import streamlit as st

def login_page():
    # pembuatan markdown dibantu oleh GPT + ASDOS
    a,b,c = st.columns(3)
    
    with b:
        st.image("LogoNuevaMoneda.png", width=750 )
        
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
        st.session_state.page = "signup"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
