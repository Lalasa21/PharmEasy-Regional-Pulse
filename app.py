### PART-4 : Dashboard & Stakeholder Presentation
### STEP - 1: Streamlit + Plotly dashboard

import streamlit as st
import pandas as pd
import plotly.express as px

# Loading the cleaned data

df = pd.read_csv("orders_clean.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.strftime("%Y-%m")

# Page title

st.title("PharmEasy Regional Pulse")

# Sidebar filters
st.sidebar.header("Filters")

regions = ["All"] + sorted(df["region"].unique())

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

if selected_region == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["region"] == selected_region]

months = sorted(df["month"].unique())

selected_month = st.sidebar.selectbox(
    "Select Month",
    months
)

month_df = filtered_df[
    filtered_df["month"] == selected_month
]

### STEP - 2 : Embedded executive summary

# Summary metrics for the selected region and month
summary_region = selected_region if selected_region != "All" else "All regions"
selected_month_label = pd.to_datetime(selected_month).strftime("%B %Y")
total_sales_all = month_df["sales_inr"].sum()
total_profit_all = month_df["profit_inr"].sum()
total_orders_all = month_df["order_id"].nunique()

# April and May sales for Guntur
guntur_april = df[
    (df["region"] == "Guntur") &
    (df["month"] == "2026-04")
]["sales_inr"].sum()

guntur_may = df[
    (df["region"] == "Guntur") &
    (df["month"] == "2026-05")
]["sales_inr"].sum()

if guntur_april != 0:
    guntur_change = ((guntur_may - guntur_april) / guntur_april) * 100
else:
    guntur_change = 0

# Top category for selected month
top_category = (
    month_df
    .groupby("category")["sales_inr"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

st.header("Executive Summary")

summary = (
    f"{summary_region} had ₹{total_sales_all:,.2f} in sales, "
    f"₹{total_profit_all:,.2f} in profit, and {total_orders_all:,} distinct orders "
    f"for {selected_month_label}. "
    
    f"Regional sales movements show meaningful month-to-month variation, "
    f"including a {guntur_change:.2f}% increase for Guntur from April to May. "
    
    f"For the selected month and region view, {top_category} is the highest-sales category. "
    
    f"Review the regional and category movements before taking operational action, "
    f"and use the charts and detail table below to investigate the underlying pattern."
)

st.info(summary)

# Overview Section

st.header("1. Overview")

# Calculate KPIs

total_sales = month_df["sales_inr"].sum()
total_profit = month_df["profit_inr"].sum()
total_orders = month_df["order_id"].nunique()

# KPI cards

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Sales (INR)",
    f"₹{total_sales:,.2f}"
)

col2.metric(
    "Total Profit (INR)",
    f"₹{total_profit:,.2f}"
)

col3.metric(
    "Distinct Order Count",
    total_orders
)

# Line Chart for monthly sales trend

trend = (
    filtered_df
    .groupby(["month", "region"], as_index=False)["sales_inr"]
    .sum()
)


fig_line = px.line(
    trend,
    x="month",
    y="sales_inr",
    color="region",
    markers=True,
    title="How did sales trend across April, May and June?"
)

# Start Y-axis at zero
fig_line.update_yaxes(
    title="Sales (INR)",
    rangemode="tozero"
)

fig_line.update_xaxes(
    title="Month"
)

st.plotly_chart(
    fig_line,
    use_container_width=True
)

# Category Section

st.header("2. Category")

category_sales = (
    month_df
    .groupby("category", as_index=False)["sales_inr"]
    .sum()
    .sort_values("sales_inr", ascending=False)
)

# Pie chart

fig_pie = px.pie(
    category_sales,
    names="category",
    values="sales_inr",
    title="Which medicine categories make up this month's sales?"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

# Bar Chart for region sales

region_sales = (
    month_df
    .groupby("region", as_index=False)["sales_inr"]
    .sum()
    .sort_values("sales_inr", ascending=False)
)

fig_bar = px.bar(
    region_sales,
    x="region",
    y="sales_inr",
    title="Which regions have the highest sales?"
)


# Start Y-axis at zero
fig_bar.update_yaxes(
    title="Sales (INR)",
    rangemode="tozero"
)

fig_bar.update_xaxes(
    title="Region"
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# Detail level table

st.header("3. Detail")

detail = (
    filtered_df
    .groupby(["region", "month"], as_index=False)
    .agg(
        sales_inr=("sales_inr", "sum"),
        profit_inr=("profit_inr", "sum"),
        order_count=("order_id", "nunique")
    )
)

# Adding S.No starting from 1
detail.insert(0, "S.No", range(1, len(detail) + 1))

# Rename columns for dashboard display
detail = detail.rename(columns={
    "region": "Region",
    "month": "Month",
    "sales_inr": "Sales (INR)",
    "profit_inr": "Profit (INR)",
    "order_count": "Order Count"
})

# Display table without pandas index
st.dataframe(
    detail,
    use_container_width=True,
    hide_index=True
)
