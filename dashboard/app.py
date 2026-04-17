import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

st.set_page_config(page_title="News & Stock Analysis", layout="wide")
st.title("📊 News Sentiment vs Stock Price Analysis")
st.markdown("*Exploring how news headlines relate to stock market movements (2019–2022)*")

# Load data
df = pd.read_csv("../project-output/agg-output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

df = df.groupby("date").agg(
    avg_sentiment=("avg_sentiment", "first"),
    Open=("Open", "mean"),
    Close=("Close", "mean"),
    return_=("return", "mean")
).reset_index()
df = df.rename(columns={"return_": "return"})

# Rolling average for smoother sentiment
df["sentiment_7d"] = df["avg_sentiment"].rolling(7).mean()
df["sentiment_30d"] = df["avg_sentiment"].rolling(30).mean()

# --- EXPLAINER BOX ---
with st.expander("🤔 What is this dashboard? (Click to learn more)"):
    st.markdown("""
    This dashboard analyzes whether **news headlines** can predict **stock price movements**.

    - **Sentiment score**: A number from -1 (very negative news) to +1 (very positive news), calculated from headlines using NLP.
    - **Stock price**: The closing price of a stock on a given day.
    - **Return**: How much the stock price changed (%) from one day to the next.
    - **Correlation**: A number from -1 to +1 showing how closely two things move together. Near 0 = no relationship.
    """)

# --- COMBINED CHART ---
st.subheader("📈 Stock Price vs News Sentiment Over Time")
st.caption("The blue area shows stock price. The orange line shows the 30-day average news sentiment.")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
fig.patch.set_facecolor("#0e1117")
for ax in [ax1, ax2]:
    ax.set_facecolor("#0e1117")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444")

ax1.fill_between(df["date"], df["Close"], alpha=0.4, color="#1f77b4")
ax1.plot(df["date"], df["Close"], color="#1f77b4", linewidth=0.8)
ax1.set_ylabel("Stock Price ($)", color="white")
ax1.set_title("Stock Price", color="white", fontsize=11)

ax2.fill_between(df["date"], df["sentiment_7d"], alpha=0.3,
                 where=df["sentiment_7d"] >= 0, color="#2ecc71", label="Positive sentiment")
ax2.fill_between(df["date"], df["sentiment_7d"], alpha=0.3,
                 where=df["sentiment_7d"] < 0, color="#e74c3c", label="Negative sentiment")
ax2.plot(df["date"], df["sentiment_30d"], color="orange", linewidth=1.5, label="30-day avg")
ax2.axhline(0, color="#888", linewidth=0.8, linestyle="--")
ax2.set_ylabel("Sentiment Score", color="white")
ax2.set_title("News Sentiment (green = positive, red = negative)", color="white", fontsize=11)
ax2.legend(facecolor="#1e1e1e", labelcolor="white", fontsize=8)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
fig.autofmt_xdate()
plt.tight_layout()
st.pyplot(fig)

# --- CORRELATION SECTION ---
st.subheader("🔗 Does News Sentiment Predict Stock Returns?")
col1, col2, col3 = st.columns(3)

corr = df["avg_sentiment"].corr(df["return"])
col1.metric("Correlation (raw)", f"{corr:.4f}", help="How closely daily sentiment matches daily returns")

corr_7d = df["sentiment_7d"].corr(df["return"])
col2.metric("Correlation (7-day avg)", f"{corr_7d:.4f}")

corr_30d = df["sentiment_30d"].corr(df["return"])
col3.metric("Correlation (30-day avg)", f"{corr_30d:.4f}")

# Plain English interpretation
if abs(corr) < 0.05:
    interp = "🟡 **Verdict:** Weak but non-zero correlation detected. This aligns with the **Efficient Market Hypothesis** — in efficient markets, publicly available news is quickly priced in, leaving little predictive power for next-day returns."
elif abs(corr) < 0.2:
    interp = "🟠 **Verdict:** There is a **weak relationship** between news sentiment and stock returns."
else:
    interp = "🟢 **Verdict:** There is a **meaningful relationship** between news sentiment and stock returns."
st.markdown(interp)

# --- SCATTER PLOT ---
st.subheader("🔵 Sentiment vs Daily Return (Scatter)")
st.caption("Each dot is one day. If news sentiment predicted returns well, you'd see a clear diagonal pattern — but here it's mostly random.")

fig3, ax3 = plt.subplots(figsize=(8, 4))
fig3.patch.set_facecolor("#0e1117")
ax3.set_facecolor("#0e1117")
ax3.tick_params(colors="white")
ax3.xaxis.label.set_color("white")
ax3.yaxis.label.set_color("white")
for spine in ax3.spines.values():
    spine.set_edgecolor("#444")

ax3.scatter(df["avg_sentiment"], df["return"], alpha=0.15, s=8, color="#1f77b4")
# Trend line
m, b = np.polyfit(df["avg_sentiment"].dropna(), df["return"].dropna(), 1)
x_line = np.linspace(df["avg_sentiment"].min(), df["avg_sentiment"].max(), 100)
ax3.plot(x_line, m * x_line + b, color="orange", linewidth=1.5, label=f"Trend (slope={m:.4f})")
ax3.axhline(0, color="#888", linewidth=0.8, linestyle="--")
ax3.axvline(0, color="#888", linewidth=0.8, linestyle="--")
ax3.set_xlabel("News Sentiment Score")
ax3.set_ylabel("Daily Stock Return")
ax3.legend(facecolor="#1e1e1e", labelcolor="white")
st.pyplot(fig3)

# --- TOP/BOTTOM SENTIMENT DAYS ---
st.subheader("📰 Most Positive & Most Negative News Days")
st.caption("These are the days with the most extreme sentiment scores. Check if big sentiment spikes lined up with notable stock moves.")

col_pos, col_neg = st.columns(2)

with col_pos:
    st.markdown("**🟢 Top 10 Most Positive Days**")
    top_pos = df.nlargest(10, "avg_sentiment")[["date", "avg_sentiment", "Close", "return"]].copy()
    top_pos["date"] = top_pos["date"].dt.strftime("%Y-%m-%d")
    top_pos.columns = ["Date", "Sentiment", "Close Price", "Return (%)"]
    top_pos["Return (%)"] = (top_pos["Return (%)"] * 100).round(2)
    top_pos["Sentiment"] = top_pos["Sentiment"].round(3)
    st.dataframe(top_pos, hide_index=True, use_container_width=True)

with col_neg:
    st.markdown("**🔴 Top 10 Most Negative Days**")
    top_neg = df.nsmallest(10, "avg_sentiment")[["date", "avg_sentiment", "Close", "return"]].copy()
    top_neg["date"] = top_neg["date"].dt.strftime("%Y-%m-%d")
    top_neg.columns = ["Date", "Sentiment", "Close Price", "Return (%)"]
    top_neg["Return (%)"] = (top_neg["Return (%)"] * 100).round(2)
    top_neg["Sentiment"] = top_neg["Sentiment"].round(3)
    st.dataframe(top_neg, hide_index=True, use_container_width=True)

# --- RAW DATA ---
with st.expander("📋 View Raw Data"):
    st.dataframe(df[["date", "avg_sentiment", "Open", "Close", "return"]].head(50), use_container_width=True)