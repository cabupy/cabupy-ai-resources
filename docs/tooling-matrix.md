# Matriz de Agents y Skills

Esta matriz define que skills reutilizables usa cada agent base.

## Agents base

| Agent | Objetivo principal | Skills |
|---|---|---|
| `code-review` | Revisar calidad, riesgo y seguridad del codigo | `risk-assessment`, `security-checklist`, `review-comment-writer`, `change-summarizer` |
| `test-engineer` | Mejorar estrategia de pruebas y cobertura de regresion | `test-case-design`, `regression-planner`, `coverage-gap-finder`, `test-prioritization` |
| `docs-maintainer` | Mantener docs utiles, precisas y accionables | `docs-structure-planner`, `clarity-rewriter`, `change-summarizer` |
| `refactor-architect` | Planificar refactors seguros por etapas | `risk-assessment`, `change-summarizer`, `regression-planner` |
| `release-manager` | Preparar releases con notas y checks claros | `changelog-drafter`, `release-checklist-runner`, `risk-assessment`, `change-summarizer` |
| `frontend-developer` | Implementar funcionalidades frontend con calidad visual y tecnica | `ui-ux-foundations`, `react-feature-development`, `angular-feature-development`, `tailwindcss-ui-engineering`, `test-case-design`, `coverage-gap-finder` |
| `angular-architect` | Disenar y evolucionar arquitectura Angular en entornos complejos | `angular-feature-development`, `ui-ux-foundations`, `test-case-design`, `coverage-gap-finder`, `risk-assessment` |
| `nodejs-backend-base` | Construir backend Node.js para casos generales de negocio | `change-summarizer`, `test-case-design`, `coverage-gap-finder`, `security-checklist` |
| `nodejs-architecture-expert` | Definir arquitectura backend mantenible en Node.js | `risk-assessment`, `change-summarizer`, `docs-structure-planner`, `clarity-rewriter` |
| `nodejs-security-expert` | Endurecer seguridad de aplicaciones Node.js | `security-checklist`, `risk-assessment`, `review-comment-writer`, `change-summarizer` |

## Notas

- Las skills son cross-agent por diseno; no duplicar capacidades con
  diferentes nombres.
- Si una nueva skill se superpone con otra existente, extender la skill
  existente antes de crear una nueva.
- Mantener esta matriz actualizada al agregar o deprecar agents o skills.
