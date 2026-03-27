---
id: ui-ux-foundations
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-26
---

## Purpose

Define a practical UX/UI baseline for frontend tasks.

## Inputs

- Required: screen scope, user goals, interaction constraints.
- Optional: design system, target devices, known accessibility needs.

## Process

1. Identify user flows and critical interactions.
2. Define layout and hierarchy decisions.
3. Validate usability and accessibility baseline.
4. Align recommendations with design-system and implementation handoff.

## Output Format

- UX checklist (`flow`, `clarity`, `feedback`, `errors`, `accessibility`).
- UI consistency notes, token guidelines, and implementation recommendations.

## Guardrails

- Do not prioritize aesthetics over usability.
- Do not ignore keyboard and screen reader scenarios.

## Quality Checks

- Critical actions are discoverable in one pass.
- Error and success feedback are explicit.

## Failure Mode

If context is insufficient, provide baseline recommendations and assumptions.
