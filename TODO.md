# TODO - Sistema de Modelado de Esterificación

## Estado del Proyecto

**Última actualización:** 2025-11-19
**Estado general:** 🟡 En desarrollo

---

## Fase 1: Configuración Inicial ✅

- [x] Investigación de plataformas opensource
- [x] Definición de arquitectura del sistema
- [x] Creación de estructura del proyecto
- [ ] Generación de documento LaTeX académico
- [ ] Configuración de archivos base

---

## Fase 2: Procesamiento de Datos 🔄

### 2.1 Módulo GC-FID (`src/data_processing/gc_processor.py`)
- [ ] Implementar lectura de datos crudos de cromatografía
- [ ] Calcular áreas corregidas con estándar interno
- [ ] Aplicar factores de respuesta para cuantificación
- [ ] Calcular composición de FAMEs (%)
- [ ] Calcular conversión de triglicéridos
- [ ] Exportar datos procesados a formato estándar
- [ ] Validar con datos de ejemplo

### 2.2 Módulo de Carga de Datos (`src/data_processing/data_loader.py`)
- [ ] Cargar variables desde JSON
- [ ] Validar integridad de datos
- [ ] Cargar datos de literatura
- [ ] Crear estructura de datos unificada

---

## Fase 3: Modelos Cinéticos 🔄

### 3.1 Módulo de Propiedades (`src/models/properties.py`)
- [ ] Implementar base de datos de propiedades termodinámicas
- [ ] Calcular densidades como función de T
- [ ] Calcular viscosidades como función de T
- [ ] Calcular capacidades caloríficas
- [ ] Implementar correlaciones de transporte

### 3.2 Módulo de Cinética (`src/models/kinetic_model.py`)
- [ ] Implementar clase base `KineticModel`
- [ ] Implementar modelo de 1 paso (pseudo-homogéneo 2º orden)
- [ ] Implementar modelo de 3 pasos (mecanístico)
- [ ] Implementar ecuaciones de Arrhenius
- [ ] Implementar modelo Eley-Rideal (opcional avanzado)
- [ ] Integración numérica con `solve_ivp`
- [ ] Validar con datos de literatura

### 3.3 Módulo de Ajuste de Parámetros (`src/models/parameter_fitting.py`)
- [ ] Implementar función objetivo (residuales)
- [ ] Configurar optimizador con `lmfit`
- [ ] Estimar parámetros cinéticos (Ea, A)
- [ ] Calcular intervalos de confianza
- [ ] Análisis de correlación de parámetros
- [ ] Exportar parámetros ajustados

---

## Fase 4: Optimización 🔄

### 4.1 Módulo de Optimización (`src/optimization/optimizer.py`)
- [ ] Implementar optimización de temperatura
- [ ] Implementar optimización de rpm (agitación)
- [ ] Implementar optimización de concentración de catalizador
- [ ] Configurar algoritmos: Nelder-Mead, SLSQP, Differential Evolution
- [ ] Implementar optimización multiobjetivo (opcional)
- [ ] Generar superficies de respuesta (RSM)

### 4.2 Análisis de Sensibilidad (`src/optimization/sensitivity.py`)
- [ ] Calcular Jacobiano numérico
- [ ] Generar tornado plots
- [ ] Análisis de sensibilidad local
- [ ] Análisis de sensibilidad global (Sobol indices)

---

## Fase 5: Integración con ASPEN HYSYS 🔄

### 5.1 Módulo HYSYS Connector (`src/aspen_integration/hysys_connector.py`)
- [ ] Implementar conexión COM con HYSYS
- [ ] Cargar/crear archivo .hsc base
- [ ] Configurar componentes (triglicéridos, metanol, FAME, glicerol)
- [ ] Configurar paquete termodinámico (UNIFAC/NRTL)
- [ ] Configurar reactor CSTR con cinética custom
- [ ] Ejecutar simulación
- [ ] Extraer resultados (conversión, composición, temperatura)
- [ ] Manejo de errores y excepciones

### 5.2 Módulo de Sincronización (`src/aspen_integration/data_sync.py`)
- [ ] Crear clase `DataSync` para gestionar datos de entrada
- [ ] Sincronizar datos entre modelos standalone y HYSYS
- [ ] Validar consistencia de unidades
- [ ] Mapear variables JSON → HYSYS paths

---

## Fase 6: Comparación y Validación 🔄

### 6.1 Módulo de Comparación (`src/utils/comparison.py`)
- [ ] Calcular métricas de error (RMSE, MAE, R²)
- [ ] Generar tablas comparativas
- [ ] Análisis estadístico de diferencias
- [ ] Generar parity plots
- [ ] Exportar reporte de validación

---

## Fase 7: Visualización y Exportación 🔄

