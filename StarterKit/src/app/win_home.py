import tkinter as tk
from tkinter import ttk, messagebox

def open_win_home(parent: tk.Tk):
    win = tk.Toplevel(parent); win.title("Inicio"); win.geometry("520x300")
    frm = ttk.Frame(win, padding=18); frm.pack(fill="both", expand=True)
    ttk.Label(frm, text="Tu problema de movilidad", font=("Segoe UI", 14, "bold")).pack(anchor="w")
    ttk.Label(frm, text="Reemplaza este texto por el problema, usuario y propuesta de valor de tu equipo.", wraplength=460).pack(anchor="w", pady=10)
    ttk.Button(frm, text="¿Por qué importa?", command=lambda: messagebox.showinfo("Impacto", "Personaliza este mensaje con evidencia de tu problema.")).pack(anchor="w")
