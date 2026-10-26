# E1. Olores, patrones y decisiones propuestas para revisión del equipo

Baseline: `src/reportes/antes/servicio.py`, creado para este experimento a partir
 del flujo del Lab 05. Ver `alcance` en README de esta carpeta.

| Olor concreto | Ubicación antes | Propuesta | SOLID | Decisión y prueba |
|---|---|---|---|---|
| if/elif por canal | sincronizar | Strategy | OCP/DIP | Adoptado. `test_open_closed_nuevo_canal_por_registro` agrega NUEVO sin editar servicio |
| Servicio conoce JSON y dos SDK | sincronizar | Adapter | DIP/ISP | Adoptado. `test_adapters_equivalentes_y_payload` compara aceptación y contenido |
| Construcción acoplada a variantes | __init__ / sincronizar | Factory por registro | OCP/DIP | Adoptado como fábrica simple; misma prueba Open/Closed |
| Bucles repetidos para TimeoutError | sincronizar | Decorator | SRP/OCP | Adoptado. `test_dos_timeouts_y_exito` y `test_decorator_no_reintenta_error_de_programacion` |
| Condicionales de estado dispersos | Reporte | State | SRP/OCP | Adoptado. `test_state_matriz_completa` y ciclo de vida |
| Avisos al panel y auditoría a mano | sincronizar | Observer | SRP/OCP | Adoptado. `test_observer_tercer_suscriptor` |
| Generación, parsing y validación mezclados | sugerir_severidad | Strategy + Adapter + Chain | SRP/DIP | Adoptados. proveedor local intercambiable y respuestas inválidas bloqueadas |
| Caché incrustada en servicio | sugerir_severidad | Decorator | SRP/OCP | Adoptado. `test_cache_ia` y `test_cache_no_guarda_excepciones` |
| Propuesta de compartir fábrica/LLM globalmente | alternativa examinada en esta asistencia | Singleton | DIP perjudicado | **Rechazado**: instancia global mezcla cachés y registros de pruebas. Inyectar dependencias es suficiente |
| Familias de objetos sin variación conjunta | alternativa examinada | Abstract Factory | Simplicidad | **Rechazado**: no hay familias completas de productos; registro basta |

Las decisiones se entregan como propuesta técnica revisada mediante pruebas;
no se atribuye una aprobación o revisión humana aún no realizada.
