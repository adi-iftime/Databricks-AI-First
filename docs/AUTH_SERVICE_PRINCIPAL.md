# Authentication: Azure Service Principal (CI/CD)

This repository uses **Microsoft Entra ID (Azure AD) service principal** authentication for Databricks Asset Bundles and GitHub Actions. **Personal access tokens (PATs), user-based CI login, and `/Workspace/Users/...` bundle roots are not used.**

## Required GitHub Actions secrets

Store these **repository or environment** secrets (names must match what workflows expect):

| Secret | Purpose |
| ------ | ------- |
| `AZURE_CLIENT_ID` | Application (client) ID of the Entra app registration / service principal |
| `AZURE_CLIENT_SECRET` | Client secret for the service principal |
| `AZURE_TENANT_ID` | Directory (tenant) ID |
| `DATABRICKS_HOST` | Azure Databricks workspace URL, e.g. `https://adb-xxxxxxxx.azuredatabricks.net` (no trailing slash) |

Workflows **also** export Databricks CLI–oriented variables (`DATABRICKS_CLIENT_ID`, `DATABRICKS_CLIENT_SECRET`, `DATABRICKS_TENANT_ID`) from the **same** four secrets so the official CLI auth type `azure-client-secret` works without introducing PATs or extra secret names.

## Entra app registration and workspace access

1. **Register an application** in Microsoft Entra ID and create a **client secret** (store only in GitHub Secrets / your vault).
2. **Add the service principal to your Azure Databricks workspace** with a role appropriate for bundle deploy (for example **Databricks Workspace Admin** in sandboxes, or a **custom role** with least privilege for production — align with your organization’s policy).
3. **Grant data plane access** as needed for Unity Catalog (catalog/schema privileges, external locations, volumes) so pipelines can read/write configured paths.
4. **Never** commit secrets, `.env` files with real values, or PATs to this repository.

## Forbidden (policy)

- Databricks **personal access tokens** for automation
- Interactive browser login inside CI
- Deploying bundle state under **`/Workspace/Users/<user>`** — this bundle uses **`/Shared/.bundle/databricks_ai_first`** only

## Local development (optional)

Developers may use their own attended auth (OAuth / Azure CLI) with a local Databricks profile; production-like validation should still rely on the same bundle targets and paths as CI.
