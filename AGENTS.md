# Reglas para Agentes y Contribuciones

Este archivo define reglas obligatorias para todo el repositorio.

## Alcance

- Aplica a todo el contenido versionado en este repo.
- Aplica a commits, pull requests, issues y comentarios de revision.

## Politica de idioma

### Espanol obligatorio

Usar espanol en:

- `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `GOVERNANCE.md`, `AGENTS.md`
- `docs/**/*.md`
- `templates/**/*.md`
- `agents/**/README.md`
- `agents/**/examples/**/*.md`
- `skills/**/README.md`
- `skills/**/examples/**/*.md`
- Issues, PRs, comentarios y revisiones en GitHub
- Mensajes de commit

### Ingles obligatorio (excepcion)

Solo estos archivos deben mantenerse en ingles por interoperabilidad:

- `agents/*/agent.md`
- `skills/*/skill.md`

## Regla para mensajes de commit

- Se mantiene el formato Conventional Commits (`feat:`, `fix:`, `docs:`, `ci:`, etc.).
- La descripcion del commit debe estar en espanol.

Ejemplos validos:

- `feat: agrega matriz de agentes y skills`
- `docs: actualiza politica de idioma`

## Regla para PRs e issues

- Titulos y descripciones en espanol.
- Si se incluye texto en ingles por interoperabilidad, agregar contexto corto en espanol.

## Cumplimiento

- Cualquier PR que no cumpla esta politica debe corregirse antes de merge.
- Excepciones adicionales solo con acuerdo explicito de maintainers.
