import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.title("📊 Stock Analysis Agent")

# User Inputs
tickers_input = st.text_input("Enter stock ticker (e.g., MSFT, AAPL):").strip().upper()
query_input = st.selectbox("Select financial metric:", 
                           ["Market Cap", "P/E Ratio", "Dividend Yield", "EPS", "Revenue"])

# Custom Time Period
time_option = st.selectbox("Select time range:", 
                           ["Last 5 Days", "Last 30 Days", "Last 6 Months", "Last 1 Year", "Custom Date Range"])

start_date, end_date = None, None

if time_option == "Custom Date Range":
    start_date = st.date_input("Start Date", datetime.today() - timedelta(days=365))
    end_date = st.date_input("End Date", datetime.today())

if st.button("Submit") and tickers_input:
    try:
        stock = yf.Ticker(tickers_input)

        # Set time period
        if time_option == "Last 5 Days":
            period = "5d"
            hist = stock.history(period=period)
        elif time_option == "Last 30 Days":
            period = "1mo"
            hist = stock.history(period=period)
        elif time_option == "Last 6 Months":
            period = "6mo"
            hist = stock.history(period=period)
        elif time_option == "Last 1 Year":
            period = "1y"
            hist = stock.history(period=period)
        elif time_option == "Custom Date Range" and start_date and end_date:
            hist = stock.history(start=start_date, end=end_date)
        else:
            st.error("Invalid date range selected.")
            hist = None
        
        if hist is not None and not hist.empty:
            # 📈 Stock Data
            tab1, tab2, tab3 = st.tabs(["📈 Stock Data", "📊 Stock Graph", "📌 Financial Insights"])
            
            with tab1:
                st.subheader(f"{tickers_input} - Stock Data")
                st.write(hist[['Open', 'Close', 'Volume']])
            
            # 📊 Stock Graph
            with tab2:
                st.subheader(f"{tickers_input} Closing Prices")
                fig, ax = plt.subplots()
                hist['Close'].plot(ax=ax, title=f"{tickers_input} Closing Prices ({time_option})")
                st.pyplot(fig)

            # 📌 Financial Insights
            with tab3:
                st.subheader("Financial Insights")
                info = stock.info
                if query_input == "Market Cap":
                    st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
                elif query_input == "P/E Ratio":
                    st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                elif query_input == "Dividend Yield":
                    st.write(f"**Dividend Yield:** {info.get('dividendYield', 'N/A')}")
                elif query_input == "EPS":
                    st.write(f"**Earnings Per Share (EPS):** {info.get('trailingEps', 'N/A')}")
                elif query_input == "Revenue":
                    st.write(f"**Revenue:** {info.get('totalRevenue', 'N/A')}")
        else:
            st.warning("No data available for the selected period.")

    except Exception as e:
        st.error(f"Error fetching data for {tickers_input}: {e}")
