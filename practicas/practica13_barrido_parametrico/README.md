# Práctica 13: Estudio Paramétrico Automatizado mediante Barrido Sistemático

## Objetivos de Aprendizaje

1. Implementar barridos paramétricos automáticos para exploración sistemática del espacio de diseño
2. Comprender la explosión combinatoria en estudios multivariables
3. Organizar y almacenar resultados de múltiples simulaciones de forma estructurada
4. Generar superficies de respuesta y mapas de contorno a partir de barridos paramétricos
5. Aplicar técnicas de visualización avanzada para interpretar resultados multidimensionales

## Introducción

En las prácticas anteriores se ha trabajado con simulaciones individuales donde se especifica un único valor para cada parámetro operacional. Sin embargo, en el diseño y optimización de procesos químicos resulta fundamental explorar sistemáticamente cómo varía el desempeño del reactor cuando se modifican múltiples parámetros simultáneamente.

Un **barrido paramétrico** (también llamado estudio paramétrico o parameter sweep) consiste en ejecutar automáticamente múltiples simulaciones evaluando todas las combinaciones posibles de valores de un conjunto de parámetros de interés. Por ejemplo, si se desea estudiar el efecto de 4 temperaturas y 3 relaciones molares, el barrido generaría automáticamente 4 × 3 = 12 simulaciones diferentes.

Esta práctica implementa un módulo de barrido paramétrico que:
- Lee configuraciones con múltiples valores por parámetro
- Calcula automáticamente todas las combinaciones (producto cartesiano)
- Ejecuta las simulaciones en secuencia
- Organiza los resultados en carpetas con marca temporal (fecha y hora)
- Genera reportes consolidados y visualizaciones comparativas

## Marco Teórico

### Producto Cartesiano y Explosión Combinatoria

Cuando se especifican múltiples valores para $n$ parámetros diferentes, el número total de simulaciones requeridas es el producto del número de valores de cada parámetro:

$$N_{simulaciones} = n_1 \times n_2 \times \cdots \times n_n$$

Por ejemplo:
- Temperatura: 4 valores → $n_1 = 4$
- Relación molar: 3 valores → $n_2 = 3$
- Concentración catalizador: 2 valores → $n_3 = 2$
- Agitación: 1 valor → $n_4 = 1$

**Total**: $4 \times 3 \times 2 \times 1 = 24$ simulaciones

Este crecimiento multiplicativo se denomina **explosión combinatoria** y limita el número de parámetros y valores que pueden explorarse de forma exhaustiva. Un barrido con 5 parámetros y 10 valores cada uno requeriría 100,000 simulaciones.

### Superficies de Respuesta

Cuando se exploran 2 parámetros manteniendo los demás constantes, los resultados pueden visualizarse como una **superficie de respuesta** que muestra cómo varía la variable de interés (ej: conversión final) en función de los 2 parámetros explorados.

Para 3 o más parámetros variables, se utilizan técnicas como:
- **Gráficos de contorno** en 2D fijando los parámetros adicionales
- **Diagramas de burbujas** donde el color/tamaño representa variables adicionales
- **Matrices de gráficos** (pair plots) mostrando todas las combinaciones 2×2

## Estructura del Código

El módulo de barrido paramétrico se implementa en `src/parametric_sweep/sweep_runner.py` y contiene:

### Clase `ParametricSweep`

**Métodos principales:**
- `cargar_configuracion(archivo_json)`: Lee la configuración del barrido
- `generar_combinaciones()`: Calcula el producto cartesiano de todos los parámetros
- `estimar_tiempo_computo()`: Estima el tiempo total basado en una simulación de prueba
- `ejecutar_barrido()`: Ejecuta todas las simulaciones secuencialmente
- `guardar_resultados(carpeta_salida)`: Almacena los resultados organizados
- `generar_reporte_consolidado()`: Crea archivo CSV con todos los resultados
- `visualizar_superficies_respuesta()`: Genera gráficas 2D y 3D

### Formato de Configuración

El archivo `config_barrido.json` especifica múltiples valores por parámetro usando listas:

