#!/usr/bin/env python3
"""Práctica 7 - EJERCICIO: Optimización de Condiciones"""

import json
import sys
import numpy as np
from pathlib import Path

# TODO 1: Agregar src al path
# sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

# TODO 2: Importar módulos necesarios
# from models.kinetic_model import KineticModel
# from optimization.optimizer import OperationalOptimizer

with open('config.json') as f:
    config = json.load(f)

print("="*70)
print("PRÁCTICA 7: Optimización de Condiciones")
print("="*70)

# TODO 3: Crear modelo cinético (descomenta)
# model = KineticModel(model_type='1-step', reversible=True)

# TODO 4: Crear optimizador (descomenta)
# optimizer = OperationalOptimizer(
#     model, 
#     objective_type=config['optimizacion']['objetivo']
# )

print("\nOBJETIVO:", config['optimizacion']['objetivo'])
print("TIEMPO DE REACCION:", config['optimizacion']['tiempo_reaccion_min'], "min")

print("\nBOUNDS:")
for var, bounds in config['optimizacion']['bounds'].items():
    print(f"  {var}: [{bounds[0]}, {bounds[1]}]")

# TODO 5: Ejecutar optimización (descomenta y completa)
# print("\nOptimizando...")
# result = optimizer.optimize(
#     C0=config['C0'],
#     t_reaction=...,  # <-- Completa
#     method='differential_evolution',
#     maxiter=50,
#     verbose=True
# )

# TODO 6: Mostrar resultados óptimos
# print("\nCONDICIONES OPTIMAS:")
# print(f"  Temperatura: {result['temperature']:.2f} °C")
# print(...)

# TODO 7: Generar perfil de agitación optimizado
perfil = config['optimizacion']['perfil_agitacion_base']
print("\nPERFIL DE AGITACION (base):")
for punto in perfil['puntos_relativos']:
    print(f"  t={punto['tiempo_min']:3.0f} min → factor={punto['factor']:.1f}")

# TODO 8: Calcular RPM real del perfil con rpm_base optimizado
# rpm_base = result['rpm']
# for punto in perfil['puntos_relativos']:
#     rpm_real = rpm_base * punto['factor']
#     print(...)

print("\n" + "="*70)
print("INSTRUCCIONES:")
print("1. Descomenta importaciones (TODOs 1-2)")
print("2. Crea modelo y optimizador (TODOs 3-4)")
print("3. Ejecuta optimización (TODO 5)")
print("4. Muestra resultados y perfil optimizado (TODOs 6-8)")
print("="*70)
