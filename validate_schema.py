###  PART -1 DATA FOUNDATION AND VALIDATION
### STEP-3 Creating Schema validation function

import pandas as pd

def validate_schema(df, required_columns):
    missing_columns = []
    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)

    if len(missing_columns) == 0:
        status = "validated"
    else:
        status = "blocked_schema"

    result = {
        "status": status,
        "row_count": len(df),
        "missing_columns": missing_columns
    }

    return result

# Loading cleaned data
df = pd.read_csv("orders_clean.csv")

# Required columns

required_columns = [
    "order_id",
    "order_date",
    "region",
    "category",
    "product",
    "quantity",
    "sales_inr",
    "profit_inr"
]

# Test 1: Correct dataset

print("TEST 1: Correct cleaned dataset")

result = validate_schema(
    df,
    required_columns
)

print(result)

# Test 2: Deliberately broken dataset

print("\nTEST 2: Broken dataset")

# Making a copy so we do not damage the original data
broken_df = df.copy()

# Remove one required column
broken_df = broken_df.drop(columns=["sales_inr"])


# Validate the broken dataset
broken_result = validate_schema(
    broken_df,
    required_columns
)

print(broken_result)