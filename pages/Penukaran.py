import streamlit as st
import requests
import json
from datetime import datetime
import google.generativeai as genai


# ==========================
# LOGIN PROTECTION
# ==========================
def require_login():
    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("LoginPages.py")

require_login()

st.title("Fitur Penukaran Mata Uang")
st.caption("Halaman ini masih dalam tahap pengembangan.")



API_URL = "https://api.exchangerate-api.com/v4/latest/USD"


# ==========================
# AMBIL DATA KURS
# ==========================
def fetch_exchange_rate():
    try:
        res = requests.get(API_URL)
        if res.status_code != 200:
            st.error("Tidak dapat menghubungi API nilai tukar.")
            return None
        raw = res.json()

        save_data = {
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "base": raw.get("base"),
            "date": raw.get("date"),
            "rates": raw.get("rates")
        }

        with open("exchange_rate_data.json", "w") as outfile:
            json.dump(save_data, outfile, indent=4)

        return raw

    except Exception as err:
        st.error(f"Terjadi error saat mengambil data: {err}")
        return None


# ----------------------------------------- #
#  KONVERSI MATA UANG DIBANTU OLEH CHAT GPT
# ----------------------------------------- #

def convert_currency(amount, source, target, rates):


    # ubah ke IDR
    if source == "IDR":
        idr_base = amount
    else:
        idr_base = amount / rates[source]

    # jika tujuan langsung IDR
    if target == "IDR":
        return idr_base

    # ubah ke mata uang tujuan
    return idr_base * rates[target]


# -------------------------------------------------- #
#  ANALISIS PROFIT (Gemini AI) DIBANTU OLEH CHAT GPT
# -------------------------------------------------- #

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

def gemini_profit_analysis(amount, rates):
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)

        prompt = (
            f"Jumlah uang: {amount}\n"
            f"Nilai tukar: {json.dumps(rates)}"
        )

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text

    except Exception as err:
        return f"Tidak dapat terhubung ke Gemini: {err}"


# ------------------------------------------------------ #
#  USER INTERFACE – PENUKARAN UANG DIBANTU OLEH CHAT GPT
# ------------------------------------------------------ #

data = fetch_exchange_rate()

if data:
    rates = data["rates"]

    st.subheader("Hitung Konversi Mata Uang")

    jumlah = st.number_input("Masukkan nominal:", min_value=1.0)
    asal = st.selectbox("Mata uang asal:", sorted(rates.keys()))
    tujuan = st.selectbox("Mata uang tujuan:", sorted(rates.keys()))

    # Opsi Kurs Beli / Kurs Jual
    jenis_transaksi = st.selectbox(
        "Jenis Transaksi",
        ["Kurs Jual (Admin menjual valas)", "Kurs Beli (Admin membeli valas)"]
    )

    if st.button("Konversi Sekarang"):

        # hasil market (tanpa profit)
        market_result = convert_currency(jumlah, asal, tujuan, rates)

        # cari nilai rupiah awal
        idr_awal = jumlah if asal == "IDR" else jumlah / rates[asal]

        # cari nilai rupiah akhir
        idr_akhir = hasil if tujuan == "IDR" else hasil / rates[tujuan]

        selisih = idr_akhir - idr_awal

        # ambil username dari session login
        admin = st.session_state.get("username", "Tidak diketahui")
        tanggal = datetime.now().strftime("%d-%m-%Y")

        # ===============================
        # FORMAT OUTPUT
        # ===============================
        st.success(
        f"""
        **Nilai Uang Awal  :** {jumlah:,.2f} {asal}

        **Hasil Konversi     :** {hasil_final:,.2f} {tujuan}

        **Profit Penukaran :** Rp {profit_value_idr:,.2f}

        **Tanggal               :** {tanggal}

        **Admin:** {admin}
        """
        )


    st.subheader("Analisis Profit Otomatis (Gemini)")

    if st.button("Jalankan Analisis AI"):
        st.info(gemini_profit_analysis(jumlah, rates))

else:
    st.error("Tidak dapat memuat nilai tukar.")
