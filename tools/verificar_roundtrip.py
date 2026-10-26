"""Contrasta nombres cualificados de clases Python con salida real de pyreverse."""
import ast
import re
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[1]
fuente = RAIZ / "src/reportes/despues"
esperadas = set()
for archivo in fuente.glob("*.py"):
    for nodo in ast.parse(archivo.read_text(encoding="utf-8")).body:
        if isinstance(nodo, ast.ClassDef):
            esperadas.add(f"reportes.despues.{archivo.stem}.{nodo.name}")
puml = (RAIZ / "docs/design/patrones/evidencias/classes_lab07.puml").read_text(encoding="utf-8")
observadas = set(re.findall(r'class "[^"]+" as ([\w.]+)', puml))
assert esperadas == observadas, {"faltantes": sorted(esperadas-observadas), "sobrantes": sorted(observadas-esperadas)}
print(f"OK: {len(esperadas)} clases Python coinciden con pyreverse.")
print("Esta comprobación cubre existencia; no acredita automáticamente composición ni multiplicidad UML.")
