# Historia de usuario crítica – SismoReporta AQP (Lab 05)

**HU-08:** Como ciudadano, quiero enviar un reporte de daños aunque no tenga señal y que se sincronice solo cuando vuelva la conexión, para no perder mi reporte en la emergencia.

## Criterios de aceptación
- **Dado** que no hay conectividad, **cuando** registro un reporte, **entonces** queda guardado localmente en estado BORRADOR/ENCOLADO con su UUID y `timestamp_dispositivo`.
- **Dado** un reporte pendiente y que la conexión se restablece, **cuando** el Sync Manager lo envía y el servidor lo acepta (HTTP 202 tras persistir en la cola), **entonces** el reporte queda RECIBIDO y no se duplica aunque se reintente.
- **Dado** un envío fallido por red, **cuando** se agota el intento, **entonces** el reporte sigue ENCOLADO y se reintenta con backoff exponencial + jitter.

Trazabilidad: RF-01 a RF-04 (Lab 04), ADR-001, ADR-002, ADR-003.
