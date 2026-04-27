from analysis.analyzer import Analyzer
from output.writer import DataWriter
from processing.cleaner import DataCleaner
from processing.feature_engineering import FeatureEngineer
from processing.integration import DataIntegrator
from processing.sentiment import SentimentAnalyzer
from utils.session import SparkSessionBuilder
from config.config import Config
from ingestion.data_loader import DataLoader
def main():
    spark = SparkSessionBuilder.get_session(app_name="News_Stock_Analysis")

    # Load Data
    loader = DataLoader(spark)
    news_df = loader.load_data(Config.NEWS_HDFS_PATH , "csv")
    stock_df = loader.load_data(Config.STOCK_HDFS_PATH , "csv")

    #Clean
    cleaner = DataCleaner()
    news_df = cleaner.clean_news_data(news_df)
    stock_df = cleaner.clean_stock_data(stock_df)

    print("=== NEWS SAMPLE ===")
    news_df.show(3)
    print("News date range:")
    news_df.selectExpr("min(date)", "max(date)").show()

    print("=== STOCK SAMPLE ===")
    stock_df.show(3)
    print("Stock date range:")
    stock_df.selectExpr("min(date)", "max(date)").show()


    #Sentiment
    sentiment = SentimentAnalyzer()
    news_df = sentiment.apply_sentiment(news_df)
    
    #Feature Engineering
    feature_engineer = FeatureEngineer()
    stock_df = feature_engineer.add_stock_features(stock_df)

    #Integration
    integrator = DataIntegrator()
    daily_sentiment = integrator.aggregate_sentiment(news_df)
    final_df = integrator.join_data(daily_sentiment, stock_df)

    print("=== SENTIMENT SAMPLE ===")
    daily_sentiment.show(3)
    print("Sentiment row count:", daily_sentiment.count())

    #Analysis
    analyzer = Analyzer()
    corr = analyzer.compute_correlation(final_df)
    print("Correlation: ", corr)

    print("Final DF count:", final_df.count())
    final_df.printSchema()
    final_df.show(5)
    daily_sentiment.show(5)
    stock_df.show(5)

    #Save
    writer = DataWriter()
    writer.write(final_df , Config.OUTPUT_PATH)

    spark.stop()

if __name__ == "__main__":
    main()