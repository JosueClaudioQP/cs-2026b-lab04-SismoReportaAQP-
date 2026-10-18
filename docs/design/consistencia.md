# Consistencia C1–C5 (E7) – SismoReporta AQP

Revisión de los cinco diagramas (clases, secuencia, estados, actividades, paquetes).

| Regla | Elemento | Hallazgo | Verificación / corrección |
|---|---|---|---|
| C1 | Secuencia: todos los mensajes a `SyncManager`, `ApiController`, `ServicioIngesta`, `ColaReportes`, `WorkerProcesamiento`, `Reporte`, `RepositorioReportes` | Todas las operaciones existen en `clases.puml`. | Cumple. |
| C1 | Mensaje `Q ->> W : procesar()` | La cola no invoca al worker; según ADR-003 el worker consume (pull). | Simplificación aceptada para mostrar el mensaje asíncrono; documentada. |
| C2 | Estados: `[*] --> BORRADOR : registrar()` | `registrar()` es de `SyncManager`, no de `Reporte`. | Corregido: etiqueta `SyncManager.registrar()`. |
| C2 | Demás transiciones (`encolar`, `reintentar`, `marcarRecibido`, `verificar`, `marcarAtendido`) | Existen en `Reporte`. | Cumple. |
| C3 | `Reporte 1 *-- 0..* Evidencia`; `Reporte 0..* -- 0..1 Brigada` | Una foto es opcional (RF-02 no fija mínimo ni máximo). | Cumple; no se asume un máximo de 3. |
| C4 | Paquetes: `ingesta`, `operaciones`, `procesamiento` → `compartido` | Sin ciclos; módulos solo se comunican por puertos/cola (ADR-001, ADR-003). | Cumple. |
| C5 | Estados del enum = estados del Mermaid; `timestamp_dispositivo`/`timestamp_servidor` como en ADR-002 | Python usa snake_case. | Equivalencia documentada en `round-trip.md`. |
| C1 | **Falso positivo de la IA:** el chequeo automático (Prompt IA 3) marcó el mensaje `Ciudadano -> App móvil : Crea reporte (sin señal)` por no ser una operación de ninguna clase. | Es una interacción humana con la interfaz, no una llamada entre clases; la regla C1 aplica a mensajes entre objetos del diagrama de clases. Se rechaza el hallazgo (14 mensajes revisados, 1 marcado). |
