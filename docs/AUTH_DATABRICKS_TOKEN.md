# Authentication: Databricks Personal Access Token (CI/CD and local)

This repository uses **Databricks unified authentication** with a **Personal Access Token (PAT)** for GitHub Actions and optional local CLI use. Bundle deployments stay under **`/Shared/.bundle/databricks_ai_first`** (not `/Workspace/Users/<user>`).

## Required GitHub Actions secrets

| Secret | Purpose |
| ------ | ------- |
| `DATABRICKS_HOST` | Workspace URL, e.g. `https://adb-xxxxxxxx.azuredatabricks.net` (no trailing slash) |
| `DATABRICKS_TOKEN` | PAT for a workspace user (or dedicated automation account) with permission to run `bundle validate` / `bundle deploy` |

Workflows export these as environment variables. The Databricks CLI picks them up automatically; **do not** set `databricks auth login` or alternate auth types in YAML.

## Creating and scoping a PAT

1. In the Databricks workspace UI, open **User Settings** (for the identity that will own automation) → **Developer** → **Access tokens** (wording may vary slightly by product version).
2. Generate a token with a clear comment (e.g. `github-actions-databricks-ai-first`) and expiration aligned with your security policy.
3. Grant that identity **workspace-level** access appropriate for bundle operations (and Unity Catalog privileges for pipelines/jobs your bundle manages). Follow least privilege for your environment.
4. Store the token only as **`DATABRICKS_TOKEN`** in GitHub **Secrets** (repository or environment). Never commit it.

## Local development

```bash
export DATABRICKS_HOST="https://adb-xxxxxxxx.azuredatabricks.net"
export DATABRICKS_TOKEN="dapixxxxxxxxxxxxxxxx"
databricks bundle validate -t dev
```

Optional: use a **`~/.databrickscfg`** profile with `host` + `token` instead of env vars.

## Host must match the bundle file

`databricks bundle validate` uses **`workspace.host` from `databricks.yml`**. That literal URL must match **`DATABRICKS_HOST`** (same workspace). Replace any placeholder host in the repo before CI will pass remote validation.

## Security hygiene

- Rotate PATs on a schedule and when people leave the owning role.
- Restrict who can view GitHub **Actions** logs if they might echo env debugging.
- Do not print `DATABRICKS_TOKEN` in workflow steps; GitHub masks secrets but avoid unnecessary `echo`.
- Prefer a dedicated workspace user for CI if your organization allows it, so token revocation does not affect individuals.

## Removed from this repo

Older workflows referenced Azure identity–based CLI variables; those are **not** used here. Only **`DATABRICKS_HOST`** and **`DATABRICKS_TOKEN`** are required for CI/CD in this project.
