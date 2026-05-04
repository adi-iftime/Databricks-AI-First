---
name: planning-rules
description: Task splitting, skills-first plans, dependencies, and replanning policy.
type: rule
applies_to: planner
---

# Planning rules

Configuration for **planner-agent** behavior. Agent personas live in `.cursor/agents/`; capabilities live in `.cursor/skills/`.

## Task splitting

- Prefer **vertical slices** that deliver testable value: smallest unit that still makes sense to review.
- Split when: distinct dependency graphs, different risk domains, or different validation commands.
- Merge when: separation would force artificial handoffs or duplicate context without benefit.
- **Data / ML / BI / security:** never combine **pipeline engineering**, **model building**, **BI reporting**, and **security review** in one task—use separate tasks per `.cursor/rules/orchestration-rules.md` isolation table.
- **QA tasks** must declare a dependency on the **security gate** task for the same slice (security **CLEAR**) before tests execute, per orchestration rules.
- **Gate phase order** for a slice is fixed in [orchestration-rules.md](orchestration-rules.md): **security-engineer** → **qa-engineer** → **pr-writer-agent** → **reviewer-agent** after implementation—do not imply a different sequence in dependencies unless documenting an exceptional one-off (document why).

## Skills-first (mandatory)

1. For each task, list **required skills** as references to **`.cursor/skills/<name>.md`** files (e.g. `backend.md`, `planning-and-task-breakdown.md`)—see [`.cursor/skills/README.md`](../skills/README.md).
2. **Do not** emit executing worker names in the planner output; the **orchestrator** assigns agents using `.cursor/rules/orchestration-rules.md`.
3. If no skill module clearly fits, document **`Skill gap:`** with what is missing and which skill module is closest.

## Dependencies

- Declare explicit upstream tasks for: shared contracts, ordering-sensitive migrations, or tests that need implementations to exist.
- Prefer **no false dependencies** that block parallelism without a concrete reason.

## Planner output shape

```text
PLAN:
- Task 1: <short title>
  - Required skills: <skill-file refs>
  - Dependencies: [no dependencies]

- Task 2: <short title>
  - Required skills: …
  - Dependencies: [depends on Task 1]
```

Optional per task: `Skill gap: …`

## Agent selection

- **Not performed here.** See `orchestration-rules.md`.

## Re-planning after major review findings

When the controller requests a **replan** (reviewer `MAJOR ISSUES`):

- Produce a **new** `PLAN:` (optionally prefix context e.g. `REPLAN v2:`) that incorporates missing requirements, architecture corrections, and explicit dependency changes.
- Call out **superseded** assumptions from the prior plan when that reduces ambiguity for workers.
- Keep tasks as small as the corrected scope allows; do not copy forward tasks that are no longer valid without editing them.
