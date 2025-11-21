"""
Práctica 9 - Parte A: Cálculo de Escalado de Reactores

Escalar de reactor de laboratorio (350 mL) a reactor piloto (20 L)
aplicando criterios de similitud hidrodinámica.

Autor: Sistema de Modelado de Biodiesel
"""

import json
import numpy as np
import matplotlib.pyplot as plt


class CalculadorEscalado:
    """Calculador de parámetros de escalado de reactores batch"""

    def __init__(self, config_file='config.json'):
        """Inicializar con configuración"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # Datos reactor laboratorio
        self.V_lab_mL = self.config['reactor_laboratorio']['volumen_mL']
        self.D_lab_cm = self.config['reactor_laboratorio']['diametro_cm']
        self.H_lab_cm = self.config['reactor_laboratorio']['altura_cm']
        self.D_imp_lab_cm = self.config['reactor_laboratorio']['diametro_impulsor_cm']
        self.N_lab_rpm = self.config['reactor_laboratorio']['rpm']
        self.P_lab_W = self.config['reactor_laboratorio']['potencia_W']

        # Datos reactor piloto
        self.V_piloto_L = self.config['reactor_piloto']['volumen_L']
        self.relacion_H_D = self.config['reactor_piloto']['relacion_H_D']

        # Propiedades del fluido (mezcla aceite-metanol a 60°C)
        self.rho = 850  # kg/m³
        self.mu = 0.0045  # Pa·s

        print("=" * 70)
        print(" " * 20 + "ESCALADO DE REACTORES BATCH")
        print("=" * 70)
        print(f"\nReactor Laboratorio:")
        print(f"  - Volumen: {self.V_lab_mL} mL")
        print(f"  - Diámetro: {self.D_lab_cm} cm")
        print(f"  - Diámetro impulsor: {self.D_imp_lab_cm} cm")
        print(f"  - Velocidad: {self.N_lab_rpm} rpm")
        print(f"  - Potencia: {self.P_lab_W} W")

        print(f"\nReactor Piloto:")
        print(f"  - Volumen objetivo: {self.V_piloto_L} L")
        print(f"  - Relación H/D: {self.relacion_H_D}")

    def calcular_geometria_piloto(self):
        """Calcular geometría del reactor piloto"""
        # Volumen = π * D² / 4 * H
        # Con H = relacion_H_D * D
        # V = π * D² / 4 * relacion_H_D * D = π * relacion_H_D * D³ / 4

        V_m3 = self.V_piloto_L / 1000
        D_m = (4 * V_m3 / (np.pi * self.relacion_H_D))**(1/3)
        H_m = self.relacion_H_D * D_m

        # Diámetro del impulsor (típicamente D_imp = 0.5 * D_reactor)
        D_imp_m = 0.5 * D_m

        self.D_piloto_m = D_m
        self.H_piloto_m = H_m
        self.D_imp_piloto_m = D_imp_m

        print(f"\n" + "=" * 70)
        print("GEOMETRÍA DEL REACTOR PILOTO CALCULADA")
        print("=" * 70)
        print(f"Diámetro reactor:   {D_m*100:.2f} cm ({D_m:.4f} m)")
        print(f"Altura líquido:     {H_m*100:.2f} cm ({H_m:.4f} m)")
        print(f"Diámetro impulsor:  {D_imp_m*100:.2f} cm ({D_imp_m:.4f} m)")

        return D_m, H_m, D_imp_m

    def criterio_P_V_constante(self):
        """Criterio 1: Mantener P/V constante"""
        # P/V = K * N³ * D⁵ / V
        # Para mantener P/V constante: N_piloto³ * D_piloto⁵ / V_piloto = N_lab³ * D_lab⁵ / V_lab

        V_lab_m3 = self.V_lab_mL / 1e6
        D_lab_m = self.D_lab_cm / 100
        D_imp_lab_m = self.D_imp_lab_cm / 100
        N_lab_rps = self.N_lab_rpm / 60

        V_piloto_m3 = self.V_piloto_L / 1000
        D_imp_piloto_m = self.D_imp_piloto_m

        # N_piloto = N_lab * (V_piloto/V_lab)^(1/3) * (D_imp_lab/D_imp_piloto)^(5/3)
        factor_escala = self.V_piloto_L / (self.V_lab_mL / 1000)  # L/L
        N_piloto_rps = N_lab_rps * (factor_escala)**(1/3) * (D_imp_lab_m / D_imp_piloto_m)**(5/3)
        N_piloto_rpm = N_piloto_rps * 60

        # Calcular potencia
        # Número de potencia Np ≈ 5 para turbinas (aproximación)
        Np = 5
        P_piloto_W = Np * self.rho * (N_piloto_rps**3) * (D_imp_piloto_m**5)

        return N_piloto_rpm, P_piloto_W

    def criterio_Re_similar(self):
        """Criterio 2: Mantener número de Reynolds similar"""
        # Re = ρ * N * D² / μ
        # Para Re constante: N_piloto * D_piloto² = N_lab * D_lab²

        D_imp_lab_m = self.D_imp_lab_cm / 100
        D_imp_piloto_m = self.D_imp_piloto_m
        N_lab_rps = self.N_lab_rpm / 60

        N_piloto_rps = N_lab_rps * (D_imp_lab_m / D_imp_piloto_m)**2
        N_piloto_rpm = N_piloto_rps * 60

        return N_piloto_rpm

    def criterio_v_tip_constante(self):
        """Criterio 3: Mantener velocidad en punta del impulsor constante"""
        # v_tip = π * D * N
        # Para v_tip constante: N_piloto * D_piloto = N_lab * D_lab

        D_imp_lab_m = self.D_imp_lab_cm / 100
        D_imp_piloto_m = self.D_imp_piloto_m
        N_lab_rps = self.N_lab_rpm / 60

        N_piloto_rps = N_lab_rps * (D_imp_lab_m / D_imp_piloto_m)
        N_piloto_rpm = N_piloto_rps * 60

        return N_piloto_rpm

    def criterio_tiempo_mezcla_constante(self):
        """Criterio 4: Mantener tiempo de mezclado similar"""
        # θ_m ∝ 1 / (N * D)
        # Para θ_m constante: N_piloto * D_piloto = N_lab * D_lab

        # Este criterio es similar al de v_tip
        return self.criterio_v_tip_constante()

    def calcular_numeros_adimensionales(self, N_rpm, D_m):
        """Calcular números adimensionales"""
        N_rps = N_rpm / 60

        # Número de Reynolds
        Re = self.rho * N_rps * (D_m**2) / self.mu

        # Número de Potencia (aproximado para turbinas)
        Np = 5.0

        # Velocidad en punta de impulsor
        v_tip = np.pi * D_m * N_rps  # m/s

        return Re, Np, v_tip

    def comparar_criterios(self):
        """Comparar todos los criterios de escalado"""
        print(f"\n" + "=" * 70)
        print("COMPARACIÓN DE CRITERIOS DE ESCALADO")
        print("=" * 70)

        resultados = []

        # Criterio 1: P/V constante
        N1, P1 = self.criterio_P_V_constante()
        Re1, Np1, v1 = self.calcular_numeros_adimensionales(N1, self.D_imp_piloto_m)
        resultados.append(('P/V constante', N1, P1, Re1, v1))
        print(f"\n1. Criterio P/V constante:")
        print(f"   - N_piloto = {N1:.1f} rpm")
        print(f"   - P_piloto = {P1:.2f} W")
        print(f"   - Re = {Re1:.0f}")
        print(f"   - v_tip = {v1:.3f} m/s")

        # Criterio 2: Re similar
        N2 = self.criterio_Re_similar()
        Re2, Np2, v2 = self.calcular_numeros_adimensionales(N2, self.D_imp_piloto_m)
        P2 = Np2 * self.rho * ((N2/60)**3) * (self.D_imp_piloto_m**5)
        resultados.append(('Re similar', N2, P2, Re2, v2))
        print(f"\n2. Criterio Re similar:")
        print(f"   - N_piloto = {N2:.1f} rpm")
        print(f"   - P_piloto = {P2:.2f} W")
        print(f"   - Re = {Re2:.0f}")
        print(f"   - v_tip = {v2:.3f} m/s")

        # Criterio 3: v_tip constante
        N3 = self.criterio_v_tip_constante()
        Re3, Np3, v3 = self.calcular_numeros_adimensionales(N3, self.D_imp_piloto_m)
        P3 = Np3 * self.rho * ((N3/60)**3) * (self.D_imp_piloto_m**5)
        resultados.append(('v_tip constante', N3, P3, Re3, v3))
        print(f"\n3. Criterio v_tip constante:")
        print(f"   - N_piloto = {N3:.1f} rpm")
        print(f"   - P_piloto = {P3:.2f} W")
        print(f"   - Re = {Re3:.0f}")
        print(f"   - v_tip = {v3:.3f} m/s")

        # Criterio 4: Tiempo de mezcla
        N4 = self.criterio_tiempo_mezcla_constante()
        Re4, Np4, v4 = self.calcular_numeros_adimensionales(N4, self.D_imp_piloto_m)
        P4 = Np4 * self.rho * ((N4/60)**3) * (self.D_imp_piloto_m**5)
        resultados.append(('Tiempo mezcla', N4, P4, Re4, v4))
        print(f"\n4. Criterio tiempo de mezcla constante:")
        print(f"   - N_piloto = {N4:.1f} rpm")
        print(f"   - P_piloto = {P4:.2f} W")
        print(f"   - Re = {Re4:.0f}")
        print(f"   - v_tip = {v4:.3f} m/s")

        # Comparación con laboratorio
        Re_lab, Np_lab, v_lab = self.calcular_numeros_adimensionales(
            self.N_lab_rpm, self.D_imp_lab_cm / 100
        )
        print(f"\n" + "-" * 70)
        print(f"REFERENCIA - Reactor Laboratorio:")
        print(f"   - N_lab = {self.N_lab_rpm:.1f} rpm")
        print(f"   - P_lab = {self.P_lab_W:.2f} W")
        print(f"   - Re_lab = {Re_lab:.0f}")
        print(f"   - v_tip_lab = {v_lab:.3f} m/s")
        print("=" * 70)

        return resultados

    def graficar_comparacion(self, resultados):
        """Graficar comparación de criterios"""
        nombres = [r[0] for r in resultados]
        rpm_values = [r[1] for r in resultados]
        potencia_values = [r[2] for r in resultados]
        re_values = [r[3] for r in resultados]

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # RPM
        axes[0].bar(nombres, rpm_values, color='steelblue')
        axes[0].axhline(y=self.N_lab_rpm, color='red', linestyle='--', label='Lab')
        axes[0].set_ylabel('RPM')
        axes[0].set_title('Velocidad de Agitación')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].legend()

        # Potencia
        axes[1].bar(nombres, potencia_values, color='coral')
        axes[1].axhline(y=self.P_lab_W, color='red', linestyle='--', label='Lab')
        axes[1].set_ylabel('Potencia (W)')
        axes[1].set_title('Potencia de Agitación')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].legend()

        # Reynolds
        Re_lab, _, _ = self.calcular_numeros_adimensionales(
            self.N_lab_rpm, self.D_imp_lab_cm / 100
        )
        axes[2].bar(nombres, re_values, color='lightgreen')
        axes[2].axhline(y=Re_lab, color='red', linestyle='--', label='Lab')
        axes[2].set_ylabel('Número de Reynolds')
        axes[2].set_title('Régimen de Flujo')
        axes[2].tick_params(axis='x', rotation=45)
        axes[2].legend()

        plt.tight_layout()
        plt.savefig('resultados/criterios_escalado.png', dpi=150)
        print(f"\n✓ Gráfica guardada: resultados/criterios_escalado.png")

    def guardar_resultados(self, resultados):
        """Guardar resultados en JSON"""
        salida = {
            'reactor_laboratorio': {
                'volumen_mL': self.V_lab_mL,
                'diametro_cm': self.D_lab_cm,
                'diametro_impulsor_cm': self.D_imp_lab_cm,
                'rpm': self.N_lab_rpm,
                'potencia_W': self.P_lab_W
            },
            'reactor_piloto': {
                'volumen_L': self.V_piloto_L,
                'diametro_m': float(self.D_piloto_m),
                'altura_m': float(self.H_piloto_m),
                'diametro_impulsor_m': float(self.D_imp_piloto_m)
            },
            'criterios_escalado': []
        }

        for nombre, rpm, potencia, re, v_tip in resultados:
            salida['criterios_escalado'].append({
                'nombre': nombre,
                'rpm': float(rpm),
                'potencia_W': float(potencia),
                'numero_reynolds': float(re),
                'velocidad_punta_m_s': float(v_tip)
            })

        with open('resultados/criterios_escalado.json', 'w', encoding='utf-8') as f:
            json.dump(salida, f, indent=2, ensure_ascii=False)

        print(f"✓ Resultados guardados: resultados/criterios_escalado.json")


def main():
    """Función principal"""
    import os
    os.makedirs('resultados', exist_ok=True)

    # Inicializar calculador
    calc = CalculadorEscalado()

    # Calcular geometría
    calc.calcular_geometria_piloto()

    # Comparar criterios
    resultados = calc.comparar_criterios()

    # Graficar
    calc.graficar_comparacion(resultados)

    # Guardar resultados
    calc.guardar_resultados(resultados)

    print("\n" + "=" * 70)
    print(" " * 20 + "✅ ANÁLISIS COMPLETADO")
    print("=" * 70)
    print("\nRECOMENDACIÓN: El criterio de P/V constante es el más común")
    print("en la industria para garantizar eficiencia energética similar.")
    print("\nRevisa analisis.md para responder las preguntas de la práctica.")
    print("=" * 70)


if __name__ == "__main__":
    main()
