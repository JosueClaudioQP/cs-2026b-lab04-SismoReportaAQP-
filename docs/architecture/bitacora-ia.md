# Bitácora de uso de IA

## Interacción IA-01 — Propuesta de estilos arquitectónicos

### Objetivo
Obtener alternativas de estilos arquitectónicos para SismoReporta AQP
a partir de los drivers arquitectónicos identificados en E1.

### Herramienta
Gemini

### Prompt
ROL:
Actúa como arquitecto de software senior especializado en sistemas
distribuidos, sistemas tolerantes a fallos y aplicaciones móviles
con conectividad intermitente.

CONTEXTO:
Estamos desarrollando "SismoReporta AQP", un sistema para registrar
y gestionar reportes de daños ocasionados por sismos.

El sistema tiene los siguientes requisitos funcionales:

RF-01: El ciudadano registra un reporte de daños ocasionados por un sismo.
RF-02: El ciudadano adjunta fotografías como evidencia.
RF-03: El sistema registra la ubicación asociada al reporte.
RF-04: El sistema almacena localmente los reportes cuando no existe
conexión a Internet y los sincroniza posteriormente.
RF-05: El operador consulta los reportes registrados.
RF-06: El operador clasifica los reportes según tipo o nivel de daño.
RF-07: El operador actualiza el estado de los reportes.

Drivers de calidad, ordenados por prioridad:

1. Disponibilidad: el sistema debe continuar aceptando reportes
   durante situaciones de emergencia y ante picos extremos de demanda.
2. Rendimiento: debe procesar una gran cantidad de reportes durante
   un periodo corto.
3. Fiabilidad: no deben perderse reportes debido a interrupciones
   de conectividad.
4. Usabilidad: el ciudadano debe poder registrar un reporte rápidamente.

Escenario crítico:
Durante la primera hora después de un sismo pueden generarse hasta
20 000 reportes, mientras la red móvil se encuentra congestionada.
El sistema debe considerar una cola offline para evitar la pérdida
de reportes.

Restricciones:

R-01: El MVP debe desarrollarse en un máximo de 1 mes.
R-02: El equipo académico tiene máximo 3 integrantes.
R-03: Debe considerarse conectividad móvil intermitente o inexistente.
R-04: La solución debe poder documentarse y versionarse mediante
las herramientas indicadas en el laboratorio.

TAREA:
Propón exactamente 3 estilos arquitectónicos adecuados para
SismoReporta AQP.

Considera estilos como arquitectura en capas, cliente-servidor,
monolito modular, microservicios, arquitectura orientada a eventos,
hexagonal u otros que consideres apropiados.

Para cada alternativa explica:

1. Nombre del estilo.
2. Cómo se aplicaría específicamente a SismoReporta AQP.
3. Cómo respondería al escenario de 20 000 reportes en una hora.
4. Cómo manejaría los reportes offline.
5. Ventajas.
6. Desventajas.
7. Complejidad de implementación para un equipo de 3 personas
   y un MVP de 1 mes.
8. Riesgos arquitectónicos.

IMPORTANTE:
No asumas que microservicios es automáticamente la mejor opción
por permitir escalabilidad. Considera también complejidad operacional,
tiempo de desarrollo, fiabilidad, disponibilidad y capacidad del
equipo.

FORMATO:
Presenta la respuesta en una tabla comparativa y después incluye
una recomendación preliminar de cuál de las tres alternativas
consideras más adecuada y por qué.

No inventes requisitos que no hayan sido proporcionados.
Distingue claramente entre hechos del caso y tus inferencias.

### Resumen de la respuesta
Gemini propuso tres alternativas:

1. Monolito Modular con Ingesta Asíncrona.
2. Arquitectura Orientada a Eventos / Serverless.
3. Cliente-Servidor N-Capas Síncrono.

La alternativa recomendada preliminarmente fue el Monolito
Modular con Ingesta Asíncrona.

Entre los argumentos utilizados se encuentra la utilización
de una cola para desacoplar la recepción de reportes del
procesamiento y persistencia, además del almacenamiento local
en el dispositivo móvil para soportar períodos sin conectividad.

#### Observaciones del equipo

La respuesta contiene algunas afirmaciones que requieren
revisión antes de ser utilizadas como decisiones arquitectónicas.

Entre ellas se encuentran la afirmación de una "escalabilidad
elástica e infinita", la garantía de que "ningún reporte se
pierda" y la utilización de una tasa de ráfaga de 50–100 req/s,
ya que esta última no está especificada explícitamente en el
caso.

Se realizará una segunda interacción con IA utilizando el
enfoque de "abogado del diablo" para cuestionar estas
afirmaciones.

### Decisión del equipo
Pendiente de evaluación mediante matriz de decisión.