from pyspark.sql.functions import col

class FeatureEngineer:
    def add_stock_features(self, df):
        return df.withColumn("return", (col("Close") - col("Open")) / col("Open"))
