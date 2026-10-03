### PART-2 : SQL Verified Metrics Engine and Significance flagging
###STEP - 4: Significance flagging with state persistence

import sqlite3
import json

#  Percentage Change

def compute_percentage_change_v1(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

# Significant Region Flagging

def flag_significant_regions_v1(changes, threshold=8):
    flagged = []
    for region, change in changes.items():
        if abs(change) > threshold:
            flagged.append(region)
            return flagged

# Saving State

def save_state_v1(month_summary, path):
    with open(path, "w") as file:
        json.dump(month_summary, file, indent=4)


# To load Previous State

def load_previous_state_v1(path):
    with open(path, "r") as file:
        return json.load(file)

# Get monthly sales from database

def get_monthly_sales(month):
    connection = sqlite3.connect("pharmeasy.db")
    rows = connection.execute("""
        SELECT
            region,SUM(sales_inr)
        FROM orders_clean
        WHERE strftime('%Y-%m', order_date) = ?
        GROUP BY region
    """, (month,)).fetchall()

    connection.close()
    sales = {}
    for row in rows:
        region = row[0]
        total_sales = row[1]
        sales[region] = total_sales
    return sales

# Calculate changes between two months

def calculate_changes(previous_month, current_month):

    previous_sales = get_monthly_sales(previous_month)
    current_sales = get_monthly_sales(current_month)

    changes = {}

    for region in current_sales:
        current = current_sales[region]
        previous = previous_sales.get(region, 0)
        change = compute_percentage_change_v1(
            current,
            previous
        )
        changes[region] = change
    return changes


# Main Testing Block

if __name__ == "__main__":

    # Transition from April -> May

    april_may_changes = calculate_changes(
        "2026-04",
        "2026-05"
    )

    april_may_flagged = flag_significant_regions_v1(
        april_may_changes
    )

    print("\nApril -> May flagged regions:")
    print(april_may_flagged)


    # Transition from May -> June

    may_june_changes = calculate_changes(
        "2026-05",
        "2026-06"
    )

    may_june_flagged = flag_significant_regions_v1(
        may_june_changes
    )

    print("\nMay -> June flagged regions:")
    print(may_june_flagged)


    # Saving April state

    april_sales = get_monthly_sales("2026-04")

    save_state_v1(
        april_sales,
        "april_state.json"
    )

    print("\nApril state saved.")


    # Loading April state

    previous_state = load_previous_state_v1(
        "april_state.json"
    )

    print("April state loaded successfully.")


    # Nellore check

    print("\nNellore check:")

    print(
        "April -> May:",
        april_may_changes.get("Nellore")
    )

    print(
        "May -> June:",
        may_june_changes.get("Nellore")
    )