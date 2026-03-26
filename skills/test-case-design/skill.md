---
id: test-case-design
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Transform requirements or diffs into concrete test cases.

## Inputs

- Required: expected behavior and change details.

## Process

1. Enumerate happy, edge, and failure paths.
2. Map each scenario to best test layer.
3. Add expected outcomes and key assertions.

## Output Format

- Table: `scenario`, `layer`, `assertions`, `priority`.

## Guardrails

- Avoid redundant cases.
- Keep assertions behavior-focused.

## Quality Checks

- Includes at least one negative path for risky areas.

## Failure Mode

If behavior is vague, return candidate scenarios and open questions.
