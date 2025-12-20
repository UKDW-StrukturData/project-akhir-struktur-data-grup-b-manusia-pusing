import streamlit as st
import requests
import json
from datetime import datetime
import os
import uuid
import google.generativeai as genai

st.markdown("""
    <style>
        /* ================= GAYA BARU (Background & Glassmorphism) ================= */
        .stApp {
            /* Gradasi Ungu Gelap ke Hitam Pekat */
            background: radial-gradient(ellipse at center, #240b36 0%, #000000 100%);
            color: #e0f7fa;
            font-family: 'Segoe UI', Roboto, sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #875aff; /* Judul Neon Ungu */
            text-shadow: 0 0 8px rgba(135, 90, 255, 0.7);
        }
        
        /* Glassmorphism Card (Meniru Container Utama) */
        .st-emotion-cache-1cypcdb { /* Targetting main content container */
            background: rgba(46, 17, 71, 0.35); 
            border-radius: 20px;
            padding: 30px;
            margin-top: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(135, 90, 255, 0.2); 
        }
        
        /* --- STYLE BARU UNTUK SIDEBAR DAN NAVIGASI --- */
        
        /* Sidebar container utama (latar belakang) */
        .st-emotion-cache-16txto3 { /* Selector untuk sidebar container */
            background-color: rgba(13, 5, 20, 0.9) !important; /* Ungu sangat gelap, hampir hitam */
        }
        
        /* Gaya untuk item navigasi yang SEDANG DIPILIH (Active/Selected Page) */
        .st-emotion-cache-1ft9w09 { /* Selector untuk item navigasi yang terpilih */
            background-color: #5e35b1 !important; /* Ungu Solid untuk highlight */
            color: #ffffff !important;
            border-radius: 10px;
        }

        /* Gaya untuk teks di sidebar */
        .st-emotion-cache-1ft9w09 a, .st-emotion-cache-1ft9w09 div { 
            color: #ffffff !important; 
        }

        /* Gaya untuk teks item navigasi yang TIDAK DIPILIH (Default/Inactive) */
        .st-emotion-cache-1ft9w09 a:not(.st-emotion-cache-1ft9w09 a) {
            color: #b196ff !important;
        }
        
        /* --- END STYLE SIDEBAR --- */

        /* Custom styling untuk Dataframe (Tabel) - Glassmorphism */
        /* ... (CSS Dataframe lainnya tetap sama) ... */
    </style>
""", unsafe_allow_html=True)

a, b, c = st.columns(3)
with a:
    st.image("LogoNuevaMoneda.png", width=750)

def require_login_page():
    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("App.py")

require_login_page()

st.title("Fitur Penukaran Mata Uang")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSACTION_FILE = os.path.join(BASE_DIR, "transaction_history.json")
CURRENCY_FILE = os.path.join(BASE_DIR, "currency_names.json")

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

if not os.path.exists(TRANSACTION_FILE):
    with open(TRANSACTION_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

if os.path.exists(CURRENCY_FILE):
    with open(CURRENCY_FILE, "r", encoding="utf-8") as f:
        currency_names = json.load(f)
else:
    st.error("currency_names.json tidak ditemukan di folder utama")
    currency_names = {}

def format_currency(code):
    return f"{code} - {currency_names.get(code, code)}"

def fetch_exchange_rate():
    try:
        res = requests.get(API_URL, timeout=5)
        return res.json()["rates"]
    except:
        return {
            "USD": 1.0,
            "IDR": 16000.0,
            "EUR": 0.9,
            "JPY": 150.0
        }

def convert_currency(amount, source, target, rates):
    usd = amount / rates[source] if source != "USD" else amount
    return usd * rates[target]

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    pass

def gemini_get_profit():
    return 2.0  # persen tetap

# Hash Table dengan Arahan dari GPT
def generate_transaction_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = uuid.uuid4().hex[:6].upper()
    return f"TRX-{timestamp}-{rand}"

def save_transaction(data):
    with open(TRANSACTION_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

    trx_id = generate_transaction_id()
    history[trx_id] = data 

    with open(TRANSACTION_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

    return trx_id

rates = fetch_exchange_rate()

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
        st.error("Mata uang asal dan tujuan tidak boleh sama")
        st.stop()

    market = convert_currency(jumlah, asal, tujuan, rates)
    profit_rate = gemini_get_profit()
    hasil = market * (1 - profit_rate / 100)

    profit_idr = (market / rates[tujuan]) * (profit_rate / 100) * rates["IDR"]

    admin = st.session_state.get("username", "unknown")
    tanggal = datetime.now().strftime("%d-%m-%Y %H:%M")

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

    st.success(f"""
Transaksi berhasil disimpan ✅

ID Transaksi        : `{trx_id}`  

Mata Uang Asal      : `{jumlah:,.2f} {asal}` ({currency_names.get(asal, asal)})  

Mata Uang Tujuan    : `{hasil:,.2f} {tujuan}` ({currency_names.get(tujuan, tujuan)})  

Profit              : `Rp {profit_idr:,.2f}`  

Admin               : `{admin}`
""")
