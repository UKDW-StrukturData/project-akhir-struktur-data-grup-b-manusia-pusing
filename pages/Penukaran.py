import streamlit as st
import requests
import json
from datetime import datetime
import google.generativeai as genai

# LOGIN GUARD dibantu oleh GPT
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
    if source == target:
        return amount

    usd_amount = amount / rates[source] if source != "USD" else amount

    return usd_amount * rates[target]

# pembuatan fungsi profit dibantu oleh GPT & ASDOS
GEMINI_API_KEY = "AIzaSyD-1_unReCLUvxQ9DM5of8-m-sygFRxsQI"
genai.configure(api_key=GEMINI_API_KEY)

def gemini_get_profit(rates, amount, source, target):
    prompt = f"""
Kamu adalah analis money changer profesional.
Tentukan persentase profit TERBAIK untuk transaksi berikut:

Jumlah: {amount}
Dari mata uang: {source}
Ke mata uang: {target}
Rates lengkap: {json.dumps(rates)}
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    try:
        return float(response.text.strip())
    except:
        return 2.0


data = fetch_exchange_rate()

if data:
    rates = data["rates"]

    st.subheader("Hitung Konversi Mata Uang")

    jumlah = st.number_input("Masukkan nominal:", min_value=1.0)
    asal = st.selectbox("Mata uang asal:", sorted(rates.keys()))
    tujuan = st.selectbox("Mata uang tujuan:", sorted(rates.keys()))

    if st.button("Konversi Sekarang"):
        market_result = convert_currency(jumlah, asal, tujuan, rates)
        # ambil profit dari Gemini dibantu oleh GPT dan ASDOS
        profit_rate = gemini_get_profit(rates, jumlah, asal, tujuan)
        hasil_final = market_result * (1 - (profit_rate / 100))

        profit_value_usd = market_result * (profit_rate / 100)
        profit_value_idr = profit_value_usd * rates["IDR"]
        admin = st.session_state.get("username", "Tidak diketahui")
        tanggal = datetime.now().strftime("%d-%m-%Y")

        st.success(
        f"""
        **Nilai Uang Awal  :** {jumlah:,.2f} {asal}

        **Hasil Konversi     :** {hasil_final:,.2f} {tujuan}

        **Profit Penukaran :** Rp {profit_value_idr:,.2f}

        **Tanggal               :** {tanggal}

        **Admin                 :** {admin}
        """
        )

else:
    st.error("Tidak dapat memuat nilai tukar.")
