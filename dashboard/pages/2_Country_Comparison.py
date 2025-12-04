# pages/2_Country_Comparison.py
import streamlit as st
import pandas as pd
import plotly.express as px
import importlib

st.title("🇮🇳 Country Comparison Dashboard")

# ---------- Load data ----------
@st.cache_data
def load_data():
    return pd.read_csv("../data/UnifiedDataset.csv")


df = load_data()

# ---------- Helper to find a column by keywords ----------
def find_col(keywords, df_cols):
    """Return first column name that contains all keywords (case-insensitive)."""
    keywords = [k.lower() for k in keywords]
    for col in df_cols:
        name = col.lower()
        if all(k in name for k in keywords):
            return col
    return None

# ---------- Detect columns robustly ----------
cols = df.columns.tolist()

life_col = find_col(["life", "expect"], cols) or find_col(["life"], cols)  # primary
infant_col = find_col(["infant"], cols) or find_col(["neonatal"], cols)
gdp_col = find_col(["gdp"], cols) or find_col(["income"], cols) or find_col(["gni"], cols)

if life_col is None:
    st.error("Could not find a Life Expectancy column in the dataset. Check your CSV column names.")
    st.stop()

# If GDP-like column exists but is constant per country (often after imputation),
# we will fallback to Income_per_Capita or GNI if available.
def is_constant_by_country(df, col):
    tmp = df.groupby("Country")[col].nunique(dropna=True)
    # If most countries have only 1 unique value, treat as constant
    return (tmp.fillna(0) <= 1).mean() > 0.5

if gdp_col:
    try:
        if is_constant_by_country(df, gdp_col):
            # Try to find an alternative numeric income column
            alt = find_col(["income"], cols) or find_col(["gni"], cols)
            if alt and alt != gdp_col:
                st.info(f"Detected {gdp_col} is nearly constant by country — using {alt} instead for GDP plot.")
                gdp_col = alt
    except Exception:
        # If grouping fails (e.g., non-numeric), ignore and proceed
        pass
else:
    st.info("No GDP-like column found; GDP plots will be disabled.")

if infant_col is None:
    st.warning("Infant mortality column not found — that plot will be hidden.")

# ---------- Country selectors ----------
countries = sorted(df["Country"].dropna().unique())
if not countries:
    st.error("No countries found in the dataset.")
    st.stop()

# sensible defaults
default1 = "India" if "India" in countries else countries[0]
default2 = "China" if "China" in countries else (countries[1] if len(countries) > 1 else countries[0])

col1, col2 = st.columns(2)
with col1:
    country1 = st.selectbox("Select Country 1", countries, index=countries.index(default1))
with col2:
    country2 = st.selectbox("Select Country 2", countries, index=countries.index(default2))

df_pair = df[df["Country"].isin([country1, country2])].copy()

# ---------- Safely coerce numeric columns ----------
def safe_numeric(series):
    return pd.to_numeric(series, errors="coerce")

# Coerce columns we will plot to numeric (if they exist)
df_pair[life_col] = safe_numeric(df_pair[life_col])
if gdp_col:
    df_pair[gdp_col] = safe_numeric(df_pair[gdp_col])
if infant_col:
    df_pair[infant_col] = safe_numeric(df_pair[infant_col])

# Drop NaNs for plotting
df_pair_le = df_pair.dropna(subset=[life_col, "Year"])
df_pair_gdp = df_pair.dropna(subset=[gdp_col, life_col]) if gdp_col else pd.DataFrame()
df_pair_infant = df_pair.dropna(subset=[infant_col, "Year"]) if infant_col else pd.DataFrame()

# ---------- Life Expectancy comparison ----------
st.subheader("📈 Life Expectancy Comparison")
if df_pair_le.empty:
    st.warning("No valid life expectancy data for the selected countries.")
else:
    fig = px.line(
        df_pair_le,
        x="Year",
        y=life_col,
        color="Country",
        title=f"Life Expectancy: {country1} vs {country2}",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- GDP vs Life Expectancy ----------
st.subheader("💰 GDP / Income vs Life Expectancy")
if gdp_col and not df_pair_gdp.empty:
    # Try adding trendline only if statsmodels is available
    trendline_kw = {}
    if importlib.util.find_spec("statsmodels") is not None:
        trendline_kw["trendline"] = "ols"
    else:
        st.info("`statsmodels` not installed — trendline disabled. To enable trendline run: pip install statsmodels")

    fig2 = px.scatter(
        df_pair_gdp,
        x=gdp_col,
        y=life_col,
        color="Country",
        hover_name="Country",
        title=f"{gdp_col} vs {life_col}",
        **trendline_kw
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No GDP/Income column available or no valid numeric rows to plot.")

# ---------- Infant Mortality comparison ----------
st.subheader("👶 Infant / Neonatal Mortality Comparison")
if infant_col and not df_pair_infant.empty:
    fig3 = px.line(
        df_pair_infant,
        x="Year",
        y=infant_col,
        color="Country",
        markers=True,
        title=f"{infant_col}: {country1} vs {country2}"
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Infant mortality data not available for selected countries.")
