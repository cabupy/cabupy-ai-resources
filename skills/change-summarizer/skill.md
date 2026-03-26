---
id: change-summarizer
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Create concise, accurate summaries of what changed and why it matters.

## Inputs

- Required: diff, commit list, or release scope.

## Process

1. Identify high-signal changes.
2. Group by user/system impact.
3. Produce concise summary bullets.

## Output Format

- 3 to 7 bullets with behavior-centric wording.

## Guardrails

- Avoid file-by-file noise.
- Do not claim unverified outcomes.

## Quality Checks

- Summary captures intent and impact.

## Failure Mode

If change set is partial, return summary plus confidence note.
