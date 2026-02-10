import streamlit as st
import pymysql
import pandas as pd

# 1. Page Setup
st.set_page_config(layout="wide", page_title="Market Analysis Dashboard")

# 2. Connect to MySQL Database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Suba@2000',
    database='test_analysis1'
)

# 3. App Title
st.title("Market Analysis Dashboard")
st.write("Compare Crypto, Oil, and Stocks using SQL.")

# ---------------------------------------------------------
# SELECT ANALYSIS
# ---------------------------------------------------------
st.divider()
st.subheader("Select Analysis")

option = st.selectbox(
    "Choose a Query to Run:",
    [
        # Crypto
        "1. Top 3 Cryptos by Market Cap",
        "2. High Supply Coins (>90% Circulating)",
        "3. Coins Near All-Time High (10%)",
        "4. Avg Rank (High Volume Coins)",
        "5. Most Recently Updated Coin",
        "6. Highest BTC Price (Last 365 Days)",
        "7. Avg ETH Price (Last 1 Year)",
        "8. Bitcoin Trend (Mar 2025)",
        "9. Coin with Highest Avg Price",
        "10. BTC % Change (Sep '24 - Sep '25)",
        # Oil
        "11. Highest Oil Price (Last 5 Years)",
        "12. Avg Oil Price per Year",
        "13. Oil Prices during COVID (2020)",
        "14. Lowest Oil Price (Last 10 Years)",
        "15. Oil Price Volatility",
        # Stocks
        "16. S&P 500 Prices (^GSPC)",
        "17. Highest NASDAQ Close (^IXIC)",
        "18. High Volatility Days (S&P 500)",
        "19. Monthly Avg Closing Price",
        "20. Avg Volume for Nifty (2024)",
        # Cross-Market
        "21. BTC vs Oil Avg Price (2025)",
        "22. BTC vs S&P 500 Correlation",
        "23. ETH vs NASDAQ Daily (2025)",
        "24. BTC Price when Oil is High",
        "25. Top Coins vs Nifty Trend",
        "26. S&P 500 vs Crude Oil",
        "27. BTC vs Oil Correlation",
        "28. NASDAQ vs ETH Trend",
        "29. Crypto vs Stock Indices (2025)",
        "30. Master View (BTC, Oil, All Stocks)" # <--- UPDATED NAME HERE
    ]
)

st.divider()

# ---------------------------------------------------------
# QUERY LOGIC
# ---------------------------------------------------------
sql = ""

# --- CRYPTO ---
if option == "1. Top 3 Cryptos by Market Cap":
    sql = "SELECT name, market_cap FROM Cryptocurrencies ORDER BY market_cap DESC LIMIT 3"

elif option == "2. High Supply Coins (>90% Circulating)":
    sql = "SELECT name, circulating_supply, total_supply FROM Cryptocurrencies WHERE total_supply > 0 AND (circulating_supply / total_supply) > 0.9"

elif option == "3. Coins Near All-Time High (10%)":
    sql = "SELECT name, current_price, ath FROM Cryptocurrencies WHERE current_price >= (ath * 0.9)"

elif option == "4. Avg Rank (High Volume Coins)":
    sql = "SELECT AVG(market_cap_rank) as 'Average Rank' FROM Cryptocurrencies WHERE total_volume > 1000000000"

elif option == "5. Most Recently Updated Coin":
    sql = "SELECT coin_id, date, price_usd FROM Crypto_prices ORDER BY date DESC LIMIT 1"

elif option == "6. Highest BTC Price (Last 365 Days)":
    sql = "SELECT price_usd, date FROM Crypto_prices WHERE coin_id = 'bitcoin' AND date >= DATE_SUB(CURDATE(), INTERVAL 365 DAY) ORDER BY price_usd DESC LIMIT 1"

elif option == "7. Avg ETH Price (Last 1 Year)":
    sql = "SELECT AVG(price_usd) FROM Crypto_prices WHERE coin_id = 'ethereum' AND date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)"

