# ADR-001: Selección del estilo arquitectónico

- **Estado:** Aceptado
- **Fecha:** 04/10/2026
- **Decisores:** Equipo de trabajo de SismoReporta AQP

## Contexto

SismoReporta AQP debe permitir que los ciudadanos registren reportes
de daños ocasionados por un sismo, incluyendo información de ubicación
y evidencia fotográfica.

El sistema debe continuar funcionando ante situaciones de conectividad
móvil intermitente y soportar un escenario de hasta 20 000 reportes
durante la primera hora posterior a un sismo.

Los principales drivers de calidad considerados son:

- QA-01: Disponibilidad.
- QA-02: Rendimiento.
- QA-03: Fiabilidad.
- QA-04: Usabilidad.

Entre las principales restricciones del proyecto se encuentran:

- R-01: El MVP debe desarrollarse en un máximo de 1 mes.
- R-02: El equipo está conformado por un máximo de 3 integrantes.
- R-03: Debe considerarse conectividad móvil intermitente.
- R-04: La solución debe poder documentarse y versionarse utilizando
  las herramientas del laboratorio.

Los requisitos funcionales relacionados con la decisión incluyen:

- RF-01: Registro de reportes.
- RF-02: Registro de evidencia fotográfica.
- RF-03: Registro de ubicación.
- RF-04: Almacenamiento y sincronización de reportes offline.
- RF-05: Consulta de reportes por operadores.
- RF-06: Clasificación de reportes.
- RF-07: Actualización del estado de los reportes.

En la matriz de decisión de E2 se evaluaron tres alternativas:

1. Monolito Modular con Ingesta Asíncrona.
2. Arquitectura Orientada a Eventos / Serverless.
3. Cliente-Servidor N-Capas Síncrono.

La evaluación consideró los drivers de calidad y las restricciones
del proyecto.

## Alternativas consideradas

### Alternativa 1: Monolito Modular con Ingesta Asíncrona

El backend se organiza en módulos dentro de un único sistema,
incorporando una cola persistente y procesamiento asíncrono.

Ventajas:

- Permite desacoplar la recepción del reporte de su procesamiento.
- Reduce la presión inmediata sobre la base de datos.
- Es posible mantener un único artefacto desplegable.
- Es compatible con el plazo y tamaño del equipo.

Desventajas:

- Introduce complejidad adicional por la cola y el procesamiento
  asíncrono.
- Requiere controlar duplicados e idempotencia.
- La cola puede convertirse en un punto de fallo si no tiene
  persistencia adecuada.

### Alternativa 2: Arquitectura Orientada a Eventos / Serverless

La recepción y procesamiento se dividirían mediante servicios
gestionados en la nube y funciones serverless.

Ventajas:

- Permite escalar horizontalmente los componentes.
- Facilita absorber variaciones importantes de carga.

Desventajas:

- Introduce dependencia de infraestructura y servicios cloud.
- Aumenta la complejidad de configuración y pruebas.
- Presenta mayor riesgo para un equipo de 3 personas con un MVP
  de 1 mes.
- Puede introducir dependencia de un proveedor específico.

### Alternativa 3: Cliente-Servidor N-Capas Síncrono

La aplicación móvil se comunica con un servidor que procesa
las solicitudes de manera síncrona utilizando una arquitectura
en capas.

Ventajas:

- Es conceptualmente sencilla.
- Presenta menor complejidad inicial de implementación.
- Puede desarrollarse rápidamente.

Desventajas:

- El procesamiento síncrono puede ser vulnerable ante ráfagas
  de solicitudes.
- La transferencia de fotografías puede incrementar el tiempo
  de procesamiento.
- La recuperación masiva de reportes offline puede generar
  presión sobre el servidor y la base de datos.

## Decisión

Se selecciona la:

**Arquitectura Monolito Modular con Ingesta Asíncrona.**

La arquitectura tendrá un único backend organizado en módulos,
con una API REST como punto de entrada, un módulo de Ingesta,
un módulo de Operaciones, una cola persistente y un Worker interno
para procesamiento asíncrono.

La aplicación móvil utilizará almacenamiento local para conservar
los reportes pendientes de sincronización.

La decisión busca equilibrar:

- Disponibilidad (QA-01).
- Rendimiento ante picos de demanda (QA-02).
- Fiabilidad ante conectividad intermitente (QA-03).
- Usabilidad (QA-04).
- Plazo de desarrollo (R-01).
- Tamaño del equipo (R-02).
- Conectividad intermitente (R-03).

La selección corresponde a la alternativa evaluada favorablemente
en la matriz de decisión de E2.

## Consecuencias positivas

- La recepción de reportes puede desacoplarse de su procesamiento.
- La cola permite absorber temporalmente variaciones en la carga.
- El procesamiento asíncrono reduce la dependencia inmediata de
  la disponibilidad de la base de datos.
- El sistema mantiene una estructura relativamente sencilla
  de desplegar y documentar.
- Los módulos permiten separar las responsabilidades de Ingesta
  y Operaciones.
- La solución es compatible con el plazo de desarrollo del MVP.

## Consecuencias negativas

- Se introduce complejidad adicional respecto a una arquitectura
  completamente síncrona.
- Se debe controlar la persistencia de la cola.
- Se debe implementar un mecanismo de idempotencia para evitar
  reportes duplicados.
- Se debe monitorear el crecimiento de la cola.
- La base de datos continúa siendo un posible punto único de fallo
  durante el MVP.
- El sistema requerirá pruebas adicionales para validar los
  escenarios de sincronización y procesamiento asíncrono.

## Relación con decisiones posteriores

Esta decisión conduce a las decisiones documentadas en:

- ADR-002: estrategia de almacenamiento y sincronización offline.
- ADR-003: cola persistente y procesamiento asíncrono.