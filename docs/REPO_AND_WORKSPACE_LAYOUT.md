# Repository and workspace layout

## Bundle identity

| Property | Value |
| -------- | ----- |
| Bundle name | `databricks_ai_first` |
| Workspace deployment root | `/Workspace/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/${bundle.target}` (resolves per deploying user / PAT identity) |
| Declarative config | [`databricks.yml`](../databricks.yml) at repository root |

Bundle files and deployment state land under the **current user’s** workspace folder (see `workspace.root_path` in [`databricks.yml`](../databricks.yml)). That avoids deploying under **`/Workspace/Shared`**, which is writable by broad workspace groups. CI deploys use whatever identity owns **`DATABRICKS_TOKEN`**, so the path resolves under that principal.

**Targets `dev` and `prod`:** both use Databricks bundle **`mode: production`**. The name `dev` is only the bundle target used by CI (`-t dev`); it does not mean “development mode” in the bundle sense.

## Repository structure

```
.
├── databricks.yml              # DAB root: workspace host (literal), root_path, targets, pipelines
├── README.md
├── docs/                       # Runbooks and traceability
├── src/
│   └── pipelines/
│       └── medallion_dlt.py    # Delta Live Tables: Bronze → Silver → Gold
├── tests/                      # Lightweight config checks (offline)
├── scripts/                    # Optional helpers (empty by default)
└── .github/
    └── workflows/              # validate + deploy (Azure SP only)
```

## Configurable data paths

Bronze ingestion uses **Auto Loader** (`cloudFiles`) against a Unity Catalog **volume** (or compatible cloud path). Override defaults with bundle variable **`bronze_source_path`** in [`databricks.yml`](../databricks.yml). Seed that location with JSON files before starting the pipeline, or adjust the path to your landing zone.
