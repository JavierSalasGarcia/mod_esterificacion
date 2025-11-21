#!/usr/bin/env python3
"""
Práctica 10: Validación con Datos de Literatura (Kouzu et al. 2008)
Enfoque: AVANZADAS - Comparar modelo con datos experimentales publicados
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import curve_fit
from pathlib import Path

# ============================================================================
# MODELO CINÉTICO
# ============================================================================

def arrhenius(T_C, A, Ea):
    """Ecuación de Arrhenius."""
    R = 8.314e-3  # kJ/(mol·K)
    T_K = T_C + 273.15
    return A * np.exp(-Ea / (R * T_K))

def modelo_simple(y, t, k, relacion_molar):
    """Modelo cinético simplificado de pseudo-primer orden."""
    X = y[0]
    exceso = relacion_molar / 3.0
    dXdt = k * (1 - X) * exceso
    return [dXdt]

def simular_conversion(T_C, tiempo, A, Ea, relacion_molar):
    """Simula conversión a temperatura constante."""
    k = arrhenius(T_C, A, Ea)
    y0 = [0.0]
    sol = odeint(modelo_simple, y0, tiempo, args=(k, relacion_molar))
    return sol[:, 0] * 100  # Convertir a porcentaje

# ============================================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================================

def calcular_R2(y_exp, y_pred):
    """Calcula coeficiente de determinación R²."""
    ss_res = np.sum((y_exp - y_pred)**2)
    ss_tot = np.sum((y_exp - np.mean(y_exp))**2)
    return 1 - (ss_res / ss_tot)

def calcular_RMSE(y_exp, y_pred):
    """Calcula raíz del error cuadrático medio."""
    return np.sqrt(np.mean((y_exp - y_pred)**2))

def calcular_MAPE(y_exp, y_pred):
    """Calcula error porcentual absoluto medio."""
    return np.mean(np.abs((y_exp - y_pred) / y_exp)) * 100

# ============================================================================
# VISUALIZACIÓN
# ============================================================================

def graficar_comparacion_literatura(datos_kouzu, modelo_nuestro, config):
    """Gráfica 1: Comparación con datos de Kouzu et al. 2008."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    temperaturas = [60, 65, 70, 75]
    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

    for idx, T in enumerate(temperaturas):
        ax = axes[idx]

        # Datos experimentales Kouzu
        t_kouzu = datos_kouzu[f'T{T}']['tiempo']
        X_kouzu = datos_kouzu[f'T{T}']['conversion']

        # Nuestro modelo
        t_modelo = modelo_nuestro[f'T{T}']['tiempo']
        X_modelo = modelo_nuestro[f'T{T}']['conversion']

        # Graficar
        ax.scatter(t_kouzu, X_kouzu, s=100, marker='o', color=colores[idx],
                  label='Datos Kouzu et al. (2008)', alpha=0.7, edgecolors='black')
        ax.plot(t_modelo, X_modelo, linewidth=2.5, color=colores[idx],
               linestyle='--', label='Nuestro modelo')

        # Estadísticas
        # Interpolar modelo en tiempos experimentales
        X_modelo_interp = np.interp(t_kouzu, t_modelo, X_modelo)
        R2 = calcular_R2(X_kouzu, X_modelo_interp)
        RMSE = calcular_RMSE(X_kouzu, X_modelo_interp)

        ax.set_xlabel('Tiempo (min)', fontsize=10, fontweight='bold')
        ax.set_ylabel('Conversión (%)', fontsize=10, fontweight='bold')
        ax.set_title(f'T = {T}°C\nR² = {R2:.4f}, RMSE = {RMSE:.2f}%',
                    fontsize=11, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 105])

    plt.tight_layout()
    return fig

