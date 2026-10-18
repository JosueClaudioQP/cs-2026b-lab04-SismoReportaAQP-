# Bitácora de IA – Lab 05 (SismoReporta AQP)

> Regla de oro: la IA propone, el equipo decide y verifica. Herramienta: Claude (sesión del 17/10/2026).

| N.º | Fecha | Herramienta | Prompt (resumen) | Propuesta | Verificación | Decisión |
|---|---|---|---|---|---|---|
| IA-06 | 17/10/2026 | Claude | Generar borradores E1–E7 para el Caso 8 a partir de la guía y del Lab 04 | Historia HU-08, clases, secuencia, estados, actividades, paquetes, round-trip | Revisado con C1–C5 (ver `consistencia.md`); se corrigió `registrar()` en estados | Aceptada con correcciones |
| IA-07 | 17/10/2026 | Claude | Prompt IA 1: diagrama de clases desde la historia y el ADR-001 | 9 clases, 2 puertos, 2 enumeraciones | Composición Reporte–Evidencia `1` a `0..*` (RF-02 no fija máximo de fotos); sin datos personales en atributos (C3, C5) | Aceptada con correcciones |
| IA-08 | 17/10/2026 | Claude | Prompt IA 2: ingeniería directa a Python | `src/reportes/dominio.py` (dataclasses y ABC) | `pyreverse` mostró 5 diferencias (ver `round-trip.md`); se agregó `servicios.py` y se repitió la ingeniería inversa | Aceptada con correcciones |
| IA-09 | 17/10/2026 | Claude | Prompt IA 3: auditor de consistencia C1–C5 | 1 hallazgo en C1 | Falso positivo: interacción humano–interfaz (ver `consistencia.md`) | Aceptada con falso positivo |
| IA-10 | 17/10/2026 | Claude | Revisión de la etiqueta de transición inicial del diagrama de estados | `registrar()` no es operación de `Reporte` | Corregida a `SyncManager.registrar()` | Corregida |
