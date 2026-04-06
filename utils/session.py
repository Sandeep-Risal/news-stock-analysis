from pyspark.sql import SparkSession

class SparkSessionBuilder:
    @staticmethod
    def get_session(app_name = "News_Stock_Analysis"):
        spark = SparkSession.builder.appName(app_name).getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        return spark