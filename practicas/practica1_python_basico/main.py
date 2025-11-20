#!/usr/bin/env python3
"""
Práctica 1: Cálculos Estequiométricos para Transesterificación
Enfoque: OBSERVAR - El estudiante ejecuta y visualiza sin modificar código
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================================
# FUNCIONES DE CÁLCULO
# ============================================================================

def calcular_moles(masa_g, masa_molar_g_mol):
    """Calcula moles a partir de masa y masa molar."""
    return masa_g / masa_molar_g_mol

def calcular_masa_metanol(moles_TG, relacion_molar, masa_molar_MeOH):
    """Calcula masa de metanol necesaria según relación molar."""
    moles_MeOH = moles_TG * relacion_molar
    masa_MeOH_g = moles_MeOH * masa_molar_MeOH
    return masa_MeOH_g, moles_MeOH

def calcular_productos_teoricos(moles_TG, conversion, masas_molares):
    """Calcula masas de productos según conversión teórica."""
    # TG + 3 MeOH → 3 FAME + 1 GL
    moles_TG_reaccionados = moles_TG * conversion

    moles_FAME = moles_TG_reaccionados * 3  # Coeficiente estequiométrico
    moles_GL = moles_TG_reaccionados * 1

    masa_FAME_g = moles_FAME * masas_molares['FAME_metil_palmitato']
    masa_GL_g = moles_GL * masas_molares['GL_glicerol']

    return masa_FAME_g, masa_GL_g, moles_FAME, moles_GL

def calcular_volumenes(masa_g, densidad_g_mL):
    """Calcula volumen a partir de masa y densidad."""
    return masa_g / densidad_g_mL

# ============================================================================
# FUNCIÓN PRINCIPAL DE ANÁLISIS
# ============================================================================

def analizar_escenarios(config):
    """Analiza todos los escenarios y genera datos para visualización."""

    masas_molares = config['masas_molares']
    densidades = config['densidades_25C']
    escenarios = config['escenarios']
    volumen_reactor_mL = config['reactor']['volumen_mL']

    resultados = {}

    for clave, escenario in escenarios.items():
        nombre = escenario['nombre']
        masa_TG_g = escenario['masa_TG_g']
        relacion_molar = escenario['relacion_molar_MeOH_TG']
        conversion = escenario['conversion_esperada_teorica']

        # Cálculos
        moles_TG = calcular_moles(masa_TG_g, masas_molares['TG_tripalmitin'])
        masa_MeOH_g, moles_MeOH = calcular_masa_metanol(
            moles_TG, relacion_molar, masas_molares['MeOH']
        )
        masa_FAME_g, masa_GL_g, moles_FAME, moles_GL = calcular_productos_teoricos(
            moles_TG, conversion, masas_molares
        )

        # Volúmenes
        vol_TG_mL = calcular_volumenes(masa_TG_g, densidades['TG_tripalmitin_g_mL'])
        vol_MeOH_mL = calcular_volumenes(masa_MeOH_g, densidades['MeOH_g_mL'])
        vol_total_reactivos_mL = vol_TG_mL + vol_MeOH_mL

        # Verificación de capacidad del reactor
        excede_capacidad = vol_total_reactivos_mL > volumen_reactor_mL

        resultados[clave] = {
            'nombre': nombre,
            'relacion_molar': relacion_molar,
            'masa_TG_g': masa_TG_g,
            'masa_MeOH_g': masa_MeOH_g,
            'moles_TG': moles_TG,
            'moles_MeOH': moles_MeOH,
            'conversion': conversion,
            'masa_FAME_g': masa_FAME_g,
            'masa_GL_g': masa_GL_g,
            'moles_FAME': moles_FAME,
            'moles_GL': moles_GL,
            'vol_TG_mL': vol_TG_mL,
            'vol_MeOH_mL': vol_MeOH_mL,
            'vol_total_mL': vol_total_reactivos_mL,
            'excede_capacidad': excede_capacidad
        }

    return resultados

# ============================================================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================================================

def graficar_comparacion_masas(resultados, config):
    """Gráfica 1: Comparación de masas de reactivos y productos."""

    nombres = [r['nombre'] for r in resultados.values()]
    masas_TG = [r['masa_TG_g'] for r in resultados.values()]
    masas_MeOH = [r['masa_MeOH_g'] for r in resultados.values()]
    masas_FAME = [r['masa_FAME_g'] for r in resultados.values()]
    masas_GL = [r['masa_GL_g'] for r in resultados.values()]

    x = np.arange(len(nombres))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(x - 1.5*width, masas_TG, width, label='TG (reactivo)', color='#2E86AB')
    ax.bar(x - 0.5*width, masas_MeOH, width, label='MeOH (reactivo)', color='#A23B72')
    ax.bar(x + 0.5*width, masas_FAME, width, label='FAME (producto)', color='#F18F01')
    ax.bar(x + 1.5*width, masas_GL, width, label='Glicerol (producto)', color='#C73E1D')

    ax.set_xlabel('Escenarios', fontsize=12, fontweight='bold')
    ax.set_ylabel('Masa (g)', fontsize=12, fontweight='bold')
    ax.set_title('Comparación de Masas: Reactivos vs Productos', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(nombres, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_relacion_molar_vs_conversion(resultados):
    """Gráfica 2: Relación molar vs conversión esperada."""

    relaciones = [r['relacion_molar'] for r in resultados.values()]
    conversiones = [r['conversion'] * 100 for r in resultados.values()]
    nombres = [r['nombre'] for r in resultados.values()]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(relaciones, conversiones, marker='o', linewidth=2, markersize=10, color='#2E86AB')

    # Anotar cada punto
    for i, nombre in enumerate(nombres):
        ax.annotate(f'{conversiones[i]:.0f}%',
                   xy=(relaciones[i], conversiones[i]),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9, fontweight='bold')

    ax.set_xlabel('Relación Molar (MeOH:TG)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Conversión Esperada (%)', fontsize=12, fontweight='bold')
    ax.set_title('Efecto de la Relación Molar en la Conversión Teórica', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 105])

    plt.tight_layout()
    return fig

def graficar_volumenes_reactor(resultados, config):
    """Gráfica 3: Volúmenes en el reactor."""

    nombres = [r['nombre'] for r in resultados.values()]
    vol_TG = [r['vol_TG_mL'] for r in resultados.values()]
    vol_MeOH = [r['vol_MeOH_mL'] for r in resultados.values()]
    vol_total = [r['vol_total_mL'] for r in resultados.values()]

    volumen_reactor = config['reactor']['volumen_mL']

    x = np.arange(len(nombres))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(x - width/2, vol_TG, width, label='TG', color='#2E86AB')
    ax.bar(x + width/2, vol_MeOH, width, label='MeOH', color='#A23B72')

    # Línea de capacidad del reactor
    ax.axhline(y=volumen_reactor, color='red', linestyle='--', linewidth=2,
               label=f'Capacidad reactor ({volumen_reactor} mL)')

    # Marcar los que exceden capacidad
    for i, excede in enumerate([r['excede_capacidad'] for r in resultados.values()]):
        if excede:
            ax.text(i, vol_total[i] + 5, 'EXCEDE', ha='center',
                   color='red', fontweight='bold', fontsize=9)

    ax.set_xlabel('Escenarios', fontsize=12, fontweight='bold')
    ax.set_ylabel('Volumen (mL)', fontsize=12, fontweight='bold')
    ax.set_title('Volúmenes de Reactivos vs Capacidad del Reactor', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(nombres, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_rendimiento_masa(resultados):
    """Gráfica 4: Rendimiento másico de biodiesel (FAME)."""

    nombres = [r['nombre'] for r in resultados.values()]
    masa_TG = [r['masa_TG_g'] for r in resultados.values()]
    masa_FAME = [r['masa_FAME_g'] for r in resultados.values()]
    rendimiento = [(fame/tg)*100 for fame, tg in zip(masa_FAME, masa_TG)]

    x = np.arange(len(nombres))

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(x, rendimiento, color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'])

    # Anotar valores
    for i, (bar, val) in enumerate(zip(bars, rendimiento)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
               f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')

    ax.set_xlabel('Escenarios', fontsize=12, fontweight='bold')
    ax.set_ylabel('Rendimiento Másico (%)', fontsize=12, fontweight='bold')
    ax.set_title('Rendimiento Másico de Biodiesel (masa FAME / masa TG inicial)',
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(nombres, rotation=15, ha='right')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim([0, max(rendimiento) + 10])

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

    print("="*70)
    print("PRÁCTICA 1: CÁLCULOS ESTEQUIOMÉTRICOS PARA TRANSESTERIFICACIÓN")
    print("="*70)
    print("\nAnalizando escenarios configurados...\n")

    # Analizar todos los escenarios
    resultados = analizar_escenarios(config)

    # Imprimir resumen en consola
    print(f"{'Escenario':<30} {'Relación':<12} {'Conversión':<12} {'FAME (g)':<12}")
    print("-"*70)
    for clave, res in resultados.items():
        print(f"{res['nombre']:<30} {res['relacion_molar']:>6.1f}:1    "
              f"{res['conversion']*100:>6.1f}%      {res['masa_FAME_g']:>8.2f}")

    print("\n" + "="*70)
    print("GENERANDO GRÁFICAS...")
    print("="*70 + "\n")

    # Generar todas las gráficas
    fig1 = graficar_comparacion_masas(resultados, config)
    fig2 = graficar_relacion_molar_vs_conversion(resultados)
    fig3 = graficar_volumenes_reactor(resultados, config)
    fig4 = graficar_rendimiento_masa(resultados)

    # Guardar figuras
    output_dir = Path(__file__).parent / 'resultados'
    output_dir.mkdir(exist_ok=True)

    fig1.savefig(output_dir / 'grafica1_comparacion_masas.png', dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / 'grafica2_relacion_molar_conversion.png', dpi=300, bbox_inches='tight')
    fig3.savefig(output_dir / 'grafica3_volumenes_reactor.png', dpi=300, bbox_inches='tight')
    fig4.savefig(output_dir / 'grafica4_rendimiento_masico.png', dpi=300, bbox_inches='tight')

    print(f"✓ Gráficas guardadas en: {output_dir}/")
    print("\nCerrando ventanas de gráficas en 3 segundos...")
    print("(Puedes cerrarlas manualmente antes si lo deseas)")

    # Mostrar todas las gráficas
    plt.show()

    print("\n" + "="*70)
    print("ANÁLISIS COMPLETADO")
    print("="*70)
    print("\nPróximos pasos:")
    print("1. Revisa las gráficas generadas en la carpeta 'resultados/'")
    print("2. Lee el README.md para responder las preguntas de investigación")
    print("3. Modifica config.json para explorar otros escenarios")
    print("4. Completa tu análisis en analisis.md")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
