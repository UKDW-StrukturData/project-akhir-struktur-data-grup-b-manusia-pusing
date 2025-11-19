import streamlit as st

# ====================== PAGE CONFIG ======================
st.set_page_config(page_title="Money Changer", page_icon="💱", layout="wide")

# ====================== HIDE AUTO PAGE TITLE "LoginPages" ======================
if st.session_state.get("logged_in", False):
    # Hanya sembunyikan LoginPages jika sudah login
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] > div:first-child {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ====================== SESSION STATE INIT ======================
if "page" not in st.session_state:
    st.session_state.page = "signup"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "CREDENTIALS" not in st.session_state:
    st.session_state.CREDENTIALS = {}

# ====================== LOGIN GUARD ======================
def login_guard():
    if not st.session_state.logged_in:
        st.warning("Anda harus login terlebih dahulu.")
        st.session_state.page = "login"
        st.rerun()

# ====================== HIDE SIDEBAR WHEN LOGGED OUT ======================
if not st.session_state.logged_in:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

# ====================== CSS STYLE LOGIN ======================
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
</style>
""", unsafe_allow_html=True)

# ====================== HELPER PAGE ROUTER ======================
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
            st.switch_page("pages/Home.py")
        else:
            st.error("Username atau password salah!")

    if st.button("Go to Sign Up"):
        goto("signup")

    st.markdown("</div>", unsafe_allow_html=True)

# ====================== SIGNUP PAGE ======================
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
            st.success("Akun berhasil dibuat!")
            goto("login")

    if st.button("Back to Login"):
        goto("login")

    st.markdown("</div>", unsafe_allow_html=True)

# ====================== DASHBOARD PAGE ======================
def page_dashboard():
    login_guard()

    st.sidebar.title("💱 Money Changer Admin Panel")
    st.sidebar.write("Menu aplikasi…")

    st.title("Selamat Datang di Dashboard Money Changer!")
    st.success(f"Anda login sebagai: {st.session_state.username}")

    # ---- LOGOUT BUTTON PALING BAWAH ----
    st.sidebar.markdown("----")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

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
