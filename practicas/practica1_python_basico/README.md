# Practica 1: Calculos Estequiometricos para Transesterificacion

## Objetivo

Comprender los calculos estequiometricos basicos involucrados en la reaccion de transesterificacion para produccion de biodiesel. Aprender a visualizar datos y comparar diferentes escenarios experimentales.

## Duracion Estimada

2 horas

## Conceptos Clave

- Relacion molar (MeOH:TG)
- Masa molar y conversiones
- Balance de masa
- Capacidad del reactor
- Rendimiento masico

## Reaccion Quimica

La transesterificacion de trigliceridos con metanol sigue la ecuacion:

```
TG + 3 MeOH → 3 FAME + GL
```

Donde:
- TG = Triglicerido (ej. tripalmitina)
- MeOH = Metanol
- FAME = Esteres metilicos de acidos grasos (biodiesel)
- GL = Glicerol

## Metodologia: OBSERVAR

En esta practica, el codigo ya esta completo. Tu tarea es:

1. **Ejecutar el script** y observar las graficas generadas
2. **Analizar los resultados** comparando los 4 escenarios predefinidos
3. **Responder preguntas** de investigacion en `analisis.md`
4. **Modificar parametros** en `config.json` para explorar otros casos
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

1. **Grafica 1**: Comparacion de masas (reactivos vs productos)
2. **Grafica 2**: Relacion molar vs conversion esperada
3. **Grafica 3**: Volumenes en el reactor vs capacidad
4. **Grafica 4**: Rendimiento masico de biodiesel

### Paso 3: Responder preguntas de investigacion

Abre el archivo `analisis.md` y responde las preguntas usando las graficas y la tabla de resultados.

### Paso 4: Experimentar con otros escenarios

Modifica el archivo `config.json` para explorar:

- Diferentes relaciones molares (prueba 4:1, 7:1, 10:1)
- Diferentes masas de TG inicial (prueba 30 g, 70 g)
- Diferentes conversiones esperadas

Vuelve a ejecutar `python main.py` y compara los nuevos resultados.

## Preguntas de Investigacion

Responde estas preguntas en el archivo `analisis.md`:

### Pregunta 1: Relacion Molar

¿Por que se necesita un exceso de metanol superior a la relacion estequiometrica (3:1)?
¿Que ventajas y desventajas tiene usar una relacion muy alta (12:1)?

### Pregunta 2: Conversion

Observa la Grafica 2. ¿La relacion entre relacion molar y conversion es lineal?
¿Que ocurre cuando aumentas la relacion molar de 9:1 a 12:1?

### Pregunta 3: Capacidad del Reactor

Segun la Grafica 3, ¿algun escenario excede la capacidad del reactor de 350 mL?
Si quisieras usar una relacion molar de 15:1 con 50 g de TG, ¿que deberian hacer?

### Pregunta 4: Rendimiento Masico

Observa la Grafica 4. ¿Por que el rendimiento masico (masa FAME / masa TG) puede ser mayor al 100%?
Pista: Revisa los coeficientes estequiometricos y las masas molares.

### Pregunta 5: Diseño de Experimento

Si tuvieras presupuesto limitado para metanol pero quisieras alcanzar al menos 90% de conversion,
¿que relacion molar elegiras? Justifica tu respuesta usando las graficas.

## Escenarios Predefinidos

El archivo `config.json` incluye 4 escenarios para comparar:

| Escenario | Relacion Molar | Conversion Esperada | Comentario |
|-----------|----------------|---------------------|------------|
| A | 3:1 | 50% | Relacion minima teorica |
| B | 6:1 | 85% | Ligero exceso |
| C | 9:1 | 95% | Alto exceso |
| D | 12:1 | 98% | Exceso extremo |

## Archivos de la Practica

```
practica1_python_basico/
├── main.py              # Script completo (NO modificar)
├── config.json          # Parametros configurables (MODIFICAR AQUI)
├── README.md            # Esta guia
├── analisis.md          # Plantilla para tus respuestas
└── resultados/          # Carpeta con graficas generadas
    ├── grafica1_comparacion_masas.png
    ├── grafica2_relacion_molar_conversion.png
    ├── grafica3_volumenes_reactor.png
    └── grafica4_rendimiento_masico.png
```

## Fuentes de Datos

Todos los parametros tienen fuentes documentadas:

- **Masas molares**: PubChem Database (https://pubchem.ncbi.nlm.nih.gov/)
- **Densidades**: Perry's Chemical Engineers' Handbook, 9th Ed.
- **Conversiones esperadas**: Kouzu et al. (2008), correlaciones empiricas

## Notas Importantes

- Este script es totalmente funcional. No necesitas escribir codigo.
- Toda la personalizacion se hace en `config.json`
- Las graficas se guardan automaticamente en `resultados/`
- Puedes ejecutar el script las veces que necesites

## Siguiente Practica

En la Practica 2 agregaremos perfiles de temperatura en funcion del tiempo y visualizaremos su efecto en la conversion.
