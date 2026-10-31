# Iteración 3 de ADD

Escenarios: QA08-04 y QA08-05.

Elemento refinado: Operaciones autorizadas y extensión por puertos.

## Siete pasos
1. Revisar RF-07, ADR-001, ADR-005 y patrones de transporte ya implementados en Lab07.
2. Objetivo: 0 escrituras sin permiso; canal nuevo con 0 cambios en servicio central.
3. Elementos refinados: servicio de asignación y contratos CanalEnvio / CanalSMS.
4. Comparar: controles solo en UI (rechazados: API directa los evita); RBAC en aplicación (aceptado); RBAC + RLS (defensa adicional, aplazada hasta definir jurisdicciones). Comparar condicionales por proveedor con fábrica extensible ya existente.
5. Instanciar: rol coordinador puede asignar; ciudadano, brigadista, anónimo y operador de lectura no. El rol procede del contexto autenticado del servidor, nunca de un campo libre del JSON.
6. Documentar ADR-008 y FF-01/02; no se sustituyen servicios existentes por el prototipo de laboratorio.
7. Evaluar: 4 clases de acceso denegado, caso coordinador y prueba heredada de canal nuevo pasan. Es un prototipo de política, no una validación de JWT, TLS, RLS o pentest. La integración HTTP autenticada queda pendiente.

## Decisión
RBAC con denegación por defecto; Adapter + fábrica por registro; inyección de dependencias.

## Evidencia
Ver ../evidencia/resultados.json, ../pytest-lab08.txt y ../lint-lab08.txt.

## Límite
La simulación es evidencia del modelo, no certificación de capacidad del despliegue real.
