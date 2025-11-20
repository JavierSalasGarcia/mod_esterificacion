#!/usr/bin/env python3
"""Práctica 4: Arrhenius y EDOs - SOLUCIÓN"""

import json
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

with open('config.json') as f:
    config = json.load(f)

params = config['parametros_cineticos']
cond = config['condiciones']

def arrhenius(T_celsius):
    """Calcula k usando Arrhenius"""
    T_K = T_celsius + 273.15
    A = params['A_forward']
    Ea = params['Ea_forward_kJ_mol'] * 1000  # J/mol
    R = params['R_J_mol_K']
    k = A * np.exp(-Ea / (R * T_K))
    return k

def edo_primer_orden(C, t, k):
    """dC/dt = -k*C"""
    return -k * C

# Tiempo
t = np.linspace(0, cond['tiempo_min'], 100)
C0 = cond['C_TG_inicial_mol_L']

print("="*70)
print("PRÁCTICA 4: Ecuación de Arrhenius y EDOs")
print("="*70)

plt.figure(figsize=(10, 6))

for T in cond['temperaturas_C']:
    k = arrhenius(T)
    C = odeint(edo_primer_orden, C0, t, args=(k,))
    conversion = ((C0 - C) / C0) * 100
    
    print(f"\nT = {T}°C → k = {k:.6e} min⁻¹")
    print(f"  Conversión final: {conversion[-1][0]:.2f}%")
    
    plt.plot(t, conversion, label=f'T = {T}°C', linewidth=2)

plt.xlabel('Tiempo (min)', fontweight='bold')
plt.ylabel('Conversión (%)', fontweight='bold')
plt.title('Efecto de la Temperatura en la Conversión', fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('arrhenius_comparison.png', dpi=300)
print("\n✓ Gráfica guardada: arrhenius_comparison.png")
plt.show()
