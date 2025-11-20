#!/usr/bin/env python3
"""Práctica 5 - EJERCICIO: Uso del GC Processor del Sistema"""

import json
import sys
from pathlib import Path
import numpy as np

# TODO 1: Agregar src al path para importar módulos del sistema
# sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

# TODO 2: Importar el módulo GCProcessor
# from data_processing.gc_processor import GCProcessor

# Cargar configuración
with open('config.json') as f:
    config = json.load(f)

exp = config['experimento']

print("="*70)
print("PRÁCTICA 5: GC Processor del Sistema")
print("="*70)

# TODO 3: Implementar función de interpolación de RPM
def interpolar_rpm(tiempo_min, perfil):
    """
    Interpola RPM según perfil configurado.
    
    Args:
        tiempo_min: Tiempo en minutos
        perfil: Dict con 'tipo' y 'puntos'
    
    Returns:
        RPM interpolado
    """
    puntos = perfil['puntos']
    tiempos = [p['tiempo_min'] for p in puntos]
    rpms = [p['rpm'] for p in puntos]
    
    # TODO: Implementa interpolación lineal usando np.interp
    rpm = None  # <-- Completa aquí
    
    return rpm

# TODO 4: Muestra el perfil de agitación
print("\nPERFIL DE AGITACION:")
print("-" * 70)
print(f"{'Tiempo (min)':>15} {'RPM':>15}")
print("-" * 70)

# TODO 5: Itera sobre tiempos de muestra e imprime RPM interpolados
tiempos_muestra = np.linspace(0, 120, 13)
# for t in tiempos_muestra:
#     rpm = interpolar_rpm(t, exp['perfil_agitacion'])
#     print(...)

# TODO 6: Crear instancia del procesador (descomenta cuando hayas importado)
# processor = GCProcessor()

print("\nINSTRUCCIONES:")
print("1. Descomenta las líneas de importación (TODOs 1-2)")
print("2. Completa la función interpolar_rpm (TODO 3)")
print("3. Implementa el bucle para mostrar el perfil (TODO 5)")
print("4. Ejecuta con datos reales: python solucion.py")

print("\n" + "="*70)
print("COMPLETA LOS TODOs Y EJECUTA DE NUEVO")
print("="*70)
