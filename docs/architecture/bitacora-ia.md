# Bitácora de uso de Inteligencia Artificial (E7) – SismoReporta AQP

Esta bitácora registra las interacciones realizadas con asistentes de Inteligencia Artificial durante las etapas de diseño arquitectónico de **SismoReporta AQP**, documentando el rol de la IA como asesora y la labor crítica del equipo de ingeniería para validar, corregir o rechazar sus propuestas conforme a los drivers de calidad y restricciones del proyecto.

---

## 1. Tabla consolidada de interacciones

| N.° | Fecha | Herramienta | Objetivo de la interacción | Decisión | Evidencia de verificación / Justificación |
|---|---|---|---|---|---|
| **IA-01** | 04/10/2026 | Google Gemini | Generar 3 alternativas de estilo arquitectónico a partir de drivers.md | **Aceptada con modificaciones** | Se obtuvieron 3 alternativas válidas (Monolito Asíncrono, Serverless, N-Capas). Sin embargo, la IA incluyó supuestos no demostrados que requirieron auditoría adversarial. |
| **IA-02** | 04/10/2026 | Google Gemini | Crítica adversarial ("Abogado del diablo") a las propuestas de estilos | **Corregida** | Se refutaron 6 afirmaciones de la IA: "escalabilidad infinita", "garantía de cero pérdida", tasa no requerida de "50-100 req/s", "costo cero en Serverless", e incapacidad injustificada de N-Capas. |
| **IA-03** | 04/10/2026 | Google Gemini | Revisión crítica del diseño preliminar del diagrama de arquitectura Mermaid | **Aceptada** | Se incorporaron recomendaciones necesarias: Sync Manager con backoff exponencial, UUID en cliente para idempotencia y desacoplamiento del flujo de fotos. |
| **IA-04** | 04/10/2026 | Google Gemini | Selección tecnológica de base de datos y almacenamiento de fotografías (ADR-003) | **Rechazada** | La IA propuso MongoDB Atlas en la nube con GridFS y AWS Lambdas. Se **rechazó** porque contradice R-01 (1 mes) y R-02 (3 devs), genera costos de nube no justificados y degrada la integridad relacional requerida para brigadas y estados (RF-05, RF-07). Se seleccionó PostgreSQL + MinIO/disco local. |
| **IA-05** | 04/10/2026 | Google Gemini | Diseño de la vista de despliegue (E6) y dimensionamiento para 20 000 reportes/hora | **Corregida** | La IA sugirió un clúster Kubernetes con Apache Kafka multirnodo. Se **corrigió** mediante cálculo de rendimiento: 20 000 req / 3600 s = 5.55 req/s promedio (pico estimado ~55 req/s). Redis soporta >50 000 ops/s sin la complejidad operacional de Kafka, cumpliendo R-01 y R-02. |

---

## 2. Detalle de interacciones

### Interacción IA-01 — Propuesta de estilos arquitectónicos

* **Objetivo:** Obtener tres alternativas de estilos arquitectónicos para SismoReporta AQP a partir de los drivers identificados en E1.
* **Herramienta:** Google Gemini
* **Decisión:** **Aceptada con modificaciones**

#### Resumen de la respuesta
Gemini propuso tres alternativas:
1. Monolito Modular con Ingesta Asíncrona.
2. Arquitectura Orientada a Eventos / Serverless.
3. Cliente-Servidor N-Capas Síncrono.

Recomendó preliminarmente el Monolito Modular con Ingesta Asíncrona, argumentando desacoplamiento temporal ante picos de demanda y menor sobrecarga operacional frente a microservicios.

#### Análisis del equipo
Si bien la propuesta de estilos fue pertinente, el equipo identificó afirmaciones excesivamente optimistas ("escalabilidad elástica infinita", "garantía absoluta de cero reportes perdidos" y una tasa arbitraria de "50–100 req/s"). Se decidió ejecutar una segunda interacción adversarial para cuestionar estos postulados.

---

### Interacción IA-02 — Abogado del diablo (Crítica adversarial)

