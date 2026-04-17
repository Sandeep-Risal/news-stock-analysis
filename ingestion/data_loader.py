from pyspark.sql import SparkSession

class DataLoader:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def load_data(self, path: str, file_type: str):
        match file_type:
            case "json":
                return self.spark.read.option("multiLine", "false").json(path)
            case "csv":
                return self.spark.read.csv(path, header=True, inferSchema=True)
            case _:
                raise ValueError(f"Unsupported file type: {file_type}")  # ✅ raise not return