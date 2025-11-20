# Practica 12: Personalizacion de Modelos

## Objetivo

Aprender a adaptar modelos cineticos segun el nivel de detalle requerido y comparar diferentes catalizadores. Entender las ventajas y desventajas de modelos simplificados vs detallados.

## Duracion Estimada

3-4 horas

## Conceptos Clave

- Modelo global (1 paso) vs modelo mecanistico (3 pasos)
- Balance entre simplicidad y precision
- Catalizadores: homogeneos vs heterogeneos vs enzimaticos
- Parametros cineticos especificos por catalizador

## Comparaciones

### Parte A: Modelos Cineticos

**Modelo 1 Paso (Global):**
```
TG + 3 MeOH → 3 FAME + GL
```
- Ventajas: Simple, pocos parametros, rapido de simular
- Desventajas: No captura especies intermedias (DG, MG)

**Modelo 3 Pasos (Mecanistico):**
```
TG + MeOH ⇌ DG + FAME
DG + MeOH ⇌ MG + FAME
MG + MeOH ⇌ GL + FAME
```
- Ventajas: Detallado, predice intermedios, mas realista
- Desventajas: 12 parametros, mas complejo, mas lento

### Parte B: Catalizadores

1. **NaOH (homogeneo):**
   - Ea = 65.0 kJ/mol
   - Rapido, economico
   - Problema: saponificacion, separacion

2. **CaO (heterogeneo):**
   - Ea = 68.5 kJ/mol
   - Reutilizable, no saponifica
   - Problema: lixiviacion, desactivacion

3. **Lipasa (enzimatico):**
   - Ea = 45.0 kJ/mol (menor barrera)
   - Tolerante a agua, condiciones suaves
   - Problema: caro, lento

## Metodologia

1. Ejecutar script para comparar modelos y catalizadores
2. Analizar diferencias en conversiones
3. Evaluar cuando usar cada modelo/catalizador
4. Responder preguntas en analisis.md

## Instrucciones

```bash
python main.py
```

## Graficas Generadas

1. **Grafica 1**: Comparacion modelo 1 paso vs 3 pasos
2. **Grafica 2**: Evolucion de especies (modelo 3 pasos)
3. **Grafica 3**: Comparacion de catalizadores

## Preguntas

Ver `analisis.md`:
1. ¿Cuando usar modelo simplificado vs detallado?
2. Interpretar diferencias entre catalizadores
3. Analisis costo-beneficio
4. Proponer modelo para aplicacion especifica

## Archivos

```
practica12_personalizacion_modelos/
├── main.py
├── config.json
├── README.md
├── analisis.md
└── resultados/
    ├── grafica1_comparacion_modelos.png
    ├── grafica2_especies_3pasos.png
    └── grafica3_comparacion_catalizadores.png
```

## Siguiente Paso

Has completado todas las practicas del sistema. Ahora puedes:
1. Revisar el README principal del repositorio
2. Explorar el codigo fuente en src/
3. Aplicar lo aprendido a tus propios datos
