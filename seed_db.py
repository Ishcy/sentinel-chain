from app.database import SessionLocal, LabeledAddress

def seed_database():
    db = SessionLocal()
    try:
        # Cek apakah data sudah ada untuk menghindari duplikasi
        existing_count = db.query(LabeledAddress).count()
        if existing_count > 0:
            print("Database sudah berisi data. Seeding dibatalkan.")
            return

        known_addresses = [
            LabeledAddress(
                address="0x8894e0a0c962cb723c1976a4421c95949be2d4e3", 
                label="Binance 8", 
                source="manual",
                risk_score=0.1
            ),
            LabeledAddress(
                address="0x742d35cc6634c0532925a3b844bc454e4438f44e", 
                label="Kraken 4", 
                source="manual",
                risk_score=0.1
            ),
            LabeledAddress(
                address="0xb5d4f343412ea6b6c8273757f5fa7d60a24a6e4f", 
                label="KuCoin", 
                source="manual",
                risk_score=0.1
            ),
            LabeledAddress(
                address="0x73bceb1cd57c711feac4224d062b0f6ff338501e", 
                label="Known Scammer: Fcoin", 
                source="manual",
                risk_score=0.9
            ),
        ]

        db.add_all(known_addresses)
        db.commit()
        print(f"{len(known_addresses)} alamat berhasil ditambahkan ke database.")
    
    except Exception as e:
        print(f"Terjadi error saat seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Memulai proses seeding database...")
    seed_database()