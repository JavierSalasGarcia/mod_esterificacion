/**
 * UDF (User Defined Function) para Ansys Fluent
 *
 * Cinética de Transesterificación de Aceites Vegetales
 * Modelo de 3 pasos reversibles con catálisis básica homogénea
 *
 * Reacciones:
 * 1. TG + MeOH <-> DG + FAME
 * 2. DG + MeOH <-> MG + FAME
 * 3. MG + MeOH <-> GL + FAME
 *
 * Autor: Sistema de Modelado de Biodiesel
 * Fecha: 2024
 * Versión compatible: Ansys Fluent 2023 R1 y superior
 */

#include "udf.h"

/* ========================================================================== */
/* PARÁMETROS CINÉTICOS                                                       */
/* ========================================================================== */

/* Constantes de Arrhenius para reacciones directas */
#define A1_FORWARD  8.4e4    /* L/(mol·s) */
#define EA1_FORWARD 55.3     /* kJ/mol */

#define A2_FORWARD  1.2e5    /* L/(mol·s) */
#define EA2_FORWARD 58.7     /* kJ/mol */

#define A3_FORWARD  2.1e5    /* L/(mol·s) */
#define EA3_FORWARD 62.1     /* kJ/mol */

/* Constantes de Arrhenius para reacciones reversas */
#define A1_REVERSE  1.2e4    /* L/(mol·s) */
#define EA1_REVERSE 50.0     /* kJ/mol */

#define A2_REVERSE  8.0e3    /* L/(mol·s) */
#define EA2_REVERSE 48.5     /* kJ/mol */

#define A3_REVERSE  5.5e3    /* L/(mol·s) */
#define EA3_REVERSE 46.2     /* kJ/mol */

/* Constante de gases */
#define R_GAS 8.314          /* J/(mol·K) */

/* ========================================================================== */
/* ÍNDICES DE ESPECIES                                                        */
/* ========================================================================== */
/* NOTA: Estos índices deben coincidir con el orden de especies en Fluent   */
/*       Verificar en: Setup > Species > Edit...                             */

#define ID_TG     0          /* Triglicérido */
#define ID_MEOH   1          /* Metanol */
#define ID_DG     2          /* Diglicérido */
#define ID_MG     3          /* Monoglicérido */
#define ID_FAME   4          /* Ésteres metílicos (biodiesel) */
#define ID_GL     5          /* Glicerol */

/* ========================================================================== */
/* FUNCIONES AUXILIARES                                                       */
/* ========================================================================== */

/**
 * Calcular constante de velocidad usando ecuación de Arrhenius
 * k = A * exp(-Ea / (R * T))
 *
 * @param A   Factor preexponencial [L/(mol·s)]
 * @param Ea  Energía de activación [kJ/mol]
 * @param T   Temperatura [K]
 * @return    Constante de velocidad [L/(mol·s)]
 */
static real calcular_k_arrhenius(real A, real Ea, real T)
{
    real Ea_J_mol = Ea * 1000.0;  /* Convertir kJ/mol a J/mol */
    real k = A * exp(-Ea_J_mol / (R_GAS * T));
    return k;
}

/* ========================================================================== */
/* UDF PRINCIPAL: TASA DE REACCIÓN                                            */
/* ========================================================================== */

/**
 * UDF para calcular tasas de reacción volumétricas (términos fuente)
 * Esta función se llama para cada celda del dominio en cada iteración
 *
 * DEFINE_SOURCE(nombre_udf, celda, hilo, dS, eqn)
 * - nombre_udf: nombre de la UDF
 * - celda: índice de la celda actual
 * - hilo: puntero al hilo (thread) actual
 * - dS: derivada del término fuente respecto a la variable (para linealización)
 * - eqn: índice de la ecuación (especie)
 *
 * @return Tasa de generación/consumo [kg/(m³·s)]
 */
