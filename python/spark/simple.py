from pyspark.sql import SparkSession
# import findspark

# findspark.init()

spark = SparkSession.builder.appName("Test").getOrCreate()

df = spark.createDataFrame([(1, "Rodrigo"), (2, "Reyes")], ["id", "nombre"])
print(df.collect())   # en vez de df.show()
