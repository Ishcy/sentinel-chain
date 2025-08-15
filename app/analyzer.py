from sqlalchemy.orm import Session
from . import crud
from .services import bitquery_handler

def analyze_transaction(db: Session, tx: crud.database.Transaction):
    """
    Fungsi utama untuk menganalisis sebuah transaksi yang sudah disimpan.
    """
    print(f"🔬 Menganalisis transaksi: {tx.tx_hash[:10]}...")
    risk_score = 0.0

    # --- Cek Nilai Transaksi ---
    if tx.value_eth > 1000: # Ambang batas nilai besar (misal 1000 ETH)
        risk_score += 20
        print(f"  [+] Aturan Nilai: Transaksi > 1000 ETH. Skor +20. Total: {risk_score}")

    # --- Analisis Alamat Pengirim (from_address) ---
    from_address_info = analyze_address(db, tx.from_address)
    if from_address_info.get("is_new_wallet"):
        risk_score += 10
        print(f"  [+] Aturan Pengirim: Alamat baru (< 5 tx). Skor +10. Total: {risk_score}")
    
    # --- Analisis Alamat Penerima (to_address) ---
    to_address_info = analyze_address(db, tx.to_address)
    if to_address_info.get("label") == "Known Scammer: Fcoin":
        risk_score += 50
        print(f"  [+] Aturan Penerima: Dikirim ke alamat scammer. Skor +50. Total: {risk_score}")
    elif "Exchange" in (to_address_info.get("label") or "") or "Binance" in (to_address_info.get("label") or ""):
        risk_score -= 5 
        print(f"  [-] Aturan Penerima: Dikirim ke bursa. Skor -5. Total: {risk_score}")

    # --- Finalisasi ---
    final_score = max(0, risk_score)
    crud.update_transaction_risk_score(db, tx_id=tx.id, risk_score=final_score)
    print(f"✅ Analisis selesai. Skor akhir: {final_score}")


def analyze_address(db: Session, address: str) -> dict:
    """
    Menganalisis sebuah alamat, baik dari DB lokal maupun Bitquery.
    """
    #Cek DB Lokal
    labeled_address = crud.get_labeled_address(db, address)
    if labeled_address:
        print(f"  [*] Info Alamat (Lokal): {address[:10]}... ditemukan, Label: {labeled_address.label}")
        return {"label": labeled_address.label, "is_new_wallet": False}
    
    #Jika tidak ada, panggil Bitquery
    print(f"  [*] Info Alamat (Bitquery): {address[:10]}... tidak ditemukan di lokal. Memanggil Bitquery...")
    bitquery_info = bitquery_handler.get_address_info(address)
    
    if not bitquery_info:
        return {}

    #Simpan label baru dari Bitquery jika ada
    if bitquery_info.get("tag") and bitquery_info["tag"] != "N/A":
        crud.create_or_update_labeled_address(
            db, 
            address=address, 
            label=bitquery_info["tag"], 
            source="bitquery"
        )
        print(f"  [*] Label baru '{bitquery_info['tag']}' disimpan untuk {address[:10]}...")

    #Terapkan aturan berdasarkan data Bitquery
    is_new = (bitquery_info.get("transaction_count", 10) < 5)
    
    return {
        "label": bitquery_info.get("tag"),
        "is_new_wallet": is_new
    }