#!/usr/bin/env python3
"""
Práctica 9 - Parte A: Cálculos de Escalado
Escala desde reactor lab (350 mL) a reactor piloto (20 L)
"""

import json
import numpy as np
import pandas as pd

with open('config.json') as f:
    config = json.load(f)

lab = config['reactor_lab']
pilot = config['reactor_20L']
props = config['propiedades_fluido_65C']
escalado = config['escalado']

print("="*80)
print("PRACTICA 9 - PARTE A: CALCULOS DE ESCALADO")
print("="*80)

# Convertir unidades
V_lab_m3 = lab['volumen_mL'] / 1e6
V_pilot_m3 = pilot['volumen_L'] / 1000
D_lab_m = lab['diametro_mm'] / 1000
D_pilot_m = pilot['diametro_tanque_mm'] / 1000
D_imp_pilot_m = pilot['impeller']['diametro_mm'] / 1000

rho = props['densidad_kg_m3']
mu = props['viscosidad_Pa_s']
nu = props['viscosidad_cinematica_m2_s']

print(f"\n[REACTOR LABORATORIO]")
print(f"  Volumen: {V_lab_m3*1e6:.0f} mL")
print(f"  Diametro: {D_lab_m*1000:.0f} mm")
print(f"  Agitacion: Mosca magnética ~{lab['agitacion']['rpm_promedio']} rpm")

print(f"\n[REACTOR PILOTO]")
print(f"  Volumen: {V_pilot_m3*1000:.1f} L")
print(f"  Diametro tanque: {D_pilot_m*1000:.0f} mm")
print(f"  Impeller (ribbon): {D_imp_pilot_m*1000:.0f} mm")

# CRITERIO 1: Potencia por volumen constante
print(f"\n{'='*80}")
print("CRITERIO 1: POTENCIA POR VOLUMEN CONSTANTE (P/V)")
print(f"{'='*80}")

P_V_lab = escalado['P_V_lab_estimado_W_L']
P_pilot = P_V_lab * pilot['volumen_L']

# Para ribbon impeller, número de potencia Np ~ 2-5 (bajo Re)
# P = Np * rho * N^3 * D^5
Np_ribbon = 3.0  # Típico para ribbon impeller

# Despejar N (rpm) del reactor piloto
# N = (P / (Np * rho * D^5))^(1/3)
N_pilot_rps = (P_pilot / (Np_ribbon * rho * D_imp_pilot_m**5))**(1/3)
N_pilot_rpm = N_pilot_rps * 60

print(f"  P/V laboratorio: {P_V_lab:.1f} W/L")
print(f"  Potencia piloto requerida: {P_pilot:.2f} W")
print(f"  RPM piloto (ribbon): {N_pilot_rpm:.1f} rpm")

# CRITERIO 2: Número de Reynolds
print(f"\n{'='*80}")
print("CRITERIO 2: NUMERO DE REYNOLDS")
print(f"{'='*80}")

N_lab_rps = lab['agitacion']['rpm_promedio'] / 60
Re_lab = rho * N_lab_rps * D_lab_m**2 / mu

# Para mantener Re constante
N_pilot_Re_rps = Re_lab * mu / (rho * D_imp_pilot_m**2)
N_pilot_Re_rpm = N_pilot_Re_rps * 60

print(f"  Re laboratorio: {Re_lab:.0f}")
print(f"  RPM piloto (Re constante): {N_pilot_Re_rpm:.1f} rpm")

# CRITERIO 3: Velocidad de punta (N*D)
print(f"\n{'='*80}")
print("CRITERIO 3: VELOCIDAD DE PUNTA CONSTANTE (N*D)")
print(f"{'='*80}")

v_tip_lab = np.pi * N_lab_rps * D_lab_m
N_pilot_tip_rps = v_tip_lab / (np.pi * D_imp_pilot_m)
N_pilot_tip_rpm = N_pilot_tip_rps * 60

print(f"  Velocidad punta lab: {v_tip_lab:.3f} m/s")
print(f"  RPM piloto (v_tip constante): {N_pilot_tip_rpm:.1f} rpm")

# CRITERIO 4: Tiempo de mezclado (estimado)
print(f"\n{'='*80}")
print("CRITERIO 4: TIEMPO DE MEZCLADO")
print(f"{'='*80}")

# theta_m ~ V / (N * D^3) para ribbon impeller
theta_m_lab = V_lab_m3 / (N_lab_rps * D_lab_m**3)
N_pilot_tm_rps = V_pilot_m3 / (theta_m_lab * D_imp_pilot_m**3)
N_pilot_tm_rpm = N_pilot_tm_rps * 60

print(f"  Tiempo mezclado lab: {theta_m_lab:.1f} s")
print(f"  RPM piloto (theta_m constante): {N_pilot_tm_rpm:.1f} rpm")

# RESUMEN Y RECOMENDACION
print(f"\n{'='*80}")
print("RESUMEN DE CRITERIOS DE ESCALADO")
print(f"{'='*80}")

resultados = {
    'Criterio': ['P/V constante', 'Re constante', 'v_tip constante', 'theta_m constante'],
    'RPM_piloto': [N_pilot_rpm, N_pilot_Re_rpm, N_pilot_tip_rpm, N_pilot_tm_rpm],
    'Re_piloto': [
        rho * (N_pilot_rpm/60) * D_imp_pilot_m**2 / mu,
        Re_lab,
        rho * (N_pilot_tip_rpm/60) * D_imp_pilot_m**2 / mu,
        rho * (N_pilot_tm_rpm/60) * D_imp_pilot_m**2 / mu
    ]
}

df = pd.DataFrame(resultados)
df['Re_piloto'] = df['Re_piloto'].astype(int)
print(df.to_string(index=False))

# DECISION
RPM_recomendado = N_pilot_rpm  # Usar P/V constante
Re_piloto = rho * (RPM_recomendado/60) * D_imp_pilot_m**2 / mu

print(f"\n{'='*80}")
print("DECISION FINAL")
print(f"{'='*80}")
print(f"  Criterio seleccionado: P/V constante")
print(f"  RPM recomendado: {RPM_recomendado:.1f} rpm")
print(f"  Re resultante: {Re_piloto:.0f}")
print(f"  Regimen: {'Turbulento' if Re_piloto > 10000 else 'Transicion' if Re_piloto > 2000 else 'Laminar'}")

# Guardar resultados
resultados_escalado = {
    'reactor_lab': {
        'volumen_mL': lab['volumen_mL'],
        'rpm': lab['agitacion']['rpm_promedio'],
        'Re': float(Re_lab)
    },
    'reactor_piloto': {
        'volumen_L': pilot['volumen_L'],
        'rpm_recomendado': float(RPM_recomendado),
        'Re': float(Re_piloto),
        'criterio': 'P/V_constante',
        'P_V_W_L': P_V_lab,
        'potencia_total_W': float(P_pilot)
    },
    'comparacion_criterios': df.to_dict('records')
}

with open('resultados_escalado.json', 'w') as f:
    json.dump(resultados_escalado, f, indent=2)

df.to_excel('comparacion_criterios_escalado.xlsx', index=False)

print(f"\nArchivos generados:")
print(f"  - resultados_escalado.json")
print(f"  - comparacion_criterios_escalado.xlsx")
print(f"\n{'='*80}")
