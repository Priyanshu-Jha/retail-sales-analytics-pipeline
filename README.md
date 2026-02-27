# 📊 Retail Sales Analytics Pipeline

An end-to-end **ETL + Analytics** pipeline that processes 10,000+ retail sales records to generate actionable business insights through SQL analysis and data visualization.

---

## 🏗️ Architecture

```
Raw CSV Data ──→ Extract ──→ Clean & Transform ──→ SQLite DB ──→ SQL Analysis ──→ Visualizations
                  (Python)    (Pandas/NumPy)       (SQLAlchemy)    (10 Queries)     (Matplotlib/Seaborn)
```

## 🗂️ Project Structure

```
retail_pipeline/
│
├── main.py                 # Pipeline orchestrator (run this!)
├── extract_clean.py        # Data extraction, cleaning & feature engineering
├── load_database.py        # SQLite loading & analytical SQL queries
├── eda_analysis.py         # 10 publication-quality visualizations
├── generate_report.py      # Automated PDF report generator
├── analysis_queries.sql    # Standalone SQL queries (portable)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
└── output/                 # Generated outputs
    ├── retail_sales.db     # SQLite database
    ├── *.csv               # Query results (10 files)
    ├── *.png               # Charts (10 files)
    └── Retail_Sales_Analysis_Report.pdf  # Auto-generated PDF report
```

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Core language |
| **Pandas** | Data manipulation & cleaning |
| **NumPy** | Numerical operations |
| **SQLAlchemy** | Database ORM & connection |
| **SQLite** | Lightweight relational database |
| **Matplotlib** | Data visualization |
| **Seaborn** | Statistical plots |

## 🚀 Quick Start

```bash
# 1. Create virtual environment
python -m venv retail_pipeline_env

# 2. Activate it
# Windows:
.\retail_pipeline_env\Scripts\Activate.ps1
# macOS/Linux:
source retail_pipeline_env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the pipeline
python main.py
```

## 📦 Dataset

- **Source:** [Kaggle - Superstore Sales Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- **Records:** 9,994 transactions
- **Time Period:** 2014–2017
- **Features:** 21 columns including Order Date, Sales, Profit, Category, Region, etc.

## 🔧 Pipeline Steps

### Step 1 — Extract
- Loads raw CSV with encoding handling
- Validates file existence

### Step 2 — Clean & Transform
- Removes duplicates
- Standardizes column names to `snake_case`
- Parses date columns
- Handles missing values
- **Feature Engineering:**
  - `delivery_days` — shipping turnaround time
  - `profit_margin_pct` — profit as % of sales
  - `revenue_per_unit` — sales / quantity
  - `order_year`, `order_month`, `order_quarter`
  - `is_profitable` — boolean flag
  - `discount_bucket` — categorized discount levels

### Step 3 — Data Quality Validation
- Record counts, date range, null checks
- Business metric summary

### Step 4 — SQL Analysis (10 Queries)
1. Monthly Revenue & Profit Trend
2. Top 15 Most Profitable Products
3. Bottom 15 Products (Biggest Losses)
4. Regional Performance Comparison
5. Category & Sub-Category Breakdown
6. Customer Segment Analysis
7. Shipping Mode Analysis
8. Discount Impact on Profitability
9. Top 10 States by Revenue
10. Year-over-Year Growth (with CTE + self-join)

### Step 5 — Visualizations (10 Charts)
1. Monthly Revenue & Profit Trend (dual-axis line)
2. Revenue & Profit by Category (grouped bar)
3. Sub-Category Profit (horizontal bar, color-coded)
4. Regional Performance (pie + bar)
5. Discount vs Profit Scatter
6. Discount Bucket Impact (margin analysis)
7. Customer Segment Revenue (donut chart)
8. Shipping Mode Analysis (delivery days vs revenue)
9. Year-over-Year Growth (bar chart)
10. Feature Correlation Heatmap

## 📈 Key Business Insights

| Finding | Impact |
|---------|--------|
| **West region** has highest revenue but lower profit margins | Over-discounting in West erodes margins |
| **Tables & Bookcases** are loss-making sub-categories | Recommend pricing review or discontinuation |
| **Discounts > 20%** consistently produce negative profits | Cap discount levels at 20% |
| **Standard Class** shipping dominates (~60%) | Optimize logistics for this mode |
| **Consumer segment** drives 50%+ of revenue | Focus retention marketing here |

## 📊 Sample Output

After running the pipeline, you'll find in the `output/` folder:
- **10 CSV files** with query results
- **10 PNG charts** ready for presentations
- **1 SQLite database** for further exploration

## 👤 Author

Built as a **Data Analytics Portfolio Project** demonstrating:
- ETL pipeline development
- SQL analytical query writing (CTEs, window functions, aggregations)
- Python data engineering
- Business insight generation
- Data visualization best practices

---

> 💡 *This project processes real-world retail data to identify revenue trends, profitability drivers, and actionable business recommendations.*
