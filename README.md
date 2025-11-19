# Sistema Integrado de Modelado de Esterificación para Producción de Biodiésel

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema completo de modelado cinético para la producción de biodiésel mediante transesterificación catalizada por CaO, con integración de modelos standalone (Python) y simulación comercial (ASPEN HYSYS).

## 🎯 Características Principales

- **Modelos Cinéticos Flexibles**: Implementación de modelos de 1 paso (simplificado) y 3 pasos (mecanístico)
- **Procesamiento Automatizado de GC-FID**: Cuantificación de FAMEs y cálculo de conversión
- **Optimización de Variables**: Temperatura, agitación y concentración de catalizador
- **Integración con ASPEN HYSYS**: Sincronización y validación cruzada mediante COM API
- **Análisis Comparativo**: Métricas estadísticas (RMSE, MAE, R²) entre modelos
- **Visualización Avanzada**: Gráficas publication-ready y reportes automatizados
- **Especificaciones CFD**: Diseño completo para reactor de 20L con Ansys Fluent

## 📁 Estructura del Proyecto

```
mod_esterificacion/
├── src/                          # Código fuente
│   ├── models/                   # Modelos cinéticos
│   │   ├── kinetic_model.py      # Modelos 1 y 3 pasos
│   │   ├── properties.py         # Propiedades termodinámicas
│   │   └── parameter_fitting.py  # Ajuste de parámetros
│   ├── data_processing/          # Procesamiento de datos
│   │   ├── gc_processor.py       # Procesador GC-FID
│   │   └── data_loader.py        # Cargador de datos
│   ├── optimization/             # Optimización
│   │   ├── optimizer.py          # Optimizador multivariable
│   │   └── sensitivity.py        # Análisis de sensibilidad
│   ├── aspen_integration/        # Integración HYSYS
│   │   ├── hysys_connector.py    # Conector COM
│   │   └── data_sync.py          # Sincronización de datos
│   ├── visualization/            # Visualización
│   │   ├── plotter.py            # Generador de gráficas
│   │   └── exporter.py           # Exportador de resultados
│   └── utils/                    # Utilidades
│       └── comparison.py         # Comparación de modelos
├── data/                         # Datos
│   ├── raw/                      # Datos crudos GC
│   ├── processed/                # Datos procesados
│   └── literature/               # Datos de literatura
├── results/                      # Resultados
│   ├── figures/                  # Gráficas generadas
│   ├── reports/                  # Reportes PDF/Excel
│   └── exports/                  # Exportaciones JSON
├── docs/                         # Documentación
│   ├── documento_latex.tex       # Documento académico
│   ├── reactor_cfd_specs.md      # Especificaciones CFD
│   └── manual_usuario.md         # Manual de usuario
├── tests/                        # Tests unitarios
├── config/                       # Archivos de configuración
├── main.py                       # Script principal
├── requirements.txt              # Dependencias
├── TODO.md                       # Lista de tareas
└── variables_esterificacion_dataset.json  # Datos experimentales
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- ASPEN HYSYS (para módulo de integración, solo Windows)
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Clonar el repositorio
git clone <repository-url>
cd mod_esterificacion

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 📚 Uso

### 1. Procesamiento de Datos GC-FID

```bash
python main.py --mode process_gc --input data/raw/experiment_01.csv --output data/processed/
```

### 2. Ajuste de Parámetros Cinéticos

```bash
python main.py --mode fit_params --input variables_esterificacion_dataset.json --output results/
```

### 3. Optimización de Condiciones Operacionales

```bash
python main.py --mode optimize --input data/processed/fitted_params.json --output results/
```

### 4. Simulación en ASPEN HYSYS

```bash
python main.py --mode simulate_hysys --input data/processed/input_data.json --output results/
```

### 5. Comparación de Modelos

```bash
python main.py --mode compare --input results/ --output results/comparison/
```

## 🔬 Ejemplos

Ver carpeta `examples/` para notebooks y scripts de ejemplo:

- `example_01_gc_processing.py`: Procesamiento de cromatogramas
- `example_02_parameter_fitting.py`: Ajuste de parámetros cinéticos
- `example_03_optimization.py`: Optimización de variables
- `example_04_hysys_integration.py`: Integración con HYSYS
- `example_05_complete_workflow.py`: Flujo completo de análisis

## 📊 Modelos Implementados

### Modelo de 1 Paso (Pseudo-homogéneo de 2º Orden)

```
TG + 3 MeOH ⇌ 3 FAME + Glicerol
r = -k(T) · C_TG · C_MeOH
k(T) = A · exp(-Ea / RT)
```

### Modelo de 3 Pasos (Mecanístico)

```
TG + MeOH ⇌ DG + FAME
DG + MeOH ⇌ MG + FAME
MG + MeOH ⇌ GL + FAME
```

## 🧪 Variables Optimizables

- **Temperatura**: 50-80°C
- **Agitación**: 200-800 rpm
- **Catalizador CaO**: 1-5% masa

## 📈 Resultados

El sistema genera automáticamente:

1. **Gráficas**:
   - Conversión vs Tiempo (experimental vs modelos)
   - Perfiles de concentración de especies
   - Superficies de respuesta 3D
   - Parity plots (Standalone vs HYSYS)
   - Análisis de sensibilidad (Tornado plots)

2. **Reportes**:
   - Excel con múltiples pestañas
   - JSON con parámetros ajustados
   - PDF con análisis completo

3. **Métricas de Validación**:
   - RMSE, MAE, R² entre modelos
   - Intervalos de confianza de parámetros
   - Análisis de residuales

## 🖥️ Integración con ASPEN HYSYS

El sistema se conecta con HYSYS vía COM automation (pywin32):

```python
from src.aspen_integration import HYSYSConnector

connector = HYSYSConnector(case_file="biodiesel_reactor.hsc")
connector.set_reactor_params(T=65, V=20, catalyst_mass=3.5)
connector.run_simulation()
results = connector.get_results()
```

## 🌊 Simulación CFD (Reactor 20L)

Especificaciones completas en `docs/reactor_cfd_specs.md`:

- Geometría del reactor y agitador (Rushton Turbine)
- Condiciones de frontera
- Modelos de turbulencia (k-ε RNG)
- Integración de cinética (UDF en C)
- Parámetros de mallado

## 📖 Documentación Académica

Documento LaTeX completo con fundamentación teórica:

```bash
cd docs
pdflatex documento_latex.tex
bibtex documento_latex
pdflatex documento_latex.tex
pdflatex documento_latex.tex
```

## 🧪 Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con coverage
pytest tests/ --cov=src --cov-report=html
```

## 🛠️ Dependencias Principales

- **numpy**, **scipy**, **pandas**: Cálculos científicos
- **lmfit**: Ajuste de parámetros
- **matplotlib**, **plotly**, **seaborn**: Visualización
- **pywin32**: Integración con ASPEN HYSYS
- **openpyxl**, **xlsxwriter**: Exportación a Excel
- **pytest**: Testing

## 📝 TODO

Ver `TODO.md` para lista detallada de tareas y progreso del desarrollo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Autores

- Sistema de Modelado de Esterificación - Versión 1.0

## 📧 Contacto

Para preguntas, sugerencias o reportar bugs, por favor abre un Issue en el repositorio.

## 🙏 Agradecimientos

- Comunidad de Python científico
- Desarrolladores de ASPEN HYSYS COM API
- Investigadores en cinética de biodiésel

---

**Última actualización:** 2025-11-19