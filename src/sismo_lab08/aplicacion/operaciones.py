from sismo_lab08.dominio import Repositorio, CanalSMS
class Operaciones:
    def __init__(self, repo: Repositorio): self.repo = repo
    def asignar(self, rol, uuid, brigada):
        if rol != 'coordinador': raise PermissionError('No autorizado')
        self.repo.asignar(uuid, brigada)  # transacción: asignación + outbox SMS
def despachar_sms(repo, canal: CanalSMS):
    enviados = 0
    for uuid, brigada in repo.sms_pendientes():
        try: canal.enviar(uuid, brigada)
        except TimeoutError: continue
        repo.confirmar_sms(uuid); enviados += 1
    return enviados
