# ===========================================
# Sales Data Analyzer - Streamlit App
# ISQS 3345 - Analytics and Development with Python
# ===========================================

# Import libraries
import pandas as pd  # You learned this in class
import streamlit as st  # New library - creates the web interface

# -------------------------------------------
# STREAMLIT BASICS:
# st.title() - displays a big title
# st.write() - displays text or data
# st.selectbox() - creates a dropdown menu
# st.button() - creates a clickable button
# st.metric() - displays a number nicely
# -------------------------------------------

# Set the page title (appears in browser tab)
st.title("Sales Data Analyzer")
st.write("Interactive dashboard to analyze sales performance")

# -------------------------------------------
# LOAD DATA
# Same as you did in Jupyter Notebook
# -------------------------------------------
df = pd.read_csv('sales_data.csv')

# Calculate total revenue (same as notebook)
df['TotalRevenue'] = df['Quantity'] * df['UnitPrice']

# -------------------------------------------
# SIDEBAR FILTERS
# st.sidebar puts elements on the left side
# -------------------------------------------
st.sidebar.header("Filters")

# Dropdown for Region
region_options = ['All'] + list(df['Region'].unique())
selected_region = st.sidebar.selectbox("Select Region", region_options)

# Dropdown for Category
category_options = ['All'] + list(df['Category'].unique())
selected_category = st.sidebar.selectbox("Select Category", category_options)

# Dropdown for Sales Rep
rep_options = ['All'] + list(df['SalesRep'].unique())
selected_rep = st.sidebar.selectbox("Select Sales Rep", rep_options)

# -------------------------------------------
# FILTER THE DATA
# Using if statements (you learned this!)
# -------------------------------------------
filtered_df = df.copy()

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

if selected_rep != 'All':
    filtered_df = filtered_df[filtered_df['SalesRep'] == selected_rep]

# -------------------------------------------
# DISPLAY KEY METRICS
# st.metric shows numbers in a nice format
# -------------------------------------------
st.header("Key Metrics")

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

# Calculate metrics (same logic as notebook)
total_revenue = filtered_df['TotalRevenue'].sum()
total_orders = len(filtered_df)
total_units = filtered_df['Quantity'].sum()

# Display metrics in columns
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Units Sold", total_units)

# -------------------------------------------
# ANALYSIS SECTIONS
# Using st.button to show/hide analyses
# -------------------------------------------

st.header("Detailed Analysis")

# Button 1: Revenue by Category
if st.button("Show Revenue by Category"):
    st.subheader("Revenue by Category")
    category_revenue = filtered_df.groupby('Category')['TotalRevenue'].sum()
    category_revenue = category_revenue.sort_values(ascending=False)
    st.write(category_revenue)

# Button 2: Revenue by Region
if st.button("Show Revenue by Region"):
    st.subheader("Revenue by Region")
    region_revenue = filtered_df.groupby('Region')['TotalRevenue'].sum()
    region_revenue = region_revenue.sort_values(ascending=False)
    st.write(region_revenue)

# Button 3: Top Products
if st.button("Show Top 5 Products"):
    st.subheader("Top 5 Products by Revenue")
    product_revenue = filtered_df.groupby('Product')['TotalRevenue'].sum()
    top_products = product_revenue.sort_values(ascending=False).head(5)
    st.write(top_products)

# Button 4: Sales Rep Performance
if st.button("Show Sales Rep Performance"):
    st.subheader("Sales Rep Performance")
    rep_stats = filtered_df.groupby('SalesRep').agg({
        'TotalRevenue': 'sum',
        'OrderID': 'count',
        'Quantity': 'sum'
    })
    rep_stats.columns = ['Revenue', 'Orders', 'Units Sold']
    rep_stats = rep_stats.sort_values('Revenue', ascending=False)
    st.write(rep_stats)

# -------------------------------------------
# SHOW RAW DATA
# Checkbox to optionally display the data
# -------------------------------------------
st.header("Raw Data")

if st.checkbox("Show filtered data table"):
    st.write(f"Showing {len(filtered_df)} records")
    st.dataframe(filtered_df)

# -------------------------------------------
# SUMMARY FUNCTION
# Same function from your notebook!
# -------------------------------------------
def generate_summary(dataframe):
    summary = {}
    summary['Total Revenue'] = f"${dataframe['TotalRevenue'].sum():,.2f}"
    summary['Total Orders'] = len(dataframe)
    summary['Average Order Value'] = f"${dataframe['TotalRevenue'].mean():,.2f}"
    
    if len(dataframe) > 0:
        summary['Best Category'] = dataframe.groupby('Category')['TotalRevenue'].sum().idxmax()
        summary['Best Region'] = dataframe.groupby('Region')['TotalRevenue'].sum().idxmax()
        summary['Top Product'] = dataframe.groupby('Product')['TotalRevenue'].sum().idxmax()
        summary['Top Sales Rep'] = dataframe.groupby('SalesRep')['TotalRevenue'].sum().idxmax()
    
    return summary

# Button for summary report
st.header("Summary Report")

if st.button("Generate Summary Report"):
    summary = generate_summary(filtered_df)
    for key, value in summary.items():
        st.write(f"**{key}:** {value}")
