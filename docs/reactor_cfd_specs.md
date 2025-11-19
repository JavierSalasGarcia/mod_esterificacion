# Especificaciones CFD - Reactor de Transesterificación 20L

**Documento:** Especificaciones para Simulación CFD
**Fecha:** 2025-11-19
**Reactor:** Tanque agitado 20L para producción de biodiésel
**Software:** Ansys Fluent / PyFluent

---

## 1. Geometría del Reactor

### 1.1 Dimensiones Principales

| Parámetro | Símbolo | Valor | Unidad | Relación |
|-----------|---------|-------|--------|----------|
| Volumen total | V_T | 20 | L | - |
| Diámetro del tanque | D_T | 270 | mm | - |
| Altura del tanque | H_T | 400 | mm | H_T/D_T = 1.48 |
| Altura del líquido | H_L | 350 | mm | H_L/D_T = 1.30 |
| Volumen líquido | V_L | 20 | L | - |

**Cálculos**:
```
D_T = (4·V_T / (π·H_L/D_T))^(1/3)
D_T = (4·20L / (π·1.3))^(1/3) ≈ 270 mm
H_L = 1.3 × D_T = 1.3 × 270 = 351 mm ≈ 350 mm
```

### 1.2 Tipo de Tanque

- **Configuración**: Tanque cilíndrico vertical
- **Fondo**: Tipo toriesférico (dished head) o plano (flat bottom)
  - Recomendado: Toriesférico con radio = D_T/10
- **Tapa**: Plana o ligeramente cónica
- **Material**: Acero inoxidable 316L (compatible con metanol y biodiésel)

---

## 2. Sistema de Agitación

### 2.1 Tipo de Impulsor

**OPCIÓN 1: Turbina Rushton (Recomendado)**

| Parámetro | Símbolo | Valor | Unidad | Relación |
|-----------|---------|-------|--------|----------|
| Diámetro impulsor | D_I | 90 | mm | D_I/D_T = 1/3 |
| Número de palas | N_b | 6 | - | - |
| Ancho de pala | W | 18 | mm | W = D_I/5 |
| Altura de pala | L | 22.5 | mm | L = D_I/4 |
| Espesor de pala | t | 2 | mm | - |
| Clearance (fondo) | C | 90 | mm | C = D_T/3 |
| Diámetro eje | D_shaft | 12 | mm | - |

**Ventajas Rushton**:
- Excelente para suspensión de sólidos (catalizador CaO)
- Alto shear rate → mejor transferencia de masa interfacial
- Patrón de flujo radial con dos loops de recirculación
- Bien documentado para scale-up (correlaciones de N_p)

**OPCIÓN 2: Pitched Blade Turbine (PBT) a 45°**

| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| Diámetro impulsor | 90 | mm |
| Número de palas | 4 o 6 | - |
| Ángulo de inclinación | 45 | ° |
| Clearance | 90 | mm |

**Ventajas PBT**:
- Menor consumo de potencia (20-30% menos que Rushton)
- Mejor mezcla axial
- Adecuado si el catalizador sedimenta rápidamente

### 2.2 Velocidad de Rotación

| Condición | RPM | Número de Reynolds (Re) |
|-----------|-----|-------------------------|
| Mínima | 200 | ~20,000 (turbulento) |
| Operación típica | 400-550 | ~40,000-55,000 |
| Máxima | 800 | ~80,000 |

**Cálculo de Re del impulsor**:
```
Re = ρ·N·D_I² / μ
donde:
- ρ ≈ 850 kg/m³ (mezcla metanol-aceite)
- N = velocidad rotacional (rps)
- D_I = 0.09 m
- μ ≈ 3 mPa·s (mezcla)

Re (500 rpm) = 850 × (500/60) × 0.09² / 0.003 ≈ 48,000 → Turbulento
```

### 2.3 Número de Potencia

Para Rushton turbine en régimen turbulento:
```
N_p ≈ 5.0 (valor estándar para Re > 10,000)

Potencia = N_p · ρ · N³ · D_I⁵

Ejemplo (500 rpm):
P = 5.0 × 850 × (500/60)³ × 0.09⁵
P ≈ 15 W
```

---

## 3. Baffles (Deflectores)

### 3.1 Configuración

