"""Offline checks for bundle configuration (no Databricks API calls)."""

import os
import subprocess
import sys
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
    pipeline_paths = [str(lib.get("file", {}).get("path", "")) for lib in libs]
    assert any("medallion_dlt.py" in p for p in pipeline_paths)


def test_pipeline_source_exists():
    path = ROOT / "src" / "pipelines" / "medallion_dlt.py"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "@dlt.table" in text
    assert "bronze_events" in text and "silver_events" in text and "gold_daily_event_counts" in text
    assert "bundle.bronze_source_path" in text, "pipeline should read bronze path from bundle spark.conf"


def test_medallion_pipeline_expectations_and_transforms():
    path = ROOT / "src" / "pipelines" / "medallion_dlt.py"
    text = path.read_text(encoding="utf-8")
    assert '@dlt.expect("valid_json"' in text
    assert ".dropDuplicates([\"event_id\"])" in text
    assert 'F.to_date("processed_at")' in text


def test_resolve_bronze_seed_dests_matches_bundle_default():
    cfg = yaml.safe_load((ROOT / "databricks.yml").read_text(encoding="utf-8"))
    expected_base = cfg["variables"]["bronze_source_path"]["default"].rstrip("/")
    env = os.environ.copy()
    env.pop("GITHUB_OUTPUT", None)
    env["BUNDLE_TARGET"] = "dev"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "resolve_bronze_seed_dests.py")],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert f"BRONZE_SEED_DEST=dbfs:{expected_base}/ci_seed.jsonl" in proc.stdout
    assert f"BRONZE_SEED_500_DEST=dbfs:{expected_base}/ci_seed_500.jsonl" in proc.stdout
