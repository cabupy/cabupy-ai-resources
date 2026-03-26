---
id: angular-feature-development
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-26
---

## Purpose

Implement Angular features with modular architecture and maintainable state
boundaries.

## Inputs

- Required: feature scope, routes, APIs, and expected user flows.
- Optional: current module layout, guards, interceptors, style conventions.

## Process

1. Define feature module boundaries and routing strategy.
2. Separate container logic, services, and presentational components.
3. Integrate data and form handling with consistent patterns.

## Output Format

- Module and routing plan.
- Service/component responsibility map.

## Guardrails

- Do not place business logic directly in templates.
- Do not bypass shared interceptors or guards.

## Quality Checks

- Module boundaries are explicit.
- Route transitions and forms handle error states clearly.

## Failure Mode

If module constraints are unknown, produce a conservative default design.
