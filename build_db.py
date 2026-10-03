### PART-2 : SQL Verified Metrics Engine and Significance flagging
###STEP-1:Building the SQLite database

import sqlite3
import pandas as pd

# STEP 1: Read our Part 1 files

orders = pd.read_csv("orders_clean.csv")
regions = pd.read_csv("regions_master.csv")

print("Clean orders loaded:", len(orders))
print("Regions loaded:", len(regions))


# STEP 2: Connecting to SQLite database

connection = sqlite3.connect("pharmeasy.db")
print("Connected to pharmeasy.db")

# STEP 3: Creating the two tables

orders.to_sql(
    "orders_clean",
    connection,
    if_exists="replace",
    index=False
)

regions.to_sql(
    "regions_master",
    connection,
    if_exists="replace",
    index=False
)

# STEP 4: Checking the number of rows

orders_count = connection.execute(
    "SELECT COUNT(*) FROM orders_clean"
).fetchone()[0]

regions_count = connection.execute(
    "SELECT COUNT(*) FROM regions_master"
).fetchone()[0]


print("\nDatabase check:")
print("orders_clean rows:", orders_count)
print("regions_master rows:", regions_count)

# STEP 5: Closing the database

connection.close()
print("\nDatabase created successfully: pharmeasy.db")