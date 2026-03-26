---
id: react-feature-development
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-26
---

## Purpose

Implement React features with clear component boundaries and predictable data
flow.

## Inputs

- Required: feature scope, route or container, API interactions.
- Optional: current component tree, performance constraints.

## Process

1. Split the feature into view, state, and side-effect responsibilities.
2. Define reusable components and their typed interfaces.
3. Implement data access and mutation patterns consistently.

## Output Format

- Component map and responsibilities.
- Data-flow notes and integration points.

## Guardrails

- Do not over-centralize local UI state.
- Do not couple business logic to presentational components.

## Quality Checks

- Components have explicit props and clear ownership.
- Data updates are predictable and testable.

## Failure Mode

If architecture is unclear, return a phased implementation proposal.
