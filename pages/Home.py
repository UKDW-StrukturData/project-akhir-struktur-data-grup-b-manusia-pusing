import streamlit as st
import pandas as pd
import json
import os

a,b,c = st.columns(3)
    
with a:
    st.image("LogoNuevaMoneda.png", width=750 )
        
# LOGIN GUARD
def require_login():    
    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("LoginPages.py")

require_login()
username = st.session_state.get("username", "User")

st.title(f"Selamat datang {username} di Halaman Home!")

# LOAD DATA JSON DARI FOLDER UTAMA
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

rate_path = os.path.join(BASE_DIR, "exchange_rate_data.json")
name_path = os.path.join(BASE_DIR, "currency_names.json")

with open(rate_path, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(name_path, "r", encoding="utf-8") as f:
    currency_names = json.load(f)

rates = data["rates"]


# GABUNGKAN: KODE + NAMA MATA UANG + NILAI
combined = []

for code, value in rates.items():
    full_name = currency_names.get(code, "Unknown Currency")
    combined.append({
        "Kode": code,
        "Mata Uang": f"{code} - {full_name}",
        "Nilai (per USD)": value
    })

# SORTING
df = pd.DataFrame(combined).sort_values(by="Nilai (per USD)", ascending=False)


# SHOW TABLE
st.dataframe(df, height=600, width=700)
st.subheader("Mata Uang dengan Nilai Tertinggi")
