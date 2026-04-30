"""Gold layer business aggregations."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import dlt
from pyspark.sql import DataFrame, functions as F


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from config_loader import load_runtime_config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG = load_runtime_config()


@dlt.table(
    name="gold_product_metrics",
    comment="Aggregated product-level metrics from Silver sales.",
    path=f"{CONFIG.storage_paths.gold}/product_metrics",
    table_properties={"quality": "gold"},
)
def gold_product_metrics() -> DataFrame:
    logger.info("Building Gold product metrics")
    silver_df = dlt.read("silver_sales")
    return silver_df.groupBy("product").agg(
        F.sum("quantity").alias("total_quantity"),
        F.sum("revenue").alias("total_revenue"),
        F.countDistinct("id").alias("distinct_orders"),
    )


@dlt.table(
    name="gold_daily_metrics",
    comment="Daily sales KPIs aggregated from Silver sales.",
    path=f"{CONFIG.storage_paths.gold}/daily_metrics",
    table_properties={"quality": "gold"},
)
def gold_daily_metrics() -> DataFrame:
    logger.info("Building Gold daily metrics")
    silver_df = dlt.read("silver_sales")
    return silver_df.withColumn("event_date", F.to_date("event_timestamp")).groupBy(
        "event_date"
    ).agg(
        F.sum("quantity").alias("total_quantity"),
        F.sum("revenue").alias("total_revenue"),
        F.count("*").alias("row_count"),
    )

