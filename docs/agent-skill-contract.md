# Agent and Skill Contract

This document defines the minimum contract for all agents and skills in this repository.

## Agent Contract

Each agent must include:

- `id`: unique kebab-case identifier.
- `purpose`: one short paragraph with the end-to-end goal.
- `inputs`: required context and optional context.
- `workflow`: ordered steps the agent follows.
- `outputs`: stable output format.
- `guardrails`: safety limits and constraints.
- `quality_checks`: validation gates before final output.
- `failure_mode`: behavior when context is missing or ambiguous.
- `compatibility`: supported tools (`generic`, `codex`, `claude-code`, `gemini-cli`, `opencode`).

## Skill Contract

Each skill must include:

- `id`: unique kebab-case identifier.
- `purpose`: specific capability in one to two lines.
- `inputs`: minimal required inputs.
- `process`: deterministic execution steps.
- `outputs`: strict format.
- `guardrails`: explicit do/don't constraints.
- `quality_checks`: output quality gates.
- `failure_mode`: safe fallback behavior.
- `compatibility`: target tools.

## Frontmatter Standard

Use this frontmatter in `agent.md` and `skill.md` files:

```yaml
id: example-id
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
```

## Naming Rules

- Agent IDs should be role-oriented (`code-review`, `release-manager`).
- Skill IDs should be capability-oriented (`risk-assessment`, `clarity-rewriter`).
- Keep names short and explicit; avoid generic labels like `helper` or `utils`.
