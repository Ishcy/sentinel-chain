import telegram
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

async def send_telegram_alert(message: str):
    """
    Mengirim pesan notifikasi ke chat ID yang ditentukan via Bot Telegram.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Gagal mengirim notifikasi: Token atau Chat ID Telegram tidak disetel.")
        return

    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode='Markdown' # Menggunakan Markdown untuk formatting
        )
        print("✅ Notifikasi Telegram berhasil terkirim.")
    except Exception as e:
        print(f"❌ Gagal mengirim notifikasi Telegram: {e}")

def format_alert_message(tx, from_info, to_info, risk_score) -> str:
    """
    Memformat pesan notifikasi agar informatif dan mudah dibaca.
    """
    from_label = from_info.get('label', 'N/A')
    to_label = to_info.get('label', 'N/A')

    etherscan_link = f"https://etherscan.io/tx/{tx.tx_hash}"

    message = (
        f"🚨 *TRANSAKSI BERISIKO TINGGI TERDETEKSI* 🚨\n\n"
        f"💰 *Nilai:* {tx.value_eth:.4f} ETH\n\n"
        f"📤 *Dari:* `{tx.from_address}`\n"
        f"   - *Label:* {from_label}\n\n"
        f"📥 *Ke:* `{tx.to_address}`\n"
        f"   - *Label:* {to_label}\n\n"
        f"📈 *Skor Risiko:* *{risk_score:.0f}/100*\n\n"
        f"🔗 *Hash Transaksi:*\n[Lihat di Etherscan]({etherscan_link})"
    )
    return message