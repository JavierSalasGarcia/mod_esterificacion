# Práctica 1: Fundamentos de Python y Cálculos Químicos Básicos

## 📖 Teoría

### ¿Qué es Python?
Python es un lenguaje de programación de alto nivel, fácil de leer y escribir. Es ampliamente usado en ciencia e ingeniería para análisis de datos, simulaciones y automatización.

### Conceptos Químicos
En la producción de biodiésel por transesterificación, la reacción simplificada es:

```
Triglicérido (TG) + 3 Metanol (MeOH) → 3 FAME (biodiésel) + Glicerol (GL)
```

**Conceptos clave:**
- **Conversión (%)**: Fracción de reactivo que ha reaccionado
- **Masa molar**: Masa de un mol de sustancia (g/mol)
- **Densidad**: Masa por unidad de volumen (g/mL o kg/L)
- **Concentración molar**: Moles de soluto por litro de solución (mol/L)

### Conceptos Python que Aprenderás
1. **Variables**: Contenedores para almacenar datos
2. **Tipos de datos**: `int`, `float`, `str`, `bool`
3. **Operadores**: `+`, `-`, `*`, `/`, `**` (potencia)
4. **Funciones**: Bloques de código reutilizables
5. **Comentarios**: Documentación con `#`
6. **Print**: Mostrar resultados en pantalla

## 🎯 Objetivos de Aprendizaje

Al completar esta práctica podrás:
- ✅ Instalar Python y crear un entorno virtual
- ✅ Usar variables para almacenar datos químicos
- ✅ Realizar cálculos estequiométricos
- ✅ Calcular conversión y rendimiento
- ✅ Definir funciones simples
- ✅ Mostrar resultados formateados

## 📦 Instalación/Requisitos

### Verificar instalación de Python

```bash
python --version  # Debe mostrar Python 3.8 o superior
```

Si no tienes Python instalado:
- **Windows**: Descargar de https://www.python.org/downloads/
- **Mac**: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip`

### Crear entorno virtual (recomendado)

```bash
cd mod_esterificacion/practicas/practica1_python_basico
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Instalar dependencias (ninguna por ahora)
Esta práctica solo usa Python estándar, sin librerías externas.

## 💡 Conceptos Clave

| Término | Definición | Ejemplo |
|---------|------------|---------|
| **Variable** | Contenedor con nombre para un valor | `temperatura = 65` |
| **Tipo int** | Número entero sin decimales | `rpm = 400` |
| **Tipo float** | Número con decimales | `masa = 15.5` |
| **Tipo str** | Texto entre comillas | `compuesto = "Metanol"` |
| **Función** | Bloque de código reutilizable | `def calcular_masa():` |
| **Return** | Devuelve un valor desde función | `return resultado` |

## 👨‍💻 Ejercicio Guiado

### Archivo: `config.json`

Este archivo contiene los parámetros configurables de la práctica:

```json
{
  "masas_molares": {
    "_comentario": "Fuente: PubChem Database (https://pubchem.ncbi.nlm.nih.gov/)",
    "TG_tripalmitin": 807.3,
    "MeOH": 32.04,
    "FAME_metil_palmitato": 270.5,
    "GL_glicerol": 92.09
  },
  "densidades_25C": {
    "_comentario": "Fuente: Perry's Chemical Engineers' Handbook, 9th Ed.",
    "TG_tripalmitin_kg_L": 0.875,
    "MeOH_kg_L": 0.792,
    "FAME_metil_palmitato_kg_L": 0.865,
    "GL_glicerol_kg_L": 1.261
  },
  "experimento": {
    "_comentario": "Datos de ejemplo típicos para biodiésel",
    "volumen_reactor_mL": 350,
    "masa_TG_inicial_g": 50.0,
    "volumen_MeOH_mL": 25.0,
    "masa_FAME_final_g": 42.3,
    "temperatura_C": 65,
    "tiempo_reaccion_min": 120
  }
}
```

### Archivo: `ejercicio.py`

Abre este archivo y completa los TODOs:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 1: Fundamentos de Python y Cálculos Químicos Básicos
===============================================================

