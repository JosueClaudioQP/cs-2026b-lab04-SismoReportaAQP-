from dataclasses import dataclass, field
from ..datos_lab07 import DatosReporte
from .estados import Estado, Borrador

@dataclass
class Reporte(DatosReporte):
    _estado: Estado = field(default_factory=Borrador, init=False, repr=False)

    @property
    def estado(self):
        return self._estado.nombre

    def encolar(self):
        self._estado.encolar(self)
    def reintentar(self):
        self._estado.reintentar(self)
    def marcar_recibido(self):
        self._estado.marcar_recibido(self)
    def verificar(self, nivel):
        self._estado.verificar(self, nivel)
    def marcar_atendido(self):
        self._estado.marcar_atendido(self)