```json
{
  "temperatura_C": [50, 55, 60, 65],
  "relacion_molar": [6, 9, 12],
  "concentracion_catalizador_pct": [1.0, 1.5],
  "agitacion_rpm": [400],
  "tiempo_reaccion_min": 60,
  "volumen_reactor_mL": 350
}
```

**Notas:**
- Parámetros con **lista de valores**: se incluyen en el barrido
- Parámetros con **valor único**: se mantienen constantes en todas las simulaciones
- El sistema calcula automáticamente: 4 × 3 × 2 × 1 = **24 combinaciones**

### Organización de Resultados

Los resultados se almacenan en:
```
resultados/barrido_YYYY-MM-DD_HH-MM-SS/
├── configuracion_barrido.json          # Configuración usada
├── resumen_barrido.txt                 # Información del barrido
├── resultados_consolidados.csv         # Tabla con todas las simulaciones
├── estadisticas_resumen.csv            # Métricas agregadas
├── simulaciones/                       # Resultados individuales
│   ├── sim_001/
│   │   ├── parametros.json
│   │   ├── concentraciones.csv
│   │   └── grafica_conversion.png
│   ├── sim_002/
│   └── ...
└── visualizaciones/                    # Gráficas comparativas
    ├── superficie_T_vs_relMolar.png
    ├── contorno_T_vs_relMolar.png
    ├── matriz_correlacion.png
    └── resumen_comparativo.html        # Dashboard interactivo
```

### Advertencias de Seguridad

El sistema implementa advertencias automáticas:

```
⚠️  ADVERTENCIA: Barrido Paramétrico
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Parámetros variables:
  • temperatura_C: 4 valores [50, 55, 60, 65]
  • relacion_molar: 3 valores [6, 9, 12]
  • concentracion_catalizador_pct: 2 valores [1.0, 1.5]

Total de simulaciones: 24
Tiempo estimado: 4.8 minutos (0.2 min/simulación)
Espacio en disco requerido: ~85 MB

¿Continuar con el barrido? [s/N]:
```

## Tareas

### Parte 1: Configuración y Ejecución Básica (45 minutos)

1. **Examinar configuración de ejemplo**
   - Abrir `config_barrido_ejemplo.json`
   - Identificar cuáles parámetros se barren y cuáles son constantes
   - Calcular manualmente el número total de simulaciones

2. **Ejecutar barrido pequeño**
   - Modificar configuración para solo 2 temperaturas × 2 relaciones molares = 4 simulaciones
   - Ejecutar: `python main.py`
   - Observar la advertencia y aceptar
   - Esperar a que terminen las 4 simulaciones

3. **Explorar resultados generados**
   - Navegar a la carpeta de resultados con timestamp
   - Abrir `resumen_barrido.txt` y verificar información
   - Inspeccionar `resultados_consolidados.csv` en Excel/LibreOffice
   - Revisar las carpetas `simulaciones/sim_001/` hasta `sim_004/`

### Parte 2: Análisis de Superficies de Respuesta (60 minutos)

4. **Ejecutar barrido completo**
   - Usar configuración original: 4 temperaturas × 3 relaciones molares = 12 simulaciones
   - Parámetros constantes: catalizador 1.5%, agitación 400 rpm
   - Ejecutar barrido completo

5. **Generar superficie de respuesta**
   - Ejecutar script de visualización: `python generar_superficie.py`
   - Examinar `superficie_T_vs_relMolar.png`
   - Identificar la región óptima (máxima conversión)

6. **Crear mapa de contorno**
   - Generar gráfico de contorno con isolíneas de conversión
   - Identificar combinaciones que logran >95% conversión
   - Documentar en `analisis.md`

### Parte 3: Estudio de Sensibilidad Multivariable (75 minutos)

7. **Diseñar barrido de sensibilidad**
   - Configurar barrido con 4 parámetros variables:
     - Temperatura: [50, 55, 60, 65] °C
     - Relación molar: [6, 9, 12]
     - Catalizador: [0.5, 1.0, 1.5, 2.0] %
     - Agitación: [300, 400, 500] rpm
   - Calcular total de simulaciones: 4×3×4×3 = 144
   - **ADVERTENCIA**: Esto tomará ~30 minutos

