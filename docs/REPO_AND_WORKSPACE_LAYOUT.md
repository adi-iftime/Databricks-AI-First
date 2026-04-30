# Repository and workspace layout

## Bundle identity

| Property | Value |
| -------- | ----- |
| Bundle name | `databricks_ai_first` |
| Workspace deployment root | `/Shared/.bundle/databricks_ai_first` |
| Declarative config | [`databricks.yml`](../databricks.yml) at repository root |

All bundle sync and deployment state for this project must remain under **`/Shared/.bundle/databricks_ai_first`**, not under any user’s **`/Workspace/Users/...`** path.

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
