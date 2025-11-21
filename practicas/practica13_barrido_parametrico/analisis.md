# Análisis de Resultados - Práctica 13: Barrido Paramétrico Automatizado

**Nombre del estudiante:** ________________________________
**Fecha:** ____________________
**Carpeta de resultados:** `barrido_____________________`

---

## Parte 1: Configuración y Ejecución Básica

### 1.1 Cálculo Manual de Combinaciones

**Configuración analizada:**
- Parámetro 1: ____________ con ____ valores
- Parámetro 2: ____________ con ____ valores
- Parámetro 3: ____________ con ____ valores
- Parámetro 4: ____________ con ____ valores

**Cálculo del total de simulaciones:**

Total = _____ × _____ × _____ × _____ = _______ simulaciones


### 1.2 Ejecución del Barrido Pequeño (4 simulaciones)

**Tiempo total de ejecución:** __________ minutos

**Observaciones del proceso:**
- ¿Se mostró correctamente la advertencia de seguridad? [ ] Sí  [ ] No
- ¿Los archivos se organizaron correctamente por timestamp? [ ] Sí  [ ] No
- ¿Se generó el archivo `resultados_consolidados.csv`? [ ] Sí  [ ] No

**Muestra de resultados (primeras 4 filas de resultados_consolidados.csv):**

| Simulación | Temp (°C) | Rel. Molar | Conversión (%) | Tiempo (min) |
|------------|-----------|------------|----------------|--------------|
| 1          |           |            |                |              |
| 2          |           |            |                |              |
| 3          |           |            |                |              |
| 4          |           |            |                |              |

---

## Parte 2: Superficies de Respuesta

### 2.1 Barrido Temperatura vs Relación Molar (12 simulaciones)

**Rango de conversiones observado:**
- Mínima: _______%
- Máxima: _______%

**Combinación óptima identificada:**
- Temperatura: _______ °C
- Relación molar: _______:1
- Conversión alcanzada: _______%

### 2.2 Interpretación de Superficie de Respuesta

![Insertar imagen: superficie_T_vs_relMolar.png]

**Descripción de la superficie:**
(Describir cómo varía la conversión con temperatura y relación molar. ¿Hay un máximo claro? ¿Es monotónica?)

______________________________________________________________________
______________________________________________________________________
______________________________________________________________________

### 2.3 Mapa de Contorno

![Insertar imagen: contorno_T_vs_relMolar.png]

**Isolíneas relevantes:**
- Conversión 90%: Pasa por puntos (T=___, r=___) hasta (T=___, r=___)
- Conversión 95%: Pasa por puntos (T=___, r=___) hasta (T=___, r=___)

**Combinaciones viables (>95% conversión):**

| Temperatura (°C) | Relación Molar | Conversión (%) |
|------------------|----------------|----------------|
|                  |                |                |
|                  |                |                |
|                  |                |                |

---

## Parte 3: Estudio de Sensibilidad Multivariable

### 3.1 Configuración del Barrido Extendido

**Parámetros incluidos:**
- Temperatura: ____________ (_____ valores)
- Relación molar: ____________ (_____ valores)
- Catalizador: ____________ (_____ valores)
- Agitación: ____________ (_____ valores)

**Total de simulaciones:** _______
**Tiempo de ejecución:** ________ minutos

### 3.2 Análisis de Correlación

**Coeficientes de correlación con conversión final:**

| Parámetro                | Correlación (r) | Interpretación          |
|--------------------------|-----------------|-------------------------|
| Temperatura              |                 | [positiva/negativa/nula]|
| Relación molar           |                 | [positiva/negativa/nula]|
| Concentración catalizador|                 | [positiva/negativa/nula]|
| Agitación                |                 | [positiva/negativa/nula]|

**Ranking de importancia (mayor a menor influencia):**

1. _________________________
2. _________________________
3. _________________________
4. _________________________

**Justificación del ranking:**
______________________________________________________________________
______________________________________________________________________

### 3.3 Identificación de Interacciones

**¿El efecto de temperatura depende de la relación molar?**
[ ] Sí  [ ] No

**Evidencia:**
______________________________________________________________________
______________________________________________________________________

**Ejemplo de interacción (si existe):**
- A baja temperatura (50°C): Aumentar relación molar de 6 a 12 incrementa conversión en ____%
- A alta temperatura (65°C): Aumentar relación molar de 6 a 12 incrementa conversión en ____%
- **Conclusión:** El efecto [es similar / es muy diferente]

---

## Parte 4: Diseño de Procesos

### 4.1 Restricciones de Diseño

