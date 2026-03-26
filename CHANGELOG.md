# Changelog

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### Added

- Pendiente.

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
