import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
 
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
 

LATITUD = 21.12          
LONGITUD = -101.68
DIAS = 7                 
 
NEGRO = "#0d0d0d"
GRIS_OSCURO = "#1a1a1a"
ROJO = "#e10600"
ROJO_CLARO = "#ff4d4d"
BLANCO = "#ffffff"
GRIS_TEXTO = "#cfcfcf"
 
 
def fetch_data():
    """
    Consulta Open-Meteo (sin autenticación) para León, Gto., 7 días.
    Devuelve un diccionario con datos horarios y diarios, o None si falla.
    """
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={LATITUD}&longitude={LONGITUD}"
            "&hourly=temperature_2m,wind_speed_10m"
            "&daily=temperature_2m_max,temperature_2m_min"
            f"&forecast_days={DIAS}&timezone=auto"
        )
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
 
        return {
            "horas": [datetime.fromisoformat(t) for t in data["hourly"]["time"]],
            "temps": data["hourly"]["temperature_2m"],
            "viento": data["hourly"]["wind_speed_10m"],
            "dias": [datetime.fromisoformat(d) for d in data["daily"]["time"]],
            "t_max": data["daily"]["temperature_2m_max"],
            "t_min": data["daily"]["temperature_2m_min"],
        }
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los datos:\n{e}")
        return None
 
 
def estilo_ejes(fig, ax, titulo, xlabel, ylabel):
    """Aplica el tema negro/rojo/blanco a una gráfica."""
    fig.patch.set_facecolor(NEGRO)
    ax.set_facecolor(GRIS_OSCURO)
    ax.set_title(titulo, color=BLANCO, fontsize=11, fontweight="bold")
    ax.set_xlabel(xlabel, color=GRIS_TEXTO)
    ax.set_ylabel(ylabel, color=GRIS_TEXTO)
    ax.tick_params(colors=GRIS_TEXTO)
    for borde in ax.spines.values():
        borde.set_color(ROJO)
    ax.grid(True, linestyle="--", alpha=0.3, color=BLANCO)
 
 
def create_line_chart(horas, temps):
    """Gráfica de línea: temperatura por hora durante 7 días."""
    fig = Figure(figsize=(8.5, 2.8))
    ax = fig.add_subplot(111)
    ax.plot(horas, temps, color=ROJO, linewidth=1.8, alpha=0.95)
    ax.fill_between(horas, temps, min(temps), color=ROJO, alpha=0.15)
    estilo_ejes(fig, ax, "Temperatura por hora en León (línea)", "Fecha", "Temperatura (°C)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    fig.tight_layout()
    return fig
 
 
def create_bar_chart(dias, t_max, t_min):
    """Gráfica de barras: temperatura máxima y mínima por día."""
    fig = Figure(figsize=(8.5, 2.8))
    ax = fig.add_subplot(111)
    etiquetas = [d.strftime("%a %d") for d in dias]
    x = range(len(dias))
    ancho = 0.38
    ax.bar([i - ancho / 2 for i in x], t_max, ancho, color=ROJO, label="Máxima")
    ax.bar([i + ancho / 2 for i in x], t_min, ancho, color=BLANCO, label="Mínima")
    ax.set_xticks(list(x))
    ax.set_xticklabels(etiquetas)
    estilo_ejes(fig, ax, "Máxima y mínima por día (barras)", "Día", "Temperatura (°C)")
    leyenda = ax.legend(facecolor=NEGRO, edgecolor=ROJO)
    for texto in leyenda.get_texts():
        texto.set_color(BLANCO)
    fig.tight_layout()
    return fig
 
 
def create_scatter_chart(temps, viento):
    """Gráfica de dispersión: temperatura vs. velocidad del viento."""
    fig = Figure(figsize=(8.5, 2.8))
    ax = fig.add_subplot(111)
    ax.scatter(temps, viento, s=22, color=ROJO_CLARO, edgecolors=BLANCO,
               linewidths=0.4, alpha=0.8)
    estilo_ejes(fig, ax, "Temperatura vs. viento (dispersión)",
                "Temperatura (°C)", "Viento (km/h)")
    fig.tight_layout()
    return fig
 
 
def mostrar_graficas(contenedor, datos):
    """Limpia el contenedor e inserta las tres gráficas (evita duplicados)."""
    for widget in contenedor.winfo_children():
        widget.destroy()
 
    figuras = [
        create_line_chart(datos["horas"], datos["temps"]),
        create_bar_chart(datos["dias"], datos["t_max"], datos["t_min"]),
        create_scatter_chart(datos["temps"], datos["viento"]),
    ]
    for fig in figuras:
        canvas = FigureCanvasTkAgg(fig, master=contenedor)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=6, fill="x")
 
 
def open_win_canvas(parent: tk.Tk):
    """Crea la ventana secundaria con las gráficas de la API."""
    win = tk.Toplevel(parent)
    win.title("Clima para rutas seguras — León, Gto.")
    win.geometry("960x1000")
    win.configure(bg=NEGRO)
 
    estilo = ttk.Style(win)
    estilo.theme_use("clam")
    estilo.configure("Rojo.TButton", background=ROJO, foreground=BLANCO,
                     font=("Segoe UI", 11, "bold"), padding=8, borderwidth=0)
    estilo.map("Rojo.TButton", background=[("active", ROJO_CLARO)])
    estilo.configure("Negro.TFrame", background=NEGRO)
    estilo.configure("Titulo.TLabel", background=NEGRO, foreground=BLANCO,
                     font=("Segoe UI", 15, "bold"))
    estilo.configure("Sub.TLabel", background=NEGRO, foreground=ROJO_CLARO,
                     font=("Segoe UI", 10))
 
    frm = ttk.Frame(win, padding=12, style="Negro.TFrame")
    frm.pack(fill="both", expand=True)
 
    ttk.Label(frm, text="Clima de los próximos 7 días", style="Titulo.TLabel").pack()
    ttk.Label(frm, text="Planea tu ruta segura en bici, patines o skate",
              style="Sub.TLabel").pack(pady=(0, 8))
 
    contenedor = ttk.Frame(frm, style="Negro.TFrame")
 
    def cargar():
        datos = fetch_data()
        if datos:
            mostrar_graficas(contenedor, datos)
 
    ttk.Button(frm, text="Cargar y mostrar gráficas", style="Rojo.TButton",
               command=cargar).pack(pady=8)
    contenedor.pack(fill="both", expand=True)

 
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Prueba win_canvas")
    ttk.Button(root, text="Abrir ventana Canvas",
               command=lambda: open_win_canvas(root)).pack(pady=20)
    root.mainloop()
