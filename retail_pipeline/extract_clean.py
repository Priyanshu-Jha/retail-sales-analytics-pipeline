"""
extract_clean.py — Data Extraction & Cleaning Module
=====================================================
Handles loading raw Superstore CSV data, cleaning it,
adding engineered features, and validating data quality.
"""

import pandas as pd
import numpy as np
import os
import sys


def extract_data(filepath: str) -> pd.DataFrame:
    """
    Load raw data from CSV file.

    Parameters
    ----------
    filepath : str
        Path to the Superstore CSV file.

    Returns
    -------
    pd.DataFrame
        Raw dataframe loaded from CSV.
    """
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        sys.exit(1)

    df = pd.read_csv(filepath, encoding='latin1')
    print(f"📥 Extracted {len(df)} records with {len(df.columns)} columns.")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform the raw data.

    Steps:
        1. Remove duplicate rows
        2. Standardize column names (snake_case)
        3. Convert date columns to datetime
        4. Handle missing values
        5. Fix data types
        6. Add engineered features

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe.

    Returns
    -------
    pd.DataFrame
        Cleaned and feature-engineered dataframe.
    """
    initial_rows = len(df)

    # --- 1. Remove duplicates ---
    df = df.drop_duplicates()
    dupes_removed = initial_rows - len(df)
    if dupes_removed > 0:
        print(f"🗑️  Removed {dupes_removed} duplicate rows.")

    # --- 2. Standardize column names ---
    df.columns = (
        df.columns.str.strip()
        .str.replace(' ', '_')
        .str.replace('-', '_')
        .str.lower()
    )

    # --- 3. Convert date columns ---
    df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', dayfirst=False)
    df['ship_date'] = pd.to_datetime(df['ship_date'], format='mixed', dayfirst=False)

    # --- 4. Handle missing values ---
    if df['postal_code'].isnull().any():
        df['postal_code'] = df['postal_code'].fillna(0).astype(int)

    # --- 5. Fix data types ---
    df['postal_code'] = df['postal_code'].astype(str)
    df['quantity'] = df['quantity'].astype(int)
    df['discount'] = df['discount'].astype(float)

    # --- 6. Feature Engineering ---
    # Delivery time
    df['delivery_days'] = (df['ship_date'] - df['order_date']).dt.days

    # Profit margin (%)
    df['profit_margin_pct'] = np.where(
        df['sales'] != 0,
        (df['profit'] / df['sales'] * 100).round(2),
        0.0
    )

    # Revenue per unit
    df['revenue_per_unit'] = np.where(
        df['quantity'] != 0,
        (df['sales'] / df['quantity']).round(2),
        0.0
    )

    # Time-based features
    df['order_year'] = df['order_date'].dt.year
    df['order_month'] = df['order_date'].dt.month
    df['order_quarter'] = df['order_date'].dt.quarter
    df['order_day_of_week'] = df['order_date'].dt.day_name()

    # Profitability flag
    df['is_profitable'] = df['profit'] > 0

    # Discount bucket
    df['discount_bucket'] = pd.cut(
        df['discount'],
        bins=[-0.01, 0.0, 0.1, 0.2, 0.3, 1.0],
        labels=['No Discount', '1-10%', '11-20%', '21-30%', '30%+']
    )

    print(f"🧹 Cleaning complete. {len(df)} records, {len(df.columns)} columns.")
    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run data quality checks and print a summary report.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe.

    Returns
    -------
    pd.DataFrame
        The same dataframe (pass-through).
    """
    print("\n" + "=" * 55)
    print("        📋 DATA QUALITY REPORT")
    print("=" * 55)
    print(f"  Total Records     : {len(df):,}")
    print(f"  Total Columns     : {len(df.columns)}")
    print(f"  Date Range        : {df['order_date'].min().date()} → {df['order_date'].max().date()}")
    print(f"  Unique Orders     : {df['order_id'].nunique():,}")
    print(f"  Unique Customers  : {df['customer_id'].nunique():,}")
    print(f"  Unique Products   : {df['product_id'].nunique():,}")
    print(f"  Total Revenue     : ${df['sales'].sum():,.2f}")
    print(f"  Total Profit      : ${df['profit'].sum():,.2f}")
    print(f"  Avg Profit Margin : {df['profit_margin_pct'].mean():.2f}%")

    # Missing values
    nulls = df.isnull().sum()
    null_cols = nulls[nulls > 0]
    if len(null_cols) > 0:
        print(f"\n  ⚠️  Columns with missing values:")
        for col, count in null_cols.items():
            print(f"      {col}: {count}")
    else:
        print(f"\n  ✅ No missing values found.")

    # Negative profit records
    neg_profit = (df['profit'] < 0).sum()
    print(f"  📉 Loss-making transactions: {neg_profit} ({neg_profit / len(df) * 100:.1f}%)")

    print("=" * 55 + "\n")
    return df


if __name__ == "__main__":
    # Quick standalone test
    raw = extract_data("../archive/Sample - Superstore.csv")
    cleaned = clean_data(raw)
    validated = validate_data(cleaned)
    print(cleaned.head())
