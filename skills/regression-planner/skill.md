---
id: regression-planner
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Plan regression coverage based on impacted behavior and dependencies.

## Inputs

- Required: changed components and affected flows.

## Process

1. Identify blast radius.
2. Rank critical regression paths.
3. Propose execution order and minimum gates.

## Output Format

- Checklist grouped by `critical`, `important`, `optional`.

## Guardrails

- Prioritize business-critical flows first.
- Avoid broad, non-actionable checklists.

## Quality Checks

- Critical paths are explicitly covered.

## Failure Mode

If dependency map is incomplete, list assumptions and tentative priorities.
