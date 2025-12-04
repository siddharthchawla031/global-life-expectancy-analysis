import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Dataset Overview")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("../data/UnifiedDataset.csv")

df = load_data()

# Debug (optional)
# st.write("COLUMNS:", df.columns.tolist())

# Basic info
st.subheader("📁 Dataset Structure")
st.write(f"**Rows:** {df.shape[0]}  |  **Columns:** {df.shape[1]}")
st.dataframe(df.head(), use_container_width=True)

# Summary
st.subheader("🌍 Summary Information")

total_countries = df["Country"].nunique()
years = sorted(df["Year"].unique())
min_year, max_year = min(years), max(years)

st.write(f"""
- **Total Countries:** {total_countries}  
- **Year Range:** {min_year} — {max_year}  
- **Genders:** {df['Gender'].unique().tolist()}
""")

# Missing values
st.subheader("🧩 Missing Values Summary")

missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)

if len(missing) > 0:
    st.write("Columns with missing values:")
    st.write(missing)
else:
    st.success("No missing values!")

# Global Life Expectancy Trend
st.subheader("📈 Global Life Expectancy Trend")

df_global = df.groupby("Year")["Life Expectancy"].mean().reset_index()

fig = px.line(
    df_global,
    x="Year",
    y="Life Expectancy",
    title="Global Average Life Expectancy Over Time",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)
