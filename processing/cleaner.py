from pyspark.sql.functions import col, to_date
from pyspark.sql import DataFrame

class DataCleaner:
    def clean_news_data (self, df:DataFrame):
        return df.select("headline", "date").dropna().withColumn("date", to_date(col("date")))
    
    def clean_stock_data (self, df:DataFrame):
        return df.select("Date", "Open" , "Close").dropna().withColumn("date" , to_date(col("Date")))