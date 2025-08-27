from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
