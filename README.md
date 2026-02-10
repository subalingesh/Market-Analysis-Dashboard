📈 Financial Market Analysis Dashboard
A full-stack data analysis application that tracks, compares, and visualizes trends across Cryptocurrencies, Commodities (Crude Oil), and Global Stock Indices (S&P 500, NASDAQ, Nifty 50). Built with Python, Streamlit, and MySQL, this project demonstrates an end-to-end data pipeline—from raw data ingestion to interactive SQL-based analytics.

🚀 Project Overview
This dashboard bridges the gap between different financial markets, allowing users to analyze correlations (e.g., Does Bitcoin move with the S&P 500?) and view historical trends in a unified interface.

Key Features
🌍 Global Market Snapshot: A unified view comparing Bitcoin, Crude Oil, S&P 500, NASDAQ, and Nifty 50.

📊 SQL-Powered Analytics: 30+ pre-defined complex SQL queries to uncover insights (e.g., "High Volatility Days," "Asset Correlations," "Price Trends during COVID").

📉 Normalized Trend Comparison: Visualizes assets on a 0-1 scale to compare performance patterns despite vastly different price ranges.

🛠️ Robust ETL Pipeline: Custom Python scripts to clean, transform, and load (ETL) raw financial data into a structured MySQL relational database.

⚡ Fault-Tolerant Data Handling: Handles missing data (holidays/weekends) using SQL LEFT JOIN logic to ensure continuous analysis.

🏗️ Tech Stack & Architecture
Frontend: Streamlit (Interactive Web Dashboard)

Backend Database: MySQL (Relational Data Storage)

Data Processing: Pandas & NumPy (Data Cleaning & Transformation)

Database Connector: PyMySQL (Python-to-SQL Bridge)

Visualization: Streamlit Native Charts (Line, Scatter, Metrics)

💾 Database Schema
The project uses a normalized relational database (market_analysis_data_structure) with the following tables:

Cryptocurrencies: Metadata for coins (Symbol, Name, Market Cap, Supply).

Crypto_prices: Daily historical OHLC data for cryptocurrencies.

Oil_prices: Historical daily Crude Oil prices.

Stock_prices: Historical daily data for global indices (^GSPC, ^IXIC, ^NSEI).
