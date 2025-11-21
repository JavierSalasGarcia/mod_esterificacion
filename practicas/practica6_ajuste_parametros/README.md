# Practica 6: Ajuste de Parametros Cineticos

## Objetivo

Aprender a ajustar parametros cineticos (A, Ea) a partir de datos experimentales usando regresion no lineal con lmfit. Calcular intervalos de confianza y evaluar calidad del ajuste.

## Duracion Estimada

3 horas

## Conceptos Clave

- Regresion no lineal
- Metodo de minimos cuadrados
- Biblioteca lmfit
- Intervalos de confianza
- Matriz de covarianza
- R², RMSE

## Metodologia: EXPERIMENTAR

1. Ejecutar script con datos experimentales
2. Observar parametros ajustados (A, Ea)
3. Modificar valores iniciales en config.json
4. Comparar resultados de ajuste
5. Responder preguntas sobre convergencia

## Instrucciones

```bash
python main.py
```

## Datos de Entrada

Archivo CSV con:
- Tiempo (min)
- Temperatura (°C)
- Conversion experimental (%)

## Graficas Generadas

1. **Grafica 1**: Ajuste de datos experimentales vs modelo
2. **Grafica 2**: Residuos del ajuste
3. **Grafica 3**: Superficie de error (A vs Ea)
4. **Grafica 4**: Intervalos de confianza de parametros

## Archivos

```
practica6_ajuste_parametros/
├── main.py
├── config.json          # MODIFICAR valores iniciales para experimentar
├── README.md
├── analisis.md
├── datos/
│   └── datos_exp_ajuste.csv
└── resultados/
    ├── graficas...
    └── parametros_ajustados.json
```

## Preguntas

Ver `analisis.md`:
1. ¿Los parametros ajustados son similares a los iniciales?
2. ¿El ajuste converge con diferentes valores iniciales?
3. Interpretar intervalos de confianza
4. Analizar residuos

## Siguiente Practica

Practica 7: Optimizacion de condiciones operacionales usando algoritmos globales.
