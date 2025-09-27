# app.py
# Streamlit ODI Match Dashboard
# Made with ❤️ using Pandas, Numpy, and Plotly

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="ODI Match Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# Styling for Attractive Look
# ===============================
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #74ebd5, #9face6);
    color: black;
}
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #f7f8f8, #acbb78);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ===============================
# Load Data
# ===============================
df = pd.read_csv("ODI_Match_info.csv")

# Handle missing values
df = df.dropna(how="all").reset_index(drop=True)

# Sidebar Options
st.sidebar.header("⚙️ Filter Matches")
all_columns = df.columns.tolist()

# Dropdown to select column for filtering
filter_col = st.sidebar.selectbox("Choose column to filter", all_columns)

# Unique values for filter
unique_vals = df[filter_col].dropna().unique()
selected_val = st.sidebar.selectbox(f"Select value in {filter_col}", unique_vals)

# Filtered Data
filtered_df = df[df[filter_col] == selected_val]

# Radio button for chart type
chart_type = st.sidebar.radio(
    "Choose chart type",
    ("Bar Chart", "Pie Chart", "Line Chart", "Scatter Plot")
)

# ===============================
# Main Page
# ===============================
st.title("🏏 ODI Match Dashboard")
st.subheader("Explore ODI Match Data with Pandas, Numpy, and Plotly 🎨")

st.write("### Sample Data Preview")
st.dataframe(filtered_df.head(20))

# ===============================
# Basic Calculations (Numpy + Pandas)
# ===============================
st.write("### 📊 Quick Match Stats")

st.write(f"Total Rows: {len(filtered_df)}")
st.write(f"Columns: {list(filtered_df.columns)}")

# Example numeric stats (if numeric cols exist)
numeric_cols = filtered_df.select_dtypes(include=np.number).columns.tolist()
if numeric_cols:
    col = numeric_cols[0]
    st.write(f"Mean of {col}: {np.mean(filtered_df[col])}")
    st.write(f"Max of {col}: {np.max(filtered_df[col])}")
    st.write(f"Min of {col}: {np.min(filtered_df[col])}")

# ===============================
# Plotly Graphs
# ===============================
st.write("### 🎨 Interactive Charts")

if chart_type == "Bar Chart":
    fig = px.bar(filtered_df, x=filtered_df.columns[0], y=filtered_df.columns[1],
                 color=filtered_df.columns[0], title="Bar Chart")
elif chart_type == "Pie Chart":
    fig = px.pie(filtered_df, names=filtered_df.columns[0], 
                 title="Pie Chart", color_discrete_sequence=px.colors.qualitative.Set3)
elif chart_type == "Line Chart":
    fig = px.line(filtered_df, x=filtered_df.columns[0], y=filtered_df.columns[1],
                  title="Line Chart", markers=True)
elif chart_type == "Scatter Plot":
    fig = px.scatter(filtered_df, x=filtered_df.columns[0], y=filtered_df.columns[1],
                     color=filtered_df.columns[0], size_max=10, title="Scatter Plot")

st.plotly_chart(fig, use_container_width=True)

# ===============================
# Extra Summary
# ===============================
st.write("### 📝 Data Summary")
st.write(filtered_df.describe(include="all"))
