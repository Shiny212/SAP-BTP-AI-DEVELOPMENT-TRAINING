# ==========================================
# Import Required Libraries
# ==========================================

import sqlite3
import pandas as pd
# ==========================================
# Create Database Connection
# ==========================================

conn = sqlite3.connect("retail_sales.db")
cursor = conn.cursor()

print("Database Created Successfully.")

# ==========================================
# Create Customers Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT,
    city TEXT,
    age INTEGER,
    gender TEXT
)
""")

print("Customers Table Created Successfully.")


# ==========================================
# Create Products Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
)
""")

print("Products Table Created Successfully.")


# ==========================================
# Create Orders Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    product_id TEXT,
    order_date TEXT,
    quantity INTEGER,
    sales_channel TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

print("Orders Table Created Successfully.")

# Save changes
conn.commit()

print("All Tables Created Successfully.")


# ==========================================
# Insert Data into Customers Table
# ==========================================

customers = [
    ("C001", "Rahul Sharma", "Patna", 32, "Male"),
    ("C002", "Priya Singh", "Delhi", 28, "Female"),
    ("C003", "Amit Kumar", "Kolkata", 35, "Male"),
    ("C004", "Sneha Verma", "Pune", 30, "Female"),
    ("C005", "Rohit Raj", "Patna", 40, "Male"),
    ("C006", "Neha Gupta", "Delhi", 26, "Female"),
    ("C007", "Ankit Sinha", "Mumbai", 38, "Male"),
    ("C008", "Riya Das", "Kolkata", 24, "Female")
]

cursor.executemany("""
INSERT OR REPLACE INTO customers
VALUES (?, ?, ?, ?, ?)
""", customers)

print("Customers data inserted successfully.")



# ==========================================
# Insert Data into Products Table
# ==========================================

products = [
    ("P001", "Laptop", "Electronics", 55000),
    ("P002", "Mobile Phone", "Electronics", 25000),
    ("P003", "Office Chair", "Furniture", 7000),
    ("P004", "Headphones", "Electronics", 3000),
    ("P005", "Study Table", "Furniture", 12000),
    ("P006", "Shoes", "Fashion", 4000),
    ("P007", "Backpack", "Fashion", 2500)
]

cursor.executemany("""
INSERT OR REPLACE INTO products
VALUES (?, ?, ?, ?)
""", products)

print("Products data inserted successfully.")



# ==========================================
# Insert Data into Orders Table
# ==========================================

orders = [
    ("O001", "C001", "P002", "2026-01-10", 2, "Online"),
    ("O002", "C002", "P001", "2026-01-15", 1, "Offline"),
    ("O003", "C003", "P004", "2026-02-05", 3, "Online"),
    ("O004", "C004", "P003", "2026-02-12", 2, "Offline"),
    ("O005", "C005", "P006", "2026-03-01", 4, "Online"),
    ("O006", "C001", "P004", "2026-03-08", 2, "Online"),
    ("O007", "C006", "P005", "2026-03-18", 1, "Offline"),
    ("O008", "C007", "P001", "2026-04-02", 1, "Online"),
    ("O009", "C008", "P007", "2026-04-10", 5, "Online"),
    ("O010", "C003", "P002", "2026-04-22", 1, "Offline"),
    ("O011", "C005", "P003", "2026-05-05", 1, "Offline"),
    ("O012", "C002", "P004", "2026-05-15", 4, "Online")
]

cursor.executemany("""
INSERT OR REPLACE INTO orders
VALUES (?, ?, ?, ?, ?, ?)
""", orders)

print("Orders data inserted successfully.")

# Save changes
conn.commit()

print("All data inserted successfully.")



# ==========================================
# SQL Task 3: View All Orders
# ==========================================

print("\nSQL Task 3: View All Orders")
print("----------------------------------")

