"""Bronze layer ingestion for raw CSV source."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import dlt
from pyspark.sql import DataFrame


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from config_loader import load_runtime_config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG = load_runtime_config()


@dlt.table(
    name="bronze_sales",
    comment="Raw sales records ingested from CSV into the Bronze layer.",
    path=CONFIG.storage_paths.bronze,
    table_properties={"quality": "bronze"},
)
def bronze_sales() -> DataFrame:
    logger.info("Reading raw CSV from %s", CONFIG.pipeline.source_csv_path)
    # Auto Loader provides resilient ingestion and schema evolution behavior.
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
        .option(
            "cloudFiles.schemaLocation",
            f"{CONFIG.pipeline.checkpoint_base_path}/bronze_schema",
        )
        .load(CONFIG.pipeline.source_csv_path)
    )

