# Guia de releases

Esta guia define el proceso estandar para publicar nuevas versiones.

## Objetivo

- Mantener trazabilidad entre cambios, tags y notas de release.
- Asegurar consistencia en versionado (`SemVer`) y comunicacion a la comunidad.

## Convenciones

- Versionado: `MAJOR.MINOR.PATCH`.
- Changelog: `CHANGELOG.md` en formato Keep a Changelog.
- Commits: Conventional Commits con descripcion en espanol.

## Flujo recomendado

1. Verificar que `main` este actualizado y estable.
2. Confirmar que los checks de CI esten en verde.
3. Actualizar `CHANGELOG.md`:
   - mover cambios relevantes desde `Unreleased` a la nueva version.
   - agregar fecha de release (`YYYY-MM-DD`).
4. Commit de release:
   - ejemplo: `docs: actualiza changelog para v0.2.0`.
5. Crear tag anotado:
   - `git tag -a vX.Y.Z -m "release: vX.Y.Z"`
6. Publicar rama y tags:
   - `git push origin main --tags`
7. Crear release en GitHub con resumen de cambios y enlaces.

## Criterios minimos antes de publicar

- Politica de idioma cumplida (`AGENTS.md`).
- Documentacion clave actualizada (`README.md`, `CHANGELOG.md`).
- No hay secretos ni datos sensibles en cambios nuevos.
- La version candidata es reproducible y trazable a commits en `main`.

## Plantilla corta de notas de release

```md
## Resumen
- Punto 1 de impacto para la comunidad.
- Punto 2 de impacto para contribuidores.

## Cambios destacados
- Added:
- Changed:
- Fixed:

## Compatibilidad
- Riesgos o breaking changes (si aplica).
```
