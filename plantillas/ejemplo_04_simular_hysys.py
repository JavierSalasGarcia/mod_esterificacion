#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo 4: Simulación en ASPEN HYSYS
=====================================

Este script muestra cómo integrar el modelo con ASPEN HYSYS para
validación cruzada.

IMPORTANTE: Requiere ASPEN HYSYS instalado y licencia válida (solo Windows)

Autor: Sistema de Modelado de Esterificación
Fecha: 2025-01-15
"""

import sys
from pathlib import Path
import json
import platform

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# =============================================================================
# VERIFICACIÓN DE PLATAFORMA
# =============================================================================

if platform.system() != 'Windows':
    print("="*80)
    print("ADVERTENCIA: ASPEN HYSYS solo está disponible en Windows")
    print("="*80)
    print("\nEste script requiere:")
    print("  - Sistema operativo: Windows")
    print("  - ASPEN HYSYS instalado")
    print("  - Licencia válida de HYSYS")
    print("\nSi no tienes HYSYS, usa el modelo standalone (ejemplos 01-03)")
    print("="*80)
    sys.exit(1)

from aspen_integration.hysys_connector import HYSYSConnector
from aspen_integration.data_sync import DataSync

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Parámetros cinéticos
PARAMETROS = {
    'A': 2.98e10,   # min⁻¹
    'Ea': 51.9      # kJ/mol
}

# Condiciones de operación
CONDICIONES = {
    'temperatura_C': 65.0,
    'presion_kPa': 101.325,
    'volumen_reactor_L': 20.0,
    'tiempo_residencia_min': 120.0
}

# Composición inicial
COMPOSICION = {
    'Tripalmitin': 0.5,   # mol/L (TG representativo)
    'Methanol': 4.5,      # mol/L
    'MethylPalmitate': 0.0,  # FAME
    'Glycerol': 0.0
}

OUTPUT_DIR = 'results/hysys/'

# =============================================================================
# SIMULACIÓN HYSYS
# =============================================================================

def main():
    """Función principal"""

    print("="*80)
    print("SIMULACIÓN EN ASPEN HYSYS")
    print("="*80)

    # 1. Conectar con HYSYS
    print(f"\n[1/6] Conectando con ASPEN HYSYS...")
    print(f"   Iniciando HYSYS (esto puede tomar 10-30 segundos)...")

    try:
        connector = HYSYSConnector(visible=True)
        print(f"   ✓ Conexión establecida")
    except Exception as e:
        print(f"   ✗ ERROR al conectar con HYSYS: {e}")
        print(f"\n   Posibles causas:")
        print(f"   - HYSYS no está instalado")
        print(f"   - Licencia no válida")
        print(f"   - pywin32 no está instalado (pip install pywin32)")
        return

    # 2. Configurar componentes
    print(f"\n[2/6] Configurando componentes...")

    componentes = ['Methanol', 'Tripalmitin', 'MethylPalmitate', 'Glycerol']
    connector.setup_components(componentes)
    print(f"   ✓ Componentes agregados: {len(componentes)}")

    # 3. Configurar paquete termodinámico
    print(f"\n[3/6] Configurando paquete termodinámico...")

    connector.setup_thermodynamic_package('UNIFAC')
    print(f"   ✓ Paquete: UNIFAC")

    # 4. Crear reactor CSTR
    print(f"\n[4/6] Creando reactor CSTR...")

    reactor = connector.create_cstr_reactor(
        name='Reactor_Biodiésel',
        volume_L=CONDICIONES['volumen_reactor_L'],
        T_celsius=CONDICIONES['temperatura_C'],
        P_kPa=CONDICIONES['presion_kPa']
    )
    print(f"   ✓ Reactor creado")
    print(f"      Volumen: {CONDICIONES['volumen_reactor_L']} L")
    print(f"      T: {CONDICIONES['temperatura_C']} °C")

    # 5. Agregar reacción con cinética
    print(f"\n[5/6] Configurando reacción cinética...")

    estequiometria = {
        'Tripalmitin': -1,
        'Methanol': -3,
        'MethylPalmitate': 3,
        'Glycerol': 1
    }

    connector.add_kinetic_reaction(
        reactor_name='Reactor_Biodiésel',
        stoichiometry=estequiometria,
        kinetic_params={
            'A': PARAMETROS['A'],
            'Ea': PARAMETROS['Ea'],
            'orders': {'Tripalmitin': 1, 'Methanol': 1}
        }
    )
    print(f"   ✓ Cinética Arrhenius configurada")
    print(f"      A  = {PARAMETROS['A']:.2e} min⁻¹")
    print(f"      Ea = {PARAMETROS['Ea']:.1f} kJ/mol")

    # 6. Configurar corrientes de entrada
    print(f"\n[6/6] Configurando corrientes...")

    # Convertir batch a continuo
    sync = DataSync()
    flujos = sync.batch_to_continuous(
        C_batch=COMPOSICION,
        V_reactor_L=CONDICIONES['volumen_reactor_L'],
        tiempo_residencia_min=CONDICIONES['tiempo_residencia_min']
    )

    connector.set_feed_stream(
        stream_name='Alimentacion',
        composition=flujos,
        T_celsius=CONDICIONES['temperatura_C']
    )
    print(f"   ✓ Corriente de alimentación configurada")

    # 7. Ejecutar simulación
    print(f"\n[7/7] Ejecutando simulación...")
    print(f"   {'─'*60}")

    success = connector.run_simulation()

    if success:
        print(f"   ✓ Simulación completada exitosamente")

        # Obtener resultados
        results = connector.get_results()

        print(f"\n{'='*80}")
        print("RESULTADOS DE LA SIMULACIÓN HYSYS")
        print('='*80)

        print(f"\n📊 CONVERSIÓN:")
        print(f"   {'─'*60}")
        print(f"   Conversión TG: {results['conversion_%']:.2f} %")
        print(f"   {'─'*60}")

        print(f"\n🧪 COMPOSICIÓN DE SALIDA:")
        print(f"   {'─'*60}")
        for comp, valor in results['composition'].items():
            print(f"   {comp:20s}: {valor:.4f} mol/L")
        print(f"   {'─'*60}")

        # 8. Exportar resultados
        print(f"\n[8/8] Exportando resultados...")

        output_path = Path(OUTPUT_DIR)
        output_path.mkdir(parents=True, exist_ok=True)

        # Guardar resultados
        results_file = output_path / 'resultados_hysys.json'
        with open(results_file, 'w') as f:
            json.dump({
                'condiciones': CONDICIONES,
                'parametros_cineticos': PARAMETROS,
                'composicion_inicial': COMPOSICION,
                'resultados': results
            }, f, indent=2)

        print(f"   ✓ Resultados guardados en: {results_file}")

        # Guardar caso HYSYS
        case_file = output_path / 'caso_biodiesel.hsc'
        connector.save_case(str(case_file))
        print(f"   ✓ Caso HYSYS guardado en: {case_file}")

    else:
        print(f"   ✗ ERROR: La simulación no convergió")
        print(f"\n   Posibles causas:")
        print(f"   - Condiciones fuera de rango")
        print(f"   - Componentes no disponibles en HYSYS")
        print(f"   - Problemas de convergencia numérica")

    # 9. Cerrar HYSYS
    print(f"\n[9/9] Cerrando HYSYS...")
    connector.close(save=True)
    print(f"   ✓ HYSYS cerrado")

    print("\n" + "="*80)
    print("SIMULACIÓN HYSYS COMPLETADA")
    print("="*80)
    if success:
        print(f"\nArchivos generados:")
        print(f"  - Resultados: {results_file}")
        print(f"  - Caso HYSYS: {case_file}")
        print(f"\nConversión obtenida: {results['conversion_%']:.2f}%")
    print("="*80)

if __name__ == '__main__':
    main()
