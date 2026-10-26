"""Clases de servicio generadas desde docs/design/clases.puml (ingeniería directa)."""
from __future__ import annotations
from datetime import datetime
from uuid import UUID

from .dominio import (ColaReportes, NivelDanio, Reporte, RepositorioReportes)


class SyncManager:
    """Cliente móvil: guarda reportes y los sincroniza con backoff exponencial."""

    def __init__(self) -> None:
        self.intentos: int = 0
        self._pendientes: dict[UUID, Reporte] = {}

    def registrar(self, r: Reporte) -> None:
        r.encolar()
        self._pendientes[r.uuid] = r

    def sincronizar_pendientes(self) -> None:
        raise NotImplementedError("Enviar cada pendiente al ApiController por HTTPS")

    def calcular_backoff(self, intento: int) -> int:
        return min(2 ** intento, 300)  # segundos; el jitter se agrega al reintentar

    def marcar_sincronizado(self, uuid: UUID) -> None:
        self._pendientes.pop(uuid, None)


class ServicioIngesta:
    def __init__(self, cola: ColaReportes, repositorio: RepositorioReportes) -> None:
        self._cola = cola
        self._repositorio = repositorio

    def validar_uuid(self, uuid: UUID) -> bool:
        return not self._repositorio.existe(uuid)

    def recibir(self, r: Reporte) -> bool:
        if not self.validar_uuid(r.uuid):
            return False
        self._cola.publicar(r)
        return True


class ApiController:
    def __init__(self, servicio: ServicioIngesta) -> None:
        self._servicio = servicio

    def recibir_reporte(self, r: Reporte) -> int:
        return 202 if self._servicio.recibir(r) else 409


class WorkerProcesamiento:
    def __init__(self, cola: ColaReportes, repositorio: RepositorioReportes) -> None:
        self._cola = cola
        self._repositorio = repositorio

    def procesar(self) -> None:
        r = self._cola.consumir()
        if not self._repositorio.existe(r.uuid):
            r.marcar_recibido(datetime.now())
            self._repositorio.guardar(r)


class ServicioOperaciones:
    def __init__(self, repositorio: RepositorioReportes) -> None:
        self._repositorio = repositorio

    def verificar(self, reporte_id: UUID, nivel: NivelDanio) -> None:
        r = self._repositorio.buscar(reporte_id)
        r.verificar(nivel)
        self._repositorio.guardar(r)

    def asignar_brigada(self, reporte_id: UUID, brigada_id: UUID) -> None:
        raise NotImplementedError("Buscar la Brigada, asignarla al reporte y solicitar el SMS (ADR-005)")

