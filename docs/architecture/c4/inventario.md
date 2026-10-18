# Inventario de elementos – SismoReporta AQP (Lab 06)

| Elemento | Tipo C4 | Origen |
|---|---|---|
| Ciudadano, Operador / Coordinador de Defensa Civil, Brigadista | Persona | README.md (actores clave) y `docs/architecture/drivers.md` (Lab 04) |
| SismoReporta AQP | Sistema de software | Caso 8 |
| Servicio de mapas | Sistema externo | `arquitectura.mmd` (Lab 04) |
| Servicio de mensajería SMS | Sistema externo | `actividades-priorizar-asignar.puml` (Lab 05: "Notifica al brigadista") y pistas de la guía; ADR-005 |
| Aplicación móvil (Flutter / React Native) | Contenedor | ADR-002, `despliegue.puml` (Lab 04) |
| Almacenamiento local (SQLite) | Contenedor | ADR-002 |
| Panel web de operaciones | Contenedor | `arquitectura.mmd` (Lab 04) |
| Backend SismoReporta (monolito modular, Python / FastAPI) | Contenedor | ADR-001, ADR-003, `despliegue.puml` |
| Cola persistente (Redis 7, AOF) | Contenedor | ADR-003, `despliegue.puml` |
| Base de datos (PostgreSQL 16 + PostGIS) | Contenedor | ADR-004 (formaliza IA-04 de la bitácora del Lab 04) |
| Almacenamiento de evidencia (MinIO) | Contenedor | ADR-004 |
| Nginx, Prometheus, Grafana | Nodo de infraestructura (despliegue) | `despliegue.puml` (Lab 04) |
| Módulos Ingesta, Operaciones, Procesamiento, Compartido | Componente (del backend) | `docs/design/paquetes.puml` (Lab 05) |
| Flujo "enviar un reporte sin señal y sincronizarlo" | Vista dinámica | `secuencia-sincronizar-reporte.puml` (Lab 05) |

Nota: el worker NO es un contenedor aparte; el ADR-003 lo mantiene dentro del artefacto del monolito, por eso es el componente "Módulo Procesamiento".
