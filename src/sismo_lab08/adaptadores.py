import sqlite3
from sismo_lab08.dominio import Repositorio, CanalSMS
class SQLiteRepositorio:
    """Prototipo de inbox durable. No reemplaza mediciones de PostgreSQL."""
    def __init__(self, ruta):
        self.db = sqlite3.connect(str(ruta))
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS reportes(uuid TEXT PRIMARY KEY, payload TEXT NOT NULL, brigada TEXT);
        CREATE TABLE IF NOT EXISTS sms(uuid TEXT PRIMARY KEY, brigada TEXT NOT NULL, enviado INTEGER DEFAULT 0);
        """)
    def recibir(self, uuid, payload):
        with self.db:
            previo = self.db.execute('SELECT payload FROM reportes WHERE uuid=?', (uuid,)).fetchone()
            if previo and previo[0] != payload: raise ValueError('UUID con payload distinto')
            self.db.execute('INSERT OR IGNORE INTO reportes(uuid,payload) VALUES (?,?)', (uuid,payload))
        return previo is None
    def asignar(self, uuid, brigada):
        with self.db:
            cur=self.db.execute('UPDATE reportes SET brigada=? WHERE uuid=?', (brigada,uuid))
            if not cur.rowcount: raise KeyError(uuid)
            self.db.execute('INSERT INTO sms(uuid,brigada,enviado) VALUES (?,?,0) ON CONFLICT(uuid) DO UPDATE SET brigada=excluded.brigada,enviado=0', (uuid,brigada))
    def sms_pendientes(self): return self.db.execute('SELECT uuid,brigada FROM sms WHERE enviado=0').fetchall()
    def confirmar_sms(self, uuid):
        with self.db: self.db.execute('UPDATE sms SET enviado=1 WHERE uuid=?', (uuid,))
    def total(self): return self.db.execute('SELECT count(*) FROM reportes').fetchone()[0]
    def cerrar(self): self.db.close()
class SMSCaido:
    def enviar(self, uuid, brigada): raise TimeoutError('Proveedor SMS caído')
