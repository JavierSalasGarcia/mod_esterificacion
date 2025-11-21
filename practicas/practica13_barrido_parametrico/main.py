"""
Práctica 13: Estudio Paramétrico Automatizado mediante Barrido Sistemático

Este script implementa un barrido paramétrico que:
1. Lee configuración con múltiples valores por parámetro
2. Genera todas las combinaciones (producto cartesiano)
3. Ejecuta simulaciones secuencialmente
4. Organiza resultados con timestamp (fecha y hora)
5. Genera visualizaciones y reportes consolidados
"""

import json
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from datetime import datetime
from pathlib import Path
import time
import sys

# Agregar el directorio raíz al path para importar módulos del sistema
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from src.models.kinetic_model import KineticModel
    from src.visualization.plotter import save_figure
except ImportError:
    print("⚠️  Advertencia: No se pueden importar módulos del sistema principal")
    print("   Este script requiere los módulos en src/")
    print("   Ejecutar desde el directorio raíz del proyecto")


class ParametricSweep:
    """Clase para ejecutar barridos paramétricos automatizados."""

    def __init__(self, config_file='config_barrido.json'):
        """Inicializa el barrido paramétrico cargando configuración."""
        self.config_file = config_file
        self.config = self.cargar_configuracion()
        self.combinaciones = []
        self.resultados = []
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def cargar_configuracion(self):
        """Carga archivo de configuración JSON."""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generar_combinaciones(self):
        """Genera producto cartesiano de todos los parámetros variables."""
        params_barrido = self.config['parametros_barrido']

        # Identificar parámetros con múltiples valores
        params_variables = {}
        params_constantes = {}

        for param, valores in params_barrido.items():
            if isinstance(valores, list) and len(valores) > 1:
                params_variables[param] = valores
            elif isinstance(valores, list):
                params_constantes[param] = valores[0]
            else:
                params_constantes[param] = valores

        # Generar producto cartesiano
        nombres_params = list(params_variables.keys())
        valores_params = list(params_variables.values())

        combinaciones_raw = list(itertools.product(*valores_params))

        # Convertir a lista de diccionarios con todos los parámetros
        self.combinaciones = []
        for combo in combinaciones_raw:
            config_sim = params_constantes.copy()
            for i, nombre in enumerate(nombres_params):
                config_sim[nombre] = combo[i]
            self.combinaciones.append(config_sim)

        return self.combinaciones

    def estimar_tiempo_computo(self):
        """Estima tiempo total ejecutando una simulación de prueba."""
        print("⏱️  Estimando tiempo de cómputo...")

        if not self.combinaciones:
            self.generar_combinaciones()

        # Tomar primera combinación para prueba
        config_prueba = self.combinaciones[0]

        inicio = time.time()
        self._simular_una_configuracion(config_prueba, mostrar_progreso=False)
        tiempo_una_sim = time.time() - inicio

        tiempo_total = tiempo_una_sim * len(self.combinaciones)

        return tiempo_una_sim, tiempo_total

    def mostrar_advertencia(self):
        """Muestra advertencia sobre el barrido a ejecutar."""
        if not self.combinaciones:
            self.generar_combinaciones()

        tiempo_una, tiempo_total = self.estimar_tiempo_computo()

        # Calcular espacio aproximado (asumiendo ~3.5 MB por simulación)
        espacio_mb = len(self.combinaciones) * 3.5

        params_barrido = self.config['parametros_barrido']
        params_variables = {k: v for k, v in params_barrido.items()
                           if isinstance(v, list) and len(v) > 1}

        print("\n" + "="*60)
        print("⚠️   ADVERTENCIA: Barrido Paramétrico")
        print("="*60)
        print("\nParámetros variables:")
        for param, valores in params_variables.items():
            print(f"  • {param}: {len(valores)} valores {valores}")

        print(f"\n📊 Total de simulaciones: {len(self.combinaciones)}")
        print(f"⏱️  Tiempo estimado: {tiempo_total/60:.1f} minutos ({tiempo_una:.1f} s/simulación)")
        print(f"💾 Espacio en disco: ~{espacio_mb:.0f} MB")
        print("="*60)

        if self.config['opciones_barrido'].get('pedir_confirmacion', True):
            respuesta = input("\n¿Continuar con el barrido? [s/N]: ")
            if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Barrido cancelado por el usuario.")
                sys.exit(0)

    def _simular_una_configuracion(self, config, mostrar_progreso=True):
        """Ejecuta una simulación con una configuración específica."""
        # Extraer parámetros
        T_celsius = config['temperatura_C']
        relacion_molar = config['relacion_molar']
        cat_pct = config['concentracion_catalizador_pct']
        agitacion_rpm = config['agitacion_rpm']

        tiempo_final = self.config['parametros_fijos']['tiempo_reaccion_min']
        volumen_mL = self.config['parametros_fijos']['volumen_reactor_mL']

        A = self.config['parametros_cineticos']['factor_preexponencial']
        Ea = self.config['parametros_cineticos']['energia_activacion_J_mol']

        # Crear instancia del modelo
        modelo = KineticModel(A=A, Ea=Ea)

        # Condiciones iniciales (simplificadas para ejemplo)
        # En implementación real, calcular a partir de masas y volumen
        C0_TG = 0.5  # mol/L (ejemplo)
        C0_MeOH = C0_TG * relacion_molar
        C0 = [C0_TG, C0_MeOH, 0, 0]  # TG, MeOH, FAME, GL

        # Vector de tiempo
        t = np.linspace(0, tiempo_final, 100)

        # Resolver sistema
        T_kelvin = T_celsius + 273.15
        sol = modelo.resolver_sistema(C0, t, T_kelvin)

        # Calcular conversión final
        conversion_final = (C0_TG - sol[-1, 0]) / C0_TG * 100

        # Compilar resultados
        resultado = {
            'temperatura_C': T_celsius,
            'relacion_molar': relacion_molar,
            'concentracion_catalizador_pct': cat_pct,
            'agitacion_rpm': agitacion_rpm,
            'conversion_final_pct': conversion_final,
            'tiempo_min': tiempo_final,
            'concentraciones': sol,
            'tiempos': t
        }

        return resultado

    def ejecutar_barrido(self):
        """Ejecuta todas las simulaciones del barrido."""
        if not self.combinaciones:
            self.generar_combinaciones()

        print(f"\n🚀 Iniciando barrido paramétrico: {len(self.combinaciones)} simulaciones")
        print(f"📁 Resultados se guardarán en: resultados/barrido_{self.timestamp}/\n")

        inicio_total = time.time()

        for i, config in enumerate(self.combinaciones, 1):
            print(f"[{i}/{len(self.combinaciones)}] ", end="", flush=True)

            # Mostrar configuración actual
            params_str = ", ".join([f"{k}={v}" for k, v in config.items()])
            print(f"{params_str[:60]}...", end=" ", flush=True)

            # Ejecutar simulación
            inicio_sim = time.time()
            resultado = self._simular_una_configuracion(config)
            tiempo_sim = time.time() - inicio_sim

            # Guardar resultado
            self.resultados.append(resultado)

            print(f"✓ ({tiempo_sim:.1f}s, Conv={resultado['conversion_final_pct']:.1f}%)")

        tiempo_total = time.time() - inicio_total
        print(f"\n✅ Barrido completado en {tiempo_total/60:.1f} minutos")
        print(f"   Promedio: {tiempo_total/len(self.combinaciones):.1f} s/simulación")

    def guardar_resultados(self):
        """Guarda resultados organizados en carpetas."""
        # Crear carpeta base con timestamp
        carpeta_base = Path(self.config['salida']['carpeta_base'])
        carpeta_barrido = carpeta_base / f"barrido_{self.timestamp}"
        carpeta_barrido.mkdir(parents=True, exist_ok=True)

        # 1. Guardar configuración usada
        with open(carpeta_barrido / 'configuracion_barrido.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

        # 2. Guardar resumen del barrido
        with open(carpeta_barrido / 'resumen_barrido.txt', 'w', encoding='utf-8') as f:
            f.write(f"Barrido Paramétrico Automatizado\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Fecha y hora: {self.timestamp}\n")
            f.write(f"Total de simulaciones: {len(self.resultados)}\n")
            f.write(f"Configuración: {self.config_file}\n")

        # 3. Generar tabla consolidada
        df_resultados = pd.DataFrame([
            {
                'simulacion': i+1,
                'temperatura_C': r['temperatura_C'],
                'relacion_molar': r['relacion_molar'],
                'catalizador_pct': r['concentracion_catalizador_pct'],
                'agitacion_rpm': r['agitacion_rpm'],
                'conversion_pct': r['conversion_final_pct']
            }
            for i, r in enumerate(self.resultados)
        ])

        df_resultados.to_csv(
            carpeta_barrido / 'resultados_consolidados.csv',
            index=False,
            float_format='%.2f'
        )

        # 4. Guardar simulaciones individuales (opcional)
        if self.config['opciones_barrido'].get('guardar_simulaciones_individuales', False):
            carpeta_sims = carpeta_barrido / 'simulaciones'
            carpeta_sims.mkdir(exist_ok=True)

            for i, resultado in enumerate(self.resultados, 1):
                carpeta_sim = carpeta_sims / f'sim_{i:03d}'
                carpeta_sim.mkdir(exist_ok=True)

                # Guardar parámetros
                params = {
                    'temperatura_C': resultado['temperatura_C'],
                    'relacion_molar': resultado['relacion_molar'],
                    'concentracion_catalizador_pct': resultado['concentracion_catalizador_pct'],
                    'agitacion_rpm': resultado['agitacion_rpm']
                }
                with open(carpeta_sim / 'parametros.json', 'w') as f:
                    json.dump(params, f, indent=2)

                # Guardar concentraciones
                df_conc = pd.DataFrame({
                    'tiempo_min': resultado['tiempos'],
                    'C_TG': resultado['concentraciones'][:, 0],
                    'C_MeOH': resultado['concentraciones'][:, 1],
                    'C_FAME': resultado['concentraciones'][:, 2],
                    'C_GL': resultado['concentraciones'][:, 3]
                })
                df_conc.to_csv(carpeta_sim / 'concentraciones.csv', index=False)

        print(f"\n💾 Resultados guardados en: {carpeta_barrido}")
        return carpeta_barrido

    def generar_visualizaciones(self, carpeta_barrido):
        """Genera superficies de respuesta y gráficos comparativos."""
        if not self.config['opciones_barrido'].get('generar_visualizaciones', True):
            return

        carpeta_viz = carpeta_barrido / 'visualizaciones'
        carpeta_viz.mkdir(exist_ok=True)

        print("\n📊 Generando visualizaciones...")

        # Preparar datos
        df = pd.DataFrame([
            {
                'temperatura_C': r['temperatura_C'],
                'relacion_molar': r['relacion_molar'],
                'catalizador_pct': r['concentracion_catalizador_pct'],
                'agitacion_rpm': r['agitacion_rpm'],
                'conversion_pct': r['conversion_final_pct']
            }
            for r in self.resultados
        ])

        # 1. Superficie de respuesta Temperatura vs Relación Molar
        self._plot_superficie_2D(df, 'temperatura_C', 'relacion_molar',
                                'conversion_pct', carpeta_viz)

        # 2. Matriz de correlación
        self._plot_correlacion(df, carpeta_viz)

        print(f"   ✓ Visualizaciones guardadas en: {carpeta_viz}")

    def _plot_superficie_2D(self, df, param_x, param_y, variable_z, carpeta_salida):
        """Genera superficie 3D y mapa de contorno para 2 parámetros."""
        # Crear grilla
        x_unique = sorted(df[param_x].unique())
        y_unique = sorted(df[param_y].unique())

        X, Y = np.meshgrid(x_unique, y_unique)
        Z = np.zeros_like(X)

        for i, y_val in enumerate(y_unique):
            for j, x_val in enumerate(x_unique):
                mask = (df[param_x] == x_val) & (df[param_y] == y_val)
                if mask.any():
                    Z[i, j] = df.loc[mask, variable_z].mean()

        # Superficie 3D
        fig = plt.figure(figsize=(12, 5))

        ax1 = fig.add_subplot(121, projection='3d')
        surf = ax1.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.8)
        ax1.set_xlabel(param_x.replace('_', ' ').title())
        ax1.set_ylabel(param_y.replace('_', ' ').title())
        ax1.set_zlabel('Conversión (%)')
        ax1.set_title('Superficie de Respuesta 3D')
        fig.colorbar(surf, ax=ax1, shrink=0.5)

        # Contorno 2D
        ax2 = fig.add_subplot(122)
        contour = ax2.contourf(X, Y, Z, levels=15, cmap=cm.viridis)
        ax2.contour(X, Y, Z, levels=[90, 95, 98], colors='white', linewidths=1.5)
        ax2.set_xlabel(param_x.replace('_', ' ').title())
        ax2.set_ylabel(param_y.replace('_', ' ').title())
        ax2.set_title('Mapa de Contorno')
        fig.colorbar(contour, ax=ax2, label='Conversión (%)')

        plt.tight_layout()
        plt.savefig(carpeta_salida / f'superficie_{param_x}_vs_{param_y}.png', dpi=300)
        plt.close()

    def _plot_correlacion(self, df, carpeta_salida):
        """Genera matriz de correlación entre parámetros y conversión."""
        # Seleccionar columnas numéricas
        df_numeric = df.select_dtypes(include=[np.number])

        corr_matrix = df_numeric.corr()

        plt.figure(figsize=(8, 6))
        im = plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)

        # Etiquetas
        labels = [col.replace('_', ' ').title() for col in corr_matrix.columns]
        plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
        plt.yticks(range(len(labels)), labels)

        # Valores en celdas
        for i in range(len(labels)):
            for j in range(len(labels)):
                text = plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                              ha="center", va="center", color="black", fontsize=10)

        plt.colorbar(im, label='Correlación')
        plt.title('Matriz de Correlación')
        plt.tight_layout()
        plt.savefig(carpeta_salida / 'matriz_correlacion.png', dpi=300)
        plt.close()


def main():
    """Función principal para ejecutar el barrido paramétrico."""
    print("\n" + "="*60)
    print("   Práctica 13: Barrido Paramétrico Automatizado")
    print("="*60)

    # Crear instancia de barrido
    sweep = ParametricSweep('config_barrido.json')

    # Generar combinaciones
    sweep.generar_combinaciones()

    # Mostrar advertencia y pedir confirmación
    sweep.mostrar_advertencia()

    # Ejecutar barrido
    sweep.ejecutar_barrido()

    # Guardar resultados
    carpeta_resultados = sweep.guardar_resultados()

    # Generar visualizaciones
    sweep.generar_visualizaciones(carpeta_resultados)

    print("\n" + "="*60)
    print("✅ Barrido paramétrico completado exitosamente")
    print("="*60)
    print(f"\n📁 Revisar resultados en: {carpeta_resultados}")
    print(f"📊 Abrir visualizaciones en: {carpeta_resultados}/visualizaciones/")
    print(f"📈 Analizar datos en: {carpeta_resultados}/resultados_consolidados.csv")
    print("\n")


if __name__ == "__main__":
    main()
