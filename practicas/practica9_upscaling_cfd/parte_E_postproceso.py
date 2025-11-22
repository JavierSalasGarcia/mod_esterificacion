"""
Práctica 9 - Parte E: Postproceso de Resultados CFD

Script para procesar resultados de simulación CFD de Ansys Fluent.
Genera visualizaciones de campos de velocidad, temperatura y conversión.

Autor: Sistema de Modelado de Biodiesel
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import json
import os


class PostprocesoCFD:
    """Procesador de resultados CFD de transesterificación"""

    def __init__(self):
        """Inicializar postprocesador"""
        print("=" * 70)
        print(" " * 15 + "POSTPROCESO DE SIMULACIÓN CFD")
        print("=" * 70)

        os.makedirs('resultados/campos_cfd', exist_ok=True)

    def generar_datos_sinteticos(self):
        """
        Generar datos sintéticos para demostración

        NOTA: En uso real, estos datos se cargarían desde archivos
        exportados de Fluent (formato .csv o .dat)
        """
        print("\n⚠️  Modo demostración: Generando datos sintéticos")
        print("    En producción, cargar datos desde Fluent Export")

        # Grid radial-axial (cilindro)
        nr = 50  # Puntos radiales
        nz = 60  # Puntos axiales

        # Geometría (reactor de 20 L)
        R = 0.15  # Radio 15 cm
        H = 0.45  # Altura 45 cm

        r = np.linspace(0, R, nr)
        z = np.linspace(0, H, nz)
        R_grid, Z_grid = np.meshgrid(r, z)

        # --- Campo de velocidades ---
        # Velocidad tangencial (rotación del ribbon impeller)
        # Mayor cerca del impulsor, menor cerca del centro y pared
        v_theta = np.zeros_like(R_grid)
        for i in range(nz):
            z_pos = z[i] / H
            # Perfil de velocidad: máximo a r = 0.7*R, decae hacia centro y pared
            v_theta[i, :] = 0.5 * np.sin(np.pi * r / R) * (1 - abs(z_pos - 0.5))

        # Velocidad axial (circulación)
        v_z = np.zeros_like(R_grid)
        for i in range(nz):
            # Ascendente en centro, descendente en pared
            v_z[i, :] = 0.2 * (1 - 2*(r/R)**2) * np.sin(2*np.pi*z[i]/H)

        # --- Campo de temperatura ---
        # Temperatura ligeramente no uniforme por serpentín
        T = 333 + 2 * np.sin(2*np.pi*Z_grid/H) * (R_grid/R)  # 333 K ± 2 K

        # --- Campo de conversión ---
        # Conversión aumenta con el tiempo de residencia (altura)
        # y es más uniforme cerca del impulsor (mezcla)
        conversion = np.zeros_like(R_grid)
        for i in range(nz):
            z_frac = z[i] / H
            r_frac = r / R
            # Mayor conversión a mayor altura (más tiempo)
            # Más uniforme en zona del ribbon (0.2 < z < 0.8)
            if 0.2 < z_frac < 0.8:
                conversion[i, :] = 85 + 10*z_frac + 2*np.random.randn(nr)
            else:
                conversion[i, :] = 70 + 15*z_frac + 5*(1-r_frac) + 3*np.random.randn(nr)

        conversion = np.clip(conversion, 0, 100)

        # --- Fracciones másicas de especies ---
        Y_TG = 0.75 * (1 - conversion/100)
        Y_FAME = 0.75 * (conversion/100)
        Y_MeOH = 0.25 * (1 - 0.8*conversion/100)
        Y_GL = 0.25 * (conversion/100)

        return {
            'r': r,
            'z': z,
            'R_grid': R_grid,
            'Z_grid': Z_grid,
            'v_theta': v_theta,
            'v_z': v_z,
            'T': T,
            'conversion': conversion,
            'Y_TG': Y_TG,
            'Y_FAME': Y_FAME,
            'Y_MeOH': Y_MeOH,
            'Y_GL': Y_GL
        }

    def graficar_campos_velocidad(self, datos):
        """Graficar campos de velocidad"""
        print("\n📊 Generando campos de velocidad...")

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Velocidad tangencial
        im1 = axes[0].contourf(datos['Z_grid']*100, datos['R_grid']*100,
                               datos['v_theta'], levels=20, cmap='coolwarm')
        axes[0].set_xlabel('Altura (cm)')
        axes[0].set_ylabel('Radio (cm)')
        axes[0].set_title('Velocidad Tangencial (m/s)')
        plt.colorbar(im1, ax=axes[0])

        # Vectores de velocidad axial
        # Subsample para visualización clara
        skip = 3
        axes[1].quiver(datos['Z_grid'][::skip, ::skip]*100,
                      datos['R_grid'][::skip, ::skip]*100,
                      datos['v_z'][::skip, ::skip],
                      np.zeros_like(datos['v_z'][::skip, ::skip]),
                      scale=2, color='blue', alpha=0.6)
        axes[1].set_xlabel('Altura (cm)')
        axes[1].set_ylabel('Radio (cm)')
        axes[1].set_title('Campo de Velocidad Axial')
        axes[1].set_aspect('equal')

        plt.tight_layout()
        plt.savefig('resultados/campos_cfd/velocidad.png', dpi=150)
        print("  ✓ Guardado: resultados/campos_cfd/velocidad.png")

    def graficar_campo_temperatura(self, datos):
        """Graficar campo de temperatura"""
        print("\n🌡️  Generando campo de temperatura...")

        fig, ax = plt.subplots(figsize=(10, 6))

        im = ax.contourf(datos['Z_grid']*100, datos['R_grid']*100,
                        datos['T'] - 273.15, levels=20, cmap='hot')
        ax.set_xlabel('Altura (cm)')
        ax.set_ylabel('Radio (cm)')
        ax.set_title('Campo de Temperatura (°C)')
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Temperatura (°C)')

        # Marcar posición del serpentín
        for i in range(10):
            z_pos = (i + 0.5) * 0.45 / 10 * 100  # cm
            ax.plot([z_pos], [14.5], 'wo', markersize=4)

        plt.tight_layout()
        plt.savefig('resultados/campos_cfd/temperatura.png', dpi=150)
        print("  ✓ Guardado: resultados/campos_cfd/temperatura.png")

    def graficar_campo_conversion(self, datos):
        """Graficar campo de conversión"""
        print("\n📈 Generando campo de conversión...")

        fig, ax = plt.subplots(figsize=(10, 6))

        im = ax.contourf(datos['Z_grid']*100, datos['R_grid']*100,
                        datos['conversion'], levels=20, cmap='viridis')
        ax.set_xlabel('Altura (cm)')
        ax.set_ylabel('Radio (cm)')
        ax.set_title('Campo de Conversión de Triglicéridos (%)')
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Conversión (%)')

        # Línea de especificación 96.5%
        contour = ax.contour(datos['Z_grid']*100, datos['R_grid']*100,
                            datos['conversion'], levels=[96.5], colors='white',
                            linewidths=2, linestyles='dashed')
        ax.clabel(contour, inline=True, fontsize=10, fmt='96.5%')

        plt.tight_layout()
        plt.savefig('resultados/campos_cfd/conversion.png', dpi=150)
        print("  ✓ Guardado: resultados/campos_cfd/conversion.png")

    def graficar_especies(self, datos):
        """Graficar distribución de especies"""
        print("\n🧪 Generando distribución de especies...")

        fig, axes = plt.subplots(2, 2, figsize=(14, 12))

        especies = [
            ('Y_TG', 'Triglicérido (TG)', 'Reds'),
            ('Y_FAME', 'Biodiesel (FAME)', 'Greens'),
            ('Y_MeOH', 'Metanol (MeOH)', 'Blues'),
            ('Y_GL', 'Glicerol (GL)', 'Purples')
        ]

        for idx, (key, titulo, cmap) in enumerate(especies):
            ax = axes.flat[idx]
            im = ax.contourf(datos['Z_grid']*100, datos['R_grid']*100,
                           datos[key], levels=15, cmap=cmap)
            ax.set_xlabel('Altura (cm)')
            ax.set_ylabel('Radio (cm)')
            ax.set_title(f'Fracción Másica de {titulo}')
            plt.colorbar(im, ax=ax)

        plt.tight_layout()
        plt.savefig('resultados/campos_cfd/especies.png', dpi=150)
        print("  ✓ Guardado: resultados/campos_cfd/especies.png")

    def analizar_zonas_muertas(self, datos):
        """Identificar zonas de baja mezcla (zonas muertas)"""
        print("\n🔍 Analizando zonas de baja mezcla...")

        # Calcular magnitud de velocidad
        v_mag = np.sqrt(datos['v_theta']**2 + datos['v_z']**2)

        # Identificar zonas con velocidad < 10% del máximo
        umbral_zona_muerta = 0.1 * np.max(v_mag)
        zonas_muertas = v_mag < umbral_zona_muerta

        # Calcular porcentaje de volumen con zona muerta
        pct_zona_muerta = np.sum(zonas_muertas) / zonas_muertas.size * 100

        print(f"  - Velocidad máxima: {np.max(v_mag):.3f} m/s")
        print(f"  - Umbral zona muerta: {umbral_zona_muerta:.3f} m/s")
        print(f"  - Porcentaje de volumen con zona muerta: {pct_zona_muerta:.2f}%")

        # Graficar
        fig, ax = plt.subplots(figsize=(10, 6))

        im = ax.contourf(datos['Z_grid']*100, datos['R_grid']*100,
                        v_mag, levels=20, cmap='plasma')
        ax.contour(datos['Z_grid']*100, datos['R_grid']*100,
                  zonas_muertas, levels=[0.5], colors='white',
                  linewidths=2, linestyles='dashed')
        ax.set_xlabel('Altura (cm)')
        ax.set_ylabel('Radio (cm)')
        ax.set_title('Magnitud de Velocidad y Zonas de Baja Mezcla')
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('|v| (m/s)')

        # Texto indicando zona muerta
        ax.text(0.5, 0.95, f'Zona muerta: {pct_zona_muerta:.1f}% del volumen',
               transform=ax.transAxes, ha='center', va='top',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
               fontsize=12)

        plt.tight_layout()
        plt.savefig('resultados/campos_cfd/zonas_muertas.png', dpi=150)
        print("  ✓ Guardado: resultados/campos_cfd/zonas_muertas.png")

        return pct_zona_muerta

    def generar_perfiles_axiales(self, datos):
        """Generar perfiles axiales en diferentes radios"""
        print("\n📉 Generando perfiles axiales...")

        # Seleccionar 3 posiciones radiales
        nr = len(datos['r'])
        idx_radios = [nr//4, nr//2, 3*nr//4]
        labels = ['r = R/4 (centro)', 'r = R/2 (medio)', 'r = 3R/4 (pared)']

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Conversión vs altura
        for idx, label in zip(idx_radios, labels):
            axes[0].plot(datos['z']*100, datos['conversion'][:, idx],
                        marker='o', label=label)
        axes[0].set_xlabel('Altura (cm)')
        axes[0].set_ylabel('Conversión (%)')
        axes[0].set_title('Conversión vs Altura')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Temperatura vs altura
        for idx, label in zip(idx_radios, labels):
            axes[1].plot(datos['z']*100, datos['T'][:, idx] - 273.15,
                        marker='s', label=label)
        axes[1].set_xlabel('Altura (cm)')
        axes[1].set_ylabel('Temperatura (°C)')
        axes[1].set_title('Temperatura vs Altura')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        # Velocidad tangencial vs altura
        for idx, label in zip(idx_radios, labels):
            axes[2].plot(datos['z']*100, datos['v_theta'][:, idx],
                        marker='^', label=label)
        axes[2].set_xlabel('Altura (cm)')
        axes[2].set_ylabel('Velocidad tangencial (m/s)')
        axes[2].set_title('Velocidad vs Altura')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('resultados/campos_cfd/perfiles_axiales.png', dpi=150)
        print("  ✓ Guardado: resultados/campos_cfd/perfiles_axiales.png")

    def generar_reporte(self, datos, pct_zona_muerta):
        """Generar reporte de resultados"""
        print("\n📄 Generando reporte de resultados...")

        # Calcular estadísticas
        conversion_promedio = np.mean(datos['conversion'])
        conversion_std = np.std(datos['conversion'])
        conversion_min = np.min(datos['conversion'])
        conversion_max = np.max(datos['conversion'])

        T_promedio = np.mean(datos['T']) - 273.15
        T_std = np.std(datos['T'])

        reporte = {
            'simulacion': {
                'tipo': 'CFD Transitorio',
                'software': 'Ansys Fluent',
                'modelo_turbulencia': 'k-epsilon',
                'modelo_cinetico': '3 pasos reversibles',
                'malla': 'Estructurada cilíndrica'
            },
            'estadisticas_conversion': {
                'promedio_pct': float(conversion_promedio),
                'desviacion_estandar_pct': float(conversion_std),
                'minimo_pct': float(conversion_min),
                'maximo_pct': float(conversion_max)
            },
            'estadisticas_temperatura': {
                'promedio_C': float(T_promedio),
                'desviacion_estandar_C': float(T_std)
            },
            'analisis_mezcla': {
                'porcentaje_zona_muerta': float(pct_zona_muerta),
                'calidad_mezcla': 'Buena' if pct_zona_muerta < 5 else 'Aceptable' if pct_zona_muerta < 10 else 'Pobre'
            },
            'conclusiones': [
                f"Conversión promedio de {conversion_promedio:.1f}% ± {conversion_std:.1f}%",
                f"Temperatura uniforme: {T_promedio:.1f}°C ± {T_std:.1f}°C",
                f"Zonas de baja mezcla: {pct_zona_muerta:.1f}% del volumen"
            ]
        }

        with open('resultados/campos_cfd/reporte_cfd.json', 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)

        print("  ✓ Guardado: resultados/campos_cfd/reporte_cfd.json")

        # Imprimir resumen
        print("\n" + "=" * 70)
        print(" " * 20 + "RESUMEN DE RESULTADOS")
        print("=" * 70)
        print(f"Conversión promedio:     {conversion_promedio:.2f}% ± {conversion_std:.2f}%")
        print(f"Conversión mínima:       {conversion_min:.2f}%")
        print(f"Conversión máxima:       {conversion_max:.2f}%")
        print(f"Temperatura promedio:    {T_promedio:.2f}°C ± {T_std:.2f}°C")
        print(f"Zonas de baja mezcla:    {pct_zona_muerta:.2f}% del volumen")
        print(f"Calidad de mezcla:       {reporte['analisis_mezcla']['calidad_mezcla']}")
        print("=" * 70)


def main():
    """Función principal"""
    postproc = PostprocesoCFD()

    # Generar/cargar datos
    datos = postproc.generar_datos_sinteticos()

    # Generar visualizaciones
    postproc.graficar_campos_velocidad(datos)
    postproc.graficar_campo_temperatura(datos)
    postproc.graficar_campo_conversion(datos)
    postproc.graficar_especies(datos)

    # Análisis avanzado
    pct_zona_muerta = postproc.analizar_zonas_muertas(datos)
    postproc.generar_perfiles_axiales(datos)

    # Reporte
    postproc.generar_reporte(datos, pct_zona_muerta)

    print("\n" + "=" * 70)
    print(" " * 20 + "✅ POSTPROCESO COMPLETADO")
    print("=" * 70)
    print("\nArchivos generados en resultados/campos_cfd/:")
    print("  - velocidad.png")
    print("  - temperatura.png")
    print("  - conversion.png")
    print("  - especies.png")
    print("  - zonas_muertas.png")
    print("  - perfiles_axiales.png")
    print("  - reporte_cfd.json")
    print("\nRevisa analisis.md para interpretar los resultados.")
    print("=" * 70)


if __name__ == "__main__":
    main()
