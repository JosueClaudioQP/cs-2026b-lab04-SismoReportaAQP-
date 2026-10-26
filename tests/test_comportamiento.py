"""La misma red de seguridad corre en ambas implementaciones."""
import importlib
import json
import pytest
from reportes.dominio import EstadoReporte as E
from reportes.externos import APIRegionalSDK, APIAlternaClient, ClienteLLMFalso, ServidorSimulado

@pytest.fixture(params=["antes", "despues"])
def m(request):
    return importlib.import_module(f"reportes.{request.param}.servicio")

def preparar(m, **kwargs):
    servicio = m.ServicioReportes(**kwargs)
    reporte = m.Reporte("Grietas en pared", uuid="reporte-001")
    servicio.registrar(reporte)
    return servicio, reporte

@pytest.mark.parametrize("canal", ["REGIONAL", "ALTERNA"])
def test_envio_aceptado_y_eventos(m, canal):
    s, r = preparar(m)
    assert s.sincronizar(r, canal) == "ACEPTADO"
    assert r.uuid not in s.pendientes
    assert s.eventos == ["panel:reporte-001:ACEPTADO", "auditoria:reporte-001:ACEPTADO"]

def test_offline_conserva_pendiente_sin_llamar_sdk(m):
    sdk = APIRegionalSDK()
    s, r = preparar(m, regional=sdk)
    assert s.sincronizar(r, conectado=False) == "PENDIENTE"
    assert s.pendientes[r.uuid] is r and sdk.llamadas == 0
    assert r.estado == E.ENCOLADO and s.eventos == []

@pytest.mark.parametrize("canal,clase,arg", [("REGIONAL", APIRegionalSDK, "regional"), ("ALTERNA", APIAlternaClient, "alterna")])
def test_dos_timeouts_y_exito(m, canal, clase, arg):
    sdk = clase(fallas=2)
    s, r = preparar(m, **{arg: sdk})
    assert s.sincronizar(r, canal) == "ACEPTADO"
    assert sdk.llamadas == 3

@pytest.mark.parametrize("canal,clase,arg", [("REGIONAL", APIRegionalSDK, "regional"), ("ALTERNA", APIAlternaClient, "alterna")])
def test_agota_reintentos_y_conserva_reporte(m, canal, clase, arg):
    sdk = clase(fallas=3)
    s, r = preparar(m, **{arg: sdk})
    assert s.sincronizar(r, canal) == "PENDIENTE"
    assert sdk.llamadas == 3 and r.uuid in s.pendientes and not s.eventos
    assert s.sincronizar(r, canal) == "ACEPTADO"

@pytest.mark.parametrize("codigo", [400, 409, 429, 503])
def test_respuesta_http_no_se_reintenta_en_el_mismo_ciclo(m, codigo):
    sdk = APIRegionalSDK(codigo=codigo)
    s, r = preparar(m, regional=sdk)
    assert s.sincronizar(r) == "PENDIENTE"
    assert sdk.llamadas == 1 and r.uuid in s.pendientes and not s.eventos

def test_canal_desconocido_no_muta(m):
    s, r = preparar(m)
    with pytest.raises(ValueError, match="Canal"):
        s.sincronizar(r, "INEXISTENTE")
    assert r.estado == E.ENCOLADO and r.uuid in s.pendientes and not s.eventos

@pytest.mark.parametrize("descripcion,lat,lon", [(" ", -16, -71), ("x"*1001, -16, -71), ("grieta", 91, 0), ("grieta", 0, -181), ("grieta", float('nan'), 0)])
def test_datos_invalidos_no_se_registran(m, descripcion, lat, lon):
    s = m.ServicioReportes()
    r = m.Reporte(descripcion, lat, lon)
    with pytest.raises(ValueError):
        s.registrar(r)
    assert r.estado == E.BORRADOR and not s.pendientes

def test_limites_validos(m):
    s = m.ServicioReportes()
    r = m.Reporte("x"*1000, 90, -180)
    s.registrar(r)
    assert s.sincronizar(r) == "ACEPTADO"