query = """
SELECT
    o.order_id,
    c.customer_name,
    c.city,
    p.product_name,
    p.category,
    o.quantity,
    p.price,
    (o.quantity * p.price) AS total_amount,
    o.sales_channel,
    o.order_date
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
JOIN products p
ON o.product_id = p.product_id
ORDER BY o.order_date;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)



    # ==========================================
# SQL Task 4: Find Total Revenue
# ==========================================

print("\nSQL Task 4: Total Revenue")
print("----------------------------------")

query = """
SELECT
    SUM(o.quantity * p.price) AS total_revenue
FROM orders o
JOIN products p
ON o.product_id = p.product_id;
"""

cursor.execute(query)

result = cursor.fetchone()

print("Total Revenue: ₹", result[0])



# ==========================================
# SQL Task 5: Revenue by City
# ==========================================

print("\nSQL Task 5: Revenue by City")
print("----------------------------------")

query = """
SELECT
    c.city,
    SUM(o.quantity * p.price) AS total_revenue
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
JOIN products p
ON o.product_id = p.product_id
GROUP BY c.city
ORDER BY total_revenue DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

print("City\t\tTotal Revenue")
print("-" * 35)

for row in rows:
    print(f"{row[0]}\t\t₹{row[1]}")



    # ==========================================
# SQL Task 6: Best-Selling Product
# ==========================================

print("\nSQL Task 6: Best-Selling Product")
print("----------------------------------")

query = """
SELECT
    p.product_name,
    SUM(o.quantity) AS total_quantity_sold
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_quantity_sold DESC
LIMIT 1;
"""

cursor.execute(query)

result = cursor.fetchone()

print("Best-Selling Product :", result[0])
print("Total Quantity Sold  :", result[1])



# ==========================================
# SQL Task 7: Category-wise Revenue
# ==========================================

print("\nSQL Task 7: Category-wise Revenue")
print("----------------------------------")

query = """
SELECT
    p.category,
    SUM(o.quantity * p.price) AS total_revenue
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

print("Category\t\tRevenue")
print("-" * 40)

for row in rows:
    print(f"{row[0]}\t\t₹{row[1]}")



    # ==========================================
# SQL Task 8: Online vs Offline Sales
# ==========================================

print("\nSQL Task 8: Online vs Offline Sales")
print("----------------------------------")

query = """
SELECT
    o.sales_channel,
    SUM(o.quantity * p.price) AS total_revenue
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY o.sales_channel
ORDER BY total_revenue DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

print("Sales Channel\tRevenue")
print("-" * 35)

for row in rows:
    print(f"{row[0]}\t\t₹{row[1]}")



    # ==========================================
# SQL Task 9: Monthly Revenue Trend
# ==========================================

print("\nSQL Task 9: Monthly Revenue Trend")
print("----------------------------------")

query = """
SELECT
    strftime('%Y-%m', o.order_date) AS month,
    SUM(o.quantity * p.price) AS total_revenue
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY month
ORDER BY month;
"""

cursor.execute(query)

rows = cursor.fetchall()

print("Month\t\tRevenue")
print("-" * 35)

for row in rows:
    print(f"{row[0]}\t₹{row[1]}")



    # ==========================================
# SQL Task 10: High-Value Customers
# ==========================================

print("\nSQL Task 10: High-Value Customers")
print("----------------------------------")