elif option == "8. Bitcoin Trend (Mar 2025)":
    sql = "SELECT date, price_usd FROM Crypto_prices WHERE coin_id = 'bitcoin' AND date BETWEEN '2025-03-01' AND '2025-03-31' ORDER BY date"

elif option == "9. Coin with Highest Avg Price":
    sql = "SELECT coin_id, AVG(price_usd) as avg_price FROM Crypto_prices WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY coin_id ORDER BY avg_price DESC LIMIT 1"

# --- OIL ---
elif option == "11. Highest Oil Price (Last 5 Years)":
    sql = "SELECT MAX(price_usd) FROM Oil_prices WHERE date >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)"

elif option == "12. Avg Oil Price per Year":
    sql = "SELECT YEAR(date) AS year, AVG(price_usd) FROM Oil_prices GROUP BY YEAR(date) ORDER BY year DESC"

elif option == "13. Oil Prices during COVID (2020)":
    sql = "SELECT date, price_usd FROM Oil_prices WHERE date BETWEEN '2020-03-01' AND '2020-04-30' ORDER BY date"

elif option == "14. Lowest Oil Price (Last 10 Years)":
    sql = "SELECT MIN(price_usd) FROM Oil_prices WHERE date >= DATE_SUB(CURDATE(), INTERVAL 10 YEAR)"

elif option == "15. Oil Price Volatility":
    sql = "SELECT YEAR(date) AS year, (MAX(price_usd) - MIN(price_usd)) as volatility FROM Oil_prices GROUP BY YEAR(date) ORDER BY year DESC"

# --- STOCKS ---
elif option == "16. S&P 500 Prices (^GSPC)":
    sql = "SELECT * FROM Stock_prices WHERE ticker = '^GSPC' ORDER BY date DESC LIMIT 100"

elif option == "17. Highest NASDAQ Close (^IXIC)":
    sql = "SELECT MAX(close) FROM Stock_prices WHERE ticker = '^IXIC'"

elif option == "18. High Volatility Days (S&P 500)":
    sql = "SELECT date, (high - low) as price_diff FROM Stock_prices WHERE ticker = '^GSPC' ORDER BY price_diff DESC LIMIT 5"

elif option == "19. Monthly Avg Closing Price":
    sql = "SELECT ticker, YEAR(date), MONTH(date), AVG(close) FROM Stock_prices GROUP BY ticker, YEAR(date), MONTH(date)"

elif option == "20. Avg Volume for Nifty (2024)":
    sql = "SELECT AVG(volume) FROM Stock_prices WHERE ticker = '^NSEI' AND YEAR(date) = 2024"

# --- CROSS MARKET JOINS ---
elif option == "21. BTC vs Oil Avg Price (2025)":
    sql = "SELECT AVG(c.price_usd) as BTC_Avg, AVG(o.price_usd) as Oil_Avg FROM Crypto_prices c JOIN Oil_prices o ON c.date = o.date WHERE c.coin_id = 'bitcoin' AND YEAR(c.date) = 2025"

elif option == "22. BTC vs S&P 500 Correlation":
    sql = "SELECT c.date, c.price_usd as BTC, s.close as SP500 FROM Crypto_prices c JOIN Stock_prices s ON c.date = s.date WHERE c.coin_id = 'bitcoin' AND s.ticker = '^GSPC' ORDER BY c.date DESC"

elif option == "23. ETH vs NASDAQ Daily (2025)":
    sql = "SELECT c.date, c.price_usd as ETH, s.close as NASDAQ FROM Crypto_prices c JOIN Stock_prices s ON c.date = s.date WHERE c.coin_id = 'ethereum' AND s.ticker = '^IXIC' AND YEAR(c.date) = 2025 ORDER BY c.date"

elif option == "24. BTC Price when Oil is High":
    sql = "SELECT o.date, o.price_usd as Oil_Price, c.price_usd as BTC_Price FROM Oil_prices o JOIN Crypto_prices c ON o.date = c.date WHERE c.coin_id = 'bitcoin' ORDER BY o.price_usd DESC LIMIT 20"

