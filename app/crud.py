from sqlalchemy.orm import Session
from . import database, schemas
from datetime import datetime

def create_transaction(db: Session, tx: schemas.TransactionCreate):
    """
    Membuat dan menyimpan record transaksi baru ke dalam database.
    """
    # Buat objek model SQLAlchemy dari data Pydantic
    db_transaction = database.Transaction(
        tx_hash=tx.tx_hash,
        from_address=tx.from_address,
        to_address=tx.to_address,
        value_eth=tx.value_eth,
        timestamp=tx.timestamp
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction