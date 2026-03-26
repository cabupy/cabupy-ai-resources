---
id: docs-structure-planner
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Define clear documentation hierarchy and navigation.

## Inputs

- Required: audience type and doc scope.

## Process

1. Classify audiences.
2. Map each audience to required information.
3. Propose structure and file ownership.

## Output Format

- TOC proposal with section goals and target files.

## Guardrails

- Avoid deep hierarchy for small projects.

## Quality Checks

- Every section has a clear reader outcome.

## Failure Mode

If audience is undefined, provide a default split (users, contributors, maintainers).
