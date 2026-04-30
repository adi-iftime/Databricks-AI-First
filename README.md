# Databricks AI First — Medallion platform (DAB + DLT)

Production-oriented starter for **Azure Databricks**: **Databricks Asset Bundles**, **Delta Live Tables** (Bronze → Silver → Gold), and **GitHub Actions** using **Azure Service Principal** authentication only.

## Quick links

- Auth and secrets: [docs/AUTH_SERVICE_PRINCIPAL.md](docs/AUTH_SERVICE_PRINCIPAL.md)
- Layout and bundle root: [docs/REPO_AND_WORKSPACE_LAYOUT.md](docs/REPO_AND_WORKSPACE_LAYOUT.md)
- Jira mapping: [docs/JIRA_TASK_MAPPING.md](docs/JIRA_TASK_MAPPING.md)

## Before first deploy

1. Edit **`databricks.yml`**: set `workspace.host` to your real workspace URL (static literal, no interpolation).
2. Create GitHub secrets: `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`, `DATABRICKS_HOST` (see auth doc).
3. Ensure Unity Catalog paths exist for **`bronze_source_path`** (default under `main` catalog) or override `bronze_source_path` in the bundle.
4. Seed the bronze path with JSON files (e.g. `{"event_id":"1","payload":{"x":1}}` per line or one JSON object per file depending on layout).

## Local commands

```bash
databricks bundle validate -t dev   # requires workspace auth
databricks bundle deploy -t dev --auto-approve
```

## Offline checks

```bash
pip install -r requirements-dev.txt
pytest -q
```

CI runs **`databricks bundle validate`** with service principal credentials against your workspace.
