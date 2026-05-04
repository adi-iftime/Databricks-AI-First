"""
Medallion Delta Live Tables pipeline: Bronze (raw) -> Silver (cleansed) -> Gold (aggregates).

Configure bundle.catalog and bundle.bronze_source_path via pipeline configuration in databricks.yml.
"""

from __future__ import annotations

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import LongType, StringType, StructField, StructType
from pyspark.sql.window import Window

# Explicit schema so Auto Loader can start when the bronze path is empty (no CF_EMPTY_DIR_FOR_SCHEMA_INFERENCE).
# Cannot combine full `.schema(...)` with `cloudFiles.schemaEvolutionMode=addNewColumns` (use schemaHints for that).
# New top-level fields later → extend `_BRONZE_SCHEMA` or switch to `cloudFiles.schemaHints` per Databricks docs.
# Fixtures under fixtures/ — upload *.jsonl to bundle.bronze_source_path (JSON Lines, not CSV).
_BRONZE_SCHEMA = StructType(
    [
        StructField("event_id", StringType(), True),
        StructField("id", StringType(), True),
        StructField(
            "payload",
            StructType(
                [
                    StructField("x", LongType(), True),
                    StructField("source", StringType(), True),
                    StructField("value", LongType(), True),
                ]
            ),
            True,
        ),
    ]
)


def _bronze_path() -> str:
    return spark.conf.get(
        "bundle.bronze_source_path",
        "/Volumes/main/default/bronze_ingest",
    )


@dlt.table(
    name="bronze_events",
    comment="Bronze: raw JSON via Auto Loader with explicit schema (empty-dir safe)",
    table_properties={"quality": "bronze"},
)
def bronze_events():
    path = _bronze_path()
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", f"{path}/_schemas/bronze_events")
        .schema(_BRONZE_SCHEMA)
        .load(path)
    )


@dlt.table(
    name="silver_events",
    comment="Silver: standardized keys, deduplicated by event_id",
    table_properties={"quality": "silver"},
)
@dlt.expect_or_fail("event_id_not_null", "event_id IS NOT NULL")
def silver_events():
    df = dlt.read_stream("bronze_events")
    cleaned = (
        df.withColumn("event_id", F.coalesce(F.col("event_id"), F.col("id")))
        .withColumn("payload", F.col("payload"))
        # `_metadata` is not present when bronze uses a fixed Auto Loader schema; `input_file_name` works for file paths.
        .withColumn("source_file", F.input_file_name())
        .withColumn("processed_at", F.current_timestamp())
        .select("event_id", "payload", "source_file", "processed_at")
    )
    window_spec = Window.partitionBy("event_id").orderBy(F.col("processed_at").desc())
    return (
        cleaned.withColumn("_rn", F.row_number().over(window_spec))
        .filter(F.col("_rn") == 1)
        .drop("_rn")
    )


@dlt.table(
    name="gold_daily_event_counts",
    comment="Gold: daily event volume (grain: calendar day)",
    table_properties={"quality": "gold"},
)
def gold_daily_event_counts():
    silver = dlt.read("silver_events")
    return (
        silver.groupBy(F.to_date("processed_at").alias("event_day"))
        .agg(F.count("*").alias("event_count"))
        .orderBy("event_day")
    )
