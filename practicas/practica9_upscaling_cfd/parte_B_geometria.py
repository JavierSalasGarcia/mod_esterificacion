#!/usr/bin/env python3
"""
Práctica 9 - Parte B: Generación de Geometría
Reactor + Ribbon Impeller + Serpentín
"""

import json
import numpy as np

with open('config.json') as f:
    config = json.load(f)

pilot = config['reactor_20L']
serpent = pilot['serpentin']

print("="*80)
print("PARTE B: GENERACION DE GEOMETRIA")
print("="*80)

# REACTOR CILINDRICO
D_tank = pilot['diametro_tanque_mm'] / 1000  # m
H_liquid = pilot['altura_liquido_mm'] / 1000  # m
R_tank = D_tank / 2

print(f"\n[REACTOR CILINDRICO]")
print(f"  Diametro: {D_tank*1000:.0f} mm")
print(f"  Altura liquido: {H_liquid*1000:.0f} mm")
print(f"  Volumen: {np.pi * R_tank**2 * H_liquid * 1000:.1f} L")

# RIBBON IMPELLER
imp = pilot['impeller']
D_ribbon = imp['diametro_mm'] / 1000
H_ribbon = imp['altura_mm'] / 1000
pitch = imp['pitch_mm'] / 1000
n_helices = imp['num_helices']

print(f"\n[RIBBON IMPELLER]")
print(f"  Tipo: {imp['tipo']} (helice helicoidal)")
print(f"  Diametro: {D_ribbon*1000:.0f} mm")
print(f"  Altura: {H_ribbon*1000:.0f} mm")
print(f"  Pitch: {pitch*1000:.0f} mm/vuelta")
print(f"  Numero de helices: {n_helices}")

# Generar coordenadas del ribbon (simplificado)
theta_ribbon = np.linspace(0, 2*np.pi*H_ribbon/pitch, 200)
r_ribbon = D_ribbon/2
x_ribbon = r_ribbon * np.cos(theta_ribbon)
y_ribbon = r_ribbon * np.sin(theta_ribbon)
z_ribbon = (theta_ribbon / (2*np.pi)) * pitch

print(f"  Puntos generados: {len(theta_ribbon)}")

# SERPENTIN
n_espiras = serpent['numero_espiras']
D_serpent = serpent['diametro_helice_mm'] / 1000
d_tubo = serpent['diametro_tubo_mm'] / 1000
pitch_serp = serpent['pitch_mm'] / 1000
z_start = serpent['altura_inicio_mm'] / 1000

print(f"\n[SERPENTIN]")
print(f"  Numero de espiras: {n_espiras}")
print(f"  Diametro helice: {D_serpent*1000:.0f} mm")
print(f"  Diametro tubo: {d_tubo*1000:.0f} mm")
print(f"  Pitch: {pitch_serp*1000:.0f} mm")

# Generar coordenadas del serpentín
theta_serp = np.linspace(0, 2*np.pi*n_espiras, 500)
r_serp = D_serpent/2
x_serp = r_serp * np.cos(theta_serp)
y_serp = r_serp * np.sin(theta_serp)
z_serp = z_start + (theta_serp / (2*np.pi)) * pitch_serp

print(f"  Puntos generados: {len(theta_serp)}")
print(f"  Altura total: {(z_serp[-1] - z_serp[0])*1000:.0f} mm")

# Guardar coordenadas
np.savez('geometria_reactor_20L.npz',
         ribbon_x=x_ribbon, ribbon_y=y_ribbon, ribbon_z=z_ribbon,
         serpentin_x=x_serp, serpentin_y=y_serp, serpentin_z=z_serp,
         R_tank=R_tank, H_liquid=H_liquid)

print(f"\nArchivo generado: geometria_reactor_20L.npz")
print(f"  (Para importar en CAD o visualizar en Python)")
print(f"\nNOTA: Para generar archivo STEP, usar libreria como pythonOCC o FreeCAD")
print("="*80)
