---
name: no-verbose-pr-sections
description: PR writer must not emit Context, Changes, or Files sections; no file-level lists in PR bodies.
type: guardrail
severity: medium
---

# no-verbose-pr-sections

Applies to **[pr-writer-agent.md](../agents/pr-writer-agent.md)** when generating or appending PR descriptions.

## Enforcement

**Do not** generate (new PRs):

- **`## Context`**, **`## Changes`**, **`## Files`**, or equivalents (`Files changed`, modified-file laundry lists, path dumps).

**Do not** use PR body space for:

- File-level summaries, directory trees, or copy-paste of `git diff --name-only`.

**Allowed:** optional **`Feature:** \`<featureKey>\``** line for traceability; **`## 🔍 Flow Impact Summary`** (behavior impact); **`## 🧪 How to Test`**; **`## 📝 Notes`** (optional).

**Append mode only:** **`### 🔄 Additional Changes`** is permitted as a **short narrative** of what this push adds—**not** a rename of the forbidden **`## Changes`** block and **not** a file list.

## Rationale

Diffs and GitHub already show **files**; PR text should explain **impact** and **verification**, not repeat the patch list.
