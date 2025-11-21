# Practica 8: Workflow Completo

## Objetivo

Integrar todos los modulos del sistema en un workflow automatizado completo: procesamiento GC → ajuste de parametros → optimizacion → reporte HTML interactivo.

## Duracion Estimada

4-5 horas

## Conceptos Clave

- Integracion de modulos
- Pipeline de datos
- Reporte automatizado HTML
- Graficas interactivas con Plotly
- Analisis end-to-end

## Workflow Completo (4 Pasos)

### Paso 1: Procesamiento de Datos GC
- Cargar areas de picos
- Aplicar estandar interno
- Calcular concentraciones
- Exportar datos procesados

### Paso 2: Ajuste de Parametros
- Cargar datos procesados
- Ajustar A y Ea con lmfit
- Calcular intervalos de confianza
- Validar ajuste (R², RMSE)

### Paso 3: Optimizacion
- Usar parametros ajustados
- Optimizar condiciones operacionales
- Generar superficies de respuesta
- Proponer condiciones optimas

### Paso 4: Reporte HTML
- Generar reporte interactivo
- Incluir todas las graficas
- Resumen de resultados
- Recomendaciones

## Instrucciones

```bash
python workflow.py
```

El script ejecutara los 4 pasos secuencialmente y generara:
- `reporte_completo.html` (archivo principal)
- Carpeta `resultados/` con todas las graficas
- Archivo JSON con resultados

## Graficas en el Reporte

1. Procesamiento GC (areas y concentraciones)
2. Ajuste de parametros (datos vs modelo)
3. Superficies de optimizacion
4. Resumen ejecutivo

## Archivos

```
practica8_workflow_completo/
├── workflow.py          # Script principal integrado
├── config.json          # Configuracion global
├── README.md
├── analisis.md
├── datos/
│   └── gc_data.csv
└── resultados/
    ├── reporte_completo.html  # ABRIR EN NAVEGADOR
    ├── resultados.json
    └── graficas/
```

## Preguntas

Ver `analisis.md`:
1. ¿El workflow se ejecuto sin errores?
2. ¿Los resultados son consistentes entre pasos?
3. Revisar recomendaciones del reporte
4. Identificar puntos de mejora

## Siguiente Practica

Practica 9: Up-scaling y CFD para escalado industrial con Ansys Fluent.
