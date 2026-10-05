# Bitácora de uso de IA

## Interacción IA-01 — Propuesta de estilos arquitectónicos

### Objetivo
Obtener alternativas de estilos arquitectónicos para SismoReporta AQP
a partir de los drivers arquitectónicos identificados en E1.

### Herramienta
Google Gemini

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

## Interacción IA-02 — Abogado del diablo

### Objetivo

Cuestionar las recomendaciones y detectar afirmaciones
exageradas, supuestos no justificados y riesgos arquitectónicos.

### Herramienta

Google Gemini

### Prompt

ACTÚA COMO ABOGADO DEL DIABLO Y AUDITOR DE TU RESPUESTA ANTERIOR.

Estamos realizando el laboratorio de Fundamentos de Arquitectura
de Software para el caso SismoReporta AQP.

Tu respuesta anterior propuso:

A1: Monolito Modular con Ingesta Asíncrona.
A2: Arquitectura Orientada a Eventos / Serverless.
A3: Cliente-Servidor N-Capas Síncrono.

Tu recomendación preliminar fue A1.

Ahora NO debes defender automáticamente esa recomendación.
Debes intentar encontrar errores, exageraciones, supuestos no
justificados y riesgos en tu propia respuesta.

CONTEXTO REAL DEL CASO:

- El sistema permite registrar reportes de daños por sismos.
- Puede incluir fotografías y ubicación.
- Debe funcionar con conectividad móvil intermitente.
- Los reportes deben poder almacenarse offline y sincronizarse.
- Puede haber hasta 20 000 reportes durante la primera hora
  después de un sismo.
- La red móvil puede estar congestionada.
- El equipo es de máximo 3 integrantes.
- El MVP debe desarrollarse en 1 mes.

DRIVERS DE CALIDAD:

1. Disponibilidad
2. Rendimiento
3. Fiabilidad
4. Usabilidad

TAREA:

Analiza críticamente las tres alternativas.

Para cada una responde:

1. ¿Qué afirmaciones de tu respuesta anterior fueron demasiado
   optimistas o exageradas?

2. ¿Qué afirmaciones no están demostradas por los datos del caso?

3. ¿Qué supuestos introdujiste que NO aparecen en los requisitos?

4. ¿Qué riesgos podrían hacer que la arquitectura falle?

5. ¿Cómo afecta la arquitectura a la disponibilidad ante
   20 000 reportes en la primera hora?

6. ¿Cómo afecta la arquitectura al funcionamiento offline?

7. ¿Cómo afecta la arquitectura a la fiabilidad de la sincronización?

8. ¿Qué complejidad introduce para un equipo de 3 personas
   y un MVP de 1 mes?

9. ¿Existe alguna razón para NO elegir el Monolito Modular
   con Ingesta Asíncrona?

10. ¿Existe alguna razón para reconsiderar alguna de las otras
    dos alternativas?

IMPORTANTE:

Distingue claramente entre:

- Hechos proporcionados por el caso.
- Inferencias razonables.
- Supuestos introducidos por la IA.
- Afirmaciones que requieren verificación.

No inventes nuevos requisitos.

Presta especial atención a estas afirmaciones de tu respuesta anterior:

- "Escalabilidad elástica e infinita".
- "Garantiza que ningún reporte se pierda".
- "ráfagas de 50–100 req/s".
- "costo cero en periodos sin actividad".
- "incapaz de soportar picos extremos" de la arquitectura
  Cliente-Servidor.

Indica si cada una es:
VERIFICADA, RAZONABLE, NO JUSTIFICADA, EXAGERADA o INCORRECTA.

FORMATO DE RESPUESTA:

1. Auditoría de afirmaciones

| Afirmación | Clasificación | Justificación |
|---|---|---|

2. Crítica de las alternativas

| Alternativa | Problema | Driver afectado | Severidad |
|---|---|---|---|

3. Recomendación revisada

Indica si mantienes o cambias la recomendación de A1.

Explica la decisión considerando principalmente los drivers
de calidad y las restricciones del proyecto.

4. Conclusión

Indica qué alternativa debería pasar a la matriz de decisión
y qué riesgos deben ser considerados posteriormente.

### Resumen de la respuesta

Gemini revisó las tres alternativas y corrigió varias afirmaciones
realizadas en su primera respuesta.

