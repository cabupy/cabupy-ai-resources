---
id: security-checklist
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Detect common security flaws in changed code.

## Inputs

- Required: diff or touched files.

## Process

1. Check input validation and output encoding.
2. Check authz/authn enforcement.
3. Check secrets handling and sensitive logging.

## Output Format

- Checklist with `pass`, `warning`, or `fail` plus notes.

## Guardrails

- Report only evidence-backed findings.
- Avoid tool-specific claims without context.

## Quality Checks

- Each fail state includes remediation guidance.

## Failure Mode

If security-sensitive paths are unknown, return baseline checklist and gaps.
