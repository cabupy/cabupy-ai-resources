# Changelog

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### Added

- Agente `angular-architect` para arquitectura Angular en entornos complejos.
- Agente `nodejs-backend-base` para desarrollo backend Node.js generalista.
- Agente `nodejs-architecture-expert` para decisiones arquitectonicas en Node.js.
- Agente `nodejs-security-expert` para seguridad de aplicaciones Node.js.
- Agente `nodejs-performance-expert` para optimizacion de rendimiento en Node.js.
- Agente `nodejs-database-expert` para capa de datos PostgreSQL/Redis en Node.js.
- Agente `linux-security-engineer` para hardening y operaciones seguras en Linux.
- Agente `postgres-dba-architect` para arquitectura y operacion avanzada de PostgreSQL.
- Agente `cybersec-ethical-hacker` para evaluacion de seguridad en alcance autorizado.
- Skill `maps-expert` para implementaciones de mapas web con foco en responsive y rendimiento.
- Skill `mobile-ux-ui` para UX/UI movil en aplicaciones hibridas o nativas.

### Changed

- `frontend-developer` ahora integra `maps-expert` y `mobile-ux-ui` en su set de skills.
- Se amplio la matriz de `docs/tooling-matrix.md` y el catalogo de `agents/README.md` y `skills/README.md` tras la curacion incremental.
- Se agrego validacion automatica de consistencia de catalogo (`Catalog Consistency`) para evitar desalineaciones entre agentes, skills y matriz.

## [0.1.0] - 2026-03-26

### Added

- Estructura base del repositorio para recursos de IA (`agents`, `skills`, `docs`, `templates`, `governance`, `.agents`, `.claude`).
- Catalogo inicial con 5 agentes base y 12 skills reutilizables, cada uno con ejemplos y documentacion asociada.
- Documentacion de contratos y matriz de relacion Agent-Skill (`docs/agent-skill-contract.md`, `docs/tooling-matrix.md`).
- Guia de evaluacion de calidad para agentes y skills (`docs/quality-evaluation.md`).
- Politica formal de idioma y colaboracion en `AGENTS.md`.
- Workflow de calidad documental (`Docs Quality`) con `markdownlint` y verificacion de enlaces.
- Workflow de validacion automatica de politica de idioma (`Language Policy`).
- Plantillas de issues y pull requests para contribuciones consistentes.

### Changed

- Normalizacion del contenido Markdown al espanol en archivos comunitarios.
- Actualizacion de `actions/checkout` a `v5` en workflows para compatibilidad con migracion de runtime de GitHub Actions.

### Security

- Lineamientos de seguridad y reporte responsable en `SECURITY.md`.

[Unreleased]: https://github.com/cabupy/cabupy-ai-resources/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/cabupy/cabupy-ai-resources/releases/tag/v0.1.0
