# Analisis de la Practica 10: Validacion con Literatura

**Nombre:** ___________________________

**Fecha:** ___________________________

---

## Pregunta 1: Calidad del Ajuste Global

**Enunciado:** Segun las metricas calculadas, ¿el modelo esta validado? Justifica tu respuesta con R² y RMSE promedio.

**Tus datos (de la consola):**

| Temperatura | R² | RMSE (%) | MAPE (%) |
|-------------|-----|----------|----------|
| 60°C | _____ | _____ | _____ |
| 65°C | _____ | _____ | _____ |
| 70°C | _____ | _____ | _____ |
| 75°C | _____ | _____ | _____ |
| **PROMEDIO** | _____ | _____ | _____ |

**¿Esta validado el modelo?**

[ ] Si, validado (R² > 0.95, RMSE < 5%)
[ ] Parcialmente validado (R² > 0.90, RMSE < 8%)
[ ] No validado

**Justificacion:**

---

## Pregunta 2: Comparacion de Parametros Cineticos

**Enunciado:** Compara los parametros A y Ea de Kouzu vs nuestro modelo. ¿Son similares? ¿Por que puede haber diferencias?

**Tus datos:**

|  | Kouzu et al. | Nuestro modelo | Diferencia (%) |
|---|--------------|----------------|----------------|
| A (L/mol/min) | _____ | _____ | _____ |
| Ea (kJ/mol) | _____ | _____ | _____ |

**Posibles razones de las diferencias:**

[Considera: tipo de aceite (soja vs palma), catalizador (CaO vs NaOH), metodo de ajuste, condiciones experimentales...]

---

## Pregunta 3: Temperatura con Mejor Ajuste

**Enunciado:** Observa la Grafica 1. ¿En que temperatura el ajuste es mejor (mayor R², menor RMSE)?

**Respuesta:**

Temperatura con mejor ajuste: _____ °C

**¿Por que crees que el ajuste es mejor en esa temperatura?**

---

## Pregunta 4: Analisis de Residuos

**Enunciado:** Observa la Grafica 1. ¿En que region (tiempo inicial, medio, final) los residuos (diferencia entre puntos y linea) son mayores?

**Tu observacion:**

Region con mayores residuos: ___________________

**¿Que implica esto para el modelo?**

[Si los residuos son mayores al inicio, el modelo subestima la velocidad inicial. Si son mayores al final, el modelo predice una conversion mayor a la real...]

---

## Pregunta 5: Extrapolacion

**Enunciado:** Si quisieras usar este modelo para predecir conversion a 55°C (fuera del rango validado 60-75°C), ¿confiar en los resultados? ¿Por que si o por que no?

**Tu respuesta:**

---

## Pregunta 6: Propuesta de Mejora

**Enunciado:** Si tuvieras que mejorar el modelo para obtener mejor ajuste, ¿que modificarias?

Opciones:
- [ ] Usar modelo de 3 pasos en vez de simplificado
- [ ] Ajustar A y Ea especificamente para estos datos
- [ ] Incluir efectos de transferencia de masa
- [ ] Otro: _______________________

**Justifica tu eleccion:**

---

## Reflexion Final

**¿Que aprendiste sobre validacion de modelos cineticos y comparacion con literatura?**

[Tu respuesta aqui]

---

## Notas Adicionales

[Espacio para observaciones o dudas]
