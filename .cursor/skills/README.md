# Skills in this repository

All skills are **single Markdown files** directly under **`.cursor/skills/`**. Names match the former pack folders (e.g. `planning-and-task-breakdown.md`). Longer workflows may merge former `SKILL.md` plus extras into one file (see **`idea-refine.md`**).

| Kind | Examples | Used for |
| ---- | -------- | -------- |
| **Route modules** (short) | `backend.md`, `testing.md`, `application-security.md`, … | Default **skill → agent** routing in [orchestration-rules.md](../rules/orchestration-rules.md). |
| **Workflow skills** (expanded) | `test-driven-development.md`, `planning-and-task-breakdown.md`, … | Reference these filenames in **`PLAN:`** tasks when that workflow applies. |

Lifecycle (workflow skills):

```
  DEFINE          PLAN           BUILD          VERIFY         REVIEW          SHIP
 idea-refine.md   planning…      incremental…   browser-devtools   code-review…   git-workflow…
 spec-driven.md                  TDD, frontend, api-design      security…      ci-cd, ship…
```

---

## Workflow skill files

| Skill file |
| ---------- |
| [idea-refine.md](idea-refine.md) |
| [spec-driven-development.md](spec-driven-development.md) |
| [planning-and-task-breakdown.md](planning-and-task-breakdown.md) |
| [incremental-implementation.md](incremental-implementation.md) |
| [test-driven-development.md](test-driven-development.md) |
| [context-engineering.md](context-engineering.md) |
| [source-driven-development.md](source-driven-development.md) |
| [frontend-ui-engineering.md](frontend-ui-engineering.md) |
| [api-and-interface-design.md](api-and-interface-design.md) |
| [browser-testing-with-devtools.md](browser-testing-with-devtools.md) |
| [debugging-and-error-recovery.md](debugging-and-error-recovery.md) |
| [code-review-and-quality.md](code-review-and-quality.md) |
| [code-simplification.md](code-simplification.md) |
| [security-and-hardening.md](security-and-hardening.md) |
| [performance-optimization.md](performance-optimization.md) |
| [git-workflow-and-versioning.md](git-workflow-and-versioning.md) |
| [ci-cd-and-automation.md](ci-cd-and-automation.md) |
| [deprecation-and-migration.md](deprecation-and-migration.md) |
| [documentation-and-adrs.md](documentation-and-adrs.md) |
| [shipping-and-launch.md](shipping-and-launch.md) |
| [using-agent-skills.md](using-agent-skills.md) |

---

## Route modules (short)

`backend.md`, `frontend.md`, `data-engineering.md`, `machine-learning.md`, `business-intelligence.md`, `application-security.md`, `testing.md`

---

## Source

Content originated from the Agent Skills–style packs; subdirectory layout was flattened so every skill is exactly **one `.md` file** per skill name.
