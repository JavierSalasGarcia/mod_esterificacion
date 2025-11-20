#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 2: Listas, Ciclos y Visualización - SOLUCIÓN
"""

import json
import matplotlib.pyplot as plt

# Cargar configuración
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

experimento = config['experimento']
graf_config = config['grafica']

print("="*70)
print("PRÁCTICA 2: Listas, Ciclos y Visualización de Datos")
print("="*70)

# Extraer datos
tiempo = experimento['tiempo_min']
conversion = experimento['conversion_pct']
temperatura = experimento['temperatura_C']

# Mostrar información
print(f"\nDatos: Experimento a {temperatura}°C")
print(f"Puntos de datos: {len(tiempo)}")
print(f"Tiempo total: {max(tiempo)} min")
print(f"Conversión final: {conversion[-1]:.2f}%\n")

# Procesar datos con ciclo for
print("Tiempo:  DATOS EXPERIMENTALES:")
print("-" * 70)
print(f"{'Tiempo (min)':>15} {'Conversión (%)':>20} {'Incremento (%)':>20}")
print("-" * 70)

for i in range(len(tiempo)):
    t = tiempo[i]
    c = conversion[i]

    # Calcular incremento respecto al punto anterior
    if i == 0:
        incremento = 0.0
    else:
        incremento = c - conversion[i-1]

    print(f"{t:>15} {c:>20.2f} {incremento:>20.2f}")

# Crear diccionario de estadísticas
estadisticas = {
    'tiempo_inicial': tiempo[0],
    'tiempo_final': tiempo[-1],
    'conversion_inicial': conversion[0],
    'conversion_final': conversion[-1],
    'conversion_promedio': sum(conversion) / len(conversion),
    'conversion_maxima': max(conversion)
}

print("\n" + "="*70)
print("Resultados: ESTADÍSTICAS")
print("="*70)
for clave, valor in estadisticas.items():
    print(f"{clave:25s}: {valor:>10.2f}")

# Crear gráfica
plt.figure(figsize=(10, 6))
plt.plot(tiempo, conversion,
         marker=graf_config['marker'],
         color=graf_config['color'],
         linewidth=graf_config['linewidth'],
         markersize=graf_config['markersize'],
         label=f'T = {temperatura}°C')

plt.xlabel(graf_config['xlabel'], fontsize=12, fontweight='bold')
plt.ylabel(graf_config['ylabel'], fontsize=12, fontweight='bold')
plt.title(graf_config['titulo'], fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(graf_config['grid'], alpha=0.3)
plt.xlim(0, max(tiempo))
plt.ylim(0, 100)

# Guardar gráfica
output_file = graf_config['output_file']
plt.savefig(output_file, dpi=graf_config['dpi'], bbox_inches='tight')
print(f"\n✓ Gráfica guardada: {output_file}")

plt.show()

print("\n" + "="*70)
print("✓ PRÁCTICA COMPLETADA")
print("="*70)
