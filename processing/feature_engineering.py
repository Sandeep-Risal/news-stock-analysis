from pyspark.sql.functions import col
from pyspark.sql import DataFrame

class FeatureEngineer:
    def add_stock_features(self, df:DataFrame):
        return df.withColumn("return", (col("Close") - col("Open")) / col("Open"))
