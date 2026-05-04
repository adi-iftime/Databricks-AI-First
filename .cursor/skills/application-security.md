---
name: application-security
description: Threat-aware review, API and dependency risk, and secure defaults.
type: skill
domain: security
---

# Skill: Application security

Reusable capability definition for **security review and hardening guidance**. Not tied to a single agent; routing is defined in orchestration rules.

## Technologies

- HTTP/API review patterns, session and token handling as used by the stack.
- Dependency manifests and known vulnerability workflows **if already adopted** by the repo (e.g. lockfiles, scanners).

## Patterns

- Threat modeling at change scope: assets, trust boundaries, abuse cases.
- Secure defaults: least privilege, safe error messages, input validation boundaries.

## Domain knowledge

- Common web/API vulnerability classes at a level appropriate to the change size.

## Best practices

- Prefer evidence-backed findings over speculation; separate must-fix from nice-to-have.
- Do not silently “fix everything”; align with task scope and follow-up tasks for large remediations.
