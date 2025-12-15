import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from streamlit_autorefresh import st_autorefresh

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f1c2c, #0d0d0d);
            color: #e0f7fa;
        }
        h1, h2, h3, h4 {
            color: #00bcd4; /* Judul Neon */
            text-shadow: 0 0 5px rgba(0, 188, 212, 0.5);
        }
        .stDataFrame {
            border: 1px solid #00bcd4;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 188, 212, 0.4);
        }
        /* Untuk input/select */
        .stSelectbox>div>div>div>div>div {
            background-color: rgba(30, 40, 50, 0.7);
            border: 1px solid #00bcd4;
            color: #e0f7fa;
            border-radius: 8px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)


st_autorefresh(interval=10000, key="auto_refresh")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("LogoNuevaMoneda.png", width=250)

# LOGIN GUARD 
def require_login():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Anda harus login untuk mengakses halaman ini.")
        st.switch_page("LoginPages.py")

require_login()

st.title("LogHistory Transaksi")
st.write("Riwayat transaksi penukaran uang Anda (Data Realtime/Otomatis Refresh).")

# LOAD DATA JSON DIBANTU ASDOS
file_path = "transaction_history.json"

if os.path.exists(file_path):
    try:
        with open(file_path, "r") as f:
            transaksi = json.load(f)
    except json.JSONDecodeError:
        transaksi = []
        st.warning("File riwayat transaksi sedang diakses atau rusak. Menampilkan data kosong.")
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

    st.subheader("📄 Filter Riwayat Transaksi")

    col_tahun, col_bulan = st.columns(2)
    
    with col_tahun:
        tahun_terpilih = st.selectbox(
            "Pilih Tahun:",
            sorted(df["tahun"].unique()),
            key="tahun_select"
        )
    
    df_tahun = df[df["tahun"] == tahun_terpilih]

    with col_bulan:
        bulan_terpilih = st.selectbox(
            "Pilih Bulan:",
            sorted(df_tahun["bulan"].unique()),
            key="bulan_select"
        )

    df_bulan = df_tahun[df_tahun["bulan"] == bulan_terpilih]

    st.markdown(f"### 📑 Data Transaksi Bulan {bulan_terpilih}")
    
    st.dataframe(
        df_bulan[[
            "tanggal", "admin", "asal", "tujuan", 
            "jumlah_awal", "hasil_akhir", "profit_idr", "profit_rate_percent"
        ]], 
        use_container_width=True,
        column_config={
            "jumlah_awal": st.column_config.NumberColumn("Jumlah Awal", format="%.2f"),
            "hasil_akhir": st.column_config.NumberColumn("Hasil Akhir", format="%.2f"),
            "profit_idr": st.column_config.NumberColumn("Profit (IDR)", format="Rp %d"),
            "profit_rate_percent": st.column_config.NumberColumn("Profit Rate (%)", format="%.1f %%"),
        }
    )

    # menampilkan grafik transaski dibantu oleh GPT
    st.subheader("📈 Analisis Profit (Bulanan)")

    chart_placeholder = st.empty()

    # Setup figure matplotlib dengan tema gelap dibantu GPT dan Asdos
    fig, ax = plt.subplots(facecolor="#0f1c2c") 

    ax.plot(
        range(1, len(df_bulan) + 1),  
        df_bulan["profit_idr"],
        marker="o",
        linestyle="-",
        linewidth=2,
        color="#00bcd4" 
    )

    ax.set_xlabel("Urutan Transaksi", color="#e0f7fa")
    ax.set_ylabel("Profit (IDR)", color="#e0f7fa")
    ax.set_title(f"Proyeksi Profit Transaksi Bulan {bulan_terpilih}", color="#00bcd4")
    ax.tick_params(axis='x', colors='#e0f7fa')
    ax.tick_params(axis='y', colors='#e0f7fa')
    ax.spines['bottom'].set_color('#00bcd4')
    ax.spines['left'].set_color('#00bcd4')
    ax.grid(axis='y', linestyle='--', alpha=0.5, color="#1a3a50")
    ax.set_facecolor("#1e2a38") 

    chart_placeholder.pyplot(fig)

else:
    st.warning("Belum ada transaksi yang tersimpan. Silakan lakukan penukaran di menu 'Fitur Penukaran Mata Uang'.")