"""
eda_analysis.py — Exploratory Data Analysis & Visualization
=============================================================
Generates publication-quality charts for the retail sales dataset.
All figures are saved to the output/ folder.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

# ── Style Configuration ──
sns.set_theme(style="whitegrid", font_scale=1.1)
COLORS = {
    'primary': '#2196F3',
    'secondary': '#4CAF50',
    'accent': '#FF9800',
    'danger': '#F44336',
    'purple': '#9C27B0',
    'palette': ['#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0', '#00BCD4']
}
OUTPUT_DIR = "output"


def _save_fig(fig, name: str):
    """Save figure to output directory."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  📈 Saved: {path}")


# ════════════════════════════════════════════════════════════════
# CHART 1: Monthly Revenue & Profit Trend
# ════════════════════════════════════════════════════════════════
def plot_monthly_trend(df: pd.DataFrame):
    """Line chart showing monthly revenue and profit over time."""
    monthly = (
        df.groupby(df['order_date'].dt.to_period('M'))
        .agg(revenue=('sales', 'sum'), profit=('profit', 'sum'))
        .reset_index()
    )
    monthly['order_date'] = monthly['order_date'].dt.to_timestamp()

    fig, ax1 = plt.subplots(figsize=(14, 5))

    ax1.plot(monthly['order_date'], monthly['revenue'],
             color=COLORS['primary'], linewidth=2, label='Revenue', marker='o', markersize=3)
    ax1.fill_between(monthly['order_date'], monthly['revenue'], alpha=0.1, color=COLORS['primary'])
    ax1.set_ylabel('Revenue ($)', color=COLORS['primary'])
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

    ax2 = ax1.twinx()
    ax2.plot(monthly['order_date'], monthly['profit'],
             color=COLORS['secondary'], linewidth=2, label='Profit', linestyle='--', marker='s', markersize=3)
    ax2.set_ylabel('Profit ($)', color=COLORS['secondary'])
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

    ax1.set_title('Monthly Revenue & Profit Trend', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Month')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.xticks(rotation=45)
    _save_fig(fig, "01_monthly_trend")


# ════════════════════════════════════════════════════════════════
# CHART 2: Sales & Profit by Category
# ════════════════════════════════════════════════════════════════
def plot_category_performance(df: pd.DataFrame):
    """Grouped bar chart for category-level revenue and profit."""
    cat = df.groupby('category').agg(
        revenue=('sales', 'sum'), profit=('profit', 'sum')
    ).sort_values('revenue', ascending=False).reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(cat))
    width = 0.35

    bars1 = ax.bar(x - width/2, cat['revenue'], width, label='Revenue',
                   color=COLORS['primary'], edgecolor='white')
    bars2 = ax.bar(x + width/2, cat['profit'], width, label='Profit',
                   color=COLORS['secondary'], edgecolor='white')

    ax.set_xticks(x)
    ax.set_xticklabels(cat['category'])
    ax.set_title('Revenue & Profit by Category', fontsize=14, fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend()

    # Add value labels
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                f'${bar.get_height():,.0f}', ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                f'${bar.get_height():,.0f}', ha='center', va='bottom', fontsize=8)

    _save_fig(fig, "02_category_performance")


