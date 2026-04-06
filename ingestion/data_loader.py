class DataLoader:
    def __init__(self, spark):
        self.spark = spark
    
    def load_data (self, path :str, fileType:str):
        match fileType:
            case "json":
                return self.spark.read.json(path)
            case "csv":
                return self.spark.read.csv(path , header=True, inferSchema = True)
            case _:
                return ValueError(f"Invalid file type: {fileType}")


    
