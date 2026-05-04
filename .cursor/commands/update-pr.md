---
description: Update an existing GitHub PR — append new work or refresh the description using PR writer format
---

Load **`.cursor/agents/pr-writer-agent.md`**. Prefer **updating** an open PR that matches this branch or **`featureKey`** over creating a duplicate.

**PR identifier:** **`{{pr-id}}`** when templated, or the number the user specifies (e.g. **`gh pr view 8`**).

## Two modes

### A — Routine update (new commits on same PR)

Per the agent: **append only** — do not delete prior sections. Append:

```markdown
---

### 🔄 Additional Changes

- Short narrative of what this push adds (no file lists)

### 🔍 Flow Impact (Update)

- Behavior changes introduced in this update

### 🔍 Key Areas (Update) (optional)

- New important paths only

### 🧪 Additional Testing

- …

### 📌 Notes

- …
```

### B — Reformulate / refresh the full description

When the user wants to replace a poor or auto-generated body (still the **same** PR): rewrite the **entire** description using the **same section layout as a new PR** — see **`write-new-pr.md`** (🚀 title block, 🧠 Context, ✨ What’s included by domain, 🔍 Flow Impact, 🔍 Key Areas, 🧪 How to Test, 📌 Notes). Base content on **`gh pr diff`** / branch vs base — **no** raw diff dumps or file inventory lists.

Forbidden: generic **Context / Changes / Files** sections filled with paths — see **`.cursor/agents/pr-writer-agent.md`**.
