# Bronze volume path: IaC vs path prefixes

## Paths in this repo

The bundle default **`bundle.bronze_source_path`** is the **volume root**:

`/Volumes/<catalog>/<schema>/<volume_name>/`

Auto Loader reads JSON files anywhere under that path (for example **`ci_seed.jsonl`** uploaded by deploy). No **`sample/`** subfolder is required.

Optional **subfolders** (e.g. **`sample/`**) are path prefixes inside storage. If you use them, create with **`databricks fs mkdir`** before **`fs cp`**, or upload via the Catalog UI.

**Deploy** runs **`databricks fs mkdir`** on the **volume root** (`…/bronze_ingest`) before **`fs cp`** to **`ci_seed.jsonl`**, because **`fs cp`** can fail with *no such directory* until that path prefix exists—without recreating a **`sample/`** subdirectory.

## Local / manual

```bash
databricks fs cp fixtures/bronze_ingest_sample.jsonl \
  "/Volumes/cursorfun/default/bronze_ingest/events.jsonl"
```

## Terraform (catalog + volume)

There is **no** Terraform resource for arbitrary folders inside a UC volume. Create **catalog** / **schema** / **volume** with the [Databricks Terraform provider](https://registry.terraform.io/providers/databricks/databricks/latest/docs).

Illustrative fragment (adjust for your cloud; requires metastore admin for new catalogs):

```hcl
terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = ">= 1.36.0"
    }
  }
}

# Often created once per workspace/account — omit if cursorfun already exists
# resource "databricks_catalog" "cursorfun" {
#   name         = "cursorfun"
#   storage_root = "abfss://...@..." # required pattern depends on Azure/GCP/AWS
# }

resource "databricks_schema" "default_in_catalog" {
  catalog_name = "cursorfun"
  name         = "default"
}

resource "databricks_volume" "bronze_ingest" {
  catalog_name = "cursorfun"
  schema_name  = databricks_schema.default_in_catalog.name
  name         = "bronze_ingest"
  volume_type  = "MANAGED"
  comment      = "Bronze landing; pipeline reads bundle.bronze_source_path under this volume"
}
```

## Summary

| Concern | IaC (Terraform) | CLI / CI |
|--------|-----------------|----------|
| Catalog / schema / **volume** | Yes (`databricks_volume`, etc.) | Catalog UI |
| Subpaths inside volume | No dedicated resource | **`databricks fs mkdir`** or upload at volume root |
