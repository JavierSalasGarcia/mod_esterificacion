#!/usr/bin/env python3
"""Práctica 3 - EJERCICIO: Completa los TODOs"""

import pandas as pd

print("="*70)
print("PRÁCTICA 3: Pandas")
print("="*70)

# TODO 1: Lee el archivo CSV
df = None  # <-- pd.read_csv('datos/cromatografia_raw.csv')

print(f"\nFilas: {len(df)}")

# TODO 2: Filtra solo datos de TG
df_TG = None  # <-- df[df['compuesto'] == 'TG']

print("\nDatos de TG:")
# TODO 3: Muestra df_TG

# TODO 4: Calcula el área promedio de TG
area_promedio_TG = None  # <-- df_TG['area_pico'].mean()

print(f"\nÁrea promedio TG: {area_promedio_TG:.2f}")

# TODO 5: Exporta a Excel
# df.to_excel('mi_resultado.xlsx', index=False)

print("\n✓ Completa los TODOs!")
