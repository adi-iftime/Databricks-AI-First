---
description: Pre-launch checklist — parallel fan-out to reviewer, security, and QA roles, then GO/NO-GO
---

Load **`.cursor/skills/shipping-and-launch.md`**. This repo’s agent definitions live under **`.cursor/agents/`**; full pipeline order is in **`AGENTS.md`** (security before QA, etc.). For the **fan-out** below, use Cursor’s **`Task`** tool with **`subagent_type`**: **`reviewer-agent`**, **`security-engineer`**, **`qa-engineer`** (see **`.cursor/agents/*.md`** YAML `name:` fields).

`/ship` runs three specialists **in parallel** against the current change, then merges into one go/no-go decision with a rollback plan.

## Phase A — Parallel fan-out

Spawn **three** subagents in **one assistant turn** (same-turn `Task` calls) so they run in parallel.

1. **`reviewer-agent`** — Five-dimension review (correctness, readability, architecture, security, performance) on staged changes or recent commits. Use the **Review Summary** + **`REVIEW RESULT`** output in **`.cursor/agents/reviewer-agent.md`**.
2. **`security-engineer`** — Vulnerability and threat-model pass: **Security Audit Report** + **`SECURITY GATE RESULT`** per **`.cursor/agents/security-engineer.md`**.
3. **`qa-engineer`** — Test strategy / coverage analysis per **`.cursor/agents/qa-engineer.md`**.

**Do not** have one subagent spawn another. Each returns only its report to this session.

**Cursor note:** If your environment uses different `subagent_type` strings, they must match the `name:` in each agent file’s frontmatter (e.g. `reviewer-agent`, not `code-reviewer`).

**Without parallel `Task` support:** run the three passes sequentially; merge phase still applies.

## Phase B — Merge in main context

Synthesize in the main thread:

1. **Code quality** — Critical/Important from **reviewer**; tests, lint, build.
2. **Security** — Critical/High from **security-engineer**; cross-check reviewer’s security axis.
3. **Performance** — From reviewer; add profiling if the stack needs it.
4. **Accessibility** — If UI changed, check a11y (not always covered by the three roles).
5. **Infrastructure** — Env, migrations, monitoring, feature flags, Databricks/bundle config if relevant.
6. **Documentation** — README, ADRs, changelog.

## Phase C — Decision and rollback

```markdown
## Ship Decision: GO | NO-GO

### Blockers (must fix before ship)
- [Source: Critical finding + file:line]

### Recommended fixes (should fix before ship)
- [Source: Important finding + file:line]

### Acknowledged risks (shipping anyway)
- [Risk + mitigation]

### Rollback plan
- Trigger conditions: [what signals would prompt rollback]
- Rollback procedure: [exact steps]
- Recovery time objective: [target]

### Specialist reports (full)
- [reviewer-agent report]
- [security-engineer report]
- [qa-engineer report]
```

## Rules

1. Phase A runs **in parallel** when tooling allows — not sequentially by default.
2. Roles do not delegate to each other; the main agent merges in Phase B.
3. Rollback plan is mandatory before **GO**.
4. Critical findings → default **NO-GO** unless the user explicitly accepts risk.
5. **Skip fan-out** only if: ≤2 files, <50 lines diff, and no auth/payments/data/config/env — otherwise run parallel review.
