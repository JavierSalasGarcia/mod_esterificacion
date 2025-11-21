# Practica 4: EDOs y Ecuacion de Arrhenius

## Objetivo

Aprender a resolver ecuaciones diferenciales ordinarias (EDOs) usando scipy.integrate.odeint para modelar la cinetica de transesterificacion. Comprender la ecuacion de Arrhenius y como los parametros cineticos (A, Ea) afectan la velocidad de reaccion.

## Duracion Estimada

3-4 horas

## Conceptos Clave

- Ecuacion de Arrhenius: k = A * exp(-Ea / RT)
- Factor pre-exponencial (A)
- Energia de activacion (Ea)
- Ecuaciones diferenciales ordinarias (EDOs)
- Modelo cinetico de tres pasos reversible
- Integracion numerica con scipy.odeint
- Grafico de Arrhenius (ln(k) vs 1/T)

## Modelo Cinetico

Esta practica utiliza un modelo de tres pasos reversible basado en Noureddini & Zhu (1997):

### Paso 1: TG + MeOH ⇌ DG + FAME
- k1 (directa): A1 * exp(-Ea1 / RT)
- k_inv1 (inversa): A_inv1 * exp(-Ea_inv1 / RT)
- Paso limitante (Ea1 = 55.3 kJ/mol)

### Paso 2: DG + MeOH ⇌ MG + FAME
- k2 (directa): A2 * exp(-Ea2 / RT)
- k_inv2 (inversa): A_inv2 * exp(-Ea_inv2 / RT)
- Paso intermedio (Ea2 = 58.7 kJ/mol)

### Paso 3: MG + MeOH ⇌ GL + FAME
- k3 (directa): A3 * exp(-Ea3 / RT)
- k_inv3 (inversa): A_inv3 * exp(-Ea_inv3 / RT)
- Paso mas rapido (Ea3 = 62.1 kJ/mol)

### EDOs del Sistema:

```
dC_TG/dt = -k1*C_TG*C_MeOH + k_inv1*C_DG*C_FAME
dC_DG/dt = k1*C_TG*C_MeOH - k_inv1*C_DG*C_FAME - k2*C_DG*C_MeOH + k_inv2*C_MG*C_FAME
dC_MG/dt = k2*C_DG*C_MeOH - k_inv2*C_MG*C_FAME - k3*C_MG*C_MeOH + k_inv3*C_GL*C_FAME
dC_GL/dt = k3*C_MG*C_MeOH - k_inv3*C_GL*C_FAME
dC_MeOH/dt = -k1*C_TG*C_MeOH - k2*C_DG*C_MeOH - k3*C_MG*C_MeOH + ...
dC_FAME/dt = k1*C_TG*C_MeOH + k2*C_DG*C_MeOH + k3*C_MG*C_MeOH + ...
```

## Metodologia: EXPERIMENTAR

En esta practica, el codigo esta completo pero TU debes:

1. **Ejecutar el script** y observar los resultados base
2. **Modificar temperaturas** en `config.json` y comparar
3. **Modificar parametros cineticos** (A, Ea) y observar el efecto
4. **Responder preguntas** de investigacion en `analisis.md`
5. **Proponer experimentos** propios y documentar resultados

## Instrucciones

### Paso 1: Ejecutar el script base

Abre una terminal en este directorio y ejecuta:

```bash
python main.py
```

El script:
- Resolvera las EDOs con scipy.odeint
- Simulara 4 escenarios de temperatura
- Calculara constantes de velocidad con Arrhenius
- Generara 4 graficas automaticamente

### Paso 2: Revisar las graficas base

Las graficas generadas son:

1. **Grafica 1**: Perfiles de todas las especies (TG, DG, MG, GL, FAME) para cada temperatura
2. **Grafica 2**: Comparacion de conversiones a diferentes temperaturas
3. **Grafica 3**: Grafico de Arrhenius (ln(k) vs 1/T)
4. **Grafica 4**: Constantes de velocidad vs temperatura

### Paso 3: EXPERIMENTAR - Modificar config.json

#### Experimento A: Efecto de la Temperatura

Modifica las temperaturas de los escenarios:

```json
"A_baja": {
  "temperatura_C": 45.0  // Cambia de 50 a 45
},
"C_alta": {
  "temperatura_C": 75.0  // Cambia de 70 a 75
}
```

Ejecuta `python main.py` de nuevo y compara:
- ¿Como cambio la conversion final?
- ¿Como cambiaron las constantes k1, k2, k3?

