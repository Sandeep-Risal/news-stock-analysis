class DataWriter:
    def write(self, df, path):
        df.coalesce(1).write.mode("overwrite").csv(path, header=True)