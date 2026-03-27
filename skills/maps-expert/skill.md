---
id: maps-expert
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-26
---

## Purpose

Implement reliable map experiences across major web mapping libraries.

## Inputs

- Required: map use case, target framework, data volume expectations.
- Optional: provider constraints, mobile targets, interaction requirements.

## Process

1. Select mapping stack and rendering strategy.
2. Define container sizing and responsive behavior.
3. Implement data layers, interactions, and resize handling.

## Output Format

- Library recommendation and rationale.
- Implementation checklist for UX, performance, and accessibility.

## Guardrails

- Do not ignore explicit map container sizing.
- Do not hardcode keys or expose sensitive map credentials.

## Quality Checks

- Desktop and mobile interactions are validated.
- Coordinate format and bounds handling are explicit.

## Failure Mode

If stack context is missing, return a library-agnostic baseline plan.
