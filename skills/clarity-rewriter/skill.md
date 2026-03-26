---
id: clarity-rewriter
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Improve technical writing clarity without altering intent.

## Inputs

- Required: source text and target audience.

## Process

1. Remove ambiguity and redundant wording.
2. Make steps explicit.
3. Preserve terminology consistency.

## Output Format

- Revised text plus short change rationale.

## Guardrails

- Do not modify technical meaning.
- Do not remove safety warnings.

## Quality Checks

- Reader can follow instructions in one pass.

## Failure Mode

If source text is inconsistent, return assumptions and flagged conflicts.