| Parámetro | Valor | Unidad | Relación |
|-----------|-------|--------|----------|
| Número de baffles | 4 | - | Distribución a 90° |
| Ancho de baffle | W_b = 27 | mm | W_b = D_T/10 |
| Espesor de baffle | t_b = 3 | mm | - |
| Offset desde pared | Gap = 5 | mm | Para evitar zonas muertas |
| Altura de baffle | H_b = 340 | mm | Hasta H_L - 10 mm |

### 3.2 Material y Posición

- **Material**: Acero inoxidable 316L
- **Fijación**: Soldados a la pared del tanque
- **Orientación**: Vertical, alineados radialmente
- **Función**: Romper el vórtex, mejorar mezcla axial, prevenir rotación sólida

---

## 4. Propiedades del Fluido

### 4.1 Composición Inicial Típica

| Componente | Fracción másica | Densidad (kg/m³) @ 65°C | Viscosidad (mPa·s) @ 65°C |
|------------|----------------|-------------------------|---------------------------|
| Aceite (TG) | 0.70 | 900 | 15 |
| Metanol | 0.27 | 750 | 0.4 |
| CaO (sólido) | 0.03 | 3350 | - |

### 4.2 Propiedades de la Mezcla (Valores Promedio)

| Propiedad | Símbolo | Valor | Unidad |
|-----------|---------|-------|--------|
| Densidad mezcla | ρ_mix | 850 | kg/m³ |
| Viscosidad dinámica | μ_mix | 3.0 | mPa·s |
| Viscosidad cinemática | ν | 3.53 × 10⁻⁶ | m²/s |
| Capacidad calorífica | Cp | 2200 | J/(kg·K) |
| Conductividad térmica | k | 0.15 | W/(m·K) |
| Tensión superficial | σ | 25 | mN/m |

**Nota**: Propiedades varían con la conversión (TG → FAME). Para análisis detallado, usar correlaciones dependientes de composición.

### 4.3 Catalizador CaO (Fase Sólida)

| Propiedad | Valor | Unidad |
|-----------|-------|--------|
| Diámetro de partícula | 50-150 | μm |
| Densidad | 3350 | kg/m³ |
| Concentración | 1-5 | % masa |
| Velocidad terminal (aprox.) | 0.1-0.5 | mm/s |

---

## 5. Condiciones de Frontera (CFD)

### 5.1 Paredes del Tanque

```
Tipo: Wall
- Condición velocidad: No-slip
- Roughness: 0 (smooth wall - acero inoxidable pulido)
- Condición térmica: Isothermal (T = T_reacción) o Adiabatic
  - Si hay intercambio de calor: Heat flux o HTC especificado
  - HTC típico (convección natural aire exterior): h ≈ 10 W/(m²·K)
```

### 5.2 Impulsor

```
Tipo: Moving Wall (MRF) o Sliding Mesh

OPCIÓN A: Multiple Reference Frame (MRF) - Steady-State
- Zona interna: Rotating Frame (velocidad angular ω)
- Zona externa: Stationary Frame
- Interface: Sliding interface (conservación de flujo)

OPCIÓN B: Sliding Mesh - Transient
- Malla del impulsor: Rota físicamente
- Time-step: Δt = 1/(6·N) [60-120 time-steps por revolución]
- Más preciso pero computacionalmente costoso
```

**Configuración MRF (Recomendado para inicio)**:
```
Rotating Zone:
- Geometry: Cilindro coaxial con eje del impulsor
- Diámetro: D_RZ = D_I + 10 mm = 100 mm
- Altura: H_RZ = 50 mm (centrada en impulsor)
- Rotational velocity: ω = 2πN/60 (rad/s)
  - Ejemplo: 500 rpm → ω = 52.36 rad/s
```

### 5.3 Superficie Libre (Tope del Líquido)

```
OPCIÓN 1: Degassing boundary condition
- Asume interfaz plana sin deformación
- Pressure outlet: P_gauge = 0 Pa
- Backflow: None

OPCIÓN 2: VOF (Volume of Fluid) - Multifásico
- Modelar interfaz líquido-aire dinámicamente
- Primary phase: Liquid mixture
- Secondary phase: Air
- Surface tension: σ = 25 mN/m
- Más realista para altas RPM (formación de vórtex)
```

