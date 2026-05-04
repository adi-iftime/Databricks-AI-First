variable "databricks_host" {
  type        = string
  description = "Workspace URL, e.g. https://adb-xxxx.azuredatabricks.net"
}

variable "databricks_token" {
  type        = string
  sensitive   = true
  description = "PAT or token for a principal that can manage Unity Catalog (e.g. metastore admin or workspace admin)."
}

variable "azure_subscription_id" {
  type        = string
  description = "Azure subscription ID (used to build Access Connector ARM resource ID)."
}

variable "azure_resource_group" {
  type        = string
  description = "Resource group that contains the Access Connector and storage account."
}

variable "access_connector_name" {
  type        = string
  description = "Name of Microsoft.Databricks/accessConnectors resource (system-assigned MI)."
}

variable "storage_account_name" {
  type        = string
  description = "ADLS Gen2 storage account name (no FQDN)."
}

variable "adls_container_name" {
  type        = string
  description = "Blob container used as UC root (same container as Bicep metastore container)."
}

variable "catalog_name" {
  type        = string
  description = "Unity Catalog name (matches bundle variable catalog, e.g. cursorfun)."
}

variable "storage_credential_name" {
  type        = string
  description = "UC storage credential name (unique in the metastore)."
}

variable "external_location_name" {
  type        = string
  description = "UC external location name (unique in the metastore)."
}

variable "uc_skip_validation" {
  type        = bool
  default     = false
  description = "If true, sets skip_validation on storage credential and external location (bootstrap only)."
}

variable "create_managed_catalog" {
  type        = bool
  default     = true
  description = "Create databricks_catalog + default schema. Disable if the catalog already exists and you will import instead."
}

variable "catalog_storage_suffix" {
  type        = string
  default     = "catalogs"
  description = "Path segment under the container for managed tables (abfss://.../catalogs/<catalog>)."
}
