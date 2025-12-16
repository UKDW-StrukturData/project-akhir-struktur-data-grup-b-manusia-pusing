import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from streamlit_autorefresh import st_autorefresh

st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(ellipse at center, #240b36 0%, #000000 100%);
            color: #e0f7fa;
            font-family: 'Segoe UI', Roboto, sans-serif;
        }
        h1, h2, h3, h4 {
            color: #875aff !important; /* Neon Ungu */
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(135, 90, 255, 0.7);
        }

        /* Container Kaca (Glassmorphism) */
        .main .block-container {
            background: rgba(46, 17, 71, 0.35);
            border-radius: 25px;
            border: 1px solid rgba(135, 90, 255, 0.25);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            padding: 40px;
            margin-top: 30px;
        }

        /* DataFrame Styles - Glassmorphism */
        .stDataFrame {
            border: 1px solid rgba(135, 90, 255, 0.5);
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(135, 90, 255, 0.3);
            background-color: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(8px);
        }
        
        /* Input Styling - Glassmorphism */
        .stSelectbox>div>div>div>div>div {
            background-color: rgba(0, 0, 0, 0.6) !important;
            border: 1px solid #875aff !important;
            color: #b196ff !important;
            border-radius: 10px;
            padding: 10px;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5), 0 0 5px #875aff;
        }
        
        /* Sidebar styling */
        .stSidebar > div:first-child {
            background: rgba(46, 17, 71, 0.5); /* Sidebar Glassmorphism */
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(135, 90, 255, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

st_autorefresh(interval=10000, key="auto_refresh")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("LogoNuevaMoneda.png", width=250)

def require_login_page():
    if not st.session_state.get("logged_in"):
        st.switch_page("LoginPages.py")

require_login_page()

st.title("Log History Transaksi")

# Path Folder dibantu GPT
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "transaction_history.json")

if not os.path.exists(file_path):
    st.info("Belum ada transaksi.")
    st.stop()

with open(file_path, "r", encoding="utf-8") as f:
    transaksi = json.load(f)

if not transaksi:
    st.info("Belum ada transaksi.")
    st.stop()

# Hash Table ke DataFrame dibantu GPT
rows = []
for trx_id, trx_data in transaksi.items():
    item = trx_data.copy()
    item["transaction_id"] = trx_id
    rows.append(item)

df = pd.DataFrame(rows)

required_cols = {"tanggal", "profit_idr"}
if not required_cols.issubset(df.columns):
    st.error("Format data transaksi tidak valid")
    st.stop()

df["tanggal"] = pd.to_datetime(
    df["tanggal"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

df = df.dropna(subset=["tanggal"])

df["tahun"] = df["tanggal"].dt.year
df["bulan"] = df["tanggal"].dt.strftime("%Y-%m")

tahun = st.selectbox("Pilih Tahun", sorted(df["tahun"].unique()))
df_tahun = df[df["tahun"] == tahun]

bulan = st.selectbox("Pilih Bulan", sorted(df_tahun["bulan"].unique()))
df_bulan = df_tahun[df_tahun["bulan"] == bulan]

st.dataframe(
    df_bulan.sort_values("tanggal", ascending=False),
    use_container_width=True
)

if not df_bulan.empty:
    fig, ax = plt.subplots(facecolor="#10051a")
    ax.plot(
            df_bulan["tanggal"], # Menggunakan kolom tanggal
            df_bulan["profit_idr"],
            marker="o",
            linestyle="-",
            linewidth=2,
            color="#b196ff"
    )
    ax.set_title("Profit Transaksi Bulanan", color="#b196ff", fontsize=16)
    ax.set_xlabel("Tanggal", color="#e0f7fa", fontsize=12)
    ax.set_ylabel("IDR", color="#e0f7fa", fontsize=12)
    plt.xticks(rotation=45)
    ax.tick_params(axis='x', colors='#e0f7fa')
    ax.tick_params(axis='y', colors='#e0f7fa')
    ax.spines['bottom'].set_color('#b196ff')
    ax.spines['top'].set_color('#240b36')
    ax.spines['right'].set_color('#240b36')
    ax.spines['left'].set_color('#b196ff')
    ax.grid(axis='y', linestyle='--', alpha=0.3, color="#5e35b1")
    ax.set_facecolor("#1a082b")
    #plt.tight_layout(rotation=45)
    plt.xticks(rotation=45)
    st.pyplot(fig)
