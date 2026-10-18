# Revisión con la lista oficial de c4model.com (E7)

Cinco vistas generadas desde `workspace.dsl` (PNG en `img/`). Preguntas: General (título, tipo y alcance, leyenda), Elementos (nombre, tipo, descripción, tecnología) y Relaciones (etiqueta con intención, dirección, protocolo).

| Vista | General | Elementos | Relaciones | Evidencia / observación |
|---|---|---|---|---|
| Contexto | Sí | Sí | Sí | Título "System Context View", descripción y leyenda; sin tecnologías internas; flechas con verbo ("Reporta daños", "Solicita avisos"). |
| Contenedores | Sí | Sí | Sí | Cada contenedor con tecnología y cada flecha entre procesos con protocolo. La flecha "Publica y consume reportes" mezcla dos intenciones; se acepta porque comparten protocolo (Redis). |
| Componentes | Sí | Sí | Sí | Los 4 componentes coinciden con `paquetes.puml` (Lab 05); sin ciclos: todos dependen de Compartido y no entre sí. |
| Dinámica | Sí | Sí | Sí | 7 pasos numerados, cada uno sobre una relación existente; el paso 5 es la respuesta HTTP 202 (retorno). |
| Despliegue | Sí | Sí | Parcial | Aparecen flechas directas móvil→backend y panel→backend además de las que pasan por Nginx. Se aclaró en la descripción de la vista: las directas son lógicas. |

## Revisión de la IA (Prompt IA 2 como segundo revisor)
La revisión se ejecutó con un chequeo automático sobre el modelo exportado (JSON de Structurizr) y lectura de las vistas.

| Hallazgo de la IA | Verificación del equipo |
|---|---|
| 8 relaciones sin tecnología: Ciudadano→Sistema, Ciudadano→App móvil, Coordinador→Sistema, Coordinador→Panel, SMS→Brigadista y 3 componentes→Compartido. | **Falso positivo:** persona→sistema y persona→app son interacción humana (en el nivel 1 no se exige protocolo) y las llamadas a Compartido ocurren dentro del mismo proceso (no hay protocolo de red). |
| Flechas duplicadas en la vista de despliegue (directa y vía Nginx). | Correcto: es el comportamiento del modelo derivado; se documentó en la descripción de la vista. |
| La flecha "Publica y consume reportes" mezcla dos intenciones. | Correcto, aceptado (ver arriba). |
| No se encontraron contenedores llamados "Docker", "servidor" o "nube". | Correcto (cumple). |
| El nombre del componente "Procesamiento asíncrono" no coincidía con el paquete `procesamiento` (C5). | Correcto: se renombró a "Módulo Procesamiento". |
