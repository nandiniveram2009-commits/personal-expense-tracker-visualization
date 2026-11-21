# 💰 Personal Expense Tracker with Data Visualization

An end-to-end Python data analytics and personal finance project that ingests expense transactions (CSV, manual entry, or synthetic simulation), automatically categorizes them, stores them in SQLite, tracks category budgets, generates publication-ready visualizations, exports monthly reports, and serves an interactive Streamlit dashboard.

---

## 📌 Problem Statement
Individuals and students often struggle to track daily micro-transactions across multiple payment modes (UPI, cards, cash), leading to overspending and zero visibility into monthly cash flow. Without access to live banking APIs, building an automated, privacy-friendly analytics pipeline solves this problem by turning raw transaction logs into actionable financial insights.

---

## 🏢 Industry Relevance
This project demonstrates practical skills applicable to **Python Developer, Data Analyst, Business Analyst, Automation Engineer, and FinTech/Finance** roles:
- **ETL & Data Engineering:** Ingestion, deduplication, schema enforcement, and SQLite persistence.
- **Data Cleaning & Analytics:** Time-series aggregation, rolling averages, MoM % variance, and KPI computation using Pandas & NumPy.
- **Automation:** Rule-based text categorization and automated monthly report generation.
- **BI & Visualization:** Executive Matplotlib/Seaborn charts and interactive Streamlit dashboards.

---

## ✨ Key Features
- **Multi-Source Ingestion:** Synthetic 6-month dataset generator, CSV upload, and manual expense entry form.
- **Auto-Categorization:** Keyword-based classifier automatically tags uncategorized merchants (e.g., *Swiggy* → *Food & Dining*, *Uber* → *Transport*).
- **SQLite Persistence:** Deduplicated relational storage (`transactions` and `budgets` tables).
- **Financial KPIs:** Total spend, average daily burn rate, highest spending category, and Month-over-Month trends.
- **Budget Alerts:** Compares monthly actuals against customizable category limits (`ON TRACK`, `WARNING`, `OVER BUDGET`).
- **4 Automated Visualizations:** Category bar chart, monthly trend line, payment method donut chart, and 7-day rolling daily spend trend.
- **Report Export:** Generates cleaned CSVs and an executive TXT summary report.

---

## 🛠️ Tech Stack
- **Language:** Python 3.9+
- **Data Manipulation:** Pandas, NumPy
- **Database:** SQLite3
- **Visualization:** Matplotlib, Seaborn
- **Web Dashboard:** Streamlit

---

## 📂 Folder Structure
```text
Personal-Expense-Tracker-Visualization/
├── src/                # Modular Python pipeline (generator, categorizer, db, analyzer, visualizer, reporter)
├── app.py              # Streamlit interactive dashboard
├── main.py             # Master CLI pipeline runner
├── requirements.txt    # Dependencies
└── README.md           # Project documentation

##Learning Outcomes

Designing modular Python packages (src/) instead of monolithic scripts.
Writing idempotent SQLite ingestion pipelines using UNIQUE constraints and INSERT OR IGNORE.
Handling messy date/numeric data cleanly with Pandas.
Building executive-ready financial visualizations and interactive Streamlit UIs.


## Authors

* **GitHub:** [nandiniverma2009](https://github.com)
* **LinkedIn:** [NandiniVerma](https://linkedin.com)
