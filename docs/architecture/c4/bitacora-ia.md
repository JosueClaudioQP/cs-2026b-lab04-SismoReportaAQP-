# Bitácora de IA – Lab 06 (SismoReporta AQP)

> Regla de oro: la IA propone, el equipo decide y verifica. Herramienta: Claude (sesión del 17/10/2026).

| N.º | Fecha | Herramienta | Prompt (resumen) | Propuesta | Verificación | Decisión |
|---|---|---|---|---|---|---|
| IA-11 | 17/10/2026 | Claude | Prompt IA 1: borrador de `workspace.dsl` a partir de inventario, ADR-001/002/003 y `despliegue.puml` | Modelo con 3 personas, 2 sistemas externos, 7 contenedores, 4 componentes, vista dinámica y despliegue | `structurizr validate` sin errores; worker modelado como componente (ADR-003) y Docker Compose/Nginx como nodos de despliegue, no contenedores | Aceptada con correcciones |
| IA-12 | 17/10/2026 | Claude | Revisar las imágenes exportadas | Se detectó numeración duplicada en la vista dinámica ("1: 1.") por numerar a mano | Se quitó la numeración manual y se re-exportó | Corregida |
| IA-13 | 17/10/2026 | Claude | Verificar coherencia del C4 con Lab 04 y Lab 05 | Contradicción: `despliegue.puml` hace que el worker guarde fotos, pero ADR-003 prohíbe fotos binarias en la cola; nombre "Procesamiento asíncrono" ≠ paquete `procesamiento` | ADR-004 define que Ingesta guarda la foto en MinIO y la cola solo lleva la referencia; componente renombrado | Corregida (artefacto equivocado: E6 del Lab 04) |
| IA-14 | 17/10/2026 | Claude | Prompt IA 2: auditor con la lista oficial | 8 relaciones sin tecnología y flechas duplicadas en despliegue | Las 8 son falso positivo (persona→sistema y llamadas en proceso); las flechas duplicadas se documentaron | Aceptada con falso positivo |
| IA-15 | 17/10/2026 | Claude | Prompt IA 3: explicación para público no técnico (máx. 120 palabras) | Texto de 109 palabras | Verificado contra el modelo: usuarios, 2 externos, SMS, offline | Aceptada |
| IA-16 | 17/10/2026 | Claude | Decidir cómo notificar al brigadista y cómo persistir datos | ADR-004 (PostgreSQL + MinIO) y ADR-005 (SMS) | Revisadas contra R-01/R-02 y las decisiones de la bitácora del Lab 04 (IA-04, IA-05) | Aceptada |
