# src/estadisticas.py

import os
import csv
from collections import Counter
from utils import box, error, success

HISTORIAL_CSV = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    "data",
    "historial_global.csv"
)

def mostrar_estadisticas():
    """
    Calcula y muestra estadísticas globales de todas las consultas
    guardadas en historial_global.csv.
    """
    print()
    box("ESTADÍSTICAS GLOBALES")
    print()

    if not os.path.exists(HISTORIAL_CSV):
        error("No hay historial global para calcular estadísticas.")
        print()
        return

    ciudades = []
    temps = []
    total_consultas = 0

    with open(HISTORIAL_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            # row: [usuario, ciudad, timestamp, temp, feels, hum, desc, viento]
            _, ciudad, _, temp, *_ = row
            ciudades.append(ciudad.lower())
            try:
                temps.append(float(temp))
            except ValueError:
                continue
            total_consultas += 1

    if total_consultas == 0:
        error("El historial está vacío.")
        print()
        return

    ciudad_mas = Counter(ciudades).most_common(1)[0][0].title()
    temp_promedio = sum(temps) / len(temps)

    success(f"Total de consultas: {total_consultas}")
    success(f"Ciudad más consultada: {ciudad_mas}")
    success(f"Temperatura promedio: {temp_promedio:.1f} °C")
    print()