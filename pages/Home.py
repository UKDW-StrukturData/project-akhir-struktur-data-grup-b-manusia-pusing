import streamlit as st
import pandas as pd
import json
import os

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f1c2c, #0d0d0d);
            color: #e0f7fa;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #00bcd4;
            text-shadow: 0 0 5px rgba(0, 188, 212, 0.5);
        }
        .stDataFrame {
            border: 1px solid #00bcd4;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 188, 212, 0.4);
        }
    </style>
""", unsafe_allow_html=True)

# Login Guard dibantu GPT dan ASDOS
def require_login_page():
    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("App.py")

require_login_page()

a, b, c = st.columns(3)
with a:
    st.image("LogoNuevaMoneda.png", width=750)

username = st.session_state.get("username", "User")

st.title(f"Selamat datang {username} di NuevaMoneda")
st.subheader("Dashboard Nilai Tukar Dunia")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

rate_path = os.path.join(BASE_DIR, "exchange_rate_data.json")
name_path = os.path.join(BASE_DIR, "currency_names.json")

if not os.path.exists(rate_path):
    st.error("File exchange_rate_data.json tidak ditemukan. Menggunakan data dummy.")
    data = {
        "rates": {"USD": 1.0, "IDR": 16000.0, "EUR": 0.9, "JPY": 150.0},
        "base": "USD"
    }
else:
    with open(rate_path, "r", encoding="utf-8") as f:
        data = json.load(f)

if not os.path.exists(name_path):
    st.error("File currency_names.json tidak ditemukan. Menggunakan data dummy.")
    currency_names = {
        "USD": "United States Dollar",
        "IDR": "Indonesian Rupiah",
        "EUR": "Euro",
        "JPY": "Japanese Yen"
    }
else:
    with open(name_path, "r", encoding="utf-8") as f:
        currency_names = json.load(f)

rates = data["rates"]
rows = []

for code, value in rates.items():
    rows.append({
        "Kode": code,
        "Mata Uang": f"{code} - {currency_names.get(code, 'Unknown')}",
        "Nilai (per USD)": value
    })

df = pd.DataFrame(rows).sort_values(by="Nilai (per USD)", ascending=False)

st.markdown("### 📊 Daftar Nilai Tukar (Base: USD)")
st.dataframe(
    df,
    height=600,
    use_container_width=True,
    column_config={
        "Nilai (per USD)": st.column_config.NumberColumn(
            "Nilai (per USD)",
            format="%.4f"
        )
    }
)
