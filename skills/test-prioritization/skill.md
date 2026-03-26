---
id: test-prioritization
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Order test work to maximize risk reduction per effort.

## Inputs

- Required: test candidates and risk context.

## Process

1. Score each candidate by risk and cost.
2. Assign priority tier.
3. Suggest execution batch for CI and local loops.

## Output Format

- Priority list with score and rationale.

## Guardrails

- Do not prioritize only by implementation convenience.

## Quality Checks

- Top priority items cover highest-impact failures.

## Failure Mode

If risk data is missing, use conservative defaults and label assumptions.
