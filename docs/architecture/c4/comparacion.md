# Comparación (E4 y E6) – SismoReporta AQP

## E4. Secuencia UML (Lab 05) frente a vista dinámica C4
La secuencia UML muestra el detalle de clases y operaciones (`validarUuid`, `existe`, `marcarRecibido`), los fragmentos `loop`/`alt` y los reintentos con backoff, y sirve a los developers para implementar y probar. La vista dinámica omite esas operaciones y las alternativas: solo muestra los 7 pasos entre contenedores y componentes con su protocolo (HTTPS/JSON, Redis, SQL), y sirve a arquitectos y operaciones para entender el recorrido de un reporte. La secuencia responde "cómo se implementa"; la dinámica, "qué se conecta con qué".

## E6. Escritura a mano frente a modelo exportado

| Aspecto | `contexto-manual.puml` (a mano) | `workspace.dsl` + exportación |
|---|---|---|
| Esfuerzo (medido en líneas escritas) | 20 líneas para 1 vista | 152 líneas para 5 vistas (se generan 227 líneas de PlantUML) |
| Errores encontrados | Hubo que repetir a mano nombres y descripciones de 3 personas y 2 sistemas externos; el Brigadista debe agregarse explícitamente. | `validate` detecta identificadores inexistentes; una vista dinámica con relación inexistente falla al validar. |
| Si mañana cambia el nombre de un contenedor | Hay que corregirlo a mano en cada archivo que lo use. | Se cambia una vez en el DSL y se vuelve a exportar: "SismoReporta AQP" aparece 11 veces en 5 archivos generados y solo se escribe una vez. |

Conclusión: el modelo único evita inconsistencias entre vistas; el diagrama a mano sirve para entender las macros de C4-PlantUML. El tiempo exacto no se midió; se compara en líneas escritas.