DEFINE_SOURCE(source_transesterification, cell, thread, dS, eqn)
{
    real source = 0.0;
    real T, rho;
    real C_TG, C_MeOH, C_DG, C_MG, C_FAME, C_GL;
    real k1f, k1r, k2f, k2r, k3f, k3r;
    real r1, r2, r3;
    real MW_TG, MW_MeOH, MW_DG, MW_MG, MW_FAME, MW_GL;

    /* -------------------------------------------------------------------- */
    /* 1. OBTENER PROPIEDADES DE LA CELDA                                   */
    /* -------------------------------------------------------------------- */

    /* Temperatura de la celda [K] */
    T = C_T(cell, thread);

    /* Densidad de la mezcla [kg/m³] */
    rho = C_R(cell, thread);

    /* -------------------------------------------------------------------- */
    /* 2. OBTENER FRACCIONES MÁSICAS Y CALCULAR CONCENTRACIONES            */
    /* -------------------------------------------------------------------- */

    /* Masas molares [kg/mol] */
    MW_TG   = 0.8073;  /* ~807.3 g/mol */
    MW_MeOH = 0.03204; /* 32.04 g/mol */
    MW_DG   = 0.6047;  /* ~604.7 g/mol */
    MW_MG   = 0.4020;  /* ~402.0 g/mol */
    MW_FAME = 0.2946;  /* ~294.6 g/mol (oleato de metilo) */
    MW_GL   = 0.09209; /* 92.09 g/mol */

    /* Fracciones másicas Yi [-] */
    real Y_TG   = C_YI(cell, thread, ID_TG);
    real Y_MeOH = C_YI(cell, thread, ID_MEOH);
    real Y_DG   = C_YI(cell, thread, ID_DG);
    real Y_MG   = C_YI(cell, thread, ID_MG);
    real Y_FAME = C_YI(cell, thread, ID_FAME);
    real Y_GL   = C_YI(cell, thread, ID_GL);

    /* Concentraciones molares Ci = (rho * Yi) / MWi [kmol/m³] = [mol/L] */
    C_TG   = (rho * Y_TG)   / MW_TG;
    C_MeOH = (rho * Y_MeOH) / MW_MeOH;
    C_DG   = (rho * Y_DG)   / MW_DG;
    C_MG   = (rho * Y_MG)   / MW_MG;
    C_FAME = (rho * Y_FAME) / MW_FAME;
    C_GL   = (rho * Y_GL)   / MW_GL;

    /* -------------------------------------------------------------------- */
    /* 3. CALCULAR CONSTANTES DE VELOCIDAD                                  */
    /* -------------------------------------------------------------------- */

    k1f = calcular_k_arrhenius(A1_FORWARD, EA1_FORWARD, T);
    k1r = calcular_k_arrhenius(A1_REVERSE, EA1_REVERSE, T);

    k2f = calcular_k_arrhenius(A2_FORWARD, EA2_FORWARD, T);
    k2r = calcular_k_arrhenius(A2_REVERSE, EA2_REVERSE, T);

    k3f = calcular_k_arrhenius(A3_FORWARD, EA3_FORWARD, T);
    k3r = calcular_k_arrhenius(A3_REVERSE, EA3_REVERSE, T);

    /* -------------------------------------------------------------------- */
    /* 4. CALCULAR TASAS DE REACCIÓN                                        */
    /* -------------------------------------------------------------------- */

    /* Reacción 1: TG + MeOH <-> DG + FAME */
    r1 = k1f * C_TG * C_MeOH - k1r * C_DG * C_FAME;

    /* Reacción 2: DG + MeOH <-> MG + FAME */
    r2 = k2f * C_DG * C_MeOH - k2r * C_MG * C_FAME;

    /* Reacción 3: MG + MeOH <-> GL + FAME */
    r3 = k3f * C_MG * C_MeOH - k3r * C_GL * C_FAME;

    /* -------------------------------------------------------------------- */
    /* 5. CALCULAR TÉRMINO FUENTE PARA LA ESPECIE ACTUAL                    */
    /* -------------------------------------------------------------------- */

    /* Balance estequiométrico para cada especie [mol/(L·s)] */
    real rate_mol_per_Ls = 0.0;

    switch(eqn) {
        case ID_TG:
            /* TG se consume en reacción 1 */
            rate_mol_per_Ls = -r1;
            break;

        case ID_MEOH:
            /* MeOH se consume en las tres reacciones */
            rate_mol_per_Ls = -r1 - r2 - r3;
            break;

        case ID_DG:
            /* DG se produce en reacción 1, se consume en reacción 2 */
            rate_mol_per_Ls = r1 - r2;
            break;

        case ID_MG:
            /* MG se produce en reacción 2, se consume en reacción 3 */
            rate_mol_per_Ls = r2 - r3;
            break;

        case ID_FAME:
            /* FAME se produce en las tres reacciones */
            rate_mol_per_Ls = r1 + r2 + r3;
            break;

        case ID_GL:
            /* GL se produce en reacción 3 */
            rate_mol_per_Ls = r3;
            break;

        default:
            rate_mol_per_Ls = 0.0;
            break;
    }

    /* Convertir de [mol/(L·s)] a [kg/(m³·s)] */
    /* mol/(L·s) × kg/mol × 1000 L/m³ = kg/(m³·s) */
    real MW_species;
    switch(eqn) {
        case ID_TG:   MW_species = MW_TG;   break;
        case ID_MEOH: MW_species = MW_MeOH; break;
        case ID_DG:   MW_species = MW_DG;   break;
        case ID_MG:   MW_species = MW_MG;   break;
        case ID_FAME: MW_species = MW_FAME; break;
        case ID_GL:   MW_species = MW_GL;   break;
        default:      MW_species = 1.0;     break;
    }

    source = rate_mol_per_Ls * MW_species * 1000.0;  /* [kg/(m³·s)] */

    /* -------------------------------------------------------------------- */
    /* 6. DERIVADA PARA LINEALIZACIÓN (OPCIONAL PERO RECOMENDADO)          */
    /* -------------------------------------------------------------------- */

    /* Para mejor convergencia, proporcionar derivada del término fuente
     * respecto a la fracción másica de la especie actual.
     * Aquí usamos una aproximación simple: dS = 0 */
    dS[eqn] = 0.0;

    return source;
}

