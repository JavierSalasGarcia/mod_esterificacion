# Practica 3: Procesamiento de Datos con Pandas

## Objetivo

Aprender a importar, manipular y analizar datos experimentales usando la biblioteca Pandas. Comprender como realizar calculos estadisticos, procesar series temporales y generar graficas de datos reales de una reaccion de transesterificacion.

## Duracion Estimada

2-3 horas

## Conceptos Clave

- Pandas DataFrames y Series
- Importacion de archivos CSV
- Estadisticas descriptivas (media, std, min, max, quartiles)
- Derivadas numericas (diferencias finitas)
- Promedios moviles y deteccion de tendencias
- Graficas de series temporales
- Boxplots y distribucion de datos
- Exportacion de resultados procesados

## Estructura de los Datos

El archivo `datos/datos_experimentales.csv` contiene datos de una reaccion de transesterificacion realizada a 60°C con relacion molar MeOH:TG de 6:1.

### Columnas del CSV:

| Columna | Descripcion | Unidades |
|---------|-------------|----------|
| `tiempo_min` | Tiempo de reaccion | min |
| `temperatura_C` | Temperatura del reactor | °C |
| `conversion_pct` | Conversion de trigliceridos | % |
| `conc_TG_mol_L` | Concentracion de trigliceridos | mol/L |
| `conc_MeOH_mol_L` | Concentracion de metanol | mol/L |
| `conc_FAME_mol_L` | Concentracion de biodiesel (FAME) | mol/L |
| `conc_GL_mol_L` | Concentracion de glicerol | mol/L |

### Frecuencia de Muestreo:

Los datos fueron tomados cada 5 minutos durante 120 minutos de reaccion.

## Metodologia: OBSERVAR

En esta practica, el codigo ya esta completo. Tu tarea es:

1. **Ejecutar el script** y observar las graficas generadas
2. **Analizar los resultados** estadisticos en consola
3. **Revisar los archivos exportados** (CSV con datos procesados)
4. **Responder preguntas** de investigacion en `analisis.md`
5. **Experimentar con otros archivos de datos** (opcional)

## Instrucciones

### Paso 1: Explorar los datos

Antes de ejecutar el script, abre el archivo CSV con un editor de texto o Excel para familiarizarte con la estructura.

### Paso 2: Ejecutar el script

Abre una terminal en este directorio y ejecuta:

```bash
python main.py
```

El script:
- Cargara el CSV usando `pandas.read_csv()`
- Calculara estadisticas descriptivas con `df.describe()`
- Calculara velocidades instantaneas usando derivadas numericas
- Detectara el estado estacionario de la reaccion
- Generara 5 graficas automaticamente
- Exportara resultados procesados

### Paso 3: Revisar los resultados

El script genera:

1. **5 graficas PNG** en la carpeta `resultados/`
2. **estadisticas_descriptivas.csv** con media, std, min, max, quartiles
3. **datos_procesados.csv** con columnas adicionales (velocidades calculadas)

### Paso 4: Responder preguntas de investigacion

Abre el archivo `analisis.md` y responde las preguntas usando las graficas y los archivos generados.

## Graficas Generadas

### Grafica 1: Evolucion Temporal de Concentraciones

Muestra como cambian las concentraciones de TG, MeOH, FAME y GL a lo largo del tiempo.

**Observa:**
- TG y MeOH disminuyen (se consumen)
- FAME y GL aumentan (se forman)
- La relacion estequiometrica: 1 TG → 3 FAME + 1 GL

### Grafica 2: Conversion y Temperatura (Eje Y Dual)

Muestra la conversion y el control de temperatura en el mismo grafico con dos ejes Y.

**Observa:**
- La temperatura se mantiene constante (60°C)
- La conversion aumenta y eventualmente se estabiliza

### Grafica 3: Velocidades Instantaneas

Muestra las velocidades de conversion y formacion de FAME calculadas con derivadas numericas.

**Observa:**
- La velocidad es maxima al inicio
- La velocidad disminuye con el tiempo (reaccion se desacelera)
- Algunas oscilaciones son normales debido al ruido experimental

### Grafica 4: Distribucion Estadistica (Boxplot)

Muestra la distribucion de concentraciones de cada especie a lo largo de todo el experimento.

**Observa:**
- TG tiene concentracion alta al inicio, baja al final (rango amplio)
- FAME tiene concentracion baja al inicio, alta al final (rango amplio)
- La mediana (linea roja) representa el valor central

