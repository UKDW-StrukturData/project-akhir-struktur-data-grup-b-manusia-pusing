import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def require_login():
    if "logged_in" not in st.session_state or st.session_state.logged_in is False:
        st.warning("Anda harus login untuk mengakses halaman ini.")
        st.switch_page("LoginPages.py")  
require_login()

st.title("LogHistory Transaksi")
st.write("proses pengembangan")


# DATA COURSE
data = {
    "Mata Uang": ["AUD", "BND", "CAD", "CHF", "CNY", "DKK", "EUR", "GBP", "HKD", "JPY", "KRW", "KWD"],
    "Nilai": [1, 1, 1, 1, 1, 1, 1, 1, 1, 100, 1, 1],
    "Kurs Jual": [10012.84, 9585.78, 9971.78, 13450.26, 1930.97, 1973.05, 14692.38, 16909.12, 1688.10,
                  12890.66, 12.80, 43409.69],
    "Kurs Beli": [9908.10, 9483.52, 9869.62, 13309.69, 1938.54, 1953.14, 14541.12, 16735.30, 1669.11,
                  12758.72, 11.92, 42921.99],
}

df = pd.DataFrame(data)

# TAMPILAN TABEL DENGAN TOMBOL "LIHAT"
st.write("### Tabel History")

for i, row in df.iterrows():
    cols = st.columns([1, 1, 1.5, 1.5, 1])
    
    cols[0].write(row["Mata Uang"])
    cols[1].write(row["Nilai"])
    cols[2].write(f"{row['Kurs Jual']:,}")
    cols[3].write(f"{row['Kurs Beli']:,}")
    
    # Tombol "Lihat" grafik per baris
    if cols[4].button("📊 Lihat", key=f"lihat_{i}"):
        st.session_state["selected_currency"] = row["Mata Uang"]

st.write("---")

# TAMPILKAN GRAFIK SAAT TOMBOL DIKLIK
#if "selected_currency" in st.session_state:
    #currency = st.session_state["selected_currency"]
    #st.subheader(f"Grafik Kurs - {currency}")

    # contoh data grafik (random)
    #x = np.arange(10)
    #y = np.random.randint(9000, 20000, size=10)

    #fig, ax = plt.subplots()
    #ax.plot(x, y, marker="o", color="skyblue")
    #ax.set_title(f"Pergerakan Kurs {currency}")
    #ax.set_xlabel("Hari")
    #ax.set_ylabel("Nilai Kurs")
    #ax.grid(True)

    #st.pyplot(fig)
