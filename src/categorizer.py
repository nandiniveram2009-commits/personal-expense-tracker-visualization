"""
Rule-based Auto-Categorizer for Expense Descriptions.
"""

CATEGORY_RULES = {
    "Food & Dining": [
        "swiggy", "zomato", "starbucks", "cafe", "restaurant", "pizza",
        "burger", "coffee", "grocery", "supermarket", "bakery", "lunch", "dinner"
    ],
    "Transport": [
        "uber", "ola", "lyft", "metro", "bus", "train", "fuel", "petrol",
        "diesel", "parking", "flight", "cab", "auto"
    ],
    "Bills & Utilities": [
        "electricity", "water", "wifi", "internet", "broadband", "mobile",
        "recharge", "rent", "gas", "bill", "insurance"
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "mall", "clothes", "shoes",
        "electronics", "ikea", "target", "walmart"
    ],
    "Entertainment": [
        "netflix", "spotify", "movie", "cinema", "prime", "gaming",
        "concert", "hotstar", "youtube"
    ],
    "Health & Fitness": [
        "pharmacy", "medicine", "doctor", "hospital", "gym", "clinic",
        "dental", "fitness", "vitamin"
    ],
    "Education": [
        "udemy", "coursera", "books", "tuition", "exam", "stationery",
        "course", "notebook"
    ]
}


def auto_categorize(description: str, existing_category: str = None) -> str:
    """
    Assigns a standardized category based on description keywords.
    Preserves valid existing categories if already provided.
    """
    if existing_category and str(existing_category).strip() not in ("", "nan", "None", "Uncategorized"):
        return str(existing_category).strip()

    desc_lower = str(description).lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(keyword in desc_lower for keyword in keywords):
            return category

    return "Other"