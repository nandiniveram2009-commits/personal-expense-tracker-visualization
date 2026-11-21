"""
Interactive Streamlit Dashboard for Personal Expense Tracker.
Run with: streamlit run app.py
"""

from datetime import date
import pandas as pd
import streamlit as st

from src.database import (
    fetch_all_transactions,
    fetch_budgets,
    add_single_transaction,
    insert_dataframe,
    update_budget,
)
from src.analyzer import (
    clean_expense_data,
    compute_kpis,
    analyze_by_category,
    analyze_monthly_trend,
    analyze_payment_methods,
    analyze_daily_trend,
    check_monthly_budget_status,
)
from src.visualizer import (
    plot_category_bar,
    plot_monthly_trend_line,
    plot_payment_method_pie,
    plot_daily_spending_trend,
)

st.set_page_config(page_title="Personal Expense Tracker", page_icon="💰", layout="wide")

st.title("💰 Personal Expense Tracker & Analytics Dashboard")
st.caption("SQLite-backed expense ingestion, rule-based auto-categorization, budget alerts, and visual insights.")

# --- SIDEBAR: DATA INGESTION & FILTERS ---
st.sidebar.header("➕ Add Manual Expense")
with st.sidebar.form("manual_expense_form", clear_on_submit=True):
    tx_date = st.date_input("Date", value=date.today())
    tx_desc = st.text_input("Description", placeholder="e.g., Starbucks Coffee")
    tx_cat = st.selectbox(
        "Category (Auto-detect if blank)",
        ["", "Food & Dining", "Transport", "Bills & Utilities", "Shopping", "Entertainment", "Health & Fitness", "Education", "Other"]
    )
    tx_amt = st.number_input("Amount ($)", min_value=0.01, step=1.0, format="%.2f")
    tx_pay = st.selectbox("Payment Method", ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"])
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if tx_desc.strip():
            assigned = add_single_transaction(str(tx_date), tx_desc, tx_amt, tx_pay, tx_cat)
            st.sidebar.success(f"Added under '{assigned}'!")
        else:
            st.sidebar.error("Please enter a description.")

st.sidebar.header("📂 Upload CSV Transactions")
uploaded_file = st.sidebar.file_uploader("Upload CSV (date, description, amount, payment_method)", type=["csv"])
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
    count = insert_dataframe(uploaded_df)
    st.sidebar.success(f"Imported {count} new transactions into SQLite!")

# --- LOAD & CLEAN DATA ---
raw_df = fetch_all_transactions()
cleaned_df = clean_expense_data(raw_df)
budgets_df = fetch_budgets()

if cleaned_df.empty:
    st.warning("No transactions found in database. Run `python main.py` first or add expenses from the sidebar.")
    st.stop()

# Month Filter
all_months = sorted(cleaned_df["month"].unique())
selected_months = st.sidebar.multiselect("Filter by Month", options=all_months, default=all_months)
filtered_df = cleaned_df[cleaned_df["month"].isin(selected_months)] if selected_months else cleaned_df

# --- ANALYTICS ---
kpis = compute_kpis(filtered_df)
category_df = analyze_by_category(filtered_df)
monthly_df = analyze_monthly_trend(filtered_df)
payment_df = analyze_payment_methods(filtered_df)
daily_df = analyze_daily_trend(filtered_df)

# --- KPI CARDS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spending", f"${kpis['total_spending']:,.2f}")
col2.metric("Avg Daily Spend", f"${kpis['avg_daily_spending']:,.2f}")
col3.metric("Top Category", kpis["highest_category"], f"${kpis['highest_category_amount']:,.2f}")
col4.metric("Transactions", kpis["transaction_count"], f"Avg ${kpis['avg_transaction']:,.2f}")

st.divider()

# --- CHARTS ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("Category-wise Spending")
    st.image(plot_category_bar(category_df), use_container_width=True)
with c2:
    st.subheader("Monthly Spending Trend")
    st.image(plot_monthly_trend_line(monthly_df), use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.subheader("Payment Method Split")
    st.image(plot_payment_method_pie(payment_df), use_container_width=True)
with c4:
    st.subheader("Daily Spend & 7-Day Rolling Avg")
    st.image(plot_daily_spending_trend(daily_df), use_container_width=True)

st.divider()

# --- BUDGET TRACKER ---
st.subheader("🎯 Monthly Budget vs Actuals")
target_month = st.selectbox("Select Month for Budget Check", options=all_months, index=len(all_months) - 1)
budget_status_df = check_monthly_budget_status(cleaned_df, budgets_df, target_month)
st.dataframe(budget_status_df, use_container_width=True)

with st.expander("⚙️ Adjust Monthly Category Budgets"):
    b_cat = st.selectbox("Category", budgets_df["category"].tolist())
    b_limit = st.number_input("New Monthly Limit ($)", min_value=10.0, value=200.0, step=10.0)
    if st.button("Update Budget"):
        update_budget(b_cat, b_limit)
        st.success(f"Updated {b_cat} budget to ${b_limit:,.2f}. Refresh to view changes.")

# --- RAW TABLE & EXPORT ---
st.subheader("📋 Recent Cleaned Transactions")
st.dataframe(filtered_df.sort_values("date", ascending=False).head(50), use_container_width=True)

csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Filtered Transactions (CSV)",
    data=csv_bytes,
    file_name="filtered_expenses.csv",
    mime="text/csv"
)