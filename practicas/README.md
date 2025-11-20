# Prácticas Progresivas: De Python Básico a CFD

## Descripción

Este conjunto de **9 prácticas progresivas** está diseñado para que un estudiante de química **sin conocimientos previos de programación** pueda dominar el sistema completo de modelado de esterificación, desde cálculos básicos hasta simulaciones CFD con Ansys Fluent.

## Estructura del Curso

### Nivel Principiante (Prácticas 1-3)
Fundamentos de Python y procesamiento de datos

### Nivel Intermedio (Prácticas 4-6)
Modelos cinéticos y uso del sistema

### Nivel Avanzado (Prácticas 7-9)
Optimización, integración y CFD

---

## Prácticas Disponibles

### Práctica 1: Fundamentos de Python y Cálculos Químicos Básicos
**Duración estimada:** 2-3 horas
**Nivel:** Principiante
**Requisitos previos:** Ninguno

**Aprenderás:**
- Variables, tipos de datos y funciones
- Cálculos estequiométricos
- Conversión y rendimiento
- Cargar configuración desde JSON

**Archivos:**
- `README.md`: Teoría completa e instrucciones
- `config.json`: Parámetros configurables
- `ejercicio.py`: Código con TODOs para completar
- `solucion.py`: Código completo de referencia

---

### Práctica 2: Listas, Ciclos y Visualización de Datos
**Duración estimada:** 2-3 horas
**Nivel:** Principiante
**Requisitos previos:** Práctica 1

**Aprenderás:**
- Trabajar con listas de datos experimentales
- Ciclos `for` para procesar series
- Crear gráficas con matplotlib
- Guardar figuras en alta resolución

**Nuevas librerías:** `matplotlib`, `numpy`

---

### Práctica 3: Lectura y Procesamiento de Datos con Pandas
**Duración estimada:** 3-4 horas
**Nivel:** Principiante-Intermedio
**Requisitos previos:** Práctica 2

**Aprenderás:**
- Leer archivos CSV con pandas
- Manipular DataFrames
- Filtrar y agrupar datos
- Exportar resultados a Excel

**Nuevas librerías:** `pandas`, `openpyxl`

---

### Práctica 4: Modelos Cinéticos Simples (Ecuación de Arrhenius)
**Duración estimada:** 3-4 horas
**Nivel:** Intermedio
**Requisitos previos:** Práctica 3

**Aprenderás:**
- Implementar ecuación de Arrhenius
- Resolver EDOs con `scipy.integrate.odeint`
- Simular perfiles de concentración
- Comparar efecto de temperatura

**Nuevas librerías:** `scipy`
**Conceptos clave:** Cinética química, EDOs, parámetros de Arrhenius

---

### Práctica 5: Procesamiento de Datos GC-FID con el Sistema
**Duración estimada:** 4-5 horas
**Nivel:** Intermedio
**Requisitos previos:** Práctica 4

**Aprenderás:**
- Importar módulos del sistema (`from src.data_processing import GCProcessor`)
- Procesar datos reales de cromatografía
- Usar la interfaz CLI del sistema
- Configurar perfiles de agitación arbitrarios (n puntos)

**Nuevos conceptos:** Importación de módulos propios, CLI, perfiles de agitación

---

### Práctica 6: Ajuste de Parámetros Cinéticos
**Duración estimada:** 4-5 horas
**Nivel:** Intermedio-Avanzado
**Requisitos previos:** Práctica 5

**Aprenderás:**
- Usar `src.models.parameter_fitting`
- Ajustar energía de activación (Ea) y factor pre-exponencial (A)
- Interpretar métricas de bondad de ajuste (R², RMSE)
- Trabajar con múltiples experimentos

**Nuevas librerías:** `lmfit`
**Conceptos clave:** Regresión no lineal, optimización numérica

---

### Práctica 7: Optimización de Condiciones de Reacción
**Duración estimada:** 4-5 horas
**Nivel:** Avanzado
**Requisitos previos:** Práctica 6

**Aprenderás:**
- Usar `src.optimization.optimizer`
- Optimizar temperatura, RPM y % catalizador
- Generar superficies de respuesta 3D
- Analizar sensibilidad de variables
- Optimizar perfil de agitación (factores relativos)

**Nuevas librerías:** `plotly` (gráficas 3D)
**Conceptos clave:** Optimización multiobjetivo, diseño experimental

---

### Práctica 8: Workflow Completo - Proyecto Integrador
**Duración estimada:** 6-8 horas
**Nivel:** Avanzado
**Requisitos previos:** Práctica 7

**Aprenderás:**
- Ejecutar flujo completo: procesar → ajustar → optimizar → reportar
- Integrar todos los módulos del sistema
- Generar reportes profesionales (Excel, PDF, gráficas)
- Comparar modelos cinéticos (1-paso vs 3-pasos)
- Configurar experimentos con perfiles de agitación variables

**Entregable:** Proyecto final completo documentado

---

### Práctica 9: Up-Scaling y Preparación para CFD (Reactor 20L)
**Duración estimada:** 8-10 horas
**Nivel:** Avanzado
**Requisitos previos:** Práctica 8

