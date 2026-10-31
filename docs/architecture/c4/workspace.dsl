workspace "SismoReporta AQP - Lab08" "Evolución del monolito modular guiada por atributos de calidad." {
    !identifiers hierarchical
    model {
        ciudadano = person "Ciudadano" "Registra daños aun sin red."
        operador = person "Coordinador" "Clasifica y asigna brigadas con autorización."
        brigadista = person "Brigadista" "Recibe avisos de asignación."
        sismo = softwareSystem "SismoReporta AQP" "20 000 reportes por hora; metadata primero, evidencia diferida." {
            movil = container "Aplicación móvil" "Sync Manager: backoff, jitter y UUID estable [QA08-01, QA08-02]." "Flutter / React Native"
            local = container "Persistencia local" "Pendiente hasta ACK; no borrar antes de confirmación [QA08-02]." "SQLite" "Database"
            panel = container "Panel de operaciones" "Permisos por rol; sin asignación desde rol ciudadano [QA08-04]." "SPA web"
            backend = container "Backend modular" "Un artefacto: API y consumidores internos. Acepta después del commit [QA08-01, QA08-06]." "Python / FastAPI" {
                ingesta = component "Ingesta" "Valida UUID y contenido; transacción de inbox [QA08-01, QA08-02]." "Módulo Python"
                operaciones = component "Operaciones" "RBAC; asignación y outbox SMS atómicos [QA08-03, QA08-04]." "Módulo Python"
                worker = component "Procesamiento interno" "Inbox: reclamar, procesar y confirmar; reintento con lease [QA08-06]." "Worker Python"
                compartido = component "Dominio y puertos" "Reglas y contratos sin infraestructura concreta [QA08-05]." "Protocol / Strategy / Adapter"
            }
            bd = container "Persistencia transaccional" "Inbox con UUID único; reportes; outbox SMS. Commit antes del 202 [QA08-01, QA08-02, QA08-03]." "PostgreSQL 16 + PostGIS" "Database"
            fotos = container "Evidencia" "Carga diferida; estado EVIDENCIA_PENDIENTE; referencia por UUID [QA08-01, QA08-02]." "MinIO / S3"
        }
        sms = softwareSystem "Proveedor SMS" "Externo: su caída no revierte asignaciones [QA08-03]."
        mapas = softwareSystem "Servicio de mapas" "Capa visual; no es requisito para guardar coordenadas."
        ciudadano -> sismo.movil "Registra reporte"
        operador -> sismo.panel "Asigna brigada"
        sismo.movil -> sismo.local "Guarda y confirma pendientes" "SQLite"
        sismo.movil -> sismo.backend "Envía metadata / evidencia por separado" "HTTPS/JSON"
        sismo.panel -> sismo.backend "Consulta y solicita operaciones autorizadas" "HTTPS/REST"
        sismo.panel -> mapas "Solicita tiles" "HTTPS"
        sismo.backend -> sismo.bd "Commit inbox; procesar; outbox" "SQL/TCP"
        sismo.backend -> sismo.fotos "Guarda fotos diferidas y enlaza UUID" "S3 / HTTPS"
        sismo.backend -> sms "Despacha outbox; timeout no revierte asignación" "HTTPS/JSON"
        sms -> brigadista "Entrega aviso"
        sismo.backend.ingesta -> sismo.backend.compartido "Usa contratos"
        sismo.backend.operaciones -> sismo.backend.compartido "Usa contratos"
        sismo.backend.worker -> sismo.backend.compartido "Usa contratos"
        sismo.backend.ingesta -> sismo.bd "Persiste inbox antes del ACK" "SQL"
        sismo.backend.operaciones -> sismo.bd "Asigna y crea outbox en transacción" "SQL"
        sismo.backend.worker -> sismo.bd "Procesa inbox y SMS pendientes" "SQL"
        sismo.backend.worker -> sms "Reintenta aviso" "HTTPS/JSON"
    }
    views {
        systemContext sismo "ContextoLab08" {
            include *
            autolayout lr
        }
        container sismo "ContenedoresLab08" {
            include *
            autolayout lr
        }
        component sismo.backend "ComponentesLab08" {
            include *
            autolayout lr
        }
        styles {
            element "Person" {
                shape person
                background #12364b
                color #ffffff
            }
            element "Container" {
                background #147d92
                color #ffffff
            }
            element "Database" {
                shape cylinder
            }
        }
    }
}

