# Practica 2: Perfiles de Temperatura en Transesterificacion

## Objetivo

Comprender el efecto de la temperatura en la cinetica de transesterificacion mediante el estudio de perfiles de conversion a temperatura constante. Aprender a aplicar la ecuacion de Arrhenius y analizar la dependencia de la constante de velocidad con la temperatura.

## Duracion Estimada

2-3 horas

## Conceptos Clave

- Ecuacion de Arrhenius: k = A * exp(-Ea / RT)
- Energia de activacion (Ea)
- Factor pre-exponencial (A)
- Constante de velocidad (k)
- Perfiles de conversion temporal
- Control termico en reactores

## Modelo Cinetico

Esta practica utiliza un modelo cinetico simplificado de pseudo-primer orden:

```
dX/dt = k(T) * (1 - X) * f(exceso_MeOH)
```

Donde:
- X: conversion de trigliceridos (0 a 1)
- k(T): constante de velocidad dependiente de temperatura (Arrhenius)
- f(exceso_MeOH): factor de exceso de metanol normalizado

La constante de velocidad sigue la ecuacion de Arrhenius:

```
k(T) = A * exp(-Ea / RT)
```

Donde:
- A: factor pre-exponencial (1.5 x 10^6 L/mol/min)
- Ea: energia de activacion (65 kJ/mol)
- R: constante de gases (8.314 x 10^-3 kJ/mol/K)
- T: temperatura absoluta (K)

## Metodologia: OBSERVAR

En esta practica, el codigo ya esta completo. Tu tarea es:

1. **Ejecutar el script** y observar las graficas generadas
2. **Analizar los resultados** comparando los 4 escenarios de temperatura
3. **Responder preguntas** de investigacion en `analisis.md`
4. **Modificar temperaturas** en `config.json` para explorar otros casos
5. **Volver a ejecutar** y comparar resultados

## Instrucciones

### Paso 1: Ejecutar el script

Abre una terminal en este directorio y ejecuta:

```bash
python main.py
```

El script generara automaticamente:
- 4 graficas interactivas (se mostraran en ventanas)
- 4 archivos PNG en la carpeta `resultados/`
- Resumen en consola con tabla de resultados

### Paso 2: Revisar las graficas

Las graficas generadas son:

1. **Grafica 1**: Perfiles individuales de conversion (4 subplots)
2. **Grafica 2**: Comparacion de todas las temperaturas en una sola grafica
3. **Grafica 3**: Constantes de velocidad vs temperatura (Arrhenius)
4. **Grafica 4**: Tiempo requerido para alcanzar 90% de conversion

### Paso 3: Responder preguntas de investigacion

Abre el archivo `analisis.md` y responde las preguntas usando las graficas y la tabla de resultados.

### Paso 4: Experimentar con otros escenarios

Modifica el archivo `config.json` para explorar:

- Diferentes temperaturas (prueba 45°C, 70°C)
- Diferentes relaciones molares (prueba 3:1, 9:1)
- Diferentes tiempos de simulacion (prueba 60 min, 180 min)

Vuelve a ejecutar `python main.py` y compara los nuevos resultados.

## Preguntas de Investigacion

Responde estas preguntas en el archivo `analisis.md`:

### Pregunta 1: Efecto de la Temperatura

Observa la Grafica 2. ¿Como cambia la conversion final cuando aumentas la temperatura de 50°C a 65°C?
¿Es un cambio lineal o exponencial?

### Pregunta 2: Constante de Velocidad

Segun la Grafica 3, ¿cuanto aumenta la constante de velocidad (k) cuando la temperatura pasa de 50°C a 65°C?
¿Que implica esto en terminos practicos para el tiempo de reaccion?

### Pregunta 3: Tiempo de Reaccion

Observa la Grafica 4. ¿Cuanto tiempo se necesita para alcanzar 90% de conversion a 50°C vs 65°C?
¿Vale la pena el consumo energetico adicional para operar a mayor temperatura?

### Pregunta 4: Limitaciones Operacionales

El metanol hierve a 64.7°C a presion atmosferica. Si quisieras operar a 70°C para acelerar la reaccion,
¿que modificaciones necesitarias hacer al reactor? ¿Que riesgos implica?

### Pregunta 5: Optimizacion Termica

Si tu objetivo es alcanzar 95% de conversion en el menor tiempo posible pero minimizando el costo energetico,
¿que temperatura elegiras entre los 4 escenarios? Justifica tu respuesta considerando:
- Tiempo de reaccion
- Consumo energetico
- Seguridad operacional

### Pregunta 6: Arrhenius

Usando los valores de la Grafica 3, calcula manualmente la constante de velocidad k para 57.5°C (punto medio entre 55°C y 60°C).
Compara tu resultado con lo que predice la ecuacion de Arrhenius. ¿Son similares?

Ayuda: k = 1.5e6 * exp(-65000 / (8.314 * T_K))

## Escenarios Predefinidos

El archivo `config.json` incluye 4 escenarios para comparar:

| Escenario | Temperatura | Comentario |
|-----------|-------------|------------|
| A | 50°C | Temperatura baja - Cinetica lenta |
| B | 55°C | Temperatura media-baja - Balance |
| C | 60°C | Temperatura optima comun |
| D | 65°C | Temperatura alta - Cerca del punto de ebullicion del MeOH |

Todos los escenarios usan:
- Relacion molar MeOH:TG = 6:1
- Tiempo de simulacion = 120 min

## Archivos de la Practica

```
practica2_perfiles_temperatura/
├── main.py              # Script completo (NO modificar)
├── config.json          # Parametros configurables (MODIFICAR AQUI)
├── README.md            # Esta guia
├── analisis.md          # Plantilla para tus respuestas
└── resultados/          # Carpeta con graficas generadas
    ├── grafica1_perfiles_individuales.png
    ├── grafica2_comparacion_temperaturas.png
    ├── grafica3_constantes_velocidad.png
    └── grafica4_tiempo_90_conversion.png
```

## Fuentes de Datos

Todos los parametros tienen fuentes documentadas:

- **Parametros cineticos**: Estimados a partir de Kouzu et al. (2008)
- **Ecuacion de Arrhenius**: Principios de cinetica quimica
- **Punto de ebullicion MeOH**: Perry's Chemical Engineers' Handbook, 9th Ed.

## Notas Importantes

- Este script es totalmente funcional. No necesitas escribir codigo.
- Toda la personalizacion se hace en `config.json`
- Las graficas se guardan automaticamente en `resultados/`
- Puedes ejecutar el script las veces que necesites
- Los calculos usan scipy.integrate.odeint para resolver EDOs

## Conceptos Avanzados (Opcional)

Si quieres profundizar, investiga:

1. **Ley de Van't Hoff**: Relacion entre temperatura y equilibrio
2. **Diagramas de Arrhenius**: Grafica de ln(k) vs 1/T (linealiza la ecuacion)
3. **Q10 factor**: Cuanto cambia la velocidad al aumentar 10°C

## Siguiente Practica

En la Practica 3 aprenderemos a procesar datos experimentales usando Pandas, importar archivos CSV y realizar analisis estadistico de series temporales.
