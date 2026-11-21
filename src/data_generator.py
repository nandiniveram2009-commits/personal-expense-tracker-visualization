"""
Synthetic Expense Dataset Generator.
Simulates 6 months of personal finance transactions when banking APIs are unavailable.
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd


def generate_synthetic_expenses(
    output_path: str = "data/synthetic_expenses.csv",
    num_records: int = 320,
    seed: int = 42
) -> pd.DataFrame:
    random.seed(seed)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Templates: (Description, Category, Min Amount, Max Amount)
    expense_templates = [
        ("Swiggy Dinner Order", "Food & Dining", 12.0, 35.0),
        ("Local Supermarket Groceries", "Food & Dining", 25.0, 95.0),
        ("Starbucks Coffee", "Food & Dining", 4.5, 12.0),
        ("Campus Cafeteria Lunch", "Food & Dining", 6.0, 15.0),
        ("Uber Ride to City Center", "Transport", 8.0, 28.0),
        ("Metro Monthly Pass", "Transport", 35.0, 50.0),
        ("Petrol Station Refill", "Transport", 20.0, 60.0),
        ("Apartment Monthly Rent", "Bills & Utilities", 450.0, 450.0),
        ("High-Speed WiFi Bill", "Bills & Utilities", 30.0, 45.0),
        ("Electricity Bill", "Bills & Utilities", 40.0, 85.0),
        ("Mobile Recharge", "Bills & Utilities", 15.0, 25.0),
        ("Amazon Electronics Order", "Shopping", 18.0, 140.0),
        ("Clothes & Footwear Store", "Shopping", 30.0, 120.0),
        ("Netflix Monthly Subscription", "Entertainment", 15.0, 15.0),
        ("Movie Theater Tickets", "Entertainment", 12.0, 32.0),
        ("Spotify Premium", "Entertainment", 10.0, 10.0),
        ("Pharmacy Medicines", "Health & Fitness", 10.0, 45.0),
        ("Monthly Gym Membership", "Health & Fitness", 30.0, 40.0),
        ("Udemy Python Course", "Education", 12.0, 25.0),
        ("Technical Books & Stationery", "Education", 15.0, 55.0),
    ]

    payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
    payment_weights = [0.40, 0.25, 0.20, 0.10, 0.05]

    end_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=180)

    records = []
    for i in range(num_records):
        random_days = random.randint(0, 180)
        tx_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        desc, cat, min_amt, max_amt = random.choice(expense_templates)
        amount = round(random.uniform(min_amt, max_amt), 2)
        pay_method = random.choices(payment_methods, weights=payment_weights, k=1)[0]

        # Intentionally leave ~15% categories blank to test auto-categorization
        if i % 7 == 0:
            cat = ""

        records.append({
            "date": tx_date,
            "description": desc,
            "category": cat,
            "amount": amount,
            "payment_method": pay_method
        })

    # Add fixed monthly rent on the 1st of each month over the last 6 months
    for m_offset in range(6):
        first_of_month = (end_date.replace(day=1) - pd.DateOffset(months=m_offset)).strftime("%Y-%m-%d")
        records.append({
            "date": first_of_month,
            "description": "Apartment Monthly Rent",
            "category": "Bills & Utilities",
            "amount": 450.00,
            "payment_method": "Net Banking"
        })

    df = pd.DataFrame(records).sort_values("date").reset_index(drop=True)
    df.to_csv(output_path, index=False)
    return df