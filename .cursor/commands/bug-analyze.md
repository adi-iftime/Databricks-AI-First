---
description: Analyze code or a diff for bugs — correctness and edge cases only
---

Examine the provided code or diff for **defects**, not style or refactors:

- Logic errors; unhandled edge cases; bad assumptions in control flow
- Concurrency or ordering issues; null/empty handling; off-by-one errors

**Rules:** Do not refactor, add features, or propose broad architecture changes unless strictly necessary to address a found bug.

**Output:** Brief summary; **Critical** / **Potential** / **Edge cases**; confidence (**Low** / **Medium** / **High**).
