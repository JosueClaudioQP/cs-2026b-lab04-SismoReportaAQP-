#import "/components/@unsareport/epis-lab/lib.typ": lab-section

#lab-section("I. RESULTADOS")[
#set text(size: 11pt, hyphenate: false)
#show raw: set text(size: 11pt)
#set par(justify: true, leading: 0.55em, spacing: 0.65em)
#show heading: set text(size: 11pt, weight: "bold")
#show heading: set block(above: 0.9em, below: 0.5em)
SismoReporta AQP debe admitir *20 000 reportes en una hora* con conectividad móvil intermitente. Se mantiene el monolito modular del ADR-001 y el plazo de un mes. La propuesta se respalda con simulaciones, un prototipo SQLite y pruebas locales; los detalles reproducibles permanecen en los anexos.


== 1. Árbol de utilidad y escenarios (E1)


H/M/L expresa importancia y dificultad. Los escenarios de carga parten de ciudadanos que recuperan señal; los de persistencia suponen disco intacto. El resto especifica fallos de SMS, roles sin permiso y extensión de canales.


#block[
#set par(justify: false, leading: 0.45em)
#show table.cell.where(y: 0): set text(weight: "bold")
#table(columns: (1.1fr,3.3fr,0.45fr), inset: 5pt,
stroke: 0.4pt + rgb("999999"), align: left + top,
fill: (x,y) => if y == 0 { rgb("f1eeec") } else { none },
table.header([Escenario y atributo],[Respuesta y medida verificable],[I/D]),
[QA08-01 · Rendimiento],
[Persistir metadata y responder 202. p95 ≤ 2 s para 20 000 reportes, incluida reconexión en 300 s.],
[H/H],
[QA08-02 · Disponibilidad],
[Guardar offline; reiniciar cliente/servidor y reenviar tras ACK perdido. 0 pérdidas, duplicados y pendientes finales.],
[H/H],
[QA08-03 · Disponibilidad],
[SMS caído: conservar 1 asignación y 1 aviso pendiente; 0 asignaciones revertidas.],
[H/M],
[QA08-04 · Seguridad],
[Denegar asignaciones de ciudadano, brigadista, anónimo y lectura. 0 escrituras no autorizadas.],
[H/M],
[QA08-05 · Modificabilidad],
[Registrar 1 canal nuevo con 0 cambios en el servicio central.],
[M/L],
[QA08-06 · Rendimiento],
[Procesar la reconexión y vaciar pendientes ≤ 1 200 s después de la última llegada.],
[H/H]
)
]


*Prioridad corregida:* QA08-05 baja de H/H a M/L porque Lab07 ya implementa la fábrica por registro. QA08-01, 02 y 06 guían las primeras decisiones. Los seis componentes completos de cada escenario están en `docs/architecture/utilidad/escenarios.md`.


#figure(image("../assets/arbol.png", width: 100%, height: 260pt, fit: "contain"), caption: none)
Figura 1. Árbol de utilidad del caso SismoReporta AQP.


== 2. Tres iteraciones de ADD (E2 y E4)


Cada iteración revisa entradas, fija el objetivo, selecciona el elemento, compara conceptos, asigna responsabilidades, actualiza vistas y verifica resultados. Los siete pasos completos están en `docs/architecture/add/`.


#block[
#set par(justify: false, leading: 0.45em)
#show table.cell.where(y: 0): set text(weight: "bold")
#table(columns: (1fr,3.4fr), inset: 5pt,
stroke: 0.4pt + rgb("999999"), align: left + top,
fill: (x,y) => if y == 0 { rgb("f1eeec") } else { none },
table.header([Iteración],[Decisión, alternativa rechazada y trade-off]),
[1 · QA08-01/06],
[Inbox SQL y worker interno; metadata antes de fotos. Síncrono y 8 workers incumplen las ráfagas. Se descarta migrar a microservicios/Kafka por complejidad no justificada. Se acepta consistencia eventual.],
[2 · QA08-02/03],
[SQLite local + UUID estable; commit antes del ACK; asignación y outbox SMS atómicos. Se rechaza solo memoria porque no conserva pendientes al reiniciar. Mayor complejidad de estados y reintentos.],
[3 · QA08-04/05],
[RBAC en aplicación y puertos/Adapter. Se rechaza autorizar solo en UI. RLS queda pendiente hasta definir jurisdicciones. La autenticación fiable del rol sigue siendo necesaria.]
)
]


== 3. Evidencia de rendimiento


Se comparan 20 000 llegadas: uniforme en 3 600 s; ráfaga de 10 000 en 600 s y el resto en 3 000 s; estrés de reconexión con todas en 300 s. La última condición amplía lo exigido por la guía.


#block[
#set par(justify: false, leading: 0.45em)
#show table.cell.where(y: 0): set text(weight: "bold")
#table(columns: (1.05fr,1fr,1fr,1fr), inset: 5pt,
stroke: 0.4pt + rgb("999999"), align: left + top,
fill: (x,y) => if y == 0 { rgb("f1eeec") } else { none },
table.header([Perfil],[p95 síncrono 4 (ms)],[p95 síncrono 8 (ms)],[p95 ingesta 4 (ms)]),
[Uniforme],
[1 527,93],
[1 009,99],
[64,10],
[Ráfaga],
[719 486,91],
[77 889,50],
[64,12],
[Reconexión],
[2 323 421,77],
[1 019 274,16],
[72,87]
)
]


