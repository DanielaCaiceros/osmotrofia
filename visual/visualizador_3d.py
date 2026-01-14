"""
Osmotrofia - Visualizador 3D con Panda3D
Visualización 3D completa de la colonia fúngica
"""

# NOTA: Este módulo requiere Panda3D instalado
# pip install panda3d

try:
    from direct.showbase.ShowBase import ShowBase
    from panda3d.core import *
    from direct.interval.IntervalGlobal import *
    from direct.task import Task
    PANDA3D_DISPONIBLE = True
except ImportError:
    PANDA3D_DISPONIBLE = False
    print("⚠️  Panda3D no está instalado. Instala con: pip install panda3d")


if PANDA3D_DISPONIBLE:
    class Visualizador3D(ShowBase):
        """
        Visualizador 3D completo usando Panda3D

        Características:
        - Renderizado 3D de hongos
        - Animación en tiempo real
        - Iluminación dinámica basada en datos
        - Cámara interactiva
        """

        def __init__(self, colonia):
            """
            Args:
                colonia: Instancia de ColoniaHongos
            """
            ShowBase.__init__(self)

            self.colonia = colonia
            self.hongos_nodos = []
            self.tiempo = 0

            # Configurar escena
            self.setup_escena()
            self.setup_iluminacion()
            self.setup_camara()

            # Generar hongos 3D
            self.generar_hongos_3d()

            # Agregar tarea de actualización
            self.taskMgr.add(self.update_task, "UpdateTask")

            print("🍄 Visualizador 3D inicializado")
            print("📹 Controles de cámara:")
            print("   - Click derecho + arrastrar: Rotar")
            print("   - Scroll: Zoom")

        def setup_escena(self):
            """Configura el ambiente 3D"""
            # Color de fondo (sustrato oscuro)
            self.setBackgroundColor(0.1, 0.1, 0.1)

            # Crear plano base (sustrato)
            self.crear_sustrato()

        def crear_sustrato(self):
            """Crea el plano base que representa el sustrato"""
            # Plano simple
            cm = CardMaker('sustrato')
            cm.setFrame(-20, 20, -20, 20)
            sustrato = self.render.attachNewNode(cm.generate())
            sustrato.setP(-90)  # Rotar para que sea horizontal
            sustrato.setColor(0.15, 0.1, 0.08, 1)  # Marrón oscuro

        def setup_iluminacion(self):
            """Configura iluminación dinámica"""
            # Luz ambiente (basada en batería/humedad)
            self.luz_ambiente = AmbientLight('ambiente')
            self.luz_ambiente.setColor((0.3, 0.3, 0.3, 1))
            self.luz_ambiente_np = self.render.attachNewNode(self.luz_ambiente)
            self.render.setLight(self.luz_ambiente_np)

            # Luz direccional (simula "luz solar" basada en CPU)
            self.luz_direccional = DirectionalLight('direccional')
            self.luz_direccional.setColor((0.8, 0.7, 0.6, 1))
            self.luz_dir_np = self.render.attachNewNode(self.luz_direccional)
            self.luz_dir_np.setHpr(45, -60, 0)
            self.render.setLight(self.luz_dir_np)

        def setup_camara(self):
            """Configura la cámara"""
            self.camera.setPos(0, -25, 15)
            self.camera.lookAt(0, 0, 0)

            # Habilitar control de cámara con mouse (opcional)
            # self.enableMouse()

        def crear_hongo_geometria(self, props):
            """
            Crea la geometría 3D de un hongo

            Args:
                props: Propiedades del hongo

            Returns:
                NodePath: Nodo del hongo
            """
            hongo_root = self.render.attachNewNode(f"hongo_{props['id']}")

            # Posición
            x, y, z = props['posicion']
            hongo_root.setPos(x, y, z)

            # CAP (esfera aplastada)
            from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter
            from panda3d.core import Geom, GeomTriangles, GeomNode

            # Usar modelos procedurales simples o cargar modelos
            # Por ahora, usar esferas y cilindros primitivos

            # Cap (usar loader de modelos básicos)
            cap = loader.loadModel("models/misc/sphere")
            cap.reparentTo(hongo_root)

            # Escalar para forma de cap
            cap_radio = props['forma']['cap_radio'] * props['escala']
            cap_altura = props['forma']['cap_altura'] * props['escala']
            cap.setScale(cap_radio, cap_radio, cap_altura)
            cap.setZ(props['forma']['stem_altura'] * props['escala'])

            # Color del cap
            color = props['color']
            cap.setColor(color['r'], color['g'], color['b'], 1)

            # Stem (cilindro)
            stem = loader.loadModel("models/misc/cylinder")
            stem.reparentTo(hongo_root)

            stem_grosor = props['forma']['stem_grosor'] * props['escala']
            stem_altura = props['forma']['stem_altura'] * props['escala']
            stem.setScale(stem_grosor, stem_grosor, stem_altura)
            stem.setZ(stem_altura / 2)

            # Color del stem (más oscuro)
            stem.setColor(color['r'] * 0.7, color['g'] * 0.7, color['b'] * 0.7, 1)

            # Bioluminiscencia (luz puntual)
            if props['bioluminiscente']:
                luz_bio = PointLight(f'bio_{props["id"]}')
                luz_bio.setColor((color['r'], color['g'], color['b'], 1))
                luz_bio_np = hongo_root.attachNewNode(luz_bio)
                luz_bio_np.setZ(stem_altura)
                hongo_root.setLight(luz_bio_np)

            return hongo_root

        def generar_hongos_3d(self):
            """Genera todos los hongos 3D de la colonia"""
            hongos_props = self.colonia.get_hongos_render(self.tiempo)

            for props in hongos_props:
                try:
                    hongo_nodo = self.crear_hongo_geometria(props)
                    self.hongos_nodos.append({
                        'nodo': hongo_nodo,
                        'props_id': props['id']
                    })
                except Exception as e:
                    print(f"Error creando hongo: {e}")

        def update_task(self, task):
            """
            Tarea de actualización (llamada cada frame)

            Args:
                task: Objeto Task de Panda3D
            """
            self.tiempo = task.time

            # Actualizar propiedades de hongos
            hongos_props = self.colonia.get_hongos_render(self.tiempo)

            # Actualizar cada hongo (animación de pulsación)
            for i, hongo_data in enumerate(self.hongos_nodos):
                if i < len(hongos_props):
                    props = hongos_props[i]

                    # Actualizar escala (pulsación)
                    hongo_data['nodo'].setScale(props['escala'])

            return Task.cont


