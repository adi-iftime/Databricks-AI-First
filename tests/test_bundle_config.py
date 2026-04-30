"""Offline checks for bundle configuration (no Databricks API calls)."""

from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_databricks_yml_structure():
    raw = (ROOT / "databricks.yml").read_text(encoding="utf-8")
    cfg = yaml.safe_load(raw)
    assert cfg["bundle"]["name"] == "databricks_ai_first"
    host = cfg["workspace"]["host"]
    assert host.startswith("https://"), "workspace.host must be an https URL literal"
    assert "${" not in host, "workspace.host must not use bundle interpolation"
    assert cfg["workspace"]["root_path"] == "/Shared/.bundle/databricks_ai_first"
    pipes = cfg["resources"]["pipelines"]["medallion_dlt"]
    assert pipes["serverless"] is True
    libs = pipes["libraries"]
    assert any(
        "medallion_dlt.py" in str(lib.get("file", {}).get("path", "")) for lib in libs
    )


def test_pipeline_source_exists():
    path = ROOT / "src" / "pipelines" / "medallion_dlt.py"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "@dlt.table" in text
    assert "bronze_events" in text and "silver_events" in text and "gold_daily_event_counts" in text
