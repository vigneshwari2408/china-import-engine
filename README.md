# 🚢 China's Import Engine: Trade Risk Analysis

Analyzing China's import dependencies and maritime supply chain risk across 2.4M+ trade records (2016–2021)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

---

## 📌 Project Overview

China is the world's largest exporter and second-largest importer, relying on global trade to power its industrial production, energy supply, and consumer demand. This project analyzes China's import patterns across product categories, supplier countries, and transportation modes to surface:

- Trade dependencies by commodity and region
- Supply chain vulnerabilities from maritime over-reliance
- Supplier concentration risk via the Herfindahl-Hirschman Index (HHI)

---

## 📊 Key Findings

| Insight | Finding |
|---|---|
| 🏆 Top Import Category | Machinery & Electrical Equipment |
| ⛽ Highest Sea Dependency | Mineral Products (~75%+ MDR) |
| 🌍 Highest Supplier Sea Risk | Russia, Middle East, Africa, South America |
| 📦 Most Concentrated Supply Chain | Electrical Machinery (High HHI > 2500) |
| 🚢 Dominant Transport Mode | Sea (by value and volume) |

Full write-up with methodology and recommendations: [FINDINGS.md](./FINDINGS.md)

Full case study deck: [ChinaCaseStudy.pdf](./ChinaCaseStudy.pdf)  
Interactive Tableau workbook: [ChinaCaseStudy.twbx](./ChinaCaseStudy.twbx)

---

## 🗂 Dataset

| Field | Description |
|---|---|
| Rows | 2,473,177 |
| Columns | 19 |
| Period | 2016 – 2021 |
| Source | [UNCTAD Trade Statistics](https://unctadstat.unctad.org/datacentre/dataviewer/US.TransportCosts) |

### Key Columns

| Column | Description |
|---|---|
| Year | Transaction year |
| HS / Description | Harmonized System commodity category (15 groups) |
| Operation | Import or Export |
| Area | Trade partner country (source for imports) |
| FobValue | Free on Board value in EUR |
| QtyKg | Weight of goods traded (kg) |
| Transport | Mode: Air, Sea, Road, Railway |

### Data Cleaning
- Converted Year to datetime
- Filtered to import records only for risk analysis
- Computed derived metrics: Maritime Dependency Ratio (MDR) and Herfindahl-Hirschman Index (HHI)

---

## 📐 Methodology

### Maritime Dependency Ratio (MDR)
Measures the proportion of imports transported by sea against total imports, used to identify which products and supplier countries carry the highest maritime supply chain risk.

MDR = (sum of FobValue where Transport = Sea) / (sum of total FobValue), computed by product and by country.

### Herfindahl-Hirschman Index (HHI)
Measures supplier market concentration per commodity, per year. A higher HHI means fewer dominant suppliers, which means greater disruption risk.

- Low Risk: HHI < 1500 (diversified supply)
- Moderate Risk: HHI 1500–2500
- High Risk: HHI > 2500 (concentrated, vulnerable)

### Combined Risk Matrix
Plotting MDR vs HHI for each product surfaces a 2D risk view — high-MDR, high-HHI products (sea-dependent AND few suppliers) are the most exposed.

---

## 🏗️ Project Structure
> ```
> china-import-engine/
> ├── mdr_hhi_analysis.ipynb   # Full analysis: load, clean, MDR, HHI, risk matrix, findings
> ├── FINDINGS.md              # Plain-English summary of results
> ├── requirements.txt
> └── README.md
> ```
>
---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip
- The UNCTAD trade dataset (see Dataset section above) — not included in this repo due to size; point the data-loading step at your local copy

### Run the analysis notebook

```bash
git clone https://github.com/vigneshwari2408/china-import-engine.git
cd china-import-engine
pip install -r requirements.txt
jupyter notebook mdr_hhi_analysis.ipynb
```

### Run the interactive dashboard

```bash
pip install streamlit plotly
streamlit run app.py
```

---

## 💡 Recommendations

1. Monitor high-risk categories. Mineral Products, Plastics/Rubbers, and Foodstuffs have the highest sea dependency.
2. Diversify supplier base. Reduce reliance on single-country sources for high-HHI subcategories.
3. Develop alternative transport routes. Encourage rail and multimodal options to reduce maritime over-dependence.
4. Strengthen maritime resilience. Invest in port infrastructure and logistics contingency planning.
5. Optimize modal shifts. Priority targets: Cereals from Argentina and Australia show the highest potential savings.

---

## 👥 Team

Built by: Vigneshwari Nalla · Ganesh Banoth · Abdullatief Kafilat · Balakireva Elizaveta

---

## 📚 References

- UNCTAD Trade Statistics: https://unctadstat.unctad.org/datacentre/dataviewer/US.TransportCosts
- Harmonized System (HS) Nomenclature, World Customs Organization

---

## About

**Vigneshwari Nalla** — MSc Data Analytics for Business, KEDGE Business School  
[LinkedIn](https://linkedin.com/in/vigna24) · [Portfolio](https://vigneshwari2408.github.io/vigneshwari-portfolio/)
