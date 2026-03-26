# Guia de evaluacion de calidad

Esta guia define como evaluar la calidad de agents y skills antes del merge.

## Objetivos de evaluacion

- Asegurar que los aportes sean utiles en flujos reales de ingenieria.
- Mantener salidas confiables, seguras y faciles de validar.
- Preservar interoperabilidad entre herramientas soportadas.

## Modelo de puntuacion

Usar escala de 1 a 5 por categoria.

- `1`: faltante o inutilizable.
- `3`: aceptable pero incompleto.
- `5`: solido y listo para produccion.

## Rubrica para agents

Evaluar cada criterio:

- Claridad del proposito: el rol end-to-end es explicito.
- Calidad de inputs: entradas requeridas y opcionales son claras.
- Calidad de workflow: pasos deterministas y practicos.
- Calidad de salida: formato estable y accionable.
- Seguridad: guardrails explicitos y suficientes.
- Modo de falla: respuesta segura si falta contexto.
- Reusabilidad: posibilidad de uso en distintos ecosistemas.

## Rubrica para skills

Evaluar cada criterio:

- Foco de capacidad: resuelve un problema claro.
- Calidad de contrato: inputs/proceso/outputs precisos.
- Evidencia: evita afirmaciones sin respaldo.
- Accionabilidad: salida utilizable por agents.
- Guardrails y limites: restricciones explicitas.
- Calidad de ejemplo: al menos un ejemplo reproducible.

## Umbrales de aceptacion

- Umbral recomendado de merge: promedio >= 4.0.
- Cualquier criterio de seguridad por debajo de 4 requiere revision.
- Falta de ejemplos bloquea merge en agents/skills nuevos.

## Checklist de revision

- Cumple el contrato de `docs/agent-skill-contract.md`.
- Cumple convenciones de nombres y estructura del repositorio.
- `docs/tooling-matrix.md` actualizado si cambian dependencias.
- No incluye secretos, credenciales o datos privados.

## Mejora continua

- Re-evaluar recursos estables cada 90 dias.
- Marcar recursos desactualizados como `deprecated` hasta revisarlos.
- Registrar fallas recurrentes de revision y ajustar templates.
