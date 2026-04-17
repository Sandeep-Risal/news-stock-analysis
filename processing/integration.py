from pyspark.sql.functions import avg
from pyspark.sql import DataFrame

class DataIntegrator:
    def aggregate_sentiment(self, df: DataFrame):
        # ✅ Group by BOTH date AND stock ticker instead of just date
        result = df.groupBy("date", "stock").agg(
            avg("sentiment").alias("avg_sentiment")
        )
        print(f"Sentiment aggregated: {result.count()} unique date/stock combinations")
        return result

    def join_data(self, sentiment_df: DataFrame, stock_df: DataFrame):
        result = sentiment_df.join(stock_df, "date", "inner")
        print(f"After join: {result.count()} rows")
        return result