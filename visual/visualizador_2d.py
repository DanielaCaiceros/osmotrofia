"""
Osmotrofia - Visualizador 2D Simple
Visualización con matplotlib para pruebas rápidas
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
import time


class Visualizador2D:
    """
    Visualizador simple en 2D usando matplotlib
    Útil para prototipar antes de pasar a 3D
    """

    def __init__(self, colonia):
        """
        Args:
            colonia: Instancia de ColoniaHongos
        """
        self.colonia = colonia
        self.fig, self.ax = plt.subplots(figsize=(12, 12))
        self.tiempo_inicio = time.time()

        # Configurar plot
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('#1a1a1a')  # Fondo oscuro (sustrato)
        self.fig.patch.set_facecolor('#0a0a0a')

        # Título
        self.title = self.ax.set_title('OSMOTROFIA - Colonia Fúngica Digital',
                                       color='white', fontsize=16, pad=20)

        # Texto de estadísticas
        self.stats_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes,
                                       verticalalignment='top', color='white',
                                       fontsize=10, family='monospace',
                                       bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

    def dibujar_hongo(self, props):
        """
        Dibuja un hongo individual

        Args:
            props: Propiedades del hongo (de get_propiedades_render)
        """
        x, y, _ = props['posicion']
        escala = props['escala']
        color_dict = props['color']
        color = (color_dict['r'], color_dict['g'], color_dict['b'])

        # Cap (círculo)
        cap_radio = props['forma']['cap_radio'] * escala * 0.5
        cap = patches.Circle((x, y), cap_radio, color=color, alpha=0.8)
        self.ax.add_patch(cap)

        # Stem (línea o rectángulo)
        stem_altura = props['forma']['stem_altura'] * escala * 0.3
        stem_grosor = props['forma']['stem_grosor'] * escala * 0.1

        stem = patches.Rectangle(
            (x - stem_grosor/2, y - stem_altura),
            stem_grosor, stem_altura,
            color=color, alpha=0.6
        )
        self.ax.add_patch(stem)

        # Bioluminiscencia (halo)
        if props['bioluminiscente']:
            halo = patches.Circle(
                (x, y), cap_radio * 1.5,
                color=color, alpha=0.3, linewidth=0
            )
            self.ax.add_patch(halo)

        # Manchas (puntos oscuros)
        if props['tiene_manchas']:
            for _ in range(3):
                offset_x = np.random.uniform(-cap_radio*0.5, cap_radio*0.5)
                offset_y = np.random.uniform(-cap_radio*0.5, cap_radio*0.5)
                mancha = patches.Circle(
                    (x + offset_x, y + offset_y),
                    cap_radio * 0.2,
                    color=(0.2, 0.3, 0.1), alpha=0.7
                )
                self.ax.add_patch(mancha)

    def actualizar(self, frame):
        """
        Actualiza el frame de animación

        Args:
            frame: Número de frame
        """
        # Limpiar
        self.ax.clear()

        # Reconfigurar
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('#1a1a1a')
        self.ax.grid(True, alpha=0.1, color='white')

        # Tiempo actual
        tiempo_actual = time.time() - self.tiempo_inicio

        # Dibujar todos los hongos
        hongos_props = self.colonia.get_hongos_render(tiempo_actual)

        for props in hongos_props:
            self.dibujar_hongo(props)

        # Actualizar estadísticas
        stats = self.colonia.get_estadisticas()
        stats_text = f"""OSMOTROFIA - Estado del Ecosistema

Total hongos: {stats['total_hongos']}
Bioluminiscentes: {stats['bioluminiscentes']}
Marchitos: {stats['marchitos']}

Salud: {stats['salud']['nivel'].upper()}
Nivel: {stats['salud']['salud_numerica']}%

Distribución:
"""
        for tipo, cantidad in stats['tipos'].items():
            stats_text += f"  {tipo}: {cantidad}\n"

        self.ax.text(0.02, 0.98, stats_text, transform=self.ax.transAxes,
                    verticalalignment='top', color='white',
                    fontsize=9, family='monospace',
                    bbox=dict(boxstyle='round', facecolor='black', alpha=0.8))

        # Título
        self.ax.set_title(
            f'OSMOTROFIA - Colonia Fúngica Digital | {stats["salud"]["descripcion"]}',
            color='white', fontsize=14, pad=20
        )

    def mostrar_estatico(self):
        """Muestra una imagen estática de la colonia"""
        self.actualizar(0)
        plt.show()

    def animar(self, intervalo=100):
        """
        Inicia animación

        Args:
            intervalo: Milisegundos entre frames
        """
        anim = FuncAnimation(
            self.fig, self.actualizar,
            interval=intervalo, blit=False
        )
        plt.show()


# Test del módulo
if __name__ == "__main__":
    from visual.colonia import ColoniaHongos

    print("=== OSMOTROFIA - Visualizador 2D ===\n")

    # Simular datos
    params_sistema = {
        'hardware': {
            'temperatura': {'cpu': 72},
            'bateria': {'porcentaje': 65}
        },
        'rendimiento': {
            'cpu': {'uso_porcentaje': 55},
            'ram': {'uso_porcentaje': 70},
            'almacenamiento': {'uso_porcentaje': 75}
        }
    }

    params_gmail = {
        'importante': 60,
        'spam': 40,
        'promociones': 100,
        'social': 30,
        'no_leidos': 35
    }

    # Crear colonia
    colonia = ColoniaHongos(radio_colonia=12)
    colonia.generar_desde_datos(params_sistema, params_gmail)

    # Visualizar
    viz = Visualizador2D(colonia)

    print("Mostrando visualización 2D...")
    print("Cierra la ventana para continuar.\n")

    # Mostrar estático
    viz.mostrar_estatico()

    # O animar (descomentar para ver animación)
    # viz.animar(intervalo=50)
