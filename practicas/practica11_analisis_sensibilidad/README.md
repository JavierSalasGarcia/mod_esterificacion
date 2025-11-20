# Practica 11: Analisis de Sensibilidad

## Objetivo

Identificar los parametros operacionales mas criticos mediante analisis de sensibilidad. Generar superficies de respuesta y diagramas de Pareto para optimizar condiciones de operacion.

## Duracion Estimada

3-4 horas

## Conceptos Clave

- Analisis de sensibilidad univariado
- Superficies de respuesta 3D
- Diseño de experimentos (DOE)
- Diagrama de Pareto (regla 80/20)
- Parametros criticos vs no criticos

## 4 Parametros Analizados

1. **Temperatura** (50-80°C)
2. **Agitacion** (300-800 rpm)
3. **Catalizador** (0.5-2.0 wt%)
4. **Relacion Molar** (3:1 a 12:1)

## Metodologia

1. Analisis univariado (variar un parametro manteniendo otros constantes)
2. Superficies de respuesta (variar dos parametros simultaneamente)
3. Calculo de sensibilidades (ΔX / Δparam)
4. Diagrama de Pareto (ordenar por importancia)

## Instrucciones

```bash
python main.py
```

## Graficas Generadas

1. **Grafica 1**: Sensibilidad individual (4 subplots)
2. **Grafica 2**: Superficie 3D (T vs Relacion Molar)
3. **Grafica 3**: Diagrama de Pareto

## Preguntas

Ver `analisis.md`:
1. ¿Cual es el parametro mas critico?
2. Interpreta la superficie 3D
3. Aplica regla 80/20
4. Propone condiciones optimas

## Siguiente Practica

Practica 12: Personalizacion de modelos (1 paso vs 3 pasos, NaOH vs CaO vs enzimatico).