def test_202_no_significa_procesado(m):
    s, r = preparar(m)
    s.sincronizar(r)
    assert r.estado == E.ENCOLADO
    s.procesar(r)
    assert r.estado == E.RECIBIDO

def test_ciclo_de_vida_completo(m):
    s, r = preparar(m)
    s.sincronizar(r)
    s.procesar(r)
    r.verificar("SEVERO")
    r.asignar_brigada("B-01")
    r.marcar_atendido()
    assert r.estado == E.ATENDIDO and r.nivel_danio == "SEVERO"

def test_verificar_borrador_es_invalido(m):
    r = m.Reporte("grieta")
    with pytest.raises(ValueError):
        r.verificar("LEVE")
    assert r.estado == E.BORRADOR and r.nivel_danio is None

def test_atender_sin_brigada_es_invalido(m):
    s, r = preparar(m)
    s.procesar(r)
    r.verificar("LEVE")
    with pytest.raises(ValueError, match="Brigada"):
        r.marcar_atendido()
    assert r.estado == E.VERIFICADO

def test_reencolar_atendido_es_invalido(m):
    s, r = preparar(m)
    s.procesar(r)
    r.verificar("LEVE")
    r.asignar_brigada("B-01")
    r.marcar_atendido()
    with pytest.raises(ValueError):
        r.encolar()
    assert r.estado == E.ATENDIDO

def test_uuid_idempotente_en_servidor_simulado(m):
    servidor = ServidorSimulado()
    s, r = preparar(m, regional=APIRegionalSDK(servidor=servidor))
    s.sincronizar(r)
    s.sincronizar(r)  # reenvío del mismo UUID: 202 también para duplicado
    assert len(servidor.aceptados) == 1

def test_respuesta_perdida_despues_de_aceptar(m):
    class RespuestaPerdida(APIRegionalSDK):
        def publicar(self, datos):
            respuesta = super().publicar(datos)
            if self.llamadas == 1:
                raise TimeoutError("Se perdió el 202, no el mensaje")
            return respuesta
    sdk = RespuestaPerdida()
    s, r = preparar(m, regional=sdk)
    assert s.sincronizar(r) == "ACEPTADO"
    assert sdk.llamadas == 2 and len(sdk.servidor.aceptados) == 1
    assert len(s.eventos) == 2

def test_ia_sugiere_sin_cambiar_el_reporte(m):
    s, r = preparar(m)
    resultado = s.sugerir_severidad(r.descripcion)
    assert resultado.severidad == "MODERADO" and resultado.requiere_revision
    assert r.nivel_danio is None and r.estado == E.ENCOLADO

def test_cache_ia(m):
    llm = ClienteLLMFalso()
    s = m.ServicioReportes(llm=llm)
    assert s.sugerir_severidad("grieta") == s.sugerir_severidad("grieta")
    assert llm.llamadas == 1
    s.sugerir_severidad("colapso")
    assert llm.llamadas == 2

@pytest.mark.parametrize("respuesta", [
    "no JSON", "[]", "x"*257,
    '{"severidad":"SEGURO","confianza":0.8}',
    '{"severidad":"LEVE","confianza":2}',
    '{"severidad":"LEVE","confianza":true}',
    '{"severidad":"LEVE","confianza":NaN}',
    '{"severidad":"LEVE","confianza":"0.9"}',
    '{"severidad":"LEVE","confianza":0.9,"habitable":true}',
    '{"severidad":["LEVE"],"confianza":0.9}',
])
def test_guardrails_bloquean_respuestas_invalidas(m, respuesta):
    s = m.ServicioReportes(llm=ClienteLLMFalso(respuesta))
    with pytest.raises(ValueError, match="Guardrail"):
        s.sugerir_severidad("grieta")

@pytest.mark.parametrize("nivel", ["LEVE", "MODERADO", "SEVERO"])
@pytest.mark.parametrize("confianza", [0, 1])
def test_ia_valores_permitidos_y_limites(m, nivel, confianza):
    s = m.ServicioReportes(llm=ClienteLLMFalso(json.dumps({"severidad": nivel, "confianza": confianza})))
    assert s.sugerir_severidad("grieta").severidad == nivel
