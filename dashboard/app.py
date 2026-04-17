import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("📊 News Sentiment vs Stock Price Analysis")

# Load data
df = pd.read_csv("../project-output/agg-output.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Sort
df = df.sort_values("date")

# --- STOCK PRICE TREND ---
st.subheader("📈 Stock Price Trend")
fig1, ax1 = plt.subplots()
ax1.plot(df["date"], df["Close"])
ax1.set_xlabel("Date")
ax1.set_ylabel("Stock Price")
st.pyplot(fig1)

# --- SENTIMENT TREND ---
st.subheader("📊 Sentiment Trend")
fig2, ax2 = plt.subplots()
ax2.plot(df["date"], df["avg_sentiment"])
ax2.set_xlabel("Date")
ax2.set_ylabel("Sentiment")
st.pyplot(fig2)

# --- CORRELATION ---
st.subheader("🔗 Correlation")
corr = df["avg_sentiment"].corr(df["return"])
st.write(f"Correlation between sentiment and return: {corr:.4f}")

# --- TABLE VIEW ---
st.subheader("📋 Data Preview")
st.dataframe(df.head(20))