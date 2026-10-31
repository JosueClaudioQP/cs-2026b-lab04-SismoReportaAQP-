# Bitácora IA del Lab08

Fecha: 31/10/2026. Herramienta: asistente de IA de esta conversación. Son siete puntos de análisis de una misma sesión de elaboración y verificación, sintetizados; no se presentan como siete conversaciones independientes ni como decisiones ya aprobadas por los estudiantes. Los nombres de los autores se incluyen por solicitud del usuario.

## IA-01: Resolver la guía y determinar el caso correcto
- Análisis / propuesta: Los recursos AgroConecta son un ejemplo docente, no el caso del grupo.
- Verificación: Se inspeccionó el proyecto local y el usuario confirmó la URL de SismoReporta.
- Resolución: Adaptar a caso 8; no copiar cifras de pagos de AgroConecta.

## IA-02: Revisar antecedentes y faltantes
- Análisis / propuesta: Falso positivo inicial: la copia local parecía no tener ADR-005 ni workspace.dsl.
- Verificación: La copia remota 529b7b6 sí contiene ambos y los patrones del Lab07.
- Resolución: Refutar la ausencia; conservar ADR-005 SMS y C4 previo como fuentes.

## IA-03: Definir prioridades medibles
- Análisis / propuesta: Extensibilidad podría calificarse H,H por incorporar canales nuevos.
- Verificación: Lab07 ya tiene fábrica por registro y un test de canal nuevo.
- Resolución: Corregir QA08-05 a M,L; priorizar disponibilidad e ingesta.

## IA-04: Evaluar si basta la tasa media de llegada
- Análisis / propuesta: 20 000/h equivale a 5,56/s; evaluar solo ese promedio oculta la reconexión.
- Verificación: Simulación con la misma cantidad y ráfaga: síncrono p95 719 487 ms frente a 1528 ms uniforme.
- Resolución: Rechazar el promedio como única prueba de capacidad.

## IA-05: Auditar ACK temprano y persistencia
- Análisis / propuesta: Un ACK rápido podría confundirse con procesamiento terminado.
- Verificación: El modelo extremo responde en 72,87 ms p95, pero drena 898,28 s después de la última llegada.
- Resolución: Separar ACEPTADO, PROCESADO y EVIDENCIA_PENDIENTE; incluir QA08-06.

## IA-06: Verificar resiliencia y alcance
- Análisis / propuesta: UUID y reintentos no prueban por sí solos durabilidad ni exactly-once.
- Verificación: Experimento SQLite: 20 000 registros, 2858 replays y 0 duplicados; reabrir no prueba destrucción de disco.
- Resolución: Usar lenguaje acotado al experimento y registrar riesgos R1/R7.

## IA-07: Comprobar arquitectura y entrega
- Análisis / propuesta: Un workflow escrito no equivale a Actions en verde ni a evaluación por pares.
- Verificación: Import-linter y pytest ejecutados localmente; import ilícito falla en rama aislada. No hubo ejecución remota.
- Resolución: Adjuntar logs y marcar evaluación cruzada, PR, tag y Aula Virtual como pendientes.

El falso positivo IA-02 fue corregido antes de redactar las decisiones. Los integrantes deben revisar los ADR propuestos y ratificar o cambiar estas resoluciones.
