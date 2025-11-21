# Practica 9: Up-scaling y CFD

## Objetivo

Aprender a escalar de escala laboratorio (350 mL) a escala piloto (20 L) aplicando criterios de escalado. Generar UDF (User Defined Function) para Ansys Fluent con cinetica de transesterificacion.

## Duracion Estimada

4-5 horas

## Conceptos Clave

- Escalado de reactores batch
- Criterios de similitud: P/V, Re, v_tip, θ_m
- Geometria de reactor: ribbon impeller + serpentin
- CFD con Ansys Fluent
- UDF en lenguaje C para cinetica

## Partes de la Practica

### Parte A: Calculos de Escalado

Escalar de:
- Laboratorio: 350 mL, agitador Rushton, 600 rpm
- Piloto: 20 L, ribbon impeller, rpm_piloto = ?

Criterios:
1. Potencia por volumen (P/V) constante
2. Numero de Reynolds similar
3. Velocidad en punta de impulsor (v_tip)
4. Tiempo de mezclado (θ_m)

### Parte B: Geometria del Reactor

Reactor cilindrico vertical con:
- Ribbon impeller (helicoidal)
- Serpentin de enfriamiento (10 espiras)
- Relacion H/D = 1.5
- 4 deflectores

### Parte C: UDF para Cinetica

Generar archivo C con:
- Ecuacion de Arrhenius
- Modelo de 3 pasos
- Terminos fuente para especies
- Compatible con Ansys Fluent 2023

### Parte D: Postproceso CFD

Procesar resultados de Fluent:
- Campos de velocidad
- Perfiles de temperatura
- Distribucion de conversion

## Instrucciones

### Parte A:
```bash
python parte_A_escalado.py
```

### Parte B:
```bash
python parte_B_geometria.py
```

### Parte C:
Revisar archivo `parte_D_udf_cinetica.c`

### Parte D:
```bash
python parte_E_postproceso.py
```

## Archivos

```
practica9_upscaling_cfd/
├── parte_A_escalado.py
├── parte_B_geometria.py
├── parte_D_udf_cinetica.c       # UDF para Ansys Fluent
├── parte_E_postproceso.py
├── config.json
├── README.md
├── README_Ansys.md              # Guia para uso en Fluent
├── analisis.md
└── resultados/
    ├── geometria_reactor_20L.png
    ├── criterios_escalado.json
    └── campos_cfd/
```

## Preguntas

Ver `analisis.md`:
1. ¿Cual es el rpm optimo para el reactor piloto?
2. Comparar criterios de escalado
3. Interpretar campos de CFD
4. Identificar zonas muertas

## Siguiente Practica

Practica 10: Validacion con datos de literatura (Kouzu et al. 2008).
