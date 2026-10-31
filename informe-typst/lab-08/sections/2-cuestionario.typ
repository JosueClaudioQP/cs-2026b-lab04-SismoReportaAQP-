#import "/components/@unsareport/epis-lab/lib.typ": lab-section

#lab-section("II. CUESTIONARIO")[
#set text(size: 11pt, hyphenate: false)
#show raw: set text(size: 11pt)
#set par(justify: true, leading: 0.55em, spacing: 0.65em)
#show heading: set text(size: 11pt, weight: "bold")
#show heading: set block(above: 0.9em, below: 0.5em)
== 1. ¿En qué se diferencia ADD de elegir un estilo arquitectónico?

El estilo define la organización general. ADD refina la arquitectura en iteraciones con objetivos, alternativas, responsabilidades y verificación. Mantuvimos el monolito del ADR-001, pero concretamos ingesta, sincronización y autorización con evidencia.

== 2. ¿Para qué sirve calificar importancia y dificultad?

Permite priorizar impacto y riesgo técnico. QA08-02 es H/H porque perder reportes afecta la función principal; QA08-01 y 06 también son H/H por la reconexión. QA08-05 baja a M/L porque la extensión por registro ya existe.

== 3. ¿Qué diferencia existe entre táctica y patrón?

Una táctica influye en un atributo; un patrón organiza responsabilidades y combina tácticas. Circuit breaker combina detección de fallas, falla rápida y prueba de recuperación; puede implementarse como Decorator. No se afirma haber integrado el breaker de pagos de AgroConecta.

== 4. Describa sensibilidad y trade-off con evidencia.

El servicio medio de ingesta de 35 → 60 ms eleva p95 de 72,87 → 2 786,23 ms. El ACK antes de foto mejora aceptación, pero deja evidencia pendiente; la cola extrema todavía tarda 898,28 s adicionales en drenarse.

== 5. ¿Qué supuestos podrían invalidar la simulación?

Se asumieron servicios de 35/120 ms, distribución lognormal, disco disponible y etapas separadas. Contención real de I/O, locks, fotos y red móvil pueden aumentar latencia o drenaje. Debe medirse el endpoint real y monitorearse el backlog.

== 6. ¿Qué riesgo de la evaluación cruzada aceptaron y por qué?

No se recibió una evaluación cruzada, por lo que no se le atribuye un riesgo. La autoevaluación propone aceptar residualmente el host único durante el MVP de un mes, coherente con ADR-004, sujeto a copia externa y prueba de restauración.

== 7. ¿Qué es una fitness function y qué detectan las propias?

Es una verificación automática de una propiedad arquitectónica. FF-01/02 controlan dependencias; FF-03/07, latencia y drenaje; FF-04, replay; FF-05, SMS; FF-06, autorización. Los presupuestos simulados no reemplazan la prueba de carga real.

== 8. ¿Qué propuesta de IA se rechazó con evidencia?

Se refutó la ausencia de ADR-005/C4 al revisar el remoto actualizado. También se rechazó dimensionar solo por la media: el mismo total arroja p95 síncrono de 1,53 s uniforme y unos 719 s en ráfaga. Sin verificar, se ignoraría la reconexión.
]

