from fastapi import FastAPI, Request
import ujson
from decimal import Decimal

from config import ETH_THRESHOLD, WEI_IN_ETH

app = FastAPI(title="Finance Alert MVP")

@app.get("/")
def read_root():
    """Endpoint utama untuk verifikasi bahwa server berjalan."""
    return {"status": "ok", "message": "Finance Alert Backend is running!"}

@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Endpoint untuk menerima webhook dari Moralis Streams.
    Logika filter menggunakan variabel dari config.py.
    """
    payload = await request.json()

    if not payload.get("txs"):
        print("Webhook diterima tanpa data transaksi. Diabaikan.")
        return {"status": "ignored", "message": "No transactions in payload"}

    for tx in payload.get("txs", []):
        value_wei_str = tx.get("value")
        if not value_wei_str:
            continue

        try:
            value_wei = Decimal(value_wei_str)
            value_eth = value_wei / WEI_IN_ETH

            # Logika filter utama
            if value_eth >= ETH_THRESHOLD:
                print("====== 🚨 TRANSAKSI BESAR TERDETEKSI 🚨 ======")
                print(f"  Hash: {tx.get('hash')}")
                print(f"  Dari: {tx.get('fromAddress')}")
                print(f"  Ke: {tx.get('toAddress')}")
                print(f"  Nilai: {value_eth:.4f} ETH (Ambang batas: {ETH_THRESHOLD} ETH)")
                print("==============================================")
                
        except Exception as e:
            print(f"Error memproses transaksi {tx.get('hash')}: {e}")
            continue
            
    return {"status": "success", "message": "Webhook processed"}