elif option == "25. Top Coins vs Nifty Trend":
    sql = "SELECT c.date, c.coin_id, c.price_usd, s.close as Nifty_Price FROM Crypto_prices c JOIN Stock_prices s ON c.date = s.date WHERE s.ticker = '^NSEI' AND c.coin_id IN ('bitcoin', 'ethereum', 'tether') ORDER BY c.date DESC"

elif option == "26. S&P 500 vs Crude Oil":
    sql = "SELECT s.date, s.close as SP500, o.price_usd as Oil FROM Stock_prices s JOIN Oil_prices o ON s.date = o.date WHERE s.ticker = '^GSPC' ORDER BY s.date DESC LIMIT 100"

elif option == "27. BTC vs Oil Correlation":
    sql = "SELECT c.price_usd as BTC, o.price_usd as Oil FROM Crypto_prices c JOIN Oil_prices o ON c.date = o.date WHERE c.coin_id = 'bitcoin'"

elif option == "28. NASDAQ vs ETH Trend":
    sql = "SELECT c.date, c.price_usd as ETH, s.close as NASDAQ FROM Crypto_prices c JOIN Stock_prices s ON c.date = s.date WHERE c.coin_id = 'ethereum' AND s.ticker = '^IXIC' ORDER BY c.date DESC LIMIT 365"

elif option == "29. Crypto vs Stock Indices (2025)":
    sql = "SELECT c.date, c.coin_id, c.price_usd, s.ticker, s.close FROM Crypto_prices c JOIN Stock_prices s ON c.date = s.date WHERE YEAR(c.date) = 2025 AND c.coin_id IN ('bitcoin', 'ethereum', 'tether') AND s.ticker IN ('^GSPC', '^IXIC', '^NSEI') ORDER BY c.date"

# --- UPDATED MASTER QUERY ---
elif option == "30. Master View (BTC, Oil, All Stocks)": # <--- Matches the dropdown now
    sql = """
    SELECT 
        c.date, 
        c.price_usd as 'Bitcoin ($)', 
        o.price_usd as 'Oil ($)', 
        s1.close as 'S&P 500', 
        s2.close as 'NASDAQ', 
        s3.close as 'Nifty 50'
    FROM Crypto_prices c
    LEFT JOIN Oil_prices o ON c.date = o.date
    LEFT JOIN Stock_prices s1 ON c.date = s1.date AND s1.ticker = '^GSPC'
    LEFT JOIN Stock_prices s2 ON c.date = s2.date AND s2.ticker = '^IXIC'
    LEFT JOIN Stock_prices s3 ON c.date = s3.date AND s3.ticker = '^NSEI'
    WHERE c.coin_id = 'bitcoin'
    ORDER BY c.date DESC 
    LIMIT 100
    """

# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------
st.subheader(f"Results for: {option}")

if sql:
        df = pd.read_sql_query(sql, connection)
        st.dataframe(df)

# Special Case: Query 10
if option == "10. BTC % Change (Sep '24 - Sep '25)":
        df_start = pd.read_sql("SELECT price_usd FROM Crypto_prices WHERE coin_id='bitcoin' AND date >= '2024-09-01' LIMIT 1", connection)
        df_end = pd.read_sql("SELECT price_usd FROM Crypto_prices WHERE coin_id='bitcoin' AND date <= '2025-09-30' ORDER BY date DESC LIMIT 1", connection)
        
        if not df_start.empty and not df_end.empty:
            start_price = df_start.iloc[0,0]
            end_price = df_end.iloc[0,0]
            
            if start_price != 0:
                change = ((end_price - start_price) / start_price) * 100
                c1, c2, c3 = st.columns(3)
                c1.metric("Start Price (Sep 2024)", f"${start_price:,.2f}")
                c2.metric("End Price (Sep 2025)", f"${end_price:,.2f}")
                c3.metric("Percentage Change", f"{change:.2f}%")
