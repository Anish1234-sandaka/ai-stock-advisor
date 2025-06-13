import streamlit as st
import matplotlib.pyplot as plt
from main import crew
from stock_tools import is_valid_ticker, summarize_stock_trend, get_stock_history, fetch_stock_news

# --- Page Configuration ---
st.set_page_config(page_title="AI Stock Advisor", layout="wide")

# --- Custom Header ---
st.markdown("<h1 style='text-align: center;'>📈 AI Stock Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze a stock and get personalized short- or long-term investment advice powered by AI.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Sidebar Info ---
st.sidebar.title("📘 About")
st.sidebar.markdown("""
This app provides stock investment insights using:
- Price history and technical trend analysis
- Real-time financial news
- AI-generated recommendations (CrewAI)
""")

# --- Input Fields ---
col1, col2 = st.columns(2)
with col1:
    ticker = st.text_input("🔎 Enter stock ticker (e.g., AAPL)")

with col2:
    time_horizon = st.selectbox("🕒 Investment horizon:", ["short-term", "long-term"])

# --- Analyze Button ---
if st.button("🚀 Analyze"):
    if not is_valid_ticker(ticker):
        st.error("❌ Invalid or fake stock ticker. Please enter a real one.")
    else:
        with st.spinner("⏳ Analyzing stock..."):
            # 1. Price History Chart
            history = get_stock_history(ticker, time_horizon)
            if history is not None and not history.empty:
                st.subheader(f"📊 {ticker.upper()} Price History ({'6mo' if time_horizon == 'short-term' else '10y'})")
                fig, ax = plt.subplots()
                ax.plot(history.index, history['Close'], label="Close Price")
                ax.set_xlabel("Date")
                ax.set_ylabel("Price (USD)")
                ax.set_title(f"{ticker.upper()} Closing Prices")
                ax.legend()
                st.pyplot(fig)
            else:
                st.warning("⚠️ Could not load price history.")

            # 2. Get trend summary and news context
            trend_summary = summarize_stock_trend(ticker, time_horizon)
            news_context = fetch_stock_news(ticker)

            # 3. AI Analysis (Crew)
            result = crew.kickoff(inputs={
                "ticker": ticker,
                "time_horizon": time_horizon,
                "trend_data": trend_summary,
                "news_context": news_context
            })

            # 4. Output result
            try:
                advisor_output = result.tasks_output[-1].raw
            except Exception as e:
                advisor_output = f"⚠️ Could not extract advisor output. Error: {e}"

            st.success("✅ Analysis complete!")
            st.markdown(f"### 🧠 Investment Recommendation\n{advisor_output}")
            st.markdown("---")

            # 5. Optional Details
            with st.expander("📄 Trend Summary and News Context"):
                st.markdown("#### 📈 Trend Summary")
                st.markdown(trend_summary)
                st.markdown("#### 📰 News Context")
                st.markdown(news_context)

            # 6. Download Button
            file_contents = f"# AI Stock Advisor Report for {ticker.upper()}\n\n"
            file_contents += f"## Investment Horizon: {time_horizon}\n\n"
            file_contents += f"## Trend Summary:\n{trend_summary}\n\n"
            file_contents += f"## Recommendation:\n{advisor_output}"

            st.download_button(
                label="📥 Download Report",
                data=file_contents,
                file_name=f"{ticker.upper()}_investment_report.md",
                mime="text/markdown"
            )
