#!/usr/bin/env python3
"""
Práctica 11: Análisis de Sensibilidad de Parámetros Operacionales
Enfoque: AVANZADAS - Diseño de experimentos y superficies de respuesta
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# ============================================================================
# MODELO CINÉTICO
# ============================================================================

def arrhenius(T_C, A, Ea):
    """Ecuación de Arrhenius."""
    R = 8.314e-3
    T_K = T_C + 273.15
    return A * np.exp(-Ea / (R * T_K))

def modelo_simple(y, t, k, factor_agitacion, factor_catalizador):
    """Modelo con factores de agitación y catalizador."""
    X = y[0]
    k_efectiva = k * factor_agitacion * factor_catalizador
    dXdt = k_efectiva * (1 - X)
    return [dXdt]

def simular_con_parametros(T_C, rpm, cat_wt, relacion_molar, A, Ea, tiempo):
    """Simula conversión con parámetros variables."""

    # Factor de agitación (normalizado respecto a 600 rpm)
    factor_agitacion = (rpm / 600) ** 0.5

    # Factor de catalizador (proporcional a concentración)
    factor_catalizador = cat_wt / 1.0  # Normalizado respecto a 1 wt%

    # Factor de relación molar
    factor_relacion = relacion_molar / 6.0  # Normalizado respecto a 6:1

    # Constante de velocidad
    k = arrhenius(T_C, A, Ea) * factor_relacion

    # Resolver EDO
    y0 = [0.0]
    sol = odeint(modelo_simple, y0, tiempo, args=(k, factor_agitacion, factor_catalizador))
    return sol[:, 0] * 100

# ============================================================================
# ANÁLISIS DE SENSIBILIDAD
# ============================================================================

def analisis_un_parametro(parametro_nombre, parametro_rango, valores_base, config):
    """Analiza sensibilidad variando un parámetro."""

    tiempo = np.linspace(0, config['tiempo_total_min'], 100)
    conversiones_finales = []

    for valor in parametro_rango:
        # Actualizar parámetro
        params = valores_base.copy()
        params[parametro_nombre] = valor

        # Simular
        X = simular_con_parametros(
            params['T'], params['rpm'], params['cat'], params['relacion'],
            config['A'], config['Ea'], tiempo
        )
        conversiones_finales.append(X[-1])

    return conversiones_finales

def analisis_dos_parametros(param1_nombre, param1_rango, param2_nombre, param2_rango,
                           valores_base, config):
    """Genera superficie de respuesta para dos parámetros."""

    tiempo = np.linspace(0, config['tiempo_total_min'], 50)

    X_grid, Y_grid = np.meshgrid(param1_rango, param2_rango)
    Z_grid = np.zeros_like(X_grid)

    for i in range(len(param2_rango)):
        for j in range(len(param1_rango)):
            params = valores_base.copy()
            params[param1_nombre] = X_grid[i, j]
            params[param2_nombre] = Y_grid[i, j]

            X_conv = simular_con_parametros(
                params['T'], params['rpm'], params['cat'], params['relacion'],
                config['A'], config['Ea'], tiempo
            )
            Z_grid[i, j] = X_conv[-1]

    return X_grid, Y_grid, Z_grid

# ============================================================================
# VISUALIZACIÓN
# ============================================================================

def graficar_sensibilidad_individual(resultados_sensibilidad, config):
    """Gráfica 1: Sensibilidad individual de cada parámetro (Diagrama de Tornado)."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    parametros = ['T', 'rpm', 'cat', 'relacion']
    nombres = ['Temperatura (°C)', 'Agitación (rpm)', 'Catalizador (wt%)', 'Relación Molar']
    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

    for idx, (param, nombre, color) in enumerate(zip(parametros, nombres, colores)):
        ax = axes[idx]
        rango = resultados_sensibilidad[param]['rango']
        conversiones = resultados_sensibilidad[param]['conversiones']

        ax.plot(rango, conversiones, linewidth=3, marker='o', markersize=8, color=color)
        ax.set_xlabel(nombre, fontsize=11, fontweight='bold')
        ax.set_ylabel('Conversión Final (%)', fontsize=11, fontweight='bold')
        ax.set_title(f'Sensibilidad a {nombre}', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Calcular sensibilidad (pendiente)
        delta_X = max(conversiones) - min(conversiones)
        delta_param = max(rango) - min(rango)
        sensibilidad = delta_X / delta_param
        ax.text(0.05, 0.95, f'ΔX/Δparam = {sensibilidad:.3f}',
               transform=ax.transAxes, fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    return fig

def graficar_superficie_3D(X_grid, Y_grid, Z_grid, xlabel, ylabel):
    """Gráfica 2: Superficie de respuesta 3D."""

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(X_grid, Y_grid, Z_grid, cmap='viridis', alpha=0.8,
                          edgecolor='none')

    ax.set_xlabel(xlabel, fontsize=11, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold')
    ax.set_zlabel('Conversión Final (%)', fontsize=11, fontweight='bold')
    ax.set_title(f'Superficie de Respuesta: {xlabel} vs {ylabel}',
                fontsize=13, fontweight='bold')

    fig.colorbar(surf, shrink=0.5, aspect=5, label='Conversión (%)')

    plt.tight_layout()
    return fig

def graficar_diagrama_pareto(sensibilidades):
    """Gráfica 3: Diagrama de Pareto mostrando parámetros más influyentes."""

    parametros = list(sensibilidades.keys())
    valores = list(sensibilidades.values())

    # Ordenar de mayor a menor
    indices = np.argsort(valores)[::-1]
    parametros_ordenados = [parametros[i] for i in indices]
    valores_ordenados = [valores[i] for i in indices]

    # Porcentaje acumulado
    valores_norm = np.array(valores_ordenados) / sum(valores_ordenados) * 100
    valores_acum = np.cumsum(valores_norm)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    bars = ax1.bar(parametros_ordenados, valores_ordenados, color=colores)
    ax1.set_xlabel('Parámetro', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Sensibilidad (ΔX / Δparam)', fontsize=12, fontweight='bold')
    ax1.set_title('Diagrama de Pareto: Parámetros Críticos', fontsize=14, fontweight='bold')

    # Línea acumulada
    ax2 = ax1.twinx()
    ax2.plot(parametros_ordenados, valores_acum, color='red', marker='D',
            linewidth=2, markersize=8, label='% Acumulado')
    ax2.set_ylabel('Porcentaje Acumulado (%)', fontsize=12, fontweight='bold', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.axhline(y=80, color='red', linestyle='--', alpha=0.5, label='Regla 80/20')

    ax1.grid(axis='y', alpha=0.3)

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
    print("PRÁCTICA 11: ANÁLISIS DE SENSIBILIDAD")
    print("="*80)
    print("\nAnalizando sensibilidad a 4 parámetros operacionales...\n")

    # Valores base
    valores_base = {
        'T': config['valores_base']['temperatura_C'],
        'rpm': config['valores_base']['agitacion_rpm'],
        'cat': config['valores_base']['catalizador_wt'],
        'relacion': config['valores_base']['relacion_molar']
    }

    # Rangos de variación
    rangos = config['rangos_sensibilidad']

    # Análisis individual
    resultados_sensibilidad = {}
    sensibilidades = {}

    for param in ['T', 'rpm', 'cat', 'relacion']:
        rango = np.linspace(rangos[param]['min'], rangos[param]['max'], 20)
        conversiones = analisis_un_parametro(param, rango, valores_base, config)
        resultados_sensibilidad[param] = {'rango': rango, 'conversiones': conversiones}

        # Calcular sensibilidad
        delta_X = max(conversiones) - min(conversiones)
        delta_param = max(rango) - min(rango)
        sensibilidades[param] = delta_X / delta_param

    print("SENSIBILIDADES CALCULADAS:")
    print("-"*80)
    print(f"{'Parámetro':<25} {'Sensibilidad (ΔX/Δparam)':<25} {'Rango explorado':<30}")
    print("-"*80)
    print(f"Temperatura              {sensibilidades['T']:>18.3f}      {rangos['T']['min']}-{rangos['T']['max']} °C")
    print(f"Agitación                {sensibilidades['rpm']:>18.3f}      {rangos['rpm']['min']}-{rangos['rpm']['max']} rpm")
    print(f"Catalizador              {sensibilidades['cat']:>18.3f}      {rangos['cat']['min']}-{rangos['cat']['max']} wt%")
    print(f"Relación Molar           {sensibilidades['relacion']:>18.3f}      {rangos['relacion']['min']:.1f}-{rangos['relacion']['max']:.1f}:1")

    # Identificar parámetro más crítico
    param_critico = max(sensibilidades, key=sensibilidades.get)
    print(f"\n→ PARÁMETRO MÁS CRÍTICO: {param_critico.upper()} (sensibilidad = {sensibilidades[param_critico]:.3f})")

    print("\n" + "="*80)
    print("GENERANDO GRÁFICAS...")
    print("="*80 + "\n")

    # Gráfica 1: Sensibilidad individual
    fig1 = graficar_sensibilidad_individual(resultados_sensibilidad, config)

    # Gráfica 2: Superficie 3D (T vs relacion_molar)
    T_rango = np.linspace(rangos['T']['min'], rangos['T']['max'], 15)
    rel_rango = np.linspace(rangos['relacion']['min'], rangos['relacion']['max'], 15)
    X_grid, Y_grid, Z_grid = analisis_dos_parametros(
        'T', T_rango, 'relacion', rel_rango, valores_base, config
    )
    fig2 = graficar_superficie_3D(X_grid, Y_grid, Z_grid, 'Temperatura (°C)', 'Relación Molar')

    # Gráfica 3: Diagrama de Pareto
    fig3 = graficar_diagrama_pareto(sensibilidades)

    # Guardar
    output_dir = Path(__file__).parent / 'resultados'
    output_dir.mkdir(exist_ok=True)

    fig1.savefig(output_dir / 'grafica1_sensibilidad_individual.png', dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / 'grafica2_superficie_3D.png', dpi=300, bbox_inches='tight')
    fig3.savefig(output_dir / 'grafica3_diagrama_pareto.png', dpi=300, bbox_inches='tight')

    print(f"✓ Gráficas guardadas en: {output_dir}/")
    plt.show()

    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO")
    print("="*80)
    print("\nRevisa analisis.md para interpretar resultados y responder preguntas.")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
