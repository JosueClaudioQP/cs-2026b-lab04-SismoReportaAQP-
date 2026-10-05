# ADR-003: Cola persistente y procesamiento asíncrono

- **Estado:** Aceptado
- **Fecha:** 04/10/2026
- **Decisores:** Equipo de trabajo de SismoReporta AQP

## Contexto

SismoReporta AQP debe soportar periodos de alta demanda posteriores
a un sismo.

El escenario definido considera hasta 20 000 reportes durante la
primera hora posterior al evento.

La arquitectura seleccionada en ADR-001 utiliza ingesta asíncrona
para desacoplar la recepción de reportes del procesamiento posterior.

La decisión está relacionada principalmente con:

- QA-01: Disponibilidad.
- QA-02: Rendimiento.
- QA-03: Fiabilidad.
- RF-01: Registro de reportes.
- RF-04: Sincronización offline.

También debe respetar:

- R-01: MVP de 1 mes.
- R-02: Equipo máximo de 3 integrantes.
- R-04: Solución documentable y versionable con las herramientas
  del laboratorio.

La revisión realizada durante E3 identificó que transportar fotografías
binarias pesadas directamente dentro de la cola podría incrementar
innecesariamente la carga del mecanismo de mensajería.

También se identificó que una cola únicamente en memoria podría perder
mensajes si el proceso se reinicia antes de completar el procesamiento.

## Alternativas consideradas

### Alternativa 1: Cola persistente + Worker interno

La API recibe el reporte y publica la información necesaria en una
cola persistente.

Una vez confirmada la escritura en la cola, la API puede responder
al cliente con `HTTP 202 Accepted`.

Un Worker interno del mismo monolito consume los mensajes y realiza
el procesamiento posterior.

Las fotografías no se transportan como archivos binarios pesados
dentro de la cola; se mantiene una referencia al recurso almacenado.

### Alternativa 2: Procesamiento completamente síncrono

La API recibe el reporte y realiza inmediatamente todas las
operaciones necesarias antes de responder.

Ventajas:

- Menor complejidad conceptual.
- No requiere una cola ni un Worker.

Desventajas:

- El tiempo de respuesta depende del procesamiento completo.
- Las ráfagas de solicitudes pueden generar presión sobre el servidor.
- La transferencia y procesamiento de fotografías pueden incrementar
  la duración de las solicitudes.

### Alternativa 3: Microservicio independiente de procesamiento

La API publicaría los reportes en una cola y un servicio independiente
sería responsable de procesarlos.

Ventajas:

- Permite escalar el procesamiento independientemente.
- Existe un mayor desacoplamiento entre componentes.

Desventajas:

- Introduce infraestructura adicional.
- Aumenta la complejidad de despliegue.
- No resulta conveniente para un equipo de 3 personas con un MVP
  de 1 mes.

## Decisión

Se selecciona:

**Cola persistente + Worker interno dentro del Monolito Modular.**

El flujo principal será:

1. La aplicación móvil envía un reporte mediante HTTPS.
2. La API recibe la solicitud.
3. El Módulo de Ingesta valida los datos y el UUID.
4. El reporte se publica en una cola persistente.
5. Después de confirmar la escritura en la cola, la API responde
   `HTTP 202 Accepted`.
6. El Worker interno consume los mensajes.
7. El Worker persiste la información del reporte en la base de datos.
8. La evidencia fotográfica se almacena o asocia mediante una referencia
   independiente.

La cola no tendrá como objetivo transportar archivos fotográficos
binarios pesados.

El Worker se mantendrá dentro del mismo artefacto del monolito para
reducir la complejidad operacional del MVP.

## Consecuencias positivas

- La recepción de solicitudes queda desacoplada del procesamiento.
- La cola puede absorber temporalmente variaciones en la demanda.
- La base de datos no necesita procesar todo el trabajo directamente
  durante la recepción de cada solicitud.
- La persistencia de la cola reduce el riesgo de perder mensajes
  debido a un reinicio del proceso.
- El uso de UUID permite controlar duplicados.
- El Worker interno mantiene una infraestructura relativamente sencilla.
- Se evita introducir microservicios innecesarios durante el MVP.

## Consecuencias negativas

- La solución es más compleja que un procesamiento completamente
  síncrono.
- Se requiere configurar y mantener la persistencia de la cola.
- Debe controlarse el crecimiento de mensajes pendientes.
- Un fallo del Worker puede provocar acumulación de mensajes.
- El procesamiento asíncrono requiere pruebas adicionales.
- El Worker interno no permite escalarlo independientemente como
  ocurriría con un microservicio separado.
- La base de datos continúa siendo un posible punto único de fallo
  durante el MVP.

## Riesgos y mitigaciones

### Riesgo 1: Acumulación de mensajes

Si el Worker procesa mensajes más lentamente que la velocidad de
llegada, la cola puede crecer.

**Mitigación:** monitorear el tamaño de la cola y establecer
mecanismos de control durante futuras iteraciones.

### Riesgo 2: Duplicación de reportes

Los clientes pueden reenviar un reporte después de una interrupción
de red.

**Mitigación:** utilizar el UUID como identificador único y aplicar
idempotencia en el procesamiento.

### Riesgo 3: Pérdida de mensajes

Una cola sin persistencia podría perder mensajes ante un reinicio.

**Mitigación:** utilizar una cola con persistencia y confirmar
la recepción al cliente solamente después de que el mensaje haya sido
persistido.

## Relación con otras decisiones

Esta decisión depende de:

- ADR-001: selección del Monolito Modular con Ingesta Asíncrona.

Y complementa:

- ADR-002: estrategia de almacenamiento y sincronización offline.