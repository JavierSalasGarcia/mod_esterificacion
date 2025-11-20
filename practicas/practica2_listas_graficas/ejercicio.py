#!/usr/bin/env python3
"""Práctica 2 - EJERCICIO: Completa los TODOs"""

import json
import matplotlib.pyplot as plt

with open('config.json', 'r') as f:
    config = json.load(f)

experimento = config['experimento']
graf_config = config['grafica']

# TODO 1: Extrae las listas de tiempo y conversión
tiempo = None  # <-- Usa experimento['tiempo_min']
conversion = None  # <-- Usa experimento['conversion_pct']

print("="*70)
print("PRÁCTICA 2: Listas y Visualización")
print("="*70)

# TODO 2: Usa un ciclo for para mostrar cada dato
print("\n⏱️  DATOS:")
print(f"{'Tiempo (min)':>15} {'Conversión (%)':>20}")
print("-" * 40)
# for ... in ...:
#     print(...)

# TODO 3: Calcula la conversión promedio
conversion_promedio = None  # <-- Usa sum() y len()

print(f"\n📊 Conversión promedio: {conversion_promedio:.2f}%")

# TODO 4: Crea la gráfica
plt.figure(figsize=(10, 6))
# plt.plot(...)
# plt.xlabel(...)
# plt.ylabel(...)
# plt.title(...)
# plt.grid(True)

# TODO 5: Guarda la gráfica
# plt.savefig(...)

print("\n✅ Completa los TODOs y ejecuta de nuevo")
