import streamlit as st

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f1c2c, #0d0d0d);
            color: #e0f7fa;
        }
        h1, h2, h3, h4 {
            color: #00bcd4; /* Judul Neon */
            text-shadow: 0 0 5px rgba(0, 188, 212, 0.5);
        }
        /* Glassmorphism Card (Mirip dengan yang ada, tapi disempurnakan) */
        .card {
            background: rgba(255, 255, 255, 0.05); /* Latar Belakang Transparan */
            padding: 30px;
            border-radius: 20px;
            color: white;
            width: 90%;
            margin: 30px auto;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .round-img {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            object-fit: cover;
            border: 5px solid #00bcd4; /* Border Neon */
            box-shadow: 0 0 10px #00bcd4;
        }
        .stButton>button {
            background: #00bcd4;
            color: #0f1c2c;
            font-weight: bold;
            border-radius: 10px;
            margin-top: 10px;
            transition: all 0.3s;
            border: none;
            box-shadow: 0 0 5px #00bcd4;
        }
        .stButton>button:hover {
            background: #00e5ff;
            box-shadow: 0 0 10px #00e5ff, 0 0 25px #00e5ff;
        }
        /* Tombol danger/primary */
        .stButton button[kind="primary"] {
            background-color: #ff4b4b !important;
            box-shadow: 0 0 5px #ff4b4b;
        }
        .stButton button[kind="primary"]:hover {
            background-color: #ff6e6e !important;
            box-shadow: 0 0 10px #ff6e6e, 0 0 25px #ff6e6e;
        }
        /* Input/Selectbox */
        .stTextInput>div>div>input, .stSelectbox>div>div>div>div>div {
            background-color: rgba(30, 40, 50, 0.7);
            border: 1px solid #00bcd4;
            color: #e0f7fa;
            border-radius: 8px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)


# Fungsi GUARD dibantu untuk CHAT GPT
def require_login():
    if "logged_in" not in st.session_state or st.session_state.logged_in is False:
        st.warning("Anda harus login untuk mengakses halaman ini.")
        st.switch_page("LoginPages.py")
require_login()

if "username" not in st.session_state:
    st.session_state.username = "ADMIN"
if "user_id" not in st.session_state:
    st.session_state.user_id = "12345678"
if "show_change_username" not in st.session_state:
    st.session_state.show_change_username = False
if "bahasa" not in st.session_state:
    st.session_state.bahasa = "Indonesia"

st.markdown("""
    <h1 style='text-align:center; color:#00bcd4; margin-bottom: 0px;'>PENGATURAN AKUN</h1>
""", unsafe_allow_html=True)


# st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        "<img class='round-img' src='https://i.ibb.co/680385F/avatar-futuristic.png'>", 
        unsafe_allow_html=True
    )

with col2:
    st.subheader("Username Aktif")
    st.markdown(f"<h2 style='color:white;'>{st.session_state.username}</h2>", unsafe_allow_html=True)
    # st.write(f"**ID Kredensial:** `{st.session_state.user_id}`") 

st.write("---")


# FITUR GANTI USERNAME (Dibuka Dengan Button)
st.subheader("Ganti Username")

if not st.session_state.show_change_username:
    if st.button("Ganti Username"):
        st.session_state.show_change_username = True
else:
    new_username = st.text_input("Masukkan Username Baru", value=st.session_state.username)
    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("Simpan Username", use_container_width=True):
            st.session_state.username = new_username
            st.session_state.show_change_username = False
            st.success("Username berhasil diperbarui!")
    with col_cancel:
        if st.button("Batal", use_container_width=True):
            st.session_state.show_change_username = False

st.write("---")


# FITUR GANTI BAHASA
st.subheader("Ganti Bahasa")

bahasa_list = [
    "Indonesia", "English (Global)", "China", "Jepang", "Korea", "Arab", "Jawa (Lokal)"
]

bahasa_index = bahasa_list.index(st.session_state.bahasa) if st.session_state.bahasa in bahasa_list else 0

bahasa = st.selectbox("Pilih Bahasa", bahasa_list, index=bahasa_index)

if st.button("Simpan"):
    st.session_state.bahasa = bahasa
    st.success(f"Antarmuka berhasil diubah ke: {bahasa}")

st.write("---")


# GANTI AKUN
st.subheader("Kelola Sesi Akun")

if st.button("LOGOUT", type="primary"):
    st.session_state.logged_in = False
    st.success("Sesi berhasil diakhiri. Kembali ke Halaman Login...")
    st.switch_page("LoginPages.py")
# HAPUS AKUN
st.subheader("Manajemen Akun Permanen")

if st.button("⚠️ Hapus Akun Permanen", type="primary"):
    # Logika penghapusan kredensial (simulasi)
    if st.session_state.get("username") in st.session_state.get("CREDENTIALS", {}):
        del st.session_state.CREDENTIALS[st.session_state.username]
    
    st.error("Akun berhasil dihapus! Sesi diakhiri.")
    st.session_state.logged_in = False
    st.switch_page("LoginPages.py")

st.markdown("</div>", unsafe_allow_html=True)