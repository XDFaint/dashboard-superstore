"""Dashboard Penjualan Superstore - Streamlit + Plotly"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------------ konfigurasi
st.set_page_config(page_title="Superstore Sales Dashboard",
                   page_icon="📊", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "superstore_clean.csv"

# Palet warna konsisten di seluruh dashboard
BLUE, ORANGE, GREEN, RED = "#1F4E79", "#F28E2B", "#2A9D8F", "#D1495B"
SEQ = [BLUE, ORANGE, GREEN]

st.markdown(f"""
<style>
.block-container {{padding-top: 1.5rem;}}
.kpi {{background:#fff;border-left:6px solid {BLUE};border-radius:8px;
      padding:14px 18px;box-shadow:0 1px 4px rgba(0,0,0,.12);}}
.kpi .label {{font-size:.85rem;color:#6b7280;}}
.kpi .value {{font-size:1.8rem;font-weight:700;color:{BLUE};}}
.insight {{background:#EEF4FA;border-radius:8px;padding:10px 14px;
          font-size:.92rem;color:#1b2a3a;margin-top:-6px;}}
</style>
""", unsafe_allow_html=True)


def usd(x: float) -> str:
    return f"${x:,.0f}"


def kpi(col, label, value):
    col.markdown(f'<div class="kpi"><div class="label">{label}</div>'
                 f'<div class="value">{value}</div></div>',
                 unsafe_allow_html=True)


def insight(text: str):
    st.markdown(f'<div class="insight">💡 {text}</div>', unsafe_allow_html=True)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, parse_dates=["order_date", "ship_date"])


if not DATA_PATH.exists():
    st.error("File data/superstore_clean.csv belum ada. Jalankan `python clean_data.py` dulu.")
    st.stop()

data = load_data()

# ------------------------------------------------------------------ sidebar: filter
st.sidebar.header("🔎 Filter Data")
dmin, dmax = data["order_date"].min().date(), data["order_date"].max().date()
rng = st.sidebar.date_input("Rentang tanggal order", (dmin, dmax),
                            min_value=dmin, max_value=dmax)
regions = st.sidebar.multiselect("Wilayah (Region)",
                                 sorted(data["region"].unique()),
                                 default=sorted(data["region"].unique()))
cats = st.sidebar.multiselect("Kategori Produk",
                              sorted(data["category"].unique()),
                              default=sorted(data["category"].unique()))
segs = st.sidebar.multiselect("Segmen Pelanggan",
                              sorted(data["segment"].unique()),
                              default=sorted(data["segment"].unique()))

start, end = (rng[0], rng[1]) if isinstance(rng, (tuple, list)) and len(rng) == 2 else (dmin, dmax)
df = data[
    data["order_date"].between(pd.Timestamp(start), pd.Timestamp(end))
    & data["region"].isin(regions)
    & data["category"].isin(cats)
    & data["segment"].isin(segs)
]

# ------------------------------------------------------------------ header
st.title("📊 Dashboard Penjualan Superstore")
st.caption("Sumber data: Kaggle - Superstore Dataset | Gunakan filter di sidebar untuk eksplorasi.")

if df.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini. Ubah filter di sidebar.")
    st.stop()

# ------------------------------------------------------------------ KPI cards
total_sales, total_profit = df["sales"].sum(), df["profit"].sum()
margin = total_profit / total_sales * 100
orders = df["order_id"].nunique()
avg_disc = df["discount"].mean() * 100

c1, c2, c3, c4, c5 = st.columns(5)
kpi(c1, "Total Penjualan", usd(total_sales))
kpi(c2, "Total Profit", usd(total_profit))
kpi(c3, "Margin Profit", f"{margin:.1f}%")
kpi(c4, "Jumlah Order", f"{orders:,}")
kpi(c5, "Rata-rata Diskon", f"{avg_disc:.1f}%")
st.write("")

# ------------------------------------------------------------------ 1. Line chart
st.subheader("Tren Penjualan & Profit Bulanan")
monthly = (df.groupby(pd.Grouper(key="order_date", freq="MS"))[["sales", "profit"]]
             .sum().reset_index())
fig = px.line(monthly, x="order_date", y=["sales", "profit"], markers=True,
              color_discrete_map={"sales": BLUE, "profit": ORANGE},
              labels={"order_date": "Bulan", "value": "USD", "variable": ""})
fig.for_each_trace(lambda t: t.update(name={"sales": "Penjualan", "profit": "Profit"}[t.name]))
peak = monthly.loc[monthly["sales"].idxmax()]
fig.add_annotation(x=peak["order_date"], y=peak["sales"], showarrow=True, arrowhead=2,
                   text=f"Puncak: {usd(peak['sales'])}")
fig.update_layout(legend=dict(orientation="h", y=1.1), margin=dict(t=30, b=10))
st.plotly_chart(fig, use_container_width=True)
insight(f"Penjualan tertinggi terjadi pada **{peak['order_date']:%B %Y}**. "
        "Pola musiman terlihat: penjualan melonjak di akhir tahun (Sep-Des).")

# ------------------------------------------------------------------ 2. Bar + 3. Donut
left, right = st.columns([3, 2])
with left:
    st.subheader("Profit per Sub-Kategori")
    sub = (df.groupby("sub_category", as_index=False)["profit"].sum().sort_values("profit"))
    sub["Status"] = sub["profit"].apply(lambda v: "Untung" if v >= 0 else "Rugi")
    fig = px.bar(sub, x="profit", y="sub_category", orientation="h", color="Status",
                 color_discrete_map={"Untung": GREEN, "Rugi": RED},
                 labels={"profit": "Profit (USD)", "sub_category": ""})
    fig.update_layout(margin=dict(t=10, b=10), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)
    best, worst = sub.iloc[-1], sub.iloc[0]
    insight(f"**{best['sub_category']}** paling menguntungkan ({usd(best['profit'])}), "
            f"sedangkan **{worst['sub_category']}** paling lemah ({usd(worst['profit'])}).")

with right:
    st.subheader("Proporsi Penjualan per Segmen")
    seg = df.groupby("segment", as_index=False)["sales"].sum()
    fig = px.pie(seg, names="segment", values="sales", hole=0.5,
                 color_discrete_sequence=SEQ)
    fig.update_layout(margin=dict(t=10, b=10), legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig, use_container_width=True)
    top = seg.loc[seg["sales"].idxmax()]
    insight(f"Segmen **{top['segment']}** menyumbang {top['sales']/seg['sales'].sum()*100:.0f}% penjualan.")

# ------------------------------------------------------------------ 4. Scatter + 5. Heatmap
left, right = st.columns(2)
with left:
    st.subheader("Diskon vs Profit")
    sample = df.sample(min(len(df), 3000), random_state=42)
    fig = px.scatter(sample, x="discount", y="profit", color="category", opacity=0.6,
                     color_discrete_sequence=SEQ,
                     labels={"discount": "Diskon", "profit": "Profit (USD)", "category": "Kategori"})
    fig.update_xaxes(tickformat=".0%")
    fig.update_layout(margin=dict(t=10, b=10), legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)
    hi = df.loc[df["discount"] > 0.2, "profit"].mean()
    lo = df.loc[df["discount"] <= 0.2, "profit"].mean()
    insight(f"Transaksi diskon >20% rata-rata profit **{usd(hi) if pd.notna(hi) else '-'}**, "
            f"vs **{usd(lo) if pd.notna(lo) else '-'}** untuk diskon ≤20%. Diskon besar menggerus profit.")

with right:
    st.subheader("Heatmap Profit: Wilayah × Kategori")
    pv = df.pivot_table(index="region", columns="category", values="profit", aggfunc="sum")
    fig = px.imshow(pv, text_auto=".0f", aspect="auto", color_continuous_scale="RdYlGn",
                    color_continuous_midpoint=0,
                    labels={"color": "Profit", "x": "Kategori", "y": "Wilayah"})
    fig.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
    reg = df.groupby("region")["profit"].sum()
    insight(f"Wilayah **{reg.idxmax()}** paling profitable ({usd(reg.max())}); "
            f"**{reg.idxmin()}** terendah ({usd(reg.min())}).")

# ------------------------------------------------------------------ 6. Top 10 state
st.subheader("10 State dengan Penjualan Tertinggi")
top_state = (df.groupby("state", as_index=False)[["sales", "profit"]].sum()
               .nlargest(10, "sales").sort_values("sales"))
fig = px.bar(top_state, x="sales", y="state", orientation="h", color="profit",
             color_continuous_scale="RdYlGn", color_continuous_midpoint=0,
             labels={"sales": "Penjualan (USD)", "state": "", "profit": "Profit"})
fig.update_layout(margin=dict(t=10, b=10))
st.plotly_chart(fig, use_container_width=True)
insight("Warna batang menunjukkan profit: state dengan penjualan tinggi belum tentu menguntungkan.")

with st.expander("📄 Lihat data (setelah filter)"):
    st.dataframe(df, use_container_width=True)
