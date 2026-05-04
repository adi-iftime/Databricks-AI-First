---
name: enforce-atomic-parallelism
description: Atomic tasks, parallel dispatch for independent work, separate Task per task even when roles match.
type: guardrail
severity: high
---

# enforce-atomic-parallelism

Ensures work is **split into atomic tasks** and **executed in parallel** when dependencies allow—including when multiple tasks map to the **same** executing agent role.

## Enforcement

### Planner ([planner-agent.md](../agents/planner-agent.md))

**Block** (reject or split further) plans that:

- **Batch** independent deliverables into one task when they could be separate (e.g. “Implement features A, B, C” as a single row without a hard dependency).
- Omit **explicit dependencies** when tasks are actually ordered (hiding parallelism incorrectly).

**Require:**

- **One clear deliverable** per task; **minimal** scope.
- **Independent** tasks each have **no dependency** on the other unless there is a real ordering/shared-contract reason.

### Orchestrator ([orchestrator-agent.md](../agents/orchestrator-agent.md))

**Block** orchestration patterns that:

- Run **independent** tasks **sequentially** when they could run in the same wave (same turn / parallel lane).
- **Reuse one subagent** or **one `Task` call** to cover **multiple** independent planned tasks (each task → **exactly one** `Task` → **one** subagent instance).

**Require:**

- **`PARALLEL:`** lane for all tasks whose dependencies are satisfied and which do not contend for the **same mutable artifact** (see [orchestration-rules.md](../rules/orchestration-rules.md) and [execution-rules.md](../rules/execution-rules.md)).
- **Same executing role** (e.g. three `backend-developer` tasks with no deps) → **three** parallel **`Task`** invocations—**not** one combined run.

### Exceptions (do not force false parallelism)

- **True dependency** (Task B needs output of Task A).
- **Exclusive mutable surface** (same file/module) unless orchestrator marks boundaries—then **sequential**.
- **Mandatory phase order** (e.g. **security gate before QA**) per [orchestration-rules.md](../rules/orchestration-rules.md)—never parallelize across that boundary.

## Priority

Works with [require-plan-approval.md](require-plan-approval.md): approval first, then **maximize parallelism** subject to dependencies and guardrails.
