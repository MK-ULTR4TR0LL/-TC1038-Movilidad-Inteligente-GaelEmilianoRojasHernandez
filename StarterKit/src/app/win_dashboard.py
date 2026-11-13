import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sys

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.data_io import cargar_csv
from src.core.logic import resumir_registros

CSV_PATH = ROOT / "data" / "sample_traffic.csv"


def _preparar_dataframe(path: Path) -> pd.DataFrame:
    """Lee el CSV con Pandas y tipa las columnas."""
    df = pd.read_csv(path)
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    for col in ("flujo", "velocidad_promedio", "incidentes"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["fecha", "flujo"])


def _dibujar_graficas(df: pd.DataFrame, fig: Figure) -> None:
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    # 1) Flujo por hora, una línea por intersección
    flujo = df.pivot_table(index="hora", columns="interseccion",
                           values="flujo", aggfunc="sum").sort_index()
    for inter in flujo.columns:
        ax1.plot(flujo.index, flujo[inter], marker="o", label=f"Intersección {inter}")
    ax1.set_title("Flujo vehicular por hora")
    ax1.set_xlabel("Hora")
    ax1.set_ylabel("Vehículos")
    ax1.grid(alpha=0.3)
    ax1.legend()


    resumen = df.groupby("interseccion").agg(
        velocidad=("velocidad_promedio", "mean"),
        incidentes=("incidentes", "sum"),
    )
    barras = ax2.bar(resumen.index.astype(str), resumen["velocidad"],
                     color=["#4C78A8", "#F58518"][:len(resumen)])
    for barra, inc in zip(barras, resumen["incidentes"]):
        ax2.text(barra.get_x() + barra.get_width() / 2, barra.get_height(),
                 f"{int(inc)} incid.", ha="center", va="bottom", fontsize=9)
    ax2.set_title("Velocidad promedio por intersección")
    ax2.set_xlabel("Intersección")
    ax2.set_ylabel("Velocidad promedio")
    ax2.set_ylim(0, resumen["velocidad"].max() * 1.2)
    ax2.grid(axis="y", alpha=0.3)

    fig.tight_layout()


def open_win_dashboard(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Dashboard base")
    win.geometry("680x680")
    win.transient(parent)

    frm = ttk.Frame(win, padding=18)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="Dashboard base", font=("Segoe UI", 14, "bold")).pack(anchor="w")

    try:
        datos = cargar_csv(CSV_PATH)
        resumen = resumir_registros(datos)
        df = _preparar_dataframe(CSV_PATH)
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró {CSV_PATH.name}", parent=win)
        win.destroy()
        return
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron procesar los datos:\n{e}", parent=win)
        win.destroy()
        return

    for k, v in resumen.items():
        ttk.Label(frm, text=f"{k.replace('_', ' ').title()}: {v}").pack(anchor="w", pady=2)

    fig = Figure(figsize=(6.4, 4.6), dpi=100)
    try:
        _dibujar_graficas(df, fig)
        canvas = FigureCanvasTkAgg(fig, master=frm)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)
    except Exception as e:
        ttk.Label(frm, text=f"No se pudo generar la gráfica: {e}",
                  foreground="red", wraplength=620).pack(anchor="w", pady=6)

    ttk.Button(frm, text="Cerrar", command=win.destroy).pack(anchor="e")
    return win