from pathlib import Path
import os
from dotenv import load_dotenv

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    count,
    sum,
    avg
)


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def create_spark_session():
    spark = (
        SparkSession.builder
        .appName("TeleConnectDataEngineering")
        .config(
            "spark.jars.packages",
            "org.postgresql:postgresql:42.7.8"
        )
        .config(
            "spark.hadoop.fs.file.impl",
            "org.apache.hadoop.fs.LocalFileSystem"
        )
        .config(
            "spark.hadoop.fs.permissions.umask-mode",
            "000"
        )
        .getOrCreate()
    )

    return spark


def process_recharges(spark):
    recharge_file = PROCESSED_DIR / "recharges_valid.csv"

    print("=" * 60)
    print("READING RECHARGE DATA")
    print("=" * 60)

    df = spark.read.csv(
        str(recharge_file),
        header=True,
        inferSchema=True
    )

    print("Total recharge records:", df.count())

    print()
    print("Recharge Data:")
    df.show(5)

    successful_recharges = df.filter(
        df.status == "SUCCESS"
    )

    customer_recharge_summary = (
        successful_recharges
        .groupBy("customer_id")
        .agg(
            count("recharge_id").alias("successful_recharges"),
            sum("amount").alias("total_recharge_amount"),
            avg("amount").alias("average_recharge_amount")
        )
        .orderBy("customer_id")
    )

    print()
    print("=" * 60)
    print("CUSTOMER RECHARGE SUMMARY")
    print("=" * 60)

    customer_recharge_summary.show(10)

    return customer_recharge_summary

def process_usage(spark):
    usage_file = PROCESSED_DIR / "usage_valid.csv"

    print()
    print("=" * 60)
    print("READING USAGE DATA")
    print("=" * 60)

    df = spark.read.csv(
        str(usage_file),
        header=True,
        inferSchema=True
    )

    print("Total usage records:", df.count())

    print()
    print("Usage Data:")
    df.show(5)

    customer_usage_summary = (
        df
        .groupBy("customer_id")
        .agg(
            sum("data_used_gb").alias("total_data_used_gb"),
            sum("voice_minutes").alias("total_voice_minutes"),
            sum("sms_count").alias("total_sms"),
            count("usage_id").alias("usage_records")
        )
        .orderBy("customer_id")
    )

    print()
    print("=" * 60)
    print("CUSTOMER USAGE SUMMARY")
    print("=" * 60)

    customer_usage_summary.show(10)
    return customer_usage_summary
def write_customer_360_to_postgresql(customer_360_df):
    load_dotenv()

    jdbc_url = (
        f"jdbc:postgresql://"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    connection_properties = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "driver": "org.postgresql.Driver"
    }

    print()
    print("=" * 60)
    print("WRITING CUSTOMER 360 DATA TO POSTGRESQL")
    print("=" * 60)

    customer_360_df.write \
        .jdbc(
            url=jdbc_url,
            table="dw.customer_360",
            mode="overwrite",
            properties=connection_properties
        )

    print("Customer 360 data successfully written to dw.customer_360")

if __name__ == "__main__":
    spark = create_spark_session()

    print("=" * 60)
    print("PYSPARK STARTED SUCCESSFULLY")
    print("=" * 60)

    print("Spark Version:", spark.version)

    recharge_summary = process_recharges(spark)
    usage_summary = process_usage(spark)

    customer_360_base = (
    recharge_summary
    .join(
        usage_summary,
        on="customer_id",
        how="left"
     )
     )
print()
print("=" * 60)
print("CUSTOMER 360 BASE DATASET")
print("=" * 60)

customer_360_base.show(10)

write_customer_360_to_postgresql(customer_360_base)

spark.stop()