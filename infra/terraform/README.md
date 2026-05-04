# Terraform — Databricks Unity Catalog (workspace)

This stack configures **Databricks-side** Unity Catalog objects that pair with `**infra/main.bicep`** (Azure access connector + ADLS Gen2 + container).

It does **not** replace:

- **Azure resource deployment** (use the Bicep workflow).
- **Account-level metastore creation** (often done once in the Databricks account console or Account API). The workspace must already be **metastore-enabled**.

## What gets created

1. `**databricks_storage_credential`** — Azure managed identity via your **Access Connector** ARM ID.
2. `**databricks_external_location`** — Container root URL (`abfss://…`).
3. `**databricks_catalog**` + `**databricks_schema**` `default` — Matches bundle defaults (`catalog_name` e.g. `cursorfun`).

## Prerequisites

- Metastore assigned to the workspace; caller token must be able to manage UC (typically **metastore admin** or equivalent).
- **Azure RBAC**: access connector’s managed identity needs **data plane** access to the storage account (e.g. **Storage Blob Data Contributor** on the account or container scope). Apply this in Azure (Bicep role assignment, Portal, or a separate ARM/Terraform AzureRM stack).

## Local usage

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars   # edit; keep tfvars out of git
terraform init
terraform plan
terraform apply
```

Use a remote **backend** (Azure Storage, Terraform Cloud, etc.) for team state — local `terraform.tfstate` is ignored by git.

## GitHub Actions

Workflow **Deploy Databricks UC (Terraform)** runs **on demand** only. It expects repository secrets `**DATABRICKS_HOST`** and `**DATABRICKS_TOKEN**`, plus workflow inputs for subscription, resource group, and resource names.

## Importing existing objects

If `cursorfun` (or your catalog) already exists, set `create_managed_catalog = false` and use `terraform import` per provider docs, or remove the `databricks_catalog` / `databricks_schema` resources and manage only credential + external location.