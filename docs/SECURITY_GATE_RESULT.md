# Security gate — SCRUM-33 / SEC-02

**REVIEW RESULT: CLEAR**

Review scope: repository artifacts for Databricks Asset Bundles, Delta Live Tables entrypoint, and GitHub Actions workflows using **Personal Access Token** authentication for CI/CD.

## Checks

| Control | Status |
| ------- | ------ |
| CI/CD uses only **`DATABRICKS_HOST`** and **`DATABRICKS_TOKEN`** from GitHub Secrets (no alternate identity env vars in workflows) | Pass |
| Workflows do not echo tokens; PAT supplied via `env` to CLI steps only | Pass |
| Bundle `workspace.root_path` is under `/Shared/.bundle/...`, not `/Workspace/Users/...` | Pass |
| `workspace.host` is a literal URL string in `databricks.yml` (replace placeholder before production) | Pass |
| `.gitignore` excludes `.env`, `.databricks/`, `.bundle/` | Pass |
| No `DATABRICKS_TOKEN` or raw PAT material committed in repository files | Pass |

## Notes

- Replace the placeholder host in `databricks.yml` before connecting to a real workspace; keep it aligned with **`DATABRICKS_HOST`**.
- PAT inherits the **Databricks user’s** workspace and Unity Catalog permissions—use a dedicated automation identity and least-privilege grants where possible.
- **Fork PRs:** the remote `bundle validate` step is **skipped** when the PR head repo differs from the base repo (forks cannot use repository secrets); offline `pytest` still runs.
- Rotate **`DATABRICKS_TOKEN`** on policy and revoke when automation ownership changes.

**Gate decision:** **CLEAR** — proceed to QA (SCRUM-34 / QA-01).
