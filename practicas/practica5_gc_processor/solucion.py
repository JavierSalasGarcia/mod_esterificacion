#!/usr/bin/env python3
"""Práctica 5: GC Processor - SOLUCIÓN"""

import json
import sys
from pathlib import Path
import numpy as np

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from data_processing.gc_processor import GCProcessor

# Cargar configuración
with open('config.json') as f:
    config = json.load(f)

exp = config['experimento']
proc = config['procesamiento']

print("="*70)
print("PRÁCTICA 5: Procesamiento GC-FID con el Sistema")
print("="*70)

# Función para interpolar perfil de agitación
def interpolar_rpm(tiempo_min, perfil):
    """
    Interpola RPM en cualquier punto según perfil configurado.
    
    Args:
        tiempo_min: Tiempo en minutos
        perfil: Diccionario con 'tipo' y 'puntos'
    
    Returns:
        RPM interpolado
    """
    puntos = perfil['puntos']
    tiempos = [p['tiempo_min'] for p in puntos]
    rpms = [p['rpm'] for p in puntos]
    
    if perfil['tipo'] == 'lineal':
        rpm = np.interp(tiempo_min, tiempos, rpms)
    elif perfil['tipo'] == 'escalonado':
        idx = np.searchsorted(tiempos, tiempo_min, side='right') - 1
        rpm = rpms[max(0, min(idx, len(rpms)-1))]
    else:
        rpm = rpms[0]  # Por defecto, primer valor
    
    return rpm

# Mostrar perfil de agitación
print(f"\n🔄 PERFIL DE AGITACIÓN ({exp['perfil_agitacion']['tipo']})")
print("-" * 70)
print(f"{'Tiempo (min)':>15} {'RPM':>15}")
print("-" * 70)

tiempos_muestra = np.linspace(0, 120, 13)
for t in tiempos_muestra:
    rpm = interpolar_rpm(t, exp['perfil_agitacion'])
    print(f"{t:>15.0f} {rpm:>15.1f}")

# Crear procesador
processor = GCProcessor()

print("\n📊 PROCESADOR GC-FID INICIADO")
print(f"  Volumen reactor: {exp['volumen_reactor_mL']} mL")
print(f"  Temperatura: {exp['temperatura_C']}°C")
print(f"  C_TG inicial: {proc['C_TG_inicial_mol_L']} mol/L")

# Nota: Para usar datos reales, descomenta:
# data = processor.load_from_csv('datos/gc_data.csv')
# results = processor.process_time_series(data, C_TG0=proc['C_TG_inicial_mol_L'])
# stats = processor.summary_statistics(results)

print("\n✅ Sistema importado correctamente")
print("✅ Perfil de agitación configurado")
print("\n💡 Para procesar datos reales:")
print("   python main.py --mode process_gc --input datos.csv --output results/")
print("="*70)
