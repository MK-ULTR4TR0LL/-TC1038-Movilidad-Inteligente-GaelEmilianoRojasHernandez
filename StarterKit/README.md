# TC1038 Starter App 2026 — Movilidad Inteligente

Plantilla funcional para el Proyecto Integrador. El objetivo es **modificar y personalizar**, no reconstruir toda la infraestructura desde cero.

## Ejecución rápida
1. Abre esta carpeta en VS Code.
2. Ejecuta `python src/app/main.py`.
3. Para activar los boosters: `python -m pip install -r requirements.txt`.

## Filosofía
EJECUTA → OBSERVA → ENTIENDE → MODIFICA → PRUEBA → PERSONALIZA → INTEGRA.

La lógica que representa la solución del equipo debe quedar principalmente en `src/core/logic.py`.

Cambios en win_canvas.py

Rango de consulta: de past_days=1 a forecast_days=7 (pronóstico de 7 días).
Variables nuevas: wind_speed_10m (viento) además de temperature_2m.
Datos diarios: temperature_2m_max y temperature_2m_min para la gráfica de barras.
Fechas: se convierten a datetime para formatear mejor el eje X.
Gráficas (3)
Línea: temperatura por hora durante 7 días, con área sombreada.
Barras: temperatura máxima (rojo) y mínima (blanco) por día. Antes se graficaban 168 barras horarias, que no se leían bien.
Dispersión: temperatura vs. viento, útil para saber si conviene salir a rodar.
Diseño
Paleta: negro, rojo  y toques blancos.
Rejilla punteada, bordes rojos, títulos en blanco y ejes con unidades (°C, km/h).
Botón rojo con estilo ttk (tema clam) y título dentro de la ventana.
Mejoras técnicas
Se usa Figure en lugar de pyplot para evitar fugas de memoria con tkinter.
mostrar_graficas() limpia el contenedor antes de dibujar, así que presionar el botón varias veces no duplica las gráficas.
