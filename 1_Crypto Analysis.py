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

# 2. Page Setup
st.set_page_config(page_title="Market Overview", layout="wide")
st.title("Global Market")
st.write("Compare Bitcoin, Oil, and Stock.")

st.divider()

# ---------------------------------------------------------
# 3. DATE FILTERS
# ---------------------------------------------------------
st.subheader("Date Selection")
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Start Date", value=date(2025, 1, 1))

with col2:
    end_date = st.date_input("End Date", value=date(2025, 12, 31))

# 4. Main Button
if st.button("Analyze Markets", type="primary"):
    
    st.divider()
    
    # ---------------------------------------------------------
    # PART A: CALCULATE AVERAGES
    # ---------------------------------------------------------
    
    # 1. Bitcoin Average
    sql_btc = f"""
    SELECT AVG(price_usd) FROM Crypto_prices 
    WHERE coin_id = 'bitcoin' AND date BETWEEN '{start_date}' AND '{end_date}'
    """
    btc_df = pd.read_sql(sql_btc, connection)
    btc_avg = btc_df.iloc[0,0] if (not btc_df.empty and btc_df.iloc[0,0] is not None) else 0.0

    # 2. Oil Average
    sql_oil = f"""
    SELECT AVG(price_usd) FROM Oil_prices 
    WHERE date BETWEEN '{start_date}' AND '{end_date}'
    """
    oil_df = pd.read_sql(sql_oil, connection)
    oil_avg = oil_df.iloc[0,0] if (not oil_df.empty and oil_df.iloc[0,0] is not None) else 0.0

    # 3. S&P 500 Average (^GSPC)
    sql_sp500 = f"""
    SELECT AVG(close) FROM Stock_prices 
    WHERE ticker = '^GSPC' AND date BETWEEN '{start_date}' AND '{end_date}'
    """
    sp500_df = pd.read_sql(sql_sp500, connection)
    sp500_avg = sp500_df.iloc[0,0] if (not sp500_df.empty and sp500_df.iloc[0,0] is not None) else 0.0

    # 4. NASDAQ Average (^IXIC) - NEW ADDITION
    sql_nasdaq = f"""
    SELECT AVG(close) FROM Stock_prices 
    WHERE ticker = '^IXIC' AND date BETWEEN '{start_date}' AND '{end_date}'
    """
    nasdaq_df = pd.read_sql(sql_nasdaq, connection)
    nasdaq_avg = nasdaq_df.iloc[0,0] if (not nasdaq_df.empty and nasdaq_df.iloc[0,0] is not None) else 0.0

    # 5. Nifty Average (^NSEI)
    sql_nifty = f"""
    SELECT AVG(close) FROM Stock_prices 
    WHERE ticker = '^NSEI' AND date BETWEEN '{start_date}' AND '{end_date}'
    """
    nifty_df = pd.read_sql(sql_nifty, connection)
    nifty_avg = nifty_df.iloc[0,0] if (not nifty_df.empty and nifty_df.iloc[0,0] is not None) else 0.0

    # Display Metrics (Now 5 columns)
    st.subheader("Average Prices")
    m1, m2, m3, m4, m5 = st.columns(5)
    
    m1.metric("Bitcoin", f"${btc_avg:,.2f}")
    m2.metric("Crude Oil", f"${oil_avg:,.2f}")
    m3.metric("S&P 500", f"${sp500_avg:,.2f}")
    m4.metric("NASDAQ", f"${nasdaq_avg:,.2f}")
    m5.metric("Nifty 50", f"${nifty_avg:,.2f}")

    # ---------------------------------------------------------
    # PART B: MASTER TABLE
    # ---------------------------------------------------------
    st.subheader("Daily Market Snapshot Table")
    st.write("Joining data from Crypto, Oil, and Stock tables...")

    # Updated Query: Joins Stock_prices 3 times (s1=S&P, s2=NASDAQ, s3=Nifty)
    sql_join = f"""
    SELECT 
        c.date as Date, 
        c.price_usd as 'Bitcoin ($)', 
        o.price_usd as 'Oil ($)', 
        s1.close as 'S&P 500 ($)', 
        s2.close as 'NASDAQ ($)',
        s3.close as 'Nifty 50 ($)'
    FROM Crypto_prices c
    LEFT JOIN Oil_prices o ON c.date = o.date
    LEFT JOIN Stock_prices s1 ON c.date = s1.date AND s1.ticker = '^GSPC'
    LEFT JOIN Stock_prices s2 ON c.date = s2.date AND s2.ticker = '^IXIC'
    LEFT JOIN Stock_prices s3 ON c.date = s3.date AND s3.ticker = '^NSEI'
    WHERE c.coin_id = 'bitcoin' 
      AND c.date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY c.date ASC
    """
    
    df_snapshot = pd.read_sql(sql_join, connection)

    if not df_snapshot.empty:
        st.dataframe(df_snapshot, use_container_width=True)
        
       