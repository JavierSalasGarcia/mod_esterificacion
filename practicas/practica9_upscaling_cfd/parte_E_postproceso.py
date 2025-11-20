#!/usr/bin/env python3
"""
Práctica 9 - Parte E: Post-procesamiento y Comparación
Compara modelo 0D (cinética simple) vs CFD 3D
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from models.kinetic_model import KineticModel

with open('config.json') as f:
    config = json.load(f)

print("="*80)
print("PARTE E: POST-PROCESAMIENTO Y COMPARACION 0D vs CFD")
print("="*80)

# MODELO 0D (Cinética simple)
print("\n[MODELO 0D - Cinética Homogénea]")

model_0D = KineticModel(model_type='1-step', reversible=True, temperature=65)

# Setear parámetros de la Práctica 6
params = config['cinetica']
model_0D.set_parameters({
    'A_forward': params['A_forward'],
    'Ea_forward': params['Ea_forward_J_mol'] / 1000,  # kJ/mol
    'A_reverse': params['A_forward'] * 0.1,
    'Ea_reverse': params['Ea_forward_J_mol'] / 1000 + 10
})

C0 = {'TG': 0.5, 'MeOH': 4.5, 'FAME': 0.0, 'GL': 0.0}
results_0D = model_0D.simulate(t_span=(0, 120), C0=C0)

conversion_0D_final = results_0D['conversion_%'][-1]
print(f"  Conversión final (120 min): {conversion_0D_final:.2f}%")

# SIMULACION CFD (datos de ejemplo)
print("\n[RESULTADOS CFD - Ansys Fluent]")
print("  NOTA: Estos son datos de ejemplo.")
print("  Para datos reales, leer archivos de Fluent (.dat, .csv)")

# Datos simulados de CFD (promedio volumétrico)
tiempo_cfd = np.array([0, 30, 60, 90, 120])
conversion_cfd_promedio = np.array([0, 42, 68, 79, 85])  # Ejemplo

# Variabilidad espacial (distribución)
conversion_cfd_std = np.array([0, 5, 8, 7, 6])  # Desviación estándar

print(f"  Conversión promedio (120 min): {conversion_cfd_promedio[-1]:.2f}%")
print(f"  Desviación estándar: {conversion_cfd_std[-1]:.2f}%")
print(f"  Rango: [{conversion_cfd_promedio[-1]-conversion_cfd_std[-1]:.1f}, "
      f"{conversion_cfd_promedio[-1]+conversion_cfd_std[-1]:.1f}]%")

# COMPARACION
print("\n" + "="*80)
print("COMPARACION DE MODELOS")
print("="*80)

diferencia = abs(conversion_0D_final - conversion_cfd_promedio[-1])
error_relativo = (diferencia / conversion_cfd_promedio[-1]) * 100

print(f"\nConversión final (120 min):")
print(f"  Modelo 0D:       {conversion_0D_final:.2f}%")
print(f"  CFD promedio:    {conversion_cfd_promedio[-1]:.2f}%")
print(f"  Diferencia:      {diferencia:.2f}% puntos")
print(f"  Error relativo:  {error_relativo:.2f}%")

if error_relativo < 5:
    print(f"\nCONCLUSION: Excelente acuerdo (error < 5%)")
elif error_relativo < 10:
    print(f"\nCONCLUSION: Buen acuerdo (error < 10%)")
else:
    print(f"\nCONCLUSION: Diferencia significativa - revisar setup CFD")

# GRAFICAR
plt.figure(figsize=(12, 5))

# Subplot 1: Comparación temporal
plt.subplot(1, 2, 1)
plt.plot(results_0D['time'], results_0D['conversion_%'], 
         'b-', linewidth=2, label='Modelo 0D (homogéneo)')
plt.errorbar(tiempo_cfd, conversion_cfd_promedio, yerr=conversion_cfd_std,
             fmt='ro-', linewidth=2, capsize=5, label='CFD 3D (promedio ± std)')
plt.xlabel('Tiempo (min)', fontweight='bold')
plt.ylabel('Conversión (%)', fontweight='bold')
plt.title('Comparación 0D vs CFD', fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 2: Distribución espacial (CFD)
plt.subplot(1, 2, 2)
# Simulación de distribución espacial
conversiones_espaciales = np.random.normal(
    conversion_cfd_promedio[-1], 
    conversion_cfd_std[-1], 
    1000
)
plt.hist(conversiones_espaciales, bins=30, density=True, 
         alpha=0.7, edgecolor='black')
plt.axvline(conversion_0D_final, color='blue', linestyle='--', 
            linewidth=2, label='Modelo 0D')
plt.axvline(conversion_cfd_promedio[-1], color='red', linestyle='--',
            linewidth=2, label='CFD promedio')
plt.xlabel('Conversión (%)', fontweight='bold')
plt.ylabel('Densidad de probabilidad', fontweight='bold')
plt.title('Distribución Espacial (CFD)', fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('comparacion_0D_vs_CFD.png', dpi=300)
print(f"\nGrafica guardada: comparacion_0D_vs_CFD.png")

plt.show()

print("\n" + "="*80)
print("ANALISIS COMPLETO")
print("="*80)
