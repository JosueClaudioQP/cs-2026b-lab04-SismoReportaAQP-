"""Dobles de servicios externos. Sin red, claves ni afirmaciones de durabilidad."""
import json

class ServidorSimulado:
    def __init__(self):
        self.aceptados = {}

    def recibir(self, datos):
        # Modelo secuencial de aceptación idempotente; no es Redis ni PostgreSQL.
        self.aceptados.setdefault(datos["uuid"], dict(datos))
        return 202

class APIRegionalSDK:
    """Interfaz A: dict -> dict, con timeout ANTES de aceptar."""
    def __init__(self, fallas=0, codigo=202, servidor=None):
        self.fallas, self.codigo, self.llamadas = fallas, codigo, 0
        self.servidor = servidor or ServidorSimulado()

    def publicar(self, datos):
        self.llamadas += 1
        if self.llamadas <= self.fallas:
            raise TimeoutError("Red regional sin respuesta")
        if self.codigo == 202:
            self.servidor.recibir(datos)
        return {"codigo": self.codigo}

class APIAlternaClient:
    """Interfaz B: JSON serializado -> código HTTP entero."""
    def __init__(self, fallas=0, codigo=202, servidor=None):
        self.fallas, self.codigo, self.llamadas = fallas, codigo, 0
        self.servidor = servidor or ServidorSimulado()

    def send(self, payload):
        self.llamadas += 1
        if self.llamadas <= self.fallas:
            raise TimeoutError("Red alterna sin respuesta")
        if self.codigo == 202:
            self.servidor.recibir(json.loads(payload))
        return self.codigo

class ClienteLLMFalso:
    """Respuesta fija, no evalúa daños reales ni mide exactitud predictiva."""
    def __init__(self, respuesta='{"severidad":"MODERADO","confianza":0.8}'):
        self.respuesta, self.llamadas = respuesta, 0

    def completar(self, prompt):
        self.llamadas += 1
        return self.respuesta

class ModeloLocalFalso:
    def __init__(self, respuesta='{"severidad":"LEVE","confianza":0.6}'):
        self.respuesta, self.llamadas = respuesta, 0

    def generate(self, model, prompt):
        self.llamadas += 1
        return {"response": self.respuesta}
