#!/usr/bin/env python3
"""Práctica 7: Optimización - SOLUCIÓN"""
import json, sys, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from models.kinetic_model import KineticModel
from optimization.optimizer import OperationalOptimizer

with open('config.json') as f:
    config = json.load(f)

print("PRÁCTICA 7: Optimización de Condiciones")
print("="*70)

model = KineticModel(model_type='1-step', reversible=True)
optimizer = OperationalOptimizer(model, objective_type=config['optimizacion']['objetivo'])

print("\n🔄 Optimizando...")
result = optimizer.optimize(
    C0=config['C0'],
    t_reaction=config['optimizacion']['tiempo_reaccion_min'],
    method='differential_evolution',
    maxiter=50,
    verbose=True
)

print(f"\n🎯 CONDICIONES ÓPTIMAS:")
print(f"  Temperatura: {result['temperature']:.2f}°C")
print(f"  RPM promedio: {result['rpm']:.0f}")
print(f"  Catalizador: {result['catalyst_%']:.2f}%")
print(f"  Conversión: {result['conversion_%']:.2f}%")

# Generar perfil de RPM optimizado
perfil = config['optimizacion']['perfil_agitacion_base']
rpm_base = result['rpm']
print(f"\n🔄 PERFIL DE AGITACIÓN OPTIMIZADO:")
for punto in perfil['puntos_relativos']:
    t = punto['tiempo_min']
    rpm = rpm_base * punto['factor']
    print(f"  t={t:3.0f} min → RPM={rpm:.0f}")
