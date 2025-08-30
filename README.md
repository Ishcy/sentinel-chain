# Sentinel Chain 🚀

**Sentinel Chain** adalah sistem intelijen keuangan yang dirancang untuk Lomba BI-OJK Hackathon 2025. Proyek ini bertujuan untuk mendeteksi potensi aliran dana ilegal secara *real-time* dengan memantau dan menganalisis transaksi di berbagai jaringan blockchain.

## 📖 Tentang Proyek

Sistem ini berfungsi sebagai "penjaga" yang mengawasi transaksi keuangan di dunia digital. Dengan memanfaatkan transparansi blockchain dan API modern, *Sentinel Chain* dapat mengidentifikasi aktivitas mencurigakan, memberikan skor risiko, dan mengirimkan notifikasi instan. Ini adalah sebuah alat *Supervisory Technology* (SupTech) yang dapat membantu regulator seperti Bank Indonesia dan OJK dalam menjalankan fungsi pengawasan di era ekonomi digital.

## ✨ Fitur Utama

  * **Pemantauan Real-Time**: Menerima data transaksi blockchain secara instan menggunakan teknologi *webhook*.
  * **Skoring Risiko Rule-Based**: Setiap transaksi dianalisis menggunakan serangkaian aturan untuk menghitung skor risiko kuantitatif.
  * **Pengayaan Data (Enrichment)**: Memperkaya data transaksi dengan informasi historis dari alamat yang terlibat.
  * **Notifikasi Instan**: Mengirimkan peringatan ke channel Telegram untuk transaksi yang teridentifikasi berisiko tinggi.
  * **Dashboard Visual**: Menampilkan daftar transaksi mencurigakan dan detailnya melalui antarmuka web yang interaktif.

## Diagram Arsitektur Sistem

Sistem ini dirancang dengan arsitektur berbasis *microservice* yang modular, memisahkan antara proses penerimaan data, analisis, dan presentasi. 

<img src="https://drive.google.com/uc?export=view&id=1LhuWS6zqqkRzsPwqhZeMrt1QoxetkhFt"/>

## 🛠️ Tumpukan Teknologi

  * **Backend API**: **FastAPI** - Untuk performa tinggi dalam menerima webhook dan menyajikan data.
  * **Dashboard**: **Streamlit** - Untuk pembuatan dashboard data interaktif yang cepat dan mudah.
  * **Database**: **SQLite** - Untuk kesederhanaan dan kecepatan setup selama hackathon.
  * **Ingestion Data**: **Moralis Streams** (via Webhook).
  * **Enrichment Data**: **Bitquery GraphQL API**.
  * **Notifikasi**: **Telegram Bot API**.
  * **Runtime**: **Python 3.9+**.

## ⚙️ Instalasi & Konfigurasi

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di lingkungan lokal Anda.

### 1\. Klona Repository

```bash
git clone https://github.com/Ishcy/sentinel-chain.git
cd sentinel-chain
```

### 2\. Buat Virtual Environment

```bash
# Untuk Windows
python -m venv venv
venv\Scripts\activate

# Untuk macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3\. Instal Dependensi

```bash
pip install -r requirements.txt
```

### 4\. Konfigurasi Environment Variables

Salin file `.env.example` menjadi `.env` dan isi dengan kredensial API Anda.

```bash
cp .env.example .env
```

Isi file `.env` dengan nilai yang sesuai:

```env
# Ganti dengan API key atau token Anda
MORALIS_API_KEY="YOUR_MORALIS_API_KEY"
BITQUERY_API_KEY="YOUR_BITQUERY_API_KEY"
TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"

# Nama file database SQLite
DATABASE_URL="YOUR_DATABASE_URL"
```

## ▶️ Cara Menjalankan

Proyek ini terdiri dari dua komponen utama yang perlu dijalankan secara terpisah: **Backend FastAPI** dan **Dashboard Streamlit**.

### 1\. Jalankan Backend FastAPI

Backend ini bertugas menerima webhook dari Moralis dan memproses data.

```bash
uvicorn app.main:app --reload
```

Server akan berjalan di `http://127.0.0.1:8000`.

### 2\. Ekspos Webhook ke Internet (Penting\!)

Layanan seperti Moralis perlu mengirim data ke URL publik. Gunakan `ngrok` untuk mengekspos server lokal Anda.

```bash
ngrok http 8000
```

Anda akan mendapatkan URL publik seperti `https://abcdef123456.ngrok.io`. Gunakan URL ini (`https://abcdef123456.ngrok.io/webhook/moralis`) saat mendaftarkan webhook di Moralis.

### 3\. Jalankan Dashboard Streamlit

Buka terminal baru, aktifkan *virtual environment*, dan jalankan perintah berikut.

```bash
streamlit run dashboard.py
```

Dashboard akan tersedia di `http://localhost:8501`.

## 🔮 Rencana Pengembangan

  * **Model Machine Learning**: Mengganti *rule-based engine* dengan model deteksi anomali (misal: Isolation Forest, Autoencoder) untuk menangkap pola yang lebih kompleks.
  * **Integrasi Data Tradisional**: Menambahkan sumber data dari API Open Banking untuk analisis lintas platform yang sesungguhnya.
  * **Visualisasi Jaringan**: Membangun grafik interaktif untuk memvisualisasikan aliran dana antar alamat.
  * **Skalabilitas**: Migrasi dari SQLite ke PostgreSQL dan menyiapkan sistem untuk *deployment* di cloud.
  * **Dashboard Plan Design**:

<img src="https://drive.google.com/uc?export=view&id=1eAADgR1Lw2FBIA-c98xYuZapIHcW8nwS"/>

-----

## 👥 Tim Pengembang

| Nama | Peran | Kontak |
| :--- | :--- | :--- |
| **M Ikmal Ramdan** | Project Lead, Backend Dev | [Github](https://github.com/Ishcy/) |
| **Anisatul Husna**| Research & Proposal Associate | [LinkedIn/Github] |
| **Amanda Aprilia**| UI/UX | [LinkedIn](https://www.linkedin.com/in/amanda-aprilia?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app) |
