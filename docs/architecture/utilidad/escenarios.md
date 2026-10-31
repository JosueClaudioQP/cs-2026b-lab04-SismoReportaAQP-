# Escenarios del Lab08

IDs QA08 evitan la numeración inconsistente entre drivers.md y ADR-001 heredados. Las medidas son objetivos de diseño, no SLO demostrados en producción.

## QA08-01 - Rendimiento / Aceptación (H,H)
- Fuente: Ciudadanos.
- Estímulo: 20 000 reportes; 10 000 en los primeros 600 s; reconexión extrema de 20 000 en 300 s.
- Entorno: Red recuperada y servidor disponible.
- Artefacto: API de ingesta.
- Respuesta: Validar y persistir metadata antes de responder 202.
- Medida: p95 de aceptación ≤ 2 000 ms; 20 000 UUID aceptados.
- Trazabilidad: QA-01 / ADR-001.

## QA08-02 - Disponibilidad / Persistencia offline (H,H)
- Fuente: Ciudadano / red móvil.
- Estímulo: Sin conexión al registrar; reinicio de app y ACK perdido después de aceptación.
- Entorno: Conectividad intermitente; disco intacto.
- Artefacto: SQLite local + inbox del servidor.
- Respuesta: Retener pendiente hasta ACK; replay idempotente por UUID y contenido.
- Medida: 0 reportes perdidos, 0 duplicados y 0 pendientes tras recuperar red.
- Trazabilidad: QA-02 / ADR-002.

## QA08-03 - Disponibilidad / Degradación de SMS (H,M)
- Fuente: Servicio externo SMS.
- Estímulo: Timeout al avisar una asignación.
- Entorno: Proveedor no disponible, base local disponible.
- Artefacto: Operaciones y outbox SMS.
- Respuesta: Confirmar asignación y conservar aviso para reintento.
- Medida: 1 asignación persistida; 1 aviso pendiente; 0 asignaciones revertidas.
- Trazabilidad: RF-07 / ADR-005.

## QA08-04 - Seguridad / Autorización de operaciones (H,M)
- Fuente: Ciudadano, brigadista, anónimo u operador de lectura.
- Estímulo: Intento de asignar brigada sin permiso.
- Entorno: Sesión cuyo rol ya fue autenticado por la frontera HTTP.
- Artefacto: Servicio de operaciones.
- Respuesta: Denegar operación antes de modificar datos.
- Medida: 0 escrituras no autorizadas en las 4 clases de prueba; coordinador permitido.
- Trazabilidad: RF-07 / propuesta Lab08.

## QA08-05 - Modificabilidad / Nuevo canal (M,L)
- Fuente: Desarrollador.
- Estímulo: Agregar un canal de envío de reportes.
- Entorno: Monolito con Strategy + Adapter del Lab07.
- Artefacto: Fábrica de canales y servicio de reportes.
- Respuesta: Registrar un adaptador que respete CanalEnvio.
- Medida: 1 canal nuevo probado; 0 cambios en el servicio central.
- Trazabilidad: Lab07 / test_open_closed_nuevo_canal_por_registro.

## QA08-06 - Rendimiento / Drenaje de pendientes (H,H)
- Fuente: Dispositivos que recuperan señal.
- Estímulo: 20 000 reportes en 300 s.
- Entorno: Ingesta disponible y 2 consumidores internos.
- Artefacto: Worker del monolito + inbox.
- Respuesta: Procesar metadata sin bloquear la aceptación.
- Medida: Cola completamente drenada ≤ 1 200 s después de la última llegada.
- Trazabilidad: QA-01 / ADR-003.

Corrección de prioridad: QA08-05 se reduce de H,H a M,L: el Lab07 ya incluye fábrica por registro y una prueba del canal nuevo. Disponibilidad e ingesta tienen prioridad sobre extensibilidad adicional.
