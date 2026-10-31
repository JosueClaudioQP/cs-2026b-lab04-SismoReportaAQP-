from pathlib import Path
import json, sys, statistics, tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT)]
from fitness.rendimiento import medir, cola, llegadas
from fitness.disponibilidad import experimentar
from reportes.servicios import SyncManager
from reportes.dominio import Reporte
from decimal import Decimal
rows=[]
for p in ['uniforme','rafaga','reconexion']:
    for t in ['sincrono','8_workers','ingesta_durable']:
        base=medir(p,t)
        seeds=[medir(p,t,s)['p95_ms'] for s in range(30)]
        rows.append({'perfil':p,'tactica':t,**base,'p95_30_min':min(seeds),'p95_30_max':max(seeds),'p95_30_media':statistics.mean(seeds)})
with tempfile.TemporaryDirectory() as tmp: dispo=experimentar(Path(tmp))
cliente=SyncManager()
for i in range(20000): cliente.registrar(Reporte(Decimal('-16'),Decimal('-71'),f'reporte-{i}'))
antes=len(cliente._pendientes)
cliente=SyncManager()  # nuevo proceso lógico: el esqueleto previo solo usa un dict
baseline={'pendientes_antes':antes,'pendientes_tras_recrear':len(cliente._pendientes),'sin_copia_durable':antes-len(cliente._pendientes)}
sens=[{'media_servicio_ms':m,'p95_ms':cola(llegadas('reconexion'),4,m/1000)['p95_ms']} for m in [20,35,50,60,80]]
out=ROOT/'docs/architecture/evidencia'; out.mkdir(parents=True,exist_ok=True)
result={'rendimiento':rows,'disponibilidad':dispo,'baseline_memoria':baseline,'sensibilidad':sens,'nota':'Tiempos de servicio supuestos; SQLite local no equivale a PostgreSQL ni a una medición del VPS.'}
(out/'resultados.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
