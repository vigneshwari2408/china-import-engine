"""
China's Import Engine — Trade Risk Dashboard
Streamlit starter app · src/app.py

Run with: streamlit run src/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="China's Import Engine",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Data loading
# ─────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """
    Load trade data from CSV.
    Replace this with tableauhyperapi if reading from .hyper file.

    Expected columns:
        Year, HS, Description, Operation, Area, Region,
        FobValue, Tcosts, QtyKg, Transport
    """
    df = pd.read_csv(path, parse_dates=["Year"])
    df["LogisticsCostRatio"] = df["Tcosts"] / df["FobValue"].replace(0, np.nan)
    return df


@st.cache_data
def compute_mdr(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Maritime Dependency Ratio: sea FobValue / total FobValue."""
    imports = df[df["Operation"] == "import"]
    sea = imports[imports["Transport"] == "Sea"].groupby(group_col)["FobValue"].sum()
    total = imports.groupby(group_col)["FobValue"].sum()
    mdr = (sea / total).rename("MDR").reset_index()
    mdr["MDR_pct"] = (mdr["MDR"] * 100).round(1)
    return mdr


@st.cache_data
def compute_hhi(df: pd.DataFrame) -> pd.DataFrame:
    """HHI per HS category per year. HHI = Σ(share²) × 10,000"""
    imports = df[df["Operation"] == "import"]
    group = imports.groupby(["Year", "HS", "Area"])["FobValue"].sum().reset_index()
    totals = group.groupby(["Year", "HS"])["FobValue"].sum().rename("Total").reset_index()
    group = group.merge(totals, on=["Year", "HS"])
    group["share_sq"] = (group["FobValue"] / group["Total"]) ** 2
    hhi = group.groupby(["Year", "HS"])["share_sq"].sum().reset_index()
    hhi["HHI"] = (hhi["share_sq"] * 10_000).round(0)
    hhi["RiskLevel"] = hhi["HHI"].apply(
        lambda h: "High Risk" if h > 2500 else ("Moderate Risk" if h > 1500 else "Low Risk")
    )
    return hhi[["Year", "HS", "HHI", "RiskLevel"]]


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
st.sidebar.title("🚢 China Import Engine")
st.sidebar.markdown("**Trade Risk Dashboard** · 2016–2021")
st.sidebar.divider()

DATA_PATH = st.sidebar.text_input("CSV Data Path", value="data/china_imports.csv")

try:
    df = load_data(DATA_PATH)
    st.sidebar.success(f"✅ Loaded {len(df):,} rows")
except FileNotFoundError:
    st.sidebar.warning("⚠️ File not found — showing demo data")
    # ── Demo dataset ──────────────────────────
    rng = np.random.default_rng(42)
    hs_cats = {
        1: "Animal & Animal Products", 2: "Vegetable Products",
        3: "Foodstuffs",               4: "Mineral Products",
        5: "Chemicals",                6: "Plastics/Rubbers",
        8: "Wood & Wood Products",     9: "Textiles",
        12: "Metals",                  13: "Machinery/Electrical",
        14: "Transportation",          15: "Miscellaneous",
    }
    n = 8_000
    df = pd.DataFrame({
        "Year":      pd.to_datetime(rng.choice(range(2016, 2022), n).astype(str)),
        "HS":        rng.choice(list(hs_cats.keys()), n),
        "Operation": rng.choice(["import", "export"], n, p=[0.65, 0.35]),
        "Area":      rng.choice(["Russia", "USA", "Germany", "Brazil",
                                  "Australia", "India", "South Korea",
                                  "Japan", "France", "Saudi Arabia"], n),
        "Region":    rng.choice(["Asia", "Europe", "Americas", "Africa", "Oceania"], n),
        "FobValue":  rng.exponential(1e9, n),
        "Tcosts":    rng.exponential(5e7, n),
        "QtyKg":     rng.exponential(1e6, n),
        "Transport": rng.choice(["Sea", "Air", "Road", "Railway"], n,
                                 p=[0.70, 0.15, 0.10, 0.05]),
    })
    df["Description"] = df["HS"].map(hs_cats)
    df["LogisticsCostRatio"] = df["Tcosts"] / df["FobValue"]

