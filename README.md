# Databricks AI First — Medallion platform (DAB + DLT)

Production-oriented starter for **Databricks**: **Databricks Asset Bundles**, **Delta Live Tables** (Bronze → Silver → Gold), and **GitHub Actions** using **Personal Access Token** authentication (`DATABRICKS_HOST` + `DATABRICKS_TOKEN`).

## Quick links

- Auth and secrets: [docs/AUTH_DATABRICKS_TOKEN.md](docs/AUTH_DATABRICKS_TOKEN.md)
- Layout and bundle root: [docs/REPO_AND_WORKSPACE_LAYOUT.md](docs/REPO_AND_WORKSPACE_LAYOUT.md)
- Jira mapping: [docs/JIRA_TASK_MAPPING.md](docs/JIRA_TASK_MAPPING.md)

## Before first deploy

1. Edit **`databricks.yml`**: set `workspace.host` to your real workspace URL (static literal, no interpolation).
2. Create GitHub secrets: **`DATABRICKS_HOST`**, **`DATABRICKS_TOKEN`** (see auth doc).
3. Ensure Unity Catalog paths exist for **`bronze_source_path`** (default under `main` catalog) or override `bronze_source_path` in the bundle.
4. Seed the bronze path with JSON files (e.g. `{"event_id":"1","payload":{"x":1}}` per line or one JSON object per file depending on layout).
5. **DLT compute:** this bundle uses **classic** pipeline clusters (`clusters` in `databricks.yml`), not serverless DLT. If deploy fails on node type or DBR, override bundle variables **`pipeline_node_type_id`** and **`pipeline_spark_version`** (see `databricks.yml`).

## Local commands

```bash
export DATABRICKS_HOST="https://adb-xxxxxxxx.azuredatabricks.net"
export DATABRICKS_TOKEN="dapixxxxxxxxxxxxxxxx"
databricks bundle validate -t dev   # requires workspace auth
databricks bundle deploy -t dev --auto-approve
```

## Offline checks

```bash
pip install -r requirements-dev.txt
pytest -q
```

CI runs **`databricks bundle validate`** with PAT credentials (`DATABRICKS_HOST` + `DATABRICKS_TOKEN`) against your workspace.

## Troubleshooting deploy

| Symptom | What to do |
| --------| ----------- |
| `You can't use serverless compute with Spark Declarative Pipelines` | Workspace does not allow serverless DLT. This repo uses classic `clusters` on the pipeline (no `serverless: true`). Pull latest and redeploy. |
| `root_path` under `/Workspace/Shared` writable by all users | Expected when using a shared bundle folder. Restrict who gets workspace access, or move `workspace.root_path` to a user-scoped path if policy requires it (that path cannot stay under `/Shared/...`). |
| Cluster / instance type errors | Set `pipeline_node_type_id` to a SKU available in your region (Azure portal or workspace **Clusters** UI). |