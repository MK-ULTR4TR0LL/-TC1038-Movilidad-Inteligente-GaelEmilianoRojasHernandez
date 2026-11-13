import tkinter as tk
from tkinter import ttk

def open_win_external(parent: tk.Tk):
    win=tk.Toplevel(parent); win.title("Datos externos / API"); win.geometry("560x300")
    frm=ttk.Frame(win,padding=18); frm.pack(fill="both",expand=True)
    ttk.Label(frm,text="API — booster por integrar",font=("Segoe UI",14,"bold")).pack(anchor="w")
    ttk.Label(frm,text="Esta ventana funciona como placeholder. En el periodo 3 integrarás el booster de API y adaptarás la fuente externa a tu proyecto.",wraplength=500).pack(anchor="w",pady=12)
