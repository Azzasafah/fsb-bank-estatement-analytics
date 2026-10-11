# Proyek Transaksi e-Statement Bank FSB

Aplikasi dashboard analitik perbankan interaktif berbasis **Streamlit** dan **Plotly** untuk memantau arus kas, mutasi transaksi, audit saldo berjalan (*running balance*), dan visualisasi rekening koran digital (*e-Statement*) nasabah Bank FSB.

Proyek ini dibangun dari data mart hasil integrasi tabel transaksi dan master data (rekening, nasabah, cabang, kode transaksi, dan bank acquirer).

---

## Fitur Utama

1. **Ringkasan Eksekutif (Executive Overview)**
   - Metrik likuiditas: Total uang masuk (kredit), uang keluar (debit), dan surplus kas bersih (*net inflow*).
   - Analisis rasio penyerapan kas (*inflow absorption ratio*) dan pendapatan biaya admin (*fee-based income*).
   - Grafik tren harian perputaran kas dan proporsi jenis mutasi (*trasmode code*: SETOR, TARIK, INCOMING, OUTGOING, OVERBOOKING, INTER).
   - Distribusi perputaran dana per produk tabungan (Gold, Platinum, Silver, Karyawan) dan pangsa kanal layanan (*channel share*).

2. **Rekening Koran Digital (e-Statement Viewer)**
   - Pencarian dan pemilihan rekening nasabah berdasarkan nomor akun atau nama.
   - Kartu identitas nasabah: CIF, cabang pembuka, tipe produk, usia rekening (*account aging*), dan saldo akhir.
   - Grafik pelacakan saldo berjalan (*running balance track*) secara kronologis.
   - Tabel mutasi rekening formal dengan fitur unduh langsung ke file CSV.

3. **Jaringan Kliring Antarbank & Cabang**
   - Pemetaan 10 bank tujuan/acquirer terpopuler untuk transaksi transfer dan QRIS.
   - Identifikasi 10 kantor cabang dengan aktivitas transaksi tertinggi.
   - Profil demografi gender nasabah dan histogram sebaran usia rekening.

4. **Dokumentasi Pipeline Data Mart (Star Schema)**
   - Standarisasi data tanggal Julian (`YYYYDDD`) ke ISO-8601 dan penggabungan waktu transaksi menjadi `datetime`.
   - Pemisahan mutasi biaya administrasi (TRX092) ke atribut `additional_fee` pada transaksi induk guna mencegah duplikasi volume debit.
   - Algoritma identifikasi transaksi internal (*overbooking*) berbasis pengulangan nomor referensi.

---

## Struktur File Repositori

```text
├── .streamlit/
│   └── config.toml                  # Konfigurasi tema terang korporasi
├── app.py                           # Kode utama aplikasi Streamlit
├── fsb_estatement_transaction.csv   # Dataset data mart hasil transformasi (1.339 baris)
├── export_to_csv.py                 # Skrip ETL ekstraksi data dari spreadsheet
├── requirements.txt                 # Dependensi pustaka Python
├── .gitignore                       # Filter file repositori (hanya aset Streamlit)
└── README.md                        # Dokumentasi proyek
```

---

## Skema Data (`fsb_estatement_transaction.csv`)

Data mart ini memuat 1.339 baris transaksi dan 31 kolom yang telah melalui validasi:

| Kelompok Kolom | Nama Kolom Utama | Keterangan |
| :--- | :--- | :--- |
| **Transaksi** | `transaction_id`, `transaction_reference`, `transaction_datetime`, `channel` | Data waktu dan jalur transaksi |
| **Finansial** | `credit_amount`, `debit_amount`, `additional_fee`, `balance` | Nominal mutasi dan kalkulasi saldo berjalan |
| **Klasifikasi** | `transaction_code`, `transaction_desc`, `trasmode_code` | Kategori jenis transaksi perbankan |
| **Pihak Lawan** | `acquirer_bank_code`, `acquirer_bank_name`, `acquirer_account_number`, `acquirer_account_name` | Identitas bank dan rekening lawan transaksi |
| **Akun & Nasabah** | `account_number`, `cif_number`, `customer_name`, `product_name`, `branch_name`, `account_aging` | Relasi nasabah, produk, dan kantor cabang |

---

## Panduan Menjalankan Aplikasi Secara Lokal

### 1. Kloning Repositori
```bash
git clone https://github.com/<username>/<nama-repo>.git
cd <nama-repo>
```

### 2. Pasang Dependensi
Pastikan Python 3.9+ sudah terpasang, lalu jalankan:
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi Streamlit
```bash
streamlit run app.py
```

Setelah perintah dijalankan, dashboard akan terbuka otomatis di peramban pada alamat:
`http://localhost:8501`

---

## Teknologi yang Digunakan

- **Python**: Bahasa komputasi utama
- **Streamlit**: Kerangka kerja antarmuka web interaktif
- **Pandas & NumPy**: Pemrosesan dan manipulasi data tabular
- **Plotly**: Visualisasi grafik keuangan
- **Data Mart Modeling**: Desain skema bintang (*star schema*) perbankan
