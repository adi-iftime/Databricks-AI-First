# Databricks AI First — Medallion platform (DAB + DLT)

Production-oriented starter for **Databricks**: **Databricks Asset Bundles**, **Delta Live Tables** (Bronze → Silver → Gold), and **GitHub Actions** using **Personal Access Token** authentication (`DATABRICKS_HOST` + `DATABRICKS_TOKEN`).

Optional **Infrastructure as Code** in this repo:

- **Azure** — Bicep (`infra/main.bicep`) via workflow **Deploy Azure infrastructure (Bicep)** (manual).
- **Databricks Unity Catalog** — Terraform (`infra/terraform/`) via workflow **Deploy Databricks UC (Terraform)** (manual).
- **Application** — **Deploy Databricks bundle** runs on push to `main`/`master` (and can be run manually).

---

## Full deployment guide (Git → Azure → Databricks)

Follow in order the first time you stand up the stack. Later you only repeat the steps that change.

### 1. Git and GitHub

1. **Clone** the repository and create a working branch if you use feature branches:

   ```bash
   git clone <repository-url>
   cd Databricks-AI-First
   ```
2. **Configure GitHub** for CI/CD:
  - **Repository secrets** (Settings → Secrets and variables → Actions):

    | Secret                  | Used by                                                                            |
    | ----------------------- | ---------------------------------------------------------------------------------- |
    | `DATABRICKS_HOST`       | Validate + Deploy bundle (+ optional Terraform UC workflow)                        |
    | `DATABRICKS_TOKEN`      | Same — PAT with permission to deploy bundles and use the CLI against the workspace |
    | `AZURE_CLIENT_ID`       | **Deploy Azure infrastructure (Bicep)** — Entra app (service principal)            |
    | `AZURE_TENANT_ID`       | Same                                                                               |
    | `AZURE_SUBSCRIPTION_ID` | Same                                                                               |

     Use **OIDC (federated credentials)** for Azure: no client secret in GitHub for the Bicep workflow; configure **Federated credentials** on the app registration for `repo:OWNER/REPO:ref:refs/heads/main` (or your branch/environment). See [Connect GitHub to Azure](https://learn.microsoft.com/azure/developer/github/connect-from-azure).
3. **Commit** `databricks.yml` with a real workspace URL (see step 5). Push to `main`/`master` to trigger **Validate Databricks bundle** and **Deploy Databricks bundle** (if secrets are set).
4. **Fork PRs** — fork workflows cannot use your secrets; validation falls back to offline **pytest** only until changes are in the upstream repo.

---

### 2. Azure (optional but typical for a dedicated stack)

Do this if you provision **Databricks workspace**, **access connector**, and **ADLS Gen2** from this repo.

1. **Create a resource group** in the Azure portal or CLI (the Bicep workflow does not create the resource group).

   ```bash
   az group create -n <your-rg> -l northeurope
   ```
2. **Grant the deployment identity** permission on that subscription or resource group (e.g. **Contributor** on the RG). If you later add ARM **role assignments** in Bicep, the identity may also need **User Access Administrator** or equivalent to assign RBAC.
3. **Run the Bicep workflow** (on demand):
  - GitHub → **Actions** → **Deploy Azure infrastructure (Bicep)** → **Run workflow**.
  - Fill in **resource group**, region, workspace name, storage account name, and access connector name (see defaults in the workflow).
  - Wait until the deployment finishes.
4. **Grant the access connector managed identity access to storage** (required for Unity Catalog and ADLS paths). In Azure, assign **Storage Blob Data Contributor** (or the role your organization requires) on the **storage account** (or container scope) to the **managed identity** of the **Databricks Access Connector**. If this step is skipped, Terraform UC steps or pipeline reads may fail until RBAC is fixed.
5. **Note** the workspace URL after creation (Azure Portal → Databricks workspace → **Launch Workspace** URL / host). You will paste it into `databricks.yml` and into `DATABRICKS_HOST`.

---

### 3. Databricks (workspace configuration)

1. **Unity Catalog metastore** — The workspace must have a **metastore assigned**. If you see `No metastore assigned`, a **Databricks account / metastore admin** must attach a metastore to this workspace (often done once in the account console). Creating the metastore itself is usually **outside** this repo’s Terraform unless you use account-level automation elsewhere.
2. **Unity Catalog objects (Terraform)** — After Azure resources and storage RBAC exist, apply **Databricks-side** UC configuration (storage credential, external location, catalog `cursorfun`, schema `default`):
  - GitHub → **Actions** → **Deploy Databricks UC (Terraform)** → **Run workflow**.
  - Provide subscription ID, resource group, connector name, storage account, container name, and names consistent with Bicep defaults (or your overrides).
  - Ensure **catalog** name matches the bundle variable `catalog` in `databricks.yml` (default `cursorfun`).
   Details: [infra/terraform/README.md](infra/terraform/README.md).
3. **Bronze volume path** — The bundle default expects data under a **Unity Catalog volume**, for example:
  - Catalog `cursorfun`, schema `default`, volume suitable for `bronze_ingest` (path `/Volumes/cursorfun/default/bronze_ingest/` — adjust if your volume name differs).
   Create the volume in Catalog Explorer if it does not exist, or change `variables.bronze_source_path` in `databricks.yml` to match your layout.
4. **Edit `databricks.yml`:**
  - Set `workspace.host` to your workspace URL (literal string, **no** bundle interpolation).
  - Align `variables.catalog` and `variables.bronze_source_path` with UC and your volume.
5. **Personal Access Token** — Create a PAT in the Databricks workspace (**User Settings → Developer → Access tokens**) with rights to deploy bundles and run jobs as needed. Store it only in **GitHub Actions secrets** as `DATABRICKS_TOKEN` (and use the same host in `DATABRICKS_HOST`).

---

### 4. Application deploy (bundle + seed)

1. **CI validate** — On every push/PR to `main`/`master`, **Validate Databricks bundle** runs **pytest** and, when secrets are available, `databricks bundle validate`.
2. **CI deploy** — On push to `main`/`master`, **Deploy Databricks bundle**:
  - Runs `databricks bundle deploy` for target `dev` (or `workflow_dispatch` input).
  - Uploads the JSONL fixture to the bronze volume path (`BRONZE_SEED_DEST` in the workflow). Ensure that path matches your volume and `bundle.bronze_source_path` / pipeline configuration.
3. **Manual deploy** — You can run **Deploy Databricks bundle** from the Actions tab and choose target `dev` or `prod`.
4. **Local deploy** (optional):

   ```bash
   export DATABRICKS_HOST="https://adb-xxxxxxxx.azuredatabricks.net"
   export DATABRICKS_TOKEN="dapi…"
   databricks bundle validate -t dev
   databricks bundle deploy -t dev --auto-approve
   ```

---

### 5. Order summary (first-time)


| Order | What                                                                         |
| ----- | ---------------------------------------------------------------------------- |
| 1     | Git repo + GitHub secrets (`DATABRICKS_*`, and Azure secrets if using Bicep) |
| 2     | Azure resource group + run **Deploy Azure infrastructure (Bicep)**           |
| 3     | Azure RBAC: access connector MI → storage                                    |
| 4     | Databricks: metastore assigned to workspace                                  |
| 5     | Run **Deploy Databricks UC (Terraform)** (or configure UC manually to match) |
| 6     | Volumes / paths + edit `databricks.yml`                                      |
| 7     | Push to `main` or run **Deploy Databricks bundle**                           |


---

## Quick links

- Auth and secrets: [docs/AUTH_DATABRICKS_TOKEN.md](docs/AUTH_DATABRICKS_TOKEN.md)
- Layout and bundle root: [docs/REPO_AND_WORKSPACE_LAYOUT.md](docs/REPO_AND_WORKSPACE_LAYOUT.md)
- **Azure (Bicep):** template [`infra/main.bicep`](infra/main.bicep), workflow [`.github/workflows/infra-azure-bicep.yml`](.github/workflows/infra-azure-bicep.yml) — run **Deploy Azure infrastructure (Bicep)** on demand.
- **Databricks (Terraform / UC):** module [`infra/terraform/`](infra/terraform/), operator notes [`infra/terraform/README.md`](infra/terraform/README.md), workflow [`.github/workflows/infra-databricks-terraform.yml`](.github/workflows/infra-databricks-terraform.yml) — run **Deploy Databricks UC (Terraform)** on demand.
- Jira mapping: [docs/JIRA_TASK_MAPPING.md](docs/JIRA_TASK_MAPPING.md)

## Before every deploy (checklist)

1. `databricks.yml` → `workspace.host` matches the workspace you deploy to.
2. GitHub secrets `DATABRICKS_HOST` and `DATABRICKS_TOKEN` are set and not expired.
3. Unity Catalog paths exist for `bronze_source_path` (default under `/Volumes/cursorfun/default/bronze_ingest`).
4. **DLT:** This bundle uses `serverless: true` on the pipeline. Adjust `serverless` / `clusters` in `databricks.yml` if your workspace policy differs.
5. `workspace.root_path` is user-scoped (`/Workspace/Users/${workspace.current_user.userName}/...`) so deploy state is not under world-writable `/Workspace/Shared` unless you change it.

## Local commands

```bash
export DATABRICKS_HOST="https://adb-xxxxxxxx.azuredatabricks.net"
export DATABRICKS_TOKEN="dapixxxxxxxxxxxxxxxx"
databricks bundle validate -t dev   # requires workspace auth
databricks bundle deploy -t dev --auto-approve
```

## Offline checks

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Troubleshooting deploy


| Symptom                                                             | What to do                                                                                                                                                                                                                                              |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `You must use serverless compute in this workspace`                 | Remove classic pipeline `clusters` from `databricks.yml` and set `serverless: true` on the pipeline (this repo’s default). Redeploy.                                                                                                                    |
| `You can't use serverless compute with Spark Declarative Pipelines` | Your workspace blocks serverless DLT. Set `serverless: false`, add a `clusters` block with `label`, `node_type_id`, and `num_workers`. See [Databricks bundle pipeline docs](https://docs.databricks.com/aws/en/dev-tools/bundles/resources#pipelines). |
| `unknown field: spark_version` on `clusters[0]`                     | `spark_version` is not valid on bundle `PipelineCluster`. Remove it from `clusters`.                                                                                                                                                                    |
| `No metastore assigned for the current workspace`                   | Assign a Unity Catalog metastore to this workspace (account/metastore admin).                                                                                                                                                                           |
| `root_path` under `/Workspace/Shared` writable by all users         | Use a user-scoped `workspace.root_path` (this repo’s default).                                                                                                                                                                                          |
| Cluster / instance type errors                                      | Relevant for **classic** pipeline clusters only. Choose a `node_type_id` available in your region.                                                                                                                                                      |


