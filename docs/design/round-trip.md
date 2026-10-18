# Round-trip (E6) – SismoReporta AQP

Ingeniería directa: `clases.puml` → `src/reportes/dominio.py` (IA, Python 3.10, dataclasses + ABC).
Ingeniería inversa: `pyreverse -o puml -p reportes src/reportes` → `classes_reportes_pyreverse.puml` / `img/classes_reportes.png`.

| # | Diferencia observada | Causa | Acción |
|---|---|---|---|
| 1 | No aparecen la composición Reporte–Evidencia ni la asociación Reporte–Brigada; las evidencias figuran como atributo `list[Evidencia]`. | pyreverse no infiere asociaciones desde colecciones tipadas ni desde `X \| None`. | Documentar la limitación; el diagrama de diseño se mantiene. |
| 2 | No hay multiplicidades. | El código no las expresa. | `Reporte.reintentar()`/`marcar_atendido()` validan reglas (brigada requerida); documentar. |
| 3 | `ColaReportes` y `RepositorioReportes` salen como clases, no como `<<puerto>>`; `ColaPersistenteAdapter` aparece con operaciones abstractas. | Python usa ABC; el adaptador lanza `NotImplementedError`. | Aceptable en Python; se documenta. |
| 4 | Faltan `SyncManager`, `ApiController`, `ServicioIngesta`, `WorkerProcesamiento` y `ServicioOperaciones`. | El esqueleto generado cubre solo el dominio y los puertos. | Corregir: pedir a la IA esas clases y regenerar (pendiente). |
| 5 | Nombres en snake_case (`marcar_recibido`) frente a camelCase en el diagrama; `tamano_bytes` vs `tamanoBytes`. | Convención de Python. | Documentar equivalencia (C5). |
