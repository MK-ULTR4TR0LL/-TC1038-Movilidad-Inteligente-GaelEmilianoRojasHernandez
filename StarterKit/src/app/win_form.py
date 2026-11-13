import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv

def open_win_form(parent: tk.Tk):
    win = tk.Toplevel(parent); win.title("Registrar observación"); win.geometry("520x360")
    frm = ttk.Frame(win, padding=16); frm.pack(fill="both", expand=True)
    campos = [("Intersección", "A"), ("Flujo", "50"), ("Velocidad promedio", "35.0"), ("Incidentes", "0")]
    entries = {}
    for i,(label,default) in enumerate(campos):
        ttk.Label(frm, text=label+":").grid(row=i, column=0, sticky="w", pady=5)
        e=ttk.Entry(frm, width=28); e.insert(0, default); e.grid(row=i, column=1, pady=5); entries[label]=e
    def guardar():
        try:
            flujo=int(entries["Flujo"].get()); vel=float(entries["Velocidad promedio"].get()); inc=int(entries["Incidentes"].get())
        except ValueError:
            messagebox.showerror("Datos inválidos", "Flujo e incidentes deben ser enteros y velocidad un número."); return
        ruta=Path(__file__).resolve().parents[2]/"data"/"observaciones_usuario.csv"
        nuevo=not ruta.exists()
        with ruta.open("a", encoding="utf-8", newline="") as f:
            w=csv.writer(f)
            if nuevo: w.writerow(["interseccion","flujo","velocidad_promedio","incidentes"])
            w.writerow([entries["Intersección"].get().strip(), flujo, vel, inc])
        messagebox.showinfo("Guardado", f"Observación guardada en {ruta.name}")
    ttk.Button(frm, text="Guardar observación", command=guardar).grid(row=5,column=0,columnspan=2,pady=16)