**Recomendación**: Iniciar con degassing; usar VOF si RPM > 600.

### 5.4 Baffles

```
Tipo: Wall
- No-slip
- Adiabatic (generalmente)
- Espesor: Shell conduction (t = 3 mm, k_steel = 16 W/(m·K))
```

---

## 6. Modelos de Turbulencia

### 6.1 Comparación de Modelos

| Modelo | Ventajas | Desventajas | Recomendación |
|--------|----------|-------------|---------------|
| **k-ε Standard** | Robusto, rápida convergencia | Sobreestima k cerca del impulsor | Análisis preliminar |
| **k-ε RNG** | Mejor para swirl y curvatura alta | Requiere malla más fina | ✅ **Recomendado** |
| **k-ω SST** | Excelente en capa límite, HT | Mayor costo computacional | Para análisis térmico detallado |
| **RSM** | Más preciso para anisotropía | Muy costoso, menos estable | Validación final |

### 6.2 Configuración Recomendada: k-ε RNG

```
Model: k-epsilon RNG
- Near-wall treatment: Enhanced Wall Treatment
- Prandtl numbers: Default (σ_k = 1.0, σ_ε = 1.3)

Turbulent intensity (inlet/initial):
I = 0.16·Re^(-1/8)
Para Re = 50,000: I ≈ 3.8%

Turbulent viscosity ratio: μ_t/μ ≈ 10 (inicial)
```

---

## 7. Mallado (Meshing)

### 7.1 Estrategia de Malla

| Región | Tipo de Malla | Tamaño | Celdas (aprox.) |
|--------|---------------|--------|------------------|
| Bulk (tanque) | Hexaédrica estructurada | 3-5 mm | 300,000 |
| Impulsor | Tetraédrica/Polyhedral | 1-2 mm | 150,000 |
| Baffles | Tetraédrica con inflation | 2-3 mm | 50,000 |
| Interface MRF | Refinamiento x2 | 1.5 mm | - |
| **Total** | - | - | **500,000 - 1,000,000** |

### 7.2 Inflation Layers (Capa Límite)

```
Ubicación: Paredes (tanque, baffles, impulsor)
- First layer thickness: y+ ≈ 30-300 (wall function)
  o Para y+ < 5 (resolved): t_1 ≈ 0.05 mm (costoso)
- Growth rate: 1.2
- Number of layers: 5-10

Cálculo de y+ (objetivo 30-100):
y+ = (u_τ · y₁) / ν
u_τ = sqrt(τ_w / ρ)
```

**Recomendación**: Usar y+ = 30-300 con wall functions (k-ε).

### 7.3 Calidad de Malla

Métricas objetivo:
- **Skewness**: < 0.85 (idealmente < 0.75)
- **Aspect Ratio**: < 20 (< 5 en regiones críticas)
- **Orthogonal Quality**: > 0.2 (> 0.4 preferible)

### 7.4 Independencia de Malla

Refinar hasta que:
```
|P_refined - P_coarse| / P_coarse < 5%
```
donde P es el consumo de potencia del impulsor (variable de control).

Secuencia sugerida:
1. Malla gruesa: 250,000 celdas
2. Malla media: 600,000 celdas ✅
3. Malla fina: 1,200,000 celdas (validación)

---

## 8. Modelos Multifásicos (Opcional)

### 8.1 Modelo Euleriano (Líquido-Sólido)

Si se desea modelar explícitamente el catalizador CaO:

```
Model: Eulerian Multiphase
- Primary phase: Liquid (mixture)
- Secondary phase: Solid (CaO particles)
- Volume fraction CaO: α_s = 0.015 (1.5% v/v)
- Diameter: d_p = 100 μm (promedio)
- Drag model: Schiller-Naumann o Gidaspow
- Turbulence: Mixture model o Per-phase
```

**Ecuaciones adicionales**:
```
∇·(α_l ρ_l u_l) = 0
∇·(α_s ρ_s u_s) = 0
α_l + α_s = 1

Interphase drag: F_drag = (3/4)·(C_D·Re / d_p)·ρ_l·α_s·|u_l - u_s|·(u_l - u_s)
```

---

## 9. Cinética Química (Species Transport)

### 9.1 Activación del Modelo

