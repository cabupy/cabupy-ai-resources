---
id: nodejs-backend-base
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-26
---

## Purpose

Build and maintain everyday Node.js backend features with production-ready
patterns.

## Inputs

- Required: feature or bug scope, API contract, current backend structure.
- Optional: framework preference, testing conventions, deployment constraints.

## Workflow

1. Map feature requirements to modules and endpoints.
2. Implement typed controllers, services, and data access.
3. Add validation, error handling, and tests.
4. Verify reliability and maintainability.

## Skills Used

- change-summarizer
- test-case-design
- coverage-gap-finder
- security-checklist

## Output Format

- Files changed and responsibilities.
- API behavior summary.
- Validation and test notes.

## Guardrails

- Do not ship endpoints without input validation.
- Do not expose internal errors to clients.

## Quality Checks

- Strict typing and explicit error paths.
- Tests cover happy and failure paths.

## Failure Mode

If architecture is ambiguous, return a minimal modular baseline and assumptions.
