# 📊 Dashboard Penjualan Superstore

**Nama / NIM:** `Stefhanus Christopher Hasiholan Simarmata` / `241051014`
**Mata Kuliah:** Visualisasi Data

## 🔗 Tautan
- **Live Dashboard:** `https://dashboard-superstore-uts.streamlit.app/`
- **Dataset Kaggle:** `https://www.kaggle.com/datasets/vivek468/superstore-dataset-final` (Superstore Dataset, ±9.994 baris)

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
git clone https://github.com/XDFaint/dashboard-superstore.git
cd dashboard-superstore

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

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
Superstore Dataset, Kaggle: `https://www.kaggle.com/datasets/vivek468/superstore-dataset-final`
