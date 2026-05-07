#!/usr/bin/env python3
"""
Compute deploy-time bronze seed URIs from `databricks.yml` so CI stays aligned with
`variables.bronze_source_path` (and optional target overrides).

Writes `bronze_seed_dest` and `bronze_seed_500_dest` to $GITHUB_OUTPUT when set;
otherwise prints BRONZE_SEED_DEST / BRONZE_SEED_500_DEST lines for local debugging.

Only Unity Catalog volume roots (`/Volumes/...`) are supported for `databricks fs cp`;
external paths (e.g. `abfss://`) require a different seed mechanism.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml


def effective_bronze_source_path(cfg: dict, target: str) -> str | None:
    variables = cfg.get("variables") or {}
    bronze_var = variables.get("bronze_source_path") or {}
    bronze = bronze_var.get("default")

    targets = cfg.get("targets") or {}
    tcfg = targets.get(target) or {}
    override = (tcfg.get("variables") or {}).get("bronze_source_path")
    if override is not None:
        bronze = override
    return bronze


def volume_paths_for_ci(bronze_source_path: str) -> tuple[str, str]:
    base = bronze_source_path.rstrip("/")
    if not base.startswith("/Volumes/"):
        raise ValueError(
            "CI bronze seeding expects a UC volume path starting with /Volumes/; "
            f"got {bronze_source_path!r}. Override paths manually or extend this script."
        )
    root = "dbfs:" + base
    return f"{root}/ci_seed.jsonl", f"{root}/ci_seed_500.jsonl"


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    target = os.environ.get("BUNDLE_TARGET", "dev")
    raw = (root / "databricks.yml").read_text(encoding="utf-8")
    cfg = yaml.safe_load(raw)

    bronze = effective_bronze_source_path(cfg, target)
    if not bronze:
        print("::error::Could not resolve bronze_source_path from databricks.yml.", file=sys.stderr)
        sys.exit(1)

    try:
        seed1, seed500 = volume_paths_for_ci(bronze)
    except ValueError as e:
        print(f"::error::{e}", file=sys.stderr)
        sys.exit(1)

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"bronze_seed_dest={seed1}\n")
            f.write(f"bronze_seed_500_dest={seed500}\n")
        print(f"Resolved bronze seeds for target {target!r}: {seed1} ; {seed500}")
    else:
        print(f"BRONZE_SEED_DEST={seed1}")
        print(f"BRONZE_SEED_500_DEST={seed500}")


if __name__ == "__main__":
    main()
