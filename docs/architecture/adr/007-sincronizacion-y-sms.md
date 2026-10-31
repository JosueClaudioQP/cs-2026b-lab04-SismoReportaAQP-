# ADR-007: Sincronización persistente y outbox SMS

- Estado: Propuesto con evidencia local; revisión de los integrantes pendiente.
- Fecha: 2026-10-31.
- Autores del informe: Josue Claudio Quispe Paucar y Diego Alejandro Carbajal Gonzales.
- Escenarios: QA08-02 y QA08-03.

## Contexto
El cliente puede perder el ACK después de que el servidor confirme el commit. ADR-005 exige que una falla de SMS no revierta una asignación.

## Alternativas consideradas
Memoria; cola independiente; inbox/outbox transaccional. No se adopta exactly-once de transporte.

## Decisión
Usaremos SQLite local persistente y UUID estable por reporte; se conservará el pendiente hasta recibir ACK durable. Repetición idéntica es idempotente; UUID repetido con otro contenido es conflicto. En servidor, asignación y outbox SMS se confirman en una transacción; el despachador reintenta sin revertir la asignación. En producción se requiere lease del worker y clave de idempotencia del proveedor para reducir avisos duplicados.

## Evidencia
20 000 registros persistidos; 22 858 intentos; 2858 ACK perdidos; 0 pérdidas y 0 duplicados después de reabrir SQLite. La prueba de SMS caído preserva la asignación y un aviso pendiente.

## Consecuencias
Se obtiene idempotencia del efecto en el modelo secuencial, no entrega de red exactamente una vez. Mayor complejidad de estados y limpieza; corrupción o eliminación del disco no está cubierta; SMS puede duplicarse si se pierde su ACK. No se envían SMS reales.
