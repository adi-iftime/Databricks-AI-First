# Bronze volume path: IaC vs path prefixes

## Why `fs cp` failed

Unity Catalog **volumes** are registered at:

`/Volumes/<catalog>/<schema>/<volume_name>/…`

Any deeper segment (e.g. **`sample/`**) is a **path prefix** inside storage, not a separate metastore object. The Databricks CLI does **not** create missing prefixes when copying a file unless you **`mkdir`** that path first.

**Deploy workflow** (`.github/workflows/deploy.yml`) runs **`databricks fs mkdir`** on the parent directory of **`BRONZE_SEED_DEST`** before **`databricks fs cp`**, so **`sample/`** is created if missing.

## Local / manual

```bash
databricks fs mkdir "/Volumes/cursorfun/default/bronze_ingest/sample"
databricks fs cp fixtures/bronze_ingest_sample.jsonl \
  "/Volumes/cursorfun/default/bronze_ingest/sample/events.jsonl"
```

## Terraform (catalog + volume — not the `sample/` folder)

There is **no** Terraform resource for “a folder inside a UC volume.” Create:

1. **Catalog** / **schema** / **managed** (or external) **volume** with the [Databricks Terraform provider](https://registry.terraform.io/providers/databricks/databricks/latest/docs).
2. Treat **`sample`** as a **prefix** created by **`databricks fs mkdir`** (CI does this), a notebook, or the first upload after **`mkdir`**.

Illustrative fragment (adjust `storage_location` / permissions for your cloud; requires metastore admin for new catalogs):

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

After apply, paths like **`…/bronze_ingest/sample`** still need **`databricks fs mkdir`** once (or rely on **CI** after deploy).

## Summary

| Concern | IaC (Terraform) | CLI / CI |
|--------|-----------------|----------|
| Catalog / schema / **volume** | Yes (`databricks_volume`, etc.) | Catalog UI |
| **`sample/` directory** inside volume | No dedicated resource | **`databricks fs mkdir`** (deploy workflow includes this) |
