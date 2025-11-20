#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 1: Fundamentos de Python y Cálculos Químicos Básicos
===============================================================

INSTRUCCIONES: Completa los TODOs marcados en el código
"""

import json

print("="*70)
print("PRÁCTICA 1: Cálculos Químicos Básicos con Python")
print("="*70)

# TODO 1: Cargar el archivo config.json
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

masas_molares = config['masas_molares']
densidades = config['densidades_25C']
experimento = config['experimento']

print("\n✓ Datos cargados exitosamente desde config.json\n")


def calcular_moles(masa_g, masa_molar):
    """Calcula moles: n = m / M"""
    # TODO 2: Implementa el cálculo
    moles = None  # <-- Reemplaza None con tu código
    return moles


def calcular_concentracion_molar(moles, volumen_L):
    """Calcula concentración: C = n / V"""
    # TODO 3: Implementa el cálculo
    concentracion = None  # <-- Reemplaza None
    return concentracion


def calcular_conversion(moles_inicial, moles_final):
    """Calcula conversión: X = ((n0 - n) / n0) * 100"""
    # TODO 4: Implementa el cálculo
    conversion_porcentaje = None  # <-- Reemplaza None
    return conversion_porcentaje


def calcular_rendimiento(moles_producto_real, moles_producto_teorico):
    """Calcula rendimiento: Y = (real / teórico) * 100"""
    # TODO 5: Implementa el cálculo
    rendimiento_porcentaje = None  # <-- Reemplaza None
    return rendimiento_porcentaje


# Mostrar datos del experimento
print("Datos: DATOS DEL EXPERIMENTO")
print("-" * 70)
print(f"Volumen del reactor: {experimento['volumen_reactor_mL']} mL")
print(f"Masa inicial de TG: {experimento['masa_TG_inicial_g']} g")
print(f"Volumen de MeOH: {experimento['volumen_MeOH_mL']} mL")
print(f"Masa final de FAME: {experimento['masa_FAME_final_g']} g")

# TODO 6: Calcula moles iniciales de TG usando la función calcular_moles
moles_TG_inicial = None  # <-- Usa calcular_moles()

# Calcular masa y moles de MeOH
masa_MeOH_g = experimento['volumen_MeOH_mL'] * densidades['MeOH_kg_L']
moles_MeOH_inicial = calcular_moles(masa_MeOH_g, masas_molares['MeOH'])

# Calcular moles de FAME producidos
moles_FAME_producido = calcular_moles(
    experimento['masa_FAME_final_g'],
    masas_molares['FAME_metil_palmitato']
)

# Estequiometría: 1 TG → 3 FAME
moles_FAME_teorico = moles_TG_inicial * 3
moles_TG_consumido = moles_FAME_producido / 3
moles_TG_final = moles_TG_inicial - moles_TG_consumido

# TODO 7: Calcula la conversión de TG
conversion_TG = None  # <-- Usa calcular_conversion()

# TODO 8: Calcula el rendimiento de FAME
rendimiento_FAME = None  # <-- Usa calcular_rendimiento()

# TODO 9: Calcula concentraciones molares iniciales
volumen_total_L = experimento['volumen_reactor_mL'] / 1000
C_TG_inicial = None  # <-- Usa calcular_concentracion_molar()
C_MeOH_inicial = None  # <-- Usa calcular_concentracion_molar()

# Mostrar resultados
print("\n" + "="*70)
print("Resultados: RESULTADOS")
print("="*70)
print(f"\nMetricas: Conversión de TG: {conversion_TG:.2f} %")
print(f"Metricas: Rendimiento FAME: {rendimiento_FAME:.2f} %")
print(f"\nDatos: [TG]₀:   {C_TG_inicial:.3f} mol/L")
print(f"Datos: [MeOH]₀: {C_MeOH_inicial:.3f} mol/L")
print("\n" + "="*70)
