"""
Data Visualization Module using Matplotlib and Seaborn.
Generates 4 analytical charts and saves them to images/.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid", palette="muted")


def plot_category_bar(category_df: pd.DataFrame, output_dir: str = "images"):
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))

    sns.barplot(
        data=category_df,
        x="total_amount",
        y="category",
        hue="category",
        palette="viridis",
        legend=False,
        ax=ax
    )
    ax.set_title("Category-wise Total Spending", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Total Amount ($)", fontsize=11)
    ax.set_ylabel("Expense Category", fontsize=11)

    for container in ax.containers:
        ax.bar_label(container, fmt=" $%.2f", padding=3, fontsize=9)

    ax.set_xlim(0, category_df["total_amount"].max() * 1.18 if not category_df.empty else 100)
    plt.tight_layout()
    path = os.path.join(output_dir, "category_spending_bar.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path


def plot_monthly_trend_line(monthly_df: pd.DataFrame, output_dir: str = "images"):
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=monthly_df,
        x="month",
        y="total_amount",
        marker="o",
        linewidth=2.5,
        color="#2563EB",
        ax=ax
    )
    ax.fill_between(monthly_df["month"], monthly_df["total_amount"], alpha=0.12, color="#2563EB")
    ax.set_title("Monthly Spending Trend", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Month (YYYY-MM)", fontsize=11)
    ax.set_ylabel("Total Spending ($)", fontsize=11)

    for idx, row in monthly_df.iterrows():
        ax.annotate(
            f"${row['total_amount']:,.0f}",
            (row["month"], row["total_amount"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
            fontweight="bold"
        )

    plt.xticks(rotation=30)
    plt.tight_layout()
    path = os.path.join(output_dir, "monthly_spending_line.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path


def plot_payment_method_pie(payment_df: pd.DataFrame, output_dir: str = "images"):
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = sns.color_palette("Set2", len(payment_df))
    wedges, texts, autotexts = ax.pie(
        payment_df["total_amount"],
        labels=payment_df["payment_method"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        pctdistance=0.78,
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    # Draw center circle for a modern donut look
    centre_circle = plt.Circle((0, 0), 0.52, fc="white")
    ax.add_artist(centre_circle)

    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight("bold")

    ax.set_title("Spending Share by Payment Method", fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    path = os.path.join(output_dir, "payment_method_pie.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path


def plot_daily_spending_trend(daily_df: pd.DataFrame, output_dir: str = "images"):
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 5))

    ax.plot(daily_df["date"], daily_df["daily_amount"], alpha=0.4, color="#64748B", label="Daily Spend")
    ax.plot(
        daily_df["date"],
        daily_df["rolling_7d_avg"],
        color="#DC2626",
        linewidth=2.2,
        label="7-Day Rolling Average"
    )
    ax.set_title("Daily Spending Trend & 7-Day Rolling Average", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Amount ($)", fontsize=11)
    ax.legend()

    plt.xticks(rotation=30)
    plt.tight_layout()
    path = os.path.join(output_dir, "daily_spending_trend.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path


def generate_all_charts(category_df, monthly_df, payment_df, daily_df, output_dir="images") -> list:
    """Generates all 4 charts and returns their saved file paths."""
    return [
        plot_category_bar(category_df, output_dir),
        plot_monthly_trend_line(monthly_df, output_dir),
        plot_payment_method_pie(payment_df, output_dir),
        plot_daily_spending_trend(daily_df, output_dir),
    ]