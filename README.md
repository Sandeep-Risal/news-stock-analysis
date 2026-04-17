# 📊 End-to-End Big Data System for News Sentiment & Stock Analysis

## 🚀 Overview

This project builds a scalable big data pipeline to analyze the impact of news sentiment on stock price trends using Hadoop and PySpark.

## 🧱 Tech Stack

- Apache Hadoop (HDFS)
- PySpark
- Python (TextBlob for NLP)
- Streamlit (Dashboard)

## ⚙️ Pipeline

1. Data ingestion from HDFS
2. Data cleaning and preprocessing
3. Sentiment analysis on news headlines
4. Feature engineering on stock data
5. Data integration (join on date)
6. Correlation analysis
7. Visualization dashboard

## 📊 Output

- Sentiment trends
- Stock price trends
- Correlation analysis

## ▶️ How to Run

### 1. Install dependencies

pip install -r requirements.txt

### 2. Run PySpark pipeline

spark-submit main.py

### 3. Launch dashboard

cd dashboard
streamlit run app.py

## 📌 Note

Dataset files are not included due to size. Place them in HDFS at:
hdfs:///project/

## 💡 Author

Sandeep Risal
