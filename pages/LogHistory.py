import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from streamlit_autorefresh import st_autorefresh

# Halaman akan refresh setiap 3 detik
st_autorefresh(interval=3000, key="auto_refresh")

col1, col2, col3 = st.columns(3)
with col1:
    st.image("LogoNuevaMoneda.png", width=250)

# LOGIN GUARD BANTUAN GPT DAN ASDOS
def require_login():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Anda harus login untuk mengakses halaman ini.")
        st.switch_page("LoginPages.py")

require_login()

st.title("LogHistory Transaksi")
st.write("Riwayat transaksi penukaran uang Anda.")

# LOAD DATA DIBANTU OLEH GPT DAN ASDOS
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

    st.subheader("📄 Tabel Riwayat Transaksi")
    st.dataframe(df, use_container_width=True)

    df["tanggal"] = pd.to_datetime(df["tanggal"], format="%d-%m-%Y", errors="coerce")
    df = df.dropna(subset=["tanggal"])

    df["bulan"] = df["tanggal"].dt.strftime("%Y-%m")

    bulan_terpilih = st.selectbox(
        "📅 Pilih bulan transaksi:",
        sorted(df["bulan"].unique())
    )

    df_bulan = df[df["bulan"] == bulan_terpilih]

    st.write(f"### 📌 Transaksi Bulan {bulan_terpilih}")
    st.dataframe(df_bulan, use_container_width=True)

    st.write("### 📊 Grafik Total Profit per Bulan")

    total_profit = (
        df.groupby("bulan", as_index=False)["profit_idr"]
        .sum()
        .sort_values("bulan")
    )

    fig, ax = plt.subplots()
    ax.plot(
        total_profit["bulan"],
        total_profit["profit_idr"],
        marker="o"
    )
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Profit (IDR)")
    ax.set_title("Grafik Total Profit per Bulan")
    ax.grid(True)

    st.pyplot(fig)

else:
    st.warning("Belum ada transaksi yang tersimpan.")
