###  PART -1 DATA FOUNDATION AND VALIDATION
### STEP-1: To generate python scripts and to check the row and column counts

# python -c "import pandas as pd; print(pd.read_csv('pharmeasy_orders_raw.csv').shape); print(pd.read_csv('regions_master.csv').shape)"
# Output:
# (2159, 8) 
# (10, 3)

### STEP-2: To build the clean pipeline

import pandas as pd

# STEP 1: To load the raw data

df = pd.read_csv("pharmeasy_orders_raw.csv")
print("Raw rows:", len(df))


# STEP 2: To remove exact duplicate rows

rows_before = len(df)
df = df.drop_duplicates()
rows_after = len(df)
duplicates_removed = rows_before - rows_after

print("Duplicate rows removed:", duplicates_removed)
print("Rows after removing duplicates:", rows_after)

# STEP 3: To normalize region names
# .str.strip()removes spaces at the beginning and end of the string
# .str.title() converts the first character of each word to uppercase and the rest to lowercase

df["region"] = df["region"].str.strip().str.title()
print("Region names normalized")


# STEP 4: To fill missing categories

# Considering rows where category is NOT missing
category_data = df.dropna(subset=["category"])

# Creating product -> category lookup
product_category = (
    category_data
    .drop_duplicates("product")
    .set_index("product")["category"]
)

# To count missing categories before filling
missing_category_before = df["category"].isna().sum()

# To fill missing category using product name
df["category"] = df["category"].fillna(
    df["product"].map(product_category)
)

# To count missing categories after filling
missing_category_after = df["category"].isna().sum()

print("Missing categories before:", missing_category_before)
print("Missing categories after:", missing_category_after)


# STEP 5: To fill missing profit

# To calculate profit margin for rows where profit exists
df["profit_margin"] = df["profit_inr"] / df["sales_inr"]

# To calculate average profit margin for each category
category_mean_margin = (
    df.dropna(subset=["profit_inr"])
    .groupby("category")["profit_margin"]
    .mean()
)

print("\nAverage profit margin by category:")
print(category_mean_margin)


# To count missing profit before filling
missing_profit_before = df["profit_inr"].isna().sum()

# To find rows where profit is missing
missing_profit = df["profit_inr"].isna()

# To get the correct category margin for each row
margin_for_row = df.loc[missing_profit, "category"].map(
    category_mean_margin
)

# To calculate missing profit
df.loc[missing_profit, "profit_inr"] = (
    df.loc[missing_profit, "sales_inr"] * margin_for_row
).round(2)

# Count missing profit after filling
missing_profit_after = df["profit_inr"].isna().sum()

print("\nMissing profit before:", missing_profit_before)
print("Missing profit after:", missing_profit_after)

# To remove temporary profit_margin column
df = df.drop(columns=["profit_margin"])

# STEP 7: Saving the clean dataset

df.to_csv("orders_clean.csv", index=False)

print("\nClean dataset saved as orders_clean.csv")
print("Final rows:", len(df))