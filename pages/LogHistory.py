import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# Fungsi GUARD dibantu untuk CHAT GPT
def require_login():
    if "logged_in" not in st.session_state or st.session_state.logged_in is False:
        st.warning("Anda harus login untuk mengakses halaman ini.")
        st.switch_page("LoginPages.py")
require_login()

st.title("LogHistory Transaksi")
st.write("Riwayat transaksi penukaran uang Anda.")

# load data transaksi dibatu oleh CHAT GPT
file_path = "transaction_history.json"

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        transaksi = json.load(f)
else:
    transaksi = []


if transaksi:
    df = pd.DataFrame(transaksi)
    st.subheader("Tabel Riwayat Transaksi")

    st.dataframe(df)

    df["tanggal"] = pd.to_datetime(df["tanggal"], format="%d-%m-%Y")

    df["bulan"] = df["tanggal"].dt.strftime("%Y-%m")

    bulan_terpilih = st.selectbox("Pilih bulan transaksi:", sorted(df["bulan"].unique()))

    df_bulan = df[df["bulan"] == bulan_terpilih]

    st.write(f"### Transaksi bulan {bulan_terpilih}")
    st.dataframe(df_bulan)

    st.write("### Grafik Profit Bulanan")

    total_profit = df.groupby("bulan")["profit_idr"].sum()

    fig, ax = plt.subplots()
    ax.plot(total_profit.index, total_profit.values, marker="o")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Profit (IDR)")
    ax.set_title("Grafik Total Profit per Bulan")
    ax.grid(True)

    st.pyplot(fig)

else:
    st.warning("Belum ada transaksi yang tersimpan.")
