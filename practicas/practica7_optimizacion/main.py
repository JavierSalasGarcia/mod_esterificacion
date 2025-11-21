"""
Práctica 7: Optimización de Condiciones Operacionales

Este script implementa optimización multi-criterio de condiciones
operacionales de transesterificación usando algoritmos de optimización
global (differential evolution de scipy).

Autor: Sistema de Modelado de Biodiesel
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import differential_evolution
from scipy.integrate import odeint
import os


class OptimizadorTransesterificacion:
    """Optimizador de condiciones operacionales con función objetivo multi-criterio"""

    def __init__(self, config_file='config.json'):
        """Inicializar optimizador con configuración"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # Parámetros cinéticos (desde validación Kouzu 2008)
        self.A = 2.47e11  # L³/(mol³·min)
        self.Ea = 67400   # J/mol
        self.R = 8.314    # J/(mol·K)

        # Pesos de función objetivo
        self.w_conv = self.config['funcion_objetivo']['peso_conversion']
        self.w_T = self.config['funcion_objetivo']['peso_costo_temperatura']
        self.w_MeOH = self.config['funcion_objetivo']['peso_costo_metanol']
        self.w_cat = self.config['funcion_objetivo']['peso_costo_catalizador']

        # Condiciones base para normalización
        self.T_base = self.config['condiciones_base']['temperatura_C']
        self.r_molar_base = self.config['condiciones_base']['relacion_molar']
        self.cat_base = self.config['condiciones_base']['catalizador_wt']

        # Restricciones
        self.bounds = [
            (self.config['restricciones']['temperatura_min_C'],
             self.config['restricciones']['temperatura_max_C']),
            (self.config['restricciones']['rpm_min'],
             self.config['restricciones']['rpm_max']),
            (self.config['restricciones']['catalizador_min_wt'],
             self.config['restricciones']['catalizador_max_wt']),
            (self.config['restricciones']['relacion_molar_min'],
             self.config['restricciones']['relacion_molar_max'])
        ]

        # Crear directorio de resultados
        os.makedirs('resultados', exist_ok=True)

    def sistema_edo(self, C, t, k):
        """
        Sistema de EDOs para modelo cinético de 1 paso irreversible
        TG + 3 MeOH -> 3 FAME + GL
        """
        C_TG, C_MeOH, C_FAME, C_GL = C

        # Velocidad de reacción
        r = k * C_TG * C_MeOH**3

        # Derivadas
        dTG_dt = -r
        dMeOH_dt = -3 * r
        dFAME_dt = 3 * r
        dGL_dt = r

        return [dTG_dt, dMeOH_dt, dFAME_dt, dGL_dt]

    def simular_conversion(self, T_C, relacion_molar, catalizador_wt):
        """Simular conversión para condiciones dadas"""
        # Calcular constante cinética
        T_K = T_C + 273.15
        k = self.A * np.exp(-self.Ea / (self.R * T_K))

        # Efecto del catalizador (proporcional a concentración)
        k_efectiva = k * catalizador_wt

        # Concentraciones iniciales (mol/L)
        # Aceite: 807.3 g/mol, densidad 0.92 g/mL
        C_TG_0 = (0.92 * 1000) / 807.3  # ~1.14 mol/L

        # Metanol: 32.04 g/mol, densidad 0.792 g/mL
        C_MeOH_0 = relacion_molar * 3 * C_TG_0  # Estequiometría TG:MeOH = 1:3

        C_FAME_0 = 0.0
        C_GL_0 = 0.0

        C0 = [C_TG_0, C_MeOH_0, C_FAME_0, C_GL_0]

        # Integrar EDOs (60 min)
        t = np.linspace(0, 60, 100)
        sol = odeint(self.sistema_edo, C0, t, args=(k_efectiva,),
                     rtol=1e-6, atol=1e-9)

        # Conversión final
        C_TG_final = sol[-1, 0]
        conversion = (C_TG_0 - C_TG_final) / C_TG_0 * 100

        return conversion

    def funcion_objetivo(self, x):
        """
        Función objetivo multi-criterio para maximizar

        Score = w1*Conversion - w2*Costo_T - w3*Costo_MeOH - w4*Costo_Cat

        Nota: differential_evolution MINIMIZA, por lo que retornamos -Score
        """
        T_C, rpm, catalizador_wt, relacion_molar = x

        # Simular conversión
        try:
            conversion = self.simular_conversion(T_C, relacion_molar, catalizador_wt)
        except:
            return 1e10  # Penalización por fallo

        # Normalizar costos
        costo_T = (T_C - self.T_base) / (70 - self.T_base)  # Normalizado 0-1
        costo_MeOH = (relacion_molar - self.r_molar_base) / (12 - self.r_molar_base)
        costo_cat = (catalizador_wt - self.cat_base) / (2.0 - self.cat_base)

        # Score (convertir conversión de 0-100 a 0-1)
        score = (self.w_conv * conversion / 100 -
                 self.w_T * max(0, costo_T) -
                 self.w_MeOH * max(0, costo_MeOH) -
                 self.w_cat * max(0, costo_cat))

        # Retornar negativo para minimización
        return -score

    def optimizar(self):
        """Ejecutar optimización global"""
        print("=" * 60)
        print("OPTIMIZACIÓN DE CONDICIONES OPERACIONALES")
        print("=" * 60)
        print(f"\nPesos de función objetivo:")
        print(f"  - Conversión:        {self.w_conv:.2f}")
        print(f"  - Costo temperatura: {self.w_T:.2f}")
        print(f"  - Costo metanol:     {self.w_MeOH:.2f}")
        print(f"  - Costo catalizador: {self.w_cat:.2f}")

        print(f"\nEjecutando optimización...")

        resultado = differential_evolution(
            self.funcion_objetivo,
            self.bounds,
            maxiter=self.config['algoritmo']['max_iteraciones'],
            popsize=self.config['algoritmo']['poblacion'],
            tol=self.config['algoritmo']['tolerancia'],
            seed=42,
            disp=True
        )

        T_opt, rpm_opt, cat_opt, r_molar_opt = resultado.x
        score_opt = -resultado.fun

        # Calcular conversión óptima
        conv_opt = self.simular_conversion(T_opt, r_molar_opt, cat_opt)

        print("\n" + "=" * 60)
        print("CONDICIONES ÓPTIMAS ENCONTRADAS")
        print("=" * 60)
        print(f"Temperatura:       {T_opt:.1f} °C")
        print(f"Agitación:         {rpm_opt:.0f} rpm")
        print(f"Catalizador:       {cat_opt:.2f} % (m/m)")
        print(f"Relación molar:    {r_molar_opt:.1f}:1")
        print(f"\nConversión:        {conv_opt:.2f} %")
        print(f"Score multi-crit:  {score_opt:.4f}")
        print("=" * 60)

        # Guardar resultados
        resultados = {
            'temperatura_C': float(T_opt),
            'rpm': float(rpm_opt),
            'catalizador_wt': float(cat_opt),
            'relacion_molar': float(r_molar_opt),
            'conversion_pct': float(conv_opt),
            'score': float(score_opt),
            'pesos_usados': {
                'w_conversion': self.w_conv,
                'w_temperatura': self.w_T,
                'w_metanol': self.w_MeOH,
                'w_catalizador': self.w_cat
            }
        }

        with open('resultados/condiciones_optimas.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)

        return T_opt, rpm_opt, cat_opt, r_molar_opt, conv_opt, score_opt

    def generar_superficies_respuesta(self, T_opt, r_molar_opt):
        """Generar superficies de respuesta 3D"""
        print("\nGenerando superficies de respuesta 3D...")

        # Grid de parámetros
        T_range = np.linspace(50, 70, 20)
        r_molar_range = np.linspace(3, 12, 20)
        T_grid, R_grid = np.meshgrid(T_range, r_molar_range)

        # Calcular conversiones (catalizador fijo en 1.0%)
        Conv_grid = np.zeros_like(T_grid)
        for i in range(len(r_molar_range)):
            for j in range(len(T_range)):
                Conv_grid[i, j] = self.simular_conversion(
                    T_grid[i, j], R_grid[i, j], 1.0
                )

        # Crear figura con 2 subplots
        fig = plt.figure(figsize=(14, 6))

        # Subplot 1: Superficie 3D
        ax1 = fig.add_subplot(121, projection='3d')
        surf = ax1.plot_surface(T_grid, R_grid, Conv_grid, cmap='viridis',
                                alpha=0.9, edgecolor='none')
        ax1.scatter([T_opt], [r_molar_opt], [self.simular_conversion(T_opt, r_molar_opt, 1.0)],
                   color='red', s=100, marker='*', label='Óptimo')
        ax1.set_xlabel('Temperatura (°C)')
        ax1.set_ylabel('Relación Molar')
        ax1.set_zlabel('Conversión (%)')
        ax1.set_title('Superficie de Respuesta 3D')
        ax1.legend()
        plt.colorbar(surf, ax=ax1, shrink=0.5)

        # Subplot 2: Contornos 2D
        ax2 = fig.add_subplot(122)
        contour = ax2.contourf(T_grid, R_grid, Conv_grid, levels=15, cmap='viridis')
        contour_lines = ax2.contour(T_grid, R_grid, Conv_grid, levels=[90, 95, 98],
                                     colors='white', linewidths=2)
        ax2.clabel(contour_lines, inline=True, fontsize=10, fmt='%0.0f%%')
        ax2.scatter([T_opt], [r_molar_opt], color='red', s=100, marker='*',
                   label='Óptimo', zorder=5)
        ax2.set_xlabel('Temperatura (°C)')
        ax2.set_ylabel('Relación Molar')
        ax2.set_title('Mapa de Contorno de Conversión')
        ax2.legend()
        plt.colorbar(contour, ax=ax2)

        plt.tight_layout()
        plt.savefig('resultados/superficie_respuesta.png', dpi=150)
        print("  ✓ Guardado: resultados/superficie_respuesta.png")

    def analisis_sensibilidad_pesos(self):
        """Analizar cómo cambian las condiciones óptimas al variar pesos"""
        print("\nAnalizando sensibilidad a pesos de función objetivo...")

        # Probar diferentes combinaciones de pesos
        configuraciones = [
            {'nombre': 'Caso base', 'w_conv': 1.0, 'w_T': 0.3, 'w_MeOH': 0.2, 'w_cat': 0.1},
            {'nombre': 'Max conversión', 'w_conv': 2.0, 'w_T': 0.1, 'w_MeOH': 0.1, 'w_cat': 0.1},
            {'nombre': 'Min costos', 'w_conv': 1.0, 'w_T': 0.5, 'w_MeOH': 0.4, 'w_cat': 0.3},
            {'nombre': 'Balanceado', 'w_conv': 1.0, 'w_T': 1.0, 'w_MeOH': 1.0, 'w_cat': 1.0}
        ]

        resultados_sensibilidad = []

        for conf in configuraciones:
            # Actualizar pesos temporalmente
            self.w_conv = conf['w_conv']
            self.w_T = conf['w_T']
            self.w_MeOH = conf['w_MeOH']
            self.w_cat = conf['w_cat']

            # Optimizar
            resultado = differential_evolution(
                self.funcion_objetivo,
                self.bounds,
                maxiter=50,
                popsize=10,
                seed=42,
                disp=False
            )

            T_opt, rpm_opt, cat_opt, r_molar_opt = resultado.x
            conv_opt = self.simular_conversion(T_opt, r_molar_opt, cat_opt)

            resultados_sensibilidad.append({
                'nombre': conf['nombre'],
                'T': T_opt,
                'relacion_molar': r_molar_opt,
                'catalizador': cat_opt,
                'conversion': conv_opt
            })

            print(f"  {conf['nombre']:15s}: T={T_opt:.1f}°C, r={r_molar_opt:.1f}:1, "
                  f"cat={cat_opt:.2f}%, conv={conv_opt:.1f}%")

        # Graficar comparación
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        nombres = [r['nombre'] for r in resultados_sensibilidad]

        # Temperatura
        axes[0, 0].bar(nombres, [r['T'] for r in resultados_sensibilidad], color='coral')
        axes[0, 0].set_ylabel('Temperatura (°C)')
        axes[0, 0].set_title('Temperatura Óptima')
        axes[0, 0].tick_params(axis='x', rotation=45)

        # Relación molar
        axes[0, 1].bar(nombres, [r['relacion_molar'] for r in resultados_sensibilidad], color='skyblue')
        axes[0, 1].set_ylabel('Relación Molar')
        axes[0, 1].set_title('Relación Molar Óptima')
        axes[0, 1].tick_params(axis='x', rotation=45)

        # Catalizador
        axes[1, 0].bar(nombres, [r['catalizador'] for r in resultados_sensibilidad], color='lightgreen')
        axes[1, 0].set_ylabel('Catalizador (% m/m)')
        axes[1, 0].set_title('Concentración de Catalizador Óptima')
        axes[1, 0].tick_params(axis='x', rotation=45)

        # Conversión
        axes[1, 1].bar(nombres, [r['conversion'] for r in resultados_sensibilidad], color='gold')
        axes[1, 1].set_ylabel('Conversión (%)')
        axes[1, 1].set_title('Conversión Alcanzada')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].axhline(y=95, color='red', linestyle='--', label='Especificación')
        axes[1, 1].legend()

        plt.tight_layout()
        plt.savefig('resultados/sensibilidad_pesos.png', dpi=150)
        print("  ✓ Guardado: resultados/sensibilidad_pesos.png")


def main():
    """Función principal"""
    # Inicializar optimizador
    opt = OptimizadorTransesterificacion()

    # Ejecutar optimización
    T_opt, rpm_opt, cat_opt, r_molar_opt, conv_opt, score_opt = opt.optimizar()

    # Generar superficies de respuesta
    opt.generar_superficies_respuesta(T_opt, r_molar_opt)

    # Análisis de sensibilidad a pesos
    opt.analisis_sensibilidad_pesos()

    print("\n" + "=" * 60)
    print("ANÁLISIS COMPLETADO")
    print("=" * 60)
    print("\nArchivos generados:")
    print("  - resultados/condiciones_optimas.json")
    print("  - resultados/superficie_respuesta.png")
    print("  - resultados/sensibilidad_pesos.png")
    print("\nRevisa el archivo analisis.md para responder las preguntas.")
    print("=" * 60)


if __name__ == "__main__":
    main()
