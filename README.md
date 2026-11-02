# 📊 Dashboard Penjualan Superstore

**Nama / NIM:** `ISI NAMA` / `ISI NIM`
**Mata Kuliah:** Visualisasi Data

## 🔗 Tautan
- **Live Dashboard:** `ISI URL STREAMLIT CLOUD`
- **Dataset Kaggle:** `ISI LINK KAGGLE` (Superstore Dataset, ±9.994 baris)

## Deskripsi
Dashboard interaktif untuk menganalisis performa penjualan toko ritel: tren waktu,
profitabilitas produk, pengaruh diskon, dan perbandingan wilayah.

**Fitur:** 5 KPI card · 6 chart (line, bar, donut, scatter, heatmap, bar top-state) ·
4 filter interaktif (tanggal, wilayah, kategori, segmen) · anotasi insight dinamis.

## 🔑 Key Insights
1. **Musiman:** penjualan melonjak tiap kuartal akhir (Sep-Des) dan puncaknya hampir selalu di November.
2. **Diskon menggerus profit:** transaksi dengan diskon >20% rata-rata merugi, sedangkan diskon kecil tetap untung.
3. **Sub-kategori:** Copiers dan Phones/Accessories menyumbang profit besar, sedangkan Tables dan Bookcases cenderung rugi.
4. **Wilayah:** West dan East paling profitable; Central punya margin terendah.
5. **Penjualan tinggi ≠ untung:** beberapa state dengan penjualan besar (mis. Texas) justru berprofit negatif.

> Verifikasi angka insight di atas dengan dashboard milikmu sebelum dikumpulkan.

## 📁 Struktur Repositori
```
├── app.py               # aplikasi dashboard
├── clean_data.py        # pra-pemrosesan data
├── requirements.txt
├── README.md
└── data/
    └── superstore_clean.csv   # data bersih
```

## ▶️ Menjalankan Secara Lokal
```bash
git clone <URL-REPO-KAMU>
cd <nama-repo>
pip install -r requirements.txt

# (opsional) bersihkan ulang data mentah dari Kaggle
python clean_data.py

streamlit run app.py
```

## 🚀 Deploy (Streamlit Community Cloud)
1. Push repo ke GitHub (status **Public**).
2. Buka share.streamlit.io, login dengan GitHub, klik **New app**.
3. Pilih repo, branch `main`, main file `app.py`, lalu **Deploy**.

## Sumber Data
Superstore Dataset, Kaggle: `ISI LINK KAGGLE`
