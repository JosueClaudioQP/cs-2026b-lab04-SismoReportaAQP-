# ADR-004: Persistencia de reportes y almacenamiento de evidencia fotográfica

- **Estado:** Aceptado
- **Fecha:** 17/10/2026
- **Decisores:** Equipo de trabajo de SismoReporta AQP

## Contexto

La bitácora del Lab 04 (IA-04) rechazó MongoDB Atlas + GridFS y eligió PostgreSQL + MinIO, y `despliegue.puml` (E6) ya los usa, pero no existía un ADR que lo formalizara. Además, al modelar el C4 se detectó una contradicción: E6 muestra al worker guardando las fotos, mientras que el ADR-003 prohíbe transportar fotos binarias dentro de la cola.

Restricciones: R-01 (MVP de 1 mes), R-02 (3 integrantes), RF-05 a RF-07 (consulta, clasificación y estados por operadores) y priorización de zonas (consultas geoespaciales).

## Alternativas consideradas

1. **MongoDB Atlas + GridFS:** rechazada en IA-04 (nube de pago, curva de aprendizaje, sin integridad relacional).
2. **PostgreSQL con fotos en columnas binarias:** infla la base de datos y mezcla datos transaccionales con binarios.
3. **PostgreSQL + PostGIS para metadata y MinIO (API S3) para fotos:** elegida.

## Decisión

- Metadata, estados, UUID y brigadas en **PostgreSQL 16 + PostGIS**.
- Fotografías en **MinIO**, referenciadas por URI desde el reporte.
- El módulo **Ingesta guarda la foto en MinIO antes de publicar** en la cola; la cola lleva solo metadata y la referencia (coherente con ADR-003). El Worker (módulo Procesamiento) persiste la metadata en PostgreSQL. Esto **corrige** la flecha "worker → MinIO" de E6 (`despliegue.puml`, `despliegue.py` y su imagen).
- Despliegue del MVP en un solo servidor con Docker Compose (Linux, 4 vCPU, 8 GB RAM, disco SSD). Es un dimensionamiento inicial, a validar con una prueba de carga; la restricción de presupuesto bajo proviene de la bitácora (IA-04, IA-05).
- Enmienda a ADR-003: Redis con persistencia AOF y `appendfsync always` para poder responder 202 solo cuando el mensaje ya está en disco.

## Consecuencias positivas

- Integridad relacional y consultas espaciales (`ST_DWithin`, índices GiST) sin costo de nube.
- La cola se mantiene liviana.

## Consecuencias negativas

- Un solo servidor es un punto único de fallo (host, Redis, PostgreSQL, MinIO) y está en la región del sismo; queda como riesgo aceptado del MVP.
- `appendfsync always` reduce el rendimiento de la cola; debe medirse en la prueba de carga.
- Si la subida de la foto falla pero el reporte ya fue aceptado, hay que definir un reintento de evidencia.
