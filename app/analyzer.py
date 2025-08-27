import asyncio
from sqlalchemy.orm import Session
from . import crud
from .services import bitquery_handler, telegram_bot


async def analyze_transaction(db: Session, tx: crud.database.Transaction):
    """
    Fungsi utama untuk menganalisis sebuah transaksi yang sudah disimpan.
    Sekarang menjadi async untuk menangani notifikasi.
    """
    print(f"🔬 Menganalisis transaksi: {tx.tx_hash[:10]}...")
    risk_score = 0.0

    if tx.value_eth > 1000:
        risk_score += 20
    from_address_info = analyze_address(db, tx.from_address)
    to_address_info = analyze_address(db, tx.to_address)
    if "Scammer" in (to_address_info.get("label") or ""):
        risk_score += 50
    if from_address_info.get("is_new_wallet"):
        risk_score += 10

    final_score = max(0, risk_score)
    crud.update_transaction_risk_score(db, tx_id=tx.id, risk_score=final_score)
    print(f"✅ Analisis selesai. Skor akhir: {final_score}")

    # --- LOGIKA NOTIFIKASI ---
    if final_score > 50:  # Ambang batas notifikasi
        print("   -> Skor risiko tinggi terdeteksi. Menyiapkan notifikasi...")
        message = telegram_bot.format_alert_message(
            tx, from_address_info, to_address_info, final_score
        )
        await telegram_bot.send_telegram_alert(message)


def analyze_address(db: Session, address: str) -> dict:
    # ... (logika analyze_address Anda) ...
    labeled_address = crud.get_labeled_address(db, address)
    if labeled_address:
        return {"label": labeled_address.label, "is_new_wallet": False}
    bitquery_info = bitquery_handler.get_address_info(address)
    if not bitquery_info:
        return {}
    if bitquery_info.get("tag") and bitquery_info["tag"] != "N/A":
        crud.create_or_update_labeled_address(
            db, address=address, label=bitquery_info["tag"], source="bitquery"
        )
        print(
            f"  [*] Label baru '{bitquery_info['tag']}' disimpan untuk {address[:10]}..."
        )
    tx_count = bitquery_info.get("transaction_count", 10)
    is_new = int(tx_count) < 5

    return {"label": bitquery_info.get("tag"), "is_new_wallet": is_new}
