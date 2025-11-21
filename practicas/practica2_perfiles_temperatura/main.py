#!/usr/bin/env python3
"""
Práctica 2: Perfiles de Temperatura en Transesterificación
Enfoque: OBSERVAR - El estudiante ejecuta y visualiza sin modificar código
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from pathlib import Path

# ============================================================================
# MODELO CINÉTICO CON DEPENDENCIA DE TEMPERATURA
# ============================================================================

def arrhenius(T_C, A, Ea):
    """
    Calcula la constante de velocidad usando la ecuación de Arrhenius.

    k = A * exp(-Ea / (R*T))

    Parámetros:
    -----------
    T_C : float
        Temperatura en °C
    A : float
        Factor pre-exponencial (L/mol/min)
    Ea : float
        Energía de activación (kJ/mol)

    Retorna:
    --------
    k : float
        Constante de velocidad (L/mol/min)
    """
    R = 8.314e-3  # kJ/(mol·K)
    T_K = T_C + 273.15  # Convertir a Kelvin
    k = A * np.exp(-Ea / (R * T_K))
    return k

def modelo_cinetico(y, t, k, relacion_molar):
    """
    Modelo cinético simplificado de pseudo-primer orden.

    Ecuación: -dX/dt = k * (1 - X) * exceso_MeOH

    Donde:
    - X: conversión de triglicéridos (0 a 1)
    - k: constante de velocidad (dependiente de T)
    - exceso_MeOH: factor de exceso de metanol
    """
    X = y[0]
    exceso_MeOH = relacion_molar / 3.0  # Normalizado respecto a estequiométrico
    dXdt = k * (1 - X) * exceso_MeOH
    return [dXdt]

def simular_perfil_temperatura(T_C, tiempo_min, A, Ea, relacion_molar, X0=0.0):
    """
    Simula la conversión en función del tiempo a temperatura constante.

    Parámetros:
    -----------
    T_C : float
        Temperatura en °C (constante)
    tiempo_min : array
        Vector de tiempos (min)
    A : float
        Factor pre-exponencial
    Ea : float
        Energía de activación (kJ/mol)
    relacion_molar : float
        Relación molar MeOH:TG
    X0 : float
        Conversión inicial

    Retorna:
    --------
    X : array
        Conversión en función del tiempo
    """
    k = arrhenius(T_C, A, Ea)
    y0 = [X0]
    solucion = odeint(modelo_cinetico, y0, tiempo_min, args=(k, relacion_molar))
    X = solucion[:, 0]
    return X

# ============================================================================
# ANÁLISIS DE ESCENARIOS
# ============================================================================

def analizar_escenarios(config):
    """Simula todos los escenarios de temperatura."""

    parametros_cineticos = config['parametros_cineticos']
    A = parametros_cineticos['A_factor_preexponencial']
    Ea = parametros_cineticos['Ea_energia_activacion_kJ_mol']

    condiciones_operacion = config['condiciones_operacion']
    relacion_molar = condiciones_operacion['relacion_molar_MeOH_TG']
    tiempo_total_min = condiciones_operacion['tiempo_total_min']

    escenarios = config['escenarios']

    # Vector de tiempo
    tiempo = np.linspace(0, tiempo_total_min, 200)

    resultados = {}

    for clave, escenario in escenarios.items():
        nombre = escenario['nombre']
        T_C = escenario['temperatura_C']

        # Simular conversión
        X = simular_perfil_temperatura(T_C, tiempo, A, Ea, relacion_molar)

        # Calcular constante de velocidad
        k = arrhenius(T_C, A, Ea)

        # Conversión final
        X_final = X[-1] * 100  # Porcentaje

        resultados[clave] = {
            'nombre': nombre,
            'temperatura_C': T_C,
            'tiempo_min': tiempo,
            'conversion': X,
            'conversion_final_pct': X_final,
            'constante_velocidad': k
        }

    return resultados

# ============================================================================
# VISUALIZACIÓN
# ============================================================================

def graficar_perfiles_individuales(resultados):
    """Gráfica 1: Perfiles de conversión individuales (4 subplots)."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

    for idx, (clave, res) in enumerate(resultados.items()):
        ax = axes[idx]

        tiempo = res['tiempo_min']
        conversion = res['conversion'] * 100
        T = res['temperatura_C']
        X_final = res['conversion_final_pct']
        k = res['constante_velocidad']

        ax.plot(tiempo, conversion, linewidth=2.5, color=colores[idx])
        ax.axhline(y=X_final, color=colores[idx], linestyle='--', alpha=0.5)

        ax.set_xlabel('Tiempo (min)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Conversión (%)', fontsize=11, fontweight='bold')
        ax.set_title(f'{res["nombre"]}\nT = {T}°C | X_final = {X_final:.1f}% | k = {k:.4f} L/mol/min',
                    fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 105])

    plt.tight_layout()
    return fig

