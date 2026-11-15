
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Reproducible dataset
random.seed(42)

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "sales_data.csv"

# Product catalog
products = {
    "Laptop": ("Electronics", 800),
    "Mouse": ("Accessories", 20),
    "Keyboard": ("Accessories", 50),
    "Monitor": ("Electronics", 200),
    "Headphones": ("Electronics", 100),
    "Desk": ("Furniture", 250),
    "Chair": ("Furniture", 150),
    "Notebook": ("Stationery", 5),
    "Pen": ("Stationery", 2),
    "Webcam": ("Electronics", 75),
}

regions = ["North", "South", "East", "West"]

statuses = ["Completed", "Pending", "Cancelled"]
status_weights = [0.75, 0.15, 0.10]

start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 10, 29)
date_range = (end_date - start_date).days

# Generate 1000 orders
rows = []

for order_id in range(1001, 2001):

    order_date = start_date + timedelta(
        days=random.randint(0, date_range)
    )

    product = random.choice(list(products.keys()))
    category, base_price = products[product]

    quantity = random.randint(1, 5)
    unit_price = round(
        base_price * random.uniform(0.9, 1.1), 2
    )

    revenue = round(quantity * unit_price, 2)

    rows.append({
        "OrderID": order_id,
        "OrderDate": order_date.strftime("%Y-%m-%d"),
        "CustomerID": f"C{random.randint(1, 250):04d}",
        "Product": product,
        "Category": category,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "Revenue": revenue,
        "Region": random.choice(regions),
        "Status": random.choices(
            statuses, weights=status_weights, k=1
        )[0]
    })

# Save CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:

    fieldnames = [
        "OrderID", "OrderDate", "CustomerID",
        "Product", "Category", "Quantity",
        "UnitPrice", "Revenue", "Region", "Status"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Dataset created successfully!")
print(f"File location: {OUTPUT_FILE}")
print(f"Total records: {len(rows)}")