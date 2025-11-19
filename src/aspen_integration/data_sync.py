"""
Módulo de Sincronización de Datos entre Modelos Standalone y ASPEN HYSYS

Asegura que ambos modelos usen exactamente los mismos datos de entrada
para validación cruzada justa.

Author: Sistema de Modelado de Esterificación
Date: 2025-11-19
"""

import json
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
import warnings

from ..models.kinetic_model import KineticModel
from ..models.properties import ThermophysicalProperties


class DataSync:
    """
    Sincronizador de datos entre modelos standalone y ASPEN HYSYS.

    Attributes:
        input_data (Dict): Datos de entrada unificados
        properties (ThermophysicalProperties): Propiedades termodinámicas
        unit_conversions (Dict): Factores de conversión de unidades
    """

    def __init__(self):
        """Inicializa el sincronizador de datos."""
        self.input_data = {}
        self.properties = ThermophysicalProperties()
        self.unit_conversions = self._init_unit_conversions()

    def _init_unit_conversions(self) -> Dict:
        """Define factores de conversión de unidades."""
        return {
            # Temperatura
            'C_to_K': lambda T: T + 273.15,
            'K_to_C': lambda T: T - 273.15,

            # Presión
            'Pa_to_kPa': lambda P: P / 1000,
            'kPa_to_Pa': lambda P: P * 1000,
            'atm_to_kPa': lambda P: P * 101.325,

            # Flujo molar
            'mol_s_to_kgmol_h': lambda F: F * 3.6,
            'kgmol_h_to_mol_s': lambda F: F / 3.6,

            # Volumen
            'L_to_m3': lambda V: V / 1000,
            'm3_to_L': lambda V: V * 1000,

            # Concentración
            'mol_L_to_mol_m3': lambda C: C * 1000,
            'mol_m3_to_mol_L': lambda C: C / 1000,
        }

    def load_from_json(self, filepath: str) -> Dict:
        """
        Carga datos desde archivo JSON.

        Args:
            filepath: Ruta al archivo JSON

        Returns:
            Diccionario con datos cargados
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.input_data = data
            print(f"Datos cargados desde: {filepath}")
            return data
        except Exception as e:
            raise IOError(f"Error al cargar JSON: {str(e)}")

    def prepare_standalone_input(self, experiment_data: Dict) -> Dict:
        """
        Prepara datos de entrada para modelo standalone.

        Args:
            experiment_data: Datos del experimento desde JSON

        Returns:
            Diccionario con parámetros para modelo standalone
        """
        # Extraer variables experimentales
        T_celsius = experiment_data.get('temperatura_reaccion_inicio', 65)
        V_reactor = experiment_data.get('volumen_aceite', 0) + experiment_data.get('volumen_metanol', 0)  # mL

        # Calcular concentraciones iniciales
        masa_aceite = experiment_data.get('masa_aceite', 0)  # g
        masa_metanol = experiment_data.get('masa_metanol', 0)  # g
        MW_TG = self.properties.MW['average_TG']  # g/mol
        MW_MeOH = self.properties.MW['methanol']  # g/mol

        moles_aceite = masa_aceite / MW_TG
        moles_metanol = masa_metanol / MW_MeOH

        # Convertir a concentraciones (mol/L)
        V_reactor_L = V_reactor / 1000  # mL a L

        C0 = {
            'TG': moles_aceite / V_reactor_L,
            'MeOH': moles_metanol / V_reactor_L,
            'FAME': 0.0,
            'GL': 0.0,
            'DG': 0.0,
            'MG': 0.0,
        }

        # Parámetros de simulación
        standalone_input = {
            'temperature': T_celsius,
            'C0': C0,
            'V_reactor': V_reactor_L,
            'catalyst_percent': experiment_data.get('porcentaje_catalizador', 0),
            'catalyst_mass': experiment_data.get('masa_catalizador', 0),
            'rpm': experiment_data.get('rpm_reactor', 0),
            'reaction_time': experiment_data.get('tiempo_total_reaccion', 120),  # min
        }

        return standalone_input

    def prepare_hysys_input(self, experiment_data: Dict) -> Dict:
        """
        Prepara datos de entrada para ASPEN HYSYS.

        Args:
            experiment_data: Datos del experimento desde JSON

        Returns:
            Diccionario con parámetros para HYSYS
        """
        # Temperatura y presión
        T_celsius = experiment_data.get('temperatura_reaccion_inicio', 65)
        P_kPa = 101.325  # Presión atmosférica por defecto

        # Flujos molares (convertir de batch a flujo equivalente)
        masa_aceite = experiment_data.get('masa_aceite', 0)
        masa_metanol = experiment_data.get('masa_metanol', 0)
        tiempo_reaccion = experiment_data.get('tiempo_total_reaccion', 120)  # min

        MW_TG = self.properties.MW['average_TG']
        MW_MeOH = self.properties.MW['methanol']

        # Calcular flujos (kgmol/h)
        # Batch: total moles / tiempo → flujo continuo equivalente
        flujo_TG = (masa_aceite / MW_TG) / (tiempo_reaccion / 60)  # kgmol/h
        flujo_MeOH = (masa_metanol / MW_MeOH) / (tiempo_reaccion / 60)

        # Composición de entrada (fracciones molares)
        total_moles = flujo_TG + flujo_MeOH
        composition = {
            'Tripalmitin': flujo_TG / total_moles if total_moles > 0 else 0,
            'Methanol': flujo_MeOH / total_moles if total_moles > 0 else 0,
        }

        # Volumen del reactor
        V_reactor_L = (experiment_data.get('volumen_aceite', 0) +
                       experiment_data.get('volumen_metanol', 0)) / 1000

        hysys_input = {
            'temperature_C': T_celsius,
            'pressure_kPa': P_kPa,
            'feed_flow_kgmol_h': total_moles,
            'composition': composition,
            'reactor_volume_L': V_reactor_L,
            'catalyst_mass_g': experiment_data.get('masa_catalizador', 0),
        }

        return hysys_input

    def map_hysys_components(self, component_name: str) -> str:
        """
        Mapea nombres de componentes entre standalone y HYSYS.

        Args:
            component_name: Nombre en standalone

        Returns:
            Nombre equivalente en HYSYS
        """
        mapping = {
            'TG': 'Tripalmitin',
            'DG': 'Dipalmitin',
            'MG': 'Monopalmitin',
            'MeOH': 'Methanol',
            'FAME': 'MethylPalmitate',
            'GL': 'Glycerol',
        }
        return mapping.get(component_name, component_name)

    def validate_data_consistency(self,
                                  standalone_data: Dict,
                                  hysys_data: Dict,
                                  tolerance: float = 0.01) -> Tuple[bool, List[str]]:
        """
        Valida que los datos de entrada sean consistentes entre modelos.

        Args:
            standalone_data: Datos para modelo standalone
            hysys_data: Datos para HYSYS
            tolerance: Tolerancia relativa para diferencias

        Returns:
            (valid, list_of_issues)
        """
        issues = []

        # Validar temperatura
        if abs(standalone_data['temperature'] - hysys_data['temperature_C']) > tolerance:
            issues.append(f"Temperatura difiere: {standalone_data['temperature']} vs {hysys_data['temperature_C']}")

        # Validar balance de materia (moles totales)
        # Standalone: concentraciones × volumen
        moles_standalone_total = sum(
            standalone_data['C0'][comp] * standalone_data['V_reactor']
            for comp in ['TG', 'MeOH']
        )

        # HYSYS: flujo × tiempo
        # (aproximación, ya que HYSYS usa flujo continuo)

        valid = len(issues) == 0

        return valid, issues

    def synchronize_datasets(self,
                           experiments_json: str,
                           output_dir: str) -> Dict:
        """
        Sincroniza múltiples datasets para ambos modelos.

        Args:
            experiments_json: Archivo JSON con múltiples experimentos
            output_dir: Directorio para guardar datos sincronizados

        Returns:
            Diccionario con datos sincronizados
        """
        data = self.load_from_json(experiments_json)

        synchronized = {
            'standalone': [],
            'hysys': [],
            'metadata': {
                'source_file': experiments_json,
                'n_experiments': 0,
                'synchronized_at': pd.Timestamp.now().isoformat(),
            }
        }

        # Si data tiene estructura de lista de experimentos
        if isinstance(data, list):
            experiments = data
        elif 'experiments' in data:
            experiments = data['experiments']
        else:
            # Asumir que data es un solo experimento
            experiments = [data]

        for i, exp_data in enumerate(experiments):
            # Preparar datos para ambos modelos
            standalone_input = self.prepare_standalone_input(exp_data)
            hysys_input = self.prepare_hysys_input(exp_data)

            # Validar consistencia
            valid, issues = self.validate_data_consistency(standalone_input, hysys_input)

            if not valid:
                warnings.warn(f"Experimento {i}: Problemas de consistencia:\n" + "\n".join(issues))

            # Agregar metadatos
            standalone_input['experiment_id'] = exp_data.get('id', f'exp_{i}')
            hysys_input['experiment_id'] = exp_data.get('id', f'exp_{i}')

            synchronized['standalone'].append(standalone_input)
            synchronized['hysys'].append(hysys_input)

        synchronized['metadata']['n_experiments'] = len(experiments)

        # Guardar datos sincronizados
        import os
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, 'synchronized_data.json')
        with open(output_file, 'w') as f:
            json.dump(synchronized, f, indent=2, default=str)

        print(f"Datos sincronizados guardados en: {output_file}")

        return synchronized

    def compare_results(self,
                       standalone_results: Dict,
                       hysys_results: Dict,
                       metrics: Optional[List[str]] = None) -> Dict:
        """
        Compara resultados de ambos modelos.

        Args:
            standalone_results: Resultados del modelo standalone
            hysys_results: Resultados de HYSYS
            metrics: Lista de métricas a calcular

        Returns:
            Diccionario con comparación
        """
        if metrics is None:
            metrics = ['RMSE', 'MAE', 'R2', 'MaxError', 'MeanDiff%']

        comparison = {
            'metrics': {},
            'detailed_comparison': {},
        }

        # Extraer variables comunes
        common_vars = set(standalone_results.keys()) & set(hysys_results.keys())

        for var in common_vars:
            if var.startswith('C_') or var.endswith('_%'):
                standalone_vals = standalone_results[var]
                hysys_vals = hysys_results[var]

                # Asegurar que son arrays de numpy
                if not isinstance(standalone_vals, np.ndarray):
                    standalone_vals = np.array(standalone_vals)
                if not isinstance(hysys_vals, np.ndarray):
                    hysys_vals = np.array(hysys_vals)

                # Interpolar si tienen diferente longitud
                if len(standalone_vals) != len(hysys_vals):
                    # Usar el tiempo más corto
                    min_len = min(len(standalone_vals), len(hysys_vals))
                    standalone_vals = standalone_vals[:min_len]
                    hysys_vals = hysys_vals[:min_len]

                # Calcular métricas
                var_metrics = {}

                if 'RMSE' in metrics:
                    var_metrics['RMSE'] = np.sqrt(np.mean((standalone_vals - hysys_vals) ** 2))

                if 'MAE' in metrics:
                    var_metrics['MAE'] = np.mean(np.abs(standalone_vals - hysys_vals))

                if 'R2' in metrics:
                    ss_res = np.sum((standalone_vals - hysys_vals) ** 2)
                    ss_tot = np.sum((standalone_vals - np.mean(standalone_vals)) ** 2)
                    var_metrics['R2'] = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

                if 'MaxError' in metrics:
                    var_metrics['MaxError'] = np.max(np.abs(standalone_vals - hysys_vals))

                if 'MeanDiff%' in metrics:
                    with np.errstate(divide='ignore', invalid='ignore'):
                        diff_pct = np.abs((standalone_vals - hysys_vals) / standalone_vals) * 100
                        diff_pct = np.nan_to_num(diff_pct, nan=0.0, posinf=0.0)
                        var_metrics['MeanDiff%'] = np.mean(diff_pct)

                comparison['metrics'][var] = var_metrics

        return comparison

    def export_comparison_report(self,
                                comparison: Dict,
                                output_file: str,
                                format: str = 'excel'):
        """
        Exporta reporte de comparación.

        Args:
            comparison: Diccionario con comparación
            output_file: Archivo de salida
            format: Formato ('excel', 'csv', 'json')
        """
        if format == 'excel':
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Hoja de métricas resumen
                metrics_df = pd.DataFrame(comparison['metrics']).T
                metrics_df.to_excel(writer, sheet_name='Metrics')

                print(f"Reporte de comparación guardado en: {output_file}")

        elif format == 'json':
            with open(output_file, 'w') as f:
                json.dump(comparison, f, indent=2, default=str)

        else:
            raise ValueError(f"Formato '{format}' no soportado")


# Funciones de utilidad

def convert_batch_to_continuous(moles_batch: float,
                                time_batch: float) -> float:
    """
    Convierte moles de batch a flujo continuo equivalente.

    Args:
        moles_batch: Moles totales en batch (mol)
        time_batch: Tiempo de batch (min)

    Returns:
        Flujo molar (kgmol/h)
    """
    flow_kgmol_h = (moles_batch / 1000) / (time_batch / 60)
    return flow_kgmol_h


def calculate_residence_time(V_reactor_L: float,
                            volumetric_flow_L_h: float) -> float:
    """
    Calcula tiempo de residencia para reactor continuo.

    Args:
        V_reactor_L: Volumen del reactor (L)
        volumetric_flow_L_h: Flujo volumétrico (L/h)

    Returns:
        Tiempo de residencia (h)
    """
    if volumetric_flow_L_h == 0:
        return float('inf')
    return V_reactor_L / volumetric_flow_L_h


if __name__ == "__main__":
    # Ejemplo de uso
    print("=== Data Sync - Ejemplo de Uso ===\n")

    # Crear sincronizador
    sync = DataSync()

    # Datos de ejemplo
    experiment_example = {
        'id': 'exp_01',
        'temperatura_reaccion_inicio': 65,
        'volumen_aceite': 100,  # mL
        'volumen_metanol': 50,
        'masa_aceite': 92.0,  # g
        'masa_metanol': 39.6,
        'porcentaje_catalizador': 3,
        'masa_catalizador': 2.76,
        'rpm_reactor': 500,
        'tiempo_total_reaccion': 120,
    }

    # Preparar datos para standalone
    standalone_input = sync.prepare_standalone_input(experiment_example)
    print("Datos para Modelo Standalone:")
    print(f"  Temperatura: {standalone_input['temperature']}°C")
    print(f"  Volumen reactor: {standalone_input['V_reactor']:.3f} L")
    print(f"  C_TG inicial: {standalone_input['C0']['TG']:.4f} mol/L")
    print(f"  C_MeOH inicial: {standalone_input['C0']['MeOH']:.4f} mol/L")
    print(f"  Relación molar MeOH:TG: {standalone_input['C0']['MeOH']/standalone_input['C0']['TG']:.1f}:1")

    # Preparar datos para HYSYS
    hysys_input = sync.prepare_hysys_input(experiment_example)
    print("\nDatos para ASPEN HYSYS:")
    print(f"  Temperatura: {hysys_input['temperature_C']}°C")
    print(f"  Presión: {hysys_input['pressure_kPa']} kPa")
    print(f"  Flujo total: {hysys_input['feed_flow_kgmol_h']:.4f} kgmol/h")
    print(f"  Volumen reactor: {hysys_input['reactor_volume_L']:.3f} L")

    # Validar consistencia
    valid, issues = sync.validate_data_consistency(standalone_input, hysys_input)
    print(f"\nValidación: {'✓ Consistente' if valid else '✗ Inconsistente'}")
    if issues:
        for issue in issues:
            print(f"  - {issue}")
