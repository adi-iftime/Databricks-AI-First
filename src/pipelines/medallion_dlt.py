import dlt
from pyspark.sql import functions as F


@dlt.table(
    comment="Raw events ingested from JSON files in the bronze volume",
    table_properties={"quality": "bronze"},
)
def bronze_events():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .load("/Volumes/cursorfun/default/bronze_ingest/")
    )


@dlt.table(
    comment="Cleaned and validated events",
    table_properties={"quality": "silver"},
)
@dlt.expect_or_fail("event_id_not_null", "event_id IS NOT NULL")
def silver_events():
    df = dlt.read_stream("bronze_events")

    if "_metadata" in df.columns:
        source_file_col = F.col("_metadata.file_path")
    else:
        source_file_col = F.lit(None).cast("string")

    cleaned = (
        df.withColumn("event_id", F.coalesce(F.col("event_id"), F.col("id")))
        .withColumn("payload", F.col("payload"))
        .withColumn("source_file", source_file_col)
        .withColumn("processed_at", F.current_timestamp())
        .select("event_id", "payload", "source_file", "processed_at")
    )
    return cleaned


@dlt.table(
    comment="Daily event count aggregations",
    table_properties={"quality": "gold"},
)
def gold_daily_event_counts():
    df = dlt.read("silver_events")
    return df.groupBy(F.date_trunc("day", "processed_at").alias("event_date")).agg(
        F.count("*").alias("event_count"),
        F.countDistinct("event_id").alias("unique_events"),
    )
