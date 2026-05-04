# Unity Catalog objects on Azure Databricks (workspace-level APIs).
# Prerequisites: metastore assigned to the workspace, Azure Bicep deployed (access connector + storage),
# and Azure RBAC on storage for the connector MI (e.g. Storage Blob Data Contributor).

locals {
  access_connector_arm_id = format(
    "/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Databricks/accessConnectors/%s",
    var.azure_subscription_id,
    var.azure_resource_group,
    var.access_connector_name
  )

  adls_container_base_url = format(
    "abfss://%s@%s.dfs.core.windows.net",
    var.adls_container_name,
    var.storage_account_name
  )

  catalog_storage_root = format(
    "%s/%s/%s",
    local.adls_container_base_url,
    var.catalog_storage_suffix,
    var.catalog_name
  )
}

provider "databricks" {
  host  = startswith(var.databricks_host, "https://") ? var.databricks_host : "https://${var.databricks_host}"
  token = var.databricks_token
}

resource "databricks_storage_credential" "this" {
  name = var.storage_credential_name

  # Azure Databricks access connector (system-assigned managed identity). Add `managed_identity_id` here
  # if your connector uses a user-assigned identity (full ARM ID to the UAMI resource).
  azure_managed_identity {
    access_connector_id = local.access_connector_arm_id
  }

  comment         = "Azure access connector — managed by Terraform"
  skip_validation = var.uc_skip_validation
  isolation_mode  = "ISOLATION_MODE_OPEN"
}

resource "databricks_external_location" "this" {
  name            = var.external_location_name
  url             = local.adls_container_base_url
  credential_name = databricks_storage_credential.this.id
  comment         = "ADLS root for UC paths — managed by Terraform"
  skip_validation = var.uc_skip_validation
  isolation_mode  = "ISOLATION_MODE_OPEN"
}

resource "databricks_catalog" "this" {
  count = var.create_managed_catalog ? 1 : 0

  name           = var.catalog_name
  storage_root   = local.catalog_storage_root
  isolation_mode = "OPEN"
  comment        = "Aligned with bundle catalog variable"

  depends_on = [databricks_external_location.this]
}

resource "databricks_schema" "default" {
  count = var.create_managed_catalog ? 1 : 0

  catalog_name = databricks_catalog.this[0].name
  name         = "default"
  comment      = "Default schema (volumes, etc.)"
}
