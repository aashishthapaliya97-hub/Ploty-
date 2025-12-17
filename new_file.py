import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Regional Sales Dashboard", layout="wide")

st.title("📊 Regional Sales & Orders Dashboard")

# -------------------------
# Create DataFrame
# -------------------------
df = pd.DataFrame({
    'Region': ['North', 'South', 'North', 'South', 'East'],
    'Sales': [100, 150, 200, 180, 120],
    'Orders': [5, 8, 10, 7, 6]
})

# -------------------------
# Sidebar Filter
# -------------------------
st.sidebar.header("Filter Options")

regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

filtered_df = df[df['Region'].isin(regions)]

# -------------------------
# KPIs (Metrics)
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", filtered_df['Sales'].sum())
col2.metric("📦 Total Orders", filtered_df['Orders'].sum())
col3.metric("📈 Avg Sales", round(filtered_df['Sales'].mean(), 2))

# -------------------------
# Grouped Summary Table (with Index)
# -------------------------
summary = (
    filtered_df
    .groupby('Region')
    .agg(
        Total_Sales=('Sales', 'sum'),
        Avg_Sales=('Sales', 'mean'),
        Orders=('Orders', 'sum')
    )
    .reset_index()
)

summary.index = range(1, len(summary) + 1)

st.subheader("📋 Summary by Region")
st.dataframe(summary, use_container_width=True)

# -------------------------
# Charts Section
# -------------------------
col4, col5 = st.columns(2)

with col4:
    st.subheader("Sales by Region")
    fig1 = px.bar(
        filtered_df,
        x='Region',
        y='Sales',
        color='Region',
        text='Sales'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    st.subheader("Orders by Region")
    fig2 = px.bar(
        filtered_df,
        x='Region',
        y='Orders',
        color='Region',
        text='Orders'
    )
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Scatter Plot
# -------------------------
st.subheader("Sales vs Orders Relationship")

fig3 = px.scatter(
    filtered_df,
    x='Orders',
    y='Sales',
    color='Region',
    size='Sales',
    hover_data=['Region']
)

st.plotly_chart(fig3, use_container_width=True)

