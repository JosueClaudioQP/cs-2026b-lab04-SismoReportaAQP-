# Iteración 2 de ADD

Escenarios: QA08-02 y QA08-03.

Elemento refinado: Sincronización móvil, persistencia y outbox de avisos.

## Siete pasos
1. Revisar ADR-002 (offline), ADR-003 (ACK persistido) y ADR-005 (SMS no revierte asignación).
2. Objetivo: 0 pérdidas y duplicados tras replay; 0 asignaciones revertidas ante timeout SMS.
3. Elementos refinados: estado local pendiente, recepción idempotente y operaciones de brigada.
4. Conceptos: memoria (rechazada ante reinicio); Redis AOF (añade frontera entre dos almacenes); inbox/outbox SQL (adoptada por atomicidad); no introducir entrega exactly-once de red.
5. Instanciar: cliente guarda antes de enviar; servidor confirma solo después del commit; repetición idéntica devuelve ACK; UUID con contenido distinto se rechaza. Asignación y aviso pendiente se escriben juntos.
6. Documentar ADR-007, estados PENDIENTE/ACEPTADO/EVIDENCIA_PENDIENTE/PROCESADO y relaciones C4.
7. Evaluar: prototipo SQLite de 20 000 registros; reapertura del cliente y servidor; 2 858 ACK perdidos y reenviados. Test de SMS caído conserva asignación y pendiente. No demuestra resistencia a pérdida física del disco ni integración móvil real.

## Decisión
SQLite local, UUID estable, inbox durable y asignación + outbox SMS en una misma transacción.

## Evidencia
Ver ../evidencia/resultados.json, ../pytest-lab08.txt y ../lint-lab08.txt.

## Límite
La simulación es evidencia del modelo, no certificación de capacidad del despliegue real.
