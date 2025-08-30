import os
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

# --- KONFIGURASI AMBANG BATAS (THRESHOLD) ---
# Mengambil nilai dari file .env. Jika tidak ada, gunakan default "1.0".
ETH_THRESHOLD_STR = os.getenv("ETH_THRESHOLD", "1.0")
ETH_THRESHOLD = Decimal(ETH_THRESHOLD_STR)


# --- KONSTANTA APLIKASI ---
# Nilai konstan untuk konversi wei ke ETH.
WEI_IN_ETH = Decimal("1000000000000000000")


# --- KUNCI API & TOKEN ---
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")
BITQUERY_API_KEY = os.getenv("BITQUERY_API_KEY")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DATABASE_URL = os.getenv("DATABASE_URL")

if not MORALIS_API_KEY:
    print("PERINGATAN: MORALIS_API_KEY tidak ditemukan di file .env.")
if not BITQUERY_API_KEY:
    print("PERINGATAN: BITQUERY_API_KEY tidak ditemukan di file .env.")
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("PERINGATAN: Kredensial Telegram tidak ditemukan di file .env.")
if not DATABASE_URL:
    print("PERINGATAN: Kredensial Database tidak ditemukan di file .env.")
