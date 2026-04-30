"""Silver layer cleansing and quality enforcement."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import dlt
from pyspark.sql import DataFrame, functions as F
from pyspark.sql.window import Window


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from config_loader import load_runtime_config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG = load_runtime_config()


@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
@dlt.expect_or_drop("valid_product", "product IS NOT NULL")
@dlt.expect_or_drop("valid_quantity", "quantity > 0")
@dlt.expect_or_drop("valid_price", "price >= 0")
@dlt.expect_or_drop("valid_timestamp", "event_timestamp IS NOT NULL")
@dlt.table(
    name="silver_sales",
    comment="Cleaned and de-duplicated sales records.",
    path=CONFIG.storage_paths.silver,
    table_properties={"quality": "silver"},
)
def silver_sales() -> DataFrame:
    logger.info("Cleaning Bronze records into Silver table")

    bronze_df = dlt.read_stream("bronze_sales")
    typed_df = (
        bronze_df.withColumn("id", F.col("id").cast("string"))
        .withColumn("product", F.trim(F.col("product")).cast("string"))
        .withColumn("quantity", F.col("quantity").cast("int"))
        .withColumn("price", F.col("price").cast("double"))
        .withColumn("event_timestamp", F.to_timestamp(F.col("timestamp")))
    )

    dedup_window = Window.partitionBy("id").orderBy(F.col("event_timestamp").desc())
    deduped = typed_df.withColumn("row_num", F.row_number().over(dedup_window)).filter(
        F.col("row_num") == 1
    )

    return (
        deduped.drop("row_num")
        .drop("timestamp")
        .withColumn("revenue", F.col("quantity") * F.col("price"))
    )

