/*
 * UDF para Ansys Fluent: Cinética de Transesterificación
 * Modelo: 1-paso pseudo-homogéneo
 * Reacción: TG + 3 MeOH -> 3 FAME + GL
 */

#include "udf.h"

/* Parametros cineticos (de Práctica 6) */
#define A_FORWARD 2.98e10    /* min^-1 */
#define EA_FORWARD 51900.0   /* J/mol */
#define R_GAS 8.314          /* J/(mol*K) */

/* Indices de especies (configurar en Fluent) */
#define I_TG 0
#define I_MEOH 1
#define I_FAME 2
#define I_GL 3

DEFINE_VR_RATE(transesterification_rate, c, t, r, mw, yi, rr, rr_t)
{
    real T = C_T(c,t);              /* Temperatura (K) */
    real rho = C_R(c,t);            /* Densidad (kg/m3) */
    
    /* Concentraciones molares (mol/m3) */
    real C_TG = rho * yi[I_TG][0] / mw[I_TG] * 1000.0;
    real C_MeOH = rho * yi[I_MEOH][0] / mw[I_MEOH] * 1000.0;
    
    /* Constante de velocidad (Arrhenius) */
    real k = A_FORWARD * exp(-EA_FORWARD / (R_GAS * T));
    
    /* Velocidad de reacción (mol/(m3*s)) */
    real rate = k * C_TG * C_MeOH;  /* r = k*[TG]*[MeOH] */
    
    /* Convertir de mol/(m3*s) a kg/(m3*s) */
    *rr = rate / 60.0;  /* Convertir min^-1 a s^-1 */
    
    /* Coeficientes estequiométricos */
    rr[I_TG] = -1.0 * (*rr) * mw[I_TG] / 1000.0;
    rr[I_MEOH] = -3.0 * (*rr) * mw[I_MEOH] / 1000.0;
    rr[I_FAME] = 3.0 * (*rr) * mw[I_FAME] / 1000.0;
    rr[I_GL] = 1.0 * (*rr) * mw[I_GL] / 1000.0;
}

/* UDF para inicialización de especies */
DEFINE_INIT(init_species, d)
{
    cell_t c;
    Thread *t;
    
    thread_loop_c(t, d)
    {
        begin_c_loop(c, t)
        {
            /* Fracciones másicas iniciales */
            C_YI(c,t,I_TG) = 0.5;      /* TG */
            C_YI(c,t,I_MEOH) = 0.45;   /* MeOH */
            C_YI(c,t,I_FAME) = 0.0;    /* FAME */
            C_YI(c,t,I_GL) = 0.05;     /* GL */
        }
        end_c_loop(c, t)
    }
}
