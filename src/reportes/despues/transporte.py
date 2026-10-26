"""Strategy + Adapter + fábrica por registro + Decorator de reintentos."""
import json
from abc import ABC, abstractmethod
from collections.abc import Callable
from ..datos_lab07 import DatosReporte

class CanalEnvio(ABC):
    @abstractmethod
    def enviar(self, reporte: DatosReporte) -> int:
        """Devuelve HTTP; TimeoutError significa respuesta desconocida."""

class RegionalAdapter(CanalEnvio):
    def __init__(self, sdk):
        self._sdk = sdk
    def enviar(self, reporte):
        return self._sdk.publicar(reporte.payload())["codigo"]

class AlternaAdapter(CanalEnvio):
    def __init__(self, cliente):
        self._cliente = cliente
    def enviar(self, reporte):
        return self._cliente.send(json.dumps(reporte.payload()))

class FabricaCanales:
    """Fábrica simple extensible por registro, no Factory Method GoF estricto."""
    def __init__(self):
        self._creadores: dict[str, Callable[[], CanalEnvio]] = {}
    def registrar(self, nombre, creador):
        self._creadores[nombre] = creador
    def crear(self, nombre):
        try:
            creador = self._creadores[nombre]
        except KeyError as exc:
            raise ValueError("Canal no soportado") from exc
        return creador()

class ConReintentos(CanalEnvio):
    """Solo reintenta TimeoutError; no convierte un 4xx en éxito.
    Sin esperas reales en la simulación; backoff+jitter productivo queda fuera.
    """
    def __init__(self, interno: CanalEnvio, max_intentos=3):
        if max_intentos < 1:
            raise ValueError("Al menos un intento")
        self._interno, self._max_intentos = interno, max_intentos
    def enviar(self, reporte):
        for _ in range(self._max_intentos):
            try:
                return self._interno.enviar(reporte)
            except TimeoutError:
                pass
        raise TimeoutError("Intentos agotados")
