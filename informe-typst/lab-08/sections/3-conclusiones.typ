#import "/components/@unsareport/epis-lab/lib.typ": lab-section

#lab-section("III. CONCLUSIONES")[
#set text(size: 11pt, hyphenate: false)
#show raw: set text(size: 11pt)
#set par(justify: true, leading: 0.55em, spacing: 0.65em)
#show heading: set text(size: 11pt, weight: "bold")
#show heading: set block(above: 0.9em, below: 0.5em)
- El monolito modular sigue siendo viable *dentro del modelo*: la ingesta durable cumple el p95 y el drenaje definidos sin justificar una migración a microservicios.

- La persistencia y el protocolo de ACK recuperan 20 000 registros con 2 858 reenvíos sin pérdidas ni duplicados en el prototipo secuencial. La prueba no cubre destrucción física del disco.

- La asignación debe confirmarse independientemente del aviso SMS, y la autorización debe verificarse antes de escribir. Los puertos facilitan extensión sin acoplar proveedores.

- La principal validación pendiente es el servidor real: a 60 ms medios de ingesta el modelo incumple. Antes de desplegar se deben medir I/O y endpoint, revisar autenticación y probar restauración.

- Los entregables se publicaron en main y GitHub Actions aprobó las pruebas y la validación C4. Faltan la evaluación cruzada, los PR individuales, la revisión de los ADR, la etiqueta y el envío al Aula Virtual.
]
