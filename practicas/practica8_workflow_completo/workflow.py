"""
Práctica 8: Workflow Completo de Análisis de Transesterificación

Este script integra todos los módulos del sistema en un pipeline automatizado:
Paso 1: Procesamiento de datos GC-FID
Paso 2: Ajuste de parámetros cinéticos
Paso 3: Optimización de condiciones operacionales
Paso 4: Generación de reporte HTML interactivo

Autor: Sistema de Modelado de Biodiesel
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.integrate import odeint
from scipy.optimize import differential_evolution, minimize
from lmfit import minimize as lmfit_minimize, Parameters
import os
from datetime import datetime


class WorkflowCompleto:
    """Pipeline completo de análisis de transesterificación"""

    def __init__(self, config_file='config.json'):
        """Inicializar workflow con configuración"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.resultados = {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Crear directorios
        os.makedirs('resultados', exist_ok=True)
        os.makedirs('resultados/graficas', exist_ok=True)

        print("=" * 70)
        print(" " * 15 + "WORKFLOW COMPLETO DE TRANSESTERIFICACIÓN")
        print("=" * 70)
        print(f"Timestamp: {self.timestamp}\n")

    def paso1_procesamiento_gc(self):
        """Paso 1: Procesar datos de cromatografía de gases"""
        print("\n" + "=" * 70)
        print("PASO 1: PROCESAMIENTO DE DATOS GC-FID")
        print("=" * 70)

        # Cargar datos
        archivo = os.path.join('datos', self.config['paso1_procesamiento_gc']['archivo_datos'])
        df = pd.read_csv(archivo)

        print(f"✓ Datos cargados: {len(df)} puntos temporales")

        # Factores de respuesta
        FR_TG = self.config['paso1_procesamiento_gc']['factores_respuesta']['FR_TG']
        FR_FAME = self.config['paso1_procesamiento_gc']['factores_respuesta']['FR_FAME']
        FR_GL = self.config['paso1_procesamiento_gc']['factores_respuesta']['FR_GL']
        C_IS = self.config['paso1_procesamiento_gc']['concentracion_IS_mol_L']

        # Calcular concentraciones usando método de estándar interno
        df['C_TG_mol_L'] = (df['area_TG'] / df['area_IS']) * FR_TG * C_IS
        df['C_FAME_mol_L'] = (df['area_FAME'] / df['area_IS']) * FR_FAME * C_IS
        df['C_GL_mol_L'] = (df['area_GL'] / df['area_IS']) * FR_GL * C_IS

        # Calcular conversión
        C_TG_inicial = df['C_TG_mol_L'].iloc[0]
        df['conversion_pct'] = (1 - df['C_TG_mol_L'] / C_TG_inicial) * 100

        print(f"✓ Concentraciones calculadas")
        print(f"  - C_TG inicial: {C_TG_inicial:.3f} mol/L")
        print(f"  - Conversión final: {df['conversion_pct'].iloc[-1]:.2f} %")

        # Guardar datos procesados
        df.to_csv('resultados/datos_procesados.csv', index=False)

        # Graficar
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Subplot 1: Concentraciones
        axes[0].plot(df['tiempo_min'], df['C_TG_mol_L'], 'o-', label='TG', color='red')
        axes[0].plot(df['tiempo_min'], df['C_FAME_mol_L'], 's-', label='FAME', color='blue')
        axes[0].plot(df['tiempo_min'], df['C_GL_mol_L'], '^-', label='GL', color='green')
        axes[0].set_xlabel('Tiempo (min)')
        axes[0].set_ylabel('Concentración (mol/L)')
        axes[0].set_title('Evolución de Concentraciones')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Subplot 2: Conversión
        axes[1].plot(df['tiempo_min'], df['conversion_pct'], 'o-', color='purple', linewidth=2)
        axes[1].axhline(y=96.5, color='red', linestyle='--', label='Especificación EN 14214')
        axes[1].set_xlabel('Tiempo (min)')
        axes[1].set_ylabel('Conversión (%)')
        axes[1].set_title('Conversión de Triglicéridos')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('resultados/graficas/paso1_procesamiento_gc.png', dpi=150)
        print(f"✓ Gráfica guardada: resultados/graficas/paso1_procesamiento_gc.png")

        self.resultados['paso1'] = {
            'datos_procesados': df.to_dict('records'),
            'conversion_final': float(df['conversion_pct'].iloc[-1])
        }

        return df

    def paso2_ajuste_parametros(self, df):
        """Paso 2: Ajustar parámetros cinéticos A y Ea"""
        print("\n" + "=" * 70)
        print("PASO 2: AJUSTE DE PARÁMETROS CINÉTICOS")
        print("=" * 70)

        # Extraer datos experimentales
        t_exp = df['tiempo_min'].values
        C_TG_exp = df['C_TG_mol_L'].values
        T_C = df['temperatura_C'].iloc[0]

        # Sistema de EDOs
        def sistema_edo(C, t, A, Ea, T_K):
            R = 8.314
            k = A * np.exp(-Ea * 1000 / (R * T_K))

            C_TG, C_MeOH, C_FAME, C_GL = C
            r = k * C_TG * C_MeOH**3

            return [-r, -3*r, 3*r, r]

        # Función residual para lmfit
        def residual(params, t, C_TG_exp, T_K, C_MeOH_0):
            A = params['A']
            Ea = params['Ea']

            C0 = [C_TG_exp[0], C_MeOH_0, 0.0, 0.0]
            sol = odeint(sistema_edo, C0, t, args=(A, Ea, T_K))
            C_TG_modelo = sol[:, 0]

            return C_TG_modelo - C_TG_exp

        # Parámetros iniciales y límites
        params = Parameters()
        params.add('A', value=self.config['paso2_ajuste_parametros']['valores_iniciales']['A_inicial'],
                   min=self.config['paso2_ajuste_parametros']['limites']['A_min'],
                   max=self.config['paso2_ajuste_parametros']['limites']['A_max'])
        params.add('Ea', value=self.config['paso2_ajuste_parametros']['valores_iniciales']['Ea_inicial'],
                   min=self.config['paso2_ajuste_parametros']['limites']['Ea_min'],
                   max=self.config['paso2_ajuste_parametros']['limites']['Ea_max'])

        # Estimar C_MeOH inicial (relación molar 6:1)
        C_MeOH_0 = 6 * 3 * C_TG_exp[0]
        T_K = T_C + 273.15

        print("Ejecutando ajuste con lmfit...")
        resultado_ajuste = lmfit_minimize(residual, params, args=(t_exp, C_TG_exp, T_K, C_MeOH_0))

        A_ajustado = resultado_ajuste.params['A'].value
        Ea_ajustado = resultado_ajuste.params['Ea'].value

        # Calcular R² y RMSE
        C0 = [C_TG_exp[0], C_MeOH_0, 0.0, 0.0]
        sol_ajustada = odeint(sistema_edo, C0, t_exp, args=(A_ajustado, Ea_ajustado, T_K))
        C_TG_ajustado = sol_ajustada[:, 0]

        SS_res = np.sum((C_TG_exp - C_TG_ajustado)**2)
        SS_tot = np.sum((C_TG_exp - np.mean(C_TG_exp))**2)
        R2 = 1 - SS_res / SS_tot
        RMSE = np.sqrt(np.mean((C_TG_exp - C_TG_ajustado)**2))

        print(f"\n✓ Ajuste completado:")
        print(f"  - A = {A_ajustado:.2e} L³/(mol³·min)")
        print(f"  - Ea = {Ea_ajustado:.2f} kJ/mol")
        print(f"  - R² = {R2:.4f}")
        print(f"  - RMSE = {RMSE:.4f} mol/L")

        # Graficar ajuste
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Subplot 1: Datos vs Modelo
        axes[0].plot(t_exp, C_TG_exp, 'o', label='Datos experimentales', markersize=8, color='red')
        axes[0].plot(t_exp, C_TG_ajustado, '-', label='Modelo ajustado', linewidth=2, color='blue')
        axes[0].set_xlabel('Tiempo (min)')
        axes[0].set_ylabel('Concentración TG (mol/L)')
        axes[0].set_title(f'Ajuste de Parámetros (R² = {R2:.4f})')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Subplot 2: Residuales
        residuales = C_TG_exp - C_TG_ajustado
        axes[1].scatter(t_exp, residuales, color='purple', s=50)
        axes[1].axhline(y=0, color='black', linestyle='--', linewidth=1)
        axes[1].set_xlabel('Tiempo (min)')
        axes[1].set_ylabel('Residuales (mol/L)')
        axes[1].set_title('Análisis de Residuales')
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('resultados/graficas/paso2_ajuste_parametros.png', dpi=150)
        print(f"✓ Gráfica guardada: resultados/graficas/paso2_ajuste_parametros.png")

        self.resultados['paso2'] = {
            'A': float(A_ajustado),
            'Ea': float(Ea_ajustado),
            'R2': float(R2),
            'RMSE': float(RMSE)
        }

        return A_ajustado, Ea_ajustado

    def paso3_optimizacion(self, A, Ea):
        """Paso 3: Optimizar condiciones operacionales"""
        print("\n" + "=" * 70)
        print("PASO 3: OPTIMIZACIÓN DE CONDICIONES OPERACIONALES")
        print("=" * 70)

        R = 8.314

        # Función de simulación
        def simular_conversion(T_C, relacion_molar, catalizador_wt):
            T_K = T_C + 273.15
            k = A * np.exp(-Ea * 1000 / (R * T_K))
            k_efectiva = k * catalizador_wt

            C_TG_0 = 1.14
            C_MeOH_0 = relacion_molar * 3 * C_TG_0
            C0 = [C_TG_0, C_MeOH_0, 0.0, 0.0]

            def sistema(C, t):
                C_TG, C_MeOH, C_FAME, C_GL = C
                r = k_efectiva * C_TG * C_MeOH**3
                return [-r, -3*r, 3*r, r]

            t = np.linspace(0, 60, 100)
            sol = odeint(sistema, C0, t)
            conversion = (C_TG_0 - sol[-1, 0]) / C_TG_0 * 100
            return conversion

        # Función objetivo
        pesos = self.config['paso3_optimizacion']['funcion_objetivo']

        def funcion_objetivo(x):
            T_C, relacion_molar = x
            cat_wt = 1.0  # Fijo

            try:
                conversion = simular_conversion(T_C, relacion_molar, cat_wt)
            except:
                return 1e10

            costo_T = (T_C - 60) / (70 - 60)
            costo_MeOH = (relacion_molar - 6) / (12 - 6)

            score = (pesos['peso_conversion'] * conversion / 100 -
                     pesos['peso_costo_temperatura'] * max(0, costo_T) -
                     pesos['peso_costo_metanol'] * max(0, costo_MeOH))

            return -score

        # Optimizar
        print("Ejecutando optimización...")
        restricciones = self.config['paso3_optimizacion']['restricciones']
        bounds = [
            (restricciones['temperatura_min_C'], restricciones['temperatura_max_C']),
            (restricciones['relacion_molar_min'], restricciones['relacion_molar_max'])
        ]

        resultado = differential_evolution(funcion_objetivo, bounds, maxiter=50, popsize=10, seed=42)
        T_opt, r_molar_opt = resultado.x
        conv_opt = simular_conversion(T_opt, r_molar_opt, 1.0)

        print(f"\n✓ Condiciones óptimas encontradas:")
        print(f"  - Temperatura: {T_opt:.1f} °C")
        print(f"  - Relación molar: {r_molar_opt:.1f}:1")
        print(f"  - Conversión esperada: {conv_opt:.2f} %")

        # Generar superficie de respuesta
        T_range = np.linspace(50, 70, 20)
        r_range = np.linspace(3, 12, 20)
        T_grid, R_grid = np.meshgrid(T_range, r_range)
        Conv_grid = np.zeros_like(T_grid)

        for i in range(len(r_range)):
            for j in range(len(T_range)):
                Conv_grid[i, j] = simular_conversion(T_grid[i, j], R_grid[i, j], 1.0)

        # Graficar
        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121, projection='3d')
        surf = ax1.plot_surface(T_grid, R_grid, Conv_grid, cmap='viridis', alpha=0.9)
        ax1.scatter([T_opt], [r_molar_opt], [conv_opt], color='red', s=100, marker='*')
        ax1.set_xlabel('Temperatura (°C)')
        ax1.set_ylabel('Relación Molar')
        ax1.set_zlabel('Conversión (%)')
        ax1.set_title('Superficie de Respuesta')
        plt.colorbar(surf, ax=ax1, shrink=0.5)

        ax2 = fig.add_subplot(122)
        contour = ax2.contourf(T_grid, R_grid, Conv_grid, levels=15, cmap='viridis')
        ax2.contour(T_grid, R_grid, Conv_grid, levels=[95, 97, 99], colors='white', linewidths=2)
        ax2.scatter([T_opt], [r_molar_opt], color='red', s=100, marker='*', zorder=5)
        ax2.set_xlabel('Temperatura (°C)')
        ax2.set_ylabel('Relación Molar')
        ax2.set_title('Mapa de Contorno')
        plt.colorbar(contour, ax=ax2)

        plt.tight_layout()
        plt.savefig('resultados/graficas/paso3_optimizacion.png', dpi=150)
        print(f"✓ Gráfica guardada: resultados/graficas/paso3_optimizacion.png")

        self.resultados['paso3'] = {
            'temperatura_optima_C': float(T_opt),
            'relacion_molar_optima': float(r_molar_opt),
            'conversion_esperada_pct': float(conv_opt)
        }

        return T_opt, r_molar_opt, conv_opt

    def paso4_generar_reporte_html(self):
        """Paso 4: Generar reporte HTML interactivo"""
        print("\n" + "=" * 70)
        print("PASO 4: GENERACIÓN DE REPORTE HTML INTERACTIVO")
        print("=" * 70)

        # Crear reporte HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config['paso4_reporte']['titulo']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
        }}
        .section {{
            background-color: white;
            margin: 20px 0;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .resultado {{
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 15px 25px;
            margin: 10px;
            border-radius: 5px;
            font-size: 18px;
        }}
        .resultado-valor {{
            font-size: 28px;
            font-weight: bold;
            display: block;
        }}
        .grafica {{
            text-align: center;
            margin: 20px 0;
        }}
        .grafica img {{
            max-width: 100%;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .recomendacion {{
            background-color: #2ecc71;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #34495e;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{self.config['paso4_reporte']['titulo']}</h1>
        <p>Generado: {self.timestamp}</p>
        <p>Autor: {self.config['paso4_reporte']['autor']}</p>
    </div>

    <div class="section">
        <h2>📊 Resumen Ejecutivo</h2>
        <div class="resultado">
            <span>Conversión Final</span>
            <span class="resultado-valor">{self.resultados['paso1']['conversion_final']:.2f}%</span>
        </div>
        <div class="resultado">
            <span>R² del Ajuste</span>
            <span class="resultado-valor">{self.resultados['paso2']['R2']:.4f}</span>
        </div>
        <div class="resultado">
            <span>Temperatura Óptima</span>
            <span class="resultado-valor">{self.resultados['paso3']['temperatura_optima_C']:.1f}°C</span>
        </div>
    </div>

    <div class="section">
        <h2>🔬 Paso 1: Procesamiento de Datos GC-FID</h2>
        <p>Datos cromatográficos procesados mediante método de estándar interno.</p>
        <div class="grafica">
            <img src="graficas/paso1_procesamiento_gc.png" alt="Procesamiento GC">
        </div>
        <p><strong>Conversión final alcanzada:</strong> {self.resultados['paso1']['conversion_final']:.2f}%</p>
    </div>

    <div class="section">
        <h2>📈 Paso 2: Ajuste de Parámetros Cinéticos</h2>
        <table>
            <tr>
                <th>Parámetro</th>
                <th>Valor</th>
            </tr>
            <tr>
                <td>Factor preexponencial (A)</td>
                <td>{self.resultados['paso2']['A']:.2e} L³/(mol³·min)</td>
            </tr>
            <tr>
                <td>Energía de activación (Ea)</td>
                <td>{self.resultados['paso2']['Ea']:.2f} kJ/mol</td>
            </tr>
            <tr>
                <td>Coeficiente de determinación (R²)</td>
                <td>{self.resultados['paso2']['R2']:.4f}</td>
            </tr>
            <tr>
                <td>Error cuadrático medio (RMSE)</td>
                <td>{self.resultados['paso2']['RMSE']:.4f} mol/L</td>
            </tr>
        </table>
        <div class="grafica">
            <img src="graficas/paso2_ajuste_parametros.png" alt="Ajuste de Parámetros">
        </div>
    </div>

    <div class="section">
        <h2>🎯 Paso 3: Optimización de Condiciones</h2>
        <p>Condiciones operacionales óptimas encontradas mediante optimización multi-criterio:</p>
        <table>
            <tr>
                <th>Variable</th>
                <th>Valor Óptimo</th>
            </tr>
            <tr>
                <td>Temperatura</td>
                <td>{self.resultados['paso3']['temperatura_optima_C']:.1f} °C</td>
            </tr>
            <tr>
                <td>Relación Molar (MeOH:TG)</td>
                <td>{self.resultados['paso3']['relacion_molar_optima']:.1f}:1</td>
            </tr>
            <tr>
                <td>Conversión Esperada</td>
                <td>{self.resultados['paso3']['conversion_esperada_pct']:.2f}%</td>
            </tr>
        </table>
        <div class="grafica">
            <img src="graficas/paso3_optimizacion.png" alt="Optimización">
        </div>
    </div>

    <div class="section">
        <h2>💡 Recomendaciones</h2>
        <div class="recomendacion">
            <h3>Recomendación 1: Implementar Condiciones Óptimas</h3>
            <p>Operar el reactor a {self.resultados['paso3']['temperatura_optima_C']:.1f}°C con relación molar {self.resultados['paso3']['relacion_molar_optima']:.1f}:1
            para maximizar conversión mientras se minimizan costos operacionales.</p>
        </div>
        <div class="recomendacion">
            <h3>Recomendación 2: Monitoreo de Calidad</h3>
            <p>El modelo predice conversión de {self.resultados['paso3']['conversion_esperada_pct']:.2f}%,
            {'superando' if self.resultados['paso3']['conversion_esperada_pct'] > 96.5 else 'por debajo de'}
            el requisito de 96.5% de la norma EN 14214.</p>
        </div>
        <div class="recomendacion">
            <h3>Recomendación 3: Validación Experimental</h3>
            <p>Validar las condiciones óptimas mediante experimentos en planta piloto antes de escalar a producción industrial.</p>
        </div>
    </div>

    <div class="section">
        <h2>📋 Conclusiones</h2>
        <ul>
            <li>El workflow automatizado procesó exitosamente todos los pasos de análisis</li>
            <li>Los parámetros cinéticos ajustados muestran excelente concordancia con datos experimentales (R² = {self.resultados['paso2']['R2']:.4f})</li>
            <li>Las condiciones óptimas identificadas balancean conversión máxima con costos operacionales mínimos</li>
            <li>El sistema está listo para escalar a producción piloto</li>
        </ul>
    </div>

</body>
</html>
"""

        # Guardar reporte
        with open('resultados/reporte_completo.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print("✓ Reporte HTML generado: resultados/reporte_completo.html")

        # Guardar resultados en JSON
        with open('resultados/resultados_completos.json', 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)

        print("✓ Resultados JSON guardados: resultados/resultados_completos.json")

    def ejecutar(self):
        """Ejecutar workflow completo"""
        try:
            # Paso 1
            df = self.paso1_procesamiento_gc()

            # Paso 2
            A, Ea = self.paso2_ajuste_parametros(df)

            # Paso 3
            T_opt, r_opt, conv_opt = self.paso3_optimizacion(A, Ea)

            # Paso 4
            self.paso4_generar_reporte_html()

            # Resumen final
            print("\n" + "=" * 70)
            print(" " * 20 + "✅ WORKFLOW COMPLETADO EXITOSAMENTE")
            print("=" * 70)
            print("\nArchivos generados:")
            print("  📄 resultados/datos_procesados.csv")
            print("  📄 resultados/resultados_completos.json")
            print("  🌐 resultados/reporte_completo.html  ← ABRIR EN NAVEGADOR")
            print("  📊 resultados/graficas/ (3 imágenes)")
            print("\n💡 Abre el archivo reporte_completo.html en tu navegador")
            print("   para ver el reporte interactivo completo.")
            print("=" * 70)

        except Exception as e:
            print(f"\n❌ ERROR durante la ejecución del workflow:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """Función principal"""
    workflow = WorkflowCompleto()
    workflow.ejecutar()


if __name__ == "__main__":
    main()