/* ========================================================================== */
/* UDF OPCIONAL: CALOR DE REACCIÓN                                           */
/* ========================================================================== */

/**
 * UDF para agregar términos fuente de energía debido a reacciones exotérmicas
 * La transesterificación es ligeramente exotérmica (~15 kJ/mol)
 *
 * NOTA: Esta UDF es opcional. Activar solo si se desea considerar
 *       el efecto térmico de las reacciones.
 */
DEFINE_SOURCE(source_heat_reaction, cell, thread, dS, eqn)
{
    real Q_source = 0.0;
    real T, rho;
    real C_TG, C_MeOH;
    real k1f;
    real r1;
    real DH_rxn = -15000.0;  /* Entalpía de reacción: -15 kJ/mol (exotérmica) */

    /* Obtener temperatura y densidad */
    T = C_T(cell, thread);
    rho = C_R(cell, thread);

    /* Calcular concentraciones (simplificado) */
    real MW_TG = 0.8073;
    real MW_MeOH = 0.03204;
    real Y_TG = C_YI(cell, thread, ID_TG);
    real Y_MeOH = C_YI(cell, thread, ID_MEOH);
    C_TG = (rho * Y_TG) / MW_TG;
    C_MeOH = (rho * Y_MeOH) / MW_MeOH;

    /* Calcular constante cinética */
    k1f = calcular_k_arrhenius(A1_FORWARD, EA1_FORWARD, T);

    /* Calcular tasa de reacción global (aproximada por reacción 1) */
    r1 = k1f * C_TG * C_MeOH;  /* [mol/(L·s)] */

    /* Convertir a calor liberado [W/m³] = [J/(m³·s)] */
    /* mol/(L·s) × J/mol × 1000 L/m³ = J/(m³·s) = W/m³ */
    Q_source = -r1 * DH_rxn * 1000.0;  /* Negativo porque DH_rxn < 0 */

    dS[eqn] = 0.0;

    return Q_source;
}

/* ========================================================================== */
/* FIN DEL ARCHIVO UDF                                                        */
/* ========================================================================== */

/**
 * INSTRUCCIONES DE USO EN ANSYS FLUENT:
 *
 * 1. Compilar la UDF:
 *    Define > User-Defined > Functions > Compiled...
 *    - Seleccionar este archivo .c
 *    - Build
 *
 * 2. Configurar especies:
 *    Setup > Models > Species > Species Transport
 *    - Activar "Species Transport"
 *    - Crear 6 especies: TG, MeOH, DG, MG, FAME, GL
 *    - Orden DEBE coincidir con índices definidos arriba
 *
 * 3. Asignar términos fuente:
 *    Setup > Cell Zone Conditions > [zona_fluido] > Edit...
 *    - Source Terms > [cada especie] > source_transesterification
 *    - (Opcional) Energy > source_heat_reaction
 *
 * 4. Condiciones iniciales:
 *    Setup > Cell Zone Conditions > [zona_fluido] > Edit...
 *    - Temperatura: 333 K (60°C)
 *    - Fracciones másicas iniciales:
 *      * Y_TG = 0.75
 *      * Y_MeOH = 0.25
 *      * Demás = 0.0
 *
 * 5. Ejecutar simulación transitoria:
 *    Run > Run Calculation
 *    - Time Step Size: 1 s
 *    - Number of Time Steps: 3600 (1 hora)
 *
 * 6. Postprocesar:
 *    Results > Graphics > Contours...
 *    - Variables: Species > Y_FAME, Y_TG, etc.
 *    - Planos de corte en diferentes alturas
 */
