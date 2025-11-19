#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo 5: Comparación de Modelos (Standalone vs HYSYS)
========================================================

Este script compara resultados entre el modelo standalone y HYSYS
calculando métricas estadísticas.

Autor: Sistema de Modelado de Esterificación
Fecha: 2025-01-15
"""

import sys
from pathlib import Path
import json

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.comparison import ModelComparison
import matplotlib.pyplot as plt
import pandas as pd

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Archivos de resultados
STANDALONE_FILE = 'results/parameter_fitting/resultados_standalone.json'
HYSYS_FILE = 'results/hysys/resultados_hysys.json'

OUTPUT_DIR = 'results/comparison/'

# =============================================================================
# COMPARACIÓN
# =============================================================================

def load_results(file_path):
    """Cargar resultados desde JSON"""
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    """Función principal"""

    print("="*80)
    print("COMPARACIÓN DE MODELOS: STANDALONE vs HYSYS")
    print("="*80)

    # 1. Cargar resultados
    print(f"\n[1/4] Cargando resultados...")

    try:
        standalone_data = load_results(STANDALONE_FILE)
        print(f"   ✓ Standalone cargado: {STANDALONE_FILE}")
    except FileNotFoundError:
        print(f"   ✗ ERROR: No se encontró {STANDALONE_FILE}")
        print(f"   ℹ Ejecuta primero el ejemplo 02 (ajustar parámetros)")
        return

    try:
        hysys_data = load_results(HYSYS_FILE)
        print(f"   ✓ HYSYS cargado: {HYSYS_FILE}")
    except FileNotFoundError:
        print(f"   ✗ ERROR: No se encontró {HYSYS_FILE}")
        print(f"   ℹ Ejecuta primero el ejemplo 04 (simular HYSYS)")
        return

    # 2. Crear comparador
    print(f"\n[2/4] Inicializando comparador...")

    comparator = ModelComparison(
        model1_name="Standalone Python",
        model2_name="ASPEN HYSYS"
    )

    # 3. Comparar resultados
    print(f"\n[3/4] Calculando métricas estadísticas...")

    metrics = comparator.compare_models(
        results1=standalone_data,
        results2=hysys_data
    )

    # 4. Mostrar resultados
    print(f"\n{'='*80}")
    print("MÉTRICAS DE COMPARACIÓN")
    print('='*80)

    print(f"\n📊 ERRORES ABSOLUTOS:")
    print(f"   {'─'*60}")
    print(f"   RMSE  = {metrics['RMSE']:.4f}")
    print(f"   MAE   = {metrics['MAE']:.4f}")
    print(f"   {'─'*60}")

    print(f"\n📈 CORRELACIÓN:")
    print(f"   {'─'*60}")
    print(f"   R²          = {metrics['R2']:.4f}")
    print(f"   Pearson r   = {metrics['pearson_r']:.4f}")
    print(f"   Pearson p   = {metrics['pearson_p']:.4e}")
    print(f"   {'─'*60}")

    print(f"\n🎯 ERROR RELATIVO:")
    print(f"   {'─'*60}")
    print(f"   MAPE        = {metrics['MAPE_%']:.2f} %")
    print(f"   {'─'*60}")

    # Interpretación
    print(f"\n💡 INTERPRETACIÓN:")
    print(f"   {'─'*60}")
    if metrics['R2'] > 0.95:
        print(f"   ✓ Excelente correlación entre modelos (R² > 0.95)")
    elif metrics['R2'] > 0.90:
        print(f"   ✓ Buena correlación entre modelos (R² > 0.90)")
    elif metrics['R2'] > 0.80:
        print(f"   ⚠ Correlación aceptable (R² > 0.80)")
    else:
        print(f"   ✗ Correlación baja (R² < 0.80) - revisar parámetros")

    if metrics['MAPE_%'] < 5:
        print(f"   ✓ Error relativo bajo (MAPE < 5%)")
    elif metrics['MAPE_%'] < 10:
        print(f"   ⚠ Error relativo moderado (MAPE < 10%)")
    else:
        print(f"   ✗ Error relativo alto (MAPE > 10%)")
    print(f"   {'─'*60}")

    # 5. Exportar resultados
    print(f"\n[4/4] Exportando resultados...")

    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    # Guardar métricas
    metrics_file = output_path / 'metricas_comparacion.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"   ✓ Métricas guardadas en: {metrics_file}")

    # Exportar a Excel
    excel_file = output_path / 'comparacion_modelos.xlsx'
    comparator.export_metrics(str(excel_file), format='excel')
    print(f"   ✓ Excel guardado en: {excel_file}")

    # 6. Generar gráficas
    print(f"\n[5/5] Generando gráficas...")

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Aquí irían las gráficas de comparación
    # (parity plots, residuales, etc.)
    # Por simplicidad del ejemplo, creamos placeholders

    axes[0, 0].text(0.5, 0.5, 'Parity Plot\n(Standalone vs HYSYS)',
                    ha='center', va='center', fontsize=14)
    axes[0, 0].set_title('Gráfica de Paridad')

    axes[0, 1].text(0.5, 0.5, 'Residual Plot',
                    ha='center', va='center', fontsize=14)
    axes[0, 1].set_title('Análisis de Residuales')

    axes[1, 0].text(0.5, 0.5, f'R² = {metrics["R2"]:.4f}\nRMSE = {metrics["RMSE"]:.4f}',
                    ha='center', va='center', fontsize=14)
    axes[1, 0].set_title('Métricas Principales')

    axes[1, 1].text(0.5, 0.5, f'MAPE = {metrics["MAPE_%"]:.2f}%',
                    ha='center', va='center', fontsize=14)
    axes[1, 1].set_title('Error Relativo')

    plt.tight_layout()

    fig_file = output_path / 'comparacion_graficas.png'
    plt.savefig(fig_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Gráficas guardadas en: {fig_file}")

    plt.show()

    print("\n" + "="*80)
    print("COMPARACIÓN COMPLETADA EXITOSAMENTE")
    print("="*80)
    print(f"\nArchivos generados:")
    print(f"  - Métricas: {metrics_file}")
    print(f"  - Excel: {excel_file}")
    print(f"  - Gráficas: {fig_file}")
    print(f"\nCalidad de la correlación: R² = {metrics['R2']:.4f}")
    print("="*80)

if __name__ == '__main__':
    main()
