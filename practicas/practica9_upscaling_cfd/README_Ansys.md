# Guía para Configurar en Ansys Fluent

## 1. Importar Geometría
- File > Import > STEP
- Seleccionar `reactor_20L.step`

## 2. Mallado (Ansys Meshing)
- Tipo: Tetrahedros + capa de prismas en paredes
- Tamaño global: 5 mm
- Refinamiento en ribbon impeller: 2 mm
- Capa límite: 5 capas, ratio 1.2
- **Total estimado**: ~300k celdas (compatible con versión Student)

## 3. Setup en Fluent

### Models
- Turbulence: k-epsilon RNG, Enhanced Wall Treatment
- Energy: ON
- Species: Species Transport (4 especies)
- Reacción: Volumetric (User-Defined)

### Materials
- Crear especies: TG, MeOH, FAME, GL
- Mezcla: propiedades de config.json

### Cell Zone Conditions
- Fluid: Mezcla reactiva
- Frame Motion: Rotating (MRF)
  - Axis: (0, 0, 1)
  - RPM: [valor de parte_A_escalado]

### Boundary Conditions
- Paredes: No-slip, adiabático
- Serpentín: Pared con T constante (65 C)

### Solution Methods
- Scheme: SIMPLE
- Discretization: Second Order Upwind

### UDF
- Compilar `parte_D_udf_cinetica.c`
- Asignar a Reaction Rate

## 4. Ejecutar
- Inicializar
- Iterar: 1000-2000 iteraciones
- Monitorear residuos (< 1e-4)

## 5. Post-Processing
- Contornos: velocidad, temperatura, fracciones másicas
- Streamlines: patrones de flujo
- Iso-surfaces: conversión = 50%, 75%, 90%
