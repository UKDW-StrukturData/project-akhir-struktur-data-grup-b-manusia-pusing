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

# LOGIN GUARD DIBANTU ASDOS DAN GPT
def require_login():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Anda harus login untuk mengakses halaman ini.")
        st.switch_page("LoginPages.py")

require_login()

st.title("LogHistory Transaksi")
st.write("Riwayat transaksi penukaran uang Anda.")

# LOAD DATA JSON DIBANTU ASDOS DAN GPT
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

    df["tanggal"] = pd.to_datetime(
        df["tanggal"],
        format="%d-%m-%Y",
        errors="coerce"
    )
    df = df.dropna(subset=["tanggal"])

    df = df.sort_values("tanggal").reset_index(drop=True)

    st.write("### 📊 Grafik Profit per Transaksi")

    chart_placeholder = st.empty()

    fig, ax = plt.subplots()

    ax.plot(
        df["tanggal"],
        df["profit_idr"],
        marker="o",
        linestyle="-",
        linewidth=2
    )

    ax.set_xlabel("Tanggal Transaksi")
    ax.set_ylabel("Profit (IDR)")
    ax.set_title("Grafik Profit per Transaksi")
    ax.grid(True)
    ax.tick_params(axis="x", rotation=45)

    chart_placeholder.pyplot(fig)

else:
    st.warning("Belum ada transaksi yang tersimpan.")
