"""Ejecutar: PYTHONPATH=src python -m reportes.demo_lab07 (o configurar PYTHONPATH)."""
from .despues.servicio import ServicioReportes, Reporte

def main():
    servicio = ServicioReportes()
    reporte = Reporte("Grietas diagonales en una pared", uuid="demo-001")
    servicio.registrar(reporte)
    print("Sin señal:", servicio.sincronizar(reporte, conectado=False))
    print("Con señal:", servicio.sincronizar(reporte), reporte.estado.value)
    servicio.procesar(reporte)
    print("Procesado:", reporte.estado.value)
    print("Sugerencia simulada:", servicio.sugerir_severidad(reporte.descripcion))
    reporte.verificar("MODERADO")  # decisión explícita del operador
    reporte.asignar_brigada("BR-01")
    reporte.marcar_atendido()
    print("Estado final:", reporte.estado.value)
    print("Observadores:", servicio.eventos)

if __name__ == "__main__":
    main()
