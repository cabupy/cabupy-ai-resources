# Ejemplo: Refactor de capa de servicios

## Entrada

- Clase de servicio grande con logica de negocio y persistencia mezcladas.

## Salida esperada

- Plan en tres fases: extraer logica de dominio, aislar adaptadores y simplificar orquestacion.
- Checklist de validacion por fase.
- Condiciones de activacion de rollback para cada fase.