```
Fluent Setup:
Models → Species → Species Transport
- Reactions: Volumetric
- Turbulence-Chemistry Interaction: Eddy-Dissipation (rápido) o PDF (preciso)
```

### 9.2 Especies Definidas

| Especie | Símbolo | MW (g/mol) | Difusividad (m²/s) @ 65°C |
|---------|---------|-----------|---------------------------|
| Triglicérido | TG | 880 | 5 × 10⁻¹⁰ |
| Diglicérido | DG | 620 | 6 × 10⁻¹⁰ |
| Monoglicérido | MG | 360 | 7 × 10⁻¹⁰ |
| Metanol | MeOH | 32 | 2 × 10⁻⁹ |
| FAME | FAME | 292 | 8 × 10⁻¹⁰ |
| Glicerol | GL | 92 | 1 × 10⁻⁹ |

**Difusividades estimadas**: Usar correlación de Wilke-Chang o valores de literatura.

### 9.3 Reacciones Volumétricas

**Modelo de 1 Paso**:
```
TG + 3 MeOH → 3 FAME + GL
Rate: r = -k · [TG] · [MeOH]
```

**Modelo de 3 Pasos**:
```
R1: TG + MeOH → DG + FAME   (k1_f, k1_r)
R2: DG + MeOH → MG + FAME   (k2_f, k2_r)
R3: MG + MeOH → GL + FAME   (k3_f, k3_r)
```

### 9.4 User-Defined Function (UDF) para Cinética

**Archivo**: `transesterification_kinetics.c`

```c
#include "udf.h"

#define R 8.314          // J/(mol·K)
#define A_1 2.98e10      // Pre-exponential factor (min^-1)
#define EA_1 51900       // Activation energy (J/mol)

DEFINE_VR_RATE(transesterification_rate_1step, c, t, r, mw, yi, rr, rr_t)
{
    real C_TG, C_MeOH, T, k, rate;
    real rho = C_R(c,t);  // Density (kg/m³)

    // Extract mass fractions
    real Y_TG = yi[0][0];    // Mass fraction TG
    real Y_MeOH = yi[0][1];  // Mass fraction MeOH

    // Convert to molar concentrations (mol/m³)
    C_TG = (Y_TG * rho) / (mw[0] / 1000.0);      // mol/m³
    C_MeOH = (Y_MeOH * rho) / (mw[1] / 1000.0);

    // Temperature (K)
    T = C_T(c,t);

    // Arrhenius rate constant (convert to s^-1)
    k = A_1 * exp(-EA_1 / (R * T)) / 60.0;  // Convert min^-1 to s^-1

    // Reaction rate (mol/(m³·s))
    rate = -k * C_TG * C_MeOH;

    // Return net production rate for TG (negative = consumption)
    *rr = rate;

    // For transient, derivative wrto time
    *rr_t = 0.0;
}
```

**Compilación en Fluent**:
```
Define → User-Defined → Functions → Compiled
Source file: transesterification_kinetics.c
Build → Load
```

**Asignación a Reacción**:
```
Define → Models → Species → Reactions → Edit
Reaction: TG + 3 MeOH → 3 FAME + GL
Rate Exponent: User-Defined
UDF: transesterification_rate_1step::libudf
```

---

## 10. Energía (Thermal Model)

### 10.1 Activación del Modelo de Energía

```
Models → Energy: ON
```

### 10.2 Calor de Reacción

Transesterificación es ligeramente exotérmica:
```
ΔH_r ≈ -80 kJ/mol (TG converted)
```

**Generación de calor volumétrica**:
```
Q_gen = |ΔH_r| · r_TG  (W/m³)
```

**Implementación en UDF**:
```c
DEFINE_SOURCE(reaction_heat_source, c, t, dS, eqn)
{
    real source, rate_TG;
    real DH_r = 80000.0;  // J/mol

    // Get reaction rate from species transport
    rate_TG = get_reaction_rate(c, t, 0);  // mol/(m³·s)

    source = DH_r * (-rate_TG);  // W/m³ (heat released)

    dS[eqn] = 0.0;  // Linearization term

    return source;
}
```

### 10.3 Condiciones de Frontera Térmicas

