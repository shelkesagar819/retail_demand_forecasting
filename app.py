import pickle
from datetime import date
import joblib
import streamlit as st
import pandas as pd
import sklearn
st.write("Scikit-learn version:", sklearn.__version__)

st.set_page_config(
    page_title="Retail Demand Forecasting",
    layout="wide"
)

st.title("Retail Demand Forecasting Dashboard")

df = pd.read_csv("data/cleaned_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Revenue"] = df["Units Sold"] * df["Price"]

# Sidebar Filters
st.sidebar.header("Filters")

regions = ["All"] + sorted(df["Region"].dropna().unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

categories = ["All"] + sorted(df["Category"].dropna().unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Apply Filters
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# KPI Cards
col1, col2 = st.columns(2)

col1.metric(
    "Total Units Sold",
    f"{filtered_df['Units Sold'].sum():,}"
)

col2.metric(
    "Total Revenue",
    f"₹{filtered_df['Revenue'].sum():,.2f}"
)

# Category Chart
st.subheader("Units Sold by Category")

category_sales = filtered_df.groupby("Category")["Units Sold"].sum()
st.bar_chart(category_sales)

# Monthly Sales Chart
st.subheader("Monthly Units Sold")

filtered_df["Month"] = filtered_df["Date"].dt.strftime("%Y-%m")

monthly_sales = (
    filtered_df.groupby("Month")["Units Sold"]
    .sum()
    .sort_index()
)

st.line_chart(monthly_sales)

# Data Table
st.subheader("Retail Sales Data")
st.dataframe(filtered_df.head(20), use_container_width=True)


st.divider()
st.subheader("🤖 ML Demand Prediction")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        inventory = st.number_input("Inventory Level", min_value=0, value=200)
        price = st.number_input("Price", min_value=0.0, value=50.0)
        discount = st.number_input("Discount", min_value=0.0, value=0.0)

    with col2:
        promotion = st.selectbox("Holiday / Promotion", [0, 1])
        forecast_date = st.date_input(
            "Forecast Date", value=date(2024, 1, 2)
        )
        lag_1 = st.number_input("Previous Day Sales", min_value=0.0, value=100.0)

    with col3:
        lag_7 = st.number_input("Sales 7 Days Ago", min_value=0.0, value=100.0)
        rolling_7 = st.number_input("7-Day Average Sales", min_value=0.0, value=100.0)

    predict_button = st.form_submit_button("Predict Demand")

if predict_button:
    d = pd.Timestamp(forecast_date)

    input_data = pd.DataFrame([{
        "Inventory Level": inventory,
        "Price": price,
        "Discount": discount,
        "Holiday/Promotion": promotion,
        "Year": d.year,
        "Month": d.month,
        "Day": d.day,
        "DayOfWeek": d.dayofweek,
        "IsWeekend": int(d.dayofweek in [5, 6]),
        "Lag_1_Day": lag_1,
        "Lag_7_Days": lag_7,
        "Rolling_7_Days": rolling_7
    }])

    try:
        model = joblib.load(
            "models/random_forest_demand_model.pkl"
        )
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted Units Sold: {max(0, prediction):.0f}")

    except FileNotFoundError:
        st.error("ML model file not found in the models folder.")