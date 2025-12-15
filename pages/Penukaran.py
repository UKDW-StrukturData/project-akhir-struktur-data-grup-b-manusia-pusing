import streamlit as st
import requests
import json
from datetime import datetime
import google.generativeai as genai
import os

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f1c2c, #0d0d0d);
            color: #e0f7fa;
        }
        h1, h2, h3, h4 {
            color: #00bcd4; /* Judul Neon */
            text-shadow: 0 0 5px rgba(0, 188, 212, 0.5);
        }
        .stTextInput>div>div>input, .stSelectbox>div>div>div>div>div, .stNumberInput>div>div>input {
            background-color: rgba(30, 40, 50, 0.7);
            border: 1px solid #00bcd4;
            color: #e0f7fa;
            border-radius: 8px;
            padding: 10px;
        }
        .stButton>button {
            width: 100%;
            background: #00bcd4;
            color: #0f1c2c;
            font-weight: bold;
            border-radius: 10px;
            margin-top: 20px;
            transition: all 0.3s;
            border: none;
            box-shadow: 0 0 5px #00bcd4, 0 0 15px #00bcd4;
        }
        .stButton>button:hover {
            background: #00e5ff;
            box-shadow: 0 0 10px #00e5ff, 0 0 25px #00e5ff;
        }
        /* Glassmorphism/Card untuk Hasil Konversi */
        .stSuccess, .stInfo {
            background: rgba(0, 188, 212, 0.1); /* Warna Cyan Transparan */
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(0, 188, 212, 0.5);
            color: #e0f7fa; /* Teks putih */
            font-family: 'Consolas', monospace; /* Font teknikal */
        }
    </style>
""", unsafe_allow_html=True)

a,b,c = st.columns(3)
    
with a:
    st.image("LogoNuevaMoneda.png", width=750 )

# LOGIN GUARD
def require_login():
    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("LoginPages.py")

require_login()

st.title("Fitur Penukaran Mata Uang")

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# FETCH EXCHANGE RATE
def fetch_exchange_rate():
    try:
        res = requests.get(API_URL)
        if res.status_code != 200:
            return None 
        raw = res.json()
        
        save_data = {
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "base": raw.get("base"),
            "date": raw.get("date"),
            "rates": raw.get("rates")
        }
        with open("exchange_rate_data.json", "w", encoding="utf-8") as outfile:
            json.dump(save_data, outfile, indent=4, ensure_ascii=False)

        return raw

    except Exception as err:
        try:
            with open("exchange_rate_data.json", "r", encoding="utf-8") as infile:
                return json.load(infile)
        except Exception:
            return {"rates": {"USD": 1.0, "IDR": 16000.0, "EUR": 0.9, "JPY": 150.0}, "base": "USD", "date": "2025-01-01"}

# CONVERT CURRENCY
def convert_currency(amount, source, target, rates):
    if source == target:
        return amount
    usd_amount = amount / rates[source] if source != "USD" else amount
    return usd_amount * rates[target]

# CONFIG GEMINI AI DIBANTU GPT 
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "DUMMY_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def gemini_get_profit(rates, amount, source, target):
    if GEMINI_API_KEY == "DUMMY_KEY":
        return 2.0 
        
    prompt = f"""
Kamu adalah analis money changer profesional.
Tentukan persentase profit yang wajar antara 0.1% sampai 5%.
Cukup jawab dengan satu angka persen saja.
"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        profit = float(response.text.strip())
    except:
        profit = 2.0

    if profit < 0.1:
        profit = 0.1
    if profit > 5:
        profit = 5

    return profit

# SAVE TRANSACTION DIBANTU OLEH GPT
def save_transaction(data):
    file_path = "transaction_history.json"

    if not os.path.exists(file_path):
        history = []
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []

    history.append(data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
# ...

# LOAD NAMA MATA UANG DIBANTU OLEH GPT
currency_file = "currency_names.json"

if os.path.exists(currency_file):
    with open(currency_file, "r", encoding="utf-8") as f:
        currency_names = json.load(f)
else:
    currency_names = {"USD": "United States Dollar", "IDR": "Indonesian Rupiah", "EUR": "Euro", "JPY": "Japanese Yen"}

def format_currency(x):
    return f"{x} - {currency_names.get(x, 'Unknown')}"

data = fetch_exchange_rate()

if data and "rates" in data:
    rates = data["rates"]

    st.subheader("Hitung Konversi Mata Uang")
    
    with st.container():
        st.markdown('<div style="background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1);">', unsafe_allow_html=True)
        jumlah = st.number_input("Masukkan nominal:", min_value=1.0)
        asal = st.selectbox(
            "Mata uang asal:",
            sorted(rates.keys()),
            format_func=format_currency
        )
        tujuan = st.selectbox(
            "Mata uang tujuan:",
            sorted(rates.keys()),
            format_func=format_currency
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Konversi Sekarang"):

        if asal == tujuan:
            st.error("Mata uang asal dan tujuan TIDAK BOLEH sama.")
            st.stop()

        market_result = convert_currency(jumlah, asal, tujuan, rates)
        profit_rate = gemini_get_profit(rates, jumlah, asal, tujuan)
        hasil_final = market_result * (1 - (profit_rate / 100))

        market_result_usd = (
            market_result / rates[tujuan]
            if tujuan != "USD"
            else market_result
        )
        
        profit_value_usd = market_result_usd * (profit_rate / 100)
        profit_value_idr = profit_value_usd * rates["IDR"]

        admin = st.session_state.get("username", "Tidak diketahui")
        tanggal = datetime.now().strftime("%d-%m-%Y")

        # Menggunakan format kustom untuk hasil yang lebih futuristik
        st.success(
            f"""
**Nilai Uang Awal  ** : `{jumlah:,.2f} {asal}` ({currency_names.get(asal, 'Unknown')})

**Hasil Konversi     ** : `{hasil_final:,.2f} {tujuan}` ({currency_names.get(tujuan, 'Unknown')})

**Profit Penukaran ** : `Rp {profit_value_idr:,.2f}`

**Tgl/Waktu            ** : `{tanggal}`

**Admin ID             ** : `{admin}`
"""
        )

        transaksi = {
            "tanggal": tanggal,
            "admin": admin,
            "asal": asal,
            "tujuan": tujuan,
            "jumlah_awal": jumlah,
            "hasil_akhir": hasil_final,
            "profit_idr": profit_value_idr,
            "profit_rate_percent": profit_rate
        }

        save_transaction(transaksi)

        st.info("Log Transaksi berhasil disimpan ke Database.")

else:
    st.error("Tidak dapat memuat nilai tukar. Cek koneksi API atau pastikan file 'exchange_rate_data.json' tersedia.")