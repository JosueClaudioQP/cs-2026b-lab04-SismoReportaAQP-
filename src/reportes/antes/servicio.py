"""Baseline ejecutable creado para E1 a partir del flujo UML del Lab 05.
No es una copia del esqueleto previo: delimita el contrato del experimento.
"""
import json
from dataclasses import dataclass
from math import isfinite
from ..datos_lab07 import DatosReporte, EstadoReporte, NivelDanio, Sugerencia, prompt_clasificacion
from ..externos import APIRegionalSDK, APIAlternaClient, ClienteLLMFalso

@dataclass
class Reporte(DatosReporte):
    estado: EstadoReporte = EstadoReporte.BORRADOR

    def encolar(self):
        if self.estado != EstadoReporte.BORRADOR:
            raise ValueError("Transición inválida")
        self.estado = EstadoReporte.ENCOLADO

    def reintentar(self):
        if self.estado != EstadoReporte.ENCOLADO:
            raise ValueError("Transición inválida")

    def marcar_recibido(self):
        if self.estado != EstadoReporte.ENCOLADO:
            raise ValueError("Transición inválida")
        self.estado = EstadoReporte.RECIBIDO

    def verificar(self, nivel):
        if self.estado != EstadoReporte.RECIBIDO:
            raise ValueError("Transición inválida")
        nivel = NivelDanio(nivel).value
        self.nivel_danio, self.estado = nivel, EstadoReporte.VERIFICADO

    def marcar_atendido(self):
        if self.estado != EstadoReporte.VERIFICADO:
            raise ValueError("Transición inválida")
        if not self.brigada_id:
            raise ValueError("Brigada requerida")
        self.estado = EstadoReporte.ATENDIDO

class ServicioReportes:
    def __init__(self, regional=None, alterna=None, llm=None):
        self.regional = regional or APIRegionalSDK()
        self.alterna = alterna or APIAlternaClient()
        self.llm = llm or ClienteLLMFalso()
        self.pendientes, self.eventos, self.cache = {}, [], {}

    def registrar(self, reporte):
        reporte.validar()
        reporte.encolar()
        self.pendientes[reporte.uuid] = reporte

    def sincronizar(self, reporte, canal="REGIONAL", conectado=True):
        reporte.reintentar()
        if not conectado:
            return "PENDIENTE"
        if canal == "REGIONAL":
            codigo = None
            for intento in range(3):
                try:
                    codigo = self.regional.publicar(reporte.payload())["codigo"]
                    break
                except TimeoutError:
                    if intento == 2:
                        return "PENDIENTE"
        elif canal == "ALTERNA":
            codigo = None
            for intento in range(3):
                try:
                    codigo = self.alterna.send(json.dumps(reporte.payload()))
                    break
                except TimeoutError:
                    if intento == 2:
                        return "PENDIENTE"
        else:
            raise ValueError("Canal no soportado")
        if codigo != 202:
            return "PENDIENTE"
        self.pendientes.pop(reporte.uuid, None)
        self.eventos.append(f"panel:{reporte.uuid}:ACEPTADO")
        self.eventos.append(f"auditoria:{reporte.uuid}:ACEPTADO")
        return "ACEPTADO"

    def procesar(self, reporte):
        # Representa el worker. Un 202 NO adelanta el estado a RECIBIDO.
        reporte.marcar_recibido()

    def sugerir_severidad(self, descripcion):
        if not descripcion.strip():
            raise ValueError("Descripción vacía")
        prompt = prompt_clasificacion(descripcion)
        if prompt not in self.cache:
            self.cache[prompt] = self.llm.completar(prompt)
        texto = self.cache[prompt]
        if not isinstance(texto, str) or len(texto) > 256:
            raise ValueError("Guardrail: longitud o tipo")
        try:
            datos = json.loads(texto)
        except (ValueError, TypeError) as exc:
            raise ValueError("Guardrail: JSON inválido") from exc
        if not isinstance(datos, dict) or set(datos) != {"severidad", "confianza"}:
            raise ValueError("Guardrail: esquema")
        if datos["severidad"] not in [n.value for n in NivelDanio]:
            raise ValueError("Guardrail: severidad")
        confianza = datos["confianza"]
        if type(confianza) not in (int, float):
            raise ValueError("Guardrail: confianza")
        if not isfinite(confianza) or not 0 <= confianza <= 1:
            raise ValueError("Guardrail: confianza")
        return Sugerencia(datos["severidad"], float(confianza))
