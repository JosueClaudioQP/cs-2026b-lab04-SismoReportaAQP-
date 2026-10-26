# Laboratorio 07 — SismoReporta AQP

Caso 8. Flujo: registrar sin señal, sincronizar con un canal simulado, procesar,
verificar por un operador y atender con una brigada. Función IA: sugerir severidad
LEVE/MODERADO/SEVERO a partir de una descripción; nunca verifica automáticamente.

## Entregables
| Ítem | Evidencia |
|---|---|
| E1 | [Antes](../../../src/reportes/antes/servicio.py), [pruebas](../../../tests/test_comportamiento.py), [olores](olores.md) |
| E2 | [Transporte](../../../src/reportes/despues/transporte.py): Strategy, Adapter y fábrica por registro |
| E3 | [State](../../../src/reportes/despues/estados.py), matriz completa de 25 pares estado/acción |
| E4 | [Observer](../../../src/reportes/despues/eventos.py), Decorator de reintentos |
| E5 | [IA](../../../src/reportes/despues/ia.py), caché y tres guardrails |
| E6 | [Métricas](metricas.md), salidas crudas en [evidencias](evidencias/) |
| E7 | [Diagramas](#diagramas), [round-trip](round-trip.md), [bitácora](bitacora-ia.md) |
| E8 | [ADR-006](../../architecture/adr/006-patrones-diseno-lab07.md), [revisión pendiente](revision-cruzada.md), README raíz |
| Cuestionario | [Ocho respuestas](cuestionario.md) |
| Reto B | [GitHub Action](../../../.github/workflows/lab07.yml), verificador de CC con código de salida no cero |

Los enlaces de código desde esta carpeta apuntan a la raíz del repositorio.

## Ejecución desde la raíz del repositorio
```bash
python -m pip install -r requirements-lab07.txt
python -m pytest -v
python tools/demo_lab07.py
python tools/verificar_complejidad.py
python tools/medir_lab07.py
```
Entorno verificado: Python 3.12. La sintaxis del proyecto usa Python 3.10+.
La instalación de dependencias requiere Internet; la demo y las pruebas no.

## Alcance y continuidad con los Labs 04–06
La rama main revisada contenía un esqueleto con métodos sin implementar.
Por ello E1 crea una versión ingenua ejecutable, no pretende ser código que ya
funcionaba en producción. Las versiones usan los enum EstadoReporte y NivelDanio
existentes en `reportes.dominio`, y datos comunes en `datos_lab07.py`.
El esqueleto `dominio.py`/`servicios.py` se conserva para no romper entregables anteriores.
La implementación del experimento se importa desde `reportes.despues.servicio`.
No se presenta como un reemplazo completo de todos los componentes del Lab 05.

La variación Strategy es el canal/proveedor de ingreso: dos interfaces simuladas
permiten cambiar el transporte sin cambiar la coordinación del flujo. Es una
variación añadida para E2, no un nuevo servicio productivo aprobado en el C4.
La guía sugiere Command para el caso 8, pero E4 permite Observer y Decorator:
se eligen estos dos, por notificaciones y reintentos existentes. No se añade Command
sin necesidad de serializar/ejecutar órdenes persistentes.

**202 = aceptación, no procesamiento final.** El reporte sigue ENCOLADO hasta
`procesar()`, que representa al worker y lo cambia a RECIBIDO. La eliminación de
pendientes representa el ACK; los SDK solo simulan el almacenamiento. Un UUID ya
aceptado vuelve a recibir 202, para tolerar la pérdida de la respuesta inicial.
Las notificaciones son por aceptación, no por atención ni procesamiento.

**Fuera de alcance:** SQLite, Redis AOF, PostgreSQL, fotos, FastAPI, SMS, red real,
backoff con espera, concurrencia y recuperación tras caídas. Pendientes, caché,
servidor y eventos están en memoria; no garantizan durabilidad. Un rechazo HTTP
mantiene el reporte pendiente pero no se reintenta dentro del mismo ciclo; una UI
real deberá distinguir rechazos definitivos y reintentos posteriores.
`procesar()` es una acción explícita de la simulación, no consume una cola real.
El Observer es síncrono: una excepción de suscriptor se propaga; no hay outbox.
La caché es por instancia y sin TTL; también conserva respuestas inválidas, pero
las vuelve a validar y nunca las publica como sugerencias aceptadas.
Los guardrails validan contrato y rango, no la verdad del daño ni la calibración
de la confianza. El LLM es fijo y no es un clasificador entrenado.

## Diagramas
| Patrón/vista | Fuente | PNG |
|---|---|---|
| Strategy | [puml](strategy.puml) | [imagen](img/strategy.png) |
| Adapter | [puml](adapter.puml) | [imagen](img/adapter.png) |
| Factory por registro | [puml](factory.puml) | [imagen](img/factory.png) |
| Decorator | [puml](decorator.puml) | [imagen](img/decorator.png) |
| State | [puml](state.puml) | [imagen](img/state.png) |
| Observer | [puml](observer.puml) | [imagen](img/observer.png) |
| Chain of Responsibility | [puml](chain.puml) | [imagen](img/chain.png) |
| IA integrada | [puml](ia.puml) | [imagen](img/ia.png) |
| Secuencia | [puml](secuencia.puml) | [imagen](img/secuencia.png) |
| Clases actualizadas | [puml](../clases.puml) | [imagen](img/clases.png) |

Seis patrones GoF estrictos más fábrica por registro; supera el mínimo de cuatro.
Factory por registro no equivale al Factory Method GoF basado en herencia.

Reproducir con Java 17+ y PlantUML 1.2025.10 (JAR obtenido separadamente):
```bash
java -jar plantuml.jar -tpng -o img docs/design/patrones/*.puml
java -jar plantuml.jar -tpng -o patrones/img docs/design/clases.puml
```
Las fuentes usan Smetana para no requerir Graphviz. El ZIP no incluye el JAR.
En shells sin expansión de comodines, renderizar cada `.puml` con la extensión de VS Code.
