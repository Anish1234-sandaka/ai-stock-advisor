# stock_tools.py
import yfinance as yf
from crewai_tools import WebsiteSearchTool
web_tool = WebsiteSearchTool()


def get_recent_performance(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="6mo")

def get_long_term_performance(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="10y") 

def is_valid_ticker(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info and 'shortName' in info
    except:
        return False
    
def summarize_stock_trend(ticker, horizon):
    try:
        if horizon == "short-term":
            df = get_recent_performance(ticker)
        else:
            df = get_long_term_performance(ticker)

        if df.empty:
            return "No historical data available."

        start_price = df['Close'].iloc[0]
        end_price = df['Close'].iloc[-1]
        percent_change = ((end_price - start_price) / start_price) * 100

        trend_summary = f"The stock price changed by {percent_change:.2f}% over the {horizon} period."
        return trend_summary

    except Exception as e:
        return f"Error analyzing stock trend: {e}"

def get_stock_history(ticker, horizon):
    try:
        stock = yf.Ticker(ticker)
        if horizon == "short-term":
            return stock.history(period="6mo")
        else:
            return stock.history(period="10y")
    except Exception as e:
        return None
    
def fetch_stock_news(ticker):
    try:
        query = f"{ticker} stock news"
        result = web_tool.run(query)
        return result if result else "No relevant news found."
    except Exception as e:
        return f"News fetch error: {e}"
