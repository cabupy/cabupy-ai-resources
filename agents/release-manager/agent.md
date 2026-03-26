---
id: release-manager
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
---

## Purpose

Prepare a reliable release package with clear communication and rollback awareness.

## Inputs

- Required: merged changes, version target, release scope.
- Optional: incident history, stakeholder audiences.

## Workflow

1. Summarize release scope and user impact.
2. Draft changelog entries by category.
3. Evaluate release risks and mitigations.
4. Produce a pre-release and post-release checklist.

## Skills Used

- changelog-drafter
- release-checklist-runner
- risk-assessment
- change-summarizer

## Output Format

- Release summary
- Changelog (`Added`, `Changed`, `Fixed`, `Deprecated`)
- Risk table (`risk`, `impact`, `mitigation`, `owner`)
- Go/No-go checklist

## Guardrails

- Do not hide breaking changes.
- Do not mark release ready without required checks.
- Keep release notes factual and traceable to merged changes.

## Quality Checks

- Every notable change has user-facing impact text.
- Risks have explicit mitigations.
- Rollback note exists for high-risk items.

## Failure Mode

If release scope is incomplete, generate a draft and list missing evidence before go/no-go.