def graficar_parametros_cineticos(comparacion_parametros):
    """Gráfica 2: Comparación de parámetros cinéticos."""

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Subplot 1: Factor pre-exponencial A
    ax1 = axes[0]
    fuentes = ['Kouzu et al.\n(2008)', 'Nuestro\nModelo']
    A_values = [comparacion_parametros['A_kouzu'], comparacion_parametros['A_nuestro']]

    bars1 = ax1.bar(fuentes, A_values, color=['#2E86AB', '#F18F01'], width=0.5)
    ax1.set_ylabel('Factor Pre-exponencial A\n(L/mol/min)', fontsize=11, fontweight='bold')
    ax1.set_title('Comparación de A', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)

    # Anotar valores
    for bar, val in zip(bars1, A_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2e}', ha='center', va='bottom', fontweight='bold', fontsize=10)

    # Subplot 2: Energía de activación Ea
    ax2 = axes[1]
    Ea_values = [comparacion_parametros['Ea_kouzu'], comparacion_parametros['Ea_nuestro']]

    bars2 = ax2.bar(fuentes, Ea_values, color=['#2E86AB', '#F18F01'], width=0.5)
    ax2.set_ylabel('Energía de Activación Ea\n(kJ/mol)', fontsize=11, fontweight='bold')
    ax2.set_title('Comparación de Ea', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)

    for bar, val in zip(bars2, Ea_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

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
    print("PRÁCTICA 10: VALIDACIÓN CON LITERATURA (KOUZU ET AL. 2008)")
    print("="*80)
    print("\nComparando modelo con datos experimentales publicados...\n")

    # Datos de Kouzu et al. 2008 (digitalizados de la publicación)
    datos_kouzu = config['datos_kouzu_2008']

    # Simular con nuestros parámetros
    tiempo_sim = np.linspace(0, 120, 200)
    relacion_molar = config['condiciones']['relacion_molar']

    A_nuestro = config['parametros_nuestro_modelo']['A']
    Ea_nuestro = config['parametros_nuestro_modelo']['Ea']

    modelo_nuestro = {}
    for T in [60, 65, 70, 75]:
        X_sim = simular_conversion(T, tiempo_sim, A_nuestro, Ea_nuestro, relacion_molar)
        modelo_nuestro[f'T{T}'] = {'tiempo': tiempo_sim, 'conversion': X_sim}

    # Calcular estadísticas globales
    print("\nESTADÍSTICAS DE VALIDACIÓN:")
    print("-"*80)
    print(f"{'Temperatura':<15} {'R²':<12} {'RMSE (%)':<12} {'MAPE (%)':<12}")
    print("-"*80)

    R2_total = []
    RMSE_total = []

    for T in [60, 65, 70, 75]:
        t_exp = np.array(datos_kouzu[f'T{T}']['tiempo'])
        X_exp = np.array(datos_kouzu[f'T{T}']['conversion'])
        t_modelo = modelo_nuestro[f'T{T}']['tiempo']
        X_modelo = modelo_nuestro[f'T{T}']['conversion']

        X_modelo_interp = np.interp(t_exp, t_modelo, X_modelo)

        R2 = calcular_R2(X_exp, X_modelo_interp)
        RMSE = calcular_RMSE(X_exp, X_modelo_interp)
        MAPE = calcular_MAPE(X_exp, X_modelo_interp)

        R2_total.append(R2)
        RMSE_total.append(RMSE)

        print(f"{T}°C            {R2:>8.4f}    {RMSE:>8.2f}      {MAPE:>8.2f}")

    print("-"*80)
    print(f"PROMEDIO:      {np.mean(R2_total):>8.4f}    {np.mean(RMSE_total):>8.2f}")

    # Comparación de parámetros
    comparacion_parametros = {
        'A_kouzu': config['parametros_kouzu']['A'],
        'Ea_kouzu': config['parametros_kouzu']['Ea'],
        'A_nuestro': A_nuestro,
        'Ea_nuestro': Ea_nuestro
    }

    print("\n" + "="*80)
    print("COMPARACIÓN DE PARÁMETROS CINÉTICOS")
    print("="*80)
    print(f"\nFactor Pre-exponencial A:")
    print(f"  Kouzu et al. (2008): {comparacion_parametros['A_kouzu']:.2e} L/mol/min")
    print(f"  Nuestro modelo:      {comparacion_parametros['A_nuestro']:.2e} L/mol/min")
    print(f"  Diferencia:          {abs(comparacion_parametros['A_kouzu'] - comparacion_parametros['A_nuestro']) / comparacion_parametros['A_kouzu'] * 100:.1f}%")

    print(f"\nEnergía de Activación Ea:")
    print(f"  Kouzu et al. (2008): {comparacion_parametros['Ea_kouzu']:.1f} kJ/mol")
    print(f"  Nuestro modelo:      {comparacion_parametros['Ea_nuestro']:.1f} kJ/mol")
    print(f"  Diferencia:          {abs(comparacion_parametros['Ea_kouzu'] - comparacion_parametros['Ea_nuestro']) / comparacion_parametros['Ea_kouzu'] * 100:.1f}%")

    print("\n" + "="*80)
    print("GENERANDO GRÁFICAS...")
    print("="*80 + "\n")

    fig1 = graficar_comparacion_literatura(datos_kouzu, modelo_nuestro, config)
    fig2 = graficar_parametros_cineticos(comparacion_parametros)

    output_dir = Path(__file__).parent / 'resultados'
    output_dir.mkdir(exist_ok=True)

    fig1.savefig(output_dir / 'grafica1_validacion_kouzu.png', dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / 'grafica2_comparacion_parametros.png', dpi=300, bbox_inches='tight')

    print(f"✓ Gráficas guardadas en: {output_dir}/")
    plt.show()

    print("\n" + "="*80)
    print("VALIDACIÓN COMPLETADA")
    print("="*80)
    print("\nConclusión:")
    if np.mean(R2_total) > 0.95:
        print("✓ Excelente ajuste (R² > 0.95). Modelo validado.")
    elif np.mean(R2_total) > 0.90:
        print("✓ Buen ajuste (R² > 0.90). Modelo aceptable.")
    else:
        print("⚠ Ajuste regular. Considerar mejoras al modelo.")

    print("\nRevisa analisis.md para responder preguntas sobre la validación.")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
