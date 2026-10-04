# Drivers arquitectónicos – SismoReporta AQP

## 1. Requisitos funcionales clave

| ID    | Requisito | Actor | Prioridad |
|-------|-----------|-------|-----------|
| RF-01 | El ciudadano registra un reporte de daños ocasionados por un sismo. | Ciudadano | Alta |
| RF-02 | El ciudadano adjunta fotografías como evidencia del daño reportado. | Ciudadano | Alta |
| RF-03 | El sistema registra la ubicación asociada al reporte. | Ciudadano | Alta |
| RF-04 | El sistema almacena localmente los reportes cuando no existe conexión a Internet y los sincroniza posteriormente. | Ciudadano | Alta |
| RF-05 | El operador consulta los reportes registrados y su información asociada. | Operador | Alta |
| RF-06 | El operador clasifica los reportes según el tipo o nivel de daño. | Operador | Media |
| RF-07 | El operador actualiza el estado de los reportes registrados. | Operador | Media |


## 2. Atributos de calidad (ordenados por prioridad)

1. **Disponibilidad** – Es crítico porque el sistema debe continuar aceptando reportes durante situaciones de emergencia y ante picos extremos de demanda.
2. **Rendimiento** – El sistema debe procesar una gran cantidad de reportes durante un periodo corto de tiempo.
3. **Fiabilidad** – Los reportes no deben perderse cuando existe una interrupción o ausencia de conectividad.
4. **Usabilidad** – Los ciudadanos deben poder registrar un reporte rápidamente durante una situación de emergencia.


## 3. Restricciones

| ID    | Tipo       | Restricción |
|-------|------------|-------------|
| R-01  | Plazo      | El MVP debe desarrollarse en un plazo máximo de 1 mes. |
| R-02  | Equipo     | El proyecto será desarrollado por un equipo académico de máximo 3 integrantes. |
| R-03  | Conectividad | El sistema debe considerar escenarios con conectividad móvil intermitente o inexistente. |
| R-04  | Herramientas | La solución debe poder ser desarrollada, documentada y versionada utilizando las herramientas indicadas en el laboratorio. |


## 4. Escenarios de atributos de calidad

| ID    | Atributo | Fuente | Estímulo | Entorno | Artefacto | Respuesta | Medida |
|-------|----------|--------|----------|---------|-----------|-----------|--------|
| QA-01 | Disponibilidad / Rendimiento | Ciudadanos afectados por un sismo | Los usuarios envían una gran cantidad de reportes simultáneamente | Primera hora después de un sismo | API de recepción de reportes | El sistema acepta, procesa o coloca en cola los reportes sin perder información | Soportar hasta 20 000 reportes durante la primera hora sin pérdida de información |
| QA-02 | Fiabilidad | Dispositivo móvil del ciudadano | El usuario registra un reporte mientras no existe conexión | Red móvil congestionada o sin conectividad | Aplicación móvil y cola local | El reporte se almacena localmente y se sincroniza cuando se restablece la conexión | 0 reportes perdidos debido a interrupciones de conectividad |
| QA-03 | Usabilidad / Rendimiento | Ciudadano | El ciudadano inicia el registro de un reporte | Situación de emergencia | Interfaz de registro de reportes | El usuario puede completar y almacenar el reporte sin pasos innecesarios | El formulario principal debe poder completarse en ≤ 60 segundos, sin considerar el tiempo de subida de fotografías |