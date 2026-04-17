class DataWriter:
    def write(self, df, path: str):
        df.coalesce(1).write.mode("overwrite").csv(path, header=True)