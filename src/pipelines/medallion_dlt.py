"""
Medallion Delta Live Tables pipeline: Bronze (raw) -> Silver (cleansed) -> Gold (aggregates).

Configure bundle.catalog and bundle.bronze_source_path via pipeline configuration in databricks.yml.
"""

from __future__ import annotations

import dlt
from pyspark.sql import functions as F

# Use schema *hints* (not full `.schema()`) so Auto Loader keeps `_metadata` (Unity Catalog requires
# `_metadata.file_path` in silver — `input_file_name()` is not supported in UC). Pair hints with
# `addNewColumns` per Databricks. Fixtures: `fixtures/*.jsonl` → `bundle.bronze_source_path`.
# Extend this DDL string if new top-level fields are expected in JSON.
_BRONZE_SCHEMA_HINTS = (
    "event_id STRING, id STRING, "
    "payload STRUCT<x: BIGINT, source: STRING, value: BIGINT>"
)


def _bronze_path() -> str:
    return spark.conf.get(
        "bundle.bronze_source_path",
        "/Volumes/main/default/bronze_ingest",
    )


@dlt.table(
    name="bronze_events",
    comment="Bronze: raw JSON via Auto Loader (schemaHints + evolution, preserves _metadata for UC)",
    table_properties={"quality": "bronze"},
)
def bronze_events():
    path = _bronze_path()
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaHints", _BRONZE_SCHEMA_HINTS)
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
        .option("cloudFiles.schemaLocation", f"{path}/_schemas/bronze_events")
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

    if "_metadata" in df.columns:
        source_file_col = F.col("_metadata.file_path")
    else:
        source_file_col = F.lit(None)

    cleaned = (
        df.withColumn("event_id", F.coalesce(F.col("event_id"), F.col("id")))
        .withColumn("payload", F.col("payload"))
        .withColumn("source_file", source_file_col)
        .withColumn("processed_at", F.current_timestamp())
        .select("event_id", "payload", "source_file", "processed_at")
    )
    # ROW_NUMBER() windows are not supported on streaming DataFrames. Use watermark + groupBy + max_by.
    wm = cleaned.withWatermark("processed_at", "7 days")
    return (
        wm.groupBy("event_id")
        .agg(
            F.max_by(
                F.struct(
                    F.col("payload"),
                    F.col("source_file"),
                    F.col("processed_at"),
                ),
                F.col("processed_at"),
            ).alias("_picked"),
        )
        .select(
            F.col("event_id"),
            F.col("_picked.payload").alias("payload"),
            F.col("_picked.source_file").alias("source_file"),
            F.col("_picked.processed_at").alias("processed_at"),
        )
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
