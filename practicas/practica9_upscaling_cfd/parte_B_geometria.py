"""
Práctica 9 - Parte B: Geometría del Reactor Piloto

Genera especificaciones geométricas detalladas del reactor piloto de 20 L
con ribbon impeller, serpentín de enfriamiento y deflectores.

Autor: Sistema de Modelado de Biodiesel
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class GeometriaReactorPiloto:
    """Generador de geometría detallada del reactor piloto"""

    def __init__(self, config_file='config.json'):
        """Inicializar con configuración"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.V_L = self.config['reactor_piloto']['volumen_L']
        self.relacion_H_D = self.config['reactor_piloto']['relacion_H_D']
        self.n_deflectores = self.config['reactor_piloto']['deflectores']
        self.n_espiras = self.config['reactor_piloto']['serpentin']['numero_espiras']
        self.d_tubo_mm = self.config['reactor_piloto']['serpentin']['diametro_tubo_mm']

        print("=" * 70)
        print(" " * 15 + "GEOMETRÍA DETALLADA DEL REACTOR PILOTO")
        print("=" * 70)

    def calcular_dimensiones_principales(self):
        """Calcular dimensiones principales del reactor"""
        # Volumen cilíndrico: V = π * D² / 4 * H
        # Con H = relacion_H_D * D
        V_m3 = self.V_L / 1000
        D_m = (4 * V_m3 / (np.pi * self.relacion_H_D))**(1/3)
        H_m = self.relacion_H_D * D_m

        # Radio
        R_m = D_m / 2

        print(f"\n📐 DIMENSIONES PRINCIPALES")
        print("-" * 70)
        print(f"Diámetro reactor (D):        {D_m*1000:.2f} mm ({D_m:.4f} m)")
        print(f"Radio reactor (R):           {R_m*1000:.2f} mm ({R_m:.4f} m)")
        print(f"Altura de líquido (H):       {H_m*1000:.2f} mm ({H_m:.4f} m)")
        print(f"Relación H/D:                {H_m/D_m:.2f}")
        print(f"Volumen total:               {self.V_L:.2f} L")
        print(f"Factor de llenado:           0.80 (espacio libre 20%)")

        return D_m, H_m, R_m

    def calcular_ribbon_impeller(self, D_m, H_m):
        """Calcular geometría del ribbon impeller (impulsor helicoidal)"""
        # El ribbon impeller típicamente ocupa 90-95% del diámetro del reactor
        D_ribbon_m = 0.92 * D_m
        R_ribbon_m = D_ribbon_m / 2

        # Altura del ribbon (típicamente 70-80% de H)
        H_ribbon_m = 0.75 * H_m

        # Paso de la hélice (pitch)
        pitch_m = D_ribbon_m  # Un pitch igual al diámetro

        # Número de vueltas
        n_vueltas = H_ribbon_m / pitch_m

        # Ancho de la cinta
        ancho_cinta_m = 0.08 * D_ribbon_m

        print(f"\n🔧 RIBBON IMPELLER (Impulsor Helicoidal)")
        print("-" * 70)
        print(f"Tipo:                        Ribbon helicoidal (doble cinta)")
        print(f"Diámetro ribbon (D_ribbon):  {D_ribbon_m*1000:.2f} mm ({D_ribbon_m:.4f} m)")
        print(f"Relación D_ribbon/D_reactor: {D_ribbon_m/D_m:.3f}")
        print(f"Altura ribbon:               {H_ribbon_m*1000:.2f} mm ({H_ribbon_m:.4f} m)")
        print(f"Paso (pitch):                {pitch_m*1000:.2f} mm ({pitch_m:.4f} m)")
        print(f"Número de vueltas:           {n_vueltas:.2f}")
        print(f"Ancho de cinta:              {ancho_cinta_m*1000:.2f} mm")
        print(f"Configuración:               2 cintas helicoidales")
        print(f"                             (1 ascendente + 1 descendente)")

        return {
            'diametro_m': D_ribbon_m,
            'radio_m': R_ribbon_m,
            'altura_m': H_ribbon_m,
            'pitch_m': pitch_m,
            'n_vueltas': n_vueltas,
            'ancho_cinta_m': ancho_cinta_m
        }

    def calcular_serpentin(self, D_m, H_m):
        """Calcular geometría del serpentín de enfriamiento/calentamiento"""
        # El serpentín se coloca en la pared del reactor
        D_serpentin_m = D_m - 0.02  # 2 cm más pequeño que reactor
        R_serpentin_m = D_serpentin_m / 2

        # Altura total del serpentín
        H_serpentin_m = 0.85 * H_m  # Ocupa 85% de la altura

        # Paso entre espiras
        paso_espiras_m = H_serpentin_m / self.n_espiras

        # Diámetro del tubo
        d_tubo_m = self.d_tubo_mm / 1000

        # Longitud total de tubo
        longitud_espira = np.pi * D_serpentin_m
        longitud_total_m = longitud_espira * self.n_espiras

        # Área de transferencia de calor
        area_transferencia_m2 = np.pi * d_tubo_m * longitud_total_m

        print(f"\n🌡️  SERPENTÍN DE CALENTAMIENTO/ENFRIAMIENTO")
        print("-" * 70)
        print(f"Tipo:                        Serpentín helicoidal de pared")
        print(f"Diámetro serpentín:          {D_serpentin_m*1000:.2f} mm")
        print(f"Número de espiras:           {self.n_espiras}")
        print(f"Altura total serpentín:      {H_serpentin_m*1000:.2f} mm")
        print(f"Paso entre espiras:          {paso_espiras_m*1000:.2f} mm")
        print(f"Diámetro tubo:               {self.d_tubo_mm:.1f} mm")
        print(f"Material:                    {self.config['reactor_piloto']['serpentin']['material']}")
        print(f"Longitud total de tubo:      {longitud_total_m:.2f} m")
        print(f"Área de transferencia:       {area_transferencia_m2:.4f} m²")

        return {
            'diametro_m': D_serpentin_m,
            'altura_m': H_serpentin_m,
            'n_espiras': self.n_espiras,
            'paso_espiras_m': paso_espiras_m,
            'd_tubo_m': d_tubo_m,
            'longitud_total_m': longitud_total_m,
            'area_transferencia_m2': area_transferencia_m2
        }

    def calcular_deflectores(self, D_m, H_m):
        """Calcular geometría de deflectores (baffles)"""
        # Ancho típico de deflector: D/10 a D/12
        ancho_deflector_m = D_m / 10

        # Altura del deflector
        altura_deflector_m = 0.90 * H_m  # 90% de la altura

        # Separación de la pared
        separacion_pared_m = 0.01  # 1 cm de la pared

        # Ángulos de posicionamiento (equiespaciados)
        angulos = np.linspace(0, 360, self.n_deflectores, endpoint=False)

        print(f"\n🛡️  DEFLECTORES (BAFFLES)")
        print("-" * 70)
        print(f"Número de deflectores:       {self.n_deflectores}")
        print(f"Ancho deflector:             {ancho_deflector_m*1000:.2f} mm")
        print(f"Altura deflector:            {altura_deflector_m*1000:.2f} mm")
        print(f"Separación de pared:         {separacion_pared_m*1000:.2f} mm")
        print(f"Ángulos de posición:         {angulos}°")
        print(f"Función:                     Prevenir vórtice y mejorar mezcla radial")

        return {
            'ancho_m': ancho_deflector_m,
            'altura_m': altura_deflector_m,
            'separacion_pared_m': separacion_pared_m,
            'angulos_deg': angulos.tolist()
        }

    def visualizar_geometria(self, D_m, H_m, ribbon, serpentin, deflectores):
        """Visualizar geometría 3D del reactor"""
        fig = plt.figure(figsize=(14, 6))

        # Vista 1: Corte transversal
        ax1 = fig.add_subplot(121)

        # Reactor (círculo)
        theta = np.linspace(0, 2*np.pi, 100)
        R_m = D_m / 2
        x_reactor = R_m * np.cos(theta)
        y_reactor = R_m * np.sin(theta)
        ax1.plot(x_reactor * 1000, y_reactor * 1000, 'k-', linewidth=2, label='Pared reactor')

        # Ribbon impeller
        R_ribbon = ribbon['radio_m']
        x_ribbon = R_ribbon * np.cos(theta)
        y_ribbon = R_ribbon * np.sin(theta)
        ax1.plot(x_ribbon * 1000, y_ribbon * 1000, 'b--', linewidth=2, label='Ribbon impeller')

        # Serpentín (círculo aproximado)
        R_serpentin = serpentin['diametro_m'] / 2
        x_serpentin = R_serpentin * np.cos(theta)
        y_serpentin = R_serpentin * np.sin(theta)
        ax1.plot(x_serpentin * 1000, y_serpentin * 1000, 'r:', linewidth=2, label='Serpentín')

        # Deflectores
        for angulo in deflectores['angulos_deg']:
            angulo_rad = np.deg2rad(angulo)
            x_def = (R_m - deflectores['separacion_pared_m']) * np.cos(angulo_rad)
            y_def = (R_m - deflectores['separacion_pared_m']) * np.sin(angulo_rad)
            ancho = deflectores['ancho_m']
            # Dibujar deflector como línea
            dx = ancho/2 * np.cos(angulo_rad + np.pi/2)
            dy = ancho/2 * np.sin(angulo_rad + np.pi/2)
            ax1.plot([x_def*1000 - dx*1000, x_def*1000 + dx*1000],
                    [y_def*1000 - dy*1000, y_def*1000 + dy*1000],
                    'g-', linewidth=3)

        ax1.set_xlabel('X (mm)')
        ax1.set_ylabel('Y (mm)')
        ax1.set_title('Corte Transversal del Reactor')
        ax1.axis('equal')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Vista 2: Corte lateral (esquemático)
        ax2 = fig.add_subplot(122)

        # Reactor (rectángulo)
        R_mm = R_m * 1000
        H_mm = H_m * 1000
        ax2.plot([-R_mm, -R_mm], [0, H_mm], 'k-', linewidth=2)
        ax2.plot([R_mm, R_mm], [0, H_mm], 'k-', linewidth=2)
        ax2.plot([-R_mm, R_mm], [0, 0], 'k-', linewidth=2)

        # Ribbon (línea central indicativa)
        H_ribbon_mm = ribbon['altura_m'] * 1000
        ax2.plot([0, 0], [0, H_ribbon_mm], 'b--', linewidth=2, label='Ribbon')

        # Serpentín (líneas helicoidales aproximadas)
        n_espiras = serpentin['n_espiras']
        H_serpentin_mm = serpentin['altura_m'] * 1000
        z_espiras = np.linspace(0, H_serpentin_mm, n_espiras)
        for z in z_espiras:
            ax2.plot([R_mm*0.95], [z], 'ro', markersize=4)

        # Deflector (línea vertical)
        H_def_mm = deflectores['altura_m'] * 1000
        ax2.plot([R_mm*0.9, R_mm*0.9], [0, H_def_mm], 'g-', linewidth=3, label='Deflector')

        ax2.set_xlabel('Radio (mm)')
        ax2.set_ylabel('Altura (mm)')
        ax2.set_title('Corte Lateral del Reactor')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_xlim(-R_mm*1.1, R_mm*1.1)

        plt.tight_layout()
        plt.savefig('resultados/geometria_reactor_20L.png', dpi=150)
        print(f"\n✓ Gráfica guardada: resultados/geometria_reactor_20L.png")

    def guardar_especificaciones(self, D_m, H_m, ribbon, serpentin, deflectores):
        """Guardar especificaciones completas en JSON"""
        especificaciones = {
            'reactor': {
                'volumen_L': self.V_L,
                'diametro_m': float(D_m),
                'radio_m': float(D_m/2),
                'altura_m': float(H_m),
                'relacion_H_D': float(H_m/D_m),
                'material': 'Acero inoxidable 316L',
                'acabado_superficial': 'Pulido sanitario'
            },
            'ribbon_impeller': ribbon,
            'serpentin': serpentin,
            'deflectores': deflectores,
            'instrumentacion': {
                'termopozo': 'PT100 de 4 hilos',
                'presion': 'Transmisor 0-2 bar',
                'nivel': 'Radar 26 GHz',
                'pH': 'Electrodo de vidrio (opcional)'
            },
            'conexiones': {
                'entrada_aceite': 'DN50 (2 pulgadas)',
                'entrada_metanol': 'DN25 (1 pulgada)',
                'salida_producto': 'DN50 (2 pulgadas)',
                'drenaje_glicerina': 'DN25 (1 pulgada)',
                'purga': 'DN15 (1/2 pulgada)'
            }
        }

        with open('resultados/especificaciones_reactor.json', 'w', encoding='utf-8') as f:
            json.dump(especificaciones, f, indent=2, ensure_ascii=False)

        print(f"✓ Especificaciones guardadas: resultados/especificaciones_reactor.json")


def main():
    """Función principal"""
    import os
    os.makedirs('resultados', exist_ok=True)

    # Inicializar
    geom = GeometriaReactorPiloto()

    # Calcular dimensiones
    D_m, H_m, R_m = geom.calcular_dimensiones_principales()

    # Calcular componentes
    ribbon = geom.calcular_ribbon_impeller(D_m, H_m)
    serpentin = geom.calcular_serpentin(D_m, H_m)
    deflectores = geom.calcular_deflectores(D_m, H_m)

    # Visualizar
    geom.visualizar_geometria(D_m, H_m, ribbon, serpentin, deflectores)

    # Guardar
    geom.guardar_especificaciones(D_m, H_m, ribbon, serpentin, deflectores)

    print("\n" + "=" * 70)
    print(" " * 20 + "✅ GEOMETRÍA COMPLETADA")
    print("=" * 70)
    print("\nArchivos generados:")
    print("  - resultados/geometria_reactor_20L.png")
    print("  - resultados/especificaciones_reactor.json")
    print("\nEsta geometría está lista para ser importada en software CAD")
    print("o utilizada como entrada para simulaciones CFD.")
    print("=" * 70)


if __name__ == "__main__":
    main()
