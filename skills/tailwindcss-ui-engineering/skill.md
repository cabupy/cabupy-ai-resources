---
id: tailwindcss-ui-engineering
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-26
---

## Purpose

Build Tailwind CSS interfaces with scalable utility composition and design
token consistency.

## Inputs

- Required: UI scope, spacing/typography expectations, theme constraints.
- Optional: component library rules, responsive breakpoints.

## Process

1. Define semantic class strategy and reusable patterns.
2. Implement responsive layouts and component states.
3. Validate readability, contrast, and interaction feedback.
4. Ensure design token usage is consistent across components.

## Output Format

- Tailwind composition guidelines per component type.
- Reusable class patterns and state variants.

## Guardrails

- Do not hardcode styles when semantic tokens exist.
- Do not duplicate utility groups without extracting patterns.

## Quality Checks

- Desktop and mobile behavior are both validated.
- Visual states are consistent across interactions.

## Failure Mode

If theme tokens are missing, return a safe temporary style contract.
