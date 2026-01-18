import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv("dirty_cafe_sales.csv")

# Clean column names
data.columns = (
    data.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Remove duplicates
data = data.drop_duplicates()

# Replace error values with NaN
data = data.replace(["UNKNOWN", "ERROR"], np.nan)

# Clean item column
data["item"] = data["item"].str.replace("#", "", regex=False)
data["item"] = data["item"].fillna("miscellaneous")

# Convert numeric columns
data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce").fillna(0)
data["price_per_unit"] = pd.to_numeric(data["price_per_unit"], errors="coerce").fillna(0)
data["total_spent"] = pd.to_numeric(data["total_spent"], errors="coerce")

# Calculate total_spent where missing
data["total_spent"] = data["total_spent"].fillna(
    data["quantity"] * data["price_per_unit"]
)

# Handle missing categorical values
data["payment_method"] = data["payment_method"].fillna("Unknown")
data["location"] = data["location"].fillna("Unknown")

# Date formatting
data["transaction_date"] = pd.to_datetime(
    data["transaction_date"], errors="coerce", dayfirst=True
)

# ------------------ Analysis & Visualizations ------------------

# Item-wise sales
item_sales = data.groupby("item")["total_spent"].sum().sort_values(ascending=False)
item_sales.plot(kind="bar", figsize=(8,4))
plt.title("Total Revenue by Item")
plt.xlabel("Item")
plt.ylabel("Total Revenue")
plt.show()

# Payment method distribution
payment_counts = data["payment_method"].value_counts()
payment_counts.plot(kind="pie", autopct="%1.1f%%", figsize=(6,6))
plt.title("Payment Method Distribution")
plt.ylabel("")
plt.show()

# Location-wise sales
location_sales = data.groupby("location")["total_spent"].sum()
location_sales.plot(kind="bar", figsize=(6,4))
plt.title("Total Revenue by Location")
plt.xlabel("Location")
plt.ylabel("Total Revenue")
plt.show()

# Daily sales trend
daily_sales = data.groupby("transaction_date")["total_spent"].sum()
daily_sales.plot(figsize=(10,4))
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.show()
