# ADR-006: Patrones para sincronización y sugerencia de severidad (Lab 07)

- Estado: Propuesto; implementación experimental verificada, pendiente de revisión del equipo.
- Fecha: 25/10/2026.
- Decisores: equipo SismoReporta AQP, por confirmar en revisión cruzada.
- Trazabilidad: E8 del Lab 07 pide ADR-005; el repositorio ya usa ADR-005 para SMS.
  Se asigna ADR-006 para no sobrescribir una decisión existente. Este archivo
  satisface el contenido de ese entregable con numeración consecutiva.

## Contexto
RF-04 requiere guardar y reenviar reportes cuando regresa la señal. El Lab 05
modela BORRADOR, ENCOLADO, RECIBIDO, VERIFICADO y ATENDIDO. El código existente
es un esqueleto, por lo que E1 necesita una baseline simulada ejecutable.
Hay dos APIs de ingreso con contratos distintos, reintentos repetidos, avisos
acoplados y validaciones de IA mezcladas. Los SDK son falsos para evitar red/costo.
La IA debe sugerir severidad, sin sustituir la revisión del operador.

## Alternativas consideradas
1. Mantener condicionales y avisos incrustados: menos archivos, mayor acoplamiento.
2. Aplicar patrones solo donde hay variación comprobable: elegida para el experimento.
3. Singleton, Abstract Factory y Command indiscriminados: rechazados por complejidad
   y ausencia de necesidad adicional demostrada en este alcance.

## Decisión
- Strategy: CanalEnvio y ProveedorLLM permiten implementaciones sustituibles.
- Adapter: normaliza SDK regional/alterno y clientes LLM.
- Factory por registro: construye el canal; no se presenta como Factory Method GoF estricto.
- State: cada estado habilita solo las transiciones del Lab 05.
- Observer: evento de aceptación con panel y auditoría como dos suscriptores.
- Decorator: reintenta solo TimeoutError (tres intentos) y añade caché de IA.
- Chain of Responsibility: JSON y longitud, esquema/severidad y confianza finita 0..1.
- Un 202 elimina el pendiente local simulado; RECIBIDO se alcanza al procesar.
- Un UUID repetido tiene aceptación idempotente en el doble de servidor.
- Las sugerencias siempre requieren revisión y nunca mutan nivel_danio ni estado.

## Consecuencias positivas
Pruebas de caracterización idénticas en ambas versiones, extensibilidad sin
editar el método coordinador y transiciones inválidas rechazadas. Se evita la
dependencia de red y claves en CI. La complejidad máxima por método baja de 13 a 5.

## Consecuencias negativas y límites
SLOC aumenta de 95 a 230. Hay más archivos y objetos. Estado y eventos son en
memoria; no hay garantías de entrega, durabilidad o concurrencia. La caché sin TTL
sirve solo al laboratorio. El Observer síncrono no aísla fallas de suscriptores.
La validación de IA no demuestra exactitud de la severidad. La separación de
patrones no equivale a escalabilidad ni acredita los 20 000 reportes/hora.

## Relación con decisiones previas
ADR-001 conserva el monolito; ADR-002 y ADR-003 siguen siendo la arquitectura
objetivo de almacenamiento offline/cola. ADR-004 y ADR-005 no se implementan aquí
como PostgreSQL/MinIO/SMS reales. La simulación agrega una variación de canal para
E2 sin cambiar el despliegue C4. Un futuro adaptador debe incorporar persistencia,
ACK recuperable y restricción UUID única antes de considerar producción.

## Evidencias
[Pruebas y métricas](../../design/patrones/README.md),
[olores](../../design/patrones/olores.md) y
[bitácora](../../design/patrones/bitacora-ia.md).
