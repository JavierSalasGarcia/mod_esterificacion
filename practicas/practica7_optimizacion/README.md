# Practica 7: Optimizacion de Condiciones Operacionales

## Objetivo

Aprender a optimizar condiciones operacionales (T, rpm, relacion molar, catalizador) usando algoritmos de optimizacion global. Diseñar experimentos para maximizar conversion mientras se minimizan costos.

## Duracion Estimada

3-4 horas

## Conceptos Clave

- Optimizacion global (vs local)
- Funcion objetivo multi-criterio
- Restricciones operacionales
- Algoritmos: scipy.optimize.differential_evolution
- Superficie de respuesta
- Scoring automatico

## Metodologia: DISEÑAR

1. Ejecutar script con funcion objetivo predefinida
2. Observar condiciones optimas propuestas
3. Modificar pesos de la funcion objetivo en config.json
4. Proponer tus propias condiciones
5. Sistema de scoring evalua tu propuesta

## Funcion Objetivo

```
Score = w1*Conversion - w2*Costo_T - w3*Costo_MeOH - w4*Costo_Cat
```

Donde:
- w1, w2, w3, w4 son pesos configurables
- Costos normalizados respecto a condiciones base

## Instrucciones

```bash
python main.py
```

El script:
1. Busca condiciones optimas automaticamente
2. Muestra scoring de la solucion
3. Permite proponer condiciones alternativas
4. Genera superficies de respuesta 3D

## Graficas Generadas

1. **Grafica 1**: Superficies de respuesta 3D (T vs relacion molar)
2. **Grafica 2**: Contornos de conversion
3. **Grafica 3**: Scoring multi-criterio
4. **Grafica 4**: Sensibilidad de la funcion objetivo a pesos

## Archivos

```
practica7_optimizacion/
├── main.py              # Script con optimizador
├── config.json          # MODIFICAR pesos y restricciones
├── README.md
├── analisis.md
└── resultados/
    ├── condiciones_optimas.json
    └── graficas...
```

## Preguntas

Ver `analisis.md`:
1. ¿Cuales son las condiciones optimas encontradas?
2. ¿Como cambian al modificar pesos?
3. Proponer condiciones alternativas y justificar
4. Analizar trade-offs conversion vs costo

## Siguiente Practica

Practica 8: Workflow completo integrando GC processing, fitting, optimization y reporte HTML.