st.sidebar.divider()
years = sorted(df["Year"].dt.year.unique())
y_min, y_max = st.sidebar.select_slider("Year Range", options=years,
                                         value=(min(years), max(years)))
df_f = df[df["Year"].dt.year.between(y_min, y_max)]

op = st.sidebar.radio("Operation", ["import", "export", "both"], index=0)
if op != "both":
    df_f = df_f[df_f["Operation"] == op]

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.title("🚢 China's Import Engine")
st.caption("Supply Chain Risk & Logistics Analysis · Source: UNCTAD")
st.divider()

# ─────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────
imp = df_f[df_f["Operation"] == "import"]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Import Value",   f"€{imp['FobValue'].sum()/1e12:.2f}T")
c2.metric("Total Logistics Cost", f"€{imp['Tcosts'].sum()/1e9:.1f}B")
sea_pct = imp[imp["Transport"] == "Sea"]["FobValue"].sum() / imp["FobValue"].sum()
c3.metric("Sea Transport Share",  f"{sea_pct*100:.1f}%")
c4.metric("Supplier Countries",   imp["Area"].nunique())
st.divider()

# ─────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📦 Top Imports",
    "🚛 Transport Modes",
    "🌊 Maritime Risk (MDR)",
    "📉 HHI Concentration",
    "💰 Logistics Efficiency",
])

hs_col = "Description" if "Description" in imp.columns else "HS"

# ── Top Imports ───────────────────────────────
with tab1:
    st.subheader("Top Import Commodities by FOB Value")
    top_hs = (imp.groupby(hs_col)["FobValue"].sum()
                 .sort_values(ascending=True).tail(15).reset_index())
    fig = px.bar(top_hs, x="FobValue", y=hs_col, orientation="h",
                 color="FobValue", color_continuous_scale="Blues",
                 template="plotly_dark",
                 labels={"FobValue": "FOB Value (€)", hs_col: ""})
    fig.update_layout(coloraxis_showscale=False, height=480)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Import Trend by Region")
    trend = (imp.groupby([imp["Year"].dt.year, "Region"])["FobValue"]
               .sum().reset_index().rename(columns={"Year": "Year"}))
    fig2 = px.line(trend, x="Year", y="FobValue", color="Region",
                   template="plotly_dark",
                   labels={"FobValue": "FOB Value (€)"})
    st.plotly_chart(fig2, use_container_width=True)

