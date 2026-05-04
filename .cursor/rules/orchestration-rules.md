---
name: orchestration-rules
description: Parallelism, role routing, security gate order, and repair loops.
type: rule
applies_to: orchestrator
---

# Orchestration rules

Configuration for **orchestrator-agent** behavior: ordering, parallelism, and **dynamic agent selection**.

## Inputs

- Planner output (`PLAN:`) with **required skills** and dependencies only.
- `.cursor/skills/*.md` for capability nuance when disambiguating.
- `.cursor/agents/*.md` for **role boundaries** (what a worker may/may not do)—not for embedded skill lists.

## Parallel vs sequential

- **PARALLEL:** tasks whose dependencies are satisfied and which do not require exclusive access to the same mutable artifacts (see guardrails for file ownership).
- **SEQUENTIAL:** tasks in dependency order; never run a task before all listed upstream tasks complete successfully.

## Agent selection (dynamic)

1. For each task, collect its **required skill references** (skill modules).
2. Map skill modules to **default executing roles** using the routing table below (extend by adding rows—**do not** hardcode mappings inside agent files).
3. If multiple roles could satisfy the task, choose the **most specialized** role whose responsibilities in `.cursor/agents/<role>.md` best match the **primary deliverable** of the task.
4. If no role fits, assign the **closest** role and record **`Skill gap:`** in the execution brief.
5. Emit an **execution plan** that adds `Assigned agent:` per task (this is the system-of-record for who runs the task).

### Strict data / analytics / ML / security isolation

Each **atomic** task maps to **exactly one** of these executing roles (no mixed ownership in a single task):

| Intent (examples) | Route to |
|---------------------|----------|
| ETL/ELT, ingestion, streaming, Spark/Databricks/Kafka/Airflow, warehouse/medallion physicalization | `data-engineer` |
| ML training, evaluation, prediction services, experimentation | `data-scientist` |
| SQL analysis, KPI/reporting, Power BI/Tableau, business insights | `data-analyst` |
| OWASP-style review, API/auth review, dependency risk, misconfiguration / leak findings | `security-engineer` |

If intent spans more than one row → **split** into separate tasks in planning; **never** assign mixed responsibilities to a single task.

### Default routing table (skill module → role)

| Skill module file | Default executing agent |
|-------------------|-------------------------|
| `backend.md` | `backend-developer` |
| `frontend.md` | `frontend-developer` |
| `data-engineering.md` | `data-engineer` |
| `machine-learning.md` | `data-scientist` |
| `business-intelligence.md` | `data-analyst` |
| `application-security.md` | `security-engineer` |
| `testing.md` | `qa-engineer` |

**Multi-skill tasks:** pick the agent responsible for the **largest** or **riskiest** slice (primary deliverable). If the task truly spans equal-weight slices, **split the task** in planning rather than overloading one worker.

---

## Mandatory execution phases (security gate)

**Decided order** for `security-engineer`, `qa-engineer`, and `reviewer-agent` relative to **`pr-writer-agent`:**

1. **`security-engineer`** first among the three gates (before **QA**).
2. **`qa-engineer`** second (only after **CLEAR**).
3. **`pr-writer-agent`** third (PR title/body so the review is not “diff-only”).
4. **`reviewer-agent`** last (merge-style **REVIEW RESULT** + GitHub comment).

For any feature slice that includes **implementation work** (backend, frontend, data-engineer, data-scientist, or data-analyst deliverables), the orchestrator **must** enforce this **relative order**:

