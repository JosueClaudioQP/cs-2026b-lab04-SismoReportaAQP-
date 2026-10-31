"""Experimento de eventos discretos; parámetros hipotéticos, no benchmark del VPS."""
import random, heapq, math, statistics
def llegadas(perfil, seed=7, n=20000):
    r=random.Random(seed)
    if perfil=='uniforme': return sorted(r.uniform(0,3600) for _ in range(n))
    if perfil=='rafaga': return sorted([r.uniform(0,600) for _ in range(n//2)]+[r.uniform(600,3600) for _ in range(n-n//2)])
    if perfil=='reconexion': return sorted(r.uniform(0,300) for _ in range(n))
    raise ValueError(perfil)
def cola(arrivals, workers, media_s, seed=17, cv=.45):
    r=random.Random(seed); libres=[0.]*workers; heapq.heapify(libres)
    sigma=math.sqrt(math.log(1+cv*cv)); mu=math.log(media_s)-sigma*sigma/2
    lat=[]; fines=[]
    for a in arrivals:
        libre=heapq.heappop(libres); fin=max(a,libre)+r.lognormvariate(mu,sigma)
        heapq.heappush(libres,fin); lat.append((fin-a)*1000); fines.append(fin)
    lat.sort()
    return {'n':len(lat),'p50_ms':lat[int(.5*(len(lat)-1))], 'p95_ms':lat[int(.95*(len(lat)-1))],
            'max_ms':max(lat),'fin_s':max(fines),'fines':fines}
def medir(perfil, tactica, seed=7):
    a=llegadas(perfil,seed)
    if tactica=='sincrono': r=cola(a,4,.55)
    elif tactica=='8_workers': r=cola(a,8,.55)
    elif tactica=='ingesta_durable': r=cola(a,4,.035)
    else: raise ValueError(tactica)
    if tactica=='ingesta_durable':
        procesados=cola(sorted(r['fines']),2,.12)
        r['drenaje_s']=max(0,procesados['fin_s']-max(a))
    return {k:v for k,v in r.items() if k!='fines'}
if __name__=='__main__':
    for p in ['uniforme','rafaga','reconexion']:
        for t in ['sincrono','8_workers','ingesta_durable']:
            print(p,t,medir(p,t))
