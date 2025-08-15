from sqlalchemy.orm import Session
from . import database, schemas
from datetime import datetime

def create_transaction(db: Session, tx: schemas.TransactionCreate):
    db_transaction = database.Transaction(**tx.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_labeled_address(db: Session, address: str):
    """Mencari alamat di tabel labeled_addresses."""
    return db.query(database.LabeledAddress).filter(database.LabeledAddress.address == address).first()

def create_or_update_labeled_address(db: Session, address: str, label: str, source: str):
    """Membuat label baru atau memperbarui yang sudah ada."""
    db_address = get_labeled_address(db, address)
    if db_address:
        # db_address.label = label 
        pass
    else:
        db_address = database.LabeledAddress(address=address, label=label, source=source)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
    return db_address

def update_transaction_risk_score(db: Session, tx_id: int, risk_score: float):
    """Memperbarui transaksi dengan skor risikonya."""
    db_tx = db.query(database.Transaction).filter(database.Transaction.id == tx_id).first()
    if db_tx:
        db_tx.risk_score = risk_score
        db.commit()
        db.refresh(db_tx)
    return db_tx