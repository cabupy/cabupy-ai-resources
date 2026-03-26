---
id: risk-assessment
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Identify and prioritize risks in a change set.

## Inputs

- Required: change summary or diff.
- Optional: release window, SLAs.

## Process

1. Detect risk vectors (correctness, security, operability).
2. Score impact and likelihood.
3. Propose mitigation and ownership.

## Output Format

- Risk table: `risk`, `impact`, `likelihood`, `mitigation`, `owner`.

## Guardrails

- Do not classify as critical without evidence.
- Keep mitigations realistic for current scope.

## Quality Checks

- Every risk includes mitigation.
- Severity aligns with user/system impact.

## Failure Mode

Return preliminary risks and list missing context.
