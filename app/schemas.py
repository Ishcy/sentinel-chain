from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class TransactionBase(BaseModel):
    tx_hash: str
    from_address: str
    to_address: str
    value_eth: Decimal
    timestamp: datetime

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True # Memungkinkan model membaca data dari objek ORM (SQLAlchemy)