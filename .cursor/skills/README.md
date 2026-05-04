# Skills in `.cursor/skills/`

**Production-grade workflow skills** for AI coding agents. Each skill is a **single file**: **`.cursor/skills/<name>.md`**. Route modules at the repo root of this folder (`backend.md`, `testing.md`, …) drive default **skill → agent** mapping in [orchestration-rules.md](../rules/orchestration-rules.md); expanded workflows use hyphenated names (`planning-and-task-breakdown.md`, …).

**Full catalog** (same tables) lives in **[AGENTS.md](../../AGENTS.md#skills-catalog)** so the repository index stays one place to read.

```
  DEFINE          PLAN           BUILD          VERIFY         REVIEW          SHIP
 ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
 │ Idea │ ───▶ │ Spec │ ───▶ │ Code │ ───▶ │ Test │ ───▶ │  QA  │ ───▶ │  Go  │
 │Refine│      │  PRD │      │ Impl │      │Debug │      │ Gate │      │ Live │
 └──────┘      └──────┘      └──────┘      └──────┘      └──────┘      └──────┘
```

---

## Route modules (short — orchestrator routing)

| File | Typical agent |
| ---- | ------------- |
| [backend.md](backend.md) | `backend-developer` |
| [frontend.md](frontend.md) | `frontend-developer` |
| [data-engineering.md](data-engineering.md) | `data-engineer` |
| [machine-learning.md](machine-learning.md) | `data-scientist` |
| [business-intelligence.md](business-intelligence.md) | `data-analyst` |
| [application-security.md](application-security.md) | `security-engineer` |
| [testing.md](testing.md) | `qa-engineer` |

---

## Workflow skills (by lifecycle phase)

### Define

| Skill file | What it does | Use when |
| ---------- | ------------ | -------- |
| [idea-refine.md](idea-refine.md) | Divergent/convergent thinking; vague → concrete | Rough concept needs exploration |
| [spec-driven-development.md](spec-driven-development.md) | PRD before code | New project, feature, or major change |

### Plan

| Skill file | What it does | Use when |
| ---------- | ------------ | -------- |
| [planning-and-task-breakdown.md](planning-and-task-breakdown.md) | Tasks + acceptance + dependency order | You have a spec, need implementable units |

### Build

| Skill file | What it does | Use when |
| ---------- | ------------ | -------- |
| [incremental-implementation.md](incremental-implementation.md) | Vertical slices; implement, test, verify, commit | Multi-file change |
| [test-driven-development.md](test-driven-development.md) | Red–green–refactor; pyramid; Prove-It for bugs | Logic, bugs, behavior change |
| [context-engineering.md](context-engineering.md) | Right context at right time; rules, MCP | Session start, task switch, quality drop |
| [source-driven-development.md](source-driven-development.md) | Official docs–first; cite sources | Framework/library work |
| [frontend-ui-engineering.md](frontend-ui-engineering.md) | UI components, a11y, design systems | User-facing UI |
| [api-and-interface-design.md](api-and-interface-design.md) | Contracts, boundaries, errors | APIs and public surfaces |

### Verify

| Skill file | What it does | Use when |
| ---------- | ------------ | -------- |
| [browser-testing-with-devtools.md](browser-testing-with-devtools.md) | DevTools MCP; DOM, network, perf | Browser apps |
| [debugging-and-error-recovery.md](debugging-and-error-recovery.md) | Reproduce → localize → fix → guard | Failures, unexpected behavior |

### Review

| Skill file | What it does | Use when |
| ---------- | ------------ | -------- |
| [code-review-and-quality.md](code-review-and-quality.md) | Five-axis review; sizing; severity | Before merge |
| [code-simplification.md](code-simplification.md) | Simplify without behavior change | Hard-to-read code |
| [security-and-hardening.md](security-and-hardening.md) | OWASP-style hardening | Input, auth, data, deps |
| [performance-optimization.md](performance-optimization.md) | Measure-first; profiling | Perf requirements / regressions |

### Ship

| Skill file | What it does | Use when |
| ---------- | ------------ | -------- |
| [git-workflow-and-versioning.md](git-workflow-and-versioning.md) | Trunk-style; atomic commits | Any code change |
| [ci-cd-and-automation.md](ci-cd-and-automation.md) | Pipelines, flags, feedback loops | CI/CD changes |
| [deprecation-and-migration.md](deprecation-and-migration.md) | Deprecation and migrations | Sunsetting / moving users |
| [documentation-and-adrs.md](documentation-and-adrs.md) | ADRs, API docs, why | Architecture / API changes |
| [shipping-and-launch.md](shipping-and-launch.md) | Launch checklist, rollback | Production go-live |

### Meta

| Skill file | What it does |
| ---------- | ------------ |
| [using-agent-skills.md](using-agent-skills.md) | How to use this skill pack |

---

## How skills are referenced

In **`PLAN:`** tasks, list paths like `backend.md` or `planning-and-task-breakdown.md` under **`.cursor/skills/`** per [planning-rules.md](../rules/planning-rules.md). See **[AGENTS.md](../../AGENTS.md)** for orchestration, gates, and **Cursor commands** that load these files.
