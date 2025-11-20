# Práctica 2: Listas, Ciclos y Visualización de Datos Experimentales

## 📖 Teoría

### Conceptos Python
- **Listas**: Colecciones ordenadas de elementos `[1, 2, 3]`
- **Ciclos for**: Repetir código para cada elemento
- **Matplotlib**: Librería para crear gráficas
- **Diccionarios**: Pares clave-valor `{"temp": 65}`

### Conceptos Químicos
En cinética de reacción, monitoreamos **conversión vs tiempo**:
- Puntos temporales: t = 0, 10, 20, ..., 120 min
- Conversión aumenta con el tiempo
- Forma de curva indica tipo de cinética

## 🎯 Objetivos

- ✅ Trabajar con listas de datos experimentales
- ✅ Usar ciclos `for` para procesar datos
- ✅ Crear gráficas con matplotlib
- ✅ Guardar gráficas como archivos PNG

## 📦 Requisitos

```bash
pip install matplotlib numpy
```

## 💡 Conceptos Clave

| Término | Ejemplo |
|---------|---------|
| Lista | `tiempos = [0, 10, 20, 30]` |
| Índice | `tiempos[0]` devuelve `0` |
| Append | `lista.append(5)` agrega 5 al final |
| Ciclo for | `for t in tiempos:` |
| Diccionario | `datos = {"T": 65, "rpm": 400}` |

## 👨‍💻 Ejercicio

Ejecuta `python ejercicio.py` y sigue las instrucciones.

## ✅ Verificación

La gráfica debe mostrar:
- Conversión aumentando de 0% a ~85%
- Curva suave (típica de 1er orden)
- Ejes etiquetados correctamente
- Archivo `conversion_vs_tiempo.png` generado

## 🚀 Desafío Extra

1. Agregar línea de tendencia exponencial
2. Graficar múltiples temperaturas (55, 65, 75°C) en una sola gráfica
3. Calcular velocidad de reacción (derivada numérica)

## 📚 Recursos

- Matplotlib tutorial: https://matplotlib.org/stable/tutorials/index.html
- Listas Python: https://docs.python.org/3/tutorial/datastructures.html
