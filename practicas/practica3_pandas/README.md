# Práctica 3: Lectura y Procesamiento de Datos con Pandas

## Teoría

**Pandas** es la librería más usada para análisis de datos en Python.

### Conceptos Clave
- **DataFrame**: Tabla de datos (como Excel)
- **Columnas**: Variables (tiempo, área_pico, compuesto)
- **Filas**: Observaciones individuales
- **Operaciones**: filtrar, agrupar, calcular

### Cromatografía GC-FID
- Gas Chromatography con detector FID
- Área del pico ∝ concentración del compuesto
- Necesitamos estándar interno para cuantificar

## Objetivos

- ✓ Leer archivos CSV con pandas
- ✓ Filtrar datos por compuesto
- ✓ Calcular concentraciones desde áreas
- ✓ Exportar resultados a Excel

## Requisitos

```bash
pip install pandas openpyxl
```

## Ejercicio

Trabajarás con datos de cromatografía simulados en `datos/cromatografia_raw.csv`.

**Estructura del CSV:**
```
tiempo_min,compuesto,area_pico,tiempo_retencion_min
0,TG,15234,8.2
0,MeOH,89234,2.1
0,FAME,0,5.4
...
```

## Verificación

- DataFrame cargado con ~40 filas
- Concentraciones calculadas correctamente
- Excel generado con múltiples hojas
- Conversión final ≈ 85%

## Desafío Extra

1. Agregar columna con conversión acumulada
2. Detectar outliers en áreas de pico
3. Generar gráfica de composición vs tiempo (stacked area chart)
