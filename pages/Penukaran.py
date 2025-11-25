import streamlit as st
import requests
import json
from datetime import datetime



def require_login():
    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("LoginPages.py")

require_login()

st.title("Fitur Penukaran Mata Uang")



API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

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



def convert_currency(amount, source, target, rates):

    if source == "USD":
        usd_value = amount
    else:
        usd_value = amount / rates[source]

    if target == "USD":
        return usd_value
    else:
        return usd_value * rates[target]


# -------------------------------------------------- #
#  ANALISIS PROFIT (Gemini AI) DIBANTU OLEH GPT
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
#  USER INTERFACE DIBANTU OLEH GPT
# ------------------------------------------------------ #

data = fetch_exchange_rate()

if data:
    rates = data["rates"]

    st.subheader("Hitung Konversi Mata Uang")

    jumlah = st.number_input("Masukkan nominal:", min_value=1.0)
    asal = st.selectbox("Mata uang asal:", sorted(rates.keys()))
    tujuan = st.selectbox("Mata uang tujuan:", sorted(rates.keys()))

    if st.button("Konversi Sekarang"):
        hasil = convert_currency(jumlah, asal, tujuan, rates)

        if asal == "IDR":
            idr_awal = jumlah
        else:
            usd_value = jumlah / rates[asal]
            idr_awal = usd_value * rates["IDR"]

        if tujuan == "IDR":
            idr_akhir = hasil
        else:
            usd_value = hasil / rates[tujuan]
            idr_akhir = usd_value * rates["IDR"]

        selisih = idr_akhir - idr_awal

        admin = st.session_state.get("username", "Tidak diketahui")
        tanggal = datetime.now().strftime("%d-%m-%Y")

        st.success(
        f"""
        **Nilai Awal (IDR):** Rp {idr_awal:,.2f}

        **Hasil Konversi:** {hasil:,.2f} {tujuan}

        **Selisih / Profit:** Rp {selisih:,.2f}

        **Tanggal:** {tanggal}

        **Admin:** {admin}
        """
        )

    st.subheader("Analisis Profit Otomatis (Gemini)")

    if st.button("Jalankan Analisis AI"):
        st.info(gemini_profit_analysis(jumlah, rates))

else:
    st.error("Tidak dapat memuat nilai tukar.")
