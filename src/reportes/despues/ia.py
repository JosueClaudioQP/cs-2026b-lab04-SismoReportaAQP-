"""Sugerencia de severidad: proveedor sustituible, caché y tres guardrails."""
import json
from abc import ABC, abstractmethod
from math import isfinite
from ..datos_lab07 import NivelDanio, Sugerencia, prompt_clasificacion

class ProveedorLLM(ABC):
    @abstractmethod
    def completar(self, prompt: str) -> str:
        pass

class LLMAdapter(ProveedorLLM):
    def __init__(self, cliente):
        self._cliente = cliente
    def completar(self, prompt):
        return self._cliente.completar(prompt)

class LocalAdapter(ProveedorLLM):
    def __init__(self, modelo):
        self._modelo = modelo
    def completar(self, prompt):
        return self._modelo.generate("simulado", prompt)["response"]

class ConCache(ProveedorLLM):
    def __init__(self, interno: ProveedorLLM):
        self._interno, self._cache = interno, {}
    def completar(self, prompt):
        if prompt not in self._cache:
            self._cache[prompt] = self._interno.completar(prompt)
        return self._cache[prompt]

class Guardrail(ABC):
    def __init__(self, siguiente=None):
        self._siguiente = siguiente
    def validar(self, valor):
        resultado = self.aplicar(valor)
        return self._siguiente.validar(resultado) if self._siguiente else resultado
    @abstractmethod
    def aplicar(self, valor):
        pass

class FormatoJSON(Guardrail):
    def aplicar(self, texto):
        if not isinstance(texto, str) or len(texto) > 256:
            raise ValueError("Guardrail: longitud o tipo")
        try:
            return json.loads(texto)
        except (ValueError, TypeError) as exc:
            raise ValueError("Guardrail: JSON inválido") from exc

class SeveridadPermitida(Guardrail):
    def aplicar(self, datos):
        if not isinstance(datos, dict) or set(datos) != {"severidad", "confianza"}:
            raise ValueError("Guardrail: esquema")
        if datos["severidad"] not in [n.value for n in NivelDanio]:
            raise ValueError("Guardrail: severidad")
        return datos

class ConfianzaValida(Guardrail):
    def aplicar(self, datos):
        confianza = datos["confianza"]
        # bool hereda de int: debe rechazarse explícitamente por tipo exacto.
        if type(confianza) not in (int, float):
            raise ValueError("Guardrail: confianza")
        if not isfinite(confianza) or not 0 <= confianza <= 1:
            raise ValueError("Guardrail: confianza")
        return datos

class ClasificadorSeveridad:
    def __init__(self, proveedor: ProveedorLLM, guardrails: Guardrail):
        self._proveedor, self._guardrails = proveedor, guardrails
    def sugerir(self, descripcion):
        if not descripcion.strip():
            raise ValueError("Descripción vacía")
        texto = self._proveedor.completar(prompt_clasificacion(descripcion))
        datos = self._guardrails.validar(texto)
        return Sugerencia(datos["severidad"], float(datos["confianza"]))