# ── Transport Modes ───────────────────────────
with tab2:
    st.subheader("Transport Cost by Mode")
    tc = (imp.groupby("Transport")["Tcosts"].sum().reset_index()
             .sort_values("Tcosts", ascending=False))
    colors = {"Sea": "#1f77b4", "Air": "#ff7f0e", "Road": "#2ca02c", "Railway": "#9467bd"}
    fig = px.bar(tc, x="Tcosts", y="Transport", orientation="h", color="Transport",
                 color_discrete_map=colors, template="plotly_dark",
                 labels={"Tcosts": "Total Cost (€)"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Products × Transport Heatmap")
    heat = (imp.groupby([hs_col, "Transport"])["FobValue"].sum().reset_index()
              .pivot(index=hs_col, columns="Transport", values="FobValue").fillna(0))
    fig2 = px.imshow(heat, color_continuous_scale="Blues", template="plotly_dark",
                     labels={"color": "FOB Value (€)"}, aspect="auto")
    st.plotly_chart(fig2, use_container_width=True)

# ── Maritime Risk ─────────────────────────────
with tab3:
    st.subheader("Maritime Dependency Ratio (MDR) by Product")
    st.caption("MDR = Sea FOB Value ÷ Total FOB Value. Higher = more exposed to disruption.")
    mdr_p = compute_mdr(df_f, hs_col).sort_values("MDR")
    fig = px.bar(mdr_p, x="MDR_pct", y=hs_col, orientation="h",
                 color="MDR_pct", color_continuous_scale="RdYlGn_r",
                 range_color=[0, 100], template="plotly_dark",
                 labels={"MDR_pct": "MDR (%)", hs_col: ""})
    fig.add_vline(x=50, line_dash="dash", line_color="orange")
    fig.update_layout(coloraxis_showscale=False, height=480)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Supplier Countries by Sea Risk")
    mdr_c = compute_mdr(df_f, "Area").sort_values("MDR", ascending=False).head(25)
    fig2 = px.bar(mdr_c, x="Area", y="MDR_pct",
                  color="MDR_pct", color_continuous_scale="RdYlGn_r",
                  range_color=[0, 100], template="plotly_dark",
                  labels={"MDR_pct": "MDR (%)"})
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

# ── HHI ──────────────────────────────────────
with tab4:
    st.subheader("Herfindahl-Hirschman Index — Supplier Concentration")
    st.markdown("**Low** < 1,500 &nbsp;|&nbsp; **Moderate** 1,500–2,500 &nbsp;|&nbsp; **High** > 2,500")
    hhi_df = compute_hhi(df_f)
    if hs_col == "Description":
        hs_map = df_f[["HS", "Description"]].drop_duplicates().set_index("HS")["Description"]
        hhi_df["Description"] = hhi_df["HS"].map(hs_map)
        c_col = "Description"
    else:
        c_col = "HS"

    fig = px.line(hhi_df, x="Year", y="HHI", color=c_col, template="plotly_dark")
    fig.add_hrect(y0=0,    y1=1500,  fillcolor="green",  opacity=0.04)
    fig.add_hrect(y0=1500, y1=2500,  fillcolor="orange", opacity=0.04)
    fig.add_hrect(y0=2500, y1=10000, fillcolor="red",    opacity=0.04)
    st.plotly_chart(fig, use_container_width=True)

    latest = hhi_df["Year"].max()
    snap = (hhi_df[hhi_df["Year"] == latest]
            .sort_values("HHI", ascending=False)[[c_col, "HHI", "RiskLevel"]])
    st.dataframe(snap, use_container_width=True, hide_index=True)

# ── Logistics Efficiency ──────────────────────
with tab5:
    st.subheader("Logistics Cost Ratio by Product & Mode")
    lcr = (imp.groupby([hs_col, "Transport"])
              .apply(lambda x: x["Tcosts"].sum() / x["FobValue"].sum())
              .reset_index(name="CostRatio"))

    fig = px.bar(lcr.sort_values("CostRatio", ascending=False).head(40),
                 x=hs_col, y="CostRatio", color="Transport", barmode="group",
                 template="plotly_dark",
                 color_discrete_map={"Sea":"#1f77b4","Air":"#ff7f0e",
                                     "Road":"#2ca02c","Railway":"#9467bd"},
                 labels={"CostRatio": "Cost Ratio", hs_col: ""})
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Potential Savings via Modal Shift")
    cheapest = (lcr.loc[lcr.groupby(hs_col)["CostRatio"].idxmin()]
                   .rename(columns={"Transport": "OptimalMode",
                                    "CostRatio":  "MinCostRatio"}))
    sav = lcr.merge(cheapest[[hs_col, "OptimalMode", "MinCostRatio"]], on=hs_col)
    sav["Saving_pct"] = ((sav["CostRatio"] - sav["MinCostRatio"])
                         / sav["CostRatio"] * 100).round(1)
    sav = (sav[sav["Transport"] != sav["OptimalMode"]]
              .sort_values("Saving_pct", ascending=False).head(15))
    fig2 = px.bar(sav, x=hs_col, y="Saving_pct", color="Transport",
                  barmode="group", template="plotly_dark",
                  labels={"Saving_pct": "Potential Saving (%)", hs_col: ""})
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.divider()
st.caption("China's Import Engine · UNCTAD Data · "
           "Vigneshwari Nalla · Ganesh Banoth · Abdullatief Kafilat · Balakireva Elizaveta")