**Paredes**:
```
CASO 1: Isothermal Wall
- T_wall = 65°C (control externo)

CASO 2: Convection
- External HTC: h_ext = 10 W/(m²·K)
- T_ambient = 25°C
- Heat flux: q = h_ext · (T_wall - T_amb)

CASO 3: Adiabatic
- q = 0 (sin intercambio de calor)
```

---

## 11. Solver Settings

### 11.1 Configuración General

```
Solver:
- Type: Pressure-Based
- Time: Steady (MRF) o Transient (Sliding Mesh)
- Velocity Formulation: Absolute
- Gravity: ON (0, -9.81, 0) m/s² [si se modela sedimentación]
```

### 11.2 Métodos Numéricos

```
Pressure-Velocity Coupling:
- Scheme: SIMPLEC (mejor convergencia que SIMPLE)
- o COUPLED (más rápido, mayor uso de memoria)

Spatial Discretization:
- Gradient: Least Squares Cell-Based
- Pressure: PRESTO! (para MRF/swirl) o Standard
- Momentum: Second Order Upwind
- Turbulence (k, ε): First Order Upwind (inicial) → Second Order
- Species: Second Order Upwind
- Energy: Second Order Upwind

Transient (si aplica):
- Time discretization: First Order Implicit
```

### 11.3 Relajación (Under-Relaxation Factors)

Para mejorar estabilidad:
```
Presión: 0.3
Densidad: 0.8 (si variable)
Fuerzas de cuerpo: 0.8
Momento: 0.5
k: 0.5
ε: 0.5
Energía: 0.9
Especies: 0.8
```

### 11.4 Criterios de Convergencia

```
Residuales:
- Continuidad: < 1e-4
- Velocidades (x, y, z): < 1e-4
- k, ε: < 1e-4
- Energía: < 1e-6
- Especies: < 1e-6

Monitoreo adicional:
- Consumo de potencia del impulsor (estable)
- Torque en el eje (variación < 1%)
- Concentración promedio de TG (si steady, debe converger)
```

### 11.5 Inicialización

```
Method: Hybrid Initialization (recomendado)
o Standard Initialization from: rotating zone

Valores iniciales:
- Velocidad: 0 m/s (o partir de solución previa)
- Presión: Gauge 0 Pa
- Temperatura: 65°C (338 K)
- Y_TG: 0.70
- Y_MeOH: 0.27
- Y_otros: 0.03
```

---

## 12. Time-Step (Transient)

Si se usa Sliding Mesh:

```
Time-step: Δt = 1 / (6 · N)  [60-120 time-steps por revolución]

Ejemplo (500 rpm):
N = 500/60 = 8.33 rps
Δt = 1 / (6 × 8.33) = 0.02 s  (60 time-steps/rev)

Iteraciones por time-step: 20-30 (hasta convergencia de residuales)

Tiempo total de simulación:
- 5-10 revoluciones para alcanzar quasi-steady state
- t_sim = 5/N = 5/8.33 = 0.6 s → 30 time-steps
```

**Courant number**:
```
CFL = u·Δt / Δx < 1
Verificar en regiones de alta velocidad (tip del impulsor)
```

---

## 13. Post-Procesamiento

### 13.1 Campos a Extraer

1. **Velocidad**:
   - Vectores de velocidad (planos XY, XZ)
   - Contornos de magnitud de velocidad
   - Streamlines (líneas de corriente)
   - Patrones de recirculación

2. **Concentraciones**:
   - Contornos de C_TG, C_FAME, C_MeOH
   - Identificar zonas de baja conversión
   - Distribución de catalizador (si multifásico)

3. **Temperatura**:
   - Contornos de T
   - Identificar hot spots (si reacción exotérmica)

4. **Turbulencia**:
   - k (energía cinética turbulenta)
   - ε (dissipation rate)
   - μ_t (viscosidad turbulenta)
   - Shear rate (γ̇ = ∂u/∂y)

5. **Consumo de Potencia**:
   ```
   Power = Torque × ω
   Torque: integrar τ_w sobre superficie del impulsor
   ```

### 13.2 Planos de Corte Recomendados

- **XY (horizontal)**: z = C (altura del impulsor)
- **XZ (vertical)**: y = 0 (pasa por eje central)
- **YZ (vertical)**: x = 0 (perpendicular a un baffle)

