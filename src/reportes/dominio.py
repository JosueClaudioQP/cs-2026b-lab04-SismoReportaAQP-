"""Esqueleto generado desde docs/design/clases.puml (ingeniería directa)."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4


class EstadoReporte(Enum):
    BORRADOR = "BORRADOR"
    ENCOLADO = "ENCOLADO"
    RECIBIDO = "RECIBIDO"
    VERIFICADO = "VERIFICADO"
    ATENDIDO = "ATENDIDO"


class NivelDanio(Enum):
    LEVE = "LEVE"
    MODERADO = "MODERADO"
    SEVERO = "SEVERO"


@dataclass
class Evidencia:
    url_referencia: str
    tamano_bytes: int
    uuid: UUID = field(default_factory=uuid4)


@dataclass
class Brigada:
    nombre: str
    disponible: bool = True
    id: UUID = field(default_factory=uuid4)


@dataclass
class Reporte:
    latitud: Decimal
    longitud: Decimal
    descripcion: str
    evidencias: list[Evidencia] = field(default_factory=list)
    nivel_danio: NivelDanio | None = None
    estado: EstadoReporte = EstadoReporte.BORRADOR
    brigada: Brigada | None = None
    timestamp_dispositivo: datetime = field(default_factory=datetime.now)
    timestamp_servidor: datetime | None = None
    uuid: UUID = field(default_factory=uuid4)

    def encolar(self) -> None:
        self.estado = EstadoReporte.ENCOLADO

    def reintentar(self) -> None:
        if self.estado is not EstadoReporte.ENCOLADO:
            raise ValueError("Solo un reporte ENCOLADO puede reintentarse")

    def marcar_recibido(self, ts: datetime) -> None:
        self.timestamp_servidor = ts
        self.estado = EstadoReporte.RECIBIDO

    def verificar(self, nivel: NivelDanio) -> None:
        self.nivel_danio = nivel
        self.estado = EstadoReporte.VERIFICADO

    def asignar_brigada(self, b: Brigada) -> None:
        self.brigada = b

    def marcar_atendido(self) -> None:
        if self.brigada is None:
            raise ValueError("Se requiere brigada asignada")
        self.estado = EstadoReporte.ATENDIDO


class ColaReportes(ABC):
    @abstractmethod
    def publicar(self, r: Reporte) -> None: ...

    @abstractmethod
    def consumir(self) -> Reporte: ...


class RepositorioReportes(ABC):
    @abstractmethod
    def existe(self, uuid: UUID) -> bool: ...

    @abstractmethod
    def guardar(self, r: Reporte) -> None: ...

    @abstractmethod
    def buscar(self, uuid: UUID) -> Reporte: ...


class ColaPersistenteAdapter(ColaReportes):
    def publicar(self, r: Reporte) -> None:
        raise NotImplementedError("Integrar con la cola persistente (Redis AOF)")

    def consumir(self) -> Reporte:
        raise NotImplementedError("Integrar con la cola persistente (Redis AOF)")

