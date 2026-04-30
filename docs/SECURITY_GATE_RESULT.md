# Security gate — SCRUM-33 / SEC-02

**REVIEW RESULT: CLEAR**

Review scope: repository artifacts for Databricks Asset Bundles, Delta Live Tables entrypoint, and GitHub Actions workflows after implementation of AUTH-01 through CICD-02.

## Checks

| Control | Status |
| ------- | ------ |
| No Databricks PATs or `DATABRICKS_TOKEN` usage in workflows or docs | Pass |
| CI uses Azure Entra service principal path (`DATABRICKS_AUTH_TYPE=azure-client-secret`) with secrets limited to `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`, `DATABRICKS_HOST` | Pass |
| Workflows map required GitHub secret names to CLI variables without adding PAT-based auth | Pass |
| Bundle `workspace.root_path` is under `/Shared/.bundle/...`, not `/Workspace/Users/...` | Pass |
| `workspace.host` is a literal URL string in `databricks.yml` (replace placeholder before production) | Pass |
| `.gitignore` excludes `.env`, `.databricks/`, `.bundle/` | Pass |
| No client secrets committed in repository files | Pass |

## Notes

- Replace the placeholder host `https://adb-0000000000000000.0.azuredatabricks.net` before connecting to a real workspace.
- Apply least-privilege workspace and Unity Catalog grants to the deployment service principal per environment.
- Pull requests from forks will fail `bundle validate` unless you use a policy that avoids exposing secrets to untrusted code (e.g. restrict workflows or use `pull_request_target` with extreme care).

**Gate decision:** **CLEAR** — proceed to QA (SCRUM-34 / QA-01).
