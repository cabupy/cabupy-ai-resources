---
id: review-comment-writer
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Rewrite raw findings into useful code review comments.

## Inputs

- Required: finding details, file location.

## Process

1. State issue and impact.
2. Explain why it matters.
3. Suggest focused next action.

## Output Format

- `severity`, `location`, `comment`, `suggested_fix`.

## Guardrails

- Keep tone constructive.
- Avoid vague advice.

## Quality Checks

- Comment is understandable without extra context.

## Failure Mode

If location is missing, return a global comment with assumptions.
