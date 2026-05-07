# Bronze ingest fixtures

The DLT pipeline reads **JSON** from `bundle.bronze_source_path` (see `databricks.yml`), not CSV. Auto Loader expects **JSON Lines** (one JSON object per line) in cloud storage or a **Unity Catalog volume**.

## Files

| File | Purpose |
|------|--------|
| `bronze_ingest_sample.jsonl` | Several mock events—copy into the configured **bronze volume** path so the stream has files to read. |
| `bronze_ingest_sample_500.jsonl` | Larger sample (500 lines)—CI deploy also uploads it as `ci_seed_500.jsonl` beside `ci_seed.jsonl`. |
| `sample_bronze_event.json` | Single example object (pretty-printed)—same shape as one line in the `.jsonl` file. |

## Upload to Databricks (example)

Default bundle path is the **volume root**, e.g. `/Volumes/cursorfun/default/bronze_ingest`:

```bash
# From repo root. For `databricks fs`, Unity Catalog volume paths must use the dbfs: scheme (see Databricks docs).
databricks fs cp fixtures/bronze_ingest_sample.jsonl \
  "dbfs:/Volumes/cursorfun/default/bronze_ingest/events.jsonl"
```

Or upload **JSON Lines** (`.jsonl`) via the workspace **Catalog** UI. After at least one file exists there, start or refresh the pipeline.

## GitHub Actions (deploy)

On **push to `main` or `master`**, **Deploy Databricks bundle** (`.github/workflows/deploy.yml`) runs **`databricks bundle deploy`**, then uploads:

- `bronze_ingest_sample.jsonl` → `dbfs:/Volumes/cursorfun/default/bronze_ingest/ci_seed.jsonl`
- `bronze_ingest_sample_500.jsonl` → `dbfs:/Volumes/cursorfun/default/bronze_ingest/ci_seed_500.jsonl`

( **`dbfs:`** required for **`databricks fs`**; pipelines still use **`/Volumes/...`** in Spark config.) Auto Loader reads all JSON/JSONL files under the bronze volume root.

Same **`DATABRICKS_HOST`** + **`DATABRICKS_TOKEN`** secrets as deploy. Adjust **`BRONZE_SEED_*`** env vars and **`bronze_source_path`** in **`databricks.yml`** if your Unity Catalog layout differs.

Deploy runs **`databricks fs mkdir`** on the **volume root** (`dirname` **`BRONZE_SEED_DEST`**) before **`fs cp`**. Paths use **`dbfs:/Volumes/...`** so the CLI targets Unity Catalog storage—not the runner’s local filesystem (**`mkdir /Volumes`** errors usually mean the **`dbfs:`** prefix was omitted).

The **bronze volume** and **`cursorfun`** catalog must exist and the token must have **WRITE** on the volume; see **`docs/BRONZE_VOLUME_IAC.md`**.

## Shape

Top-level: optional `event_id`, optional `id`, optional `payload` with optional nested fields (see samples). New fields should stay compatible with **`medallion_dlt.py`** and Auto Loader **`inferColumnTypes`** / schema evolution in your workspace.
