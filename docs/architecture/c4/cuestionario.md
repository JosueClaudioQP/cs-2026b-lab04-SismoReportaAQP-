# Cuestionario – Lab 06 (SismoReporta AQP)

1. **Cajas y flechas:** C4 fija qué es cada elemento y cada flecha. Ambigüedad evitada: "Cola" podía ser un servicio o una tecnología; ahora es el contenedor "Cola persistente [Redis 7]" y el worker es un componente, no un servicio aparte.
2. **Contenedor:** unidad que se ejecuta o despliega por separado; no equivale a Docker. La aplicación móvil y el panel web no se ejecutan en Docker (corren en el teléfono y el navegador).
3. **Niveles:** 1 contexto (todos), 2 contenedores (equipo técnico), 3 componentes (arquitectos y developers), 4 código (developers). El nivel 4 rara vez se dibuja a mano porque se genera del código (aquí, `docs/design/clases.puml`).
4. **Dinámica vs secuencia:** la dinámica muestra 7 pasos de alto nivel con protocolos; la secuencia detalla operaciones y alternativas. Dinámica para explicar el flujo; secuencia para implementar y probar.
5. **Structurizr DSL:** un solo modelo genera las 5 vistas; renombrar un elemento se hace una vez (en nuestro caso, un nombre aparece en 11 líneas de 5 archivos generados).
6. **ADR:** ADR-001 (monolito modular → un contenedor Backend con módulos), ADR-002 (SQLite + Sync Manager → contenedores Aplicación móvil y Almacenamiento local), ADR-003 (cola persistente y worker interno → contenedor Cola y componente Procesamiento), ADR-004 (PostgreSQL + MinIO).
7. **Error de la IA:** marcó como problema 8 relaciones sin tecnología; la lista oficial muestra que en el nivel 1 y en llamadas dentro del mismo proceso no se exige protocolo (falso positivo). Aceptarlo habría llenado el modelo de protocolos inventados.
8. **Audiencias:** docente evaluador → trazabilidad ADR→C4 y lista de revisión; inversionista → vista de contexto y la explicación sin jerga; developer nuevo → componentes, vista dinámica y despliegue.
