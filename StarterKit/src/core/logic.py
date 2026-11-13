"""Lógica base del proyecto TC1038.

Personaliza estas funciones para que representen las reglas de negocio de tu solución.
"""

def clasificar_riesgo(flujo: int, velocidad_promedio: float, incidentes: int) -> str:
    """Clasifica un registro de movilidad con reglas simples editables por el equipo."""
    if incidentes > 0:
        return "ALTO"
    if flujo >= 60 and velocidad_promedio < 35:
        return "MEDIO"
    return "BAJO"


def promedio(valores: list[float]) -> float:
    """Calcula el promedio sin depender de pandas; sirve para practicar fundamentos."""
    if not valores:
        return 0.0
    acumulado = 0.0
    for valor in valores:
        acumulado += valor
    return acumulado / len(valores)


def resumir_registros(registros: list[dict]) -> dict:
    """Ejemplo de procesamiento que el equipo debe comprender y adaptar."""
    flujos = []
    velocidades = []
    incidentes = 0
    for r in registros:
        flujos.append(int(r["flujo"]))
        velocidades.append(float(r["velocidad_promedio"]))
        incidentes += int(r["incidentes"])
    return {
        "flujo_promedio": round(promedio(flujos), 2),
        "velocidad_promedio": round(promedio(velocidades), 2),
        "incidentes": incidentes,
    }
