class DataWriter:
    def write(self, df, path):
        df.write.mode("overwrite").csv(path, header=True)