1. **Implementation workers** — all implementation tasks for the slice, respecting their own dependency graph and parallelism rules.
2. **`security-engineer`** — **mandatory security gate** before QA: produces a findings report and a gate decision (**CLEAR** / **BLOCKED**).
3. **`qa-engineer`** — **only after** security gate is **CLEAR** for the same slice (model as explicit dependency in `EXECUTION` / task graph).
4. **`pr-writer-agent`** — after QA completes for the slice (or when policy says PR notes are needed).
5. **`reviewer-agent`** — final review pass on the assembled change narrative and diffs; **must** post its summary as a **GitHub PR comment** (see `.cursor/agents/reviewer-agent.md`). Dispatch **after** a PR exists or is updated (draft PR from hooks and/or pr-writer output) so the reviewer receives **PR URL or number**, **diff vs base**, and **PR metadata**.

**Reviewer inputs (mandatory bundle):** `PR URL` or (`owner/repo` + `PR number`), base branch name, head branch, and the same diff / description context used for review.

**Reviewer output:** structured `REVIEW RESULT` **and** a posted GitHub comment per reviewer-agent—**not** optional when a PR is in scope.

**Hard blocker:** if security is **BLOCKED**, **do not dispatch QA** for that slice. Return to the appropriate **implementation workers** (and/or planner for scope errors), then **re-run the security gate** before QA resumes.

Purely analytical or docs-only slices with **no** implementation surface may omit implementation workers; still run **security-engineer** when the change touches auth, data handling, or deployable artifacts—when in doubt, include the gate.

## Cursor execution mapping

- One runnable task → one **`Task` tool** invocation (subagent) unless guardrails forbid splitting.
- **Parallel** lane: multiple `Task` calls **in the same assistant turn** when tasks are independent.
- **Sequential** lane: await results, pass condensed context forward, then dispatch the next `Task`(s).

## Execution plan shape

```text
EXECUTION:
PARALLEL:
- Task A → Assigned agent: …
SEQUENTIAL:
- Task B → Assigned agent: …
```

---

## Self-healing loop (post-review)

The workflow is a **closed loop**, not strictly linear: **Planner → Orchestrator → Workers → Security gate → QA → PR writer → Reviewer → (repair)**. After **PR create/update**, the orchestrator **must** invoke **`reviewer-agent`** with PR identifiers so the review can be **posted to the PR thread** (GitHub-native feedback loop).

### Reviewer routing (input to orchestrator)

The reviewer emits the mandatory block defined in `.cursor/agents/reviewer-agent.md`:

- `APPROVED` → orchestrator takes **no** further dispatch action for that feature slice.
- `MINOR FIXES` → **Case A** (below).
- `MAJOR ISSUES` → **Case B** (below).

Respect **repair iteration limits** in `.cursor/guardrails/guardrails.md`.

### Case A — Minor fixes

- **Do not** invoke planner again for the same feature unless guardrails say otherwise.
- Build a **delta execution plan**: only tasks/workers implicated by `ISSUES` and `RECOMMENDED ACTION`.
- Re-dispatch **only** those workers via **`Task`**, in parallel when their dependencies are satisfied.
- **Preserve** outputs from tasks not listed for redo (do not re-run unchanged lanes).
- If **implementation** code paths change, **re-run `security-engineer`** for the slice before any **qa-engineer** dispatch resumes (gate must return **CLEAR** again).

### Case B — Major issues

- **Re-run planner** to produce a revised `PLAN:` that incorporates reviewer findings and missing requirements.
- **Re-orchestrate** from the new plan (full or partial tree per planner output).
- **Jira:** when a Jira issue exists and Atlassian MCP is available, **update** the story (description, AC, or comment) to reflect the replan—do not silently diverge from the ticket.
- Then dispatch workers per the new execution plan.

### Re-execution mode (orchestrator)

- Accept **corrected tasks** or a **subset plan** from the system controller.
- Maintain a **preserve list** (tasks/files OK as-is) vs **redo list** (must re-execute).
- Support **parallel** re-dispatch for independent redo tasks.
- After each repair pass, re-run the **post-implementation tail** as needed: **`security-engineer`** (when implementation changed) → **`qa-engineer`** → **`pr-writer`** (if PR text should change) → **`reviewer-agent`** until `APPROVED` or iteration cap.
