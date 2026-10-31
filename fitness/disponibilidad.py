"""Inyección de ACK perdido después de persistir y reapertura de SQLite."""
import sqlite3, json
from sismo_lab08.bootstrap import crear
def experimentar(carpeta, n=20000):
    local=sqlite3.connect(str(carpeta/'local.db'))
    local.execute('CREATE TABLE pendientes(uuid TEXT PRIMARY KEY,payload TEXT,ack INTEGER DEFAULT 0)')
    with local:
        local.executemany('INSERT INTO pendientes(uuid,payload) VALUES (?,?)',
                          ((f'reporte-{i}',json.dumps({'descripcion':f'daño-{i}'})) for i in range(n)))
    local.close()  # reinicio de aplicación después de registrar sin red
    local=sqlite3.connect(str(carpeta/'local.db'))
    repo,ingesta,_=crear(carpeta/'servidor.db'); intentos=0; ack_perdidos=0
    for i,(uuid,payload) in enumerate(local.execute('SELECT uuid,payload FROM pendientes').fetchall()):
        ingesta.recibir(uuid,payload); intentos+=1
        if i%7==0: ack_perdidos+=1; continue # servidor aceptó, cliente desconoce el resultado
        local.execute('UPDATE pendientes SET ack=1 WHERE uuid=?',(uuid,))
    local.commit(); repo.cerrar()
    repo,ingesta,_=crear(carpeta/'servidor.db') # reinicio del servidor antes del replay
    for uuid,payload in local.execute('SELECT uuid,payload FROM pendientes WHERE ack=0').fetchall():
        ingesta.recibir(uuid,payload); intentos+=1
        local.execute('UPDATE pendientes SET ack=1 WHERE uuid=?',(uuid,))
    local.commit()
    pendientes=local.execute('SELECT count(*) FROM pendientes WHERE ack=0').fetchone()[0]
    r={'creados':n,'persistidos':repo.total(),'perdidos':n-repo.total(),'duplicados':max(0,repo.total()-n),
       'pendientes':pendientes,'intentos':intentos,'ack_perdidos':ack_perdidos}
    repo.cerrar(); local.close(); return r