#figure(image("../assets/rendimiento-lab08.png", width: 100%), caption: none)
Figura 2. Comparación del p95; escala logarítmica.


*Supuestos:* servicio lognormal, CV 0,45; medias de 550 ms síncrono, 35 ms de ingesta y 120 ms por consumidor; 4 servidores lógicos de aceptación y 2 consumidores. Las 30 semillas varían llegadas, manteniendo la secuencia de servicio. El p95 extremo de ingesta varía entre *71,66 y 73,77 ms*. No es una medición del VPS ni un intervalo de confianza.


#block[
#set par(justify: false, leading: 0.45em)
#show table.cell.where(y: 0): set text(weight: "bold")
#table(columns: (1.6fr,2.8fr), inset: 5pt,
stroke: 0.4pt + rgb("999999"), align: left + top,
fill: (x,y) => if y == 0 { rgb("f1eeec") } else { none },
table.header([Sensibilidad],[Resultado del modelo]),
[Servicio medio 20 / 35 / 50 ms],
[p95: 37,27 / 72,87 / 172,13 ms; cumple.],
[Servicio medio 60 / 80 ms],
[p95: 2 786,23 / 94 257,30 ms; incumple.],
[Procesamiento tras reconexión],
[Drenaje: 898,28 s después de la última llegada; cumple el objetivo de 1 200 s.]
)
]


*Límite:* el modelo no reproduce contención de disco, locks, radio móvil, TLS ni fotos binarias. Un commit más lento puede invalidar la decisión; se requiere medir el endpoint real antes de campaña. ACEPTADO no significa PROCESADO.


== 4. Persistencia, disponibilidad y seguridad


#block[
#set par(justify: false, leading: 0.45em)
#show table.cell.where(y: 0): set text(weight: "bold")
#table(columns: (1.2fr,3.2fr), inset: 5pt,
stroke: 0.4pt + rgb("999999"), align: left + top,
fill: (x,y) => if y == 0 { rgb("f1eeec") } else { none },
table.header([Prueba],[Evidencia observada]),
[Offline + reinicio + replay],
[20 000 creados y persistidos; 2 858 ACK perdidos; 22 858 intentos; 0 pérdidas, duplicados y pendientes finales.],
[Proveedor SMS caído],
[La brigada B1 permanece asignada y hay 1 aviso pendiente. La falla no revierte la operación.],
[RBAC],
[4 clases de rol rechazadas sin cambiar brigada; coordinador permitido.],
[Canal nuevo],
[La prueba heredada registra CanalNuevo y obtiene ACEPTADO sin modificar el servicio central.]
)
]


El cliente retiene el reporte hasta ACK durable; un UUID repetido con contenido idéntico es idempotente y con contenido distinto es conflicto. El prototipo prueba ejecución secuencial, no pérdida física del disco ni concurrencia. El rol productivo debe proceder de una sesión verificada, nunca de un campo libre del cliente.


== 5. Modelo C4 y decisiones (E6)


#figure(image("../assets/contenedores.png", width: 100%, height: 330pt, fit: "contain"), caption: none)
Figura 3. Contenedores con trazabilidad a escenarios QA08; el worker permanece en el backend.


#block[
#set par(justify: false, leading: 0.45em)
#show table.cell.where(y: 0): set text(weight: "bold")
#table(columns: (1.2fr,3.2fr), inset: 5pt,
stroke: 0.4pt + rgb("999999"), align: left + top,
fill: (x,y) => if y == 0 { rgb("f1eeec") } else { none },
table.header([ADR propuesto],[Decisión y consecuencia]),
[006 · Ingesta durable],
[Inbox PostgreSQL reemplaza Redis como frontera del ACK. Las fotos se difieren; se enmiendan ADR-003/004 y se admite evidencia pendiente.],
[007 · Sincronización y SMS],
[SQLite local, UUID y outbox transaccional. Concreta ADR-005; el SMS puede duplicarse si se pierde su ACK externo.],
[008 · Autorización y puertos],
[Denegación por defecto, coordinador autorizado y extensión por contratos. No se declara validación de JWT, TLS o RLS.]
)
]


`workspace.dsl` pasó Structurizr CLI validate con salida 0 y exportó contexto, contenedores y componentes. El C4 anterior se conserva como histórico. Los ADR-006 a 008 requieren revisión de los integrantes.


== 6. ATAM-lite y riesgos (E3 y E7)


