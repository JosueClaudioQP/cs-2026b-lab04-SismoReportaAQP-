workspace "SismoReporta AQP" "Modelo C4 de la plataforma ciudadana de reporte de daños tras un sismo (Caso 8, Labs 04 y 05)." {

    !identifiers hierarchical

    model {
        ciudadano = person "Ciudadano" "Persona afectada que reporta daños con ubicación y fotos, incluso sin conectividad."
        coordinador = person "Operador / Coordinador de Defensa Civil" "Visualiza el mapa de daños, clasifica reportes, actualiza estados y asigna brigadas."
        brigadista = person "Brigadista" "Recibe los incidentes priorizados y los atiende en terreno."

        sismo = softwareSystem "SismoReporta AQP" "Recibe reportes ciudadanos de daños tras un sismo (hasta 20 000 en la primera hora) y apoya la priorización de zonas." {
            movil = container "Aplicación móvil" "Registra reportes con ubicación y fotografías; funciona sin conexión y sincroniza con reintentos (backoff exponencial + jitter)." "Flutter / React Native" "Mobile App"
            local = container "Almacenamiento local" "Reportes pendientes de sincronización, con UUID y estado." "SQLite" "Database"
            panel = container "Panel web de operaciones" "Mapa de daños, filtros, clasificación, estados y asignación de brigadas." "SPA web" "Web Browser"
            backend = container "Backend SismoReporta" "Monolito modular con API REST (ADR-001); el worker interno corre dentro del mismo artefacto (ADR-003)." "Python / FastAPI" {
                ingesta = component "Módulo Ingesta" "Valida el UUID, guarda la evidencia, publica en la cola y responde HTTP 202 (RF-01 a RF-03)." "Módulo Python"
                operaciones = component "Módulo Operaciones" "Consulta, clasifica y cambia el estado de reportes; asigna brigadas (RF-05 a RF-07)." "Módulo Python"
                procesamiento = component "Módulo Procesamiento" "Worker interno asíncrono: consume la cola y persiste el reporte de forma idempotente." "Módulo Python"
                compartido = component "Módulo Compartido" "Entidad Reporte y puertos ColaReportes y RepositorioReportes." "Módulo Python"
            }
            cola = container "Cola persistente" "Mensajes de reportes (metadata y referencias, sin fotos binarias); persistencia AOF." "Redis 7" "Queue"
            bd = container "Base de datos" "Reportes, estados, UUID, brigadas y geolocalización." "PostgreSQL 16 + PostGIS" "Database"
            fotos = container "Almacenamiento de evidencia" "Fotografías de daños, referenciadas por URI desde el reporte." "MinIO (API S3)" "Storage"
        }

        mapas = softwareSystem "Servicio de mapas" "Provee los mapas (tiles) para ubicar los reportes." "Externo"
        sms = softwareSystem "Servicio de mensajería SMS" "Entrega los avisos de asignación a los brigadistas." "Externo"

        ciudadano -> sismo "Reporta daños tras un sismo"
        coordinador -> sismo "Prioriza zonas y asigna brigadas"
        sismo -> mapas "Obtiene mapas para ubicar reportes" "HTTPS"
        sismo -> sms "Solicita avisos de asignación" "HTTPS/JSON"
        sms -> brigadista "Envía el aviso de asignación"

        ciudadano -> sismo.movil "Registra reportes de daños y fotos"
        coordinador -> sismo.panel "Revisa el mapa y asigna brigadas"
        sismo.movil -> sismo.local "Guarda y lee reportes pendientes" "SQLite"
        sismo.movil -> sismo.backend "Envía reportes con UUID" "HTTPS/JSON"
        sismo.panel -> sismo.backend "Consulta reportes y los gestiona" "HTTPS/REST"
        sismo.panel -> mapas "Descarga mapas para ubicar reportes" "HTTPS"
        sismo.backend -> sismo.cola "Publica y consume reportes" "Redis protocol"
        sismo.backend -> sismo.bd "Persiste y consulta reportes" "SQL/TCP"
        sismo.backend -> sismo.fotos "Guarda evidencia fotográfica" "API S3 / HTTPS"
        sismo.backend -> sms "Solicita avisos de asignación" "HTTPS/JSON"

        sismo.movil -> sismo.backend.ingesta "Envía reportes con UUID" "HTTPS/JSON"
        sismo.panel -> sismo.backend.operaciones "Consulta, clasifica y asigna" "HTTPS/REST"
        sismo.backend.ingesta -> sismo.fotos "Guarda evidencia fotográfica" "API S3 / HTTPS"
        sismo.backend.ingesta -> sismo.cola "Publica el reporte (metadata y referencias)" "Redis protocol"
        sismo.backend.procesamiento -> sismo.cola "Consume reportes" "Redis protocol"
        sismo.backend.procesamiento -> sismo.bd "Persiste el reporte (idempotente por UUID)" "SQL/TCP"
        sismo.backend.operaciones -> sismo.bd "Consulta y actualiza estados y asignaciones" "SQL/TCP"
        sismo.backend.operaciones -> sms "Solicita aviso de asignación" "HTTPS/JSON"
        sismo.backend.ingesta -> sismo.backend.compartido "Usa Reporte y ColaReportes"
        sismo.backend.procesamiento -> sismo.backend.compartido "Usa ColaReportes y RepositorioReportes"
        sismo.backend.operaciones -> sismo.backend.compartido "Usa Reporte y RepositorioReportes"

        produccion = deploymentEnvironment "Producción" {
            telefono = deploymentNode "Smartphone del ciudadano" "" "Android / iOS" {
                movil = containerInstance sismo.movil
                local = containerInstance sismo.local
            }
            estacion = deploymentNode "Estación del operador" "" "PC con navegador web" {
                panel = containerInstance sismo.panel
            }
            servidor = deploymentNode "Servidor de producción" "Un solo host para el MVP (ver ADR-004)." "Linux, 4 vCPU, 8 GB RAM, disco SSD" {
                compose = deploymentNode "Docker Compose" "" "Docker" {
                    nginx = infrastructureNode "Nginx" "Reverse proxy: TLS y rate limiting." "Nginx"
                    backend = containerInstance sismo.backend
                    cola = containerInstance sismo.cola
                    bd = containerInstance sismo.bd
                    fotos = containerInstance sismo.fotos
                    prometheus = infrastructureNode "Prometheus" "Métricas de ingesta y longitud de la cola." "Prometheus"
                    grafana = infrastructureNode "Grafana" "Tablero operacional y alertas." "Grafana"
                }
            }
            telefono.movil -> servidor.compose.nginx "Envía reportes" "HTTPS/443"
            estacion.panel -> servidor.compose.nginx "Consulta y gestiona reportes" "HTTPS/443"
            servidor.compose.nginx -> servidor.compose.backend "Reenvía las solicitudes" "HTTP"
            servidor.compose.prometheus -> servidor.compose.backend "Lee métricas" "HTTP /metrics"
            servidor.compose.prometheus -> servidor.compose.cola "Lee la longitud de la cola" "Redis protocol"
            servidor.compose.grafana -> servidor.compose.prometheus "Consulta métricas" "HTTP"
        }
    }

    views {
        systemContext sismo "Contexto" "Nivel 1: SismoReporta AQP, sus usuarios y sistemas externos." {
            include *
            include brigadista
            autolayout lr
        }
        container sismo "Contenedores" "Nivel 2: contenedores de SismoReporta AQP." {
            include *
            autolayout lr
        }
        component sismo.backend "Componentes" "Nivel 3: módulos del backend (paquetes del Lab 05)." {
            include *
            autolayout lr
        }
        dynamic sismo.backend "SincronizarReporte" "Dinámico: enviar un reporte sin señal y sincronizarlo (secuencia del Lab 05)." {
            sismo.movil -> sismo.local "Guarda el reporte pendiente (ENCOLADO)"
            sismo.movil -> sismo.backend.ingesta "Envía el reporte con UUID al recuperar señal"
            sismo.backend.ingesta -> sismo.fotos "Guarda las fotografías y obtiene su referencia"
            sismo.backend.ingesta -> sismo.cola "Publica el mensaje persistente"
            sismo.backend.ingesta -> sismo.movil "Responde HTTP 202 Accepted"
            sismo.backend.procesamiento -> sismo.cola "Consume el mensaje"
            sismo.backend.procesamiento -> sismo.bd "Verifica el UUID y persiste el reporte"
            autolayout lr
        }
        deployment sismo produccion "Despliegue" "Despliegue en producción (MVP): un servidor con Docker Compose. Las flechas directas son lógicas; físicamente el tráfico HTTPS pasa por Nginx." {
            include *
            autolayout lr
        }

        styles {
            element "Person" {
                shape person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "Externo" {
                background #999999
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "Component" {
                background #85BBF0
                color #000000
            }
            element "Database" {
                shape cylinder
            }
            element "Queue" {
                shape pipe
            }
            element "Storage" {
                shape folder
            }
            element "Web Browser" {
                shape WebBrowser
            }
            element "Mobile App" {
                shape MobileDevicePortrait
            }
        }
    }
}
