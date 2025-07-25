from fastapi import FastAPI, Request
import ujson
from decimal import Decimal
from config import ETH_THRESHOLD, WEI_IN_ETH
from app.services.bitquery_handler import get_address_info

app = FastAPI(title="Finance Alert MVP")

@app.get("/")
def read_root():
    """Endpoint utama untuk verifikasi bahwa server berjalan."""
    return {"status": "ok", "message": "Finance Alert Backend is running!"}

@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Endpoint untuk menerima webhook, memfilter transaksi, dan
    memperkaya (enrich) data alamat dengan Bitquery.
    """
    payload = await request.json()

    if not payload.get("txs"):
        return {"status": "ignored", "message": "No transactions in payload"}

    for tx in payload.get("txs", []):
        value_wei_str = tx.get("value")
        if not value_wei_str:
            continue

        try:
            value_wei = Decimal(value_wei_str)
            value_eth = value_wei / WEI_IN_ETH

            if value_eth >= ETH_THRESHOLD:
                print("\n" + "="*50)
                print("🚨 TRANSAKSI BESAR TERDETEKSI 🚨")
                print(f"  Hash: {tx.get('hash')}")
                print(f"  Nilai: {value_eth:.4f} ETH")
                print("-"*50)

                # --- INTEGRASI BITQUERY ---
                from_address = tx.get('fromAddress')
                to_address = tx.get('toAddress')

                # Get info untuk alamat pengirim
                print(f"🔍 Get data untuk alamat PENGIRIM...")
                from_info = get_address_info(from_address)
                if from_info:
                    print(f"  -> Alamat: {from_info.get('address')}")
                    print(f"  -> Tag: {from_info.get('tag', 'N/A')}")
                    print(f"  -> Total Transaksi: {from_info.get('transaction_count', 0)}")
                else:
                    print(f"  -> Gagal mendapatkan info untuk {from_address}")
                
                print("-"*50)

                # Get info untuk alamat penerima
                print(f"🔍 Get data untuk alamat PENERIMA...")
                to_info = get_address_info(to_address)
                if to_info:
                    print(f"  -> Alamat: {to_info.get('address')}")
                    print(f"  -> Tag: {to_info.get('tag', 'N/A')}")
                    print(f"  -> Total Transaksi: {to_info.get('transaction_count', 0)}")
                else:
                    print(f"  -> Gagal mendapatkan info untuk {to_address}")

                print("="*50 + "\n")
                
        except Exception as e:
            print(f"Error memproses transaksi {tx.get('hash')}: {e}")
            continue
            
    return {"status": "success", "message": "Webhook processed"}