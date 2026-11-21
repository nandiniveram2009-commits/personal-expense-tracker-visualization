"""
SQLite Database Manager for Personal Expense Tracker.
"""

import os
import sqlite3
import pandas as pd
from src.categorizer import auto_categorize

DEFAULT_DB_PATH = "data/expenses.db"

DEFAULT_BUDGETS = {
    "Food & Dining": 450.0,
    "Transport": 200.0,
    "Bills & Utilities": 650.0,
    "Shopping": 250.0,
    "Entertainment": 100.0,
    "Health & Fitness": 120.0,
    "Education": 120.0,
    "Other": 100.0,
}


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """Creates transactions and budgets tables if they do not exist."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, description, amount, payment_method)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                monthly_limit REAL NOT NULL
            )
        """)
        for cat, limit in DEFAULT_BUDGETS.items():
            cursor.execute(
                "INSERT OR IGNORE INTO budgets (category, monthly_limit) VALUES (?, ?)",
                (cat, limit)
            )
        conn.commit()


def insert_dataframe(df: pd.DataFrame, db_path: str = DEFAULT_DB_PATH) -> int:
    """Cleans, auto-categorizes, and inserts a DataFrame into SQLite without duplicates."""
    init_db(db_path)
    inserted_count = 0

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        for _, row in df.iterrows():
            date_val = str(row.get("date", "")).strip()
            desc_val = str(row.get("description", "Unknown Expense")).strip()
            cat_val = auto_categorize(desc_val, row.get("category", ""))
            try:
                amt_val = float(row.get("amount", 0))
            except (ValueError, TypeError):
                continue
            pay_val = str(row.get("payment_method", "Cash")).strip() or "Cash"

            if not date_val or amt_val <= 0:
                continue

            cursor.execute("""
                INSERT OR IGNORE INTO transactions (date, description, category, amount, payment_method)
                VALUES (?, ?, ?, ?, ?)
            """, (date_val, desc_val, cat_val, round(amt_val, 2), pay_val))
            inserted_count += cursor.rowcount
        conn.commit()

    return inserted_count


def add_single_transaction(
    date: str,
    description: str,
    amount: float,
    payment_method: str,
    category: str = "",
    db_path: str = DEFAULT_DB_PATH
) -> str:
    """Inserts a single manual expense and returns the assigned category."""
    init_db(db_path)
    assigned_cat = auto_categorize(description, category)

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO transactions (date, description, category, amount, payment_method)
            VALUES (?, ?, ?, ?, ?)
        """, (date, description.strip(), assigned_cat, round(float(amount), 2), payment_method.strip()))
        conn.commit()

    return assigned_cat


def fetch_all_transactions(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Loads all transactions from SQLite into a Pandas DataFrame."""
    init_db(db_path)
    with get_connection(db_path) as conn:
        df = pd.read_sql_query(
            "SELECT id, date, description, category, amount, payment_method FROM transactions ORDER BY date ASC",
            conn
        )
    return df


def fetch_budgets(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Loads monthly category budgets from SQLite."""
    init_db(db_path)
    with get_connection(db_path) as conn:
        return pd.read_sql_query("SELECT category, monthly_limit FROM budgets", conn)


def update_budget(category: str, monthly_limit: float, db_path: str = DEFAULT_DB_PATH) -> None:
    """Updates or inserts a monthly budget limit for a category."""
    init_db(db_path)
    with get_connection(db_path) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO budgets (category, monthly_limit) VALUES (?, ?)",
            (category, float(monthly_limit))
        )
        conn.commit()