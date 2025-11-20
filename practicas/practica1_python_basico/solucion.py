#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 1: Fundamentos de Python y Cálculos Químicos Básicos - SOLUCIÓN
==========================================================================

Este es el código completo con todas las soluciones implementadas.
"""

import json

# ==============================================================================
# PASO 1: Cargar configuración desde JSON
# ==============================================================================
print("="*70)
print("PRÁCTICA 1: Cálculos Químicos Básicos con Python")
print("="*70)

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

masas_molares = config['masas_molares']
densidades = config['densidades_25C']
experimento = config['experimento']

print("\n✓ Datos cargados exitosamente desde config.json\n")

# ==============================================================================
# PASO 2: Definir funciones para cálculos
# ==============================================================================

def calcular_moles(masa_g, masa_molar):
    """
    Calcula moles a partir de masa y masa molar.

    Fórmula: n = m / M
    """
    moles = masa_g / masa_molar
    return moles


def calcular_concentracion_molar(moles, volumen_L):
    """
    Calcula concentración molar (mol/L).

    Fórmula: C = n / V
    """
    concentracion = moles / volumen_L
    return concentracion


def calcular_conversion(moles_inicial, moles_final):
    """
    Calcula conversión porcentual.

    Fórmula: X = ((n0 - n) / n0) * 100
    """
    conversion_porcentaje = ((moles_inicial - moles_final) / moles_inicial) * 100
    return conversion_porcentaje


def calcular_rendimiento(moles_producto_real, moles_producto_teorico):
    """
    Calcula rendimiento porcentual.

    Fórmula: Y = (real / teórico) * 100
    """
    rendimiento_porcentaje = (moles_producto_real / moles_producto_teorico) * 100
    return rendimiento_porcentaje


# ==============================================================================
# PASO 3: Realizar cálculos con datos del experimento
# ==============================================================================

print("📊 DATOS DEL EXPERIMENTO")
print("-" * 70)
print(f"Volumen del reactor: {experimento['volumen_reactor_mL']} mL")
print(f"Masa inicial de TG: {experimento['masa_TG_inicial_g']} g")
print(f"Volumen de MeOH: {experimento['volumen_MeOH_mL']} mL")
print(f"Masa final de FAME: {experimento['masa_FAME_final_g']} g")
print(f"Temperatura: {experimento['temperatura_C']} °C")
print(f"Tiempo de reacción: {experimento['tiempo_reaccion_min']} min")

# Calcular moles iniciales de TG
moles_TG_inicial = calcular_moles(
    experimento['masa_TG_inicial_g'],
    masas_molares['TG_tripalmitin']
)

# Calcular masa de MeOH
masa_MeOH_g = experimento['volumen_MeOH_mL'] * densidades['MeOH_kg_L']

# Calcular moles iniciales de MeOH
moles_MeOH_inicial = calcular_moles(masa_MeOH_g, masas_molares['MeOH'])

# Calcular moles de FAME producidos
moles_FAME_producido = calcular_moles(
    experimento['masa_FAME_final_g'],
    masas_molares['FAME_metil_palmitato']
)

# Según estequiometría: 1 TG → 3 FAME
moles_FAME_teorico = moles_TG_inicial * 3

# Moles de TG consumidos (basado en FAME producido)
moles_TG_consumido = moles_FAME_producido / 3

# Moles finales de TG
moles_TG_final = moles_TG_inicial - moles_TG_consumido

# Calcular conversión de TG
conversion_TG = calcular_conversion(moles_TG_inicial, moles_TG_final)

# Calcular rendimiento de FAME
rendimiento_FAME = calcular_rendimiento(moles_FAME_producido, moles_FAME_teorico)

# Volumen total en litros
volumen_total_L = experimento['volumen_reactor_mL'] / 1000

# Calcular concentraciones molares iniciales
C_TG_inicial = calcular_concentracion_molar(moles_TG_inicial, volumen_total_L)
C_MeOH_inicial = calcular_concentracion_molar(moles_MeOH_inicial, volumen_total_L)

# ==============================================================================
# PASO 4: Mostrar resultados
# ==============================================================================

print("\n" + "="*70)
print("📈 RESULTADOS DE LOS CÁLCULOS")
print("="*70)

print("\n🔬 MOLES:")
print(f"  TG inicial:       {moles_TG_inicial:.4f} mol")
print(f"  MeOH inicial:     {moles_MeOH_inicial:.4f} mol")
print(f"  FAME producido:   {moles_FAME_producido:.4f} mol")
print(f"  FAME teórico:     {moles_FAME_teorico:.4f} mol")

print("\n📊 CONCENTRACIONES INICIALES:")
print(f"  [TG]₀:   {C_TG_inicial:.3f} mol/L")
print(f"  [MeOH]₀: {C_MeOH_inicial:.3f} mol/L")

print("\n✨ MÉTRICAS DE DESEMPEÑO:")
print(f"  Conversión de TG: {conversion_TG:.2f} %")
print(f"  Rendimiento FAME: {rendimiento_FAME:.2f} %")

# Relación molar MeOH:TG
relacion_molar = moles_MeOH_inicial / moles_TG_inicial
print(f"  Relación molar MeOH:TG = {relacion_molar:.1f}:1")

# Verificar si es exceso de MeOH (estequiométrico es 3:1)
if relacion_molar >= 3:
    print(f"  ✓ Metanol en exceso (estequiométrico: 3:1)")
else:
    print(f"  ⚠ Metanol deficiente (se requiere mínimo 3:1)")

print("\n" + "="*70)
print("✅ PRÁCTICA COMPLETADA EXITOSAMENTE")
print("="*70)
