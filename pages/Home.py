import streamlit as st
import pandas as pd
import json
import os

st.markdown("""
    <style>
        .stApp {
            /* Gradasi Ungu Gelap ke Hitam Pekat */
            background: radial-gradient(ellipse at center, #240b36 0%, #000000 100%);
            color: #e0f7fa;
            font-family: 'Segoe UI', Roboto, sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #875aff; /* Judul Neon Ungu */
            text-shadow: 0 0 8px rgba(135, 90, 255, 0.7);
        }
        
        /* Glassmorphism Card (Meniru Container Utama) */
        .st-emotion-cache-1cypcdb { /* Targetting main content container */
            background: rgba(46, 17, 71, 0.35); 
            border-radius: 20px;
            padding: 30px;
            margin-top: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(135, 90, 255, 0.2); 
        }

        /* Custom styling untuk Dataframe (Tabel) - Glassmorphism */
        .stDataFrame {
            border: 1px solid rgba(135, 90, 255, 0.5);
            border-radius: 15px;
            box-shadow: 0 0 15px rgba(135, 90, 255, 0.3);
            background-color: rgba(0, 0, 0, 0.4); /* Background hitam transparan */
        }
        /* Header Dataframe */
        .data-header {
            background-color: #3b0e5c !important; /* Ungu gelap */
            color: #e0f7fa !important;
            font-weight: bold;
        }
        /* Rows Dataframe */
        .data-row {
            background-color: rgba(0, 0, 0, 0.4) !important;
            color: #e0f7fa !important;
        }
        .data-row:nth-child(even) {
            background-color: rgba(20, 5, 30, 0.4) !important; /* Row genap sedikit lebih gelap */
        }
        
        /* Sidebar styling */
        .stSidebar > div:first-child {
            background: rgba(46, 17, 71, 0.5); /* Sidebar Glassmorphism */
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(135, 90, 255, 0.3);
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
