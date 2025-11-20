#!/usr/bin/env python3
"""
Práctica 12: Personalización de Modelos
Enfoque: AVANZADAS - Comparar modelo 1 paso vs 3 pasos y diferentes catalizadores
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from pathlib import Path

# ============================================================================
# MODELOS CINÉTICOS
# ============================================================================

def arrhenius(T_C, A, Ea):
    """Ecuación de Arrhenius."""
    R = 8.314e-3
    T_K = T_C + 273.15
    return A * np.exp(-Ea / (R * T_K))

def modelo_1_paso(y, t, k, relacion_molar):
    """Modelo global simplificado de 1 paso: TG + 3 MeOH → 3 FAME + GL"""
    X = y[0]
    exceso = relacion_molar / 3.0
    dXdt = k * (1 - X) * exceso
    return [dXdt]

def modelo_3_pasos(y, t, k1, k2, k3, k_inv1, k_inv2, k_inv3):
    """Modelo detallado de 3 pasos reversibles."""
    C_TG, C_DG, C_MG, C_GL, C_MeOH, C_FAME = y

    r1 = k1 * C_TG * C_MeOH - k_inv1 * C_DG * C_FAME
    r2 = k2 * C_DG * C_MeOH - k_inv2 * C_MG * C_FAME
    r3 = k3 * C_MG * C_MeOH - k_inv3 * C_GL * C_FAME

    dC_TG = -r1
    dC_DG = r1 - r2
    dC_MG = r2 - r3
    dC_GL = r3
    dC_MeOH = -r1 - r2 - r3
    dC_FAME = r1 + r2 + r3

    return [dC_TG, dC_DG, dC_MG, dC_GL, dC_MeOH, dC_FAME]

def simular_modelo_1_paso(T_C, tiempo, parametros, relacion_molar):
    """Simula con modelo de 1 paso."""
    k = arrhenius(T_C, parametros['A'], parametros['Ea'])
    y0 = [0.0]
    sol = odeint(modelo_1_paso, y0, tiempo, args=(k, relacion_molar))
    return sol[:, 0] * 100

def simular_modelo_3_pasos(T_C, tiempo, parametros, condiciones_iniciales):
    """Simula con modelo de 3 pasos."""
    k1 = arrhenius(T_C, parametros['A1'], parametros['Ea1'])
    k2 = arrhenius(T_C, parametros['A2'], parametros['Ea2'])
    k3 = arrhenius(T_C, parametros['A3'], parametros['Ea3'])
    k_inv1 = arrhenius(T_C, parametros['A_inv1'], parametros['Ea_inv1'])
    k_inv2 = arrhenius(T_C, parametros['A_inv2'], parametros['Ea_inv2'])
    k_inv3 = arrhenius(T_C, parametros['A_inv3'], parametros['Ea_inv3'])

    y0 = [condiciones_iniciales['C_TG_0'], 0, 0, 0,
          condiciones_iniciales['C_MeOH_0'], 0]
    sol = odeint(modelo_3_pasos, y0, tiempo, args=(k1, k2, k3, k_inv1, k_inv2, k_inv3))

    C_TG = sol[:, 0]
    C_TG_0 = condiciones_iniciales['C_TG_0']
    conversion = (C_TG_0 - C_TG) / C_TG_0 * 100
    return conversion, sol

# ============================================================================
# VISUALIZACIÓN
# ============================================================================

def graficar_comparacion_modelos(tiempo, X_1paso, X_3pasos, T):
    """Gráfica 1: Comparación modelo 1 paso vs 3 pasos."""
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(tiempo, X_1paso, linewidth=3, label='Modelo 1 paso (simplificado)',
           color='#2E86AB', linestyle='--')
    ax.plot(tiempo, X_3pasos, linewidth=3, label='Modelo 3 pasos (detallado)',
           color='#F18F01')

    ax.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Conversión (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'Comparación de Modelos Cinéticos a T = {T}°C',
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_especies_3pasos(tiempo, sol):
    """Gráfica 2: Evolución de todas las especies (modelo 3 pasos)."""
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(tiempo, sol[:, 0], label='TG', linewidth=2.5, marker='o', markersize=4, markevery=20)
    ax.plot(tiempo, sol[:, 1], label='DG', linewidth=2.5, marker='s', markersize=4, markevery=20)
    ax.plot(tiempo, sol[:, 2], label='MG', linewidth=2.5, marker='^', markersize=4, markevery=20)
    ax.plot(tiempo, sol[:, 3], label='GL', linewidth=2.5, marker='d', markersize=4, markevery=20)
    ax.plot(tiempo, sol[:, 5], label='FAME', linewidth=3, color='#F18F01')

    ax.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Concentración (mol/L)', fontsize=12, fontweight='bold')
    ax.set_title('Evolución de Especies - Modelo 3 Pasos', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_comparacion_catalizadores(tiempo, resultados_catalizadores):
    """Gráfica 3: Comparación de diferentes catalizadores."""
    fig, ax = plt.subplots(figsize=(12, 7))

    colores = {'NaOH': '#2E86AB', 'CaO': '#F18F01', 'Lipasa': '#C73E1D'}

    for cat, datos in resultados_catalizadores.items():
        ax.plot(tiempo, datos['conversion'], linewidth=3, label=cat,
               color=colores.get(cat, '#000000'), marker='o', markersize=5, markevery=15)

    ax.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Conversión (%)', fontsize=12, fontweight='bold')
    ax.set_title('Comparación de Catalizadores', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

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
    print("PRÁCTICA 12: PERSONALIZACIÓN DE MODELOS")
    print("="*80)
    print("\nComparando diferentes modelos cinéticos y catalizadores...\n")

    tiempo = np.linspace(0, config['tiempo_total_min'], 300)
    T = config['temperatura_C']
    relacion_molar = config['relacion_molar']

    # Comparación 1: Modelo 1 paso vs 3 pasos
    print("PARTE A: COMPARACIÓN DE MODELOS (1 paso vs 3 pasos)")
    print("-"*80)

    # Modelo 1 paso
    X_1paso = simular_modelo_1_paso(T, tiempo, config['modelo_1_paso'], relacion_molar)

    # Modelo 3 pasos
    X_3pasos, sol_3pasos = simular_modelo_3_pasos(T, tiempo,
                                                  config['modelo_3_pasos'],
                                                  config['condiciones_iniciales'])

    print(f"Conversión final - Modelo 1 paso: {X_1paso[-1]:.2f}%")
    print(f"Conversión final - Modelo 3 pasos: {X_3pasos[-1]:.2f}%")
    print(f"Diferencia: {abs(X_1paso[-1] - X_3pasos[-1]):.2f} puntos porcentuales")

    # Comparación 2: Diferentes catalizadores
    print("\nPARTE B: COMPARACIÓN DE CATALIZADORES")
    print("-"*80)

    resultados_catalizadores = {}
    for cat, params in config['catalizadores'].items():
        X_cat = simular_modelo_1_paso(T, tiempo, params, relacion_molar)
        resultados_catalizadores[cat] = {'conversion': X_cat}
        print(f"{cat:<12} - Conversión final: {X_cat[-1]:.2f}%  "
              f"(Ea = {params['Ea']:.1f} kJ/mol)")

    print("\n" + "="*80)
    print("GENERANDO GRÁFICAS...")
    print("="*80 + "\n")

    fig1 = graficar_comparacion_modelos(tiempo, X_1paso, X_3pasos, T)
    fig2 = graficar_especies_3pasos(tiempo, sol_3pasos)
    fig3 = graficar_comparacion_catalizadores(tiempo, resultados_catalizadores)

    output_dir = Path(__file__).parent / 'resultados'
    output_dir.mkdir(exist_ok=True)

    fig1.savefig(output_dir / 'grafica1_comparacion_modelos.png', dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / 'grafica2_especies_3pasos.png', dpi=300, bbox_inches='tight')
    fig3.savefig(output_dir / 'grafica3_comparacion_catalizadores.png', dpi=300, bbox_inches='tight')

    print(f"✓ Gráficas guardadas en: {output_dir}/")
    plt.show()

    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO")
    print("="*80)
    print("\nRevisa analisis.md para responder preguntas sobre personalización de modelos.")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
