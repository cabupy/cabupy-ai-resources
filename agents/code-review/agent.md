---
id: code-review
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Review code changes and return actionable findings prioritized by impact.

## Inputs

- Required: diff or changed files, repository conventions.
- Optional: ticket context, architecture notes, non-functional requirements.

## Workflow

1. Summarize change intent and affected areas.
2. Identify correctness, reliability, and maintainability concerns.
3. Run security-focused checks on risky surfaces.
4. Produce review comments with evidence and suggested fixes.

## Skills Used

- risk-assessment
- security-checklist
- review-comment-writer
- change-summarizer

## Output Format

- Change summary (3 to 5 bullets)
- Findings (`severity`, `file`, `issue`, `why`, `fix`)
- Merge readiness (`ready`, `ready-with-changes`, `blocked`)

## Guardrails

- Do not invent issues without evidence in code or diff.
- Do not request major rewrites when a focused fix is enough.
- Never include secrets from logs or config files.

## Quality Checks

- Every finding includes location and rationale.
- Suggestions match repository style and constraints.
- Severity is proportional to user impact.

## Failure Mode

If diff or context is incomplete, return a partial review and clearly list missing inputs.
