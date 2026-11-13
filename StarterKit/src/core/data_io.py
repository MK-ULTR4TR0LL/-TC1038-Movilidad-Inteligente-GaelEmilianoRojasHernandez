"""Carga de datos base con la biblioteca estándar csv."""
from pathlib import Path
import csv


def cargar_csv(ruta: str | Path) -> list[dict]:
    ruta = Path(ruta)
    with ruta.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))
