"""
Data Cleaning and Financial Analytics Engine.
"""

import numpy as np
import pandas as pd


def clean_expense_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw expense data:
    - Converts date column to datetime
    - Drops invalid dates or non-positive amounts
    - Adds 'month' (YYYY-MM) and 'day_name' helper columns
    """
    if df.empty:
        return df

    cleaned = df.copy()
    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
    cleaned["amount"] = pd.to_numeric(cleaned["amount"], errors="coerce")
    cleaned = cleaned.dropna(subset=["date", "amount"])
    cleaned = cleaned[cleaned["amount"] > 0].copy()

    cleaned["category"] = cleaned["category"].fillna("Other").astype(str).str.strip()
    cleaned["payment_method"] = cleaned["payment_method"].fillna("Cash").astype(str).str.strip()
    cleaned["description"] = cleaned["description"].fillna("Expense").astype(str).str.strip()

    cleaned["month"] = cleaned["date"].dt.to_period("M").astype(str)
    cleaned["day_name"] = cleaned["date"].dt.day_name()

    return cleaned.sort_values("date").reset_index(drop=True)


def compute_kpis(df: pd.DataFrame) -> dict:
    """Calculates core financial summary metrics."""
    if df.empty:
        return {
            "total_spending": 0.0,
            "transaction_count": 0,
            "avg_transaction": 0.0,
            "avg_daily_spending": 0.0,
            "avg_monthly_spending": 0.0,
            "highest_category": "N/A",
            "highest_category_amount": 0.0,
            "latest_month": "N/A",
            "latest_month_spending": 0.0,
        }

    total_spending = float(df["amount"].sum())
    date_span_days = max((df["date"].max() - df["date"].min()).days + 1, 1)
    avg_daily_spending = total_spending / date_span_days

    cat_totals = df.groupby("category")["amount"].sum()
    highest_category = cat_totals.idxmax()
    highest_category_amount = float(cat_totals.max())

    monthly_totals = df.groupby("month")["amount"].sum().sort_index()
    latest_month = monthly_totals.index[-1]
    latest_month_spending = float(monthly_totals.iloc[-1])

    return {
        "total_spending": round(total_spending, 2),
        "transaction_count": int(len(df)),
        "avg_transaction": round(float(df["amount"].mean()), 2),
        "avg_daily_spending": round(avg_daily_spending, 2),
        "avg_monthly_spending": round(float(monthly_totals.mean()), 2),
        "highest_category": highest_category,
        "highest_category_amount": round(highest_category_amount, 2),
        "latest_month": latest_month,
        "latest_month_spending": round(latest_month_spending, 2),
    }


def analyze_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Groups expenses by category with total, count, average, and share %."""
    if df.empty:
        return pd.DataFrame(columns=["category", "total_amount", "tx_count", "avg_amount", "share_pct"])

    summary = (
        df.groupby("category", as_index=False)
        .agg(
            total_amount=("amount", "sum"),
            tx_count=("amount", "count"),
            avg_amount=("amount", "mean"),
        )
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
    total = summary["total_amount"].sum()
    summary["share_pct"] = np.round((summary["total_amount"] / total) * 100, 2)
    summary["total_amount"] = summary["total_amount"].round(2)
    summary["avg_amount"] = summary["avg_amount"].round(2)
    return summary


def analyze_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Computes chronological monthly spending and Month-over-Month % change."""
    if df.empty:
        return pd.DataFrame(columns=["month", "total_amount", "tx_count", "mom_change_pct"])

    monthly = (
        df.groupby("month", as_index=False)
        .agg(total_amount=("amount", "sum"), tx_count=("amount", "count"))
        .sort_values("month")
        .reset_index(drop=True)
    )
    monthly["total_amount"] = monthly["total_amount"].round(2)
    monthly["mom_change_pct"] = (monthly["total_amount"].pct_change() * 100).round(2).fillna(0.0)
    return monthly


def analyze_payment_methods(df: pd.DataFrame) -> pd.DataFrame:
    """Analyzes spending distribution across payment methods."""
    if df.empty:
        return pd.DataFrame(columns=["payment_method", "total_amount", "tx_count", "share_pct"])

    pay_df = (
        df.groupby("payment_method", as_index=False)
        .agg(total_amount=("amount", "sum"), tx_count=("amount", "count"))
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
    total = pay_df["total_amount"].sum()
    pay_df["share_pct"] = np.round((pay_df["total_amount"] / total) * 100, 2)
    pay_df["total_amount"] = pay_df["total_amount"].round(2)
    return pay_df


def analyze_daily_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates daily spending and computes a 7-day rolling average."""
    if df.empty:
        return pd.DataFrame(columns=["date", "daily_amount", "rolling_7d_avg"])

    daily = (
        df.groupby("date", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "daily_amount"})
        .sort_values("date")
        .reset_index(drop=True)
    )
    daily["rolling_7d_avg"] = daily["daily_amount"].rolling(window=7, min_periods=1).mean().round(2)
    daily["daily_amount"] = daily["daily_amount"].round(2)
    return daily


def check_monthly_budget_status(
    df: pd.DataFrame, budgets_df: pd.DataFrame, target_month: str = None
) -> pd.DataFrame:
    """Compares actual category spending for a given month against budget limits."""
    if df.empty:
        return pd.DataFrame(columns=["category", "actual_spent", "monthly_limit", "remaining", "status"])

    if not target_month:
        target_month = sorted(df["month"].unique())[-1]

    month_df = df[df["month"] == target_month]
    actuals = month_df.groupby("category", as_index=False)["amount"].sum().rename(
        columns={"amount": "actual_spent"}
    )

    merged = pd.merge(budgets_df, actuals, on="category", how="outer").fillna(0.0)
    merged["monthly_limit"] = merged["monthly_limit"].replace(0.0, 100.0)
    merged["actual_spent"] = merged["actual_spent"].round(2)
    merged["remaining"] = (merged["monthly_limit"] - merged["actual_spent"]).round(2)
    merged["utilization_pct"] = ((merged["actual_spent"] / merged["monthly_limit"]) * 100).round(1)
    merged["status"] = np.where(
        merged["actual_spent"] > merged["monthly_limit"],
        "OVER BUDGET",
        np.where(merged["utilization_pct"] >= 80, "WARNING (80%+)", "ON TRACK")
    )
    return merged.sort_values("utilization_pct", ascending=False).reset_index(drop=True)