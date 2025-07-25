from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
from . import crud, schemas, database

app = FastAPI(title="Finance Alert MVP")

@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """Endpoint utama untuk verifikasi bahwa server berjalan."""
    return {"status": "ok", "message": "Finance Alert Backend is running!"}

@app.post("/webhook")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint untuk menerima webhook, memvalidasi data, dan menyimpannya ke DB.
    """
    payload = await request.json()

    # Ekstrak data transaksi dari payload Moralis
    for tx_data in payload.get("txs", []):
        try:
            raw_timestamp = payload.get("block", {}).get("timestamp")
            parsed_timestamp = datetime.fromtimestamp(int(raw_timestamp))
            transaction_to_save = schemas.TransactionCreate(
                tx_hash=tx_data.get("hash"),
                from_address=tx_data.get("fromAddress"),
                to_address=tx_data.get("toAddress"),
                value_eth=Decimal(tx_data.get("value")) / 10**18,
                timestamp=parsed_timestamp
            )

            # Panggil fungsi CRUD untuk menyimpan transaksi ke database
            crud.create_transaction(db=db, tx=transaction_to_save)
            
            # Cetak konfirmasi ke konsol server
            print(f"✅ Transaksi {transaction_to_save.tx_hash[:10]}... berhasil disimpan ke DB.")

        except Exception as e:
            print(f"❌ Gagal memproses atau menyimpan transaksi: {e}")
            continue
   
    return {"status": "success", "message": "Webhook processed and data saved"}