def graficar_comparacion_temperaturas(resultados):
    """Gráfica 2: Comparación de todas las temperaturas en una sola gráfica."""

    fig, ax = plt.subplots(figsize=(12, 7))

    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

    for idx, (clave, res) in enumerate(resultados.items()):
        tiempo = res['tiempo_min']
        conversion = res['conversion'] * 100
        T = res['temperatura_C']

        ax.plot(tiempo, conversion, linewidth=2.5, color=colores[idx],
               label=f'T = {T}°C (X_final = {res["conversion_final_pct"]:.1f}%)',
               marker='o', markersize=4, markevery=20)

    ax.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Conversión (%)', fontsize=12, fontweight='bold')
    ax.set_title('Efecto de la Temperatura en la Conversión de Triglicéridos',
                fontsize=14, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 105])

    plt.tight_layout()
    return fig

def graficar_constantes_velocidad(resultados):
    """Gráfica 3: Constantes de velocidad vs temperatura (Arrhenius)."""

    temperaturas = [res['temperatura_C'] for res in resultados.values()]
    constantes = [res['constante_velocidad'] for res in resultados.values()]
    nombres = [res['nombre'] for res in resultados.values()]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(temperaturas, constantes, marker='o', linewidth=2.5, markersize=12,
           color='#2E86AB')

    # Anotar valores
    for i, (T, k) in enumerate(zip(temperaturas, constantes)):
        ax.annotate(f'{k:.4f}',
                   xy=(T, k),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9, fontweight='bold')

    ax.set_xlabel('Temperatura (°C)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Constante de Velocidad k (L/mol/min)', fontsize=12, fontweight='bold')
    ax.set_title('Dependencia de la Constante de Velocidad con la Temperatura\n(Ecuación de Arrhenius)',
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_tiempo_90_conversion(resultados):
    """Gráfica 4: Tiempo para alcanzar 90% de conversión vs temperatura."""

    temperaturas = []
    tiempos_90 = []

    for res in resultados.values():
        tiempo = res['tiempo_min']
        conversion = res['conversion'] * 100

        # Encontrar tiempo para 90% conversión
        idx = np.where(conversion >= 90.0)[0]
        if len(idx) > 0:
            t_90 = tiempo[idx[0]]
            temperaturas.append(res['temperatura_C'])
            tiempos_90.append(t_90)

    if not temperaturas:
        # Si ningún escenario alcanza 90%, crear gráfica vacía con mensaje
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Ningún escenario alcanza 90% de conversión\nen el tiempo simulado',
               ha='center', va='center', fontsize=14, fontweight='bold')
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.axis('off')
        return fig

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(range(len(temperaturas)), tiempos_90, color='#F18F01')

    # Anotar valores
    for i, (bar, t) in enumerate(zip(bars, tiempos_90)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
               f'{t:.1f} min', ha='center', va='bottom', fontweight='bold')

    ax.set_xlabel('Temperatura (°C)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Tiempo para 90% conversión (min)', fontsize=12, fontweight='bold')
    ax.set_title('Tiempo Requerido para Alcanzar 90% de Conversión',
                fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(temperaturas)))
    ax.set_xticklabels([f'{T}°C' for T in temperaturas])
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta el análisis completo."""

    # Cargar configuración
    config_path = Path(__file__).parent / 'config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    print("="*80)
    print("PRÁCTICA 2: PERFILES DE TEMPERATURA EN TRANSESTERIFICACIÓN")
    print("="*80)
    print("\nSimulando perfiles de conversión a diferentes temperaturas...\n")

    # Analizar escenarios
    resultados = analizar_escenarios(config)

    # Imprimir resumen
    print(f"{'Escenario':<35} {'T (°C)':<10} {'X_final (%)':<15} {'k (L/mol/min)':<15}")
    print("-"*80)
    for clave, res in resultados.items():
        print(f"{res['nombre']:<35} {res['temperatura_C']:>6.1f}   "
              f"{res['conversion_final_pct']:>10.2f}      {res['constante_velocidad']:>10.4f}")

    print("\n" + "="*80)
    print("GENERANDO GRÁFICAS...")
    print("="*80 + "\n")

    # Generar gráficas
    fig1 = graficar_perfiles_individuales(resultados)
    fig2 = graficar_comparacion_temperaturas(resultados)
    fig3 = graficar_constantes_velocidad(resultados)
    fig4 = graficar_tiempo_90_conversion(resultados)

    # Guardar figuras
    output_dir = Path(__file__).parent / 'resultados'
    output_dir.mkdir(exist_ok=True)

    fig1.savefig(output_dir / 'grafica1_perfiles_individuales.png', dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / 'grafica2_comparacion_temperaturas.png', dpi=300, bbox_inches='tight')
    fig3.savefig(output_dir / 'grafica3_constantes_velocidad.png', dpi=300, bbox_inches='tight')
    fig4.savefig(output_dir / 'grafica4_tiempo_90_conversion.png', dpi=300, bbox_inches='tight')

    print(f"✓ Gráficas guardadas en: {output_dir}/")
    print("\nMostrando gráficas interactivas...")
    print("(Cierra las ventanas para continuar)")

    # Mostrar gráficas
    plt.show()

    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO")
    print("="*80)
    print("\nPróximos pasos:")
    print("1. Revisa las gráficas generadas en la carpeta 'resultados/'")
    print("2. Lee el README.md para entender los conceptos clave")
    print("3. Responde las preguntas de investigación en analisis.md")
    print("4. Modifica config.json para explorar otros escenarios de temperatura")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
