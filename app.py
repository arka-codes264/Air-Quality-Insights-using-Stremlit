import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Custom CSS Styling ---
def local_css(css):
    import streamlit as st
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

local_css("""
    /* Center and style title */
    h1 {
        text-align: center;
        font-size: 3rem;
        color: #FF6F61;
    }

    h2, h3 {
        color: #FF6F61;
    }

    /* Style dataframes */
    .stDataFrame {
        border: 2px solid #FF6F61;
        border-radius: 10px;
        padding: 5px;
        background-color: #1E1E1E;
    }

    /* Sidebar style */
    section[data-testid="stSidebar"] {
        background-color: #262730;
        color: #FAFAFA;
    }

    /* Dropdown style */
    div[data-baseweb="select"] > div {
        background-color: #1E1E1E;
        border-radius: 8px;
    }
""")


# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_air_quality_data.csv")   # replace with your file
    return df

df = load_data()

# --- Title & Intro ---
# Title + short description (styled)
st.markdown(
    "<h1 style='text-align:center; margin-bottom:0.25rem;'>🌍 Air Quality Index (AQI) Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#BFC7D6; margin-top:0; font-size:1.05rem;'>"
    "Interactive dashboard to explore air quality data — filter by city, date and pollutant, "
    "and export reports.</p>",
    unsafe_allow_html=True
)

# Optional: small tagline / quick metrics row
col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.metric("Records", f"{len(df):,}")
with col2:
    st.markdown("<div style='text-align:center; color:#FFFFFF; font-weight:bold;'>"
                "Explore trends • Compare cities • Export plots</div>", unsafe_allow_html=True)
with col3:
    st.metric("Cities", f"{df['city'].nunique() if 'city' in df.columns else 'N/A'}")

# --- Dataset Preview ---
st.subheader("📊 Dataset Preview")
# Add city filter
city_filter = st.text_input("🔍 Search by city (leave blank to see all):")

if city_filter:
    filtered_df = df[df["city"].str.contains(city_filter, case=False, na=False)]
    st.dataframe(filtered_df)
else:
    st.dataframe(df)


# --- Column Selection ---
numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
selected_col = st.selectbox("Choose a column to analyze:", numeric_cols)

# --- Summary Statistics ---
st.subheader("📈 Summary Statistics")
st.write(df[selected_col].describe())

# ------------------------------
# 📊 City Insights Section
# ------------------------------
st.markdown("## 🌆 City Insights")

# Dropdown to choose city
selected_city = st.selectbox("Choose a city to analyze:", df['city'].dropna().unique())

# Filter data for that city
city_data = df[df['city'] == selected_city]

if not city_data.empty:
    st.markdown(f"### 🏙️ {selected_city} Overview")

    # Show summary metrics in a nice layout
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average AQI", round(city_data['aqi_value'].mean(), 2))
    with col2:
        st.metric("Max AQI", city_data['aqi_value'].max())
    with col3:
        st.metric("Overall Category", city_data['aqi_category'].mode()[0] if not city_data['aqi_category'].mode().empty else "N/A")

    # Add detailed table of that city
    st.markdown("#### 📋 Detailed Records")
    st.dataframe(city_data, use_container_width=True)
else:
    st.warning("No data available for this city.")


# --- Histogram ---
st.subheader(f"📉 Distribution of {selected_col}")
fig, ax = plt.subplots()
df[selected_col].hist(bins=30, ax=ax)
st.pyplot(fig)

# --- Line Plot (Trend Over Time) ---
if "Date" in df.columns:   # Only if you have a date column
    st.subheader("📅 AQI Trend Over Time")
    fig, ax = plt.subplots()
    df.groupby("Date")[selected_col].mean().plot(ax=ax)
    st.pyplot(fig)

# --- Missing Values ---
st.subheader("🔍 Missing Values Check")
st.write(df.isna().sum())
