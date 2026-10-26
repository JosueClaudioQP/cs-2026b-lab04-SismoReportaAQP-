"""STATE: prohibición por defecto y una clase por estado del Lab 05."""
from ..datos_lab07 import EstadoReporte, NivelDanio

class Estado:
    nombre = None
    def encolar(self, reporte):
        raise ValueError("Transición inválida")
    def reintentar(self, reporte):
        raise ValueError("Transición inválida")
    def marcar_recibido(self, reporte):
        raise ValueError("Transición inválida")
    def verificar(self, reporte, nivel):
        raise ValueError("Transición inválida")
    def marcar_atendido(self, reporte):
        raise ValueError("Transición inválida")

class Borrador(Estado):
    nombre = EstadoReporte.BORRADOR
    def encolar(self, reporte):
        reporte._estado = Encolado()

class Encolado(Estado):
    nombre = EstadoReporte.ENCOLADO
    def reintentar(self, reporte):
        return None
    def marcar_recibido(self, reporte):
        reporte._estado = Recibido()

class Recibido(Estado):
    nombre = EstadoReporte.RECIBIDO
    def verificar(self, reporte, nivel):
        reporte.nivel_danio = NivelDanio(nivel).value
        reporte._estado = Verificado()

class Verificado(Estado):
    nombre = EstadoReporte.VERIFICADO
    def marcar_atendido(self, reporte):
        if not reporte.brigada_id:
            raise ValueError("Brigada requerida")
        reporte._estado = Atendido()

class Atendido(Estado):
    nombre = EstadoReporte.ATENDIDO
