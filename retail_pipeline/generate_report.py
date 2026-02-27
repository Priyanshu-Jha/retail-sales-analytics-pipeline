"""
generate_report.py — PDF Report Generator
===========================================
Creates a professional PDF report with all findings,
charts, and business recommendations from the pipeline.
"""

import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime


OUTPUT_DIR = "output"
REPORT_PATH = os.path.join(OUTPUT_DIR, "Retail_Sales_Analysis_Report.pdf")


class SalesReport(FPDF):
    """Custom PDF class with header/footer."""

    @staticmethod
    def _sanitize(text):
        """Replace Unicode characters that Helvetica can't encode."""
        replacements = {
            '\u2014': '-',   # em dash
            '\u2013': '-',   # en dash
            '\u2018': "'",   # left single quote
            '\u2019': "'",   # right single quote
            '\u201c': '"',   # left double quote
            '\u201d': '"',   # right double quote
            '\u2022': '-',   # bullet
            '\u2026': '...',  # ellipsis
            '\u2192': '->',  # right arrow
            '\u2190': '<-',  # left arrow
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Retail Sales Analytics Report", align="L")
        self.cell(0, 8, f"Generated: {datetime.now().strftime('%B %d, %Y')}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(33, 150, 243)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(33, 33, 33)
        self.ln(4)
        self.cell(0, 10, self._sanitize(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(33, 150, 243)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(66, 66, 66)
        self.cell(0, 8, self._sanitize(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, self._sanitize(text))
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        x = self.get_x()
        self.cell(10, 5.5, "  - ", new_x="END")
        self.multi_cell(170, 5.5, self._sanitize(text))
        self.set_x(x)

    def add_chart(self, image_path, title, w=180):
        if os.path.exists(image_path):
            if self.get_y() > 180:
                self.add_page()
            self.sub_title(title)
            self.image(image_path, x=15, w=w)
            self.ln(6)

    def add_table(self, df, col_widths=None):
        """Add a simple table from a DataFrame."""
        if col_widths is None:
            available = 190
            col_widths = [available / len(df.columns)] * len(df.columns)

        # Header
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(33, 150, 243)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(df.columns):
            self.cell(col_widths[i], 7, str(col)[:20], border=1, fill=True, align="C")
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(50, 50, 50)
        fill = False
        for _, row in df.iterrows():
            if self.get_y() > 270:
                self.add_page()
            if fill:
                self.set_fill_color(240, 245, 250)
            else:
                self.set_fill_color(255, 255, 255)
            for i, val in enumerate(row):
                text = self._sanitize(str(val)[:25])
                self.cell(col_widths[i], 6, text, border=1, fill=True, align="C")
            self.ln()
            fill = not fill
        self.ln(4)


def generate_report():
    """Generate the complete PDF report."""

    pdf = SalesReport()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ──────────────────────────────────────────────
    # PAGE 1: COVER PAGE
    # ──────────────────────────────────────────────
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(33, 33, 33)
    pdf.cell(0, 15, "Retail Sales Analytics", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(33, 150, 243)
    pdf.cell(0, 12, "Data Pipeline & Business Intelligence Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_draw_color(33, 150, 243)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(15)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Dataset: Superstore Sales (9,994 Transactions)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Period: January 2014 - December 2017", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Report Date: {datetime.now().strftime('%B %d, %Y')}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, "Tech Stack: Python | Pandas | SQL | SQLite | Matplotlib | Seaborn", align="C", new_x="LMARGIN", new_y="NEXT")

    # ──────────────────────────────────────────────
    # PAGE 2: EXECUTIVE SUMMARY
    # ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("1. Executive Summary")
    pdf.body_text(
        "This report presents the findings from an end-to-end data analytics pipeline built to analyze "
        "retail sales data from a US-based superstore. The pipeline processes 9,994 transaction records "
        "spanning 4 years (2014-2017), covering 793 unique customers across 4 US regions."
    )

    pdf.sub_title("Key Metrics at a Glance")
    pdf.body_text(
        "Total Revenue: $2,297,200.86\n"
        "Total Profit: $286,397.02\n"
        "Overall Profit Margin: 12.03%\n"
        "Unique Orders: 5,009\n"
        "Unique Customers: 793\n"
        "Product Catalog: 1,862 unique products\n"
        "Loss-Making Transactions: 1,871 (18.7% of all sales)"
    )

    pdf.sub_title("Top 5 Findings")
    pdf.bullet("West region leads revenue ($725K) but suffers from over-discounting that erodes profit margins.")
    pdf.bullet("Tables and Bookcases sub-categories are consistent loss-makers, requiring pricing strategy review.")
    pdf.bullet("Discounts exceeding 20% almost always result in negative profit — recommend capping at 20%.")
    pdf.bullet("Consumer segment drives 50%+ of revenue — focus retention and loyalty programs here.")
    pdf.bullet("Year-over-year revenue grew 20.36% in the latest year, showing healthy business growth.")

    # ──────────────────────────────────────────────
    # PAGE 3: REVENUE TRENDS
    # ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("2. Revenue & Profit Trends")
    pdf.body_text(
        "The monthly trend analysis reveals a clear seasonal pattern with revenue peaks in November-December "
        "(holiday season) and consistent dips in January-February. Profit generally follows revenue trends "
        "but shows occasional divergence when heavy discounting occurs."
    )
    pdf.add_chart(os.path.join(OUTPUT_DIR, "01_monthly_trend.png"), "Fig 2.1 — Monthly Revenue & Profit Trend")

    pdf.add_chart(os.path.join(OUTPUT_DIR, "09_yoy_growth.png"), "Fig 2.2 — Year-over-Year Growth")

    # Load YoY data
    yoy_path = os.path.join(OUTPUT_DIR, "yoy_growth.csv")
    if os.path.exists(yoy_path):
        yoy = pd.read_csv(yoy_path)
        pdf.sub_title("Year-over-Year Performance")
        pdf.add_table(yoy, col_widths=[20, 35, 30, 25, 40, 40])

    # ──────────────────────────────────────────────
    # PAGE 4: CATEGORY ANALYSIS
    # ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("3. Category & Product Analysis")
    pdf.body_text(
        "Technology leads in both revenue and profit, while Furniture has the lowest profit margins. "
        "At the sub-category level, Copiers and Phones are the most profitable, whereas Tables and "
        "Bookcases generate significant losses."
    )
    pdf.add_chart(os.path.join(OUTPUT_DIR, "02_category_performance.png"), "Fig 3.1 — Revenue & Profit by Category")
    pdf.add_chart(os.path.join(OUTPUT_DIR, "03_subcategory_profit.png"), "Fig 3.2 — Sub-Category Profitability")

    # Category table
    cat_path = os.path.join(OUTPUT_DIR, "category_analysis.csv")
    if os.path.exists(cat_path):
        pdf.add_page()
        cat = pd.read_csv(cat_path)
        pdf.sub_title("Category & Sub-Category Breakdown")
        pdf.add_table(cat, col_widths=[25, 25, 27, 27, 27, 27, 27])

    # Top products
    top_path = os.path.join(OUTPUT_DIR, "top_products.csv")
    if os.path.exists(top_path):
        pdf.sub_title("Top 15 Most Profitable Products")
        top = pd.read_csv(top_path)
        top_display = top[['product_name', 'category', 'total_sales', 'total_profit']].copy()
        top_display['product_name'] = top_display['product_name'].str[:35]
        pdf.add_table(top_display, col_widths=[70, 30, 40, 40])

    # Worst products
    worst_path = os.path.join(OUTPUT_DIR, "worst_products.csv")
    if os.path.exists(worst_path):
        pdf.add_page()
        pdf.sub_title("Bottom 15 Products (Biggest Losses)")
        worst = pd.read_csv(worst_path)
        worst_display = worst[['product_name', 'category', 'total_sales', 'total_profit']].copy()
        worst_display['product_name'] = worst_display['product_name'].str[:35]
        pdf.add_table(worst_display, col_widths=[70, 30, 40, 40])

    # ──────────────────────────────────────────────
    # REGIONAL PERFORMANCE
    # ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("4. Regional Performance")
    pdf.body_text(
        "The West region generates the highest revenue ($725K) followed by East ($678K). "
        "However, the Central region shows concerning metrics with lower profit margins despite "
        "decent revenue, indicating potential pricing or cost issues."
    )
    pdf.add_chart(os.path.join(OUTPUT_DIR, "04_regional_performance.png"), "Fig 4.1 — Revenue & Profit by Region")

    reg_path = os.path.join(OUTPUT_DIR, "regional_performance.csv")
    if os.path.exists(reg_path):
        reg = pd.read_csv(reg_path)
        pdf.sub_title("Regional Metrics Summary")
        pdf.add_table(reg, col_widths=[22, 28, 25, 28, 28, 30, 30])

    # Top states
    states_path = os.path.join(OUTPUT_DIR, "top_states.csv")
    if os.path.exists(states_path):
        pdf.sub_title("Top 10 States by Revenue")
        states = pd.read_csv(states_path)
        pdf.add_table(states, col_widths=[35, 22, 28, 35, 35, 35])

    # ──────────────────────────────────────────────
    # DISCOUNT ANALYSIS
    # ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("5. Discount Impact Analysis")
    pdf.body_text(
        "This is the most critical finding. There is a strong negative correlation between discount "
        "levels and profitability. Transactions with no discount have an average profit margin of ~28%, "
        "while discounts above 20% consistently produce negative margins. "
        "This suggests the company is over-discounting, particularly in the Furniture category."
    )
    pdf.add_chart(os.path.join(OUTPUT_DIR, "05_discount_vs_profit.png"), "Fig 5.1 — Discount vs Profit (Scatter)")
    pdf.add_chart(os.path.join(OUTPUT_DIR, "06_discount_bucket_impact.png"), "Fig 5.2 — Profit Margin by Discount Level")

    disc_path = os.path.join(OUTPUT_DIR, "discount_impact.csv")
    if os.path.exists(disc_path):
        disc = pd.read_csv(disc_path)
        pdf.sub_title("Discount Bucket Impact")
        pdf.add_table(disc, col_widths=[30, 30, 30, 30, 35, 30])

    # ──────────────────────────────────────────────
    # CUSTOMER SEGMENTS
    # ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("6. Customer Segment Analysis")
    pdf.body_text(
        "The Consumer segment is the largest revenue driver (50%+), followed by Corporate and Home Office. "
        "Home Office has the highest revenue-per-customer, making it an efficient segment to target. "
        "Corporate customers order in higher quantities but at slightly lower margins."
    )
    pdf.add_chart(os.path.join(OUTPUT_DIR, "07_segment_analysis.png"), "Fig 6.1 — Revenue by Customer Segment")

    seg_path = os.path.join(OUTPUT_DIR, "segment_analysis.csv")
    if os.path.exists(seg_path):
        seg = pd.read_csv(seg_path)
        pdf.sub_title("Segment Performance Metrics")
        pdf.add_table(seg, col_widths=[30, 30, 30, 30, 35, 35])

    # ──────────────────────────────────────────────
    # SHIPPING ANALYSIS
    # ──────────────────────────────────────────────
    pdf.section_title("7. Shipping Mode Analysis")
    pdf.body_text(
        "Standard Class shipping dominates with ~60% of orders and 4-5 day average delivery. "
        "Same Day shipping is used least but shows similar profit margins, suggesting customers "
        "are not charged enough premium for expedited shipping."
    )
    pdf.add_chart(os.path.join(OUTPUT_DIR, "08_shipping_analysis.png"), "Fig 7.1 — Shipping Mode Comparison")

    ship_path = os.path.join(OUTPUT_DIR, "shipping_analysis.csv")
    if os.path.exists(ship_path):
        ship = pd.read_csv(ship_path)
        pdf.sub_title("Shipping Performance")
        pdf.add_table(ship, col_widths=[30, 25, 35, 30, 30, 30])

    # ──────────────────────────────────────────────
    # CORRELATION ANALYSIS
    # ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("8. Correlation Analysis")
    pdf.body_text(
        "The correlation heatmap reveals key relationships between numerical features. "
        "Sales and Profit have a strong positive correlation (expected). Discount has a notable "
        "negative correlation with Profit Margin, confirming our discount impact findings. "
        "Quantity shows weak correlation with profit, suggesting pricing matters more than volume."
    )
    pdf.add_chart(os.path.join(OUTPUT_DIR, "10_correlation_heatmap.png"), "Fig 8.1 — Feature Correlation Matrix")

    # ──────────────────────────────────────────────
    # RECOMMENDATIONS
    # ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("9. Business Recommendations")
    pdf.ln(2)

    recommendations = [
        ("Cap Discounts at 20%",
         "Discounts above 20% consistently destroy profitability. Implementing a hard cap could "
         "recover an estimated $50K+ in annual profit without significantly impacting sales volume."),

        ("Review Furniture Pricing Strategy",
         "Tables and Bookcases are consistent loss-makers. Consider discontinuing low-margin SKUs, "
         "renegotiating supplier costs, or repositioning these as premium products."),

        ("Optimize West Region Discounting",
         "Despite leading in revenue, the West region's profit margins are compressed due to "
         "aggressive discounting. Reduce promotional intensity by 15% in this region."),

        ("Invest in Consumer Segment Retention",
         "The Consumer segment drives majority revenue. Implement loyalty programs and personalized "
         "marketing to increase repeat purchases and lifetime value."),

        ("Charge Premium for Same-Day Shipping",
         "Same-Day shipping costs are not being adequately passed to customers. Increase expedited "
         "shipping fees or make it exclusive to high-value orders."),

        ("Focus on High-Margin Sub-Categories",
         "Copiers, Phones, and Accessories show the highest margins. Increase marketing spend "
         "and inventory allocation for these product lines."),
    ]

    for i, (title, desc) in enumerate(recommendations, 1):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(33, 150, 243)
        pdf.cell(0, 7, f"Recommendation {i}: {title}", new_x="LMARGIN", new_y="NEXT")
        pdf.body_text(desc)

    # ──────────────────────────────────────────────
    # METHODOLOGY
    # ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("10. Methodology & Tech Stack")
    pdf.body_text(
        "This analysis was conducted using an automated ETL (Extract, Transform, Load) pipeline "
        "built in Python. The pipeline follows industry-standard data engineering practices."
    )

    pdf.sub_title("Pipeline Architecture")
    pdf.body_text(
        "Raw CSV Data -> Extract (Python) -> Clean & Transform (Pandas/NumPy) -> "
        "Load to SQLite (SQLAlchemy) -> SQL Analysis (10 Queries) -> "
        "Visualization (Matplotlib/Seaborn) -> PDF Report (FPDF2)"
    )

    pdf.sub_title("Tools Used")
    tools = [
        "Python 3.10+ — Core programming language",
        "Pandas — Data manipulation, cleaning, and feature engineering",
        "NumPy — Numerical operations and calculations",
        "SQLAlchemy — Database ORM and SQL query execution",
        "SQLite — Lightweight relational database for data storage",
        "Matplotlib — Primary visualization library",
        "Seaborn — Statistical visualization and styling",
        "FPDF2 — PDF report generation",
    ]
    for tool in tools:
        pdf.bullet(tool)

    pdf.ln(4)
    pdf.sub_title("Feature Engineering")
    features = [
        "delivery_days — Shipping turnaround time (Ship Date - Order Date)",
        "profit_margin_pct — Profit as percentage of sales",
        "revenue_per_unit — Sales divided by quantity",
        "order_year / order_month / order_quarter — Temporal features",
        "is_profitable — Boolean flag for profitable transactions",
        "discount_bucket — Categorized discount levels (No Discount, 1-10%, 11-20%, 21-30%, 30%+)",
    ]
    for feat in features:
        pdf.bullet(feat)

    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, "-- End of Report --", align="C")

    # ── Save PDF ──
    pdf.output(REPORT_PATH)
    size_kb = os.path.getsize(REPORT_PATH) / 1024
    print(f"\n📄 PDF Report Generated: {REPORT_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    generate_report()
