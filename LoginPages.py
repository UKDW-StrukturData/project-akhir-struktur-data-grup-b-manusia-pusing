import streamlit as st

# ====================== PAGE CONFIG ======================
st.set_page_config(page_title="Money Changer", page_icon="💱", layout="wide")

# ====================== SESSION STATE INIT ======================
if "page" not in st.session_state:
    st.session_state.page = "signup"   # wajib sign up dulu

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "CREDENTIALS" not in st.session_state:
    st.session_state.CREDENTIALS = {}  # kosong, harus signup dulu

# ====================== HIDE SIDEBAR WHEN LOGGED OUT ======================
if not st.session_state.logged_in:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

# ====================== CSS STYLE (UI MIRIP GAMBAR) ======================
st.markdown("""
<style>
body { background-color: #e8e8e8; }

.login-container {
    width: 420px;
    margin: auto;
    margin-top: 50px;
    background: white;
    padding: 45px 40px;
    border-radius: 10px;
    border: 3px solid #c9c9c9;
}

.logo-box {
    width: 150px;
    margin: auto;
    padding: 8px;
    border: 1px solid black;
    text-align: center;
    font-weight: bold;
    margin-bottom: 25px;
}

.title {
    font-size: 28px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 25px;
}
.link-center {
    text-align:center;
    margin-top:15px;
}
.google-btn img {
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

# ====================== PAGE ROUTER ======================
def goto(page):
    st.session_state.page = page
    st.rerun()

# ====================== LOGIN PAGE ======================
def page_login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="logo-box">LOGO</div>', unsafe_allow_html=True)
    st.markdown('<div class="title">Welcome Back 👋</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Continue"):
        if username in st.session_state.CREDENTIALS and st.session_state.CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username

            # ====================== REDIRECT KE HOME ======================
            st.switch_page("pages/Home.py")

        else:
            st.error("Username atau password salah!")

    st.markdown("<p style='text-align:center;'>or continue with</p>", unsafe_allow_html=True)
    st.markdown(
        '<div class="google-btn" style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/4/4a/Logo_2013_Google.png" width="40"></div>',
        unsafe_allow_html=True,
    )

    st.write("")
    if st.button("Go to Sign Up"):
        goto("signup")

    st.markdown('</div>', unsafe_allow_html=True)

# ====================== SIGN UP PAGE ======================
def page_signup():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="logo-box">LOGO</div>', unsafe_allow_html=True)
    st.markdown('<div class="title">Create Account</div>', unsafe_allow_html=True)

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if new_user == "" or new_pass == "":
            st.error("Semua field harus diisi")
        elif new_user in st.session_state.CREDENTIALS:
            st.error("Username sudah digunakan")
        elif new_pass != confirm:
            st.error("Password tidak cocok")
        else:
            st.session_state.CREDENTIALS[new_user] = new_pass
            st.success("Akun berhasil dibuat! Silakan login.")
            goto("login")

    st.write("")
    if st.button("Back to Login"):
        goto("login")

    st.markdown('</div>', unsafe_allow_html=True)

# ====================== DASHBOARD PAGE (tidak terpakai untuk pindah layar) ======================
def page_dashboard():
    st.sidebar.title("💱 Money Changer Admin Panel")
    st.sidebar.write("Menu aplikasi di sini…")

    st.title("Selamat Datang di Dashboard Money Changer!")
    st.success(f"Anda login sebagai: {st.session_state.username}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        goto("login")

# ====================== PROTECT ROUTES ======================
if not st.session_state.logged_in:
    if st.session_state.page not in ["login", "signup"]:
        st.session_state.page = "signup"

# ====================== MAIN ROUTER ======================
if st.session_state.page == "login":
    page_login()
elif st.session_state.page == "signup":
    page_signup()
else:
    page_dashboard()
