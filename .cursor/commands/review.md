---
description: Conduct a five-axis code review — correctness, readability, architecture, security, performance
---

Load **`.cursor/skills/code-review-and-quality.md`**, then execute as **`.cursor/agents/reviewer-agent.md`** (merge review, GitHub PR comment when a PR exists).

Default scope: **current changes** (staged or recent commits). If the user gives a **PR number**, use **`gh pr view` / `gh pr diff`** for that PR and post the review there.

Review the change set across all five axes:

1. **Correctness** — Does it match the spec? Edge cases handled? Tests adequate?
2. **Readability** — Clear names? Straightforward logic? Well-organized?
3. **Architecture** — Follows existing patterns? Clean boundaries? Right abstraction level?
4. **Security** — Input validated? Secrets safe? Auth checked? (Use security-and-hardening skill)
5. **Performance** — No N+1 queries? No unbounded ops? (Use performance-optimization skill)

Categorize findings as Critical, Important, or Suggestion.
Output a structured review with specific file:line references and fix recommendations.
