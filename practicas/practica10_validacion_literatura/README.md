# Practica 10: Validacion con Datos de Literatura

## Objetivo

Validar nuestro modelo cinetico comparandolo con datos experimentales publicados en literatura cientifica. Aprender a evaluar la calidad del ajuste usando metricas estadisticas (R², RMSE, MAPE).

## Duracion Estimada

2-3 horas

## Conceptos Clave

- Validacion de modelos cineticos
- Coeficiente de determinacion (R²)
- Raiz del error cuadratico medio (RMSE)
- Error porcentual absoluto medio (MAPE)
- Digitalizacion de datos de graficas publicadas
- Comparacion de parametros cineticos

## Referencia Principal

**Kouzu, M., Kasuno, T., Tajika, M., Sugimoto, Y., Yamanaka, S., & Hidaka, J. (2008).**
*Calcium oxide as a solid base catalyst for transesterification of soybean oil and its application to biodiesel production.*
**Fuel, 87(12), 2798-2806.**
DOI: 10.1016/j.fuel.2007.10.019

## Metricas Estadisticas

### R² (Coeficiente de Determinacion):
```
R² = 1 - (SS_res / SS_tot)
```
- R² = 1: Ajuste perfecto
- R² > 0.95: Excelente ajuste
- R² > 0.90: Buen ajuste
- R² < 0.90: Ajuste pobre

### RMSE (Root Mean Square Error):
```
RMSE = sqrt(mean((y_exp - y_pred)²))
```
- Medida del error absoluto promedio
- Unidades: % de conversion
- RMSE < 3%: Muy buen ajuste
- RMSE < 5%: Ajuste aceptable

### MAPE (Mean Absolute Percentage Error):
```
MAPE = mean(|y_exp - y_pred| / y_exp) * 100
```
- Medida del error relativo promedio
- MAPE < 5%: Muy buen ajuste
- MAPE < 10%: Ajuste aceptable

## Metodologia: AVANZADAS

1. Ejecutar script y observar validacion
2. Analizar graficas de comparacion
3. Interpretar metricas estadisticas
4. Comparar parametros cineticos (A, Ea)
5. Responder preguntas sobre calidad del ajuste

## Instrucciones

### Paso 1: Ejecutar script

```bash
python main.py
```

El script:
- Carga datos experimentales de Kouzu et al. (2008)
- Simula con nuestro modelo a las mismas condiciones
- Calcula R², RMSE, MAPE para cada temperatura
- Compara parametros cineticos

### Paso 2: Revisar resultados en consola

Observa la tabla de estadisticas:
- ¿R² es mayor a 0.95?
- ¿RMSE es menor a 5%?
- ¿Los parametros A y Ea son similares?

### Paso 3: Analizar graficas

**Grafica 1:** Comparacion punto a punto (4 subplots para 60, 65, 70, 75°C)
- Puntos: datos experimentales Kouzu
- Linea: nuestro modelo
- R² y RMSE en el titulo

**Grafica 2:** Comparacion de parametros cineticos
- Barras lado a lado
- Kouzu vs Nuestro modelo

## Preguntas de Investigacion

Ver `analisis.md`:

1. ¿El modelo esta validado? Justificar con R² y RMSE
2. ¿Por que hay diferencias entre parametros?
3. ¿En que temperatura el ajuste es mejor?
4. Proponer mejoras al modelo

## Archivos

```
practica10_validacion_literatura/
├── main.py              # Script completo
├── config.json          # Datos de Kouzu y parametros
├── README.md            # Esta guia
├── analisis.md          # Plantilla para respuestas
└── resultados/
    ├── grafica1_validacion_kouzu.png
    └── grafica2_comparacion_parametros.png
```

## Datos de Kouzu et al. 2008

Los datos fueron digitalizados de la Figura 3 de la publicacion:
- Temperaturas: 60, 65, 70, 75°C
- Catalizador: CaO (1 wt%)
- Relacion molar MeOH:TG = 6:1
- Aceite: Soja
- Tiempo: 0-120 min

## Siguiente Practica

Practica 11: Analisis de sensibilidad de 4 parametros operacionales (T, agitacion, catalizador, relacion molar).
