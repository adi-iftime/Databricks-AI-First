---
name: require-plan-approval
description: Blocks Task / subagent execution until the user explicitly approves the current plan or repair batch.
type: guardrail
severity: critical
---

# require-plan-approval

Cross-cutting **human-in-the-loop** gate: **no worker execution** until plan approval is explicit.

## Enforcement

**Block** use of the **`Task`** tool (and any subagent spawn) when **any** of the following hold:

- The active planner output ends with **`STATUS: WAITING_FOR_APPROVAL`** **and** the user has **not** clearly approved execution since that plan version.
- The user **requested changes** to the plan and execution has **not** been re-approved after the revised `PLAN:`.
- Approval is **not** explicitly detected (silence, ambiguous ack, or unrelated message).

**Allow** `Task` dispatch **only when**:

- **`STATUS: APPROVED`** is recorded for the **current** plan in session/controller context, **or**
- The user’s message **explicitly** approves running the plan (e.g. approve / go ahead / run / proceed / execute the plan / lgtm—judge intent, not a single keyword only), **or**
- For **repair** work only: explicit user authorization for **that repair batch** per [orchestrator-agent.md](../agents/orchestrator-agent.md).

## Interaction with agents

- **[planner-agent.md](../agents/planner-agent.md):** Emits **`WAITING_FOR_APPROVAL`** after every full plan; does **not** trigger orchestrator or `Task`.
- **[orchestrator-agent.md](../agents/orchestrator-agent.md):** Checks approval **before** grouping work or calling `Task`; emits **`EXECUTION BLOCKED:`** when not approved.

## Priority

This guardrail **overrides** convenience shortcuts: **never** parallelize or dispatch workers to “save time” without approval.