### 7.1 Módulo de Visualización (`src/visualization/plotter.py`)
- [ ] Gráfica: Conversión vs Tiempo (standalone vs HYSYS)
- [ ] Gráfica: Perfiles de concentración (TG, DG, MG, FAME, Glicerol)
- [ ] Gráfica: Superficie de respuesta 3D (Temp vs Cat% vs Conversión)
- [ ] Gráfica: Tornado plot (análisis sensibilidad)
- [ ] Gráfica: Parity plot (standalone vs HYSYS)
- [ ] Gráfica: Residuales del ajuste
- [ ] Configurar estilo de gráficas (publicación)

### 7.2 Módulo de Exportación (`src/visualization/exporter.py`)
- [ ] Exportar a Excel (múltiples pestañas)
- [ ] Exportar a JSON (parámetros y resultados)
- [ ] Exportar figuras en alta resolución (PNG, SVG, PDF)
- [ ] Generar reporte automático en PDF

---

## Fase 8: Especificaciones CFD 🔄

### 8.1 Documento de Especificaciones (`docs/reactor_cfd_specs.md`)
- [ ] Especificar geometría del reactor 20L
- [ ] Diseño del agitador/impulsor
- [ ] Especificaciones de baffles
- [ ] Condiciones de frontera
- [ ] Parámetros de malla
- [ ] Modelos de turbulencia recomendados
- [ ] Integración de cinética en Fluent UDF

### 8.2 Módulo PyFluent (Futuro - Opcional)
- [ ] Instalar y configurar PyFluent
- [ ] Generar geometría programáticamente
- [ ] Configurar mallado
- [ ] Importar cinética como UDF
- [ ] Ejecutar simulación CFD
- [ ] Extraer campos de velocidad y temperatura

---

## Fase 9: Documentación 🔄

### 9.1 Documento LaTeX (`docs/documento_latex.tex`)
- [ ] Escribir introducción y marco teórico
- [ ] Documentar modelos cinéticos
- [ ] Documentar metodología de optimización
- [ ] Documentar integración con HYSYS
- [ ] Incluir resultados y validación
- [ ] Incluir especificaciones CFD
- [ ] Generar bibliografía
- [ ] Compilar con pdflatex

### 9.2 Manual de Usuario (`docs/manual_usuario.md`)
- [ ] Guía de instalación
- [ ] Guía de uso de cada módulo
- [ ] Ejemplos de uso
- [ ] Troubleshooting

---

## Fase 10: Testing y Validación 🔄

### 10.1 Tests Unitarios (`tests/`)
- [ ] Tests para `gc_processor.py`
- [ ] Tests para `kinetic_model.py`
- [ ] Tests para `optimizer.py`
- [ ] Tests para `hysys_connector.py`
- [ ] Tests para `comparison.py`

### 10.2 Tests de Integración
- [ ] Test del pipeline completo
- [ ] Validación con los 5 datasets experimentales
- [ ] Verificación de reproducibilidad

---

## Fase 11: Scripts Principales 🔄

### 11.1 Script Principal (`main.py`)
- [ ] Implementar CLI con argparse
- [ ] Modo: procesamiento de datos GC
- [ ] Modo: ajuste de parámetros
- [ ] Modo: optimización de variables
- [ ] Modo: simulación HYSYS
- [ ] Modo: comparación y validación
- [ ] Modo: generación de reportes

### 11.2 Scripts de Ejemplo (`examples/`)
- [ ] Ejemplo 1: Procesamiento de datos GC
- [ ] Ejemplo 2: Ajuste de parámetros cinéticos
- [ ] Ejemplo 3: Optimización de condiciones
- [ ] Ejemplo 4: Comparación con HYSYS
- [ ] Ejemplo 5: Análisis completo

---

## Prioridades

### 🔴 Alta Prioridad (Esta Semana)
1. Completar documento LaTeX académico
2. Módulo de procesamiento GC-FID
3. Módulo de modelo cinético básico
4. Módulo de integración con HYSYS

### 🟡 Media Prioridad (Próximas 2 Semanas)
1. Módulo de optimización
2. Módulo de visualización
3. Sistema de sincronización y comparación
4. Tests unitarios

### 🟢 Baja Prioridad (Futuro)
1. Integración con PyFluent
2. Optimización multiobjetivo avanzada
3. Interface gráfica (GUI)

---

## Notas Importantes

- **ASPEN HYSYS**: El usuario tiene HYSYS (no Plus), usar COM con 'HYSYS.Application'
- **Reactor**: 20L para scaled-up, necesita especificaciones CFD completas
- **Datos**: 5 datasets experimentales disponibles en JSON
- **Ejecutable**: Todo debe correr desde VS Code como scripts .py
- **Documentación**: LaTeX compilable con pdflatex para soporte académico

---

## Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest tests/ -v --cov=src

# Ejecutar script principal (cuando esté listo)
python main.py --mode process_gc --input data/raw/experiment_01.csv

# Compilar documento LaTeX
cd docs && pdflatex documento_latex.tex && bibtex documento_latex && pdflatex documento_latex.tex && pdflatex documento_latex.tex
```

---

**Última revisión:** 2025-11-19
**Autor:** Sistema de Modelado de Esterificación
**Versión:** 1.0
