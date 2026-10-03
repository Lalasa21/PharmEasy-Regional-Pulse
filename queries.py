### PART-2 : SQL Verified Metrics Engine and Significance flagging
###STEP-2:JOIN Validation

import sqlite3

# Connect to database

connection = sqlite3.connect("pharmeasy.db")

# CHECK 1: LEFT JOIN vs INNER JOIN

left_join_count = connection.execute("""
    SELECT COUNT(*) FROM regions_master r
    LEFT JOIN orders_clean o ON r.region = o.region
""").fetchone()[0]

inner_join_count = connection.execute("""
    SELECT COUNT(*) FROM regions_master r
    INNER JOIN orders_clean o ON r.region = o.region
""").fetchone()[0]

print("LEFT JOIN count:", left_join_count)
print("INNER JOIN count:", inner_join_count)
print("Difference:", left_join_count - inner_join_count)


# CHECK 2: Duplicate key check

duplicate_orders = connection.execute("""
    SELECT order_id, COUNT(*) AS order_count FROM orders_clean
    GROUP BY order_id
    HAVING COUNT(*) > 1
""").fetchall()

print("\nDuplicate order IDs found:", len(duplicate_orders))

if len(duplicate_orders) == 0:
    print("PASS: No duplicate order_id values.")
else:
    for row in duplicate_orders:
        print(row)

# CHECK 3: NULL Check( COUNT(*) vs COUNT(order_id) )

count_comparison = connection.execute("""
    SELECT r.region,COUNT(*) AS count_star,COUNT(o.order_id) AS count_order_id
    FROM regions_master r
    LEFT JOIN orders_clean o ON r.region = o.region
    GROUP BY r.region
    ORDER BY r.region
""").fetchall()

# Find regions where the two counts differ
print("\nRegions where COUNT(*) and COUNT(order_id) differ:")

for row in count_comparison:

    region = row[0]
    count_star = row[1]
    count_order_id = row[2]

    if count_star != count_order_id:
        print(
            region,
            "| COUNT(*) =",
            count_star,
            "| COUNT(order_id) =",
            count_order_id
        )

# CHECK 4: Per-region order counts

region_counts = connection.execute("""
    SELECT r.region,COUNT(o.order_id) AS order_count
    FROM regions_master r
    LEFT JOIN orders_clean o ON r.region = o.region
    GROUP BY r.region
    ORDER BY order_count ASC
""").fetchall()

print("\nPer-region order counts")

for row in region_counts:
    print(row)

###STEP-3:Region-Month Sales and MOM Growth

monthly_sales = connection.execute("""
    SELECT region,strftime('%Y-%m', order_date) AS month,SUM(sales_inr) AS total_sales
    FROM orders_clean
    GROUP BY region, month
    ORDER BY region, month
""").fetchall()


print("\nMonthly sales:")

for row in monthly_sales:
    print(row)

sales_by_region = {}

for row in monthly_sales:

    region = row[0]
    month = row[1]
    sales = row[2]

    if region not in sales_by_region:
        sales_by_region[region] = {}

    sales_by_region[region][month] = sales


# MONTH-ON-MONTH GROWTH

# April -> May

print("\nApril -> May")

for region in sorted(sales_by_region):

    april_sales = sales_by_region[region].get("2026-04", 0)
    may_sales = sales_by_region[region].get("2026-05", 0)

    if april_sales == 0:
        growth = 0
    else:
        growth = ((may_sales - april_sales) / april_sales * 100)

    print(
        region,
        "| April:", round(april_sales, 2),
        "| May:", round(may_sales, 2),
        "| Growth:", round(growth, 2), "%"
    )

# May -> June

print("\nMay -> June")

for region in sorted(sales_by_region):

    may_sales = sales_by_region[region].get("2026-05", 0)
    june_sales = sales_by_region[region].get("2026-06", 0)

    if may_sales == 0:
        growth = 0
    else:
        growth = ((june_sales - may_sales) / may_sales * 100)

    print(
        region,
        "| May:", round(may_sales, 2),
        "| June:", round(june_sales, 2),
        "| Growth:", round(growth, 2), "%"
    )

# Closing the database

connection.close()
print("\nAll SQL checks and monthly calculations completed")

