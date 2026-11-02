"""Pra-pemrosesan data Superstore (Kaggle) -> data/superstore_clean.csv

Jalankan:  python clean_data.py
Input   :  data/Sample - Superstore.csv  (unduh dari Kaggle)
Output  :  data/superstore_clean.csv
"""
from pathlib import Path
import pandas as pd

RAW = Path("data/Sample - Superstore.csv")
OUT = Path("data/superstore_clean.csv")

df = pd.read_csv(RAW, encoding="latin-1")
print(f"Baris awal: {len(df):,}")

# 1. Standarisasi nama kolom: "Sub-Category" -> "sub_category"
df.columns = (
    df.columns.str.strip().str.lower()
    .str.replace(r"[\s\-]+", "_", regex=True)
)

# 2. Hapus duplikat dan baris kosong pada kolom kunci
df = df.drop_duplicates()
key_cols = ["order_id", "order_date", "ship_date", "segment", "region",
            "category", "sub_category", "sales", "quantity", "discount", "profit"]
df = df.dropna(subset=key_cols)

# 3. Tipe data
for c in ["order_date", "ship_date"]:
    df[c] = pd.to_datetime(df[c], errors="coerce")
df = df.dropna(subset=["order_date", "ship_date"])
for c in ["sales", "discount", "profit"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").astype(int)

# 4. Rapikan teks
for c in ["ship_mode", "segment", "country", "city", "state",
          "region", "category", "sub_category"]:
    df[c] = df[c].astype(str).str.strip()

# 5. Fitur turunan
df["year"] = df["order_date"].dt.year
df["delivery_days"] = (df["ship_date"] - df["order_date"]).dt.days

# 6. Validasi: tanggal kirim tidak boleh sebelum tanggal order
df = df[df["delivery_days"] >= 0]

df = df.dropna().reset_index(drop=True)
df.to_csv(OUT, index=False)
print(f"Baris bersih: {len(df):,} -> {OUT}")
