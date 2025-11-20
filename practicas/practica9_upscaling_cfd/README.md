# Práctica 9: Up-Scaling y Preparación para CFD (Reactor 20L)

## 📖 Teoría

### Escalado de Reactores
Escalamos desde **350 mL** (batch con mosca magnética) a **20 L** (reactor piloto).

**Criterios de escalado:**
- P/V constante (potencia por volumen)
- Re constante (número de Reynolds)
- Tiempo de mezclado constante (θ_m)

### Geometría Reactor 20L
- **Impulsor**: Ribbon (helicoidal, tipo mezclador de pintura)
- **Serpentín**: 10 espiras para control de temperatura
- **Sin baffles**: El serpentín rompe el vórtice

## 🎯 Objetivos

- ✅ Calcular escalado dimensional
- ✅ Diseñar geometría reactor + ribbon + serpentín
- ✅ Preparar archivos para Ansys Fluent
- ✅ Crear UDF con cinética ajustada
- ✅ Comparar modelo 0D vs CFD 3D

## 📦 Software

- **Python 3.8+**: Cálculos y geometría
- **Ansys Fluent Student** (opcional): Simulación CFD
- **OpenFOAM** (alternativa gratuita)

## 📋 Flujo de Trabajo

### Parte A: Escalado (Python)
1. Cálculos dimensionales (Re, P/V, θ_m)
2. Determinar RPM del ribbon impeller
3. Dimensiones del serpentín

### Parte B: Geometría (Python)
1. Coordenadas del reactor cilíndrico
2. Geometría del ribbon impeller
3. Geometría del serpentín (10 espiras)
4. Exportar a STEP/IGES

### Parte C: Ansys Fluent
1. Importar geometría
2. Configurar mallado
3. Modelos (turbulencia, energía, especies)
4. UDF con cinética
5. Ejecutar simulación

### Parte D: Post-procesamiento
1. Leer resultados CFD
2. Comparar con modelo 0D
3. Analizar distribución espacial

## ✅ Entregables

- `escalado_calculos.xlsx`: Cálculos de escalado
- `reactor_20L.step`: Geometría CAD
- `setup_fluent.cas`: Caso Ansys configurado
- `cinetica.c`: UDF para Fluent
- `comparacion_0D_vs_CFD.pdf`: Reporte final
