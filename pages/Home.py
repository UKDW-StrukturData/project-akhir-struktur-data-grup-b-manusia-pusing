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
            color: #00bcd4; /* Judul Neon */
            text-shadow: 0 0 5px rgba(0, 188, 212, 0.5);
        }
        /* Custom styling untuk Dataframe (Tabel) */
        .stDataFrame {
            border: 1px solid #00bcd4;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 188, 212, 0.4);
        }
        /* Header Dataframe */
        .data-header {
            background-color: #1a3a50 !important;
            color: #e0f7fa !important;
            font-weight: bold;
        }
        /* Rows Dataframe */
        .data-row {
            background-color: #1e2a38 !important;
            color: #e0f7fa !important;
        }
        .data-row:nth-child(even) {
            background-color: #253342 !important;
        }
    </style>
""", unsafe_allow_html=True)

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

st.title(f"Selamat datang {username} di NuevaMoneda")
st.subheader("Dashboard Nilai Tukar Dunia")

# LOAD DATA JSON DARI FOLDER UTAMA
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

rate_path = os.path.join(BASE_DIR, "exchange_rate_data.json")
name_path = os.path.join(BASE_DIR, "currency_names.json")

# Periksa dan buat file dummy jika tidak ada (untuk menjaga kode tetap berjalan)
if not os.path.exists(rate_path):
    st.error(f"File {rate_path} tidak ditemukan. Membuat data dummy.")
    data = {"rates": {"USD": 1.0, "IDR": 16000.0, "EUR": 0.9, "JPY": 150.0}, "updated_at": "2025-01-01", "base": "USD", "date": "2025-01-01"}
else:
    with open(rate_path, "r", encoding="utf-8") as f:
        data = json.load(f)

if not os.path.exists(name_path):
    st.error(f"File {name_path} tidak ditemukan. Membuat data dummy.")
    currency_names = {"USD": "United States Dollar", "IDR": "Indonesian Rupiah", "EUR": "Euro", "JPY": "Japanese Yen"}
else:
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
        "Nilai (per USD)": f"{value:,.4f}" # Format angka
    })

df = pd.DataFrame(combined).sort_values(by="Nilai (per USD)", ascending=False)
st.markdown("### 📊 Daftar Nilai Tukar (Base: USD)", unsafe_allow_html=True)
st.dataframe(
    df, 
    height=600, 
    use_container_width=True,
    column_config={
        "Nilai (per USD)": st.column_config.NumberColumn(
            "Nilai (per USD)",
            format="%.4f", 
        )
    }
)