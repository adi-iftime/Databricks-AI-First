# Bronze ingest fixtures

The DLT pipeline reads **JSON** from `bundle.bronze_source_path` (see `databricks.yml`), not CSV. Auto Loader expects **JSON Lines** (one JSON object per line) in cloud storage or a **Unity Catalog volume**.

## Files

| File | Purpose |
|------|--------|
| `bronze_ingest_sample.jsonl` | Several mock events—copy this into your bronze volume path (e.g. `sample/` under `bronze_ingest`) so the stream has files to read. |
| `sample_bronze_event.json` | Single example object (pretty-printed)—same shape as one line in the `.jsonl` file. |

## Upload to Databricks (example)

Use the path from your bundle, e.g. `/Volumes/cursorfun/default/bronze_ingest/sample`:

```bash
# From repo root; use the same catalog/schema/volume as in databricks.yml
databricks fs cp fixtures/bronze_ingest_sample.jsonl \
  "/Volumes/cursorfun/default/bronze_ingest/sample/events.jsonl"
```

Or upload **JSON Lines** (`.jsonl`) via the workspace **Catalog** UI into that volume path. After at least one file exists there, start or refresh the pipeline.

## GitHub Actions (deploy)

On **push to `main` or `master`**, **Deploy Databricks bundle** (`.github/workflows/deploy.yml`) runs **`databricks bundle deploy`**, then uploads `bronze_ingest_sample.jsonl` to:

`/Volumes/cursorfun/default/bronze_ingest/sample/ci_seed.jsonl`

Same **`DATABRICKS_HOST`** + **`DATABRICKS_TOKEN`** secrets as deploy. Adjust **`BRONZE_SEED_DEST`** (and catalog/schema/volume in **`databricks.yml`**) if your Unity Catalog layout differs.

Before **`fs cp`**, the workflow runs **`databricks fs mkdir`** on the **parent** of the seed file (e.g. **`…/bronze_ingest/sample`**) so the **`sample`** path prefix exists inside the volume.

The **bronze volume**, catalog, and metastore must allow your principal to write; see **`docs/BRONZE_VOLUME_IAC.md`** for Terraform vs **`mkdir`** behavior.

## Shape

Top-level: optional `event_id`, optional `id`, optional `payload` with optional `x`, `source`, `value` (must match `_BRONZE_SCHEMA` in `src/pipelines/medallion_dlt.py`).
