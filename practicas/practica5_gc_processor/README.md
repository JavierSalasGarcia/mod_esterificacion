# Practica 5: Procesamiento de Datos de Cromatografia de Gases (GC-FID)

## Objetivo

Aprender a procesar datos de cromatografia de gases usando el metodo de estandar interno, calcular factores de respuesta y correlacionar perfiles de agitacion con la conversion de la reaccion.

## Duracion Estimada

2-3 horas

## Conceptos Clave

- Cromatografia de gases con detector FID
- Metodo de estandar interno
- Factores de respuesta (FR)
- Conversion de areas a concentraciones
- Perfiles de agitacion (constante, lineal, escalonado)
- Interpolacion de datos

## Metodologia del Estandar Interno

### Formula:

```
C_analito = (Area_analito / Area_IS) * C_IS * FR
```

Donde:
- C_analito: concentracion del analito (mol/L)
- Area_analito: area del pico del analito (unidades arbitrarias)
- Area_IS: area del pico del estandar interno (constante)
- C_IS: concentracion conocida del estandar interno
- FR: factor de respuesta relativo

### Ventajas del Estandar Interno:

1. Compensa variaciones en volumen de inyeccion
2. Corrige fluctuaciones del detector
3. Mejora precision y reproducibilidad

## Metodologia: EXPERIMENTAR

1. Ejecutar script base
2. Modificar factores de respuesta en config.json
3. Cambiar perfiles de agitacion (constante, lineal, escalonado)
4. Observar como afectan las concentraciones calculadas
5. Responder preguntas en analisis.md

## Instrucciones

### Paso 1: Ejecutar script base

```bash
python main.py
```

### Paso 2: Experimentar con Factores de Respuesta

Modifica en config.json:

```json
"FR_FAME": 1.10  // Cambia de 0.95 a 1.10
```

Ejecuta de nuevo y compara concentraciones calculadas.

### Paso 3: Experimentar con Perfiles de Agitacion

Cambia el tipo de perfil:

```json
"tipo": "lineal"  // Cambia de "constante" a "lineal"
```

Opciones:
- **constante**: rpm fijo durante toda la reaccion
- **lineal**: rpm aumenta linealmente de rpm_inicial a rpm_final
- **escalonado**: rpm cambia en escalones definidos

## Graficas Generadas

1. **Grafica 1**: Areas de picos de GC vs tiempo
2. **Grafica 2**: Concentraciones calculadas vs tiempo
3. **Grafica 3**: Conversion y perfil de agitacion (eje Y dual)

## Archivos

```
practica5_gc_processor/
├── main.py
├── config.json          # MODIFICAR para experimentar
├── README.md
├── analisis.md
├── datos/
│   └── gc_areas.csv     # Datos de entrada
└── resultados/
    ├── grafica1_areas_gc.png
    ├── grafica2_concentraciones.png
    ├── grafica3_conversion_agitacion.png
    └── datos_procesados.csv
```

## Preguntas de Investigacion

Ver `analisis.md`:
1. Efecto de factores de respuesta en concentraciones
2. Correlacion entre agitacion y conversion
3. Deteccion de puntos anomalos en GC
4. Comparacion de perfiles de agitacion

## Siguiente Practica

Practica 6: Ajuste de parametros cineticos con regresion no lineal usando lmfit.
