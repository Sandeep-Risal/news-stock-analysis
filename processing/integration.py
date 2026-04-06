from pyspark.sql.functions import avg

class DataIntegrator:
    def aggregate_sentiment(self, df):
        return df.groupBy("date").agg(avg("sentiment").alias("avg_sentiment"))
    
    def join_data(self, sentiment_df, stock_df):
        return sentiment_df.join(stock_df, "date")

