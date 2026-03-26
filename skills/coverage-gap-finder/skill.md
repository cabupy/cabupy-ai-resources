---
id: coverage-gap-finder
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Find behavior changes that are not represented in tests.

## Inputs

- Required: diff and current tests.

## Process

1. Map changed branches and side effects.
2. Cross-check with existing tests.
3. Report missing scenarios.

## Output Format

- Gap list: `area`, `missing_case`, `suggested_layer`.

## Guardrails

- Focus on behavior gaps, not line-count metrics.

## Quality Checks

- Every gap has a concrete test suggestion.

## Failure Mode

If tests are unavailable, provide likely gap candidates and confidence level.
