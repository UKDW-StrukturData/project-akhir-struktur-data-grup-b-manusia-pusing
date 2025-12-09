import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=3000, key="auto_refresh")
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
st.write("Riwayat transaksi penukaran uang Anda.")

# LOAD DATA JSON DIBANTU ASDOS
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

    # menampilkan grafik transaski dibantu oleh GPT
    st.subheader("📈 Grafik Profit per Transaksi (Bulanan)")

    chart_placeholder = st.empty()

    fig, ax = plt.subplots()

    ax.plot(
        range(1, len(df_bulan) + 1),  
        df_bulan["profit_idr"],
        marker="o",
        linestyle="-",
        linewidth=2
    )

    ax.set_xlabel("Urutan Transaksi")
    ax.set_ylabel("Profit (IDR)")
    ax.set_title(f"Grafik Profit Transaksi Bulan {bulan_terpilih}")
    ax.grid(True)

    chart_placeholder.pyplot(fig)

else:
    st.warning("Belum ada transaksi yang tersimpan.")