### 13.3 Volúmenes de Control

Calcular promedios:
```
C_TG_avg = (1/V) ∫ C_TG dV
T_avg = (1/V) ∫ T dV
```

### 13.4 Tiempo de Mezcla (Mixing Time)

Simular inyección de trazador inerte:
```
Setup:
- Patch: región pequeña con trazador (C_tracer = 1 mol/m³)
- Ejecutar transient
- Medir tiempo hasta que CoV < 5%

CoV = σ(C_tracer) / C_avg × 100%
```

### 13.5 Exportación de Datos

```
File → Export → Solution Data
- Format: ASCII, Tecplot, CSV
- Surfaces: walls, interior, planes
- Variables: velocity, pressure, species, temperature
```

---

## 14. Validación Experimental

### 14.1 Parámetros a Validar

| Parámetro | CFD | Experimental | Método Experimental |
|-----------|-----|--------------|---------------------|
| Consumo de potencia | Integrar torque | Torquímetro | P = T·ω |
| Tiempo de mezcla | Simulación trazador | Test de decoloración | Inyectar colorante |
| Distribución de velocidad | Campos CFD | PIV, LDA | Laser-based |
| Perfil de temperatura | Campos T | Termopares múltiples | Grid de sensores |
| Conversión vs tiempo | Reacción química | GC-FID | Muestreo temporal |

### 14.2 Número de Potencia (N_p)

Comparar con correlaciones:
```
Rushton Turbine (Re > 10,000):
N_p ≈ 5.0

N_p_CFD = P_CFD / (ρ · N³ · D_I⁵)
```

Error aceptable: |N_p_CFD - N_p_exp| / N_p_exp < 10%

---

## 15. Integración con PyFluent (Python)

### 15.1 Script de Automatización

```python
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

# Launch Fluent
solver = pyfluent.launch_fluent(
    precision='double',
    processor_count=4,
    mode='solver'
)

# Import mesh
solver.file.read(file_type="case", file_name="reactor_20L.cas")

# Setup models
solver.setup.models.viscous.model = "k-epsilon-rng"
solver.setup.models.energy.enabled = True
solver.setup.models.species.model = "species-transport"

# Define materials
solver.setup.materials.fluid["liquid-mixture"].density.constant = 850  # kg/m³
solver.setup.materials.fluid["liquid-mixture"].viscosity.constant = 0.003  # Pa·s

# Boundary conditions
solver.setup.boundary_conditions.wall["tank_wall"].thermal.thermal_bc = "Temperature"
solver.setup.boundary_conditions.wall["tank_wall"].thermal.t.value = 338  # K

# Cell zone conditions (rotating zone for MRF)
solver.setup.cell_zone_conditions.fluid["rotating_zone"].motion_type = "moving-reference-frame"
solver.setup.cell_zone_conditions.fluid["rotating_zone"].rotation_speed = 52.36  # rad/s (500 rpm)

# Solution methods
solver.solution.methods.p_v_coupling.flow_scheme = "simplec"
solver.solution.methods.discretization_scheme.mom = "second-order-upwind"

# Initialize
solver.solution.initialization.hybrid_initialize()

# Run calculation
solver.solution.run_calculation.iterate(number_of_iterations=2000)

# Post-processing
solver.results.graphics.contour.create("contour-velocity")
solver.results.graphics.contour["contour-velocity"].field = "velocity-magnitude"
solver.results.graphics.contour["contour-velocity"].surfaces_list = ["symmetry-plane"]
solver.results.graphics.contour["contour-velocity"].display()

# Save
solver.file.write(file_type="case-data", file_name="reactor_20L_converged.cas.h5")

# Exit
solver.exit()
```

### 15.2 Loop de Optimización

Integrar con modelo cinético Python:

```python
import numpy as np
from scipy.optimize import minimize

def run_cfd_simulation(T, rpm, cat_percent):
    """Ejecuta simulación CFD y retorna conversión"""
    solver = pyfluent.launch_fluent(...)
    # Configurar T, rpm, cat_percent
    solver.solution.run_calculation.iterate(1000)
    conversion = extract_conversion(solver)
    solver.exit()
    return conversion

def objective(x):
    T, rpm, cat = x
    conv = run_cfd_simulation(T, rpm, cat)
    return -conv  # Minimizar negativo = maximizar

# Optimización
x0 = [65, 500, 3]  # Inicial
bounds = [(50, 80), (200, 800), (1, 5)]
result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')

print(f"Condiciones óptimas: T={result.x[0]}°C, RPM={result.x[1]}, Cat={result.x[2]}%")
```

