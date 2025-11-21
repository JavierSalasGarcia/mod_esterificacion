#!/usr/bin/env python3
"""
Práctica 4: EDOs y Ecuación de Arrhenius
Enfoque: EXPERIMENTAR - El estudiante modifica config.json para explorar parámetros
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from pathlib import Path

# ============================================================================
# MODELO CINÉTICO CON ARRHENIUS
# ============================================================================

def arrhenius(T_C, A, Ea):
    """
    Ecuación de Arrhenius: k = A * exp(-Ea / RT)

    Parámetros:
    -----------
    T_C : float
        Temperatura en °C
    A : float
        Factor pre-exponencial
    Ea : float
        Energía de activación (kJ/mol)

    Retorna:
    --------
    k : float
        Constante de velocidad
    """
    R = 8.314e-3  # kJ/(mol·K)
    T_K = T_C + 273.15
    k = A * np.exp(-Ea / (R * T_K))
    return k

def modelo_tres_pasos(y, t, k1, k2, k3, k_inv1, k_inv2, k_inv3):
    """
    Modelo cinético de tres pasos reversible:

    TG + MeOH <-> DG + FAME   (k1, k_inv1)
    DG + MeOH <-> MG + FAME   (k2, k_inv2)
    MG + MeOH <-> GL + FAME   (k3, k_inv3)

    Parámetros:
    -----------
    y : list
        [C_TG, C_DG, C_MG, C_GL, C_MeOH, C_FAME]
    t : float
        Tiempo
    k1, k2, k3 : float
        Constantes de velocidad directas
    k_inv1, k_inv2, k_inv3 : float
        Constantes de velocidad inversas

    Retorna:
    --------
    dydt : list
        Derivadas de las concentraciones
    """
    C_TG, C_DG, C_MG, C_GL, C_MeOH, C_FAME = y

    # Velocidades de reacción
    r1 = k1 * C_TG * C_MeOH - k_inv1 * C_DG * C_FAME
    r2 = k2 * C_DG * C_MeOH - k_inv2 * C_MG * C_FAME
    r3 = k3 * C_MG * C_MeOH - k_inv3 * C_GL * C_FAME

    # EDOs
    dC_TG_dt = -r1
    dC_DG_dt = r1 - r2
    dC_MG_dt = r2 - r3
    dC_GL_dt = r3
    dC_MeOH_dt = -r1 - r2 - r3
    dC_FAME_dt = r1 + r2 + r3

    return [dC_TG_dt, dC_DG_dt, dC_MG_dt, dC_GL_dt, dC_MeOH_dt, dC_FAME_dt]

def simular_reaccion(T_C, parametros_cineticos, condiciones_iniciales, tiempo_min):
    """
    Simula la reacción de transesterificación a temperatura constante.

    Parámetros:
    -----------
    T_C : float
        Temperatura en °C
    parametros_cineticos : dict
        Diccionario con A, Ea para cada paso
    condiciones_iniciales : dict
        Concentraciones iniciales
    tiempo_min : array
        Vector de tiempos

    Retorna:
    --------
    solucion : array
        Matriz con las concentraciones [TG, DG, MG, GL, MeOH, FAME]
    """
    # Calcular constantes de velocidad con Arrhenius
    k1 = arrhenius(T_C, parametros_cineticos['A1'], parametros_cineticos['Ea1'])
    k2 = arrhenius(T_C, parametros_cineticos['A2'], parametros_cineticos['Ea2'])
    k3 = arrhenius(T_C, parametros_cineticos['A3'], parametros_cineticos['Ea3'])

    k_inv1 = arrhenius(T_C, parametros_cineticos['A_inv1'], parametros_cineticos['Ea_inv1'])
    k_inv2 = arrhenius(T_C, parametros_cineticos['A_inv2'], parametros_cineticos['Ea_inv2'])
    k_inv3 = arrhenius(T_C, parametros_cineticos['A_inv3'], parametros_cineticos['Ea_inv3'])

    # Condiciones iniciales
    y0 = [
        condiciones_iniciales['C_TG_0'],
        condiciones_iniciales['C_DG_0'],
        condiciones_iniciales['C_MG_0'],
        condiciones_iniciales['C_GL_0'],
        condiciones_iniciales['C_MeOH_0'],
        condiciones_iniciales['C_FAME_0']
    ]

    # Resolver EDOs
    solucion = odeint(modelo_tres_pasos, y0, tiempo_min,
                     args=(k1, k2, k3, k_inv1, k_inv2, k_inv3))

    return solucion

# ============================================================================
# ANÁLISIS DE ESCENARIOS
# ============================================================================

def analizar_escenarios(config):
    """Simula todos los escenarios y calcula constantes de velocidad."""

    parametros_cineticos = config['parametros_cineticos']
    condiciones_iniciales = config['condiciones_iniciales']
    tiempo_total = config['tiempo_total_min']
    tiempo = np.linspace(0, tiempo_total, 300)

    escenarios = config['escenarios']

    resultados = {}

    for clave, escenario in escenarios.items():
        nombre = escenario['nombre']
        T_C = escenario['temperatura_C']

        # Simular
        solucion = simular_reaccion(T_C, parametros_cineticos, condiciones_iniciales, tiempo)

        # Extraer especies
        C_TG = solucion[:, 0]
        C_DG = solucion[:, 1]
        C_MG = solucion[:, 2]
        C_GL = solucion[:, 3]
        C_MeOH = solucion[:, 4]
        C_FAME = solucion[:, 5]

        # Calcular conversión
        C_TG_0 = condiciones_iniciales['C_TG_0']
        conversion = (C_TG_0 - C_TG) / C_TG_0 * 100

        # Constantes de velocidad
        k1 = arrhenius(T_C, parametros_cineticos['A1'], parametros_cineticos['Ea1'])
        k2 = arrhenius(T_C, parametros_cineticos['A2'], parametros_cineticos['Ea2'])
        k3 = arrhenius(T_C, parametros_cineticos['A3'], parametros_cineticos['Ea3'])

        resultados[clave] = {
            'nombre': nombre,
            'temperatura_C': T_C,
            'tiempo': tiempo,
            'C_TG': C_TG,
            'C_DG': C_DG,
            'C_MG': C_MG,
            'C_GL': C_GL,
            'C_MeOH': C_MeOH,
            'C_FAME': C_FAME,
            'conversion': conversion,
            'k1': k1,
            'k2': k2,
            'k3': k3,
            'conversion_final': conversion[-1]
        }

    return resultados

# ============================================================================
# VISUALIZACIÓN
# ============================================================================

def graficar_perfiles_especies(resultados):
    """Gráfica 1: Perfiles de todas las especies para cada temperatura."""

    n_escenarios = len(resultados)
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for idx, (clave, res) in enumerate(resultados.items()):
        ax = axes[idx]

        ax.plot(res['tiempo'], res['C_TG'], label='TG', linewidth=2, marker='o', markersize=3)
        ax.plot(res['tiempo'], res['C_DG'], label='DG', linewidth=2, marker='s', markersize=3)
        ax.plot(res['tiempo'], res['C_MG'], label='MG', linewidth=2, marker='^', markersize=3)
        ax.plot(res['tiempo'], res['C_GL'], label='GL', linewidth=2, marker='d', markersize=3)
        ax.plot(res['tiempo'], res['C_FAME'], label='FAME', linewidth=2.5, marker='*', markersize=5, color='#F18F01')

        ax.set_xlabel('Tiempo (min)', fontsize=10, fontweight='bold')
        ax.set_ylabel('Concentración (mol/L)', fontsize=10, fontweight='bold')
        ax.set_title(f'{res["nombre"]} - T = {res["temperatura_C"]}°C\nConversión final: {res["conversion_final"]:.1f}%',
                    fontsize=11, fontweight='bold')
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_comparacion_conversion(resultados):
    """Gráfica 2: Comparación de conversiones a diferentes temperaturas."""

    fig, ax = plt.subplots(figsize=(12, 7))

    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

    for idx, (clave, res) in enumerate(resultados.items()):
        ax.plot(res['tiempo'], res['conversion'], linewidth=2.5,
               marker='o', markersize=4, markevery=30, color=colores[idx],
               label=f'T = {res["temperatura_C"]}°C (final: {res["conversion_final"]:.1f}%)')

    ax.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Conversión de TG (%)', fontsize=12, fontweight='bold')
    ax.set_title('Efecto de la Temperatura en la Conversión', fontsize=14, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 105])

    plt.tight_layout()
    return fig

def graficar_arrhenius(resultados, parametros_cineticos):
    """Gráfica 3: Gráfico de Arrhenius (ln(k) vs 1/T)."""

    temperaturas_C = [res['temperatura_C'] for res in resultados.values()]
    temperaturas_K = [T + 273.15 for T in temperaturas_C]
    inv_T = [1000 / T for T in temperaturas_K]  # 1000/T para mejor visualización

    k1_values = [res['k1'] for res in resultados.values()]
    k2_values = [res['k2'] for res in resultados.values()]
    k3_values = [res['k3'] for res in resultados.values()]

    ln_k1 = np.log(k1_values)
    ln_k2 = np.log(k2_values)
    ln_k3 = np.log(k3_values)

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.plot(inv_T, ln_k1, marker='o', markersize=10, linewidth=2, label='k1 (TG→DG)', color='#2E86AB')
    ax.plot(inv_T, ln_k2, marker='s', markersize=10, linewidth=2, label='k2 (DG→MG)', color='#A23B72')
    ax.plot(inv_T, ln_k3, marker='^', markersize=10, linewidth=2, label='k3 (MG→GL)', color='#F18F01')

    ax.set_xlabel('1000/T (1/K)', fontsize=12, fontweight='bold')
    ax.set_ylabel('ln(k)', fontsize=12, fontweight='bold')
    ax.set_title('Gráfico de Arrhenius\nPendiente = -Ea/R', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Anotar energías de activación
    text_Ea = (f"Ea1 = {parametros_cineticos['Ea1']:.1f} kJ/mol\n"
              f"Ea2 = {parametros_cineticos['Ea2']:.1f} kJ/mol\n"
              f"Ea3 = {parametros_cineticos['Ea3']:.1f} kJ/mol")
    ax.text(0.05, 0.95, text_Ea, transform=ax.transAxes,
           fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    return fig

def graficar_constantes_vs_temperatura(resultados):
    """Gráfica 4: Constantes de velocidad vs temperatura."""

    temperaturas = [res['temperatura_C'] for res in resultados.values()]
    k1_values = [res['k1'] for res in resultados.values()]
    k2_values = [res['k2'] for res in resultados.values()]
    k3_values = [res['k3'] for res in resultados.values()]

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.plot(temperaturas, k1_values, marker='o', markersize=10, linewidth=2, label='k1 (TG→DG)', color='#2E86AB')
    ax.plot(temperaturas, k2_values, marker='s', markersize=10, linewidth=2, label='k2 (DG→MG)', color='#A23B72')
    ax.plot(temperaturas, k3_values, marker='^', markersize=10, linewidth=2, label='k3 (MG→GL)', color='#F18F01')

    ax.set_xlabel('Temperatura (°C)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Constante de Velocidad k (L/mol/min)', fontsize=12, fontweight='bold')
    ax.set_title('Dependencia de las Constantes de Velocidad con la Temperatura', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta el análisis completo."""

    config_path = Path(__file__).parent / 'config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    print("="*80)
    print("PRÁCTICA 4: EDOs Y ECUACIÓN DE ARRHENIUS")
    print("="*80)
    print("\nSimulando transesterificación con modelo de tres pasos...\n")

    # Analizar escenarios
    resultados = analizar_escenarios(config)

    # Imprimir resumen
    print(f"{'Escenario':<40} {'T (°C)':<10} {'Conv. final (%)':<18} {'k1':<15}")
    print("-"*80)
    for clave, res in resultados.items():
        print(f"{res['nombre']:<40} {res['temperatura_C']:>6.1f}   "
              f"{res['conversion_final']:>12.2f}      {res['k1']:>10.4e}")

    print("\n" + "="*80)
    print("GENERANDO GRÁFICAS...")
    print("="*80 + "\n")

    # Generar gráficas
    fig1 = graficar_perfiles_especies(resultados)
    fig2 = graficar_comparacion_conversion(resultados)
    fig3 = graficar_arrhenius(resultados, config['parametros_cineticos'])
    fig4 = graficar_constantes_vs_temperatura(resultados)

    # Guardar
    output_dir = Path(__file__).parent / 'resultados'
    output_dir.mkdir(exist_ok=True)

    fig1.savefig(output_dir / 'grafica1_perfiles_especies.png', dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / 'grafica2_comparacion_conversion.png', dpi=300, bbox_inches='tight')
    fig3.savefig(output_dir / 'grafica3_arrhenius.png', dpi=300, bbox_inches='tight')
    fig4.savefig(output_dir / 'grafica4_constantes_temperatura.png', dpi=300, bbox_inches='tight')

    print(f"✓ Gráficas guardadas en: {output_dir}/")

    plt.show()

    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO")
    print("="*80)
    print("\nPróximos pasos:")
    print("1. Modifica temperaturas en config.json para explorar otros escenarios")
    print("2. Modifica parámetros cinéticos (A, Ea) para ver su efecto")
    print("3. Responde las preguntas en analisis.md")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
