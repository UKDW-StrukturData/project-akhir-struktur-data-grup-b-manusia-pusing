import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from streamlit_autorefresh import st_autorefresh

# ================== STYLE ==================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle, #1b2735, #090a0f);
    color: #e0f7fa;
}
h1 {
    color: #00bcd4;
}
</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=10000, key="refresh")

# ================== LOGIN GUARD ==================
def require_login_page():
    if not st.session_state.get("logged_in"):
        st.switch_page("LoginPages.py")

require_login_page()

st.title("Log History Transaksi")

# ================== PATH KE FOLDER UTAMA ==================
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

# ================== HASH TABLE → DATAFRAME ==================
rows = []
for trx_id, trx_data in transaksi.items():
    item = trx_data.copy()
    item["transaction_id"] = trx_id
    rows.append(item)

df = pd.DataFrame(rows)

# ================== VALIDASI KOLOM ==================
required_cols = {"tanggal", "profit_idr"}
if not required_cols.issubset(df.columns):
    st.error("Format data transaksi tidak valid")
    st.stop()

# ================== PARSING TANGGAL (FIX ERROR) ==================
df["tanggal"] = pd.to_datetime(
    df["tanggal"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

# Buang baris yang gagal parsing
df = df.dropna(subset=["tanggal"])

# ================== FILTER ==================
df["tahun"] = df["tanggal"].dt.year
df["bulan"] = df["tanggal"].dt.strftime("%Y-%m")

tahun = st.selectbox("Pilih Tahun", sorted(df["tahun"].unique()))
df_tahun = df[df["tahun"] == tahun]

bulan = st.selectbox("Pilih Bulan", sorted(df_tahun["bulan"].unique()))
df_bulan = df_tahun[df_tahun["bulan"] == bulan]

# ================== TABEL ==================
st.dataframe(
    df_bulan.sort_values("tanggal", ascending=False),
    use_container_width=True
)

# ================== GRAFIK ==================
if not df_bulan.empty:
    fig, ax = plt.subplots()
    ax.plot(df_bulan["tanggal"], df_bulan["profit_idr"], marker="o")
    ax.set_title("Profit Transaksi")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("IDR")
    plt.xticks(rotation=45)
    st.pyplot(fig)
