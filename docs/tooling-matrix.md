# Agent to Skill Matrix

This matrix defines which reusable skills are used by each base agent.

## Base Agents

| Agent | Core goal | Skills |
|---|---|---|
| `code-review` | Review code quality, risk, and security | `risk-assessment`, `security-checklist`, `review-comment-writer`, `change-summarizer` |
| `test-engineer` | Improve test strategy and regression coverage | `test-case-design`, `regression-planner`, `coverage-gap-finder`, `test-prioritization` |
| `docs-maintainer` | Keep docs useful, accurate, and actionable | `docs-structure-planner`, `clarity-rewriter`, `change-summarizer` |
| `refactor-architect` | Plan safe refactors with migration steps | `risk-assessment`, `change-summarizer`, `regression-planner` |
| `release-manager` | Prepare releases with clear notes and checks | `changelog-drafter`, `release-checklist-runner`, `risk-assessment`, `change-summarizer` |

## Notes

- Skills are cross-agent by design; do not duplicate the same capability under different names.
- If a new skill overlaps with an existing one, prefer extending the existing skill.
- Keep this matrix updated when adding or deprecating agents or skills.
