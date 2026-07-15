# 📋 Key Findings — China's Import Engine

> Plain-English summary of the trade risk analysis. Full details and code in [mdr_hhi_analysis.ipynb](./mdr_hhi_analysis.ipynb).

---

## What We Analyzed

China's import patterns across **2.4 million trade records** (2016–2021), covering 15 commodity categories, 180+ supplier countries, and 4 transport modes (Sea, Air, Road, Railway). We focused on two risk dimensions:

- **Maritime Dependency** — how exposed each product/supplier is to sea route disruptions
- **Supplier Concentration** — how fragile the supply chain is if one country stops exporting

---

## Finding 1 — Sea Dominates, Creating Systemic Fragility

Sea transport accounts for **~70% of China's import value**. This means any disruption to global shipping lanes — a Suez Canal blockage, South China Sea conflict, or port strike — cascades across nearly every product category.

Air, road, and railway combined handle less than 30%, mostly for high-value or time-sensitive goods.

---

## Finding 2 — Mineral Products Face the Highest Maritime Risk

Using the **Maritime Dependency Ratio (MDR)**, we found that **Mineral Products** (including oil, gas, and coal) have the highest sea dependency at **~75%+**. Plastics/Rubbers, Foodstuffs, Wood & Wood Products, and Vegetable Products follow closely.

These are not luxury goods — they are industrial and energy inputs that keep China's economy running. A disruption here has second-order effects across manufacturing and agriculture.

---

## Finding 3 — Russia, Middle East & Africa Are the Riskiest Supplier Regions

At the country level, **Russia, Middle Eastern energy exporters, African resource suppliers, and South American commodity exporters** show the highest maritime dependency ratios.

This means China's exposure isn't just about *what* it imports — it's about *where* those goods come from and how they travel.

---

## Finding 4 — Electrical Machinery Has a Dangerously Concentrated Supplier Base

The **Herfindahl-Hirschman Index (HHI)** reveals that **Electrical Machinery & Electronics** imports are heavily concentrated among a small number of supplier countries (HHI > 2,500 = High Risk).

This was made painfully clear during COVID-19, when semiconductor shortages from a handful of countries caused global production halts. The HHI data shows this structural vulnerability existed before the pandemic and has persisted since.

---

## Finding 5 — The Risk Is Structural, Not Cyclical

MDR values remained **consistently high across all six years** (2016–2021). This is not a temporary imbalance — it reflects deep structural dependencies baked into China's trade routes and supplier relationships. Policy intervention requires long-term, systemic change, not short-term fixes.

---

## The Most Dangerous Products (High MDR + High HHI)

Products that combine **high maritime dependency AND concentrated supplier bases** are the highest priority for risk mitigation:

| Product | MDR Risk | HHI Risk | Priority |
|---|---|---|---|
| Mineral Products | 🔴 High | 🟡 Moderate | ⚠️ Critical |
| Plastics/Rubbers | 🔴 High | 🟡 Moderate | ⚠️ Critical |
| Electrical Machinery | 🟡 Moderate | 🔴 High | ⚠️ Critical |
| Foodstuffs | 🔴 High | 🟢 Low | 🔶 Monitor |
| Metals | 🟡 Moderate | 🟡 Moderate | 🔶 Monitor |

---

## Recommendations

**1. Diversify transport modes for Mineral Products**
Invest in rail capacity along Belt & Road corridors to reduce oil/gas dependence on sea routes.

**2. Expand supplier base for Electrical Machinery**
Actively develop relationships with alternative semiconductor and electronics suppliers in Southeast Asia, India, and Europe.

**3. Build strategic reserves for high-MDR essentials**
Minerals, plastics, and foodstuffs should have buffer stockpiles to absorb short-term maritime disruptions.

**4. Monitor MDR and HHI annually**
Establish a yearly tracking dashboard (like this one) to catch dependency creep before it becomes a crisis.

**5. Prioritize multimodal infrastructure investment**
The long-term solution is building robust road and rail alternatives so sea disruptions don't cascade into economic shocks.

---

*Analysis by: Vigneshwari Nalla · Ganesh Banoth · Abdullatief Kafilat · Balakireva Elizaveta*
*Data source: UNCTAD Trade Statistics (2016–2021)*
