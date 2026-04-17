from textblob import TextBlob
from pyspark.sql.functions import udf, col
from pyspark.sql.types import FloatType
from pyspark.sql import DataFrame

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_udf = udf(self._get_sentiment, FloatType())

    def _get_sentiment(self, text):
        if not text:         
            return 0.0
        try:
            return float(TextBlob(text).sentiment.polarity)
        except:
            return 0.0        

    def apply_sentiment(self, df: DataFrame):
        return df.withColumn("sentiment", self.sentiment_udf(col("headline")))