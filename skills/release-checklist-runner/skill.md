---
id: release-checklist-runner
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Track release readiness checks and post-release verification.

## Inputs

- Required: release scope and deployment process.

## Process

1. Build pre-release checklist.
2. Mark required checks and blockers.
3. Build post-release validation items.

## Output Format

- Checklist with `done`, `pending`, `blocked` statuses.

## Guardrails

- Never mark ready if required checks are blocked.

## Quality Checks

- Includes rollback verification and monitoring checks.

## Failure Mode

If process details are missing, return baseline checklist plus unknowns.
