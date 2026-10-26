"""Falla si un método/función del código refactorizado supera CC 10.
Radon --min C solo filtra: por sí solo NO hace fallar GitHub Actions.
"""
import sys
from pathlib import Path
from radon.complexity import cc_visit

RAIZ = Path(__file__).resolve().parents[1]
carpetas = [RAIZ / "src/reportes/despues"]
fallos = []
for carpeta in carpetas:
    for archivo in sorted(carpeta.rglob("*.py")):
        for bloque in cc_visit(archivo.read_text(encoding="utf-8")):
            candidatos = [] if hasattr(bloque, "methods") else [bloque]
            for funcion in candidatos:
                if funcion.complexity > 10:
                    fallos.append(f"{archivo.relative_to(RAIZ)}:{funcion.lineno} {funcion.name}: {funcion.complexity}")
if fallos:
    print("\n".join(fallos))
    sys.exit(1)
print("OK: todos los métodos/funciones de despues tienen CC <= 10.")
