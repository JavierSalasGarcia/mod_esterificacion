# Práctica 4: Modelos Cinéticos Simples (Ecuación de Arrhenius)

## Teoría

**Ecuación de Arrhenius:** k = A × exp(-Ea/RT)
- k: constante de velocidad
- A: factor pre-exponencial
- Ea: energía de activación (kJ/mol)
- R: constante de gases (8.314 J/mol·K)
- T: temperatura (K)

**EDO de 1er orden:** dC/dt = -k×C

## Objetivos

- ✓ Implementar ecuación de Arrhenius
- ✓ Resolver EDOs con scipy.integrate.odeint
- ✓ Simular perfiles de concentración
- ✓ Comparar diferentes temperaturas

## Requisitos

```bash
pip install numpy scipy matplotlib
```

## Verificación

- Gráfica muestra decaimiento exponencial
- A mayor T → mayor k → reacción más rápida
- Conversión a 75°C > 65°C > 55°C
