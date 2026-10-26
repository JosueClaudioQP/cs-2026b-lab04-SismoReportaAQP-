# E7. Consistencia UML ↔ código

Se actualiza `docs/design/clases.puml` con la vista resumida del experimento.
Se conserva `clases-lab05.puml` con el diseño original; no se borran los artefactos
históricos de los laboratorios anteriores. Las vistas detalladas están en
`patrones/*.puml`, una por patrón aplicado.

## Reproducción de ingeniería inversa
Desde la raíz, después de instalar requirements-lab07.txt:
```bash
pyreverse -o puml -p lab07 -d docs/design/patrones/evidencias src/reportes/despues
python tools/verificar_roundtrip.py
```
En el entorno de preparación se ejecutó el equivalente:
```bash
python -c "from pylint import run_pyreverse; run_pyreverse()" -o puml -p lab07 -d docs/design/patrones/evidencias src/reportes/despues
```
Se configuró PYTHONPATH=src para resolver imports. Con PowerShell:
`$env:PYTHONPATH="src"`; con bash: `export PYTHONPATH=src`.
Salidas reales: `evidencias/classes_lab07.puml` y `packages_lab07.puml`.

| Vista | Correspondencia comprobada |
|---|---|
| Strategy / Adapter | CanalEnvio, RegionalAdapter y AlternaAdapter declaran enviar; las dos clases heredan del puerto |
| Factory | FabricaCanales registra creadores por instancia y devuelve CanalEnvio; creación por registro, no herencia GoF |
| State | Reporte contiene _estado: Estado; Borrador, Encolado, Recibido, Verificado y Atendido heredan de Estado |
| Observer | Publicador contiene suscriptores; PanelObserver y AuditoriaObserver implementan actualizar |
| Decorator | ConReintentos hereda de CanalEnvio y contiene otro CanalEnvio; ConCache hace lo mismo con ProveedorLLM |
| Chain | FormatoJSON, SeveridadPermitida y ConfianzaValida heredan de Guardrail; siguiente encadena validaciones |
| IA | ClasificadorSeveridad recibe proveedor y guardrails; devuelve Sugerencia sin modificar Reporte |

El verificador compara el conjunto completo de clases Python con los alias
cualificados de pyreverse. Las operaciones y herencias anteriores se revisan
contra código/diagrama y mediante las pruebas de patrones.
Pyreverse no reconstruye intención GoF, propiedad del ciclo de vida ni cardinalidad
solo a partir de tipos. Por ello los estereotipos, composiciones y multiplicidades
se documentan manualmente. Los estados son clases, no renombrados del enum: la
propiedad estado expone el enum existente para mantener el contrato observable.

La secuencia detalla el camino exitoso; los errores y el estado sin conectividad
se cubren en test_comportamiento.py. La llamada procesar() representa el worker
simulado: no hay proceso separado ni cola real en esta práctica.