#### Experimento B: Efecto de la Energia de Activacion

Modifica Ea1 (energia de activacion del paso 1):

```json
"Ea1": 70.0  // Cambia de 55.3 a 70.0
```

Ejecuta de nuevo y observa:
- ¿Como cambio el grafico de Arrhenius?
- ¿Como afecto la conversion final?

#### Experimento C: Efecto del Factor Pre-exponencial

Modifica A1:

```json
"A1": 1.68e5  // Duplica el valor original (8.4e4 * 2)
```

Ejecuta de nuevo y observa:
- ¿Como cambio k1?
- ¿La conversion aumento proporcionalmente?

### Paso 4: Responder preguntas de investigacion

Abre el archivo `analisis.md` y responde las preguntas usando los resultados de tus experimentos.

## Preguntas de Investigacion

Responde estas preguntas en el archivo `analisis.md`:

### Pregunta 1: Interpretacion del Grafico de Arrhenius

Observa la Grafica 3 (grafico de Arrhenius). Las lineas son rectas. ¿Por que?
¿Que representa la pendiente de cada linea?

### Pregunta 2: Paso Limitante

Observa la Grafica 4. ¿Cual de las tres constantes (k1, k2, k3) es la menor?
¿Que paso (1, 2 o 3) es el paso limitante? ¿Como afecta esto a la reaccion global?

### Pregunta 3: Efecto de la Temperatura

Compara los escenarios A (50°C) y C (70°C) en la Grafica 2.
¿Cuanto aumenta la conversion final? ¿Es un aumento lineal o exponencial?

### Pregunta 4: Especies Intermedias

Observa la Grafica 1. Las concentraciones de DG y MG aumentan al inicio y luego disminuyen.
¿Por que ocurre esto? ¿En que momento alcanzan su maximo?

### Pregunta 5: Energia de Activacion

Segun los parametros en config.json:
- Ea1 = 55.3 kJ/mol (TG → DG)
- Ea2 = 58.7 kJ/mol (DG → MG)
- Ea3 = 62.1 kJ/mol (MG → GL)

¿Por que Ea aumenta en cada paso? ¿Que implica para la velocidad relativa de cada paso?

### Pregunta 6: Experimento Propio

Diseña tu propio experimento modificando config.json. Por ejemplo:
- Cambiar todas las temperaturas a +20°C
- Igualar todas las energias de activacion (Ea1 = Ea2 = Ea3 = 60.0)
- Triplicar todos los factores pre-exponenciales

Documenta:
1. ¿Que modificaste?
2. ¿Que observaste?
3. ¿Por que ocurrio ese cambio?

## Archivos de la Practica

```
practica4_arrhenius_edo/
├── main.py              # Script completo funcional (NO modificar)
├── config.json          # Parametros configurables (MODIFICAR AQUI para experimentar)
├── README.md            # Esta guia
├── analisis.md          # Plantilla para tus respuestas
└── resultados/          # Carpeta con graficas generadas
    ├── grafica1_perfiles_especies.png
    ├── grafica2_comparacion_conversion.png
    ├── grafica3_arrhenius.png
    └── grafica4_constantes_temperatura.png
```

## Fuentes de Datos

- **Parametros cineticos**: Noureddini, H., & Zhu, D. (1997). J. Am. Oil Chem. Soc. 74(11):1457-1463
- **Metodo de integracion**: scipy.integrate.odeint (algoritmo LSODA)
- **Ecuacion de Arrhenius**: Principios de cinetica quimica

## Notas Importantes

- El codigo esta completo y funcional. Experimenta modificando config.json
- Guarda copias de config.json antes de hacer cambios grandes
- Documenta todos tus experimentos en analisis.md
- Las constantes inversas (k_inv) son generalmente mucho menores que las directas

## Conceptos Avanzados (Opcional)

Si quieres profundizar, investiga:

1. **Regla de Van't Hoff**: k se duplica cada 10°C (aproximacion)
2. **Metodo de Euler**: Alternativa simple a odeint
3. **Analisis de sensibilidad**: ¿Que parametro tiene mayor impacto?
4. **Diagramas de energia**: Perfiles de energia vs coordenada de reaccion

## Siguiente Practica

En la Practica 5 aprenderemos a procesar datos de cromatografia de gases (GC-FID) con estandar interno, calcular factores de respuesta y convertir areas de picos en concentraciones reales.