#block[
#set par(justify: false, leading: 0.45em)
#show table.cell.where(y: 0): set text(weight: "bold")
#table(columns: (1fr,3.4fr), inset: 5pt,
stroke: 0.4pt + rgb("999999"), align: left + top,
fill: (x,y) => if y == 0 { rgb("f1eeec") } else { none },
table.header([Hallazgo],[Evidencia y respuesta]),
[Sensibilidad],
[Servicio medio 35 → 60 ms: p95 72,87 → 2 786,23 ms. Medir el almacenamiento real.],
[Trade-off],
[Metadata antes de foto reduce espera, pero deja información temporalmente incompleta; indicar estado pendiente.],
[No riesgo acotado],
[El monolito cumple en el modelo; replay secuencial no duplica UUID. No se extiende la conclusión a todo el sistema.]
)
]


#block[
#set par(justify: false, leading: 0.45em)
#show table.cell.where(y: 0): set text(weight: "bold")
#table(columns: (1.4fr,0.45fr,2.55fr), inset: 5pt,
stroke: 0.4pt + rgb("999999"), align: left + top,
fill: (x,y) => if y == 0 { rgb("f1eeec") } else { none },
table.header([Riesgo],[P×I],[Tratamiento propuesto]),
[R1 · Host/disco único],
[10],
[Aceptar residual en MVP; copia externa y restauración antes de despliegue.],
[R2 · Commit lento],
[16],
[Medir I/O; limitar admisión y conservar pendientes locales.],
[R3 · Backlog],
[16],
[Monitorear edad del pendiente; objetivo de drenaje 20 min.],
[R4 · Rol manipulado],
[15],
[Verificar firma, expiración y audiencia; no confiar en JSON.],
[R5 · Foto sin sincronizar],
[9],
[Estado pendiente, reintento y alerta a las 24 h.],
[R6 · SMS duplicado],
[6],
[Aceptar residual; idempotencia del proveedor si está disponible.],
[R7 · Borrado del móvil],
[10],
[Mantener pendientes hasta ACK y evitar borrado automático.]
)
]


P e I son escalas ordinales 1–5; producto ≥ 10 crítico, 5–9 moderado. Es *autoevaluación asistida*: falta el issue real emitido/recibido de otro grupo. No se atribuyen estos hallazgos a evaluadores externos.


== 7. Fitness functions y bitácora IA (E5 y E7)


#block[
#set par(justify: false, leading: 0.45em)
#show table.cell.where(y: 0): set text(weight: "bold")
#table(columns: (1.2fr,3.2fr), inset: 5pt,
stroke: 0.4pt + rgb("999999"), align: left + top,
fill: (x,y) => if y == 0 { rgb("f1eeec") } else { none },
table.header([Verificación],[Degradación detectada]),
[FF-01 / FF-02],
[Dependencia dominio → aplicación e imports concretos en aplicación. 2 contratos conservados.],
[FF-03 / FF-07],
[p95 de ingesta \> 2 s o drenaje \> 20 min en el modelo.],
[FF-04 / FF-05],
[Pérdidas/duplicados tras replay o reversión de asignación por SMS fallido.],
[FF-06],
[Escrituras de roles no autorizados.]
)
]


*Resultado:* 130 pruebas aprobadas. En la rama aislada `prueba-violacion-e5`, importar un adaptador desde Ingesta produjo FF-02 BROKEN (salida 1); retirarlo restauró 2 contratos conservados (salida 0). El workflow está preparado, pero no ejecutado remotamente. Los contratos abarcan `sismo_lab08`, no todo el código heredado.


#block[
#set par(justify: false, leading: 0.45em)
#show table.cell.where(y: 0): set text(weight: "bold")
#table(columns: (1.15fr,3.25fr), inset: 5pt,
stroke: 0.4pt + rgb("999999"), align: left + top,
fill: (x,y) => if y == 0 { rgb("f1eeec") } else { none },
table.header([Revisión con IA],[Verificación y resolución]),
[Caso y antecedentes],
[El usuario confirmó SismoReporta. El remoto 529b7b6 refutó el falso positivo de que faltaban ADR-005 y C4.],
[Prioridad y carga],
[Se bajó extensibilidad a M/L y se rechazó dimensionar solo con 5,56 req/s: la ráfaga síncrona llega a p95 ≈ 719 s.],
[ACK y persistencia],
[Se separó ACEPTADO de PROCESADO; UUID no sustituye almacenamiento durable. Se contrastó con replay y reinicios.],
[Entrega],
[Se distinguieron pruebas locales, evaluación cruzada y publicación remota; no se inventaron issues ni Actions en verde.]
)
]


La bitácora completa conserva siete puntos de análisis de esta sesión, incluidos el falso positivo y sus correcciones. Los anexos incluyen escenarios de seis partes, iteraciones, ADR, C4, riesgos y logs. Pendientes externos: evaluación cruzada, revisión de ambos integrantes, PR, Actions en verde, tag `v0.8-arquitectura` y envío al aula.


== Fuentes principales


Guía Lab08 de Construcción de Software, UNSA, 2026-B; #link("https://github.com/JosueClaudioQP/cs-2026b-lab04-SismoReportaAQP-")[repositorio del grupo], commit 529b7b6; recursos docentes AgroConecta como referencia metodológica; Kazman, Klein y Clements (2000), #link("https://insights.sei.cmu.edu/library/atam-method-for-architecture-evaluation/")[ATAM]. Las fuentes y archivos de reproducción completos acompañan el paquete.

]

