---
description: Create a new GitHub PR with the PR writer structured description format
---

Load **`.cursor/agents/pr-writer-agent.md`**. Open a **new** pull request for the changes on this branch. Default new PRs to **draft** unless the user asks for ready-for-review.

Use **`featureKey`** and branch name from the agent doc to avoid duplicating an existing PR for the same work.

## Title

Plain descriptive sentence (no `feat:` prefixes, no ticket IDs) — see the agent.

## Body — use this structure for NEW PRs

Do **not** paste raw `git diff`, directory listings, or generic **Context / Changes / Files** dumps. Group by **domain** (Backend, Data, etc.), not by filename.

```markdown
### 🚀 <Short Feature Title>

Feature: <featureKey>

---

### 🧠 Context

1–3 sentences explaining why this exists.

---

### ✨ What’s included

Group by domain (NOT files). Omit empty sections.

#### 🖥 Backend
- …

#### 🎨 Frontend
- …

#### ⚙️ Data / Pipelines
- …

#### 🤖 ML / Data Science (if applicable)
- …

#### 🧪 Testing
- …

---

### 🔍 Flow Impact Summary

- 3–6 bullets: behavioral / system impact only (no file paths)
- Based on the actual diff — no invented behavior

---

### 🔍 Key Areas to Review

- `path/to/file` → why it matters (important paths only)

---

### 🧪 How to Test

Minimal runnable steps (commands, targets).

---

### 📌 Notes (optional)

- Draft status, limitations, special instructions
```

Full detail and constraints: **`.cursor/agents/pr-writer-agent.md`** (Flow Impact rules, forbidden sections).
