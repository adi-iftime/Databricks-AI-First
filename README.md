# Databricks Medallion DLT Pipeline

Production-style Databricks project implementing a Medallion Architecture (Bronze, Silver, Gold) with Delta Live Tables (DLT), Databricks Asset Bundles (DAB), and GitHub Actions CI/CD.

## Architecture Overview

This project ingests a CSV dataset from DBFS and processes it through:

- `bronze_sales`: raw ingestion with schema evolution support.
- `silver_sales`: cleaned, typed, deduplicated records with DLT expectations.
- `gold_product_metrics` and `gold_daily_metrics`: business aggregates.

End-to-end deployment flow:

`Git push` -> `GitHub Actions` -> `Upload CSV to DBFS` -> `Bundle deploy` -> `DLT pipeline run`

## Project Structure

```text
.
├── .github/workflows/deploy.yml
├── config/config.yml
├── data/sample.csv
├── databricks.yml
├── scripts/generate_sample_csv.py
├── src/bronze.py
├── src/config_loader.py
├── src/gold.py
├── src/silver.py
├── .env.example
└── .gitignore
```

## Prerequisites

- Databricks workspace access.
- Databricks personal access token (PAT) for local development.
- Databricks CLI v2 installed locally.
- Python 3.10+.

## Local Setup

### 1) Configure local environment variables

Copy `.env.example` to `.env` and set values:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
DATABRICKS_HOST=https://<your-workspace-host>
DATABRICKS_TOKEN=<your-pat-token>
```

`DATABRICKS_TOKEN` and `DATABRICKS_HOST` are required for local CLI authentication and are intentionally excluded from git.

### 2) Install local Python dependencies

```bash
python -m pip install --upgrade pip
pip install pyyaml python-dotenv
```

### 3) (Optional) Regenerate sample dataset

```bash
python scripts/generate_sample_csv.py --rows 10 --seed 42 --output data/sample.csv
```

## Databricks PAT Token Setup

1. In Databricks workspace, open **User Settings**.
2. Go to **Developer** (or **Access Tokens**, depending on workspace UI).
3. Create a new token with a suitable expiration policy.
4. Copy token immediately and store it securely.
5. Use it in local `.env` and GitHub Secrets (never commit it).

Least-privilege recommendation: use a service principal token with only required workspace permissions for CI/CD.

## Bundle Configuration

The project uses a root-level `databricks.yml` Databricks Asset Bundle that defines:

- DLT pipeline resource (`medallion_sales_pipeline`)
- target (`dev`)
- Unity Catalog target schema
- cluster autoscaling config
- environment and source path configuration

The workspace URL is **not** set in `databricks.yml`: bundle authentication resolves from **`DATABRICKS_HOST`** and **`DATABRICKS_TOKEN`** (or your CLI profile). Interpolation such as `${env.DATABRICKS_HOST}` under `targets.*.workspace.host` is not supported.

## Local Development and Pipeline Execution

Run from repository root:

1. Validate bundle:

```bash
databricks bundle validate -t dev
```

2. Upload raw CSV to DBFS:

```bash
databricks fs mkdir dbfs:/mnt/demo/raw
databricks fs cp data/sample.csv dbfs:/mnt/demo/raw/sample.csv --overwrite
```

3. Deploy bundle:

```bash
databricks bundle deploy -t dev
```

4. Run DLT pipeline:

```bash
databricks bundle run medallion_sales_pipeline -t dev
```

Note: pipeline execution happens in Databricks compute; local machine is used for validation/deploy/trigger operations.

## GitHub Actions CI/CD

Workflow file: `.github/workflows/deploy.yml`

Trigger: `push` to `main` (and manual `workflow_dispatch`).

The deployment job:

1. Checks out code.
2. Installs Python dependencies.
3. Installs Databricks CLI v2.
4. Authenticates via GitHub Secrets.
5. Uploads `data/sample.csv` to `dbfs:/mnt/demo/raw/sample.csv`.
6. Validates and deploys the Databricks bundle.
7. Runs the DLT pipeline.

## GitHub Secrets Configuration

In GitHub repo settings, add:

- `DATABRICKS_HOST`
- `DATABRICKS_TOKEN`

Do not use `.env` in CI/CD. GitHub Actions reads from Secrets only.

## Configuration Details

Non-sensitive runtime settings are in `config/config.yml`:

- pipeline name
- source and checkpoint paths
- schema name
- environment name (`dev`)
- storage paths for bronze/silver/gold

Sensitive values remain externalized through environment variables.

## Troubleshooting

- **Authentication error**: verify `DATABRICKS_HOST`/`DATABRICKS_TOKEN` values and token validity.
- **DBFS upload failure**: ensure the `dbfs:/mnt/demo/raw` path is writable and exists.
- **Bundle validation fails**: run `databricks bundle validate -t dev` locally and inspect YAML/resource names.
- **Pipeline run fails**: inspect DLT event logs and expectations in Databricks pipeline UI.
- **Bundle deploy errors under `.bundle/.../files` or `.bundle/.../state`**:
  - **`Cannot apply local deployment permissions`**: declaring `permissions` under a target makes the CLI **apply workspace ACLs** on the bundle file deployment path. Many workspace users **cannot grant `CAN_MANAGE`/`CAN_RUN` to themselves or others**, so deploy fails. This repo’s `dev` target intentionally **does not** set target-level `permissions`; rely on normal access to your own `/Workspace/Users/<you>/...` tree. If you need shared bundle deployments between people or a service principal, use a **workspace admin** or an identity with ACL-management rights, and follow [Bundle permissions](https://docs.databricks.com/en/dev-tools/bundles/permissions.html).
  - **`deploy.lock` / access denied**: another identity may hold the deployment lock or own the bundle metadata folder. The `dev` target uses `mode: development` so the deployment lock is off by default. Retry with `databricks bundle deploy -t dev --force-lock` if a lock is stuck.
  - **Stale deployment**: with admin coordination, you can remove `/Workspace/Users/<you>/.bundle/databricks-medallion-dlt/` and deploy again if permissions are corrupted.

## Security Notes

- Never hardcode credentials in source files.
- `.env` is for local development only and is git-ignored.
- Use GitHub Secrets in CI/CD for all sensitive values.
