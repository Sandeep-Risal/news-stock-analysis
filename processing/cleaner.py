from pyspark.sql.functions import col, to_date, expr
from pyspark.sql import DataFrame
from pyspark.sql.types import DoubleType

class DataCleaner:
    def clean_news_data(self, df: DataFrame):
        return (df.select("headline", "date", "stock")  # ✅ keep stock column
                .dropna()
                .withColumn("date", expr("try_cast(substring(date, 1, 10) as date)"))
                .filter(col("date").isNotNull())
        )

    def clean_stock_data(self, df: DataFrame):
        print("Stock columns:", df.columns)
        return (df.select(
                    to_date(col("Date")).alias("date"),
                    col("Open").cast(DoubleType()),
                    col("Close").cast(DoubleType())
                  )
                  .dropna()
        )