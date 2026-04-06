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
    news_df = loader.load_data(Config.NEWS_HDFS_PATH , "json")
    stock_df = loader.load_data(Config.STOCK_HDFS_PATH , "csv")

    #Clean
    cleaner = DataCleaner()
    news_df = cleaner.clean_news_data(news_df)
    stock_df = cleaner.clean_stock_data(stock_df)

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

    #Analysis
    analyzer = Analyzer()
    corr = analyzer.compute_correlation(final_df)
    print("Correlation: ", corr)

    #Save
    writer = DataWriter()
    writer.write(final_df , Config.OUTPUT_PATH)

    spark.stop()

if __name__ == "__main__":
    main()