---
name: execution-rules
description: Worker scope, determinism, file ownership, and repair-pass behavior.
type: rule
applies_to: workers
---

# Execution rules

Configuration for **worker** invocations (backend, frontend, data, QA) once the orchestrator has dispatched work.

## Scope

- Each subagent receives **exactly one** task identifier and a bounded file/context list.
- Implement **only** what that task describes; defer scope questions upstream.

## Determinism and traceability

- Prefer deterministic logic for the same inputs; avoid hidden globals and time-dependent behavior unless the task requires it.
- Keep commits/diffs **minimal** and explain non-obvious choices in a short note when needed.

## File and ownership rules

- Touch **only** paths in scope for the task; do not opportunistically refactor neighbors.
- If two parallel tasks must avoid overlap, respect directory or module boundaries set by the orchestrator.
- When a shared file is genuinely required, that requirement should appear as an explicit dependency (sequential execution).

## Validation before handoff

- Run the narrowest check the repo supports for the change (unit tests, formatter, linter) when available.
- Report failures honestly; do not silence errors with broad catches unless existing code already establishes that pattern.

## Completion signal

- Return: summary, list of changed paths, commands run, and open risks or follow-ups **scoped to the task**.

## Repair passes (minor fixes)

- When invoked for a **repair iteration**, the orchestrator supplies **prior review `ISSUES`** and the **narrow scope** to fix.
- Address only listed items; do not expand into unrelated refactors.
- If an issue is unclear, return questions instead of guessing—especially when near the **repair iteration cap** in guardrails.

## After the security gate

- **Implementation workers** must treat **security-engineer** findings as input: fix **BLOCKED** items before expecting QA dispatch.
- **qa-engineer** should assume security gate **CLEAR** for the slice; if not, stop and escalate to the orchestrator.
