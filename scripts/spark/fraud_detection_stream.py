from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, LongType

# Define the schema of the transaction data
schema = StructType() \
    .add("transaction_id", StringType()) \
    .add("user_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("type", StringType()) \
    .add("location", StringType()) \
    .add("timestamp", LongType())

# Initialize Spark session
spark = SparkSession.builder \
    .appName("FraudDetectionStream") \
    .getOrCreate()

# Set log level to reduce verbosity
spark.sparkContext.setLogLevel("WARN")

# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "bank_transactions") \
    .load()

# Convert Kafka value from binary to JSON
json_df = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# Define simple fraud rule: flag transactions over $900
fraud_df = json_df.filter(col("amount") > 900)

# Write flagged transactions to console
query = fraud_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
