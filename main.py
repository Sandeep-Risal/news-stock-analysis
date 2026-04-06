from utils.session import SparkSessionBuilder
from config.config import Config
from ingestion.data_loader import DataLoader
def main():
    spark = SparkSessionBuilder.get_session(app_name="News_Stock_Analysis")

    # Load Data
    loader = DataLoader(spark)
    news_df = loader.load_data(Config.NEWS_HDFS_PATH , "json")
    print("News Data Loaded Successfully" , news_df.count())

    spark.stop()

if __name__ == "__main__":
    main()