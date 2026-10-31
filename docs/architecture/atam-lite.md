# ATAM-lite: autoevaluación asistida, no evaluación cruzada recibida

No se proporcionó issue ni evidencia de otro grupo. Los siguientes son hallazgos propios para preparar E3; no se atribuyen a evaluadores externos. La revisión cruzada y su respuesta siguen pendientes.

## Hallazgos y respuesta propuesta
- S1 Sensibilidad: duración del commit. En reconexión, pasar de media de 35 a 60 ms cambia p95 de 72,87 a 2786,23 ms. Aceptar hallazgo y exigir prueba real del almacenamiento.
- S2 Sensibilidad: consumidores internos. Con 2 y servicio medio 120 ms, el drenaje posterior dura 898,28 s; una menor capacidad puede incumplir QA08-06. Medir age_of_oldest y backlog.
- T1 Trade-off: ACK temprano mejora disponibilidad, pero el reporte y sus fotos pueden ser temporalmente incompletos. Exponer estado EVIDENCIA_PENDIENTE y no presentarlo como verificado.
- T2 Trade-off: SQLite/inbox aumenta durabilidad y reduce pérdida por reinicio, pero añade escrituras y compite por disco con consultas.
- NR1 No riesgo acotado: en el modelo de tres perfiles, un monolito con ingesta durable cumple p95 ≤ 2 s; no se justifica migrar a microservicios solo por 20 000/h.
- NR2 No riesgo acotado: perder el ACK no duplica UUID en el prototipo SQLite secuencial. No se extiende a carreras concurrentes o pérdida de disco.

## Matriz de riesgos
Escalas ordinales 1 a 5; producto ≥ 10 crítico, 5 a 9 moderado, ≤ 4 bajo. Son juicios de diseño, no probabilidades medidas.

|ID|Riesgo|P|I|P×I|Zona|Tratamiento|
|---|---|---|---|---|---|---|
|R1|Host único / disco destruido|2|5|10|Crítico|Aceptar residual en MVP; copia externa diaria y simulacro de restauración antes de despliegue. La copia aún no se ejecutó.|
|R2|Disco lento: commit medio ≥ 60 ms|4|4|16|Crítico|Medir p95 en VPS, limitar admisión con 429/Retry-After y mantener pendientes locales; reservar IOPS. Gate antes de campaña.|
|R3|Cola interna crece tras reconexión|4|4|16|Crítico|Medir edad del pendiente; objetivo drenaje 20 min; priorizar metadata y aplicar backpressure. Modelo: 898 s.|
|R4|Token/rol manipulado en frontera HTTP|3|5|15|Crítico|Verificar firma, expiración y audiencia; no confiar en rol del JSON; pruebas de integración antes de exponer API.|
|R5|Foto pendiente nunca sincronizada|3|3|9|Moderado|Estado explícito, reintento y alerta a las 24 h; no impedir recepción de metadata; validación visual pendiente.|
|R6|SMS repetido por ACK externo perdido|3|2|6|Moderado|Aceptar residual para MVP; usar clave de idempotencia si proveedor la ofrece y mostrar asignación en panel.|
|R7|Borrado de datos de móvil antes de sincronizar|2|5|10|Crítico|Aviso visible de pendientes y confirmación de ACK; fuera de garantía ante pérdida física. Evitar borrado automático.|

Responsables propuestos: ambos integrantes revisan R1/R2/R3 antes de desplegar; Diego integra validación de frontera HTTP (R4) y Josue revisa protocolo offline (R5/R7), sujeto a acuerdo del equipo. No se afirma que estas tareas se hayan ejecutado.

## Para cerrar E3
Registrar URL del issue recibido y emitido, equipo evaluador, fecha, hallazgo original y aceptación/refutación con resultados. No sustituir este requisito por la autoevaluación con IA.
