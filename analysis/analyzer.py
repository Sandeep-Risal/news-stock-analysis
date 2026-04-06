class Analyzer:
    def compute_correlation(self, df):
        return df.stat.corr("avg_sentiment", "return")

