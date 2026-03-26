# Quality Evaluation Guide

This guide defines how to evaluate the quality of agents and skills before merge.

## Evaluation Goals

- Ensure contributions are useful in real engineering workflows.
- Keep outputs reliable, safe, and easy to validate.
- Maintain interoperability across supported tools.

## Scoring Model

Use a 1-5 score for each category.

- `1`: missing or unusable
- `3`: acceptable but incomplete
- `5`: strong and production-ready

## Agent Evaluation Rubric

Score each criterion:

- Purpose clarity: is the end-to-end role explicit?
- Input quality: are required and optional inputs clear?
- Workflow quality: are steps deterministic and practical?
- Output quality: is output format stable and actionable?
- Safety: are guardrails explicit and sufficient?
- Failure behavior: does it fail safely with missing context?
- Reusability: can it run across tool ecosystems?

## Skill Evaluation Rubric

Score each criterion:

- Capability focus: does it solve one clear problem?
- Contract quality: are inputs/process/outputs precise?
- Evidence orientation: does it avoid unsupported claims?
- Actionability: are outputs directly usable by agents?
- Guardrails and limits: are constraints explicit?
- Example quality: is there at least one reproducible example?

## Acceptance Thresholds

- Recommended merge threshold: average score >= 4.0.
- Any safety criterion below 4 requires revision.
- Missing examples block merge for new agents/skills.

## Review Checklist

- Contract follows `docs/agent-skill-contract.md`.
- Naming and structure follow repository conventions.
- `docs/tooling-matrix.md` updated when dependencies change.
- No secrets, credentials, or private data included.

## Continuous Improvement

- Re-evaluate stable resources every 90 days.
- Mark stale resources as `deprecated` until reviewed.
- Track recurring review failures and update templates accordingly.
