# E6. Métricas y trade-off

Entorno medido: Python 3.12.14, radon 6.0.1, pytest 9.1.1.
Reproducir: `python tools/medir_lab07.py` desde la raíz.

## Alcance y criterio de comparación
Se comparan TODOS los archivos de `src/reportes/antes/` y `src/reportes/despues/`.
Ambas versiones soportan el mismo contrato observable de envío, estados y sugerencia IA.
Se excluyen de ambas las pruebas, los SDK simulados, `datos_lab07.py` y el esqueleto Lab 05.
Esas dependencias comunes no se trasladaron de antes a después para ocultar complejidad.
El promedio de Radon incluye clases y métodos; también se informa el promedio solo de métodos.
El incremento de clases puede reducir el promedio: por eso se publica máximo, SLOC y detalle.

| Indicador | Antes | Después |
|---|---:|---:|
| SLOC | 95 | 230 |
| Bloques Radon (clases + métodos) | 12 | 81 |
| CC promedio Radon | 4.25 | 1.83 |
| Métodos/funciones | 10 | 54 |
| CC promedio solo métodos | 4.10 | 1.48 |
| CC máxima de un método | 13 | 5 |

## Trade-off (7 líneas)
1. La sincronización pasa de CC 11 a 4 al separar selección, traducción y reintentos.
2. El método de IA pasa de CC 13 a 1 en la fachada; la lógica continúa en los guardrails (no desaparece).
3. Los nuevos canales se registran sin cambiar el algoritmo del servicio, como prueba el test Open/Closed.
4. El costo es más SLOC, objetos y archivos, con mayor esfuerzo de navegación y aprendizaje.
5. Las mismas pruebas protegen resultados, errores, eventos y reintentos antes y después.
6. Para un único canal estable, sin IA ni cambios de estado complejos, la versión inicial podría bastar.
7. Se justifica aquí por las variaciones del laboratorio; estas métricas no prueban rendimiento ni exactitud de IA.

## Patrón rechazado
Singleton para fábricas/LLM: no hay necesidad de instancia global y contaminaría registros y cachés entre pruebas.
También se descarta Abstract Factory: no hay familias completas de productos relacionados.
La Factory por registro es simple, no se contabiliza como Factory Method GoF estricto.

## Complejidad por método (todos)
| Versión | Archivo | Método | CC | Rango |
|---|---|---|---:|---|
| antes | servicio.py | `Reporte.encolar` | 2 | A |
| antes | servicio.py | `Reporte.reintentar` | 2 | A |
| antes | servicio.py | `Reporte.marcar_recibido` | 2 | A |
| antes | servicio.py | `Reporte.verificar` | 2 | A |
| antes | servicio.py | `Reporte.marcar_atendido` | 3 | A |
| antes | servicio.py | `ServicioReportes.__init__` | 4 | A |
| antes | servicio.py | `ServicioReportes.registrar` | 1 | A |
| antes | servicio.py | `ServicioReportes.sincronizar` | 11 | C |
| antes | servicio.py | `ServicioReportes.procesar` | 1 | A |
| antes | servicio.py | `ServicioReportes.sugerir_severidad` | 13 | C |
| despues | estados.py | `Estado.encolar` | 1 | A |
| despues | estados.py | `Estado.reintentar` | 1 | A |
| despues | estados.py | `Estado.marcar_recibido` | 1 | A |
| despues | estados.py | `Estado.verificar` | 1 | A |
| despues | estados.py | `Estado.marcar_atendido` | 1 | A |
| despues | estados.py | `Borrador.encolar` | 1 | A |
| despues | estados.py | `Encolado.reintentar` | 1 | A |
| despues | estados.py | `Encolado.marcar_recibido` | 1 | A |
| despues | estados.py | `Recibido.verificar` | 1 | A |
| despues | estados.py | `Verificado.marcar_atendido` | 2 | A |
| despues | eventos.py | `Suscriptor.actualizar` | 1 | A |
| despues | eventos.py | `Publicador.__init__` | 1 | A |
| despues | eventos.py | `Publicador.suscribir` | 1 | A |
| despues | eventos.py | `Publicador.publicar` | 2 | A |
| despues | eventos.py | `PanelObserver.__init__` | 1 | A |
| despues | eventos.py | `PanelObserver.actualizar` | 1 | A |
| despues | eventos.py | `AuditoriaObserver.__init__` | 1 | A |
| despues | eventos.py | `AuditoriaObserver.actualizar` | 1 | A |
| despues | ia.py | `ProveedorLLM.completar` | 1 | A |
| despues | ia.py | `LLMAdapter.__init__` | 1 | A |
| despues | ia.py | `LLMAdapter.completar` | 1 | A |
| despues | ia.py | `LocalAdapter.__init__` | 1 | A |
| despues | ia.py | `LocalAdapter.completar` | 1 | A |
| despues | ia.py | `ConCache.__init__` | 1 | A |
| despues | ia.py | `ConCache.completar` | 2 | A |
| despues | ia.py | `Guardrail.__init__` | 1 | A |
| despues | ia.py | `Guardrail.validar` | 2 | A |
| despues | ia.py | `Guardrail.aplicar` | 1 | A |
| despues | ia.py | `FormatoJSON.aplicar` | 4 | A |
| despues | ia.py | `SeveridadPermitida.aplicar` | 5 | A |
| despues | ia.py | `ConfianzaValida.aplicar` | 4 | A |
| despues | ia.py | `ClasificadorSeveridad.__init__` | 1 | A |
| despues | ia.py | `ClasificadorSeveridad.sugerir` | 2 | A |
| despues | modelo.py | `Reporte.estado` | 1 | A |
| despues | modelo.py | `Reporte.encolar` | 1 | A |
| despues | modelo.py | `Reporte.reintentar` | 1 | A |
| despues | modelo.py | `Reporte.marcar_recibido` | 1 | A |
| despues | modelo.py | `Reporte.verificar` | 1 | A |
| despues | modelo.py | `Reporte.marcar_atendido` | 1 | A |
| despues | servicio.py | `ServicioReportes.__init__` | 5 | A |
| despues | servicio.py | `ServicioReportes.registrar` | 1 | A |
| despues | servicio.py | `ServicioReportes.sincronizar` | 4 | A |
| despues | servicio.py | `ServicioReportes.procesar` | 1 | A |
| despues | servicio.py | `ServicioReportes.sugerir_severidad` | 1 | A |
| despues | transporte.py | `CanalEnvio.enviar` | 1 | A |
| despues | transporte.py | `RegionalAdapter.__init__` | 1 | A |
| despues | transporte.py | `RegionalAdapter.enviar` | 1 | A |
| despues | transporte.py | `AlternaAdapter.__init__` | 1 | A |
| despues | transporte.py | `AlternaAdapter.enviar` | 1 | A |
| despues | transporte.py | `FabricaCanales.__init__` | 1 | A |
| despues | transporte.py | `FabricaCanales.registrar` | 1 | A |
| despues | transporte.py | `FabricaCanales.crear` | 2 | A |
| despues | transporte.py | `ConReintentos.__init__` | 2 | A |
| despues | transporte.py | `ConReintentos.enviar` | 3 | A |

Salidas crudas: [evidencias/](evidencias/). MI se conserva como dato complementario; no se usa para afirmar calidad absoluta.
