"""
load_database.py — Database Loading Module
============================================
Loads cleaned data into a SQLite database and
runs analytical SQL queries, saving results to CSV.
"""

import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text
import os


def load_to_database(df: pd.DataFrame, db_path: str = "output/retail_sales.db") -> create_engine:
    """
    Load cleaned DataFrame into a SQLite database.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe to load.
    db_path : str
        Path for the SQLite database file.

    Returns
    -------
    sqlalchemy.engine.Engine
        Database engine for running queries.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    engine = create_engine(f"sqlite:///{db_path}")

    # Convert datetime columns to string for SQLite compatibility
    df_db = df.copy()
    for col in df_db.select_dtypes(include=['datetime64']).columns:
        df_db[col] = df_db[col].astype(str)

    # Convert categorical columns to string
    for col in df_db.select_dtypes(include=['category']).columns:
        df_db[col] = df_db[col].astype(str)

    # Load into database
    df_db.to_sql('sales', engine, if_exists='replace', index=False)
    print(f"💾 Loaded {len(df_db):,} records into SQLite → {db_path}")

    return engine


def run_analysis_queries(engine, output_dir: str = "output") -> dict:
    """
    Run analytical SQL queries and save results.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        Database engine.
    output_dir : str
        Directory to save query results as CSV.

    Returns
    -------
    dict
        Dictionary of query names → result DataFrames.
    """
    os.makedirs(output_dir, exist_ok=True)

    queries = {
        # --- 1. Monthly Revenue & Profit Trend ---
        "monthly_trend": """
            SELECT
                substr(order_date, 1, 7)        AS month,
                ROUND(SUM(sales), 2)             AS total_revenue,
                ROUND(SUM(profit), 2)            AS total_profit,
                COUNT(DISTINCT order_id)          AS total_orders,
                COUNT(DISTINCT customer_id)       AS unique_customers,
                ROUND(AVG(profit_margin_pct), 2)  AS avg_profit_margin
            FROM sales
            GROUP BY month
            ORDER BY month
        """,

        # --- 2. Top 15 Products by Profit ---
        "top_products": """
            SELECT
                product_name,
                category,
                sub_category,
                ROUND(SUM(sales), 2)    AS total_sales,
                ROUND(SUM(profit), 2)   AS total_profit,
                SUM(quantity)            AS units_sold,
                ROUND(AVG(discount), 2) AS avg_discount
            FROM sales
            GROUP BY product_name, category, sub_category
            ORDER BY total_profit DESC
            LIMIT 15
        """,

        # --- 3. Bottom 15 Products (Biggest Losses) ---
        "worst_products": """
            SELECT
                product_name,
                category,
                sub_category,
                ROUND(SUM(sales), 2)    AS total_sales,
                ROUND(SUM(profit), 2)   AS total_profit,
                SUM(quantity)            AS units_sold,
                ROUND(AVG(discount), 2) AS avg_discount
            FROM sales
            GROUP BY product_name, category, sub_category
            ORDER BY total_profit ASC
            LIMIT 15
        """,

        # --- 4. Regional Performance ---
        "regional_performance": """
            SELECT
                region,
                COUNT(DISTINCT customer_id)       AS unique_customers,
                COUNT(DISTINCT order_id)          AS total_orders,
                ROUND(SUM(sales), 2)             AS total_revenue,
                ROUND(SUM(profit), 2)            AS total_profit,
                ROUND(AVG(profit_margin_pct), 2)  AS avg_profit_margin,
                ROUND(AVG(delivery_days), 1)      AS avg_delivery_days
            FROM sales
            GROUP BY region
            ORDER BY total_revenue DESC
        """,

        # --- 5. Category & Sub-Category Analysis ---
        "category_analysis": """
            SELECT
                category,
                sub_category,
                ROUND(SUM(sales), 2)             AS total_revenue,
                ROUND(SUM(profit), 2)            AS total_profit,
                ROUND(AVG(profit_margin_pct), 2)  AS avg_profit_margin,
                SUM(quantity)                     AS total_units,
                ROUND(AVG(discount), 2)           AS avg_discount
            FROM sales
            GROUP BY category, sub_category
            ORDER BY category, total_revenue DESC
        """,

        # --- 6. Customer Segment Performance ---
        "segment_analysis": """
            SELECT
                segment,
                COUNT(DISTINCT customer_id)       AS unique_customers,
                ROUND(SUM(sales), 2)             AS total_revenue,
                ROUND(SUM(profit), 2)            AS total_profit,
                ROUND(AVG(profit_margin_pct), 2)  AS avg_profit_margin,
                ROUND(SUM(sales) * 1.0 / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
            FROM sales
            GROUP BY segment
            ORDER BY total_revenue DESC
        """,

        # --- 7. Shipping Mode Analysis ---
        "shipping_analysis": """
            SELECT
                ship_mode,
                COUNT(*)                     AS order_count,
                ROUND(AVG(delivery_days), 1) AS avg_delivery_days,
                ROUND(SUM(sales), 2)         AS total_revenue,
                ROUND(SUM(profit), 2)        AS total_profit,
                ROUND(AVG(discount), 3)      AS avg_discount
            FROM sales
            GROUP BY ship_mode
            ORDER BY order_count DESC
        """,

        # --- 8. Discount Impact Analysis ---
        "discount_impact": """
            SELECT
                discount_bucket,
                COUNT(*)                          AS transaction_count,
                ROUND(SUM(sales), 2)             AS total_revenue,
                ROUND(SUM(profit), 2)            AS total_profit,
                ROUND(AVG(profit_margin_pct), 2)  AS avg_profit_margin,
                SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS loss_count
            FROM sales
            GROUP BY discount_bucket
            ORDER BY discount_bucket
        """,

        # --- 9. State-Level Top 10 Revenue ---
        "top_states": """
            SELECT
                state,
                region,
                COUNT(DISTINCT customer_id)  AS unique_customers,
                ROUND(SUM(sales), 2)         AS total_revenue,
                ROUND(SUM(profit), 2)        AS total_profit,
                ROUND(AVG(profit_margin_pct), 2) AS avg_profit_margin
            FROM sales
            GROUP BY state, region
            ORDER BY total_revenue DESC
            LIMIT 10
        """,

        # --- 10. Year-over-Year Growth ---
        "yoy_growth": """
            WITH yearly AS (
                SELECT
                    order_year,
                    ROUND(SUM(sales), 2) AS revenue,
                    ROUND(SUM(profit), 2) AS profit,
                    COUNT(DISTINCT order_id) AS orders
                FROM sales
                GROUP BY order_year
            )
            SELECT
                y.order_year,
                y.revenue,
                y.profit,
                y.orders,
                ROUND((y.revenue - prev.revenue) / prev.revenue * 100, 2) AS revenue_growth_pct,
                ROUND((y.profit - prev.profit) / prev.profit * 100, 2) AS profit_growth_pct
            FROM yearly y
            LEFT JOIN yearly prev ON y.order_year = prev.order_year + 1
            ORDER BY y.order_year
        """
    }

    results = {}
    print("\n📊 Running SQL Analysis Queries...")
    print("-" * 50)

    for name, query in queries.items():
        with engine.connect() as conn:
            result_df = pd.read_sql(text(query), conn)
        results[name] = result_df

        # Save to CSV
        csv_path = os.path.join(output_dir, f"{name}.csv")
        result_df.to_csv(csv_path, index=False)
        print(f"  ✅ {name:<25} → {len(result_df)} rows → {csv_path}")

    print("-" * 50)
    print(f"📁 All query results saved to '{output_dir}/' folder.\n")

    return results


if __name__ == "__main__":
    # Quick test
    df = pd.read_csv("../archive/Sample - Superstore.csv", encoding='latin1')
    engine = load_to_database(df)
    results = run_analysis_queries(engine)
