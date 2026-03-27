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
- `frontend-developer`: implementacion frontend estandar con foco en UX y accesibilidad.
- `angular-architect`: arquitectura Angular para proyectos de alta complejidad.
- `nodejs-backend-base`: desarrollo backend Node.js para casos generales.
- `nodejs-architecture-expert`: diseno arquitectonico backend en Node.js/TypeScript.
- `nodejs-security-expert`: seguridad aplicada a APIs y autenticacion en Node.js.
- `nodejs-performance-expert`: optimizacion de rendimiento y observabilidad en Node.js.
- `nodejs-database-expert`: capa de datos PostgreSQL/Redis para sistemas Node.js.
- `linux-security-engineer`: hardening y operaciones seguras en Linux.
- `postgres-dba-architect`: arquitectura y operacion avanzada de PostgreSQL.
- `cybersec-ethical-hacker`: evaluacion de seguridad ofensiva/defensiva autorizada.

Ver `docs/tooling-matrix.md` para la matriz actual de agentes y skills.

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

Todas las especificaciones de agentes deben cumplir `docs/agent-skill-contract.md`.
