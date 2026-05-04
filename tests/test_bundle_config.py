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
    rp = cfg["workspace"]["root_path"]
    assert rp.startswith("/Workspace/Users/")
    assert "${workspace.current_user.userName}" in rp
    assert "${bundle.name}" in rp
    assert "${bundle.target}" in rp
    pipes = cfg["resources"]["pipelines"]["medallion_dlt"]
    assert pipes.get("serverless") is True, "workspace requires serverless DLT"
    clusters = pipes.get("clusters") or []
    assert not clusters, "serverless pipeline must not use classic clusters block"
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
    assert "bundle.bronze_source_path" in text, "pipeline should read bronze path from bundle spark.conf"
