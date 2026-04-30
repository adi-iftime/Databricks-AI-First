# Databricks AI First — Medallion platform (DAB + DLT)

Production-oriented starter for **Databricks**: **Databricks Asset Bundles**, **Delta Live Tables** (Bronze → Silver → Gold), and **GitHub Actions** using **Personal Access Token** authentication (`DATABRICKS_HOST` + `DATABRICKS_TOKEN`).

## Quick links

- Auth and secrets: [docs/AUTH_DATABRICKS_TOKEN.md](docs/AUTH_DATABRICKS_TOKEN.md)
- Layout and bundle root: [docs/REPO_AND_WORKSPACE_LAYOUT.md](docs/REPO_AND_WORKSPACE_LAYOUT.md)
- Jira mapping: [docs/JIRA_TASK_MAPPING.md](docs/JIRA_TASK_MAPPING.md)

## Before first deploy

1. Edit **`databricks.yml`**: set `workspace.host` to your real workspace URL (static literal, no interpolation).
2. Create GitHub secrets: **`DATABRICKS_HOST`**, **`DATABRICKS_TOKEN`** (see auth doc).
3. Ensure Unity Catalog paths exist for **`bronze_source_path`** (default **`/Volumes/cursorfun/default/bronze_ingest/sample`**) and create the **`bronze_ingest`** volume under catalog **`cursorfun`**, schema **`default`**, or override paths in the bundle.
4. Seed the bronze path with JSON files (e.g. `{"event_id":"1","payload":{"x":1}}` per line or one JSON object per file depending on layout).
5. **Unity Catalog:** the workspace must have a **Unity Catalog metastore** assigned (`No metastore assigned` during deploy means an admin must attach one in account/workspace settings). This bundle publishes to **`catalog`** + **`schema`** and uses **`/Volumes/...`** paths, which require UC.
6. **DLT compute:** this bundle uses **`serverless: true`** on the pipeline resource. Some workspaces **require** serverless DLT and reject classic pipeline clusters; others block serverless—adjust `serverless` and optional `clusters` to match your workspace policy. **`workspace.root_path`** is user-scoped (`/Workspace/Users/${workspace.current_user.userName}/...`) so deploy state is not under world-writable **`/Workspace/Shared`** unless you change it.

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
| `You must use serverless compute in this workspace` | Remove classic pipeline `clusters` from `databricks.yml` and set **`serverless: true`** on the pipeline (this repo’s default). Redeploy. |
| `You can't use serverless compute with Spark Declarative Pipelines` | Your workspace blocks serverless DLT. Set **`serverless: false`**, add a **`clusters`** block with `label`, `node_type_id`, and `num_workers`, and remove conflicting flags—see [Databricks SDP pipeline docs](https://docs.databricks.com/aws/en/dev-tools/bundles/resources#pipelines). |
| `unknown field: spark_version` on `clusters[0]` | `spark_version` is not valid on bundle `PipelineCluster`. Remove it from `clusters` (runtime follows pipeline defaults). |
| `No metastore assigned for the current workspace` | Assign a **Unity Catalog metastore** to this workspace (account/metastore admin). Required for `catalog` + `schema` and for **`/Volumes/`** bronze paths. |
| `root_path` under `/Workspace/Shared` writable by all users | Switch to a **user-scoped** `workspace.root_path` (this repo uses `/Workspace/Users/${workspace.current_user.userName}/.bundle/...`). Only applies if you override back to **`/Shared`** or **`/Workspace/Shared`**. |
| Cluster / instance type errors | Only relevant when using **classic** pipeline clusters (not serverless). Pick a **`node_type_id`** available in your region. |