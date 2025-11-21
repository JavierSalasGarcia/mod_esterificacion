#!/usr/bin/env python3
"""
Práctica 5: Procesamiento de Datos de Cromatografía de Gases (GC-FID)
Enfoque: EXPERIMENTAR - El estudiante modifica factores de respuesta y perfiles de agitación
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================================
# PROCESAMIENTO GC CON ESTÁNDAR INTERNO
# ============================================================================

def calcular_concentracion(area_analito, area_IS, C_IS, FR):
    """
    Calcula concentración usando método de estándar interno.

    C_analito = (Area_analito / Area_IS) * C_IS * FR

    Donde FR = factor de respuesta relativo al estándar interno
    """
    return (area_analito / area_IS) * C_IS * FR

def procesar_datos_gc(df, factores_respuesta, C_IS):
    """Procesa áreas de GC y convierte a concentraciones."""

    # Calcular concentraciones
    df['conc_TG'] = calcular_concentracion(df['area_TG'], df['area_IS'], C_IS, factores_respuesta['FR_TG'])
    df['conc_FAME'] = calcular_concentracion(df['area_FAME'], df['area_IS'], C_IS, factores_respuesta['FR_FAME'])
    df['conc_GL'] = calcular_concentracion(df['area_GL'], df['area_IS'], C_IS, factores_respuesta['FR_GL'])

    # Calcular conversión
    C_TG_0 = df['conc_TG'].iloc[0]
    df['conversion_pct'] = (C_TG_0 - df['conc_TG']) / C_TG_0 * 100

    return df

def interpolar_perfil_agitacion(tiempo, config_perfil):
    """Interpola perfil de agitación (rpm vs tiempo)."""
    tipo = config_perfil['tipo']

    if tipo == 'constante':
        return np.ones_like(tiempo) * config_perfil['rpm_constante']

    elif tipo == 'lineal':
        rpm_inicial = config_perfil['rpm_inicial']
        rpm_final = config_perfil['rpm_final']
        return np.linspace(rpm_inicial, rpm_final, len(tiempo))

    elif tipo == 'escalonado':
        escalones = config_perfil['escalones']
        rpm_values = np.zeros_like(tiempo)
        for i, t in enumerate(tiempo):
            for escalon in escalones:
                if t >= escalon['tiempo_inicio'] and t < escalon['tiempo_fin']:
                    rpm_values[i] = escalon['rpm']
                    break
        return rpm_values

    else:
        return np.ones_like(tiempo) * 600  # Default

# ============================================================================
# VISUALIZACIÓN
# ============================================================================

def graficar_areas_gc(df):
    """Gráfica 1: Áreas de picos de GC en función del tiempo."""
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(df['tiempo_min'], df['area_TG'], marker='o', linewidth=2, label='TG', color='#2E86AB')
    ax.plot(df['tiempo_min'], df['area_FAME'], marker='s', linewidth=2, label='FAME', color='#F18F01')
    ax.plot(df['tiempo_min'], df['area_GL'], marker='^', linewidth=2, label='GL', color='#C73E1D')
    ax.axhline(y=df['area_IS'].iloc[0], color='green', linestyle='--', linewidth=2, label='IS (estándar interno)')

    ax.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Área de Pico (unidades arbitrarias)', fontsize=12, fontweight='bold')
    ax.set_title('Áreas de Picos de Cromatografía de Gases (GC-FID)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_concentraciones(df):
    """Gráfica 2: Concentraciones calculadas."""
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(df['tiempo_min'], df['conc_TG'], marker='o', linewidth=2.5, label='TG', color='#2E86AB')
    ax.plot(df['tiempo_min'], df['conc_FAME'], marker='s', linewidth=2.5, label='FAME (biodiesel)', color='#F18F01')
    ax.plot(df['tiempo_min'], df['conc_GL'], marker='^', linewidth=2.5, label='Glicerol', color='#C73E1D')

    ax.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Concentración (mol/L)', fontsize=12, fontweight='bold')
    ax.set_title('Concentraciones Calculadas a partir de GC-FID', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_conversion_agitacion(df, rpm_perfil):
    """Gráfica 3: Conversión y perfil de agitación (eje Y dual)."""
    fig, ax1 = plt.subplots(figsize=(12, 7))

    color1 = '#2E86AB'
    ax1.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Conversión (%)', fontsize=12, fontweight='bold', color=color1)
    ax1.plot(df['tiempo_min'], df['conversion_pct'], linewidth=2.5, marker='o', markersize=6, color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color2 = '#C73E1D'
    ax2.set_ylabel('Agitación (rpm)', fontsize=12, fontweight='bold', color=color2)
    ax2.plot(df['tiempo_min'], rpm_perfil, linewidth=2, linestyle='--', marker='s', markersize=5, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    ax1.set_title('Conversión y Perfil de Agitación', fontsize=14, fontweight='bold')

    plt.tight_layout()
    return fig

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    config_path = Path(__file__).parent / 'config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    print("="*80)
    print("PRÁCTICA 5: PROCESAMIENTO DE DATOS GC-FID")
    print("="*80)
    print("\nProcesando áreas de cromatografía de gases...\n")

    # Cargar datos
    datos_path = Path(__file__).parent / 'datos' / config['archivo_datos']
    df = pd.read_csv(datos_path)

    # Procesar con factores de respuesta
    factores_respuesta = config['factores_respuesta']
    C_IS = config['concentracion_IS_mol_L']

    df = procesar_datos_gc(df, factores_respuesta, C_IS)

    # Perfil de agitación
    rpm_perfil = interpolar_perfil_agitacion(df['tiempo_min'].values, config['perfil_agitacion'])

    print(f"{'Tiempo (min)':<15} {'Área TG':<12} {'Conc TG':<12} {'Conversión (%)':<15}")
    print("-"*80)
    for i in range(0, len(df), 3):
        print(f"{df['tiempo_min'].iloc[i]:<15.0f} {df['area_TG'].iloc[i]:<12.0f} "
              f"{df['conc_TG'].iloc[i]:<12.4f} {df['conversion_pct'].iloc[i]:<15.2f}")

    print("\n" + "="*80)
    print("GENERANDO GRÁFICAS...")
    print("="*80 + "\n")

    fig1 = graficar_areas_gc(df)
    fig2 = graficar_concentraciones(df)
    fig3 = graficar_conversion_agitacion(df, rpm_perfil)

    output_dir = Path(__file__).parent / 'resultados'
    output_dir.mkdir(exist_ok=True)

    fig1.savefig(output_dir / 'grafica1_areas_gc.png', dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / 'grafica2_concentraciones.png', dpi=300, bbox_inches='tight')
    fig3.savefig(output_dir / 'grafica3_conversion_agitacion.png', dpi=300, bbox_inches='tight')

    df.to_csv(output_dir / 'datos_procesados.csv', index=False)

    print(f"✓ Gráficas guardadas en: {output_dir}/")
    plt.show()

    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO")
    print("="*80)
    print("\nPróximos pasos:")
    print("1. Modifica factores de respuesta en config.json")
    print("2. Cambia el perfil de agitación (constante, lineal, escalonado)")
    print("3. Responde las preguntas en analisis.md")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
