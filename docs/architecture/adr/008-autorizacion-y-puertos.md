# ADR-008: RBAC y puertos de extensión

- Estado: Propuesto con evidencia local; revisión de los integrantes pendiente.
- Fecha: 2026-10-31.
- Autores del informe: Josue Claudio Quispe Paucar y Diego Alejandro Carbajal Gonzales.
- Escenarios: QA08-04 y QA08-05.

## Contexto
No basta ocultar botones. La asignación debe autorizarse en servidor y la infraestructura debe sustituirse sin acoplar la política a proveedores concretos.

## Alternativas consideradas
Controles en interfaz; RBAC en aplicación; RBAC + RLS; condicionales frente a fábrica por registro.

## Decisión
Usaremos RBAC con denegación por defecto en la aplicación y rol obtenido de sesión autenticada. Se conservará Strategy/Adapter del Lab07 para nuevos canales. La aplicación depende de puertos, no de adaptadores concretos; bootstrap compone implementaciones. RLS se aplaza hasta definir particiones territoriales y pruebas PostgreSQL; este laboratorio no declara aislamiento multicooperativa porque el caso no es AgroConecta.

## Evidencia
Cuatro clases de rol no autorizado rechazadas sin modificar la brigada; coordinador permitido. La prueba heredada test_open_closed_nuevo_canal_por_registro pasa. Import-linter: 2 contratos kept; import de infraestructura inyectado rompe FF-02 y su reversión restaura el éxito.

## Consecuencias
RBAC simplifica el MVP pero exige gestión de roles fiable. No valida tokens ni canales cifrados. La regla de imports cubre el paquete experimental sismo_lab08, no garantiza ausencia de ciclos en todo el repositorio heredado.
