"""Regenera evidencia y tablas desde el código actual. Ejecutar desde la raíz."""
import json
import platform
import subprocess
import sys
from pathlib import Path
from radon.complexity import cc_visit, cc_rank
from radon.raw import analyze
from importlib.metadata import version

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "docs/design/patrones/evidencias"
DESTINO.mkdir(parents=True, exist_ok=True)
resumen, detalle = {}, []
for variante in ("antes", "despues"):
    ruta = f"src/reportes/{variante}"
    for nombre, args in (("cc", ["cc", "-s", "-a"]), ("raw", ["raw", "-s"]), ("mi", ["mi", "-s"])):
        salida = subprocess.run([sys.executable, "-m", "radon", *args, ruta], cwd=RAIZ, text=True, capture_output=True, check=True)
        (DESTINO / f"radon-{nombre}-{variante}.txt").write_text(salida.stdout, encoding="utf-8")
    bloques, metodos, sloc = [], [], 0
    for archivo in sorted((RAIZ/ruta).rglob("*.py")):
        codigo = archivo.read_text(encoding="utf-8")
        sloc += analyze(codigo).sloc
        analisis = cc_visit(codigo)
        for bloque in analisis:
            bloques.append(bloque.complexity)
            if not hasattr(bloque, "methods"):
                metodos.append(bloque.complexity)
                nombre = f"{bloque.classname}.{bloque.name}" if bloque.classname else bloque.name
                detalle.append((variante, archivo.name, nombre, bloque.complexity))
    resumen[variante] = {"sloc":sloc, "bloques":len(bloques), "promedio_radon":sum(bloques)/len(bloques), "metodos":len(metodos), "promedio_metodos":sum(metodos)/len(metodos), "maximo_metodo":max(metodos)}
(DESTINO/'resumen.json').write_text(json.dumps(resumen,indent=2),encoding='utf-8')
filas = ["| Indicador | Antes | Después |", "|---|---:|---:|"]
for etiqueta, clave in [("SLOC", "sloc"), ("Bloques Radon (clases + métodos)", "bloques"), ("CC promedio Radon", "promedio_radon"), ("Métodos/funciones", "metodos"), ("CC promedio solo métodos", "promedio_metodos"), ("CC máxima de un método", "maximo_metodo")]:
    a,b=resumen['antes'][clave],resumen['despues'][clave]
    if isinstance(a,float): a,b=f"{a:.2f}",f"{b:.2f}"
    filas.append(f"| {etiqueta} | {a} | {b} |")
tabla='\n'.join(filas)
(DESTINO/'tabla-resumen.md').write_text(tabla+'\n',encoding='utf-8')
contenido = f"""# E6. Métricas y trade-off

Entorno medido: Python {platform.python_version()}, radon {version('radon')}, pytest {version('pytest')}.
Reproducir: `python tools/medir_lab07.py` desde la raíz.

## Alcance y criterio de comparación
Se comparan TODOS los archivos de `src/reportes/antes/` y `src/reportes/despues/`.
Ambas versiones soportan el mismo contrato observable de envío, estados y sugerencia IA.
Se excluyen de ambas las pruebas, los SDK simulados, `datos_lab07.py` y el esqueleto Lab 05.
Esas dependencias comunes no se trasladaron de antes a después para ocultar complejidad.
El promedio de Radon incluye clases y métodos; también se informa el promedio solo de métodos.
El incremento de clases puede reducir el promedio: por eso se publica máximo, SLOC y detalle.

{tabla}

## Trade-off (7 líneas)
1. La sincronización pasa de CC 11 a 4 al separar selección, traducción y reintentos.
2. El método de IA pasa de CC 13 a 1 en la fachada; la lógica continúa en los guardrails (no desaparece).
3. Los nuevos canales se registran sin cambiar el algoritmo del servicio, como prueba el test Open/Closed.
4. El costo es más SLOC, objetos y archivos, con mayor esfuerzo de navegación y aprendizaje.
5. Las mismas pruebas protegen resultados, errores, eventos y reintentos antes y después.
6. Para un único canal estable, sin IA ni cambios de estado complejos, la versión inicial podría bastar.
7. Se justifica aquí por las variaciones del laboratorio; estas métricas no prueban rendimiento ni exactitud de IA.

## Patrón rechazado
Singleton para fábricas/LLM: no hay necesidad de instancia global y contaminaría registros y cachés entre pruebas.
También se descarta Abstract Factory: no hay familias completas de productos relacionados.
La Factory por registro es simple, no se contabiliza como Factory Method GoF estricto.

## Complejidad por método (todos)
| Versión | Archivo | Método | CC | Rango |
|---|---|---|---:|---|
"""
for variante,archivo,metodo,cc in detalle:
    contenido += f"| {variante} | {archivo} | `{metodo}` | {cc} | {cc_rank(cc)} |\n"
contenido += "\nSalidas crudas: [evidencias/](evidencias/). MI se conserva como dato complementario; no se usa para afirmar calidad absoluta.\n"
(RAIZ/'docs/design/patrones/metricas.md').write_text(contenido,encoding='utf-8')
print(tabla)
