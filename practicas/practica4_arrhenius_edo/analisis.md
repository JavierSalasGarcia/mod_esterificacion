# Analisis de la Practica 4: EDOs y Ecuacion de Arrhenius

**Nombre del estudiante:** ___________________________

**Fecha:** ___________________________

---

## Pregunta 1: Interpretacion del Grafico de Arrhenius

**Enunciado:** Observa la Grafica 3 (grafico de Arrhenius). Las lineas son rectas. ¿Por que? ¿Que representa la pendiente de cada linea?

**Tu respuesta:**

¿Por que son rectas?

[Pista: ln(k) = ln(A) - Ea/(R*T). Es una ecuacion lineal de la forma y = b + m*x]

¿Que representa la pendiente?

[Pista: pendiente = -Ea/R]

---

## Pregunta 2: Paso Limitante

**Enunciado:** Observa la Grafica 4. ¿Cual de las tres constantes (k1, k2, k3) es la menor? ¿Que paso (1, 2 o 3) es el paso limitante? ¿Como afecta esto a la reaccion global?

**Tu respuesta:**

Constante menor: k_____

Paso limitante: Paso _____

Efecto en la reaccion global:

[La velocidad de la reaccion global esta determinada por el paso mas lento...]

---

## Pregunta 3: Efecto de la Temperatura

**Enunciado:** Compara los escenarios A (50°C) y C (70°C) en la Grafica 2. ¿Cuanto aumenta la conversion final? ¿Es un aumento lineal o exponencial?

**Tus datos:**

Conversion a 50°C: _______ %
Conversion a 70°C: _______ %
Aumento absoluto: _______ puntos porcentuales
Aumento relativo: _______ %

**Tipo de cambio:**

[ ] Lineal
[ ] Exponencial

**Justificacion:**

[Grafica k vs T o calcula el factor de aumento]

---

## Pregunta 4: Especies Intermedias

**Enunciado:** Observa la Grafica 1. Las concentraciones de DG y MG aumentan al inicio y luego disminuyen. ¿Por que ocurre esto? ¿En que momento alcanzan su maximo?

**Tu respuesta:**

Tiempo de maximo para DG: _______ min
Tiempo de maximo para MG: _______ min

Explicacion:

[Al inicio se forman rapidamente (TG → DG → MG), pero luego se consumen para formar GL. Son intermediarios de reaccion...]

---

## Pregunta 5: Energia de Activacion

**Enunciado:** Segun los parametros en config.json:
- Ea1 = 55.3 kJ/mol (TG → DG)
- Ea2 = 58.7 kJ/mol (DG → MG)
- Ea3 = 62.1 kJ/mol (MG → GL)

¿Por que Ea aumenta en cada paso? ¿Que implica para la velocidad relativa de cada paso?

**Tu respuesta:**

[Mayor Ea = mayor barrera energetica. Pero observa que los factores pre-exponenciales A1, A2, A3 tambien aumentan...]

Implicacion para las velocidades:

[A mayor Ea, menor k (si A es constante). Pero si A aumenta mas que Ea, k puede aumentar...]

---

## Pregunta 6: Experimento Propio

**Enunciado:** Diseña tu propio experimento modificando config.json.

### Experimento 1

**¿Que modificaste?**

[Ejemplo: Cambie todas las temperaturas aumentandolas en 15°C]

**¿Que observaste?**

[Ejemplo: La conversion final aumento de X% a Y%]

**¿Por que ocurrio ese cambio?**

[Explicacion basada en Arrhenius]

### Experimento 2 (opcional)

**¿Que modificaste?**

**¿Que observaste?**

**¿Por que ocurrio ese cambio?**

### Experimento 3 (opcional)

**¿Que modificaste?**

**¿Que observaste?**

**¿Por que ocurrio ese cambio?**

---

## Reflexion Final

**¿Que aprendiste sobre la ecuacion de Arrhenius y la resolucion de EDOs?**

[Escribe aqui un parrafo resumen de tus principales conclusiones.]

---

## Calculos Adicionales (Opcional)

### Calculo manual de k a una temperatura intermedia

Usando la ecuacion de Arrhenius, calcula k1 a 55°C:

```
T = 55°C = _______ K
A1 = 8.4e4 L/mol/min
Ea1 = 55.3 kJ/mol
R = 8.314e-3 kJ/(mol·K)

k1 = A1 * exp(-Ea1 / (R*T))
   = 8.4e4 * exp(-55.3 / (8.314e-3 * _______))
   = 8.4e4 * exp(________)
   = _______ L/mol/min
```

Compara con el valor de la Grafica 4. ¿Coincide?

---

## Notas y Observaciones Adicionales

[Espacio para cualquier observacion, duda o idea que te haya surgido durante la practica.]
