"""
Módulo de Integración con ASPEN HYSYS

Conexión vía COM (Component Object Model) con ASPEN HYSYS para simulación
de reactores de transesterificación y validación cruzada de modelos.

Author: Sistema de Modelado de Esterificación
Date: 2025-11-19

NOTA: Este módulo requiere Windows y ASPEN HYSYS instalado
"""

import os
import warnings
from typing import Dict, List, Optional, Tuple
import numpy as np

# Importación condicional de win32com (solo Windows)
try:
    import win32com.client as win32
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    warnings.warn("pywin32 no disponible. Módulo HYSYS no funcionará.")


class HYSYSConnector:
    """
    Conector con ASPEN HYSYS vía COM automation.

    Attributes:
        hyApp: Aplicación HYSYS
        hyCase: Caso de simulación activo
        hyFlowsheet: Flowsheet del caso
        case_file (str): Ruta al archivo .hsc
    """

    def __init__(self,
                 case_file: Optional[str] = None,
                 visible: bool = True,
                 version: Optional[str] = None):
        """
        Inicializa conexión con ASPEN HYSYS.

        Args:
            case_file: Ruta al archivo .hsc (si None, crea caso nuevo)
            visible: Si mostrar interfaz gráfica de HYSYS
            version: Versión específica de HYSYS (si None, usa default)

        Raises:
            RuntimeError: Si pywin32 no está disponible o HYSYS no se puede iniciar
        """
        if not WIN32_AVAILABLE:
            raise RuntimeError("pywin32 no está instalado. Ejecute: pip install pywin32")

        self.hyApp = None
        self.hyCase = None
        self.hyFlowsheet = None
        self.case_file = case_file

        try:
            # Conectar con HYSYS Application
            if version:
                prog_id = f'HYSYS.Application.{version}'
            else:
                prog_id = 'HYSYS.Application'

            self.hyApp = win32.Dispatch(prog_id)
            self.hyApp.Visible = visible

            # Abrir o crear caso
            if case_file and os.path.exists(case_file):
                self.hyCase = self.hyApp.SimulationCases.Open(case_file)
                print(f"Archivo HYSYS cargado: {case_file}")
            else:
                self.hyCase = self.hyApp.SimulationCases.Add()
                print("Nuevo caso HYSYS creado")

            self.hyFlowsheet = self.hyCase.Flowsheet

        except Exception as e:
            raise RuntimeError(f"No se pudo conectar con HYSYS: {str(e)}")

    def close(self, save: bool = False):
        """
        Cierra la conexión con HYSYS.

        Args:
            save: Si guardar el caso antes de cerrar
        """
        try:
            if save and self.case_file:
                self.hyCase.Save()
                print(f"Caso guardado: {self.case_file}")

            self.hyCase.Close()
            self.hyApp.Quit()
            print("HYSYS cerrado")

        except Exception as e:
            warnings.warn(f"Error al cerrar HYSYS: {str(e)}")

    def setup_components(self, components: List[str]):
        """
        Configura componentes del sistema.

        Args:
            components: Lista de componentes (nombres HYSYS)

        Example:
            >>> connector.setup_components(['Methanol', 'Tripalmitin', 'Glycerol'])
        """
        try:
            comp_list = self.hyCase.Flowsheet.FluidPackage.Components

            for comp_name in components:
                comp_list.Add(comp_name)

            print(f"Componentes agregados: {', '.join(components)}")

        except Exception as e:
            warnings.warn(f"Error al agregar componentes: {str(e)}")

    def setup_thermodynamic_package(self, package_name: str = 'UNIFAC'):
        """
        Configura paquete termodinámico.

        Args:
            package_name: Nombre del paquete ('UNIFAC', 'NRTL', 'Peng-Robinson', etc.)
        """
        try:
            fluid_pkg = self.hyCase.Flowsheet.FluidPackages.Add()
            fluid_pkg.PropertyPackage = package_name
            print(f"Paquete termodinámico configurado: {package_name}")

        except Exception as e:
            warnings.warn(f"Error al configurar paquete termodinámico: {str(e)}")

    def create_material_stream(self,
                              name: str,
                              T_celsius: float,
                              P_kPa: float,
                              flow_kgmol_h: float,
                              composition: Dict[str, float]) -> object:
        """
        Crea corriente de materia.

        Args:
            name: Nombre de la corriente
            T_celsius: Temperatura (°C)
            P_kPa: Presión (kPa)
            flow_kgmol_h: Flujo molar (kgmol/h)
            composition: Composición molar {componente: fracción}

        Returns:
            Objeto MaterialStream de HYSYS
        """
        try:
            stream = self.hyFlowsheet.MaterialStreams.Add(name)

            # Configurar condiciones
            stream.Temperature.SetValue(T_celsius, "C")
            stream.Pressure.SetValue(P_kPa, "kPa")
            stream.MolarFlow.SetValue(flow_kgmol_h, "kgmol/h")

            # Configurar composición
            comp_obj = stream.ComponentMolarFraction
            for comp_name, fraction in composition.items():
                comp_obj.SetValue(comp_name, fraction)

            print(f"Corriente '{name}' creada: T={T_celsius}°C, P={P_kPa}kPa, F={flow_kgmol_h}kgmol/h")
            return stream

        except Exception as e:
            warnings.warn(f"Error al crear corriente: {str(e)}")
            return None

    def create_cstr_reactor(self,
                           name: str,
                           volume_L: float,
                           T_celsius: Optional[float] = None,
                           duty_kW: Optional[float] = None) -> object:
        """
        Crea reactor CSTR (Continuous Stirred Tank Reactor).

        Args:
            name: Nombre del reactor
            volume_L: Volumen del reactor (L)
            T_celsius: Temperatura isotérmica (°C), si None es adiabático
            duty_kW: Duty térmico (kW), si None calculado

        Returns:
            Objeto CSTR de HYSYS
        """
        try:
            # Agregar operación CSTR
            reactor = self.hyFlowsheet.Operations.Add("CSTR", name)

            # Configurar volumen
            reactor.Volume.SetValue(volume_L, "L")

            # Configurar temperatura (si isotérmico)
            if T_celsius is not None:
                reactor.Temperature.SetValue(T_celsius, "C")

            # Configurar duty
            if duty_kW is not None:
                reactor.Duty.SetValue(duty_kW, "kW")

            print(f"Reactor CSTR '{name}' creado: V={volume_L}L, T={T_celsius}°C")
            return reactor

        except Exception as e:
            warnings.warn(f"Error al crear reactor CSTR: {str(e)}")
            return None

    def add_kinetic_reaction(self,
                            reactor_name: str,
                            reaction_type: str = 'Kinetic',
                            stoichiometry: Dict[str, float] = None,
                            kinetic_params: Dict = None):
        """
        Agrega reacción cinética al reactor.

        Args:
            reactor_name: Nombre del reactor
            reaction_type: Tipo de reacción ('Kinetic', 'Equilibrium', 'Conversion')
            stoichiometry: Coeficientes estequiométricos {componente: coef} (negativos=reactivos)
            kinetic_params: Parámetros cinéticos {'A': valor, 'Ea': valor, 'order': dict}

        Example:
            >>> stoich = {'Tripalmitin': -1, 'Methanol': -3, 'MethylPalmitate': 3, 'Glycerol': 1}
            >>> params = {'A': 2.98e10, 'Ea': 51900, 'order': {'Tripalmitin': 1, 'Methanol': 1}}
            >>> connector.add_kinetic_reaction('R-100', stoichiometry=stoich, kinetic_params=params)
        """
        try:
            reactor = self.hyFlowsheet.Operations.Item(reactor_name)

            # Crear set de reacciones
            rxn_set = reactor.ReactionSet

            # Agregar reacción
            if reaction_type == 'Kinetic':
                reaction = rxn_set.KineticReactions.Add()

                # Configurar estequiometría
                if stoichiometry:
                    for comp, coef in stoichiometry.items():
                        if coef < 0:
                            reaction.Reactants.Add(comp, abs(coef))
                        else:
                            reaction.Products.Add(comp, coef)

                # Configurar cinética (si se proporcionan parámetros)
                if kinetic_params:
                    # Factor pre-exponencial
                    if 'A' in kinetic_params:
                        reaction.PreExponentialFactor.SetValue(kinetic_params['A'], "")

                    # Energía de activación
                    if 'Ea' in kinetic_params:
                        reaction.ActivationEnergy.SetValue(kinetic_params['Ea'], "J/kgmol")

                    # Órdenes de reacción
                    if 'order' in kinetic_params:
                        for comp, order in kinetic_params['order'].items():
                            reaction.ReactionOrders.SetValue(comp, order)

                print(f"Reacción cinética agregada a '{reactor_name}'")

        except Exception as e:
            warnings.warn(f"Error al agregar reacción: {str(e)}")

    def run_simulation(self, max_iterations: int = 100, tolerance: float = 1e-6) -> bool:
        """
        Ejecuta la simulación.

        Args:
            max_iterations: Número máximo de iteraciones
            tolerance: Tolerancia de convergencia

        Returns:
            True si converge, False si no
        """
        try:
            solver = self.hyCase.Solver

            # Configurar solver
            solver.CanSolve = True

            # Esperar convergencia
            converged = solver.IsSolved

            if converged:
                print("Simulación convergió exitosamente")
            else:
                warnings.warn("Simulación no convergió")

            return converged

        except Exception as e:
            warnings.warn(f"Error durante simulación: {str(e)}")
            return False

    def get_stream_properties(self, stream_name: str) -> Dict:
        """
        Obtiene propiedades de una corriente.

        Args:
            stream_name: Nombre de la corriente

        Returns:
            Diccionario con propiedades
        """
        try:
            stream = self.hyFlowsheet.MaterialStreams.Item(stream_name)

            properties = {
                'temperature_C': stream.Temperature.GetValue("C"),
                'pressure_kPa': stream.Pressure.GetValue("kPa"),
                'molar_flow_kgmol_h': stream.MolarFlow.GetValue("kgmol/h"),
                'mass_flow_kg_h': stream.MassFlow.GetValue("kg/h"),
                'composition': {}
            }

            # Composición molar
            comp_obj = stream.ComponentMolarFraction
            for i in range(comp_obj.Count):
                comp_name = comp_obj.Item(i).ComponentName
                fraction = comp_obj.GetValue(comp_name)
                properties['composition'][comp_name] = fraction

            return properties

        except Exception as e:
            warnings.warn(f"Error al obtener propiedades: {str(e)}")
            return {}

    def get_reactor_results(self, reactor_name: str) -> Dict:
        """
        Obtiene resultados del reactor.

        Args:
            reactor_name: Nombre del reactor

        Returns:
            Diccionario con resultados
        """
        try:
            reactor = self.hyFlowsheet.Operations.Item(reactor_name)

            results = {
                'conversion_%': {},
                'temperature_C': reactor.Temperature.GetValue("C"),
                'duty_kW': reactor.Duty.GetValue("kW"),
                'volume_L': reactor.Volume.GetValue("L"),
            }

            # Conversión por componente (si disponible)
            try:
                for rxn_idx in range(reactor.ReactionSet.KineticReactions.Count):
                    rxn = reactor.ReactionSet.KineticReactions.Item(rxn_idx)
                    # La conversión se puede obtener del componente limitante
                    # Esto varía según la configuración de HYSYS
                    pass
            except:
                pass

            return results

        except Exception as e:
            warnings.warn(f"Error al obtener resultados del reactor: {str(e)}")
            return {}

    def save_case(self, filepath: Optional[str] = None):
        """
        Guarda el caso actual.

        Args:
            filepath: Ruta donde guardar (si None, usa self.case_file)
        """
        try:
            if filepath:
                self.hyCase.SaveAs(filepath)
                self.case_file = filepath
            elif self.case_file:
                self.hyCase.Save()
            else:
                raise ValueError("Debe proporcionar filepath o tener case_file definido")

            print(f"Caso guardado: {filepath or self.case_file}")

        except Exception as e:
            warnings.warn(f"Error al guardar caso: {str(e)}")

    def export_to_excel(self, filepath: str):
        """
        Exporta resultados a Excel (función de HYSYS).

        Args:
            filepath: Ruta del archivo Excel
        """
        try:
            self.hyCase.ExportToExcel(filepath)
            print(f"Resultados exportados a: {filepath}")

        except Exception as e:
            warnings.warn(f"Error al exportar a Excel: {str(e)}")

    # Métodos de utilidad

    def list_operations(self) -> List[str]:
        """Lista todas las operaciones unitarias del flowsheet."""
        try:
            operations = []
            for i in range(self.hyFlowsheet.Operations.Count):
                op = self.hyFlowsheet.Operations.Item(i)
                operations.append(f"{op.Name} ({op.TypeName})")
            return operations
        except:
            return []

    def list_streams(self) -> List[str]:
        """Lista todas las corrientes de materia."""
        try:
            streams = []
            for i in range(self.hyFlowsheet.MaterialStreams.Count):
                stream = self.hyFlowsheet.MaterialStreams.Item(i)
                streams.append(stream.Name)
            return streams
        except:
            return []