Se determinó que la afirmación sobre una "escalabilidad elástica
e infinita" de Serverless era exagerada y que la garantía de que
"ningún reporte se pierda" tampoco podía considerarse absoluta.

También se identificó que la estimación de ráfagas de 50–100 req/s
no corresponde a un dato explícito del caso, por lo que debe
considerarse una inferencia y no un requisito.

La complejidad de A1 también fue reconsiderada, pasando de una
estimación inicial de baja-media a una valoración alta debido a
la implementación de colas, workers, idempotencia y sincronización
offline.

Afirmaciones corregidas
1. Se rechazó la afirmación de escalabilidad "infinita".
2. Se rechazó la garantía absoluta de cero pérdida de reportes.
3. Se corrigió la tasa de 50–100 req/s como una inferencia.
4. Se corrigió la afirmación de costo cero de Serverless.
5. Se corrigió la afirmación de que A3 es incapaz de soportar picos.
6. Se corrigió la estimación de complejidad de A1.

### Decisión del equipo
Después de revisar las alternativas y aplicar una matriz de decisión
ponderada, se seleccionó A1: Monolito Modular con Ingesta Asíncrona
Simplificada, con una puntuación de 4.40/5.

### IA-03 — Revisión del diagrama arquitectónico

**Herramienta:** Gemini

Actúa como revisor de arquitectura de software.

Estamos diseñando el diagrama arquitectónico de SismoReporta AQP.

La arquitectura seleccionada mediante una matriz de decisión es:

"Monolito Modular con Ingesta Asíncrona Simplificada".

El diseño propuesto contiene:

- Ciudadano.
- Aplicación móvil.
- SQLite local para almacenamiento offline.
- Panel web para operadores.
- API REST.
- Módulo de Ingesta.
- Módulo de Operaciones.
- Cola de mensajes persistente.
- Worker de procesamiento asíncrono.
- Base de datos.
- Almacenamiento de fotografías.
- Servicio externo de mapas.

Flujos principales:

Ciudadano → Aplicación móvil → API REST → Módulo de Ingesta
→ Cola → Worker → Base de datos.

Operador → Panel web → API REST → Módulo de Operaciones
→ Base de datos.

La aplicación móvil también utiliza SQLite para almacenar
reportes cuando no existe conectividad.

TAREA:

Revisa críticamente este diseño antes de implementarlo
en un diagrama Mermaid.

Identifica:

1. Componentes innecesarios.
2. Componentes que podrían faltar.
3. Dependencias incorrectas.
4. Posibles puntos únicos de fallo.
5. Problemas relacionados con la sincronización offline.
6. Problemas relacionados con duplicación de reportes.
7. Problemas relacionados con fotografías.
8. Si el flujo de ingesta asíncrona es coherente con los drivers
   de disponibilidad, rendimiento y fiabilidad.
9. Si el diseño sigue siendo coherente con un equipo de 3 personas
   y un MVP de 1 mes.

No agregues funcionalidades que no estén justificadas.
Distingue entre una recomendación y un requisito obligatorio.

Presenta la respuesta en una tabla:

Elemento | Observación | Severidad | 

Resultado: Se identificaron problemas relacionados con el
manejo de fotografías, idempotencia, sincronización offline,
persistencia de la cola y dependencia del servicio externo de mapas.

Decisiones posteriores:

Se agregó un Sync Manager a la aplicación móvil.
Se incorporó un UUID único por reporte.
Se estableció persistencia para la cola.
Se desacopló el almacenamiento de fotografías.
El servicio de mapas quedó fuera del flujo crítico de ingesta.
El Worker se mantiene dentro del monolito para reducir complejidad.
Se mantiene una única BD durante el MVP.


---

# 11. E3 ya queda prácticamente terminado

Nuestra estructura queda:

```text
docs/
└── architecture/
    ├── drivers.md
    ├── matriz-decision.md
    ├── bitacora-ia.md       ← IA-01, IA-02, IA-03
    │
    ├── adr/
    │   ├── 000-plantilla.md
    │   ├── 001-estilo-arquitectonico.md
    │   ├── 002-decision.md
    │   └── 003-decision.md
    │
    └── diagramas/
        ├── arquitectura.mmd ← ACTUALIZADO
        ├── alternativa.puml
        └── img/
            └── arquitectura.png