---

## 16. Checklist de Configuración

### Pre-procesamiento
- [ ] Geometría CAD creada con dimensiones correctas
- [ ] Malla generada con calidad adecuada (skewness < 0.85)
- [ ] Estudio de independencia de malla realizado
- [ ] Inflation layers configuradas (y+ adecuado)

### Setup
- [ ] Modelo de turbulencia seleccionado (k-ε RNG)
- [ ] Propiedades de fluidos definidas
- [ ] Condiciones de frontera configuradas
- [ ] MRF o Sliding Mesh configurado
- [ ] Species transport activado con reacciones
- [ ] UDF compilada y asignada
- [ ] Modelo de energía activado (si térmico)
- [ ] Gravedad activada (si multifásico)

### Solver
- [ ] Esquema de acoplamiento P-V seleccionado (SIMPLEC)
- [ ] Discretización de segundo orden configurada
- [ ] Under-relaxation factors ajustados
- [ ] Criterios de convergencia definidos
- [ ] Inicialización realizada (hybrid)

### Ejecución
- [ ] Monitoreo de residuales activo
- [ ] Monitoreo de variables físicas (P, torque)
- [ ] Guardado automático cada N iteraciones
- [ ] Convergencia alcanzada

### Post-procesamiento
- [ ] Campos de velocidad visualizados
- [ ] Perfiles de concentración extraídos
- [ ] Consumo de potencia calculado
- [ ] Tiempo de mezcla estimado (si transient)
- [ ] Resultados exportados

---

## 17. Troubleshooting

### Problema: Divergencia de la Solución

**Síntomas**: Residuales explotan, valores no físicos

**Soluciones**:
1. Reducir under-relaxation factors (0.3-0.5)
2. Usar First Order Upwind temporalmente
3. Iniciar con RPM baja, incrementar gradualmente
4. Verificar calidad de malla (refinar si skewness > 0.9)
5. Usar time-stepping pseudo-transient

### Problema: Convergencia Lenta

**Síntomas**: Residuales estancados en 1e-3

**Soluciones**:
1. Cambiar a COUPLED solver
2. Usar FMG (Full Multigrid) initialization
3. Activar PRESTO! para presión
4. Incrementar iteraciones máximas

### Problema: Resultados No Físicos (Velocidades Negativas, etc.)

**Soluciones**:
1. Verificar orientación de normales (debe apuntar hacia fluido)
2. Revisar definición de rotating zone (eje, dirección)
3. Verificar unidades en UDF (conversión min → s, kJ → J)

---

## 18. Referencias

1. **Rushton, J.H., Costich, E.W., Everett, H.J.** (1950). "Power characteristics of mixing impellers". *Chemical Engineering Progress*, 46(8), 395-404.

2. **Paul, E.L., Atiemo-Obeng, V.A., Kresta, S.M.** (2004). *Handbook of Industrial Mixing: Science and Practice*. Wiley-Interscience.

3. **Ansys Fluent Theory Guide** (2023). Chapter 4: Turbulence Models; Chapter 7: Species Transport and Finite-Rate Chemistry.

4. **Stamenkovic, O.S., et al.** (2008). "Kinetics of sunflower oil methanolysis at low temperatures". *Bioresource Technology*, 99(5), 1131-1140.

5. **Liu, X., He, H., Wang, Y., Zhu, S.** (2008). "Transesterification of soybean oil to biodiesel using CaO as a solid base catalyst". *Fuel*, 87(2), 216-221.

---

## 19. Contacto y Soporte

Para preguntas sobre esta especificación o asistencia en la implementación:

- **Documentación Ansys Fluent**: https://ansyshelp.ansys.com/
- **PyFluent Docs**: https://fluent.docs.pyansys.com/
- **Ansys Learning Forum**: https://forum.ansys.com/

---

**Documento actualizado:** 2025-11-19
**Versión:** 1.0
**Autor:** Sistema de Modelado de Esterificación
