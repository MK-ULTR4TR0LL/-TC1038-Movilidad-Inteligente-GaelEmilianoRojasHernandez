"""Aplicación principal Tkinter — TC1038 Movilidad Inteligente."""
from pathlib import Path
import sys
import tkinter as tk
from tkinter import ttk

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.app.win_home import open_win_home
from src.app.win_form import open_win_form
from src.app.win_table import open_win_table
from src.app.win_dashboard import open_win_dashboard
from src.app.win_external import open_win_external


def main():
    root = tk.Tk()
    root.title("TC1038 — Movilidad Inteligente")
    root.geometry("520x420")
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Movilidad Inteligente 2026", font=("Segoe UI", 16, "bold")).pack(pady=(0, 6))
    ttk.Label(frame, text="Starter App — personaliza cada componente para tu problema").pack(pady=(0, 18))
    buttons = [
        ("1) Inicio / propuesta", open_win_home),
        ("2) Captura / formulario", open_win_form),
        ("3) Datos / tabla CSV", open_win_table),
        ("4) Análisis / dashboard", open_win_dashboard),
        ("5) Datos externos / API", open_win_external),
    ]
    for text, fn in buttons:
        ttk.Button(frame, text=text, command=lambda f=fn: f(root)).pack(fill="x", pady=5)
    ttk.Separator(frame).pack(fill="x", pady=12)
    ttk.Button(frame, text="Salir", command=root.destroy).pack()
    root.mainloop()

if __name__ == "__main__":
    main()
