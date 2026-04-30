# QA validation report — SCRUM-34 / QA-01

**Security prerequisite:** SEC-02 **CLEAR** (see [SECURITY_GATE_RESULT.md](SECURITY_GATE_RESULT.md)).

## Automated offline tests

- Command: `pytest -q` from repository root (after `pip install -r requirements-dev.txt`).
- Scope: `tests/test_bundle_config.py` validates `databricks.yml` structure (bundle name, static `workspace.host` without interpolation, Shared bundle root, pipeline library path) and presence of DLT pipeline layers in `src/pipelines/medallion_dlt.py`.

## CI / workspace validation

- GitHub Actions workflow **Validate Databricks bundle** runs `pytest` then `databricks bundle validate -t dev` using **`DATABRICKS_HOST`** and **`DATABRICKS_TOKEN`** (repository secrets).
- **Local** `databricks bundle validate` requires the same env vars (or a `~/.databrickscfg` profile with host + token); see [AUTH_DATABRICKS_TOKEN.md](AUTH_DATABRICKS_TOKEN.md).

## Medallion acceptance (manual / workspace)

| Layer | Table | Criterion |
| ----- | ----- | --------- |
| Bronze | `bronze_events` | Auto Loader ingests JSON with schema evolution; data lands before Silver |
| Silver | `silver_events` | `event_id` not null; dedupe by `event_id` on latest `processed_at` |
| Gold | `gold_daily_event_counts` | Grain: one row per `event_day`; ordered chronologically |

## Fixture sample

- [fixtures/sample_bronze_event.json](../fixtures/sample_bronze_event.json) can be copied to the configured `bronze_source_path` volume for smoke testing.

**Outcome:** QA evidence recorded; CI is the regression path for bundle validation with live PAT auth.