def iniciar_visualizador_3d(colonia):
    """
    Función helper para iniciar el visualizador 3D

    Args:
        colonia: Instancia de ColoniaHongos
    """
    if not PANDA3D_DISPONIBLE:
        print("❌ No se puede iniciar visualizador 3D sin Panda3D")
        print("   Instala con: pip install panda3d")
        return None

    viz = Visualizador3D(colonia)
    viz.run()
    return viz


# Test del módulo
if __name__ == "__main__":
    if not PANDA3D_DISPONIBLE:
        print("Este módulo requiere Panda3D instalado.")
        exit(1)

    from visual.colonia import ColoniaHongos

    print("=== OSMOTROFIA - Visualizador 3D ===\n")

    # Simular datos
    params_sistema = {
        'hardware': {
            'temperatura': {'cpu': 68},
            'bateria': {'porcentaje': 80}
        },
        'rendimiento': {
            'cpu': {'uso_porcentaje': 50},
            'ram': {'uso_porcentaje': 65},
            'almacenamiento': {'uso_porcentaje': 70}
        }
    }

    params_gmail = {
        'importante': 50,
        'spam': 30,
        'promociones': 80,
        'social': 40,
        'no_leidos': 20
    }

    # Crear colonia
    colonia = ColoniaHongos(radio_colonia=10)
    colonia.generar_desde_datos(params_sistema, params_gmail)

    # Iniciar visualizador 3D
    print("Iniciando visualizador 3D...")
    iniciar_visualizador_3d(colonia)
