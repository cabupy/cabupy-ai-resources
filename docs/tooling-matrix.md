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
| `frontend-developer` | Implementar funcionalidades frontend con calidad visual y tecnica | `ui-ux-foundations`, `react-feature-development`, `angular-feature-development`, `tailwindcss-ui-engineering`, `maps-expert`, `mobile-ux-ui`, `test-case-design`, `coverage-gap-finder` |
| `angular-architect` | Disenar y evolucionar arquitectura Angular en entornos complejos | `angular-feature-development`, `ui-ux-foundations`, `test-case-design`, `coverage-gap-finder`, `risk-assessment` |
| `nodejs-backend-base` | Construir backend Node.js para casos generales de negocio | `change-summarizer`, `test-case-design`, `coverage-gap-finder`, `security-checklist` |
| `nodejs-architecture-expert` | Definir arquitectura backend mantenible en Node.js | `risk-assessment`, `change-summarizer`, `docs-structure-planner`, `clarity-rewriter` |
| `nodejs-security-expert` | Endurecer seguridad de aplicaciones Node.js | `security-checklist`, `risk-assessment`, `review-comment-writer`, `change-summarizer` |
| `nodejs-performance-expert` | Optimizar latencia, throughput y uso de recursos en Node.js | `risk-assessment`, `coverage-gap-finder`, `test-prioritization`, `change-summarizer` |
| `nodejs-database-expert` | Mejorar capa de datos PostgreSQL/Redis en sistemas Node.js | `risk-assessment`, `regression-planner`, `change-summarizer`, `test-case-design` |
| `linux-security-engineer` | Operar y endurecer infraestructura Linux con seguridad | `security-checklist`, `risk-assessment`, `release-checklist-runner`, `change-summarizer` |
| `cybersec-ethical-hacker` | Evaluar seguridad ofensiva/defensiva en alcance autorizado | `security-checklist`, `risk-assessment`, `review-comment-writer`, `change-summarizer` |
| `postgres-dba-architect` | Disenar y operar plataformas PostgreSQL seguras y eficientes | `risk-assessment`, `regression-planner`, `release-checklist-runner`, `change-summarizer` |

## Notas

- Las skills son cross-agent por diseno; no duplicar capacidades con
  diferentes nombres.
- Si una nueva skill se superpone con otra existente, extender la skill
  existente antes de crear una nueva.
- Mantener esta matriz actualizada al agregar o deprecar agents o skills.
