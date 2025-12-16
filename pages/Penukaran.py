import streamlit as st
import requests
import json
from datetime import datetime
import google.generativeai as genai
import os
import uuid

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f1c2c, #0d0d0d);
    color: #e0f7fa;
}
h1, h2, h3, h4 {
    color: #00bcd4;
}
.stButton>button {
    width: 100%;
    background: #00bcd4;
    color: #0f1c2c;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

a, b, c = st.columns(3)
with a:
    st.image("LogoNuevaMoneda.png", width=750)

# LOGIN GUARD
def require_login_page():
    if not st.session_state.get("logged_in"):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("LoginPages.py")

require_login_page()

st.title("Fitur Penukaran Mata Uang")

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

currency_file = "currency_names.json"

if os.path.exists(currency_file):
    with open(currency_file, "r", encoding="utf-8") as f:
        currency_names = json.load(f)
else:
    currency_names = {
        "USD": "United States Dollar",
        "IDR": "Indonesian Rupiah",
        "EUR": "Euro",
        "JPY": "Japanese Yen"
    }

def format_currency(code):
    return f"{code} - {currency_names.get(code, 'Unknown')}"

def fetch_exchange_rate():
    try:
        res = requests.get(API_URL)
        raw = res.json()
        return raw
    except:
        return {
            "rates": {"USD": 1.0, "IDR": 16000.0, "EUR": 0.9, "JPY": 150.0}
        }

def convert_currency(amount, source, target, rates):
    usd = amount / rates[source] if source != "USD" else amount
    return usd * rates[target]

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = "DUMMY_KEY"

genai.configure(api_key=GEMINI_API_KEY)

def gemini_get_profit():
    return 2.0  

def generate_transaction_id():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    rand = uuid.uuid4().hex[:6].upper()
    return f"TRX-{timestamp}-{rand}"

def save_transaction(data):
    file_path = "transaction_history.json"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
                if not isinstance(history, dict):
                    history = {}
            except:
                history = {}
    else:
        history = {}

    trx_id = generate_transaction_id()
    history[trx_id] = data

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

    return trx_id

data = fetch_exchange_rate()
rates = data["rates"]

jumlah = st.number_input("Nominal:", min_value=1.0)

asal = st.selectbox(
    "Mata Uang Asal:",
    sorted(rates.keys()),
    format_func=format_currency
)

tujuan = st.selectbox(
    "Mata Uang Tujuan:",
    sorted(rates.keys()),
    format_func=format_currency
)

if st.button("Konversi"):
    if asal == tujuan:
        st.error("Mata uang tidak boleh sama")
        st.stop()

    market = convert_currency(jumlah, asal, tujuan, rates)
    profit_rate = gemini_get_profit()
    hasil = market * (1 - profit_rate / 100)

    profit_idr = (market / rates[tujuan]) * (profit_rate / 100) * rates["IDR"]

    admin = st.session_state.get("username", "unknown")
    tanggal = datetime.now().strftime("%d-%m-%Y")

    transaksi = {
        "tanggal": tanggal,
        "admin": admin,
        "asal": asal,
        "tujuan": tujuan,
        "jumlah_awal": jumlah,
        "hasil_akhir": hasil,
        "profit_idr": profit_idr,
        "profit_rate_percent": profit_rate
    }

    trx_id = save_transaction(transaksi)

    st.success(
    f"""
Transaksi berhasil disimpan ✅

ID Transaksi        : `{trx_id}`  

Mata Uang Asal      : `{jumlah:,.2f} {asal}` ({currency_names.get(asal)})  

Mata Uang Tujuan    : H`{hasil:,.2f} {tujuan}` ({currency_names.get(tujuan)})  

Profit              : `Rp {profit_idr:,.2f}`  

Admin               : `{admin}`
"""
)