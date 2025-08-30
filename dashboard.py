import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.database import SessionLocal, Transaction
from datetime import datetime

# --- Konfigurasi Halaman & CSS ---
st.set_page_config(
    page_title="Shield.ai Dashboard", layout="wide", initial_sidebar_state="expanded"
)


# Suntikkan CSS Kustom untuk membuatnya terlihat mirip
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- Fungsi untuk mengambil data ---
@st.cache_data(ttl=60)  # Cache data selama 60 detik
def fetch_data():
    db = SessionLocal()
    try:
        transactions = (
            db.query(Transaction)
    .order_by(Transaction.timestamp.desc())
    .limit(500)
    .all()
        )

        if not transactions:
            return pd.DataFrame(), {}

        df = pd.DataFrame(
            [
                {
                    "timestamp": tx.timestamp,
                    "risk_score": tx.risk_score,
                    "value_eth": float(tx.value_eth),
                    "from_address": tx.from_address,
                    "to_address": tx.to_address,
                    "tx_hash": tx.tx_hash,
                }
                for tx in transactions
            ]
        )

        # Hitung statistik untuk KPI
        total_tx = len(df)
        high_risk_tx = len(df[df["risk_score"] > 70])
        medium_risk_tx = len(df[(df["risk_score"] > 30) & (df["risk_score"] <= 70)])
        low_risk_tx = len(df[df["risk_score"] <= 30])

        stats = {
            "total": total_tx,
            "high": high_risk_tx,
            "medium": medium_risk_tx,
            "low": low_risk_tx,
        }

        return df, stats
    finally:
        db.close()


# Panggil CSS
load_css()

# --- DATA ---
df, stats = fetch_data()

# # --- SIDEBAR ---
# with st.sidebar:
#     st.image(
#         "https://i.imgur.com/g0y6p2u.png", width=60
#     )  # Ganti dengan URL logo Anda jika ada
#     st.title("Shield.ai")
#     st.markdown("---")
#     # Tambahkan menu navigasi jika diperlukan di masa depan
# menu = st.sidebar.radio("Pilih Halaman:", ["Home", "Transaksi", "Laporan"])

# if menu == "Home":
#     st.header("🏠 Home")
#     st.write("Ini adalah halaman utama dashboard.")

# elif menu == "Transaksi":
#     st.header("💸 Transaksi")
#     st.write("Data transaksi ditampilkan di sini.")

# elif menu == "Laporan":
#     st.header("📊 Laporan")
#     st.write("Halaman laporan keuangan.")

# --- HEADER UTAMA ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Daftar Transaksi")
with col2:
    st.markdown(
        f"""
        <div style="text-align: right;">
            <p style="margin-bottom: -5px;">Hi!</p>
            <small>{datetime.now().strftime('%d %b %Y, %A')}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("---")

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1, 2])

# --- KOLOM KIRI (KPI & GRAFIK) ---
with col1:
    st.subheader("Ringkasan Risiko")

    # KPI Cards
    kpi1, kpi2 = st.columns(2)
    with kpi1:
        st.metric(label="Total Transaksi", value=stats.get("total", 0))
        st.metric(label="Risiko Sedang", value=stats.get("medium", 0))
    with kpi2:
        st.metric(label="Risiko Tinggi", value=stats.get("high", 0))
        st.metric(label="Risiko Rendah", value=stats.get("low", 0))

    st.markdown("---")
    st.subheader("Insight")

    # Gauge Chart
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=stats.get("total", 0),
            title={"text": "Total Alert Mencurigakan"},
            gauge={
                "axis": {
                    "range": [None, max(150, stats.get("total", 0) * 1.2)],
                    "tickwidth": 1,
                    "tickcolor": "darkblue",
                },
                "bar": {"color": "#7B68EE"},
                "steps": [
                    {"range": [0, 50], "color": "green"},
                    {"range": [50, 100], "color": "orange"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 120,
                },
            },
        )
    )
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

# --- KOLOM KANAN (DAFTAR TRANSAKSI) ---
with col2:
    st.subheader("Detail Transaksi Berisiko")

    # Filter dan Sorting
    sort_by = st.selectbox(
        "Urutkan Berdasarkan",
        ["Risiko Tinggi", "Risiko Rendah", "Terbaru"],
        label_visibility="collapsed",
    )

    if sort_by == "Risiko Rendah":
        df_display = df.sort_values("risk_score", ascending=True)
    elif sort_by == "Terbaru":
        df_display = df.sort_values("timestamp", ascending=False)
    else:  # Default Risiko Tinggi
        df_display = df.sort_values("risk_score", ascending=False)

    if df_display.empty:
        st.warning("Tidak ada transaksi untuk ditampilkan.")
    else:
        for index, row in df_display.head(10).iterrows():  # Tampilkan 10 teratas
            score = row["risk_score"]

            # Tentukan tag risiko
            if score > 70:
                tag = "🔺 Risiko Tinggi Terdeteksi"
                color = "red"
            elif score > 30:
                tag = "⚠️ Risiko Sedang"
                color = "orange"
            else:
                tag = "✅ Risiko Rendah"
                color = "green"

            st.markdown(
                f"""
                <div style="border: 1px solid #333; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: #1E1E2F;">
                    <table width="100%">
                        <tr>
                            <td style="width: 80px; text-align: center;">
                                <small>Skor Risiko</small>
                                <h2 style="color: {color}; margin: 0;">{int(score)}</h2>
                            </td>
                            <td style="padding-left: 15px;">
                                <b style="color:{color};">{tag}</b><br>
                                <small>
                                    <b>Jumlah:</b> {row['value_eth']:.6f} ETH<br>
                                    <b>Dari:</b> {row['from_address']}<br>
                                    <b>Ke:</b> {row['to_address']}
                                </small>
                            </td>
                            <td style="width: 150px; text-align: right;">
                                <a href="https://etherscan.io/tx/{row['tx_hash']}" target="_blank">
                                    <button style="background-color: #7B68EE; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer;">
                                        Lihat Di Etherscan
                                    </button>
                                </a>
                            </td>
                        </tr>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )
