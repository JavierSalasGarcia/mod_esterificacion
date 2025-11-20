#!/usr/bin/env python3
"""
Práctica 3: Procesamiento de Datos con Pandas
Enfoque: OBSERVAR - El estudiante ejecuta y visualiza sin modificar código
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================================
# FUNCIONES DE CARGA Y PROCESAMIENTO
# ============================================================================

def cargar_datos_experimentales(archivo_csv):
    """
    Carga datos experimentales desde un archivo CSV.

    Parámetros:
    -----------
    archivo_csv : str o Path
        Ruta al archivo CSV

    Retorna:
    --------
    df : pandas.DataFrame
        DataFrame con los datos experimentales
    """
    df = pd.read_csv(archivo_csv)
    return df

def calcular_estadisticas_por_columna(df, columnas_numericas):
    """
    Calcula estadísticas descriptivas para columnas específicas.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame con los datos
    columnas_numericas : list
        Lista de nombres de columnas numéricas

    Retorna:
    --------
    stats : pandas.DataFrame
        DataFrame con estadísticas (media, std, min, max, etc.)
    """
    stats = df[columnas_numericas].describe()
    return stats

def calcular_velocidades_instantaneas(df, columna_y, columna_t='tiempo_min'):
    """
    Calcula la velocidad instantánea (derivada numérica) de una variable.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame con los datos
    columna_y : str
        Nombre de la columna de la variable dependiente
    columna_t : str
        Nombre de la columna de tiempo

    Retorna:
    --------
    velocidades : pandas.Series
        Serie con las velocidades instantáneas
    """
    # Derivada numérica usando diferencias finitas
    dy = df[columna_y].diff()
    dt = df[columna_t].diff()
    velocidades = dy / dt
    return velocidades

def detectar_fase_estacionaria(df, columna='conversion_pct', ventana=5, umbral=1.0):
    """
    Detecta cuándo la reacción alcanza un estado estacionario.

    Criterio: La desviación estándar móvil es menor que un umbral.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame con los datos
    columna : str
        Nombre de la columna a analizar
    ventana : int
        Tamaño de la ventana móvil
    umbral : float
        Umbral de desviación estándar para considerar estacionario

    Retorna:
    --------
    idx : int o None
        Índice donde se alcanza el estado estacionario (o None si no se alcanza)
    """
    std_movil = df[columna].rolling(window=ventana).std()

    # Encontrar el primer punto donde std_movil < umbral
    estacionarios = std_movil < umbral
    if estacionarios.any():
        idx = estacionarios.idxmax()  # Primer índice donde es True
        return idx
    else:
        return None

# ============================================================================
# ANÁLISIS PRINCIPAL
# ============================================================================

def analizar_datos(config):
    """Realiza el análisis completo de los datos experimentales."""

    # Cargar datos
    datos_dir = Path(__file__).parent / 'datos'
    archivo_csv = datos_dir / config['archivo_datos']

    print(f"Cargando datos desde: {archivo_csv}")
    df = cargar_datos_experimentales(archivo_csv)

    print(f"\nDatos cargados exitosamente:")
    print(f"  - Número de filas: {len(df)}")
    print(f"  - Número de columnas: {len(df.columns)}")
    print(f"  - Columnas: {list(df.columns)}")

    # Calcular estadísticas
    columnas_concentracion = ['conc_TG_mol_L', 'conc_MeOH_mol_L', 'conc_FAME_mol_L', 'conc_GL_mol_L']
    stats = calcular_estadisticas_por_columna(df, columnas_concentracion)

    print("\n" + "="*80)
    print("ESTADÍSTICAS DESCRIPTIVAS DE CONCENTRACIONES (mol/L)")
    print("="*80)
    print(stats.to_string())

    # Calcular velocidades de reacción instantáneas
    df['velocidad_conversion'] = calcular_velocidades_instantaneas(df, 'conversion_pct')
    df['velocidad_FAME'] = calcular_velocidades_instantaneas(df, 'conc_FAME_mol_L')

    # Detectar estado estacionario
    idx_estacionario = detectar_fase_estacionaria(df, columna='conversion_pct', ventana=5, umbral=1.0)

    if idx_estacionario is not None:
        tiempo_estacionario = df.loc[idx_estacionario, 'tiempo_min']
        conversion_estacionario = df.loc[idx_estacionario, 'conversion_pct']
        print("\n" + "="*80)
        print("DETECCIÓN DE ESTADO ESTACIONARIO")
        print("="*80)
        print(f"  Estado estacionario alcanzado en t = {tiempo_estacionario:.1f} min")
        print(f"  Conversión en estado estacionario: {conversion_estacionario:.1f}%")
    else:
        print("\n" + "="*80)
        print("DETECCIÓN DE ESTADO ESTACIONARIO")
        print("="*80)
        print("  No se detectó estado estacionario en el tiempo de reacción.")
        idx_estacionario = None

    return df, stats, idx_estacionario

# ============================================================================
# VISUALIZACIÓN
# ============================================================================

def graficar_evolucion_concentraciones(df):
    """Gráfica 1: Evolución temporal de las concentraciones de todas las especies."""

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(df['tiempo_min'], df['conc_TG_mol_L'], label='TG (triglicéridos)',
           linewidth=2.5, marker='o', markersize=5, color='#2E86AB')
    ax.plot(df['tiempo_min'], df['conc_MeOH_mol_L'], label='MeOH (metanol)',
           linewidth=2.5, marker='s', markersize=5, color='#A23B72')
    ax.plot(df['tiempo_min'], df['conc_FAME_mol_L'], label='FAME (biodiesel)',
           linewidth=2.5, marker='^', markersize=5, color='#F18F01')
    ax.plot(df['tiempo_min'], df['conc_GL_mol_L'], label='GL (glicerol)',
           linewidth=2.5, marker='d', markersize=5, color='#C73E1D')

    ax.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Concentración (mol/L)', fontsize=12, fontweight='bold')
    ax.set_title('Evolución Temporal de Concentraciones de Especies', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_conversion_temperatura(df):
    """Gráfica 2: Conversión y temperatura en función del tiempo (eje Y dual)."""

    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Eje Y1: Conversión
    color1 = '#2E86AB'
    ax1.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Conversión (%)', fontsize=12, fontweight='bold', color=color1)
    ax1.plot(df['tiempo_min'], df['conversion_pct'], linewidth=2.5,
            marker='o', markersize=6, color=color1, label='Conversión')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    # Eje Y2: Temperatura
    ax2 = ax1.twinx()
    color2 = '#C73E1D'
    ax2.set_ylabel('Temperatura (°C)', fontsize=12, fontweight='bold', color=color2)
    ax2.plot(df['tiempo_min'], df['temperatura_C'], linewidth=2.5,
            marker='s', markersize=6, color=color2, linestyle='--', label='Temperatura')
    ax2.tick_params(axis='y', labelcolor=color2)

    # Título
    ax1.set_title('Perfil de Conversión y Control de Temperatura', fontsize=14, fontweight='bold')

    # Leyendas combinadas
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

    plt.tight_layout()
    return fig

def graficar_velocidades_reaccion(df):
    """Gráfica 3: Velocidades instantáneas de conversión y formación de FAME."""

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))

    # Subplot 1: Velocidad de conversión
    ax1 = axes[0]
    ax1.plot(df['tiempo_min'], df['velocidad_conversion'], linewidth=2,
            marker='o', markersize=5, color='#2E86AB')
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Tiempo (min)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Velocidad de Conversión (%/min)', fontsize=11, fontweight='bold')
    ax1.set_title('Velocidad Instantánea de Conversión', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Subplot 2: Velocidad de formación de FAME
    ax2 = axes[1]
    ax2.plot(df['tiempo_min'], df['velocidad_FAME'], linewidth=2,
            marker='^', markersize=5, color='#F18F01')
    ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Tiempo (min)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Velocidad de Formación FAME (mol/L/min)', fontsize=11, fontweight='bold')
    ax2.set_title('Velocidad Instantánea de Formación de Biodiesel', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_distribucion_concentraciones_boxplot(df):
    """Gráfica 4: Distribución estadística de concentraciones (boxplot)."""

    columnas = ['conc_TG_mol_L', 'conc_MeOH_mol_L', 'conc_FAME_mol_L', 'conc_GL_mol_L']
    datos_boxplot = [df[col].values for col in columnas]
    etiquetas = ['TG', 'MeOH', 'FAME', 'GL']

    fig, ax = plt.subplots(figsize=(10, 7))

    bp = ax.boxplot(datos_boxplot, labels=etiquetas, patch_artist=True,
                   boxprops=dict(facecolor='#A6CEE3', linewidth=1.5),
                   medianprops=dict(color='#FF5733', linewidth=2),
                   whiskerprops=dict(linewidth=1.5),
                   capprops=dict(linewidth=1.5))

    ax.set_xlabel('Especie Química', fontsize=12, fontweight='bold')
    ax.set_ylabel('Concentración (mol/L)', fontsize=12, fontweight='bold')
    ax.set_title('Distribución Estadística de Concentraciones\n(Min, Q1, Mediana, Q3, Max)',
                fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

def graficar_estado_estacionario(df, idx_estacionario):
    """Gráfica 5: Detección visual del estado estacionario."""

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(df['tiempo_min'], df['conversion_pct'], linewidth=2.5,
           marker='o', markersize=6, color='#2E86AB', label='Conversión')

    if idx_estacionario is not None:
        tiempo_estacionario = df.loc[idx_estacionario, 'tiempo_min']
        conversion_estacionario = df.loc[idx_estacionario, 'conversion_pct']

        ax.axvline(x=tiempo_estacionario, color='red', linestyle='--', linewidth=2,
                  label=f'Estado estacionario (t = {tiempo_estacionario:.1f} min)')
        ax.scatter([tiempo_estacionario], [conversion_estacionario],
                  s=200, color='red', marker='*', zorder=5,
                  label=f'Conversión = {conversion_estacionario:.1f}%')

    ax.set_xlabel('Tiempo (min)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Conversión (%)', fontsize=12, fontweight='bold')
    ax.set_title('Detección de Estado Estacionario en la Reacción', fontsize=14, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3)

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
    print("PRÁCTICA 3: PROCESAMIENTO DE DATOS CON PANDAS")
    print("="*80)
    print("\nProcesando datos experimentales de transesterificación...\n")

    # Análisis
    df, stats, idx_estacionario = analizar_datos(config)

    print("\n" + "="*80)
    print("GENERANDO GRÁFICAS...")
    print("="*80 + "\n")

    # Generar gráficas
    fig1 = graficar_evolucion_concentraciones(df)
    fig2 = graficar_conversion_temperatura(df)
    fig3 = graficar_velocidades_reaccion(df)
    fig4 = graficar_distribucion_concentraciones_boxplot(df)
    fig5 = graficar_estado_estacionario(df, idx_estacionario)

    # Guardar figuras
    output_dir = Path(__file__).parent / 'resultados'
    output_dir.mkdir(exist_ok=True)

    fig1.savefig(output_dir / 'grafica1_evolucion_concentraciones.png', dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / 'grafica2_conversion_temperatura.png', dpi=300, bbox_inches='tight')
    fig3.savefig(output_dir / 'grafica3_velocidades_reaccion.png', dpi=300, bbox_inches='tight')
    fig4.savefig(output_dir / 'grafica4_distribucion_boxplot.png', dpi=300, bbox_inches='tight')
    fig5.savefig(output_dir / 'grafica5_estado_estacionario.png', dpi=300, bbox_inches='tight')

    # Exportar estadísticas a CSV
    stats.to_csv(output_dir / 'estadisticas_descriptivas.csv')

    # Exportar datos procesados (con velocidades calculadas)
    df.to_csv(output_dir / 'datos_procesados.csv', index=False)

    print(f"✓ Gráficas guardadas en: {output_dir}/")
    print(f"✓ Estadísticas exportadas a: {output_dir}/estadisticas_descriptivas.csv")
    print(f"✓ Datos procesados exportados a: {output_dir}/datos_procesados.csv")

    print("\nMostrando gráficas interactivas...")
    print("(Cierra las ventanas para continuar)")

    # Mostrar gráficas
    plt.show()

    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO")
    print("="*80)
    print("\nPróximos pasos:")
    print("1. Revisa las gráficas generadas en la carpeta 'resultados/'")
    print("2. Abre 'datos_procesados.csv' para ver los datos con velocidades calculadas")
    print("3. Lee el README.md para entender el uso de Pandas")
    print("4. Responde las preguntas de investigación en analisis.md")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
