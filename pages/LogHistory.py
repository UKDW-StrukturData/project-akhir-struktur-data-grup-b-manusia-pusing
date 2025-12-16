import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from streamlit_autorefresh import st_autorefresh

st.markdown("""
<style>
.stApp {
    background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%);
    color: #e0f7fa;
    font-family: 'Segoe UI', Roboto, sans-serif;
}
h1, h2, h3, h4 {
    color: #00bcd4 !important;
    letter-spacing: 2px;
    text-shadow: 0 0 10px rgba(0, 188, 212, 0.7);
}
.main .block-container {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 25px;
    border: 1px solid rgba(0, 188, 212, 0.15);
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    padding: 30px;
}
</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=10000, key="auto_refresh")

col1, col2, col3 = st.columns(3)
with col1:
    st.image("LogoNuevaMoneda.png", width=250)

def require_login_page():
    if not st.session_state.get("logged_in"):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("LoginPages.py")

require_login_page()

st.title("LogHistory Transaksi")
st.write("Riwayat transaksi penukaran uang Anda.")

file_path = "transaction_history.json"

if not os.path.exists(file_path):
    st.warning("Belum ada transaksi yang tersimpan.")
    st.stop()

try:
    with open(file_path, "r") as f:
        transaksi = json.load(f)
except json.JSONDecodeError:
    st.error("File transaksi rusak.")
    st.stop()

if not transaksi:
    st.info("Belum ada transaksi.")
    st.stop()

df = pd.DataFrame(transaksi)

required_columns = {"tanggal", "profit_idr"}

missing = required_columns - set(df.columns)
if missing:
    st.error(f"Format data salah. Kolom hilang: {missing}")
    st.write("Kolom tersedia:", df.columns.tolist())
    st.stop()

df["tanggal"] = pd.to_datetime(
    df["tanggal"],
    errors="coerce",
    dayfirst=True
)

df = df.dropna(subset=["tanggal"])

if df.empty:
    st.warning("Data transaksi tidak valid.")
    st.stop()

df = df.sort_values("tanggal").reset_index(drop=True)

df["tahun"] = df["tanggal"].dt.year
df["bulan"] = df["tanggal"].dt.strftime("%Y-%m")

st.subheader("📄 Tabel Transaksi Tahunan")

tahun_terpilih = st.selectbox(
    "Pilih Tahun:",
    sorted(df["tahun"].unique())
)

df_tahun = df[df["tahun"] == tahun_terpilih]
st.dataframe(df_tahun, use_container_width=True)

st.subheader("📄 Tabel Transaksi Bulanan")

bulan_terpilih = st.selectbox(
    "Pilih Bulan:",
    sorted(df_tahun["bulan"].unique()),
    key="bulan_select"
)

df_bulan = df_tahun[df_tahun["bulan"] == bulan_terpilih]
st.dataframe(df_bulan, use_container_width=True)

st.subheader("📈 Grafik Profit per Transaksi")

if not df_bulan.empty:
    fig, ax = plt.subplots(facecolor="#0f1c2c")

    ax.plot(
        range(1, len(df_bulan) + 1),
        df_bulan["profit_idr"],
        marker="o",
        linewidth=2,
        color="#00bcd4"
    )

    ax.set_xlabel("Urutan Transaksi", color="#e0f7fa")
    ax.set_ylabel("Profit (IDR)", color="#e0f7fa")
    ax.set_title(f"Profit Bulan {bulan_terpilih}", color="#00bcd4")
    ax.tick_params(colors="#e0f7fa")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_facecolor("#1e2a38")

    st.pyplot(fig)
else:
    st.info("Tidak ada transaksi pada bulan ini.")
