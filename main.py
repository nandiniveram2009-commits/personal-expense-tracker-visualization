"""
Master CLI Pipeline for Personal Expense Tracker with Data Visualization.
Runs: Synthetic Data Creation -> SQLite Storage -> Cleaning -> Analysis -> Charts -> Reports.
"""

import os
from src.data_generator import generate_synthetic_expenses
from src.database import insert_dataframe, fetch_all_transactions, fetch_budgets
from src.analyzer import (
    clean_expense_data,
    compute_kpis,
    analyze_by_category,
    analyze_monthly_trend,
    analyze_payment_methods,
    analyze_daily_trend,
    check_monthly_budget_status,
)
from src.visualizer import generate_all_charts
from src.report_generator import export_reports


def run_pipeline():
    print("\n[1/6] Generating synthetic expense dataset...")
    csv_path = "data/synthetic_expenses.csv"
    if not os.path.exists(csv_path):
        raw_df = generate_synthetic_expenses(csv_path)
        print(f"      Created {len(raw_df)} synthetic records at {csv_path}")
    else:
        import pandas as pd
        raw_df = pd.read_csv(csv_path)
        print(f"      Loaded existing dataset ({len(raw_df)} rows) from {csv_path}")

    print("[2/6] Auto-categorizing & storing records in SQLite (data/expenses.db)...")
    inserted = insert_dataframe(raw_df)
    print(f"      Inserted {inserted} new records into SQLite.")

    print("[3/6] Fetching & cleaning data from SQLite...")
    db_df = fetch_all_transactions()
    budgets_df = fetch_budgets()
    cleaned_df = clean_expense_data(db_df)
    print(f"      Clean dataset ready: {len(cleaned_df)} valid transactions.")

    print("[4/6] Running financial & trend analysis...")
    kpis = compute_kpis(cleaned_df)
    category_df = analyze_by_category(cleaned_df)
    monthly_df = analyze_monthly_trend(cleaned_df)
    payment_df = analyze_payment_methods(cleaned_df)
    daily_df = analyze_daily_trend(cleaned_df)
    budget_status_df = check_monthly_budget_status(cleaned_df, budgets_df)

    print("[5/6] Generating visualization charts in images/...")
    chart_paths = generate_all_charts(category_df, monthly_df, payment_df, daily_df)
    for path in chart_paths:
        print(f"      Saved chart: {path}")

    print("[6/6] Exporting CSV & TXT monthly reports...")
    report_paths = export_reports(
        cleaned_df, kpis, category_df, monthly_df, payment_df, budget_status_df
    )
    for key, path in report_paths.items():
        print(f"      Exported {key}: {path}")

    print("\n--- QUICK INSIGHT SUMMARY ---")
    print(f"Total Spending           : ${kpis['total_spending']:,.2f}")
    print(f"Average Daily Spending   : ${kpis['avg_daily_spending']:,.2f}")
    print(f"Highest Spending Category: {kpis['highest_category']} (${kpis['highest_category_amount']:,.2f})")
    print(f"Latest Month ({kpis['latest_month']})  : ${kpis['latest_month_spending']:,.2f}")
    print("Pipeline completed successfully! Run `streamlit run app.py` to launch the dashboard.\n")


if __name__ == "__main__":
    run_pipeline()