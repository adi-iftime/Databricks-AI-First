---
name: backend
description: Backend services, HTTP APIs, layering, and server-side practices.
type: skill
domain: backend
---

# Skill: Backend

Reusable capability definition. **Not** tied to any single agent; routing is defined in orchestration rules.

## Technologies

- HTTP APIs (REST, common status/error patterns)
- Common backend runtimes (e.g. Python, JVM languages) as chosen by the project
- Serialization, validation, configuration, logging

## Patterns

- Layering (transport vs domain vs persistence) where the codebase already uses it
- Idempotent handlers, explicit error contracts, pagination/filtering when listing resources
- Dependency injection or composition only when the repo already establishes that style

## Domain knowledge

- Authentication/authorization boundaries (when applicable)
- Data modeling basics (entities, identifiers, consistency expectations)
- Operational concerns: health checks, graceful degradation (project-dependent)

## Best practices

- Prefer small, testable units and clear module boundaries
- Match existing framework and folder conventions in the repository
- Avoid speculative abstractions; implement what the task requires