# ════════════════════════════════════════════════════════════════
# CHART 3: Sub-Category Profitability Heatmap
# ════════════════════════════════════════════════════════════════
def plot_subcategory_heatmap(df: pd.DataFrame):
    """Horizontal bar chart of sub-category profit (sorted)."""
    sub = df.groupby('sub_category')['profit'].sum().sort_values()

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = [COLORS['danger'] if v < 0 else COLORS['secondary'] for v in sub.values]
    ax.barh(sub.index, sub.values, color=colors, edgecolor='white')

    ax.set_title('Profit by Sub-Category', fontsize=14, fontweight='bold')
    ax.set_xlabel('Total Profit ($)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.axvline(x=0, color='black', linewidth=0.8)

    # Annotate values
    for i, (val, name) in enumerate(zip(sub.values, sub.index)):
        ax.text(val + (1000 if val >= 0 else -1000), i,
                f'${val:,.0f}', va='center', fontsize=8,
                ha='left' if val >= 0 else 'right')

    _save_fig(fig, "03_subcategory_profit")


# ════════════════════════════════════════════════════════════════
# CHART 4: Regional Performance
# ════════════════════════════════════════════════════════════════
def plot_regional_performance(df: pd.DataFrame):
    """Pie chart + bar chart side by side for regional comparison."""
    region = df.groupby('region').agg(
        revenue=('sales', 'sum'), profit=('profit', 'sum')
    ).sort_values('revenue', ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Pie chart – Revenue share
    ax1.pie(region['revenue'], labels=region.index, autopct='%1.1f%%',
            colors=COLORS['palette'][:len(region)], startangle=90,
            textprops={'fontsize': 10})
    ax1.set_title('Revenue Distribution by Region', fontsize=12, fontweight='bold')

    # Bar chart – Profit
    bars = ax2.bar(region.index, region['profit'],
                   color=COLORS['palette'][:len(region)], edgecolor='white')
    ax2.set_title('Total Profit by Region', fontsize=12, fontweight='bold')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

    for bar in bars:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                 f'${bar.get_height():,.0f}', ha='center', fontsize=9)

    plt.tight_layout()
    _save_fig(fig, "04_regional_performance")


# ════════════════════════════════════════════════════════════════
# CHART 5: Discount vs Profit Scatter
# ════════════════════════════════════════════════════════════════
def plot_discount_vs_profit(df: pd.DataFrame):
    """Scatter plot showing the relationship between discount and profit."""
    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(
        df['discount'], df['profit'],
        c=df['profit'], cmap='RdYlGn',
        alpha=0.4, s=15, edgecolors='none'
    )
    ax.axhline(y=0, color='black', linewidth=0.8, linestyle='--')

    ax.set_title('Discount vs Profit (Each Transaction)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Discount (%)')
    ax.set_ylabel('Profit ($)')
    plt.colorbar(scatter, ax=ax, label='Profit ($)')

    _save_fig(fig, "05_discount_vs_profit")


# ════════════════════════════════════════════════════════════════
# CHART 6: Discount Bucket Impact
# ════════════════════════════════════════════════════════════════
def plot_discount_bucket_impact(df: pd.DataFrame):
    """Bar chart showing avg profit margin by discount bucket."""
    bucket = df.groupby('discount_bucket', observed=True).agg(
        avg_margin=('profit_margin_pct', 'mean'),
        count=('sales', 'count'),
        total_profit=('profit', 'sum')
    ).reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Avg profit margin by bucket
    colors = [COLORS['secondary'] if v > 0 else COLORS['danger'] for v in bucket['avg_margin']]
    ax1.bar(bucket['discount_bucket'].astype(str), bucket['avg_margin'], color=colors)
    ax1.set_title('Avg Profit Margin by Discount Level', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Avg Profit Margin (%)')
    ax1.axhline(y=0, color='black', linewidth=0.8)

    # Total profit by bucket
    colors2 = [COLORS['secondary'] if v > 0 else COLORS['danger'] for v in bucket['total_profit']]
    ax2.bar(bucket['discount_bucket'].astype(str), bucket['total_profit'], color=colors2)
    ax2.set_title('Total Profit by Discount Level', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Total Profit ($)')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax2.axhline(y=0, color='black', linewidth=0.8)

    plt.tight_layout()
    _save_fig(fig, "06_discount_bucket_impact")


# ════════════════════════════════════════════════════════════════
# CHART 7: Segment Analysis
# ════════════════════════════════════════════════════════════════
def plot_segment_analysis(df: pd.DataFrame):
    """Donut chart for customer segment revenue split."""
    seg = df.groupby('segment')['sales'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        seg.values, labels=seg.index, autopct='%1.1f%%',
        colors=COLORS['palette'][:len(seg)],
        startangle=90, pctdistance=0.8,
        wedgeprops=dict(width=0.4, edgecolor='white')
    )
    ax.set_title('Revenue by Customer Segment', fontsize=14, fontweight='bold')
    centre_circle = plt.Circle((0, 0), 0.55, fc='white')
    ax.add_artist(centre_circle)

    # Center text
    ax.text(0, 0, f'${seg.sum():,.0f}\nTotal', ha='center', va='center',
            fontsize=13, fontweight='bold')

    _save_fig(fig, "07_segment_analysis")


# ════════════════════════════════════════════════════════════════
# CHART 8: Shipping Mode Analysis
# ════════════════════════════════════════════════════════════════
def plot_shipping_analysis(df: pd.DataFrame):
    """Bar chart for shipping mode delivery days vs revenue."""
    ship = df.groupby('ship_mode').agg(
        avg_delivery=('delivery_days', 'mean'),
        total_revenue=('sales', 'sum'),
        count=('order_id', 'count')
    ).sort_values('avg_delivery')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Avg delivery days
    ax1.barh(ship.index, ship['avg_delivery'], color=COLORS['palette'][:len(ship)])
    ax1.set_title('Avg Delivery Days by Ship Mode', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Days')
    for i, v in enumerate(ship['avg_delivery']):
        ax1.text(v + 0.1, i, f'{v:.1f} days', va='center', fontsize=10)

    # Revenue by ship mode
    ax2.barh(ship.index, ship['total_revenue'], color=COLORS['palette'][:len(ship)])
    ax2.set_title('Revenue by Ship Mode', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Revenue ($)')
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

    plt.tight_layout()
    _save_fig(fig, "08_shipping_analysis")


# ════════════════════════════════════════════════════════════════
# CHART 9: Year-over-Year Growth
# ════════════════════════════════════════════════════════════════
def plot_yoy_growth(df: pd.DataFrame):
    """Bar chart showing yearly revenue and profit."""
    yearly = df.groupby('order_year').agg(
        revenue=('sales', 'sum'),
        profit=('profit', 'sum'),
        orders=('order_id', 'nunique')
    ).reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(yearly))
    width = 0.35

    bars1 = ax.bar(x - width/2, yearly['revenue'], width,
                   label='Revenue', color=COLORS['primary'])
    bars2 = ax.bar(x + width/2, yearly['profit'], width,
                   label='Profit', color=COLORS['secondary'])

    ax.set_xticks(x)
    ax.set_xticklabels(yearly['order_year'].astype(int))
    ax.set_title('Year-over-Year Revenue & Profit', fontsize=14, fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend()

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                f'${bar.get_height():,.0f}', ha='center', fontsize=8, rotation=0)

    _save_fig(fig, "09_yoy_growth")


# ════════════════════════════════════════════════════════════════
# CHART 10: Correlation Heatmap
# ════════════════════════════════════════════════════════════════
def plot_correlation_heatmap(df: pd.DataFrame):
    """Heatmap of correlations between numeric columns."""
    numeric_cols = ['sales', 'quantity', 'discount', 'profit',
                    'delivery_days', 'profit_margin_pct', 'revenue_per_unit']
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(9, 7))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
                cmap='RdYlGn', center=0, ax=ax,
                linewidths=1, linecolor='white',
                vmin=-1, vmax=1)
    ax.set_title('Feature Correlation Matrix', fontsize=14, fontweight='bold')

    _save_fig(fig, "10_correlation_heatmap")


# ════════════════════════════════════════════════════════════════
# MASTER FUNCTION
# ════════════════════════════════════════════════════════════════
def run_eda(df: pd.DataFrame):
    """Run all EDA visualizations and save to output/ folder."""
    print("\n🎨 Generating Visualizations...")
    print("-" * 50)

    plot_monthly_trend(df)
    plot_category_performance(df)
    plot_subcategory_heatmap(df)
    plot_regional_performance(df)
    plot_discount_vs_profit(df)
    plot_discount_bucket_impact(df)
    plot_segment_analysis(df)
    plot_shipping_analysis(df)
    plot_yoy_growth(df)
    plot_correlation_heatmap(df)

    print("-" * 50)
    print(f"✅ All 10 charts saved to '{OUTPUT_DIR}/' folder.\n")


if __name__ == "__main__":
    from extract_clean import extract_data, clean_data
    df = extract_data("../archive/Sample - Superstore.csv")
    df = clean_data(df)
    run_eda(df)
