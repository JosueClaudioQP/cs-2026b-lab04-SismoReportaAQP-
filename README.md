# Diseño de la arquitectura (Lab 08)

**Integrantes:** Josue Claudio Quispe Paucar y Diego Alejandro Carbajal Gonzales.

Caso 8: SismoReporta AQP. Base remota: commit 529b7b6214954df22134274fd611543c9ed3b3e8. Esta carpeta conserva los Labs04-07 y agrega un paquete de experimentos aislado en src/sismo_lab08. No reemplaza silenciosamente la implementación previa de reportes.

|Iteración|Escenarios|Táctica|Evidencia local|¿Cumple?|
|---|---|---|---|---|
|1|QA08-01/06|Ingesta durable, fotos diferidas, worker interno|p95 extremo 72,87 ms; drenaje 898,28 s|Sí en el modelo; VPS sin medir|
|2|QA08-02/03|SQLite local, UUID e inbox/outbox|20 000 persistidos; 0 pérdidas/duplicados; SMS no revierte|Sí en el prototipo secuencial|
|3|QA08-04/05|RBAC, puertos, fábrica por registro|4 roles rechazados y canal extensible probado|Sí en política local; JWT sin integrar|

- [Árbol de utilidad](docs/architecture/utilidad/arbol.png) y [escenarios de seis partes](docs/architecture/utilidad/escenarios.md).
- [Iteración 1](docs/architecture/add/iteracion-1.md), [iteración 2](docs/architecture/add/iteracion-2.md), [iteración 3](docs/architecture/add/iteracion-3.md).
- [ADR-006](docs/architecture/adr/006-ingesta-durable.md), [ADR-007](docs/architecture/adr/007-sincronizacion-y-sms.md), [ADR-008](docs/architecture/adr/008-autorizacion-y-puertos.md).
- [ATAM-lite](docs/architecture/atam-lite.md), [bitácora IA](docs/architecture/bitacora-ia-lab08.md), [C4](docs/architecture/c4/workspace.dsl).
- [Resultados](docs/architecture/evidencia/resultados.json), logs de [tests](docs/architecture/pytest-lab08.txt) y [contratos](docs/architecture/lint-lab08.txt).

## Reproducir
Python 3.12. En la raíz:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-lab08.txt
$env:PYTHONPATH="src;."
lint-imports --no-cache
python -m pytest -v
python tools/medir_lab08.py
```
En Linux: `export PYTHONPATH=src:.`. Logs conservan los resultados de Windows del 31/10/2026. Los tiempos de servicio de simulación son supuestos, no mediciones productivas. Las 30 semillas cambian las llegadas; la secuencia de servicio se mantiene fija para comparar alternativas.

## Estado de entrega E3 / E8
Workflow preparado: [.github/workflows/fitness.yml](.github/workflows/fitness.yml). Insignia para usar después de subirlo:

![fitness-functions](https://github.com/JosueClaudioQP/cs-2026b-lab04-SismoReportaAQP-/actions/workflows/fitness.yml/badge.svg)

Los entregables del Lab08 se publican directamente en main por solicitud del usuario. El workflow se ejecuta al hacer push; su resultado debe verificarse en Actions. Falta la evaluación cruzada real y los PR individuales de cada integrante; la autoevaluación no los sustituye. No se ha enviado el informe al Aula Virtual. La etiqueta v0.8-arquitectura queda pendiente hasta la revisión final.

## Fitness y alcance
FF-01/02 controlan el paquete experimental sismo_lab08, no todo el código heredado. FF-03 p95, FF-04 persistencia/replay, FF-05 SMS, FF-06 RBAC y FF-07 drenaje. Los tests heredados de Lab07 también se ejecutan. Ver docs/architecture/evidencia/violacion-ff02.txt y violacion-revertida.txt.


## Antecedentes

El README histórico de los Labs04-07 se conserva en [README-Labs04-07.md](README-Labs04-07.md), con sus créditos originales.


## Informe con plantilla UNSAReport

Fuente editable: [informe-typst/lab-08/main.typ](informe-typst/lab-08/main.typ). Para recompilar consulta [informe-typst/LEEME.md](informe-typst/LEEME.md).

