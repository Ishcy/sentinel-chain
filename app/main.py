from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
from . import crud, schemas, database
from . import crud, schemas, database, analyzer

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
    payload = await request.json()

    # Ekstrak data transaksi dari payload Moralis
    for tx_data in payload.get("txs", []):
        try:
            unix_timestamp = int(payload.get("block", {}).get("timestamp"))
            readable_timestamp = datetime.fromtimestamp(unix_timestamp)

            transaction_schema = schemas.TransactionCreate(
                tx_hash=tx_data.get("hash"),
                from_address=tx_data.get("fromAddress"),
                to_address=tx_data.get("toAddress"),
                value_eth=Decimal(tx_data.get("value")) / 10**18,
                timestamp=readable_timestamp
            )
            
            db_transaction = crud.create_transaction(db=db, tx=transaction_schema)
            print(f"✅ Transaksi {db_transaction.tx_hash[:10]}... berhasil disimpan.")

            analyzer.analyze_transaction(db=db, tx=db_transaction)
            
        except Exception as e:
            print(f"❌ Gagal memproses atau menganalisis transaksi: {e}")
            continue
            
    return {"status": "success", "message": "Webhook processed, saved, and analyzed"}