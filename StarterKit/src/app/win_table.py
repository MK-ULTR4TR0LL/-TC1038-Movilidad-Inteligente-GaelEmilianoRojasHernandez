import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from src.core.data_io import cargar_csv

def open_win_table(parent: tk.Tk):
    win=tk.Toplevel(parent); win.title("Datos de movilidad"); win.geometry("760x380")
    frm=ttk.Frame(win,padding=12); frm.pack(fill="both",expand=True)
    cols=("fecha","hora","interseccion","flujo","velocidad_promedio","incidentes")
    tv=ttk.Treeview(frm,columns=cols,show="headings")
    for c in cols: tv.heading(c,text=c.replace("_"," ").title()); tv.column(c,width=110,anchor="center")
    tv.pack(fill="both",expand=True)
    ruta=ROOT/"data"/"sample_traffic.csv"
    for r in cargar_csv(ruta): tv.insert("","end",values=tuple(r[c] for c in cols))
