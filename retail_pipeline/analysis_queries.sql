-- =============================================================
-- analysis_queries.sql
-- Standalone SQL Queries for Retail Sales Analysis
-- Database: retail_sales.db  |  Table: sales
-- =============================================================
-- You can run these directly in any SQLite client or DB Browser.
-- These are the same queries used in load_database.py


-- ---------------------------------------------------------------
-- 1. MONTHLY REVENUE & PROFIT TREND
-- Shows how revenue and profit change month-over-month
-- ---------------------------------------------------------------
SELECT
    substr(order_date, 1, 7)        AS month,
    ROUND(SUM(sales), 2)            AS total_revenue,
    ROUND(SUM(profit), 2)           AS total_profit,
    COUNT(DISTINCT order_id)         AS total_orders,
    COUNT(DISTINCT customer_id)      AS unique_customers,
    ROUND(AVG(profit_margin_pct), 2) AS avg_profit_margin
FROM sales
GROUP BY month
ORDER BY month;


-- ---------------------------------------------------------------
-- 2. TOP 15 MOST PROFITABLE PRODUCTS
-- ---------------------------------------------------------------
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
LIMIT 15;


-- ---------------------------------------------------------------
-- 3. BOTTOM 15 PRODUCTS (BIGGEST LOSSES)
-- ---------------------------------------------------------------
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
LIMIT 15;


-- ---------------------------------------------------------------
-- 4. REGIONAL PERFORMANCE
-- Compares the 4 US regions on key metrics
-- ---------------------------------------------------------------
SELECT
    region,
    COUNT(DISTINCT customer_id)      AS unique_customers,
    COUNT(DISTINCT order_id)         AS total_orders,
    ROUND(SUM(sales), 2)            AS total_revenue,
    ROUND(SUM(profit), 2)           AS total_profit,
    ROUND(AVG(profit_margin_pct), 2) AS avg_profit_margin,
    ROUND(AVG(delivery_days), 1)     AS avg_delivery_days
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;


-- ---------------------------------------------------------------
-- 5. CATEGORY & SUB-CATEGORY BREAKDOWN
-- ---------------------------------------------------------------
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2)            AS total_revenue,
    ROUND(SUM(profit), 2)           AS total_profit,
    ROUND(AVG(profit_margin_pct), 2) AS avg_profit_margin,
    SUM(quantity)                    AS total_units,
    ROUND(AVG(discount), 2)          AS avg_discount
FROM sales
GROUP BY category, sub_category
ORDER BY category, total_revenue DESC;


-- ---------------------------------------------------------------
-- 6. CUSTOMER SEGMENT PERFORMANCE
-- ---------------------------------------------------------------
SELECT
    segment,
    COUNT(DISTINCT customer_id)       AS unique_customers,
    ROUND(SUM(sales), 2)             AS total_revenue,
    ROUND(SUM(profit), 2)            AS total_profit,
    ROUND(AVG(profit_margin_pct), 2)  AS avg_profit_margin,
    ROUND(SUM(sales) * 1.0 / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM sales
GROUP BY segment
ORDER BY total_revenue DESC;


-- ---------------------------------------------------------------
-- 7. SHIPPING MODE ANALYSIS
-- ---------------------------------------------------------------
SELECT
    ship_mode,
    COUNT(*)                     AS order_count,
    ROUND(AVG(delivery_days), 1) AS avg_delivery_days,
    ROUND(SUM(sales), 2)        AS total_revenue,
    ROUND(SUM(profit), 2)       AS total_profit,
    ROUND(AVG(discount), 3)     AS avg_discount
FROM sales
GROUP BY ship_mode
ORDER BY order_count DESC;


-- ---------------------------------------------------------------
-- 8. DISCOUNT IMPACT ON PROFITABILITY
-- Shows how discount levels affect profit margins
-- ---------------------------------------------------------------
SELECT
    discount_bucket,
    COUNT(*)                          AS transaction_count,
    ROUND(SUM(sales), 2)             AS total_revenue,
    ROUND(SUM(profit), 2)            AS total_profit,
    ROUND(AVG(profit_margin_pct), 2)  AS avg_profit_margin,
    SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS loss_count
FROM sales
GROUP BY discount_bucket
ORDER BY discount_bucket;


-- ---------------------------------------------------------------
-- 9. TOP 10 STATES BY REVENUE
-- ---------------------------------------------------------------
SELECT
    state,
    region,
    COUNT(DISTINCT customer_id)      AS unique_customers,
    ROUND(SUM(sales), 2)            AS total_revenue,
    ROUND(SUM(profit), 2)           AS total_profit,
    ROUND(AVG(profit_margin_pct), 2) AS avg_profit_margin
FROM sales
GROUP BY state, region
ORDER BY total_revenue DESC
LIMIT 10;


-- ---------------------------------------------------------------
-- 10. YEAR-OVER-YEAR GROWTH (Window-style via self-join)
-- ---------------------------------------------------------------
WITH yearly AS (
    SELECT
        order_year,
        ROUND(SUM(sales), 2)  AS revenue,
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
    ROUND((y.revenue  - prev.revenue)  / prev.revenue  * 100, 2) AS revenue_growth_pct,
    ROUND((y.profit   - prev.profit)   / prev.profit   * 100, 2) AS profit_growth_pct
FROM yearly y
LEFT JOIN yearly prev ON y.order_year = prev.order_year + 1
ORDER BY y.order_year;
