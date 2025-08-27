from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Konfigurasi Database
DATABASE_URL = "sqlite:///./finance_alert.db" 

engine = create_engine(
    DATABASE_URL, connect_args={
        "check_same_thread": False,
        "timeout": 15
        }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model Tabel 'transactions'
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    tx_hash = Column(String, unique=True, index=True, nullable=False)
    from_address = Column(String, index=True, nullable=False)
    to_address = Column(String, index=True, nullable=False)
    value_eth = Column(Numeric(18, 8), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    risk_score = Column(Float, default=0.0)

# Model Tabel 'labeled_addresses'
class LabeledAddress(Base):
    __tablename__ = "labeled_addresses"

    address = Column(String, primary_key=True, index=True)
    label = Column(String, nullable=False)
    source = Column(String) 
    risk_score = Column(Float, default=0.0)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)