#!/usr/bin/env python3
"""
SismoReporta AQP - Diagrama de Vista de Despliegue (E6)
Basado en la arquitectura seleccionada: Monolito Modular con Ingesta Asíncrona.

Instrucciones de ejecución (Google Colab o entorno con Graphviz):
    !apt-get install -y graphviz
    !pip install diagrams
    python despliegue.py
"""

import os
from diagrams import Diagram, Cluster, Edge
from diagrams.generic.device import Mobile
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx, Internet
from diagrams.programming.framework import FastAPI
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.storage import Minio
from diagrams.onprem.monitoring import Prometheus, Grafana

# Determinar la ruta de salida para guardar en docs/architecture/diagramas/img/despliegue
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "img")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "despliegue")

graph_attr = {
    "fontsize": "16",
    "fontname": "Helvetica",
    "bgcolor": "#F8F9FA",
    "pad": "0.5",
    "splines": "ortho"
}

node_attr = {
    "fontsize": "11",
    "fontname": "Helvetica"
}

edge_attr = {
    "fontsize": "10",
    "fontname": "Helvetica"
}

with Diagram(
    "SismoReporta AQP - Vista de Despliegue Física y Lógica",
    filename=OUTPUT_FILE,
    outformat="png",
    show=False,
    direction="TB",
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr
):
    # ==========================================
    # DISPOSITIVOS Y USUARIOS
    # ==========================================
    with Cluster("Dispositivos de Clientes y Actores"):
        with Cluster("Dispositivos Móviles (Offline-First)"):
            app_ciudadano = Mobile("App Móvil Ciudadano\n(Android / iOS)\n[SQLite Local + Sync]")
        
        with Cluster("Puesto de Comando"):
            operador = User("Operador / Defensa Civil\n[Navegador Web / PC]")

    # ==========================================
    # RED EXTERNA Y CONECTIVIDAD
    # ==========================================
    red_movil = Internet("Red Móvil Celular\n(Intermitente / Post-sismo)")
    red_internet = Internet("Red Internet / WAN")

    # ==========================================
    # INFRAESTRUCTURA DE SERVIDOR (MONOLITO MODULAR)
    # ==========================================
    with Cluster("Servidor de Producción SismoReporta AQP (Host / VM / Docker Host)"):
        # Proxy inverso y balanceador de entrada
        proxy = Nginx("Nginx Reverse Proxy\n[SSL Termination, Rate Limit\n& Static Asset Cache]")

        # Capa de Aplicación Monolítica Modular
        with Cluster("Contenedor Backend (Monolito Modular)"):
            backend_api = FastAPI("API REST (FastAPI)\n- Mód. Ingesta (UUID/Idempotencia)\n- Mód. Operaciones & Brigadas")
            worker_interno = FastAPI("Worker Asíncrono Interno\n[Consumidor de Cola]")

        # Capa de Mensajería y Caché
        with Cluster("Caché y Cola Persistente"):
            cola_redis = Redis("Redis 7 (AOF Persistente)\n[Cola de Reportes BullMQ/Celery]\nCapacidad: >20k msgs")

        # Capa de Persistencia
        with Cluster("Almacenamiento y Base de Datos"):
            bd_postgres = PostgreSQL("PostgreSQL 16 + PostGIS\n[Reportes, Zonas, Brigadas]\n(Persistencia Relacional)")
            storage_fotos = Minio("Storage de Evidencia (MinIO)\n[Fotos de Daños / Vol. Persistente]")

        # Capa de Monitoreo y Observabilidad
        with Cluster("Observabilidad y Monitoreo"):
            prom = Prometheus("Prometheus\n[Métricas de Cola y Latencia]")
            grafana = Grafana("Grafana Dashboard\n[Alertas y Rendimiento]")

    # ==========================================
    # SERVICIOS EXTERNOS
    # ==========================================
    with Cluster("Servicios Externos"):
        mapas_externos = Internet("Servicio Externo de Mapas\n(OpenStreetMap / Mapbox Tiles)")

    # ==========================================
    # CONEXIONES Y FLUJOS CON ETIQUETAS
    # ==========================================

    # Flujo Ciudadano (Ingesta y sincronización)
    app_ciudadano >> Edge(label="1. Reporte offline o reintento\n(HTTPS / JSON + UUID)", color="#D9534F") >> red_movil
    red_movil >> Edge(label="HTTPS / 443", color="#D9534F") >> proxy

    # Flujo Operador (Consulta y triage)
    operador >> Edge(label="Consulta panel / Asignar brigada\n(HTTPS / REST)", color="#0275D8") >> red_internet
    red_internet >> Edge(label="HTTPS / 443", color="#0275D8") >> proxy

    # Nginx a API REST
    proxy >> Edge(label="Proxy pass :8000\n[Ruta /api/v1/reportes]", color="#333333") >> backend_api

    # Desacoplamiento de Ingesta hacia Cola Redis
    backend_api >> Edge(label="2. Encolar payload liviano\n[Retorna HTTP 202 en <100ms]", color="#5CB85C") >> cola_redis

    # Worker asíncrono consumiendo de Redis
    cola_redis >> Edge(label="3. Pop / Consumo ordenado", color="#F0AD4E") >> worker_interno

    # Worker persistiendo en PostgreSQL y MinIO
    worker_interno >> Edge(label="4. INSERT reporte (PostGIS)", color="#2E6DA4") >> bd_postgres
    worker_interno >> Edge(label="5. Guardar fotos referenciadas", color="#5BC0DE") >> storage_fotos

    # Operaciones síncronas de lectura del operador
    backend_api >> Edge(label="Consultar / Priorizar zonas\n(SELECT con índices)", color="#0275D8") >> bd_postgres

    # Visualización de mapas desde el frontend del operador
    operador >> Edge(label="Descarga de Map Tiles\n(Fuera del servidor central)", style="dotted", color="#8A6D3B") >> mapas_externos

    # Monitoreo
    backend_api >> Edge(label="Expose /metrics", style="dashed", color="#777777") >> prom
    cola_redis >> Edge(label="Monitoreo de cola", style="dashed", color="#777777") >> prom
    prom >> Edge(label="Visualizar estado", color="#F39C12") >> grafana

if __name__ == "__main__":
    print(f"Diagrama de despliegue generado exitosamente en: {OUTPUT_FILE}.png")
