"""Runtime configuration loader for DLT pipelines."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = ROOT_DIR / "config" / "config.yml"


@dataclass(frozen=True)
class PipelineConfig:
    name: str
    source_csv_path: str
    checkpoint_base_path: str


@dataclass(frozen=True)
class SchemaConfig:
    name: str


@dataclass(frozen=True)
class StoragePaths:
    bronze: str
    silver: str
    gold: str


@dataclass(frozen=True)
class RuntimeConfig:
    pipeline: PipelineConfig
    schema: SchemaConfig
    storage_paths: StoragePaths
    environment: str


@dataclass(frozen=True)
class DatabricksAuthConfig:
    host: str
    token: str


def _required(mapping: Dict[str, Any], key: str, context: str) -> Any:
    value = mapping.get(key)
    if value in (None, ""):
        raise ValueError(f"Missing required config '{context}.{key}'.")
    return value


def load_runtime_config(config_path: Path | None = None) -> RuntimeConfig:
    """Load and validate non-sensitive runtime config."""
    path = config_path or DEFAULT_CONFIG_PATH
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at: {path}")

    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    pipeline_map = _required(data, "pipeline", "root")
    schema_map = _required(data, "schema", "root")
    storage_map = _required(data, "storage_paths", "root")
    environment = _required(data, "environment", "root")

    return RuntimeConfig(
        pipeline=PipelineConfig(
            name=_required(pipeline_map, "name", "pipeline"),
            source_csv_path=_required(pipeline_map, "source_csv_path", "pipeline"),
            checkpoint_base_path=_required(
                pipeline_map,
                "checkpoint_base_path",
                "pipeline",
            ),
        ),
        schema=SchemaConfig(name=_required(schema_map, "name", "schema")),
        storage_paths=StoragePaths(
            bronze=_required(storage_map, "bronze", "storage_paths"),
            silver=_required(storage_map, "silver", "storage_paths"),
            gold=_required(storage_map, "gold", "storage_paths"),
        ),
        environment=str(environment),
    )


def load_databricks_auth() -> DatabricksAuthConfig:
    """Load Databricks auth vars from local .env or process environment."""
    load_dotenv(ROOT_DIR / ".env")
    host = os.getenv("DATABRICKS_HOST", "")
    token = os.getenv("DATABRICKS_TOKEN", "")
    if not host or not token:
        raise ValueError(
            "DATABRICKS_HOST and DATABRICKS_TOKEN must be set in environment or .env."
        )
    return DatabricksAuthConfig(host=host, token=token)

