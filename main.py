#!/usr/bin/env python3
"""
Sistema de Modelado de Esterificación para Producción de Biodiésel

Script principal con interfaz de línea de comandos (CLI).

Author: Sistema de Modelado de Esterificación
Date: 2025-11-19
"""

import argparse
import sys
from pathlib import Path
import numpy as np

# Importar módulos del proyecto
from src.data_processing.gc_processor import GCProcessor
from src.data_processing.data_loader import DataLoader
from src.models.kinetic_model import KineticModel
from src.models.parameter_fitting import ParameterFitter
from src.optimization.optimizer import OperationalOptimizer
from src.utils.comparison import ModelComparison
from src.visualization.plotter import ResultsPlotter
from src.visualization.exporter import ResultsExporter


def process_gc_mode(args):
    """Modo: Procesamiento de datos GC-FID."""
    print("=== Modo: Procesamiento de Datos GC-FID ===\n")

    processor = GCProcessor()

    # Cargar datos crudos
    data = processor.load_from_csv(args.input)
    print(f"Datos cargados: {len(data)} filas")

    # Procesar
    C_TG0 = args.c_tg0 if hasattr(args, 'c_tg0') else 0.5  # mol/L
    results = processor.process_time_series(data, C_TG0)

    # Estadísticas
    stats = processor.summary_statistics(results)
    print(f"\nConversión final: {stats['conversion']['final']:.2f}%")
    print(f"Rendimiento FAME final: {stats['FAME_yield']['final']:.2f}%")

    # Exportar
    output_path = Path(args.output) / "processed_gc_data.csv"
    processor.export_processed_data(results, str(output_path), format='csv')

    print(f"\nResultados guardados en: {output_path}")


def fit_params_mode(args):
    """Modo: Ajuste de parámetros cinéticos."""
    print("=== Modo: Ajuste de Parámetros Cinéticos ===\n")

    # Cargar datos experimentales
    loader = DataLoader(args.input)
    data = loader.load_json()

    # Crear fitter
    model_type = args.model_type if hasattr(args, 'model_type') else '1-step'
    fitter = ParameterFitter(model_type=model_type, reversible=True)

    # Agregar experimentos
    if 'experiments' in data:
        for exp in data['experiments']:
            # Convertir a formato apropiado
            # (Esto depende de la estructura exacta de tu JSON)
            fitter.add_experiment(exp['data'], exp['temperature'], exp['C0'], exp['id'])

    # Ajustar
    results = fitter.fit(method='leastsq', verbose=True)

    # Exportar resultados
    output_path = Path(args.output) / "fitted_parameters.json"
    fitter.export_results(str(output_path), format='json')

    print(f"\nParámetros ajustados guardados en: {output_path}")


def optimize_mode(args):
    """Modo: Optimización de variables operacionales."""
    print("=== Modo: Optimización de Variables Operacionales ===\n")

    # Crear modelo
    model = KineticModel(model_type='1-step', reversible=True, temperature=65)

    # Condiciones iniciales
    C0 = {
        'TG': 0.5,
        'MeOH': 4.5,
        'FAME': 0.0,
        'GL': 0.0,
    }

    # Crear optimizador
    optimizer = OperationalOptimizer(model, objective_type='maximize_conversion')

    # Optimizar
    optimal = optimizer.optimize(
        C0=C0,
        t_reaction=120,
        method='differential_evolution',
        maxiter=100,
        verbose=True
    )

    # Exportar resultados
    exporter = ResultsExporter(args.output)
    exporter.export_to_json(optimal, "optimal_conditions.json")

    print(f"\n✓ Condiciones óptimas guardadas en: {args.output}/optimal_conditions.json")


def compare_mode(args):
    """Modo: Comparación de modelos."""
    print("=== Modo: Comparación de Modelos ===\n")

    # Simular modelo 1
    model1 = KineticModel(model_type='1-step', reversible=True, temperature=65)
    C0 = {'TG': 0.5, 'MeOH': 4.5, 'FAME': 0.0, 'GL': 0.0}

    results_model1 = model1.simulate(t_span=(0, 120), C0=C0)

    # Para este ejemplo, usamos el mismo con ruido como segundo modelo
    results_model2 = results_model1.copy()
    results_model2['conversion_%'] += np.random.normal(0, 2, len(results_model2['conversion_%']))

    # Comparar
    comparator = ModelComparison(model1_name="Model1", model2_name="Model2")
    metrics_df = comparator.compare_models(results_model1, results_model2)

    # Imprimir resumen
    print(comparator.generate_summary())

    # Exportar
    output_path = Path(args.output) / "comparison_metrics.xlsx"
    comparator.export_metrics(str(output_path), format='excel')

    print(f"\n✓ Métricas de comparación guardadas en: {output_path}")


def main():
    """Función principal con CLI."""
    parser = argparse.ArgumentParser(
        description='Sistema de Modelado de Esterificación para Producción de Biodiésel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Procesamiento de datos GC
  python main.py --mode process_gc --input data/raw/exp_01.csv --output data/processed/

  # Ajuste de parámetros
  python main.py --mode fit_params --input variables_esterificacion_dataset.json --output results/

  # Optimización de condiciones
  python main.py --mode optimize --output results/

  # Comparación de modelos
  python main.py --mode compare --output results/comparison/
        """
    )

    parser.add_argument('--mode',
                       choices=['process_gc', 'fit_params', 'optimize', 'compare'],
                       required=True,
                       help='Modo de operación')

    parser.add_argument('--input',
                       help='Archivo de entrada')

    parser.add_argument('--output',
                       default='results',
                       help='Directorio de salida (default: results)')

    parser.add_argument('--model-type',
                       choices=['1-step', '3-step'],
                       default='1-step',
                       help='Tipo de modelo cinético (default: 1-step)')

    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Salida detallada')

    args = parser.parse_args()

    # Validar input cuando es requerido
    if args.mode in ['process_gc', 'fit_params'] and not args.input:
        parser.error(f"--input es requerido para modo '{args.mode}'")

    # Ejecutar modo seleccionado
    try:
        if args.mode == 'process_gc':
            process_gc_mode(args)
        elif args.mode == 'fit_params':
            fit_params_mode(args)
        elif args.mode == 'optimize':
            optimize_mode(args)
        elif args.mode == 'compare':
            compare_mode(args)

    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
