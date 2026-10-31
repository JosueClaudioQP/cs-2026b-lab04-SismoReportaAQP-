# ADR-006: Ingesta durable y evidencia diferida

- Estado: Propuesto con evidencia local; revisión de los integrantes pendiente.
- Fecha: 2026-10-31.
- Autores del informe: Josue Claudio Quispe Paucar y Diego Alejandro Carbajal Gonzales.
- Escenarios: QA08-01 y QA08-06.

## Contexto
La carga media 20 000/3600 = 5,56 req/s oculta ráfagas de reconexión. El modelo usa 4 servidores de ingesta y tiempos medios hipotéticos de 550 ms síncronos frente a 35 ms de aceptación durable.

## Alternativas consideradas
Síncrono; duplicar workers; ingesta asíncrona con inbox SQL; microservicios/Kafka.

## Decisión
Usaremos una tabla inbox de PostgreSQL con UUID único y commit antes de responder 202. El worker interno procesa metadata. Las fotos se subirán en un flujo separado asociado al UUID; el reporte indica evidencia pendiente hasta completarse. Se mantiene el monolito y el servidor del ADR-004. Esta decisión reemplaza Redis/AOF como frontera de aceptación de ADR-003/004 y modifica la precondición de subida de fotos del ADR-004; el modelo Lab06 se conserva como histórico.

## Evidencia
Reconexión: p95 2 323 422 ms síncrono, 1 019 274 ms con 8 workers y 72,87 ms durable. Drenaje modelado 898,28 s después de la última llegada, dentro de 1200 s. Servicio medio 60 ms eleva el p95 a 2786 ms: se exige medir el disco real antes de aceptar el despliegue.

## Consecuencias
Menor latencia de aceptación a cambio de consistencia eventual y reportes temporalmente sin foto. Inbox y consultas comparten disco: no hay escalabilidad ilimitada. Reserva de disco, métricas de edad de pendiente y control de carga son obligatorios antes del despliegue.
