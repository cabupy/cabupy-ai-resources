# Hub de Recursos para Agentes de IA

Repositorio colaborativo de recursos para agentes de IA orientados a desarrollo de software.

Objetivo: ofrecer un set curado, versionado y reutilizable de `agents`, `skills`, plantillas y guias para herramientas como Codex, Claude Code, Gemini CLI, OpenCode y similares.

## Principios del proyecto

- Interoperabilidad primero: los recursos deben poder adaptarse entre herramientas.
- Calidad sobre cantidad: preferimos pocos recursos, bien documentados y probados.
- Transparencia: cada aporte explica el problema que resuelve y sus limites.
- Seguridad por defecto: no se aceptan secretos, credenciales ni material sensible.
- Colaboracion abierta: decisiones y cambios relevantes se documentan en PRs.

## Estado (Marzo 2026)

El proyecto se encuentra en fase de consolidacion temprana. Ya cuenta con catalogo base de agentes/skills, politicas de colaboracion y validaciones automaticas para calidad documental y consistencia de catalogo.

## Estructura del repositorio

```text
.
├── .agents/                      # Configs o definiciones para agentes
├── .claude/                      # Recursos especificos para Claude Code
├── agents/                       # Agentes reutilizables por dominio
├── skills/                       # Skills modulares por capacidad
├── templates/                    # Plantillas de prompts, README y checklists
├── docs/                         # Documentacion tecnica y guias
├── governance/                   # Modelo de toma de decisiones
├── .github/
│   ├── ISSUE_TEMPLATE/           # Templates de issues
│   └── pull_request_template.md  # Template de PR
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── SECURITY.md
└── README.md
```

## Convenciones y estandares

- Versionado: Semantic Versioning (`MAJOR.MINOR.PATCH`).
- Commits recomendados: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.).
- Changelog: formato Keep a Changelog.
- Documentacion: Markdown claro, ejemplos minimos reproducibles.
- Idioma: seguir politica de `AGENTS.md`.

## Como contribuir

1. Revisa `CONTRIBUTING.md`.
2. Abre un issue con contexto claro (problema, alcance, criterio de exito).
3. Crea un PR pequeno, enfocado y con descripcion verificable.
4. Sigue el template de PR y checklist de seguridad/documentacion.

## Tipos de recursos esperados

- Agentes especializados (code review, testing, refactor, docs, release).
- Skills de flujo (debugging, planning, migration, observability, security).
- Plantillas de prompts para tareas frecuentes.
- Guias de integracion por herramienta.
- Buenas practicas de evaluacion para prompts/agentes.

## Catalogo base

- Agentes base: `agents/`
- Skills reutilizables: `skills/`
- Contrato Agent/Skill: `docs/agent-skill-contract.md`
- Matriz Agent/Skill: `docs/tooling-matrix.md`
- Plantillas de contribucion: `templates/`

Estado actual del catalogo:

- 15 agentes en formato estandar.
- 18 skills en formato estandar.

## Calidad automatizada

- `Docs Quality`: lint de Markdown y validacion de enlaces.
- `Language Policy`: cumplimiento de politica de idioma y mensajes de commit.
- `Catalog Consistency`: consistencia entre catalogos, matriz y contratos.

## Seguridad y uso responsable

- Nunca subir tokens, secretos, credenciales o dumps de datos privados.
- En recursos que toquen codigo productivo: explicitar riesgos y limites.
- En prompts para acciones destructivas: incluir advertencias y guardrails.

Consulta `SECURITY.md` para reporte responsable de vulnerabilidades.

## Roadmap inicial

- [x] Definir 5 agentes base cross-tool.
- [x] Definir 10+ skills reutilizables con ejemplos.
- [x] Publicar guia de evaluacion de calidad de prompts/agentes.
- [x] Agregar templates de contribucion por tipo de recurso.
- [x] Automatizar validaciones basicas (lint markdown + enlaces).
- [x] Validar consistencia automatica entre catalogos y matriz Agent-Skill.

## Licencia

Este proyecto se distribuye bajo licencia Apache-2.0. Consulta `LICENSE` y `NOTICE`.

## Releases

- Changelog oficial: `CHANGELOG.md`.
- Proceso de publicacion: `RELEASE.md`.

## Comunidad

Si te interesa co-crear este repositorio, abre un issue en modo propuesta (`proposal`) para discutir alcance y priorizacion.
