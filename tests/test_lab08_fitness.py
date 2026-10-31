import pytest
from fitness.rendimiento import medir, cola, llegadas
from fitness.disponibilidad import experimentar
from sismo_lab08.bootstrap import crear
from sismo_lab08.aplicacion.operaciones import despachar_sms
from sismo_lab08.adaptadores import SMSCaido
@pytest.mark.parametrize('perfil',['uniforme','rafaga','reconexion'])
def test_ff03_p95_ingesta(perfil):
    assert medir(perfil,'ingesta_durable')['p95_ms']<=2000
def test_ff04_reinicio_replay_cero_perdidas(tmp_path):
    r=experimentar(tmp_path)
    assert r['persistidos']==20000 and r['perdidos']==r['duplicados']==r['pendientes']==0
def test_ff07_cola_se_drena_en_20_minutos():
    assert medir('reconexion','ingesta_durable')['drenaje_s']<=1200
def test_ff05_sms_caido_no_revierte_asignacion(tmp_path):
    repo,ingesta,ops=crear(tmp_path/'s.db'); ingesta.recibir('a','{}')
    ops.asignar('coordinador','a','B1')
    assert despachar_sms(repo,SMSCaido())==0
    repo.cerrar(); repo,_,_=crear(tmp_path/'s.db')
    assert repo.db.execute('SELECT brigada FROM reportes WHERE uuid=?',('a',)).fetchone()[0]=='B1'
    assert repo.sms_pendientes()==[('a','B1')]; repo.cerrar()
@pytest.mark.parametrize('rol',['ciudadano','brigadista','anonimo','operador_lectura'])
def test_ff06_rbac_rechaza_asignacion(tmp_path,rol):
    repo,ingesta,ops=crear(tmp_path/'s.db'); ingesta.recibir('a','{}')
    with pytest.raises(PermissionError): ops.asignar(rol,'a','B1')
    assert repo.db.execute('SELECT brigada FROM reportes').fetchone()[0] is None
    repo.cerrar()
def test_uuid_repetido_con_payload_distinto_se_rechaza(tmp_path):
    repo,ingesta,_=crear(tmp_path/'s.db'); ingesta.recibir('a','original')
    with pytest.raises(ValueError): ingesta.recibir('a','modificado')
    assert repo.total()==1; repo.cerrar()
def test_sensibilidad_disco_lento_supera_presupuesto():
    # Reconexión: 66.7 req/s; media 80 ms supera capacidad 4/.08=50 req/s.
    assert cola(llegadas('reconexion'),4,.08)['p95_ms']>2000