**Criterios establecidos:**
- Conversión mínima: 95%
- Tiempo máximo: 60 min
- Objetivo secundario: Minimizar relación molar (costo de metanol)

### 4.2 Resultados Filtrados

**Número de configuraciones que cumplen conversión ≥95%:** _______

**Top 3 configuraciones (menor relación molar):**

| Ranking | Temp (°C) | Rel. Molar | Cat. (%) | Agit. (rpm) | Conversión (%) |
|---------|-----------|------------|----------|-------------|----------------|
| 1       |           |            |          |             |                |
| 2       |           |            |          |             |                |
| 3       |           |            |          |             |                |

**Configuración óptima seleccionada:** Ranking #_____

### 4.3 Validación del Resultado Óptimo

**Simulación individual ejecutada con condiciones óptimas:**
- Conversión predicha por barrido: ______%
- Conversión de simulación individual: ______%
- Diferencia: ______ puntos porcentuales

**¿Coincide con la optimización numérica (Práctica 7)?**
[ ] Sí  [ ] No  [ ] No realicé Práctica 7

**Comparación (si aplica):**

| Método                    | Temp | Rel. Molar | Cat. | Conversión |
|---------------------------|------|------------|------|------------|
| Barrido paramétrico       |      |            |      |            |
| Optimización numérica (P7)|      |            |      |            |

---

## Preguntas de Análisis

### Pregunta 1: Explosión Combinatoria
**Si se exploran 6 parámetros con 5 valores cada uno, ¿cuántas simulaciones se requieren?**

Cálculo: _______________________________________________

Respuesta: _____________ simulaciones

**¿Es esto práctico?**
[ ] Sí  [ ] No

**Justificación:**
______________________________________________________________________
______________________________________________________________________

### Pregunta 2: Estrategias de Reducción

**Proponer 2 estrategias para reducir el número de simulaciones:**

1. **Estrategia 1:** _____________________________________________________

   **Cómo funciona:** ____________________________________________________
   ______________________________________________________________________

2. **Estrategia 2:** _____________________________________________________

   **Cómo funciona:** ____________________________________________________
   ______________________________________________________________________

### Pregunta 3: Interpretación Físico-Química

**¿Por qué la conversión aumenta con temperatura pero eventualmente se estabiliza?**

______________________________________________________________________
______________________________________________________________________
______________________________________________________________________

**Fenómeno limitante:** __________________________________________________

### Pregunta 4: Efecto de Interacción

**¿El efecto de aumentar relación molar es igual a 50°C que a 65°C?**
[ ] Sí, es igual  [ ] No, es diferente

**Explicación:**
______________________________________________________________________
______________________________________________________________________
______________________________________________________________________

### Pregunta 5: Optimización vs Barrido

**Comparación de métodos:**

| Característica        | Barrido Paramétrico | Optimización Numérica |
|-----------------------|---------------------|-----------------------|
| Precisión del óptimo  |                     |                       |
| Tiempo de cómputo     |                     |                       |
| Facilidad de uso      |                     |                       |
| Información adicional |                     |                       |

**¿Cuál método es más apropiado en cada caso?**
______________________________________________________________________
______________________________________________________________________

### Pregunta 6: Aplicabilidad Industrial

**¿En qué etapa del desarrollo es más útil el barrido paramétrico exhaustivo?**
[ ] Laboratorio  [ ] Piloto  [ ] Industrial  [ ] Todas

**Justificación:**
______________________________________________________________________
______________________________________________________________________

**¿En qué etapa es más útil la optimización numérica?**
[ ] Laboratorio  [ ] Piloto  [ ] Industrial  [ ] Todas

**Justificación:**
______________________________________________________________________
______________________________________________________________________

---

## Reflexión Personal

**Ventajas y limitaciones de los barridos paramétricos (200-300 palabras):**

______________________________________________________________________
______________________________________________________________________
______________________________________________________________________
______________________________________________________________________
______________________________________________________________________
______________________________________________________________________
______________________________________________________________________
______________________________________________________________________
______________________________________________________________________
______________________________________________________________________

---

## Anexos

### A1. Capturas de Pantalla

- [ ] Dashboard interactivo (`resumen_comparativo.html`)
- [ ] Superficie 3D principal
- [ ] Mapa de contorno
- [ ] Matriz de correlación

### A2. Archivos Adjuntos

- [ ] `resultados_consolidados.csv`
- [ ] `estadisticas_resumen.csv`
- [ ] Carpeta `visualizaciones/` completa
- [ ] Este archivo `analisis.md` completado

---

**Fecha de entrega:** ____________________
**Firma:** ____________________
