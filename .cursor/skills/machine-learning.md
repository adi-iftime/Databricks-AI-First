---
name: machine-learning
description: Model training, evaluation, features, and ML experimentation.
type: skill
domain: data
---

# Skill: Machine learning

Reusable capability definition for **modeling and prediction**. Not tied to a single agent; routing is defined in orchestration rules.

## Technologies

- Training and evaluation stacks **already present** in the repository (e.g. scikit-learn, PyTorch, XGBoost, notebooks).
- Feature stores or offline feature pipelines **when the project already uses them**.

## Patterns

- Train/validation/test discipline, leakage avoidance, reproducible seeds and configs.
- Model cards or equivalent documentation when the team expects them.

## Domain knowledge

- Metrics selection per problem type; calibration; drift basics at a high level.

## Best practices

- Prefer simple, interpretable baselines before complexity.
- Keep experiment scope aligned to the task; do not expand into pipeline or BI ownership.
