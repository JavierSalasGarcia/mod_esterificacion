# Analisis de la Practica 3: Procesamiento de Datos con Pandas

**Nombre del estudiante:** ___________________________

**Fecha:** ___________________________

---

## Pregunta 1: Analisis de Concentraciones

**Enunciado:** Segun la Grafica 1, ¿en que momento las concentraciones de TG y FAME se cruzan (tienen el mismo valor)? ¿Que implica esto en terminos de la conversion?

**Tu respuesta:**

Tiempo aproximado del cruce: _______ min

Implicacion:

[Escribe aqui tu respuesta. Considera que si [FAME] = [TG], y la reaccion produce 3 moles de FAME por cada mol de TG consumido, ¿que conversion se ha alcanzado?]

---

## Pregunta 2: Velocidades de Reaccion

**Enunciado:** Observa la Grafica 3. ¿Por que la velocidad de conversion es maxima al inicio y disminuye con el tiempo? Relacionalo con las concentraciones de reactivos.

**Tu respuesta:**

[Escribe aqui tu respuesta. Considera la ley de velocidad y como cambian las concentraciones de TG y MeOH.]

---

## Pregunta 3: Estado Estacionario

**Enunciado:** Segun la Grafica 5, ¿en que tiempo se alcanza el estado estacionario? ¿Vale la pena continuar la reaccion despues de ese punto?

**Tu respuesta:**

Tiempo de estado estacionario: _______ min

Conversion en ese punto: _______ %

¿Vale la pena continuar?

[Escribe aqui tu respuesta. Considera factores economicos como consumo energetico y tiempo de produccion.]

---

## Pregunta 4: Control de Temperatura

**Enunciado:** Observa la Grafica 2. ¿La temperatura se mantiene constante durante todo el experimento? Si hay pequeñas variaciones, ¿cual es el rango de variacion y crees que es aceptable?

**Tu respuesta:**

Temperatura promedio: _______ °C

Rango de variacion: de _______ °C a _______ °C

¿Es aceptable?

[Escribe aqui tu respuesta. Considera que variaciones menores a ±1°C suelen considerarse aceptables en control termico.]

---

## Pregunta 5: Analisis Estadistico

**Enunciado:** Abre el archivo `resultados/estadisticas_descriptivas.csv`. Compara la media y la desviacion estandar de `conc_TG_mol_L` y `conc_FAME_mol_L`. ¿Cual tiene mayor variabilidad? ¿Por que?

**Tus datos:**

|  | Media | Desv. Std | Coef. Variacion (%) |
|---|-------|-----------|---------------------|
| TG | _____ | _____ | _____ |
| FAME | _____ | _____ | _____ |

Nota: Coef. Variacion = (Desv. Std / Media) * 100

**Tu respuesta:**

[Escribe aqui tu respuesta. ¿Cual tiene mayor coeficiente de variacion? ¿Por que tiene sentido dado el comportamiento de la reaccion?]

---

## Pregunta 6: Boxplot

**Enunciado:** Observa la Grafica 4 (boxplot). ¿Cual especie tiene el rango intercuartil (IQR) mas amplio? ¿Que significa esto en terminos de la dinamica de la reaccion?

**Tu respuesta:**

Especie con mayor IQR: _______

Significado:

[Escribe aqui tu respuesta. El IQR representa el rango donde esta el 50% central de los datos. Un IQR amplio indica que la variable cambia mucho durante el experimento.]

---

## Reflexion Final

**¿Que aprendiste sobre el uso de Pandas para analizar datos experimentales?**

[Escribe aqui un parrafo resumen de tus principales conclusiones sobre las herramientas de Pandas utilizadas.]

---

## Experimentos Adicionales (Opcional)

Si generaste otros archivos de datos y los analizaste:

1. **Que datos adicionales analizaste:**

2. **Que resultados obtuviste:**

3. **Que diferencias observaste:**

---

## Ejercicio de Codigo (Opcional)

Intenta modificar el script para:

1. Agregar una columna calculando el rendimiento molar de FAME respecto a TG inicial
2. Graficar la correlacion entre temperatura y velocidad de conversion
3. Exportar solo los datos del periodo 30-90 min a un CSV separado

**Describe tus modificaciones y resultados:**

[Espacio para tus anotaciones]

---

## Notas y Observaciones Adicionales

[Espacio para cualquier observacion, duda o idea que te haya surgido durante la practica.]
