# Jira traceability (plan execution)

Epic and stories were created under **SCRUM** via Atlassian MCP.

**Org policy update:** CI/CD authentication was moved to **Databricks PAT** (`DATABRICKS_HOST` + `DATABRICKS_TOKEN`). Jira issue **SCRUM-25** (historical “Azure SP / CI secret contract”) is **superseded** by [AUTH_DATABRICKS_TOKEN.md](AUTH_DATABRICKS_TOKEN.md); adjust or close that ticket in Jira if you still track it.


| Plan task ID | Jira key | Summary |
| ------------ | -------- | ------- |
| Epic | [SCRUM-24](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-24) | Production Databricks platform — DAB + DLT + Medallion + GitHub Actions |
| AUTH-01 | [SCRUM-25](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-25) | Azure Service Principal and CI secret contract |
| INFRA-01 | [SCRUM-26](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-26) | Bundle structure and workspace conventions |
| DAB-01 | [SCRUM-27](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-27) | Databricks Asset Bundle definition |
| DLT-01 | [SCRUM-28](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-28) | Bronze DLT pipeline |
| DLT-02 | [SCRUM-29](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-29) | Silver DLT pipeline |
| DLT-03 | [SCRUM-30](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-30) | Gold DLT pipeline |
| CICD-01 | [SCRUM-31](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-31) | GitHub Actions validate |
| CICD-02 | [SCRUM-32](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-32) | GitHub Actions deploy |
| SEC-02 | [SCRUM-33](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-33) | Security gate |
| QA-01 | [SCRUM-34](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-34) | Post-security QA |
| PR-01 | [SCRUM-35](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-35) | PR narrative |
| REV-01 | [SCRUM-36](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-36) | Final review |

### PAT auth migration (follow-up epic SCRUM-24 children)

| Plan task ID | Jira key | Summary |
| ------------ | -------- | ------- |
| PAT-DOC-01 | [SCRUM-37](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-37) | PAT runbook + repo pointers |
| PAT-CICD-01 | [SCRUM-38](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-38) | Validate workflow — PAT only |
| PAT-CICD-02 | [SCRUM-39](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-39) | Deploy workflow — PAT only |
| PAT-DOC-02 | [SCRUM-40](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-40) | SECURITY_GATE + QA docs refresh |

Dependency links between issues are captured in each issue description; use Jira **blocks / relates to** links manually if your project requires explicit link types.
