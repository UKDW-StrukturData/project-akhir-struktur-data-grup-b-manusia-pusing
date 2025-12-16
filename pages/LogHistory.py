import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from streamlit_autorefresh import st_autorefresh

# CSS KUSTOM FUTURISTIK MODERN GLASS
st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%);
            color: #e0f7fa;
            font-family: 'Segoe UI', Roboto, sans-serif;
        }
        h1, h2, h3, h4 {
            color: #00bcd4 !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 188, 212, 0.7);
        }

        /* Container Kaca */
        .main .block-container {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 25px;
            border: 1px solid rgba(0, 188, 212, 0.15);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            padding: 30px;
            margin-top: 20px;
        }

        /* DataFrame Styles */
        .stDataFrame {
            border: 1px solid rgba(0, 188, 212, 0.3);
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0, 188, 212, 0.1);
            background-color: rgba(13, 25, 42, 0.6);
            backdrop-filter: blur(10px);
        }

        /* Input Styling */
        .stSelectbox>div>div>div>div>div {
            background-color: rgba(0, 0, 0, 0.5) !important;
            border: 1px solid #00bcd4 !important;
            color: #00e5ff !important;
            border-radius: 10px;
            padding: 10px;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        }
    </style>
""", unsafe_allow_html=True)


st_autorefresh(interval=10000, key="auto_refresh")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("LogoNuevaMoneda.png", width=250)

# LOGIN GUARD 
def require_login_page():
    if not st.session_state.get("logged_in"):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("LoginPages.py")
require_login_page()

st.title("LogHistory Transaksi")
st.write("Riwayat transaksi penukaran uang Anda.")

# LOAD DATA JSON
file_path = "transaction_history.json"

if os.path.exists(file_path):
    try:
        with open(file_path, "r") as f:
            transaksi = json.load(f)
    except json.JSONDecodeError:
        transaksi = []
        st.error("File JSON rusak atau sedang diakses.")
else:
    transaksi = []

if transaksi:
    df = pd.DataFrame(transaksi)
    df["tanggal"] = pd.to_datetime(
        df["tanggal"],
        format="%d-%m-%Y",
        errors="coerce"
    )
    df = df.dropna(subset=["tanggal"])
    df = df.sort_values("tanggal").reset_index(drop=True)

    df["tahun"] = df["tanggal"].dt.year
    df["bulan"] = df["tanggal"].dt.strftime("%Y-%m")

    st.subheader("📄 Tabel Transaksi 1 Tahun")

    tahun_terpilih = st.selectbox(
        "Pilih Tahun:",
        sorted(df["tahun"].unique())
    )

    df_tahun = df[df["tahun"] == tahun_terpilih]
    st.dataframe(df_tahun, use_container_width=True)

    st.subheader("📄 Tabel Transaksi Per Bulan")

    bulan_terpilih = st.selectbox(
        "Pilih Bulan:",
        sorted(df_tahun["bulan"].unique()),
        key="bulan_select"
    )

    df_bulan = df_tahun[df_tahun["bulan"] == bulan_terpilih]
    st.dataframe(df_bulan, use_container_width=True)

    st.subheader("📈 Grafik Profit per Transaksi (Bulanan)")

    chart_placeholder = st.empty()

    # Matplotlib Theme Dark Cyberpunk
    fig, ax = plt.subplots(facecolor="#0f1c2c") 

    ax.plot(
        range(1, len(df_bulan) + 1),  
        df_bulan["profit_idr"],
        marker="o",
        linestyle="-",
        linewidth=2,
        color="#00bcd4" # Warna garis neon
    )

    # Styling futuristik
    ax.set_xlabel("Urutan Transaksi", color="#e0f7fa")
    ax.set_ylabel("Profit (IDR)", color="#e0f7fa")
    ax.set_title(f"Grafik Profit Transaksi Bulan {bulan_terpilih}", color="#00bcd4")
    ax.tick_params(axis='x', colors='#e0f7fa')
    ax.tick_params(axis='y', colors='#e0f7fa')
    ax.spines['bottom'].set_color('#00bcd4')
    ax.spines['left'].set_color('#00bcd4')
    ax.grid(axis='y', linestyle='--', alpha=0.5, color="#1a3a50")
    ax.set_facecolor("#1e2a38") 

    chart_placeholder.pyplot(fig)

else:
    st.warning("Belum ada transaksi yang tersimpan.")