### Grafica 5: Deteccion de Estado Estacionario

Muestra cuando la reaccion alcanza un estado estacionario (conversion casi constante).

**Observa:**
- La linea vertical roja marca el tiempo de estado estacionario
- Despues de ese punto, la conversion ya no aumenta significativamente

## Operaciones de Pandas Utilizadas

El script utiliza las siguientes operaciones de Pandas:

```python
# 1. Cargar CSV
df = pd.read_csv('datos_experimentales.csv')

# 2. Estadisticas descriptivas
stats = df[columnas].describe()

# 3. Derivadas numericas (diferencias finitas)
dy = df['conversion_pct'].diff()
dt = df['tiempo_min'].diff()
velocidad = dy / dt

# 4. Promedio movil
df['conversion_pct'].rolling(window=5).std()

# 5. Seleccion condicional
estacionarios = std_movil < umbral

# 6. Exportar a CSV
df.to_csv('datos_procesados.csv', index=False)
```

## Preguntas de Investigacion

Responde estas preguntas en el archivo `analisis.md`:

### Pregunta 1: Analisis de Concentraciones

Segun la Grafica 1, ¿en que momento las concentraciones de TG y FAME se cruzan (tienen el mismo valor)?
¿Que implica esto en terminos de la conversion?

### Pregunta 2: Velocidades de Reaccion

Observa la Grafica 3. ¿Por que la velocidad de conversion es maxima al inicio y disminuye con el tiempo?
Relacionalo con las concentraciones de reactivos.

### Pregunta 3: Estado Estacionario

Segun la Grafica 5, ¿en que tiempo se alcanza el estado estacionario?
¿Vale la pena continuar la reaccion despues de ese punto?

### Pregunta 4: Control de Temperatura

Observa la Grafica 2. ¿La temperatura se mantiene constante durante todo el experimento?
Si hay pequeñas variaciones, ¿cual es el rango de variacion y crees que es aceptable?

### Pregunta 5: Analisis Estadistico

Abre el archivo `resultados/estadisticas_descriptivas.csv`. Compara la media y la desviacion estandar de `conc_TG_mol_L` y `conc_FAME_mol_L`. ¿Cual tiene mayor variabilidad? ¿Por que?

### Pregunta 6: Boxplot

Observa la Grafica 4 (boxplot). ¿Cual especie tiene el rango intercuartil (IQR) mas amplio?
¿Que significa esto en terminos de la dinamica de la reaccion?

## Archivos de la Practica

```
practica3_pandas/
├── main.py                  # Script completo (NO modificar)
├── config.json              # Configuracion (puede modificarse)
├── README.md                # Esta guia
├── analisis.md              # Plantilla para tus respuestas
├── datos/
│   └── datos_experimentales.csv  # Datos de entrada
└── resultados/              # Carpeta con resultados generados
    ├── grafica1_evolucion_concentraciones.png
    ├── grafica2_conversion_temperatura.png
    ├── grafica3_velocidades_reaccion.png
    ├── grafica4_distribucion_boxplot.png
    ├── grafica5_estado_estacionario.png
    ├── estadisticas_descriptivas.csv
    └── datos_procesados.csv
```

## Fuentes de Datos

- **Datos experimentales**: Simulados a partir de modelo cinetico validado con Kouzu et al. (2008)
- **Metodo de procesamiento**: Basado en tecnicas estandar de analisis de series temporales
- **Biblioteca Pandas**: https://pandas.pydata.org/

## Notas Importantes

- Este script es totalmente funcional. No necesitas escribir codigo.
- Los datos son simulados pero representan comportamiento realista
- Las velocidades se calculan con diferencias finitas (aproximacion numerica)
- El estado estacionario se detecta cuando la desviacion estandar movil es menor a 1.0%

## Conceptos Avanzados (Opcional)

Si quieres profundizar, investiga:

1. **Interpolacion de datos**: Como estimar valores intermedios
2. **Filtros de suavizado**: Savitzky-Golay, promedios moviles ponderados
3. **Analisis de residuos**: Comparar datos experimentales con modelos
4. **Test de estacionariedad**: Augmented Dickey-Fuller test

## Siguiente Practica

En la Practica 4 aprenderemos a integrar ecuaciones diferenciales ordinarias (EDOs) usando scipy.integrate.odeint y profundizaremos en la ecuacion de Arrhenius para modelar la cinetica de transesterificacion.
