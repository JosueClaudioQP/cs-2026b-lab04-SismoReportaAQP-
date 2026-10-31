from sismo_lab08.adaptadores import SQLiteRepositorio
from sismo_lab08.aplicacion.ingesta import Ingesta
from sismo_lab08.aplicacion.operaciones import Operaciones
def crear(ruta):
    repo=SQLiteRepositorio(ruta)
    return repo, Ingesta(repo), Operaciones(repo)