query = """
SELECT
    c.customer_name,
    c.city,
    SUM(o.quantity * p.price) AS total_purchase_value
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
JOIN products p
ON o.product_id = p.product_id
GROUP BY c.customer_id, c.customer_name, c.city
HAVING SUM(o.quantity * p.price) > 50000
ORDER BY total_purchase_value DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

print("Customer Name\t\tCity\t\tTotal Purchase Value")
print("-" * 70)

for row in rows:
    print(f"{row[0]}\t{row[1]}\t\t₹{row[2]}")





    # ==========================================
# Pandas Task 1: Create DataFrames
# ==========================================

print("\nPandas Task 1: Create DataFrames")
print("----------------------------------")

# Read Customers Table
customers_df = pd.read_sql_query(
    "SELECT * FROM customers",
    conn
)

# Read Products Table
products_df = pd.read_sql_query(
    "SELECT * FROM products",
    conn
)

# Read Orders Table
orders_df = pd.read_sql_query(
    "SELECT * FROM orders",
    conn
)

print("\nCustomers DataFrame")
print(customers_df)

print("\nProducts DataFrame")
print(products_df)

print("\nOrders DataFrame")
print(orders_df)



# ==========================================
# Pandas Task 2: Merge DataFrames
# ==========================================

print("\nPandas Task 2: Merge DataFrames")
print("----------------------------------")

# Merge Customers and Orders
sales_df = pd.merge(
    customers_df,
    orders_df,
    on="customer_id"
)

# Merge with Products
sales_df = pd.merge(
    sales_df,
    products_df,
    on="product_id"
)

print("\nMerged Sales DataFrame")
print(sales_df)



# ==========================================
# Pandas Task 3: Create Total Amount Column
# ==========================================

print("\nPandas Task 3: Create Total Amount Column")
print("----------------------------------")

# Create Total Amount column
sales_df["total_amount"] = sales_df["quantity"] * sales_df["price"]

# Display the updated DataFrame
print(sales_df)



# ==========================================
# Pandas Task 4: Calculate Total Revenue
# ==========================================

print("\nPandas Task 4: Calculate Total Revenue")
print("----------------------------------")

# Calculate total revenue
total_revenue = sales_df["total_amount"].sum()

print("Total Revenue: ₹", total_revenue)



# ==========================================
# Pandas Task 5: Revenue by City
# ==========================================

print("\nPandas Task 5: Revenue by City")
print("----------------------------------")

# Revenue by City
city_revenue = (
    sales_df
    .groupby("city")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(city_revenue)



# ==========================================
# Pandas Task 6: Product-wise Quantity Sold
# ==========================================

print("\nPandas Task 6: Product-wise Quantity Sold")
print("----------------------------------")

# Product-wise Quantity Sold
product_quantity = (
    sales_df
    .groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
)

print(product_quantity)



# ==========================================
# Pandas Task 7: Category-wise Revenue
# ==========================================

print("\nPandas Task 7: Category-wise Revenue")
print("----------------------------------")

# Category-wise Revenue
category_revenue = (
    sales_df
    .groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(category_revenue)



# ==========================================
# Pandas Task 8: Sales Channel Analysis
# ==========================================

print("\nPandas Task 8: Sales Channel Analysis")
print("----------------------------------")

# Sales Channel Analysis
channel_revenue = (
    sales_df
    .groupby("sales_channel")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(channel_revenue)



# ==========================================
# Pandas Task 9: Monthly Revenue Trend
# ==========================================

print("\nPandas Task 9: Monthly Revenue Trend")
print("----------------------------------")

# Convert order_date to datetime
sales_df["order_date"] = pd.to_datetime(sales_df["order_date"])

# Extract Year-Month
sales_df["month"] = sales_df["order_date"].dt.strftime("%Y-%m")

# Monthly Revenue
monthly_revenue = (
    sales_df
    .groupby("month")["total_amount"]
    .sum()
    .sort_index()
)

print(monthly_revenue)



# ==========================================
# Pandas Task 10: High-Value Customers
# ==========================================

print("\nPandas Task 10: High-Value Customers")
print("----------------------------------")

# High-Value Customers
high_value_customers = (
    sales_df
    .groupby(["customer_name", "city"])["total_amount"]
    .sum()
    .reset_index()
)

high_value_customers = high_value_customers[
    high_value_customers["total_amount"] > 50000
]

high_value_customers = high_value_customers.sort_values(
    by="total_amount",
    ascending=False
)

print(high_value_customers)

# ==========================================
# Save Final Sales Report
# ==========================================

sales_df.to_csv("sales_analysis_report.csv", index=False)

print("\nSales report saved as 'sales_analysis_report.csv'")

# ==========================================
# Close Database Connection
# ==========================================

conn.close()

print("\nDatabase connection closed.")