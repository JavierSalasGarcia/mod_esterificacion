#!/usr/bin/env python3
"""Práctica 4 - EJERCICIO"""

import json
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

with open('config.json') as f:
    config = json.load(f)

params = config['parametros_cineticos']

# TODO 1: Implementa la ecuación de Arrhenius
def arrhenius(T_celsius):
    T_K = T_celsius + 273.15
    A = params['A_forward']
    Ea = params['Ea_forward_kJ_mol'] * 1000
    R = params['R_J_mol_K']
    # k = ... (completa la ecuación)
    k = None
    return k

# TODO 2: Define la EDO
def edo_primer_orden(C, t, k):
    # return ... (dC/dt = -k*C)
    return None

# TODO 3: Resuelve la EDO con odeint
t = np.linspace(0, 120, 100)
C0 = 0.5
k_65C = arrhenius(65)
# C = odeint(...)

# TODO 4: Grafica el resultado
# plt.plot(...)

print("✅ Completa los TODOs!")
