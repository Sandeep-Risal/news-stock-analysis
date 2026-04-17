from pyspark.sql import DataFrame

class Analyzer:
    def compute_correlation(self, df: DataFrame):
        corr = df.stat.corr("avg_sentiment", "return")
        print(f"Correlation between avg_sentiment and return: {corr:.4f}")
        return corr