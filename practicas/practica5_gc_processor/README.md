# Práctica 5: Procesamiento de Datos GC-FID con el Sistema

## 📖 Teoría

Ahora usarás el módulo **real** del repositorio: `src.data_processing.gc_processor`

Este módulo automatiza todo el procesamiento de cromatografía.

## 🎯 Objetivos

- ✅ Importar módulos del sistema (`from src.data_processing import GCProcessor`)
- ✅ Procesar datos GC-FID reales
- ✅ Ejecutar desde línea de comandos (CLI)
- ✅ Generar reportes automáticos

## 📦 Requisitos

```bash
cd /home/user/mod_esterificacion
pip install -r requirements.txt
```

## 👨‍💻 Uso del Módulo

```python
from src.data_processing.gc_processor import GCProcessor

processor = GCProcessor()
data = processor.load_from_csv('datos.csv')
results = processor.process_time_series(data, C_TG0=0.5)
```

## ✅ Verificación

- Importación exitosa sin errores
- Conversión calculada automáticamente
- Estadísticas generadas

## 🚀 CLI

```bash
python main.py --mode process_gc --input datos.csv --output results/
```
