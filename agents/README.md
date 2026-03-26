# Agents

Catalogo de agentes reutilizables para flujos de ingenieria de software.

## Objetivo

Cada agente define una responsabilidad clara, con entradas/salidas observables, guardrails y criterios de calidad para facilitar su portabilidad entre herramientas.

## Catalogo inicial

- `code-review`: revision tecnica y de riesgo sobre cambios de codigo.
- `test-engineer`: diseno y mejora de pruebas con enfoque en regresiones.
- `refactor-architect`: refactor seguro por etapas con preservacion de comportamiento.
- `docs-maintainer`: documentacion operativa y tecnica accionable.
- `release-manager`: preparacion de release notes, versionado y checklist de entrega.

See `docs/tooling-matrix.md` for the current agent-to-skill mapping.

## Estructura por agente

```text
agents/<agent-id>/
├── README.md      # descripcion rapida, alcance y limites
├── agent.md       # instruccion principal portable
└── examples/      # ejemplos reproducibles
```

## Estandar minimo de calidad

- Explicita supuestos y riesgos.
- Evita acciones destructivas por defecto.
- Incluye pasos de verificacion.
- Define salida esperada con formato estable.
- Declara compatibilidad objetivo (`generic`, `codex`, `claude-code`, `gemini-cli`, `opencode`).

All agent specs must follow `docs/agent-skill-contract.md`.
