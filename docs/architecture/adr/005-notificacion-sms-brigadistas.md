# ADR-005: Aviso de asignación a brigadistas por SMS

- **Estado:** Aceptado
- **Fecha:** 17/10/2026
- **Decisores:** Equipo de trabajo de SismoReporta AQP

## Contexto

El diagrama de actividades del Lab 05 incluye "Notifica al brigadista" al asignar una brigada (RF-07 y rol Brigadista). Ningún ADR anterior define el canal. Los brigadistas están en terreno y la red celular puede estar congestionada.

## Alternativas consideradas

1. **Notificación push:** requiere una app para el brigadista (fuera del alcance del MVP de 1 mes).
2. **WhatsApp Business API:** requiere cuenta y plantillas aprobadas.
3. **SMS mediante un servicio externo (HTTPS/JSON):** elegida.

## Decisión

El módulo Operaciones registra la asignación en la base de datos y solicita el SMS a un servicio externo por HTTPS/JSON. Un fallo del servicio SMS no revierte la asignación. El proveedor concreto se elige en la implementación; el modelo C4 lo representa como el sistema externo "Servicio de mensajería SMS".

## Consecuencias positivas

- No requiere una app adicional ni datos móviles en el brigadista.
- Es un sistema externo simple, coherente con R-01 y R-02.

## Consecuencias negativas

- Depende de un tercero y de la red celular congestionada tras el sismo.
- Los mensajes de texto tienen contenido limitado.
- Se debe definir el reintento de envíos fallidos.
