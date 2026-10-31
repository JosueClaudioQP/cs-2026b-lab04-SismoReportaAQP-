from sismo_lab08.dominio import Repositorio
class Ingesta:
    def __init__(self, repo: Repositorio): self.repo = repo
    def recibir(self, uuid, payload):
        if not uuid: raise ValueError('UUID requerido')
        self.repo.recibir(uuid, payload)
        return 202  # incluye repetición idéntica; conflicto -> ValueError
