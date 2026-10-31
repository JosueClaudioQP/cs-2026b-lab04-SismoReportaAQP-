# Iteración 1 de ADD

Escenarios: QA08-01 y QA08-06.

Elemento refinado: API de ingesta y procesamiento interno.

## Siete pasos
1. Revisar entradas: drivers, ADR-001/003/004, Lab07 y carga de crecimiento. No hay mediciones reales de servicio; se declaran supuestos.
2. Objetivo: p95 de aceptación ≤ 2 s y drenaje ≤ 20 min tras la ráfaga extrema.
3. Elemento refinado: API, inbox y worker del mismo monolito.
4. Conceptos: síncrono (simple, bloquea); 8 workers (más recursos, no resuelve carga extrema); ingesta durable (consistencia eventual); microservicios/Kafka (rechazados por plazo y complejidad sin necesidad demostrada).
5. Instanciar: 4 servidores lógicos de ingesta, 2 consumidores internos; UUID único y transacción en PostgreSQL. Fotos diferidas, sin binarios en mensajes.
6. Registrar vistas y ADR-006; C4 muestra PostgreSQL inbox y elimina Redis como frontera de aceptación.
7. Evaluar: resultados.json compara tres perfiles y 30 semillas de llegadas. El modelo cumple; la latencia real del VPS continúa sin medir.

## Decisión
Separar el ACK durable del procesamiento pesado; metadata primero, fotos después.

## Evidencia
Ver ../evidencia/resultados.json, ../pytest-lab08.txt y ../lint-lab08.txt.

## Límite
La simulación es evidencia del modelo, no certificación de capacidad del despliegue real.
