import streamlit as st
import yfinance as yf

st.set_page_config(page_title="AI Stock Assistant", layout="wide")

st.title("Stock App")

st.markdown("### 🔍 Search any stock and get insights instantly")

stock = st.text_input("Enter stock (apple, tesla, nifty)")

time_range = st.selectbox(
    "Select Time Range",
    ["1mo", "3mo", "6mo", "1y"]
)

mapping = {
    "apple": "AAPL",
    "tesla": "TSLA",
    "nifty": "^NSEI"
}

if st.button("Check"):
    if stock.strip() == "":
        st.warning("Enter stock name")
    else:
        name = stock.lower()

        if name in mapping:
            data = yf.download(mapping[name], period=time_range)

            if not data.empty:

                # Moving averages
                data["MA20"] = data["Close"].rolling(20).mean()
                data["MA50"] = data["Close"].rolling(50).mean()

                ma20 = data["MA20"].iloc[-1]
                ma50 = data["MA50"].iloc[-1]

                # Suggestion
                if ma20 > ma50:
                    st.success("📈 BUY (Uptrend)")
                elif ma20 < ma50:
                    st.error("📉 SELL (Downtrend)")
                else:
                    st.info("⚖️ HOLD")

                # Price
                price = data["Close"].iloc[-1].item()
                st.success("Price: " + str(round(price, 2)))

                # Chart
                st.line_chart(data["Close"])

            else:
                st.error("No data")

        else:
            st.error("Not supported")