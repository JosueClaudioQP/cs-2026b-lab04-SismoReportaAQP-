# Matriz de decisión arquitectónica – SismoReporta AQP

## 1. Alternativas evaluadas

| ID | Alternativa |
|---|---|
| A1 | Monolito Modular con Ingesta Asíncrona Simplificada |
| A2 | Arquitectura Orientada a Eventos / Serverless |
| A3 | Cliente-Servidor N-Capas Síncrono |

La alternativa A1 utiliza un módulo de ingesta desacoplado mediante
una cola y procesamiento asíncrono. La aplicación móvil utiliza
almacenamiento local para soportar períodos sin conectividad.

La alternativa A2 utiliza una arquitectura orientada a eventos
basada en servicios serverless y servicios administrados en la nube.

La alternativa A3 utiliza una arquitectura tradicional de
cliente-servidor organizada en capas, con procesamiento síncrono.


## 2. Criterios de evaluación

| ID | Criterio | Peso |
|---|---|---:|
| C1 | Disponibilidad ante picos de demanda | 25 % |
| C2 | Fiabilidad de sincronización offline | 20 % |
| C3 | Rendimiento durante el envío de reportes | 15 % |
| C4 | Complejidad y tiempo de implementación | 20 % |
| C5 | Facilidad de mantenimiento y evaluación local | 10 % |
| C6 | Escalabilidad futura | 10 % |
| | **TOTAL** | **100 %** |


## 3. Justificación de los pesos

### C1 — Disponibilidad ante picos de demanda: 25 %

Es el criterio de mayor peso porque el principal desafío del caso
es mantener disponible el sistema ante hasta 20 000 reportes durante
la primera hora posterior a un sismo y bajo condiciones de
congestión de la red móvil.

### C2 — Fiabilidad de sincronización offline: 20 %

El sistema debe considerar la pérdida o interrupción de conectividad.
Los reportes generados sin conexión deben poder almacenarse y
sincronizarse posteriormente.

### C3 — Rendimiento: 15 %

El rendimiento es uno de los principales atributos de calidad y
determina la capacidad del sistema para procesar los reportes
durante situaciones de alta demanda.

### C4 — Complejidad y tiempo de implementación: 20 %

El MVP debe desarrollarse en un plazo máximo de un mes y el equipo
está limitado a tres integrantes. Por ello la complejidad de
implementación tiene un peso importante.

### C5 — Facilidad de mantenimiento y evaluación local: 10 %

La solución debe ser adecuada para el contexto académico y poder
ser desarrollada, documentada, versionada y evaluada con las
herramientas utilizadas en el laboratorio.

### C6 — Escalabilidad futura: 10 %

Aunque el objetivo inmediato es implementar el MVP, la arquitectura
debe permitir aumentar la capacidad del sistema posteriormente.


## 4. Escala de evaluación

| Puntuación | Significado |
|---:|---|
| 1 | Muy deficiente |
| 2 | Deficiente |
| 3 | Aceptable |
| 4 | Bueno |
| 5 | Excelente |


## 5. Puntuaciones

| Criterio | Peso | A1: Monolito Asíncrono | A2: Serverless | A3: N-Capas Síncrono |
|---|---:|---:|---:|---:|
| C1. Disponibilidad ante picos | 25 % | 5 | 5 | 2 |
| C2. Fiabilidad offline | 20 % | 5 | 5 | 3 |
| C3. Rendimiento | 15 % | 5 | 5 | 3 |
| C4. Complejidad / tiempo | 20 % | 3 | 1 | 5 |
| C5. Mantenimiento / evaluación local | 10 % | 4 | 2 | 5 |
| C6. Escalabilidad futura | 10 % | 4 | 5 | 3 |


## 6. Cálculo ponderado

La puntuación se obtiene mediante:

Puntaje = Σ (Peso × Puntuación) / 100


### A1 — Monolito Modular con Ingesta Asíncrona

(25×5 + 20×5 + 15×5 + 20×3 + 10×4 + 10×4) / 100

= (125 + 100 + 75 + 60 + 40 + 40) / 100

= 440 / 100

= **4.40 / 5**


### A2 — Arquitectura Orientada a Eventos / Serverless

(25×5 + 20×5 + 15×5 + 20×1 + 10×2 + 10×5) / 100

= (125 + 100 + 75 + 20 + 20 + 50) / 100

= 390 / 100

= **3.90 / 5**


### A3 — Cliente-Servidor N-Capas Síncrono

(25×2 + 20×3 + 15×3 + 20×5 + 10×5 + 10×3) / 100

= (50 + 60 + 45 + 100 + 50 + 30) / 100

= 335 / 100

= **3.35 / 5**


## 7. Resultado

| Posición | Alternativa | Puntaje |
|---:|---|---:|
| 1 | A1 — Monolito Modular con Ingesta Asíncrona | **4.40 / 5** |
| 2 | A2 — Serverless Event-Driven | **3.90 / 5** |
| 3 | A3 — Cliente-Servidor N-Capas Síncrono | **3.35 / 5** |

La alternativa seleccionada es:

**A1 — Monolito Modular con Ingesta Asíncrona Simplificada.**


## 8. Justificación de la decisión

A1 obtiene el mayor puntaje debido a que presenta un equilibrio
entre disponibilidad, rendimiento, fiabilidad y complejidad de
implementación.

La utilización de una estrategia de ingesta asíncrona permite
desacoplar la recepción del reporte del procesamiento posterior,
reduciendo el riesgo de que la base de datos se convierta
inmediatamente en el punto de bloqueo durante un pico de demanda.

Además, el almacenamiento local en el dispositivo móvil permite
mantener los reportes pendientes cuando existe una interrupción
de conectividad.

A diferencia de A2, A1 evita introducir una dependencia importante
de infraestructura serverless y servicios específicos de un
proveedor cloud.

A3 presenta la menor complejidad de implementación, pero obtiene
una puntuación inferior debido al riesgo de saturación durante
picos de demanda y durante la sincronización de múltiples
dispositivos.


## 9. Verificación de afirmaciones de IA

Durante las interacciones con Google Gemini se identificaron
afirmaciones que requerían corrección.

| Afirmación | Evaluación | Corrección |
|---|---|---|
| "Escalabilidad elástica e infinita" | Exagerada | La escalabilidad depende de los recursos y límites de la infraestructura utilizada. |
| "Garantiza que ningún reporte se pierda" | Exagerada | La arquitectura reduce el riesgo de pérdida, pero no permite garantizar pérdida cero ante todos los fallos posibles. |
| "Ráfagas de 50–100 req/s" | No especificada por el caso | Se considera una inferencia y no un requisito del sistema. |
| "Costo cero en periodos sin actividad" | Exagerada | Pueden existir costos asociados a almacenamiento, monitoreo y otros servicios. |
| "A3 es incapaz de soportar picos extremos" | Exagerada | Su capacidad depende de cómo se diseñe la recepción y procesamiento de los reportes. |
| "A1 tiene baja-media complejidad" | No justificada | La complejidad se considera media-alta debido a la cola, workers, idempotencia y sincronización offline. |


## 10. Conclusión

La matriz de decisión selecciona A1, Monolito Modular con Ingesta
Asíncrona Simplificada, con una puntuación de 4.40/5.

La decisión no se basa únicamente en la recomendación de la IA.
Se consideraron los drivers arquitectónicos, las restricciones del
proyecto y los riesgos identificados durante la revisión crítica
de las propuestas generadas por IA.

La arquitectura seleccionada deberá ser detallada y documentada
mediante los diagramas y decisiones arquitectónicas de las
siguientes etapas del laboratorio.