# ADR-002: Estrategia de almacenamiento y sincronización offline

- **Estado:** Aceptado
- **Fecha:** 04/10/2026
- **Decisores:** Equipo de trabajo de SismoReporta AQP

## Contexto

SismoReporta AQP debe permitir que un ciudadano registre un reporte
incluso cuando la conectividad móvil sea inexistente o intermitente.

Este requisito está relacionado principalmente con:

- RF-01: Registro de reportes.
- RF-02: Registro de evidencia.
- RF-03: Registro de ubicación.
- RF-04: Almacenamiento y sincronización offline.

La decisión afecta principalmente a:

- QA-01: Disponibilidad.
- QA-03: Fiabilidad.
- QA-04: Usabilidad.
- R-03: Conectividad móvil intermitente.

Durante un escenario de emergencia, la aplicación no puede depender
exclusivamente de una conexión permanente con el servidor.

Además, los reintentos posteriores a una interrupción de red pueden
provocar duplicación de reportes si el cliente vuelve a enviar un
reporte que ya había sido recibido por el servidor.

## Alternativas consideradas

### Alternativa 1: Almacenamiento local SQLite + Sync Manager

Los reportes se almacenan localmente en SQLite cuando son creados.

Un componente denominado Sync Manager administra la sincronización
con el servidor cuando existe conectividad.

El mecanismo utiliza:

- Identificador UUID por reporte.
- Reintentos.
- Exponential backoff.
- Jitter.
- Estado local del reporte.

### Alternativa 2: Mantener los reportes únicamente en memoria

La aplicación mantendría temporalmente los reportes en memoria
hasta recuperar la conectividad.

Ventajas:

- Implementación sencilla.
- No requiere una base de datos local.

Desventajas:

- Los datos pueden perderse si la aplicación se cierra.
- Los datos pueden perderse si el sistema operativo termina
  el proceso.
- No es adecuado para una situación de emergencia.

### Alternativa 3: Almacenamiento local mediante archivos JSON

Cada reporte pendiente se almacenaría como un archivo local.

Ventajas:

- Implementación relativamente sencilla.
- Fácil inspección del contenido durante el desarrollo.

Desventajas:

- La gestión de estados y búsquedas es menos conveniente.
- El control de sincronización resulta más complejo.
- El control de duplicados y actualización de estados requiere
  lógica adicional.

## Decisión

Se selecciona:

**SQLite local + Sync Manager.**

Cada reporte creado por el ciudadano tendrá un UUID único y será
almacenado localmente cuando sea necesario.

El Sync Manager será responsable de identificar reportes pendientes
y enviarlos al backend cuando exista conectividad.

Los reintentos deberán considerar exponential backoff y jitter para
reducir el riesgo de que múltiples dispositivos realicen solicitudes
simultáneas después de recuperar la conexión.

La aplicación conservará información suficiente para conocer el estado
de sincronización de cada reporte.

El reporte deberá distinguir entre:

- `timestamp_dispositivo`: momento en que el ciudadano creó el reporte.
- `timestamp_servidor`: momento en que el backend recibió el reporte.

El UUID permitirá al servidor reconocer reintentos de un mismo reporte
y evitar duplicaciones.

## Consecuencias positivas

- El ciudadano puede registrar reportes sin conexión.
- Los reportes permanecen almacenados localmente mientras esperan
  sincronización.
- La estrategia es compatible con conectividad intermitente.
- El UUID permite implementar idempotencia.
- El uso de backoff y jitter reduce la posibilidad de una avalancha
  de solicitudes al recuperar la conectividad.
- La estrategia mejora la fiabilidad de la sincronización.

## Consecuencias negativas

- Se requiere implementar lógica adicional en la aplicación móvil.
- Se debe administrar el estado de cada reporte pendiente.
- El almacenamiento local consume espacio en el dispositivo.
- Si el dispositivo se pierde o sus datos son eliminados antes
  de sincronizarse, el sistema no puede recuperar automáticamente
  ese reporte.
- La sincronización debe probarse bajo diferentes escenarios
  de pérdida y recuperación de conectividad.

## Relación con otras decisiones

Esta decisión complementa:

- ADR-001: selección del Monolito Modular con Ingesta Asíncrona.
- ADR-003: cola persistente y procesamiento asíncrono.