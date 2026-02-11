import streamlit as st
import pymysql
import pandas as pd
from datetime import date

# 1. Connect to Database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Suba@2000',
    database='test_analysis2'
)

# 2. Set up the App Page
st.set_page_config(page_title="Crypto Tracker", layout="wide")
st.title("Top 5 Crypto Analysis")
st.write("Select a coin and date range to view daily price trends.")

st.divider()

# ---------------------------------------------------------
# 3. FILTERS (MOVED TO MAIN PAGE)
# ---------------------------------------------------------
st.subheader("Filter Options")

# Get Top 5 Coins directly
sql_coins = "SELECT DISTINCT coin_id FROM Crypto_prices LIMIT 5"
df_coins = pd.read_sql_query(sql_coins, connection)
coin_list = df_coins['coin_id'].tolist()

# Organize filters using columns for a clean look
col1, col2, col3 = st.columns(3)

with col1:
    selected_coin = st.selectbox("Select Coin", coin_list)

with col2:
    start_date = st.date_input("Start Date", value=date(2025, 1, 1))

with col3:
    end_date = st.date_input("End Date", value=date(2025, 12, 31))

# 4. Button to Show Data
if st.button("Show Data", type="primary"):
    
    # Fetch Data
    sql_data = f"""
    SELECT date, price_usd 
    FROM Crypto_prices 
    WHERE coin_id = '{selected_coin}' 
    AND date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY date ASC
    """
    
    # Load into DataFrame
    df = pd.read_sql_query(sql_data, connection)

    # Check if we got any data
    if not df.empty:
        st.divider()
        st.subheader(f"Results for: {selected_coin}")

        # Basic Math for Metrics
        current_price = df.iloc[-1]['price_usd']
        max_price = df['price_usd'].max()
        min_price = df['price_usd'].min()

        # Display Metrics in Columns
        m1, m2, m3 = st.columns(3)
        m1.metric("Current Price", f"${current_price:.2f}")
        m2.metric("Highest Price", f"${max_price:.2f}")
        m3.metric("Lowest Price", f"${min_price:.2f}")

        # Charts and Tables
        st.write("### Price Chart")
        st.line_chart(df.set_index('date'))

        with st.expander("View Data Table"):
            st.dataframe(df, use_container_width=True)

    else:
        st.warning("No data found for this date range.")