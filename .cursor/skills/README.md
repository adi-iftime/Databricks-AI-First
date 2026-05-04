# Skills in this repository

Two kinds of skill assets live under **`.cursor/skills/`**:

| Kind | Path pattern | Used for |
| ---- | ------------ | -------- |
| **Route modules** | `*.md` at this directory root (`backend.md`, `testing.md`, …) | Default **skill → agent** mapping in [orchestration-rules.md](../rules/orchestration-rules.md); short capability tags for planner tasks. |
| **Workflow packs** | `<skill-name>/SKILL.md` | Long-form workflows (steps, checks, anti-rationalization). Incorporated from the Agent Skills pack; reference by folder + `SKILL.md` in plans. |

The orchestration **routing table** still maps the **top-level modules** (`backend.md`, `data-engineering.md`, `application-security.md`, `testing.md`, …). Packs are **additional context**: load them when the task needs that workflow even if routing stays on a domain module.

Lifecycle overview (pack skills):

```
  DEFINE          PLAN           BUILD          VERIFY         REVIEW          SHIP
 idea-refine    planning…      incremental…   browser-devtools code-review   git-workflow…
 spec-driven                   TDD, frontend, api-design       security…      ci-cd, ship…
```

---

## Workflow packs (indexed)

### Define

| Pack | Entry |
| ---- | ----- |
| idea-refine | [idea-refine/SKILL.md](idea-refine/SKILL.md) · [examples](idea-refine/examples.md) · [frameworks](idea-refine/frameworks.md) · [refinement-criteria](idea-refine/refinement-criteria.md) · [scripts/idea-refine.sh](idea-refine/scripts/idea-refine.sh) |
| spec-driven-development | [spec-driven-development/SKILL.md](spec-driven-development/SKILL.md) |

### Plan

| Pack | Entry |
| ---- | ----- |
| planning-and-task-breakdown | [planning-and-task-breakdown/SKILL.md](planning-and-task-breakdown/SKILL.md) |

### Build

| Pack | Entry |
| ---- | ----- |
| incremental-implementation | [incremental-implementation/SKILL.md](incremental-implementation/SKILL.md) |
| test-driven-development | [test-driven-development/SKILL.md](test-driven-development/SKILL.md) |
| context-engineering | [context-engineering/SKILL.md](context-engineering/SKILL.md) |
| source-driven-development | [source-driven-development/SKILL.md](source-driven-development/SKILL.md) |
| frontend-ui-engineering | [frontend-ui-engineering/SKILL.md](frontend-ui-engineering/SKILL.md) |
| api-and-interface-design | [api-and-interface-design/SKILL.md](api-and-interface-design/SKILL.md) |

### Verify

| Pack | Entry |
| ---- | ----- |
| browser-testing-with-devtools | [browser-testing-with-devtools/SKILL.md](browser-testing-with-devtools/SKILL.md) |
| debugging-and-error-recovery | [debugging-and-error-recovery/SKILL.md](debugging-and-error-recovery/SKILL.md) |

### Review

| Pack | Entry |
| ---- | ----- |
| code-review-and-quality | [code-review-and-quality/SKILL.md](code-review-and-quality/SKILL.md) |
| code-simplification | [code-simplification/SKILL.md](code-simplification/SKILL.md) |
| security-and-hardening | [security-and-hardening/SKILL.md](security-and-hardening/SKILL.md) |
| performance-optimization | [performance-optimization/SKILL.md](performance-optimization/SKILL.md) |

### Ship

| Pack | Entry |
| ---- | ----- |
| git-workflow-and-versioning | [git-workflow-and-versioning/SKILL.md](git-workflow-and-versioning/SKILL.md) |
| ci-cd-and-automation | [ci-cd-and-automation/SKILL.md](ci-cd-and-automation/SKILL.md) |
| deprecation-and-migration | [deprecation-and-migration/SKILL.md](deprecation-and-migration/SKILL.md) |
| documentation-and-adrs | [documentation-and-adrs/SKILL.md](documentation-and-adrs/SKILL.md) |
| shipping-and-launch | [shipping-and-launch/SKILL.md](shipping-and-launch/SKILL.md) |

### Meta

| Pack | Entry |
| ---- | ----- |
| using-agent-skills | [using-agent-skills/SKILL.md](using-agent-skills/SKILL.md) |

---

## Route modules (existing)

These short files drive default role routing—see [AGENTS.md](../../AGENTS.md) and [orchestration-rules.md](../rules/orchestration-rules.md):

- `backend.md`, `frontend.md`, `data-engineering.md`, `machine-learning.md`, `business-intelligence.md`, `application-security.md`, `testing.md`

---

## Source

Workflow packs were incorporated from the former `new/skills/` tree (Agent Skills–style material); that duplicate has been removed from the repository.
