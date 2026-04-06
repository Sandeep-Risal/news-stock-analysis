from textblob import TextBlob
from pyspark.sql.functions import udf, col
from pyspark.sql.types import FloatType

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_udf = udf(self.get_sentiment, FloatType())
    
    def get_sentiment(self, text):
        return TextBlob(text).sentiment.polarity
    
    def apply_sentiment(self, df):
        return df.withColumn("sentiment", self.sentiment_udf(col("headline")))