# Funciones auxiliares

def check_hysys_availability() -> Tuple[bool, str]:
    """
    Verifica si ASPEN HYSYS está disponible.

    Returns:
        (disponible, mensaje)
    """
    if not WIN32_AVAILABLE:
        return False, "pywin32 no está instalado"

    try:
        app = win32.Dispatch('HYSYS.Application')
        version = app.Version
        app.Quit()
        return True, f"HYSYS disponible (Versión: {version})"
    except:
        return False, "HYSYS no está instalado o no se puede acceder"


def create_biodiesel_case_template(filepath: str,
                                   oil_type: str = 'palm',
                                   catalyst: str = 'CaO') -> HYSYSConnector:
    """
    Crea un caso template de HYSYS para biodiésel.

    Args:
        filepath: Ruta donde guardar el caso
        oil_type: Tipo de aceite ('palm', 'soybean', 'used_cooking')
        catalyst: Catalizador ('CaO', 'NaOH', 'KOH')

    Returns:
        Instancia de HYSYSConnector configurada
    """
    # Componentes típicos
    if oil_type == 'palm':
        components = ['Tripalmitin', 'Methanol', 'MethylPalmitate', 'Glycerol']
    elif oil_type == 'soybean':
        components = ['Triolein', 'Methanol', 'MethylOleate', 'Glycerol']
    else:  # used cooking oil (mixture)
        components = ['Tripalmitin', 'Triolein', 'Methanol', 'MethylPalmitate', 'MethylOleate', 'Glycerol']

    connector = HYSYSConnector(visible=True)

    # Setup básico
    connector.setup_components(components)
    connector.setup_thermodynamic_package('UNIFAC')

    # Crear corrientes de alimentación
    # (Esto se puede personalizar más)

    # Guardar template
    connector.save_case(filepath)

    return connector


if __name__ == "__main__":
    # Verificar disponibilidad
    available, message = check_hysys_availability()
    print(f"HYSYS: {message}")

    if available:
        print("\n=== Ejemplo de Uso de HYSYS Connector ===")
        print("NOTA: Este ejemplo requiere HYSYS instalado en Windows")

        # Crear conector (esto iniciará HYSYS)
        # connector = HYSYSConnector(visible=True)

        # Configurar componentes
        # connector.setup_components(['Methanol', 'Tripalmitin', 'MethylPalmitate', 'Glycerol'])

        # ... más configuración ...

        # connector.close()
    else:
        print("Para usar este módulo, instale ASPEN HYSYS en Windows y ejecute: pip install pywin32")
