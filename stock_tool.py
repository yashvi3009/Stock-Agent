import yfinance as yf
from datetime import date, timedelta
import matplotlib.pyplot as plt
import io
import base64

def fetch_stock_data(tickers):
    if isinstance(tickers, str):  
        tickers = [tickers]  

    end_date = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=5)).strftime("%Y-%m-%d")

    try:
        data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')

        if data.empty:
            return {"error": f"No data available for {', '.join(tickers)}"}

        # Convert Timestamp to string
        close_prices = {
            ticker: {str(date): price for date, price in data[ticker]["Close"].dropna().items()} 
            for ticker in tickers if ticker in data
        }

        # Generate plot
        fig, ax = plt.subplots(figsize=(8, 4))
        for ticker in tickers:
            if ticker in data:
                ax.plot(data[ticker].index, data[ticker]["Close"], label=ticker)
        
        ax.set_title("Stock Closing Prices (Last 5 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Closing Price")
        ax.legend()
        plt.xticks(rotation=45)

        # Convert plot to base64 image
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format="png")
        img_buf.seek(0)
        img_base64 = base64.b64encode(img_buf.getvalue()).decode()

        return {
            "data": close_prices,
            "graph": img_base64
        }

    except Exception as e:
        return {"error": f"Error fetching data: {str(e)}"}