**Aprenderás:**
- Escalar desde reactor batch (350 mL) a piloto (20 L)
- Cálculos dimensionales (Re, P/V, tiempo de mezclado)
- Diseñar geometría: reactor + ribbon impeller + serpentín
- Preparar archivos para Ansys Fluent
- Crear UDF (User Defined Function) con cinética
- Comparar modelo 0D vs CFD 3D

**Componentes diseñados:**
- **Reactor:** 20 L, cilíndrico
- **Impeller:** Ribbon (hélice helicoidal tipo mezclador de pintura)
- **Serpentín:** 10 espiras configurables (control de temperatura)
- **Sin baffles:** El serpentín rompe el vórtice

**Software requerido:**
- Python 3.8+ (obligatorio)
- Ansys Fluent Student (opcional, gratis)
- OpenFOAM (alternativa gratuita)

**Archivos generados:**
- Cálculos de escalado (Excel)
- Geometría 3D (coordenadas NPZ, STEP)
- UDF para Fluent (código C)
- Comparación 0D vs CFD (gráficas y reportes)

---

## Características Especiales

### Perfiles de Agitación Configurables
Desde la Práctica 5, todos los experimentos soportan perfiles de agitación arbitrarios vía JSON:

```json
{
  "perfil_agitacion": {
    "tipo": "lineal",
    "puntos": [
      {"tiempo_min": 0, "rpm": 300},
      {"tiempo_min": 30, "rpm": 500},
      {"tiempo_min": 60, "rpm": 600},
      {"tiempo_min": 90, "rpm": 500},
      {"tiempo_min": 120, "rpm": 400}
    ]
  }
}
```

**Tipos disponibles:**
- `"lineal"`: Interpolación lineal entre puntos
- `"escalonado"`: Cambios abruptos (step function)
- `"constante"`: Un solo valor durante todo el experimento

### Parámetros Documentados
Todos los valores numéricos incluyen sus fuentes:
- PubChem Database (masas molares)
- Perry's Chemical Engineers' Handbook (propiedades físicas)
- Kouzu et al., Fuel 2008 (parámetros cinéticos)
- Datos experimentales propios (cuando aplica)

### Sin Emojis
Todos los archivos están libres de emojis para garantizar compatibilidad multiplataforma.

---

## Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd mod_esterificacion
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## Uso

### Ejecutar una práctica

```bash
cd practicas/practica1_python_basico
python ejercicio.py
```

### Verificar solución

```bash
python solucion.py
```

### Configurar parámetros

Edita `config.json` en cada práctica (NO toques el código Python).

---

## Progresión Recomendada

1. **Semana 1-2:** Prácticas 1-3 (Fundamentos Python)
2. **Semana 3-4:** Prácticas 4-6 (Modelos cinéticos)
3. **Semana 5-6:** Prácticas 7-8 (Optimización y proyecto)
4. **Semana 7-8:** Práctica 9 (Up-scaling y CFD)

**Total:** ~30-40 horas de aprendizaje efectivo

---

## Estructura de Cada Práctica

```
practicaX_nombre/
├── README.md              # Teoría, objetivos, verificación
├── config.json            # Parámetros configurables
├── ejercicio.py           # Código con TODOs
├── solucion.py            # Código completo
├── datos/                 # Datos de ejemplo (si aplica)
└── resultados_esperados/  # Salidas de referencia
```

---

## Soporte y Recursos

### Documentación del Sistema
- `docs/tutorial_uso_sistema.tex`: Tutorial completo LaTeX
- `docs/reactor_cfd_specs.md`: Especificaciones CFD detalladas
- `plantillas/`: Scripts de ejemplo para el sistema completo

### Recursos Python
- Python oficial: https://docs.python.org/es/3/tutorial/
- Matplotlib: https://matplotlib.org/stable/tutorials/
- Pandas: https://pandas.pydata.org/docs/user_guide/
- SciPy: https://docs.scipy.org/doc/scipy/tutorial/

### Recursos de Ingeniería Química
- Perry's Handbook (propiedades físicas)
- Levenspiel (ingeniería de reactores)
- Kouzu et al. 2008 (cinética de biodiésel)

---

## Solución de Problemas

### Error: "ModuleNotFoundError"
**Solución:** Asegúrate de tener el entorno virtual activado e instaladas las dependencias.

```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError: config.json"
**Solución:** Asegúrate de estar en el directorio correcto de la práctica.

```bash
cd practicas/practicaX_nombre/
```

### Resultados diferentes a los esperados
**Solución:** Verifica que los valores en `config.json` sean exactos (sin redondeo).

---

## Licencia

MIT License - Ver archivo LICENSE en la raíz del repositorio.

---

## Contribuciones

Si encuentras errores o tienes sugerencias:
1. Abre un issue en GitHub
2. Describe el problema con detalles
3. Incluye capturas de pantalla si es relevante

---

**¡Felicidades por embarcarte en este viaje de aprendizaje desde Python básico hasta simulaciones CFD!**

El dominio de estas herramientas te permitirá modelar, optimizar y escalar procesos químicos de manera profesional.
