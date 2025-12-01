import streamlit as st

# Fungsi GUARD dibantu untuk CHAT GPT
def require_login():
    if "logged_in" not in st.session_state or st.session_state.logged_in is False:
        st.warning("Anda harus login untuk mengakses halaman ini.")
        st.switch_page("LoginPages.py")
require_login()

st.title("Pengaturan")
st.write("proses pengembangan")

# Setup user state
if "username" not in st.session_state:
    st.session_state.username = "ADMIN"
if "user_id" not in st.session_state:
    st.session_state.user_id = "12345678"
if "show_change_username" not in st.session_state:
    st.session_state.show_change_username = False

# ----------- TITLE -----------
st.markdown("""
    <h1 style='text-align:center; color:white; margin-bottom: 0px;'>PENGATURAN</h1>
""", unsafe_allow_html=True)


# ----------- CUSTOM CSS -----------
st.markdown("""
<style>
.card {
    background: linear-gradient(160deg, #0f4c81, #0b61c9);
    padding: 30px;
    border-radius: 20px;
    color: white;
    width: 80%;
    margin: auto;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
}
.round-img {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid white;
}
</style>
""", unsafe_allow_html=True)


# -------- CARD PROFILE ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        "<img class='round-img' src='https://i.ibb.co/4Y7JjQZ/avatar.png'>",
        unsafe_allow_html=True
    )

with col2:
    st.subheader("Username")
    st.markdown(f"<h2 style='color:white;'>{st.session_state.username}</h2>", unsafe_allow_html=True)
    st.write(f"**ID USER {st.session_state.user_id}**")

st.write("---")


# FITUR GANTI USERNAME (Dibuka Dengan Button)
st.subheader("Ganti Username")

if not st.session_state.show_change_username:
    if st.button("Ganti Username"):
        st.session_state.show_change_username = True
else:
    new_username = st.text_input("Masukkan Username Baru", value=st.session_state.username)
    if st.button("Simpan Username"):
        st.session_state.username = new_username
        st.session_state.show_change_username = False
        st.success("Username berhasil diperbarui!")
    if st.button("Batal"):
        st.session_state.show_change_username = False

st.write("---")


# FITUR GANTI BAHASA
st.subheader("Ganti Bahasa")

bahasa_list = [
    "Indonesia", "English", "China", "Jepang", "Korea", "Arab", "Jawa"
]

bahasa = st.selectbox("Pilih Bahasa", bahasa_list)

if st.button("Simpan Bahasa"):
    st.session_state.bahasa = bahasa
    st.success(f"Bahasa berhasil diubah ke: {bahasa}")

st.write("---")


# GANTI AKUN
st.subheader("Ganti Akun")

if st.button("Keluar & Ganti Akun"):
    st.session_state.logged_in = False
    st.success("Berhasil logout, silakan login dengan akun lain.")
    st.switch_page("LoginPages.py")

st.write("---")


# HAPUS AKUN
st.subheader("Hapus Akun")

if st.button("⚠️ Hapus Akun", type="primary"):
    st.error("Akun berhasil dihapus! (Simulasi)")
    st.session_state.logged_in = False
    st.switch_page("LoginPages.py")

st.markdown("</div>", unsafe_allow_html=True)