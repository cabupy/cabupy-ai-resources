# Contrato de Agents y Skills

Este documento define el contrato minimo para todos los agents y skills
del repositorio.

## Contrato para agents

Cada agent debe incluir:

- `id`: identificador unico en kebab-case.
- `purpose`: un parrafo corto con el objetivo end-to-end.
- `inputs`: contexto requerido y opcional.
- `workflow`: pasos ordenados que sigue el agent.
- `outputs`: formato de salida estable.
- `guardrails`: limites y restricciones de seguridad.
- `quality_checks`: validaciones previas a la salida final.
- `failure_mode`: comportamiento cuando falta contexto o hay ambiguedad.
- `compatibility`: herramientas soportadas
  (`generic`, `codex`, `claude-code`, `gemini-cli`, `opencode`).

## Contrato para skills

Cada skill debe incluir:

- `id`: identificador unico en kebab-case.
- `purpose`: capacidad especifica en una o dos lineas.
- `inputs`: entradas minimas requeridas.
- `process`: pasos de ejecucion deterministas.
- `outputs`: formato de salida estricto.
- `guardrails`: restricciones explicitas de lo que puede y no puede hacer.
- `quality_checks`: controles de calidad de salida.
- `failure_mode`: comportamiento seguro ante falta de contexto.
- `compatibility`: herramientas objetivo.

## Estandar de frontmatter

Usar este frontmatter en `agent.md` y `skill.md`:

```yaml
id: example-id
version: 0.1.0
status: stable
owner: cabupy-ia-resources contributors
compatibility: [generic, codex, claude-code, gemini-cli, opencode]
last_reviewed: 2026-03-25
```

## Reglas de nombres

- Los IDs de agents deben orientarse a rol (`code-review`, `release-manager`).
- Los IDs de skills deben orientarse a capacidad
  (`risk-assessment`, `clarity-rewriter`).
- Mantener nombres cortos y explicitos; evitar etiquetas genericas como
  `helper` o `utils`.
