# import streamlit as st
# from backend_auth import init_db, register_user, login_user


# # Jalankan DB saat start
# init_db()


# def main():
#     st.title("Money Changer Admin")

#     menu = ["Login", "Register"]
#     choice = st.sidebar.selectbox("Menu", menu)

#     if choice == "Login":
#         st.subheader("Login Admin")

#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")

#         if st.button("Login"):
#             user = login_user(username, password)

#             if user:
#                 st.session_state["login"] = True
#                 st.session_state["user"] = username
#                 st.success(f"Welcome, {username}")
#             else:
#                 st.error("Username atau password salah!")

#     elif choice == "Register":
#         st.subheader("Buat Akun Baru")

#         new_user = st.text_input("Username Baru")
#         new_password = st.text_input("Password Baru", type="password")

#         if st.button("Register"):
#             if register_user(new_user, new_password):
#                 st.success("Akun berhasil dibuat! Silahkan login.")
#             else:
#                 st.error("Username sudah digunakan!")


# if __name__ == "__main__":
#     main()
