output "storage_credential_name" {
  description = "Unity Catalog storage credential name (same as resource id)."
  value       = databricks_storage_credential.this.id
}

output "external_location_name" {
  description = "Unity Catalog external location name."
  value       = databricks_external_location.this.id
}

output "catalog_name" {
  description = "Unity Catalog name when create_managed_catalog is true."
  value       = var.create_managed_catalog ? databricks_catalog.this[0].name : null
}

output "access_connector_arm_id" {
  description = "Resolved ARM resource ID for the access connector."
  value       = local.access_connector_arm_id
}

output "adls_container_base_url" {
  description = "abfss:// base URL used for the external location and catalog paths."
  value       = local.adls_container_base_url
}
