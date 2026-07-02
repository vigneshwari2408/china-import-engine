# 🚢 China's Import Engine: Trade Risk Dashboard

> Analyzing China's import dependencies, maritime supply chain risk, and logistics efficiency across 2.4M+ trade records (2016–2021)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Tableau](https://img.shields.io/badge/Tableau-E97627?style=flat-square&logo=tableau&logoColor=white)](https://public.tableau.com)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

---

## 📌 Project Overview

China is the world's largest exporter and second-largest importer, relying on global trade to power its industrial production, energy supply, and consumer demand. This project analyzes **China's import patterns** across product categories, supplier countries, and transportation modes to surface:

- **Trade dependencies** by commodity and region
- **Supply chain vulnerabilities** from maritime over-reliance
- **Logistics inefficiencies** and potential cost savings
- **Supplier concentration risk** via the Herfindahl-Hirschman Index (HHI)

> 🔗 **[View Tableau Dashboard →](#)** &nbsp;|&nbsp; 📄 **[Read Case Study →](./ChinaCaseStudy.pdf)**

---

## 📊 Key Findings

| Insight | Finding |
|---|---|
| 🏆 Top Import Category | Machinery & Electrical Equipment |
| ⛽ Highest Sea Dependency | Mineral Products (~75%+ MDR) |
| 🌍 Highest Supplier Sea Risk | Russia, Middle East, Africa, South America |
| 📦 Most Concentrated Supply Chain | Electrical Machinery (High HHI > 2500) |
| 💸 Largest Potential Savings | Cereals & Aircraft Parts via modal shift |
| 🚢 Dominant Transport Mode | Sea (by value and volume) |

---

## 🗂️ Dataset

| Field | Description |
|---|---|
| **Rows** | 2,473,177 |
| **Columns** | 19 |
| **Period** | 2016 – 2021 |
| **Source** | [UNCTAD Trade Statistics](https://unctadstat.unctad.org/datacentre/dataviewer/US.TransportCosts) |

### Key Columns

| Column | Description |
|---|---|
| `Year` | Transaction year |
| `HS` | Harmonized System commodity category (15 groups) |
| `Operation` | Import or Export |
| `Area` | Trade partner country (source for imports) |
| `FobValue` | Free on Board value in EUR |
| `Tcosts` | Total transportation/logistics cost |
| `QtyKg` | Weight of goods traded (kg) |
| `Transport` | Mode: Air, Sea, Road, Railway |

### Data Cleaning Steps

- Converted `Year` to datetime
- Mapped `Area` to geographical region (Africa, Americas, Asia, Europe, Oceania)
- Computed derived metrics: **MDR** (Maritime Dependency Ratio) and **Logistics Cost Ratio**

---

## 📐 Methodology

### Maritime Dependency Ratio (MDR)
Measures the proportion of imports transported by sea against total imports, used to identify which products and supplier countries carry the highest maritime supply chain risk.

```
MDR_Product  = SUM(FobValue if Transport = 'Sea') / SUM(FobValue)
MDR_Country  = SUM(FobValue if Transport = 'Sea') / SUM(FobValue)  [by Area]
```

### Herfindahl-Hirschman Index (HHI)
Measures supplier market concentration per commodity. A higher HHI means fewer dominant suppliers, which means greater disruption risk.

```
Low Risk:      HHI < 1500  (diversified supply)
Moderate Risk: HHI 1500–2500
High Risk:     HHI > 2500  (concentrated, vulnerable)
```

### Transport Efficiency & Potential Savings
Identifies product-country combinations currently using suboptimal transport modes, calculating the cost delta against the cheapest viable alternative.

---

## 🏗️ Project Structure

```
china-import-engine/
│
├── data/
│   ├── ChinaImportEngine_CaseStudy.hyper   # Tableau data source
│   └── README.md                           # Data documentation
│
├── tableau/
│   └── ChinaCaseStudy.twbx                 # Tableau packaged workbook
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_mdr_analysis.ipynb
│   ├── 03_hhi_concentration.ipynb
│   └── 04_logistics_efficiency.ipynb
│
├── src/
│   ├── app.py                              # Streamlit dashboard
│   ├── metrics.py                          # MDR, HHI, savings calculations
│   └── viz.py                              # Plotly chart components
│
├── ChinaCaseStudy.pdf                      # Project presentation
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/vigneshwari2408/china-import-engine.git
cd china-import-engine

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit dashboard
streamlit run src/app.py
```

---

## 📈 Dashboard Tabs

| Tab | Analysis |
|---|---|
| **Top Imports** | Commodity rankings by FOB value, regional breakdown, import trends 2016–2021 |
| **Transport Modes** | Cost by mode (Sea/Air/Road/Railway), product vs. transport matrix |
| **Policy Analysis** | Maritime Dependency Ratio by product & country, interactive world map |
| **HHI Risk** | Supplier concentration over time, subcategory drill-down |
| **Logistics Efficiency** | Cost ratio heatmap, potential savings by country–product pair |

---

## 💡 Recommendations

1. **Monitor high-risk categories.** Mineral Products, Plastics/Rubbers, and Foodstuffs have the highest sea dependency.
2. **Diversify supplier base.** Reduce reliance on single-country sources for high-HHI subcategories.
3. **Develop alternative transport routes.** Encourage rail and multimodal options to reduce maritime over-dependence.
4. **Strengthen maritime resilience.** Invest in port infrastructure and logistics contingency planning.
5. **Optimize modal shifts.** Priority targets: Cereals from Argentina and Australia show the highest potential savings.

---

## 👥 Team

Built by: Vigneshwari Nalla · Ganesh Banoth · Abdullatief Kafilat · Balakireva Elizaveta

---

## 📚 References

- UNCTAD Trade Statistics: https://unctadstat.unctad.org/datacentre/dataviewer/US.TransportCosts
- Harmonized System (HS) Nomenclature, World Customs Organization