8. **Ejecutar y monitorear**
   - Iniciar barrido extenso
   - Monitorear progreso en consola
   - Si es demasiado largo, reducir a 3×2×2×2 = 24 simulaciones

9. **Análisis de correlación**
   - Generar matriz de correlación entre parámetros y conversión
   - Identificar cuál parámetro tiene mayor influencia (mayor correlación)
   - Crear ranking de importancia de parámetros

10. **Identificar interacciones**
    - Examinar si el efecto de temperatura depende de la relación molar
    - Buscar sinergias (efectos no aditivos)
    - Documentar hallazgos

### Parte 4: Aplicación a Diseño de Procesos (60 minutos)

11. **Definir restricciones de diseño**
    - Conversión mínima requerida: 95%
    - Tiempo máximo de proceso: 60 min
    - Restricción económica: minimizar relación molar (menor consumo de metanol)

12. **Filtrar resultados**
    - Usar `resultados_consolidados.csv`
    - Filtrar simulaciones que cumplen conversión ≥95%
    - Entre las viables, identificar la de menor relación molar
    - Reportar condiciones óptimas

13. **Validar resultado óptimo**
    - Ejecutar simulación individual con condiciones óptimas identificadas
    - Verificar que efectivamente alcanza la conversión esperada
    - Comparar con resultados de optimización numérica (Práctica 7)

14. **Dashboard interactivo**
    - Abrir `visualizaciones/resumen_comparativo.html` en navegador
    - Explorar interactivamente las superficies de respuesta
    - Usar controles deslizantes para fijar parámetros y observar efectos

## Preguntas de Análisis

1. **Explosión combinatoria**: Si se quisieran explorar 6 parámetros con 5 valores cada uno, ¿cuántas simulaciones se requerirían? ¿Es esto práctico?

2. **Estrategias de reducción**: Proponer 2 estrategias para reducir el número de simulaciones manteniendo buena cobertura del espacio paramétrico (investigar: diseños factoriales fraccionados, Latin Hypercube Sampling)

3. **Interpretación física**: ¿Por qué la conversión aumenta con temperatura pero eventualmente se estabiliza? ¿Qué fenómeno físico-químico limita la conversión máxima?

4. **Efecto de interacción**: ¿El efecto de aumentar la relación molar es el mismo a 50°C que a 65°C? Si no, explicar por qué existe esta interacción

5. **Optimización vs Barrido**: Comparar las condiciones óptimas encontradas mediante barrido paramétrico con las de optimización numérica (Práctica 7). ¿Son similares? ¿Cuál método es más preciso? ¿Más costoso computacionalmente?

6. **Aplicabilidad industrial**: ¿En qué etapa del desarrollo de un proceso (laboratorio, piloto, industrial) es más útil un barrido paramétrico exhaustivo vs optimización numérica?

## Entregables

1. Archivo `analisis.md` completado con respuestas y hallazgos
2. Carpeta de resultados `barrido_YYYY-MM-DD_HH-MM-SS/` con:
   - Resultados consolidados
   - Superficies de respuesta generadas
   - Dashboard HTML interactivo
3. Tabla resumen identificando las 3 mejores configuraciones según criterios de diseño
4. Reflexión personal (200-300 palabras) sobre ventajas/limitaciones de barridos paramétricos

## Recursos Adicionales

- Documentación de `itertools.product()`: Generación de productos cartesianos en Python
- Tutorial de `matplotlib` para superficies 3D
- Artículo: "Design of Experiments for Chemical Engineers" (Montgomery, 2017)
- Video: "Response Surface Methodology" (StatQuest)

## Tiempo Estimado

- Parte 1 (Básico): 45 minutos
- Parte 2 (Superficies): 60 minutos
- Parte 3 (Multivariable): 75 minutos
- Parte 4 (Diseño): 60 minutos
- **Total**: 4 horas

## Notas del Instructor

- Supervisar que los estudiantes no lancen barridos demasiado grandes (>500 simulaciones) sin autorización
- Verificar espacio en disco disponible antes de barridos extensos
- Sugerir trabajar en parejas para discutir interpretación de superficies de respuesta
- Preparar datos pre-computados para barridos muy grandes si hay limitaciones de tiempo
