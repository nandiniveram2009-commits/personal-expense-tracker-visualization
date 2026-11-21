"""
Automated Report Generator (CSV & Executive Text Summary).
"""

import os
from datetime import datetime
import pandas as pd


def export_reports(
    cleaned_df: pd.DataFrame,
    kpis: dict,
    category_df: pd.DataFrame,
    monthly_df: pd.DataFrame,
    payment_df: pd.DataFrame,
    budget_df: pd.DataFrame,
    outputs_dir: str = "outputs",
    reports_dir: str = "reports"
) -> dict:
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    cleaned_csv = os.path.join(outputs_dir, "cleaned_expenses.csv")
    category_csv = os.path.join(outputs_dir, "category_summary.csv")
    monthly_csv = os.path.join(reports_dir, "monthly_summary.csv")
    text_report = os.path.join(reports_dir, "expense_analysis_report.txt")

    cleaned_df.to_csv(cleaned_csv, index=False)
    category_df.to_csv(category_csv, index=False)
    monthly_df.to_csv(monthly_csv, index=False)

    overspent = budget_df[budget_df["status"] == "OVER BUDGET"]

    lines = [
        "=" * 65,
        "        PERSONAL EXPENSE TRACKER - FINANCIAL REPORT",
        f"        Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 65,
        "",
        "1. EXECUTIVE KPI SUMMARY",
        "-" * 65,
        f"Total Tracked Spending     : ${kpis['total_spending']:,.2f}",
        f"Total Transactions         : {kpis['transaction_count']}",
        f"Average Transaction Size   : ${kpis['avg_transaction']:,.2f}",
        f"Average Daily Spending     : ${kpis['avg_daily_spending']:,.2f}",
        f"Average Monthly Spending   : ${kpis['avg_monthly_spending']:,.2f}",
        f"Highest Spending Category  : {kpis['highest_category']} (${kpis['highest_category_amount']:,.2f})",
        f"Latest Month ({kpis['latest_month']}) Spend: ${kpis['latest_month_spending']:,.2f}",
        "",
        "2. CATEGORY-WISE BREAKDOWN",
        "-" * 65,
        category_df.to_string(index=False),
        "",
        "3. MONTHLY SPENDING TREND",
        "-" * 65,
        monthly_df.to_string(index=False),
        "",
        "4. PAYMENT METHOD DISTRIBUTION",
        "-" * 65,
        payment_df.to_string(index=False),
        "",
        f"5. BUDGET STATUS FOR LATEST MONTH ({kpis['latest_month']})",
        "-" * 65,
        budget_df[["category", "actual_spent", "monthly_limit", "remaining", "status"]].to_string(index=False),
        "",
        "6. ACTIONABLE INSIGHTS & ALERTS",
        "-" * 65,
    ]

    if not overspent.empty:
        for _, row in overspent.iterrows():
            lines.append(
                f"[ALERT] {row['category']} exceeded budget by ${abs(row['remaining']):,.2f} "
                f"(Spent ${row['actual_spent']:,.2f} vs Limit ${row['monthly_limit']:,.2f})."
            )
    else:
        lines.append("[OK] All categories are within monthly budget limits for the latest month.")

    lines.append(
        f"[INSIGHT] Top category '{kpis['highest_category']}' accounts for "
        f"{category_df.iloc[0]['share_pct'] if not category_df.empty else 0}% of total expenses."
    )
    lines.append("=" * 65)

    with open(text_report, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return {
        "cleaned_csv": cleaned_csv,
        "category_csv": category_csv,
        "monthly_csv": monthly_csv,
        "text_report": text_report,
    }