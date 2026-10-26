# Cuestionario — Laboratorio 07

1. **Arquitectura frente a diseño.** El monolito modular con cola organiza el
sistema completo (Lab 04). State organiza cómo Reporte delega sus transiciones
a objetos de estado. Operan a escalas diferentes.

2. **Strategy y OCP.** ServicioReportes usa CanalEnvio. El test Open/Closed crea
CanalNuevo y registra su constructor en FabricaCanales; no cambia sincronizar.
Se extiende la configuración y se agrega una implementación del puerto.

3. **Adapter frente a Decorator.** AlternaAdapter traduce payload a JSON y el
contrato `send()` a `enviar()`. ConReintentos conserva `enviar()` y añade tolerancia
a TimeoutError. Uno adapta una interfaz; el otro compone responsabilidad transversal.

4. **State.** Reporte delega al estado actual, cuya clase habilita solo las
operaciones permitidas. Estado prohíbe todo por defecto; Encolado permite reintentar
y marcar_recibido. La matriz de 25 pares estado/acción prueba tanto caminos válidos
como inválidos, sin if sobre nombres de estados en las subclases.

5. **Caracterización.** Permite comprobar que el refactor conserva estado,
resultado, eventos y reintentos. En el ensayo de mutación documentado,
`isinstance(confianza, (int, float))` aceptó `true`; una prueba falló y la validación
estricta se restauró. Se distingue ese ensayo deliberado de un fallo histórico.

6. **Patrón rechazado.** Singleton para fábricas y LLM dificultaría el aislamiento
de las pruebas y compartiría cachés accidentalmente. Patternitis es acumular
patrones sin un olor que los justifique. Abstract Factory tampoco aporta aquí:
no hay familias de objetos que deban variar juntas.

7. **IA no confiable.** Puede producir JSON inválido, inventar categorías o
emitir confianza fuera de rango. FormatoJSON limita tipo/longitud y parsea;
SeveridadPermitida exige claves exactas y una categoría válida; ConfianzaValida
rechaza booleanos, NaN y valores fuera de 0..1. No garantizan que la severidad sea
verdadera. Por ello el resultado es Sugerencia con requiere_revision=True y no
modifica automáticamente Reporte.

8. **Balance medido.** La máxima CC por método baja 13→5; sincronizar pasa 11→4.
El promedio Radon baja 4.25→1.83, pero el número de bloques sube 12→81 y SLOC
95→230. Parte de la reducción del promedio proviene de distribuir responsabilidades.
Se justifica por canales, proveedores, estados y validaciones cambiantes; un
script estable de un solo proveedor podría quedarse con funciones simples.