Aprenderás a:
- Cargar datos desde JSON
- Realizar cálculos estequiométricos
- Calcular conversión y rendimiento
- Usar funciones
"""

import json

# ==============================================================================
# PASO 1: Cargar configuración desde JSON
# ==============================================================================
print("="*70)
print("PRÁCTICA 1: Cálculos Químicos Básicos con Python")
print("="*70)

# TODO 1: Cargar el archivo config.json
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extraer datos
masas_molares = config['masas_molares']
densidades = config['densidades_25C']
experimento = config['experimento']

print("\n✓ Datos cargados exitosamente desde config.json\n")

# ==============================================================================
# PASO 2: Definir funciones para cálculos
# ==============================================================================

def calcular_moles(masa_g, masa_molar):
    """
    Calcula moles a partir de masa y masa molar.

    Fórmula: n = m / M

    Args:
        masa_g (float): Masa en gramos
        masa_molar (float): Masa molar en g/mol

    Returns:
        float: Número de moles
    """
    # TODO 2: Implementa el cálculo de moles
    moles = masa_g / masa_molar
    return moles


def calcular_concentracion_molar(moles, volumen_L):
    """
    Calcula concentración molar (mol/L).

    Fórmula: C = n / V

    Args:
        moles (float): Número de moles
        volumen_L (float): Volumen en litros

    Returns:
        float: Concentración en mol/L
    """
    # TODO 3: Implementa el cálculo de concentración
    concentracion = moles / volumen_L
    return concentracion


def calcular_conversion(moles_inicial, moles_final):
    """
    Calcula conversión porcentual.

    Fórmula: X = ((n0 - n) / n0) * 100

    Args:
        moles_inicial (float): Moles iniciales del reactivo
        moles_final (float): Moles finales del reactivo

    Returns:
        float: Conversión en %
    """
    # TODO 4: Implementa el cálculo de conversión
    conversion_porcentaje = ((moles_inicial - moles_final) / moles_inicial) * 100
    return conversion_porcentaje


def calcular_rendimiento(moles_producto_real, moles_producto_teorico):
    """
    Calcula rendimiento porcentual.

    Fórmula: Y = (real / teórico) * 100

    Args:
        moles_producto_real (float): Moles obtenidos experimentalmente
        moles_producto_teorico (float): Moles teóricos máximos

    Returns:
        float: Rendimiento en %
    """
    # TODO 5: Implementa el cálculo de rendimiento
    rendimiento_porcentaje = (moles_producto_real / moles_producto_teorico) * 100
    return rendimiento_porcentaje


# ==============================================================================
# PASO 3: Realizar cálculos con datos del experimento
# ==============================================================================

print("📊 DATOS DEL EXPERIMENTO")
print("-" * 70)
print(f"Volumen del reactor: {experimento['volumen_reactor_mL']} mL")
print(f"Masa inicial de TG: {experimento['masa_TG_inicial_g']} g")
print(f"Volumen de MeOH: {experimento['volumen_MeOH_mL']} mL")
print(f"Masa final de FAME: {experimento['masa_FAME_final_g']} g")
print(f"Temperatura: {experimento['temperatura_C']} °C")
print(f"Tiempo de reacción: {experimento['tiempo_reaccion_min']} min")

# Calcular moles iniciales de TG
# TODO 6: Usa la función calcular_moles
moles_TG_inicial = calcular_moles(
    experimento['masa_TG_inicial_g'],
    masas_molares['TG_tripalmitin']
)

# Calcular masa de MeOH
masa_MeOH_g = experimento['volumen_MeOH_mL'] * densidades['MeOH_kg_L']

# Calcular moles iniciales de MeOH
moles_MeOH_inicial = calcular_moles(masa_MeOH_g, masas_molares['MeOH'])

# Calcular moles de FAME producidos
moles_FAME_producido = calcular_moles(
    experimento['masa_FAME_final_g'],
    masas_molares['FAME_metil_palmitato']
)

# Según estequiometría: 1 TG → 3 FAME
# Moles teóricos de FAME si todo el TG reacciona
moles_FAME_teorico = moles_TG_inicial * 3

# Moles de TG consumidos (basado en FAME producido)
moles_TG_consumido = moles_FAME_producido / 3

# Moles finales de TG
moles_TG_final = moles_TG_inicial - moles_TG_consumido

# TODO 7: Calcula la conversión de TG usando tu función
conversion_TG = calcular_conversion(moles_TG_inicial, moles_TG_final)

# TODO 8: Calcula el rendimiento de FAME usando tu función
rendimiento_FAME = calcular_rendimiento(moles_FAME_producido, moles_FAME_teorico)

# Volumen total en litros
volumen_total_L = experimento['volumen_reactor_mL'] / 1000

# TODO 9: Calcula concentraciones molares iniciales
C_TG_inicial = calcular_concentracion_molar(moles_TG_inicial, volumen_total_L)
C_MeOH_inicial = calcular_concentracion_molar(moles_MeOH_inicial, volumen_total_L)

# ==============================================================================
# PASO 4: Mostrar resultados
# ==============================================================================

print("\n" + "="*70)
print("📈 RESULTADOS DE LOS CÁLCULOS")
print("="*70)

print("\n🔬 MOLES:")
print(f"  TG inicial:       {moles_TG_inicial:.4f} mol")
print(f"  MeOH inicial:     {moles_MeOH_inicial:.4f} mol")
print(f"  FAME producido:   {moles_FAME_producido:.4f} mol")
print(f"  FAME teórico:     {moles_FAME_teorico:.4f} mol")

print("\n📊 CONCENTRACIONES INICIALES:")
print(f"  [TG]₀:   {C_TG_inicial:.3f} mol/L")
print(f"  [MeOH]₀: {C_MeOH_inicial:.3f} mol/L")

print("\n✨ MÉTRICAS DE DESEMPEÑO:")
print(f"  Conversión de TG: {conversion_TG:.2f} %")
print(f"  Rendimiento FAME: {rendimiento_FAME:.2f} %")

# Relación molar MeOH:TG
relacion_molar = moles_MeOH_inicial / moles_TG_inicial
print(f"  Relación molar MeOH:TG = {relacion_molar:.1f}:1")

# Verificar si es exceso de MeOH (estequiométrico es 3:1)
if relacion_molar >= 3:
    print(f"  ✓ Metanol en exceso (estequiométrico: 3:1)")
else:
    print(f"  ⚠ Metanol deficiente (se requiere mínimo 3:1)")

print("\n" + "="*70)
print("✅ PRÁCTICA COMPLETADA EXITOSAMENTE")
print("="*70)
```

## ✅ Verificación

Ejecuta el código:

```bash
python ejercicio.py
```

**Salida esperada:**
```
======================================================================
PRÁCTICA 1: Cálculos Químicos Básicos con Python
======================================================================

✓ Datos cargados exitosamente desde config.json

📊 DATOS DEL EXPERIMENTO
----------------------------------------------------------------------
Volumen del reactor: 350 mL
Masa inicial de TG: 50.0 g
Volumen de MeOH: 25.0 mL
Masa final de FAME: 42.3 g
Temperatura: 65 °C
Tiempo de reacción: 120 min

======================================================================
📈 RESULTADOS DE LOS CÁLCULOS
======================================================================

🔬 MOLES:
  TG inicial:       0.0619 mol
  MeOH inicial:     0.6188 mol
  FAME producido:   0.1564 mol
  FAME teórico:     0.1858 mol

📊 CONCENTRACIONES INICIALES:
  [TG]₀:   0.177 mol/L
  [MeOH]₀: 1.768 mol/L

✨ MÉTRICAS DE DESEMPEÑO:
  Conversión de TG: 84.08 %
  Rendimiento FAME: 84.16 %
  Relación molar MeOH:TG = 10.0:1
  ✓ Metanol en exceso (estequiométrico: 3:1)

======================================================================
✅ PRÁCTICA COMPLETADA EXITOSAMENTE
======================================================================
```

### ¿Cómo saber si lo hiciste bien?

1. **No hay errores** al ejecutar
2. **Conversión ≈ 84%** (tolerancia ±1%)
3. **Rendimiento ≈ 84%** (tolerancia ±1%)
4. **Relación molar ≈ 10:1**

## 🚀 Desafío Extra (Opcional)

### Desafío 1: Calcular reactivo limitante
Modifica el código para determinar cuál es el reactivo limitante (TG o MeOH).

**Pista:** El reactivo limitante es el que se agota primero según la estequiometría.

### Desafío 2: Crear función para eficiencia catalítica
Define una función que calcule la eficiencia catalítica:

```
Eficiencia = (moles FAME producido) / (masa catalizador en g)
```

Asume que se usaron 2.5 g de catalizador CaO.

### Desafío 3: Experimentar con otros valores
Modifica `config.json` con:
- Menos MeOH (15 mL) → ¿Qué pasa con la conversión?
- Más TG (75 g) → ¿Cambia el rendimiento?

## 📚 Recursos Adicionales

### Documentación Python
- Tutorial oficial: https://docs.python.org/es/3/tutorial/
- Variables y tipos: https://www.w3schools.com/python/python_variables.asp
- Funciones: https://www.w3schools.com/python/python_functions.asp

### Química de Biodiésel
- Transesterificación: https://en.wikipedia.org/wiki/Transesterification
- Estequiometría: https://chem.libretexts.org/Bookshelves/General_Chemistry/Map:_Chemistry_-_The_Central_Science_(Brown_et_al.)/03:_Stoichiometry/3.04:_Determining_the_Formula_of_a_Compound

### Próximos Pasos
Cuando domines esta práctica, continúa con:
- **Práctica 2**: Listas, ciclos y visualización de datos experimentales

---

## 🆘 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'json'`
**Solución:** `json` viene incluido con Python. Verifica tu instalación.

### Error: `FileNotFoundError: config.json`
**Solución:** Asegúrate de estar en el directorio correcto:
```bash
cd mod_esterificacion/practicas/practica1_python_basico
```

### Resultados diferentes
**Solución:** Verifica que los valores en `config.json` sean exactos (sin redondeo).

---

**¡Felicidades por completar tu primera práctica de Python para ingeniería química! 🎉**
