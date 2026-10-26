"""Observer síncrono en memoria; los suscriptores no usan red."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class EventoAceptado:
    reporte_id: str

class Suscriptor(ABC):
    @abstractmethod
    def actualizar(self, evento: EventoAceptado):
        pass

class Publicador:
    def __init__(self):
        self._suscriptores: list[Suscriptor] = []
    def suscribir(self, suscriptor: Suscriptor):
        self._suscriptores.append(suscriptor)
    def publicar(self, evento: EventoAceptado):
        for suscriptor in tuple(self._suscriptores):
            suscriptor.actualizar(evento)

class PanelObserver(Suscriptor):
    def __init__(self, registros):
        self._registros = registros
    def actualizar(self, evento):
        self._registros.append(f"panel:{evento.reporte_id}:ACEPTADO")

class AuditoriaObserver(Suscriptor):
    def __init__(self, registros):
        self._registros = registros
    def actualizar(self, evento):
        self._registros.append(f"auditoria:{evento.reporte_id}:ACEPTADO")
