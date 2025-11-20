#!/usr/bin/env python3
"""Práctica 6: Ajuste de Parámetros - SOLUCIÓN"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from models.parameter_fitting import ParameterFitter

with open('config.json') as f:
    config = json.load(f)

print("PRÁCTICA 6: Ajuste de Parámetros Cinéticos")
print("="*70)

fitter = ParameterFitter(
    model_type=config['ajuste']['model_type'],
    reversible=config['ajuste']['reversible']
)

C0 = config['condiciones_iniciales']
for exp in config['experimentos']:
    print(f"\nAgregando {exp['id']}: T={exp['temperatura_C']}°C")
    fitter.add_experiment(
        t_exp=exp['tiempo_min'],
        y_exp=exp['conversion_pct'],
        T=exp['temperatura_C'],
        C0=C0,
        exp_id=exp['id']
    )

print("\n🔄 Ajustando parámetros...")
results = fitter.fit(method=config['ajuste']['method'], verbose=True)

print(f"\n✅ A_forward: {results['params']['A_forward']:.4e}")
print(f"✅ Ea_forward: {results['params']['Ea_forward']:.2f} kJ/mol")
print(f"✅ R²: {results['metrics']['R_squared']:.4f}")