* **Objetivo:** Cuestionar las recomendaciones iniciales, detectar afirmaciones exageradas, supuestos no justificados y riesgos arquitectónicos.
* **Herramienta:** Google Gemini
* **Decisión:** **Corregida**

#### Resumen de la respuesta
Gemini auditó su propia propuesta previa y admitió seis desviaciones técnicas:
1. **Escalabilidad infinita:** Admitió que los límites de concurrencia y pools de conexiones cloud impiden escalabilidad infinita real.
2. **Pérdida cero:** Reconoció que ninguna arquitectura elimina el 100% de fallos catastróficos de hardware o red sin mecanismos de idempotencia y almacenamiento local persistente.
3. **Tasa de ráfaga (50–100 req/s):** Corrigió que esta cifra fue una inferencia suya y no un dato del caso.
4. **Costo cero en Serverless:** Rectificó señalando costos fijos de almacenamiento, telemetría y transferencias de red.
5. **Incapacidad de la arquitectura N-Capas:** Matizó que un sistema en capas con escalado horizontal puede soportar picos moderados, aunque con mayor riesgo de saturación en base de datos.
6. **Complejidad de A1:** Reevaluó la complejidad de A1 de "baja-media" a "media-alta" debido a la gestión de colas, idempotencia y workers.

#### Evidencia de verificación
El equipo verificó estas correcciones contrastando los requisitos del caso y la literatura de arquitectura distribuida (patrones de colas e idempotencia con UUID), lo que fundamentó la puntuación objetiva en [`matriz-decision.md`](file:///home/gocardi/Unsa/cs/cs-2026b-lab04-SismoReportaAQP-/docs/architecture/matriz-decision.md).

---

### Interacción IA-03 — Revisión del diagrama arquitectónico

* **Objetivo:** Revisar críticamente los componentes, flujos y dependencias del diagrama Mermaid antes de su consolidación final.
* **Herramienta:** Google Gemini
* **Decisión:** **Aceptada**

#### Resumen de la respuesta y aportes
Gemini detectó tres debilidades críticas en el borrador inicial:
1. El envío de fotografías binarias pesadas dentro de la cola saturaría la memoria de la mensajería.
2. La falta de un mecanismo de reintento ordenado en la app móvil provocaría tormentas de solicitudes (*retry storms*) al regresar la conectividad.
3. El servicio externo de mapas no debía interponerse en la ruta crítica de ingesta.

#### Acciones adoptadas por el equipo
1. Se incorporó un **Sync Manager** en el cliente móvil con *Exponential Backoff* y *Jitter*.
2. Se estableció un **UUID generado en el cliente** para garantizar idempotencia en reintentos.
3. Se desacopló el almacenamiento de imágenes mediante almacenamiento de objetos referenciado por URL.
4. El servicio de mapas se limitó exclusivamente al panel web del operador.

---

### Interacción IA-04 — Selección tecnológica de Base de Datos y Almacenamiento

* **Objetivo:** Evaluar el motor de base de datos y la estrategia de almacenamiento de evidencia fotográfica (ADR-003).
* **Herramienta:** Google Gemini
* **Decisión:** **Rechazada**

#### Propuesta de la IA
Gemini propuso utilizar **MongoDB Atlas Cloud con GridFS** para almacenar tanto la metadata de los reportes como los binarios de las imágenes dentro de documentos BSON divididos en chunks, complementado con funciones serverless AWS Lambda para redimensionar imágenes.

#### Análisis y evidencia de rechazo del equipo
El equipo **rechazó** la recomendación de la IA con base en las siguientes evidencias verificables:
1. **Violación de restricciones de equipo y plazo (R-01, R-02):** Configurar y asegurar un clúster MongoDB Atlas, permisos de AWS IAM y Lambdas excede el plazo de 1 mes para un equipo de 3 estudiantes que ya domina bases de datos relacionales SQL.
2. **Inadecuación de GridFS para alto rendimiento de lectura/escritura:** Documentación oficial y benchmarks demuestran que GridFS incrementa el consumo de memoria en el motor de base de datos al mezclar binarios con datos transaccionales, saturando el Working Set de RAM durante picos de 20 000 reportes.
3. **Integridad referencial y soporte geoespacial (RF-05, RF-06, RF-07):** El caso exige consultar reportes por operador, clasificar daños, asignar brigadas y priorizar zonas. Un modelo relacional con **PostgreSQL + PostGIS** garantiza transacciones ACID, integridad referencial y funciones nativas espaciales (`ST_DWithin`, índices GiST) a costo de infraestructura cero en servidores locales o contenedores Docker.
4. **Estrategia adoptada:** PostgreSQL 16 para metadata y MinIO / almacenamiento en volumen de disco para fotografías referenciadas mediante paths URI livianos.

---

### Interacción IA-05 — Dimensionamiento de colas y vista de despliegue (E6)

* **Objetivo:** Definir la infraestructura de despliegue para absorber 20 000 reportes en la primera hora post-sismo (E6).
* **Herramienta:** Google Gemini
* **Decisión:** **Corregida**

#### Propuesta de la IA
La IA sugirió una infraestructura distribuida basada en un **clúster de Kubernetes (EKS)** con **Apache Kafka** multirnodo para la cola de eventos, balanceador AWS ALB y microservicios escalados horizontalmente mediante HPA (*Horizontal Pod Autoscaler*).

#### Análisis y evidencia de corrección del equipo
El equipo **corrigió** la propuesta por presentar una sobreingeniería desproporcionada:
1. **Cálculo de flujo de datos:**
   $$\text{Tasa promedio} = \frac{20\,000 \text{ peticiones}}{3\,600 \text{ segundos}} \approx 5.55 \text{ peticiones/segundo}$$
   Incluso con un factor de concentración pico de $10\times$ durante los 10 minutos más críticos posteriores al sismo, la tasa pico no excede:
   $$\text{Tasa pico} = 5.55 \times 10 \approx 55.5 \text{ peticiones/segundo}$$
2. **Capacidad de Redis vs Kafka:**
   * Apache Kafka requiere clúster de coordinación (ZooKeeper/KRaft), mínimo 3 brokers y >4 GB de RAM por nodo, introduciendo una complejidad operacional inmanejable para 3 desarrolladores en 1 mes (R-01, R-02).
   * Un único nodo de **Redis 7** en memoria con persistencia AOF maneja holgadamente más de **50 000 operaciones por segundo** con latencias sub-milisegundo (< 2 ms).
3. **Proxy perimetral:** Nginx como reverse proxy absorbe fácilmente ráfagas de 55 req/s consumiendo menos de 100 MB de RAM.
4. **Infraestructura final adoptada:** Servidor de despliegue único con Docker Compose conteniendo: Nginx (Proxy) + FastAPI Monolito Modular + Redis 7 (Cola) + Worker Interno + PostgreSQL 16 + MinIO + Prometheus/Grafana. Se documentó formalmente en [`despliegue.py`](file:///home/gocardi/Unsa/cs/cs-2026b-lab04-SismoReportaAQP-/docs/architecture/diagramas/despliegue.py) y [`despliegue.puml`](file:///home/gocardi/Unsa/cs/cs-2026b-lab04-SismoReportaAQP-/docs/architecture/diagramas/despliegue.puml).

---

## 3. Anexo de prompts completos

### Anexo IA-01: Prompt de propuesta de estilos arquitectónicos
```text
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
7. Complejidad de implementación para un equipo de 3 personas y un MVP de 1 mes.
8. Riesgos arquitectónicos.

IMPORTANTE:
No asumas que microservicios es automáticamente la mejor opción por permitir escalabilidad. Considera también complejidad operacional, tiempo de desarrollo, fiabilidad, disponibilidad y capacidad del equipo.

FORMATO:
Presenta la respuesta en una tabla comparativa y después incluye una recomendación preliminar de cuál de las tres alternativas consideras más adecuada y por qué.
No inventes requisitos que no hayan sido proporcionados. Distingue claramente entre hechos del caso y tus inferencias.
```

### Anexo IA-02: Prompt de Abogado del Diablo (Crítica adversarial)
```text
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
- Puede haber hasta 20 000 reportes durante la primera hora después de un sismo.
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
1. ¿Qué afirmaciones de tu respuesta anterior fueron demasiado optimistas o exageradas?
2. ¿Qué afirmaciones no están demostradas por los datos del caso?
3. ¿Qué supuestos introdujiste que NO aparecen en los requisitos?
4. ¿Qué riesgos podrían hacer que la arquitectura falle?
5. ¿Cómo afecta la arquitectura a la disponibilidad ante 20 000 reportes en la primera hora?
6. ¿Cómo afecta la arquitectura al funcionamiento offline?
7. ¿Cómo afecta la arquitectura a la fiabilidad de la sincronización?
8. ¿Qué complejidad introduce para un equipo de 3 personas y un MVP de 1 mes?
9. ¿Existe alguna razón para NO elegir el Monolito Modular con Ingesta Asíncrona?
10. ¿Existe alguna razón para reconsiderar alguna de las otras dos alternativas?

IMPORTANTE:
Presta especial atención a estas afirmaciones de tu respuesta anterior:
- "Escalabilidad elástica e infinita".
- "Garantiza que ningún reporte se pierda".
- "ráfagas de 50–100 req/s".
- "costo cero en periodos sin actividad".
- "incapaz de soportar picos extremos" de la arquitectura Cliente-Servidor.

Indica si cada una es:
VERIFICADA, RAZONABLE, NO JUSTIFICADA, EXAGERADA o INCORRECTA.
```

### Anexo IA-03: Prompt de revisión del diagrama arquitectónico
```text
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
Ciudadano → Aplicación móvil → API REST → Módulo de Ingesta → Cola → Worker → Base de datos.
Operador → Panel web → API REST → Módulo de Operaciones → Base de datos.
La aplicación móvil también utiliza SQLite para almacenar reportes cuando no existe conectividad.

TAREA:
Revisa críticamente este diseño antes de implementarlo en un diagrama Mermaid.
Identifica:
1. Componentes innecesarios.
2. Componentes que podrían faltar.
3. Dependencias incorrectas.
4. Posibles puntos únicos de fallo.
5. Problemas relacionados con la sincronización offline.
6. Problemas relacionados con duplicación de reportes.
7. Problemas relacionados con fotografías.
8. Si el flujo de ingesta asíncrona es coherente con los drivers de disponibilidad, rendimiento y fiabilidad.
9. Si el diseño sigue siendo coherente con un equipo de 3 personas y un MVP de 1 mes.
```

### Anexo IA-04: Prompt de selección de base de datos y fotos
```text
Actúa como arquitecto de bases de datos para SismoReporta AQP.
Necesitamos decidir la tecnología de persistencia de datos y de archivos de evidencia (fotografías) para redactar el ADR-003.

Contexto y restricciones:
- MVP en 1 mes (R-01).
- 3 desarrolladores universitarios (R-02).
- Presupuesto bajo (servicios de pago deben justificarse).
- 20 000 reportes en 1 hora tras un sismo.
- Cada reporte tiene metadata (fecha, coordenadas, nivel de daño) y hasta 3 fotografías.
- Actores: Ciudadano registra; Operador consulta, clasifica, actualiza estado y asigna brigadas en mapa (RF-05, RF-06, RF-07).

Pregunta:
¿Qué motor de base de datos recomiendas para almacenar reportes y fotografías? Compara MongoDB con GridFS frente a PostgreSQL con almacenamiento en archivos/S3.
```

### Anexo IA-05: Prompt de dimensionamiento de cola y vista de despliegue
```text
Actúa como ingeniero de infraestructura y DevOps.
Estamos preparando la vista de despliegue física y de contenedores (E6) para SismoReporta AQP.

Requisito de carga:
- Soportar 20 000 reportes en la primera hora tras el sismo.
- Atributo crítico: Disponibilidad y p95 <= 3 segundos en el endpoint de recepción.
- Restricciones: MVP en 1 mes, 3 desarrolladores, despliegue reproducible y bajo presupuesto.

Pregunta:
¿Qué infraestructura de despliegue, proxy, motor de colas y clúster recomiendas para garantizar que el endpoint no colapse ante los 20 000 reportes? ¿Deberíamos usar Apache Kafka y Kubernetes (EKS)? Proporciona el dimensionamiento en req/s y la justificación.
```