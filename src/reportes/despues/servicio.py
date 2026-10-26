"""Orquestación: los patrones encapsulan las decisiones variables."""
from ..externos import APIRegionalSDK, APIAlternaClient, ClienteLLMFalso
from .modelo import Reporte
from .transporte import FabricaCanales, RegionalAdapter, AlternaAdapter, ConReintentos
from .eventos import Publicador, PanelObserver, AuditoriaObserver, EventoAceptado
from .ia import (LLMAdapter, ConCache, FormatoJSON, SeveridadPermitida,
                 ConfianzaValida, ClasificadorSeveridad)

class ServicioReportes:
    def __init__(self, regional=None, alterna=None, llm=None, proveedor=None):
        regional = regional or APIRegionalSDK()
        alterna = alterna or APIAlternaClient()
        self.fabrica = FabricaCanales()
        self.fabrica.registrar("REGIONAL", lambda: RegionalAdapter(regional))
        self.fabrica.registrar("ALTERNA", lambda: AlternaAdapter(alterna))
        self.pendientes, self.eventos = {}, []
        self.publicador = Publicador()
        self.publicador.suscribir(PanelObserver(self.eventos))
        self.publicador.suscribir(AuditoriaObserver(self.eventos))
        proveedor = proveedor or LLMAdapter(llm or ClienteLLMFalso())
        self.clasificador = ClasificadorSeveridad(
            ConCache(proveedor), FormatoJSON(SeveridadPermitida(ConfianzaValida())))

    def registrar(self, reporte: Reporte):
        reporte.validar()
        reporte.encolar()
        self.pendientes[reporte.uuid] = reporte

    def sincronizar(self, reporte: Reporte, canal="REGIONAL", conectado=True):
        reporte.reintentar()
        if not conectado:
            return "PENDIENTE"
        envio = ConReintentos(self.fabrica.crear(canal))
        try:
            codigo = envio.enviar(reporte)
        except TimeoutError:
            return "PENDIENTE"
        if codigo != 202:
            return "PENDIENTE"
        self.pendientes.pop(reporte.uuid, None)
        self.publicador.publicar(EventoAceptado(reporte.uuid))
        return "ACEPTADO"

    def procesar(self, reporte: Reporte):
        reporte.marcar_recibido()

    def sugerir_severidad(self, descripcion):
        return self.clasificador.sugerir(descripcion)
