---
id: changelog-drafter
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Convert merged changes into user-relevant release notes.

## Inputs

- Required: commit set or merged PR summaries.

## Process

1. Group changes by category.
2. Remove internal-only noise.
3. Draft concise release entries.

## Output Format

- Sections: `Added`, `Changed`, `Fixed`, `Deprecated`.

## Guardrails

- Include breaking changes explicitly.

## Quality Checks

- Entries describe user/system impact.

## Failure Mode

If commit data is sparse, produce draft entries with confidence labels.
