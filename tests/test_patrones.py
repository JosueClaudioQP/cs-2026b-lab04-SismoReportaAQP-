import pytest
from reportes.dominio import EstadoReporte as E
from reportes.despues.servicio import ServicioReportes, Reporte
from reportes.despues.transporte import CanalEnvio, ConReintentos, RegionalAdapter, AlternaAdapter
from reportes.despues.eventos import Suscriptor
from reportes.despues.ia import LocalAdapter, ProveedorLLM, ConCache
from reportes.externos import APIRegionalSDK, APIAlternaClient, ModeloLocalFalso

class CanalNuevo(CanalEnvio):
    def enviar(self, reporte):
        return 202

def test_open_closed_nuevo_canal_por_registro():
    s = ServicioReportes()
    s.fabrica.registrar("NUEVO", CanalNuevo)
    r = Reporte("grieta")
    s.registrar(r)
    assert s.sincronizar(r, "NUEVO") == "ACEPTADO"

def test_adapters_equivalentes_y_payload():
    a, b = APIRegionalSDK(), APIAlternaClient()
    r = Reporte("grieta", uuid="id-1")
    assert RegionalAdapter(a).enviar(r) == AlternaAdapter(b).enviar(r) == 202
    assert a.servidor.aceptados == b.servidor.aceptados

def test_observer_tercer_suscriptor():
    class Contador(Suscriptor):
        def __init__(self):
            self.ids = []
        def actualizar(self, evento):
            self.ids.append(evento.reporte_id)
    s, contador = ServicioReportes(), Contador()
    s.publicador.suscribir(contador)
    r = Reporte("grieta")
    s.registrar(r)
    s.sincronizar(r)
    assert contador.ids == [r.uuid] and len(s.eventos) == 2

def test_decorator_no_reintenta_error_de_programacion():
    class Roto(CanalEnvio):
        def __init__(self):
            self.llamadas = 0
        def enviar(self, reporte):
            self.llamadas += 1
            raise RuntimeError("fallo no transitorio")
    interno = Roto()
    with pytest.raises(RuntimeError):
        ConReintentos(interno).enviar(Reporte("grieta"))
    assert interno.llamadas == 1

def test_decorator_valida_numero_intentos():
    with pytest.raises(ValueError):
        ConReintentos(CanalNuevo(), 0)

def test_segundo_proveedor_ia_sin_modificar_servicio():
    modelo = ModeloLocalFalso()
    s = ServicioReportes(proveedor=LocalAdapter(modelo))
    assert s.sugerir_severidad("grieta").severidad == "LEVE"
    assert modelo.llamadas == 1

def test_cache_no_guarda_excepciones():
    class Intermitente(ProveedorLLM):
        def __init__(self):
            self.llamadas = 0
        def completar(self, prompt):
            self.llamadas += 1
            if self.llamadas == 1:
                raise TimeoutError()
            return "ok"
    proveedor = Intermitente()
    cache = ConCache(proveedor)
    with pytest.raises(TimeoutError):
        cache.completar("p")
    assert cache.completar("p") == cache.completar("p") == "ok"
    assert proveedor.llamadas == 2

@pytest.mark.parametrize("origen", list(E))
@pytest.mark.parametrize("accion", ["encolar", "reintentar", "marcar_recibido", "verificar", "marcar_atendido"])
def test_state_matriz_completa(origen, accion):
    r = Reporte("grieta")
    camino = [r.encolar, r.marcar_recibido, lambda: r.verificar("LEVE"), r.marcar_atendido]
    r.asignar_brigada("B-01")
    for paso in camino[:list(E).index(origen)]:
        paso()
    permitidas = {
        (E.BORRADOR, "encolar"): E.ENCOLADO,
        (E.ENCOLADO, "reintentar"): E.ENCOLADO,
        (E.ENCOLADO, "marcar_recibido"): E.RECIBIDO,
        (E.RECIBIDO, "verificar"): E.VERIFICADO,
        (E.VERIFICADO, "marcar_atendido"): E.ATENDIDO,
    }
    args = ("LEVE",) if accion == "verificar" else ()
    destino = permitidas.get((origen, accion))
    if destino is None:
        with pytest.raises(ValueError):
            getattr(r, accion)(*args)
        assert r.estado == origen
    else:
        getattr(r, accion)(*args)
        assert r.estado == destino
