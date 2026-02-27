"""
main.py — Retail Sales Analytics Pipeline Runner
==================================================
Orchestrates the complete ETL + Analysis pipeline:
  1. Extract   → Load raw CSV data
  2. Clean     → Transform, engineer features, validate
  3. Load      → Store in SQLite database
  4. Analyze   → Run 10 SQL analytical queries
  5. Visualize → Generate 10 publication-quality charts

Usage:
    python main.py
"""

import time
import sys
import os

# Ensure we run from the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from extract_clean import extract_data, clean_data, validate_data
from load_database import load_to_database, run_analysis_queries
from eda_analysis import run_eda
from generate_report import generate_report


# ── Configuration ──
DATA_PATH    = "../archive/Sample - Superstore.csv"
DB_PATH      = "output/retail_sales.db"
OUTPUT_DIR   = "output"


def print_banner():
    print("\n" + "=" * 60)
    print("  🚀 RETAIL SALES ANALYTICS PIPELINE")
    print("  Automated ETL → SQL Analysis → Visualization")
    print("=" * 60)


def print_summary(df, results, elapsed):
    """Print final pipeline summary."""
    print("\n" + "=" * 60)
    print("  ✅ PIPELINE COMPLETE — SUMMARY")
    print("=" * 60)
    print(f"  📦 Records Processed   : {len(df):,}")
    print(f"  📊 SQL Queries Run     : {len(results)}")
    print(f"  🎨 Charts Generated    : 10")
    print(f"  💾 Database            : {DB_PATH}")
    print(f"  📁 Output Folder       : {OUTPUT_DIR}/")
    print(f"  ⏱️  Execution Time      : {elapsed:.2f} seconds")
    print("=" * 60)

    print("\n📂 Output Files:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
        print(f"  {'📊' if f.endswith('.csv') else '📈' if f.endswith('.png') else '🗄️'} {f:<40} ({size:>10,} bytes)")

    print("\n💡 Key Business Insights to Present:")
    
    # Pull insights from results
    if 'regional_performance' in results:
        reg = results['regional_performance']
        top_region = reg.iloc[0]
        print(f"  1. {top_region['region']} region leads with ${top_region['total_revenue']:,.0f} revenue")

    if 'discount_impact' in results:
        disc = results['discount_impact']
        print(f"  2. Discount impact: Higher discounts correlate with lower/negative margins")

    if 'category_analysis' in results:
        cat = results['category_analysis']
        worst = cat.sort_values('total_profit').iloc[0]
        print(f"  3. '{worst['sub_category']}' sub-category is the biggest loss-maker")

    if 'yoy_growth' in results:
        yoy = results['yoy_growth']
        last = yoy.iloc[-1]
        if 'revenue_growth_pct' in last and last['revenue_growth_pct'] is not None:
            print(f"  4. Latest year revenue growth: {last.get('revenue_growth_pct', 'N/A')}%")

    print("\n" + "=" * 60 + "\n")


def run_pipeline():
    """Execute the full analytics pipeline."""
    print_banner()
    start_time = time.time()

    # ── Step 1: Extract ──
    print("\n📥 STEP 1/6: Extracting Data...")
    df = extract_data(DATA_PATH)

    # ── Step 2: Clean & Transform ──
    print("\n🧹 STEP 2/6: Cleaning & Transforming Data...")
    df = clean_data(df)

    # ── Step 3: Validate ──
    print("\n📋 STEP 3/6: Validating Data Quality...")
    df = validate_data(df)

    # ── Step 4: Load to Database & Run SQL ──
    print("\n💾 STEP 4/6: Loading to Database & Running Analysis...")
    engine = load_to_database(df, db_path=DB_PATH)
    results = run_analysis_queries(engine, output_dir=OUTPUT_DIR)

    # ── Step 5: Generate Visualizations ──
    print("\n🎨 STEP 5/6: Generating Visualizations...")
    run_eda(df)

    # ── Step 6: Generate PDF Report ──
    print("\n📄 STEP 6/6: Generating PDF Report...")
    generate_report()

    # ── Final Summary ──
    elapsed = time.time() - start_time
    print_summary(df, results, elapsed)


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        print(f"\n❌ Pipeline Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
