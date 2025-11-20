#!/usr/bin/env python3
"""Práctica 3: Pandas - SOLUCIÓN"""

import pandas as pd

print("="*70)
print("PRÁCTICA 3: Procesamiento de Datos con Pandas")
print("="*70)

# Leer CSV
df = pd.read_csv('datos/cromatografia_raw.csv')
print(f"\n✓ Datos cargados: {len(df)} filas, {len(df.columns)} columnas\n")
print(df.head(10))

# Factores de respuesta (área/concentración) - Fuente: Calibración experimental típica
factores_respuesta = {
    'TG': 1.2,
    'MeOH': 0.8,
    'FAME': 1.0,
    'GL': 0.9
}

C_TG_inicial = 0.5  # mol/L (del experimento)

# Calcular concentraciones relativas
area_estandar = df[df['compuesto'] == 'Estandar']['area_pico'].iloc[0]

# Procesar cada compuesto
resultados = []
for tiempo in df['tiempo_min'].unique():
    df_tiempo = df[df['tiempo_min'] == tiempo]

    fila_resultado = {'tiempo_min': tiempo}

    for compuesto in ['TG', 'MeOH', 'FAME', 'GL']:
        area = df_tiempo[df_tiempo['compuesto'] == compuesto]['area_pico'].values[0]
        # Concentración relativa normalizada por estándar
        area_rel = area / area_estandar
        C_rel = area_rel / factores_respuesta[compuesto]
        fila_resultado[f'{compuesto}_area'] = area
        fila_resultado[f'{compuesto}_Crel'] = C_rel

    resultados.append(fila_resultado)

df_procesado = pd.DataFrame(resultados)

# Calcular conversión
C_TG_rel_inicial = df_procesado['TG_Crel'].iloc[0]
df_procesado['conversion_%'] = ((C_TG_rel_inicial - df_procesado['TG_Crel']) / C_TG_rel_inicial) * 100

print("\n" + "="*70)
print("📊 DATOS PROCESADOS")
print("="*70)
print(df_procesado[['tiempo_min', 'TG_Crel', 'FAME_Crel', 'conversion_%']])

# Estadísticas
print("\n" + "="*70)
print("📈 ESTADÍSTICAS")
print("="*70)
print(df_procesado[['TG_Crel', 'FAME_Crel', 'conversion_%']].describe())

# Exportar a Excel
with pd.ExcelWriter('resultados_procesados.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Datos Crudos', index=False)
    df_procesado.to_excel(writer, sheet_name='Procesados', index=False)

print("\n✅ Excel generado: resultados_procesados.xlsx")
print(f"✅ Conversión final: {df_procesado['conversion_%'].iloc[-1]:.2f}%")
print("\n" + "="*70)
