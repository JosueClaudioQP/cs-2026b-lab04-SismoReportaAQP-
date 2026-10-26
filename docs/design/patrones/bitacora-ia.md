# E7. Bitácora de asistencia y verificación — 25/10/2026

Registro de esta preparación con ChatGPT. Los enunciados son síntesis de las
etapas de trabajo, no citas literales de prompts ni conversaciones inventadas
entre integrantes. El equipo debe revisarlo y añadir sus interacciones reales.
Solicitud del usuario: preparar las indicaciones del Lab 07 usando el ZIP del docente,
adaptadas al repositorio SismoReporta AQP y listas para subir.

| Registro | Necesidad / propuesta de IA | Verificación real | Resultado y decisión |
|---|---|---|---|
| IA-01 | Interpretar guía y ejecutar recursos AgroConecta antes de adaptar | pytest sobre ZIP docente: 27 passed, 1 xfailed | Ejemplo conservado como referencia; no se copian pagos como dominio del proyecto |
| IA-02 | Crear baseline ejecutable del flujo de sincronización y caracterizarlo | 43 casos de la variante antes pasan; `pytest-antes.txt` | Se especifica diferencia 202/RECIBIDO y memoria/persistencia real |
| IA-03 | Extraer Strategy, Adapter y Factory por registro; considerar Singleton | prueba de tercer canal y SDK equivalentes | Adoptados los tres primeros; Singleton y Abstract Factory rechazados por complejidad/estado global |
| IA-04 | State, Observer y Decorator para estados, avisos y reintentos | matriz 25 combinaciones; tercer observador; excepciones y agotamiento | Sincronización refactorizada mantiene resultados de baseline |
| IA-05 | Aislar IA, caché y guardrails; probar una regresión deliberada | `mutacion-bool.txt`: 1 failed, 9 passed al sustituir tipo exacto por isinstance | Se detecta aceptación incorrecta de `true` como número (bool hereda int); se restaura el guardrail correcto y suite verde. Es ensayo de mutación, no error histórico espontáneo |
| IA-06 | Medir CC y SLOC; contrastar script con salida cruda de radon | Primer script duplicaba métodos al iterar clases y lista plana; inspección de cc_visit reveló duplicación | Se corrige conteo; 12/81 bloques coinciden con CLI. No se oculta aumento de SLOC |
| IA-07 | Generar PlantUML y verificar por ingeniería inversa | pyreverse genera clases y paquetes; comprobación AST y render PNG | Se conserva diagrama Lab 05 como histórico; modelos concretos del experimento documentados |

No se usaron claves ni datos personales de ciudadanos. No se llamó a un LLM
externo desde las pruebas. La IA del producto es simulada y sus sugerencias no
cambian estados operacionales.

## Corrección demostrada por pruebas
Python considera `isinstance(True, (int, float))` verdadero. La mutación reemplazó
el chequeo estricto por esa expresión y el caso de confianza `true` dejó de lanzar
ValueError. La salida fallida se guardó y el archivo se restauró con
`type(confianza) not in (int, float)`. No hay un xfail que oculte la regresión.

## Trabajo humano pendiente
Leer y aprobar las decisiones, ejecutar localmente, crear PR por integrante,
realizar revisión cruzada y publicar la etiqueta. No se fabrican nombres, PR,
aprobaciones ni commits pasados para simular el cronograma del curso.
