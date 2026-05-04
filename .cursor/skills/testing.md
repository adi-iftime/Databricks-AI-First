---
name: testing
description: Unit and integration tests, runners, fixtures, and quality gates.
type: skill
domain: qa
---

# Skill: Testing

Reusable capability definition. **Not** tied to any single agent; routing is defined in orchestration rules.

## Technologies

- Test runners and frameworks **already in the repository** (e.g. pytest, JUnit, vitest)
- HTTP testing tools appropriate to the stack (client libraries, in-process app clients)
- Fixtures, factories, and snapshot tools if the repo already adopts them

## Patterns

- Arrange–act–assert; isolated unit tests vs narrower integration tests
- Stable selectors and boundary testing for public APIs
- Data setup/teardown that avoids cross-test coupling

## Domain knowledge

- Coverage as a signal, not a goal; risk-based test selection
- Flake detection: time, network, concurrency, shared global state
- CI expectations: fast feedback suites vs heavier nightly suites (project-dependent)

## Best practices

- One logical behavior per test; descriptive names
- Prefer testing public contracts over implementation details
- Fail messages should explain *what* broke and *where* to look
