import streamlit as st
import requests 
import pandas as pd
import matplotlib.pyplot as plt
import json

# Fungsi GUARD dibantu untuk CHAT GPT
def require_login():
    if "logged_in" not in st.session_state or st.session_state.logged_in is False:
        st.warning("Anda harus login untuk mengakses halaman ini.")
        st.switch_page("LoginPages.py")
require_login()
username = st.session_state.get("username", "User")

st.title(f"Selamat datang {username} di Halaman Home!")
st.write("proses pengembangan")

# API_URL = "https://api.exchangerate-api.com/v4/latest/IDR"
# response = requests.get(API_URL)

# if response.status_code == 200:
#     table_data = response



# Menampilkan 8 Mata uang dengan currency tertinggi


a, b = st.columns([1, 1])

with a:
    with open ("exchange_rate_data.json", "r") as table_data:
        data = json.load(table_data)

    rates = data["rates"]
    Best_currency = sorted(rates.items(), key=lambda x: x[1], reverse=True) # Sorting nilai currency melalui GPT

    st.dataframe(Best_currency, height=600, width=700)
    st.write("Mata Uang dengan Nilai Tertinggi")
    
# with b:
#     with open ("exchange_rate_data.json", "r") as table_data:
#         data = json.load(table_data)
    
    
#     st.write("Mata Uang dengan Nilai Terendah")