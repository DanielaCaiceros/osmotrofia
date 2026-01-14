"""
Osmotrofia - Hongo Digital
Clase que representa un hongo individual con sus propiedades visuales
"""

import math
import random


class HongoDigital:
    """
    Representa un hongo digital individual que descompone datos

    Cada hongo tiene:
    - Tipo (basado en tipo de email/dato)
    - Propiedades visuales (color, tamaño, forma)
    - Estado metabólico (basado en uso de CPU)
    - Características ambientales (basadas en temperatura, batería, etc.)
    """

    def __init__(self, tipo_nutriente='importante', posicion=(0, 0, 0)):
        """
        Inicializa un hongo digital

        Args:
            tipo_nutriente: Tipo de dato que descompone ('importante', 'spam', etc.)
            posicion: Tupla (x, y, z) de posición en el espacio 3D
        """
        self.tipo = tipo_nutriente
        self.posicion = posicion

        # Propiedades visuales base
        self.color = {'r': 1.0, 'g': 1.0, 'b': 1.0}
        self.escala = 1.0
        self.brillo = 0.5
        self.saturacion = 1.0

        # Propiedades animadas
        self.fase_pulsacion = random.uniform(0, 2 * math.pi)
        self.velocidad_pulsacion = 1.0

        # Propiedades de forma
        self.forma = {
            'cap_radio': 1.0,
            'cap_altura': 0.5,
            'stem_altura': 1.5,
            'stem_grosor': 0.3,
            'gills_visibles': True
        }

        # Estado
        self.bioluminiscente = False
        self.marchito = False
        self.tiene_manchas = False

        # ID único
        self.id = id(self)

    def actualizar_por_nutriente(self, caracteristicas_nutriente):
        """
        Actualiza el hongo basado en características del nutriente

        Args:
            caracteristicas_nutriente: Dict con color, forma, tamaño, etc.
        """
        # Color base
        if 'color' in caracteristicas_nutriente:
            self.color = caracteristicas_nutriente['color']

        # Tamaño
        if 'tamano_final' in caracteristicas_nutriente:
            self.escala = caracteristicas_nutriente['tamano_final']
        elif 'tamano_base' in caracteristicas_nutriente:
            self.escala = caracteristicas_nutriente['tamano_base']

        # Forma
        if caracteristicas_nutriente.get('forma') == 'irregular_deforme':
            # Hongos de spam son deformes
            self.forma['cap_radio'] *= random.uniform(0.7, 1.3)
            self.forma['stem_altura'] *= random.uniform(0.6, 0.9)
            self.tiene_manchas = True

        elif caracteristicas_nutriente.get('forma') == 'redondeada_grande':
            # Hongos importantes son grandes y redondeados
            self.forma['cap_radio'] *= 1.2
            self.forma['cap_altura'] *= 1.1

        # Bioluminiscencia (para no leídos)
        if caracteristicas_nutriente.get('bioluminiscencia'):
            self.bioluminiscente = True
            self.brillo = caracteristicas_nutriente.get('brillo_intensidad', 0.8)

    def actualizar_por_ambiente(self, ambiente):
        """
        Actualiza el hongo basado en condiciones ambientales

        Args:
            ambiente: Dict con temperatura, humedad, metabolismo, etc.
        """
        # Temperatura afecta color
        if 'color' in ambiente:
            # Mezclar color ambiente con color base
            factor_ambiente = 0.3
            self.color['r'] = self.color['r'] * (1 - factor_ambiente) + ambiente['color']['r'] * factor_ambiente
            self.color['g'] = self.color['g'] * (1 - factor_ambiente) + ambiente['color']['g'] * factor_ambiente
            self.color['b'] = self.color['b'] * (1 - factor_ambiente) + ambiente['color']['b'] * factor_ambiente

        # Velocidad de crecimiento afecta animación
        if 'velocidad_crecimiento' in ambiente:
            self.velocidad_pulsacion = ambiente['velocidad_crecimiento']

        # Humedad afecta brillo
        if 'brillo' in ambiente:
            if not self.bioluminiscente:  # No override bioluminiscencia
                self.brillo = ambiente['brillo']

        # Saturación de color
        if 'saturacion' in ambiente:
            self.saturacion = ambiente['saturacion']

        # Estado marchito
        if ambiente.get('estado') == 'extremo':
            self.marchito = True
            self.forma['cap_altura'] *= 0.7
            self.forma['stem_altura'] *= 0.8

    def actualizar_por_ram(self, caracteristicas_ram):
        """
        Actualiza basado en disponibilidad de RAM (micelio)

        Args:
            caracteristicas_ram: Dict con densidad de micelio, porosidad, etc.
        """
        # Grosor del stem basado en densidad de micelio
        self.forma['stem_grosor'] *= caracteristicas_ram.get('densidad_micelio', 1.0)

        # Manchas negras si hay sobrecarga
        if caracteristicas_ram.get('manchas_negras'):
            self.tiene_manchas = True

    def actualizar_por_disco(self, caracteristicas_disco):
        """
        Actualiza basado en espacio en disco

        Args:
            caracteristicas_disco: Dict con expansión, densidad, etc.
        """
        # Si hay hacinamiento, deformar
        if caracteristicas_disco.get('hongos_deformados'):
            self.forma['cap_radio'] *= random.uniform(0.7, 0.9)
            self.escala *= 0.8

        # Si están muriendo
        if caracteristicas_disco.get('hongos_muriendo'):
            self.marchito = True

    def calcular_pulsacion(self, tiempo):
        """
        Calcula la pulsación actual del hongo (animación de "respiración")

        Args:
            tiempo: Tiempo actual en segundos

        Returns:
            float: Factor de escala de pulsación (0.95 - 1.05)
        """
        if self.marchito:
            return 1.0  # Sin pulsación si está marchito

        fase = self.fase_pulsacion + (tiempo * self.velocidad_pulsacion)
        pulsacion = 1.0 + 0.05 * math.sin(fase)
        return pulsacion

    def get_color_final(self):
        """
        Obtiene el color final considerando saturación y estado

        Returns:
            dict: Color RGB final
        """
        color_final = dict(self.color)

        # Aplicar saturación
        if self.saturacion < 1.0:
            gris = (color_final['r'] + color_final['g'] + color_final['b']) / 3
            for c in ['r', 'g', 'b']:
                color_final[c] = color_final[c] * self.saturacion + gris * (1 - self.saturacion)

        # Si está marchito, oscurecer
        if self.marchito:
            for c in ['r', 'g', 'b']:
                color_final[c] *= 0.5

        # Si tiene manchas, agregar tono verdoso oscuro
        if self.tiene_manchas:
            color_final['g'] += 0.1
            color_final['r'] *= 0.8
            color_final['b'] *= 0.8

        return color_final

    def get_propiedades_render(self, tiempo=0):
        """
        Obtiene todas las propiedades necesarias para renderizar

        Args:
            tiempo: Tiempo actual para animación

        Returns:
            dict: Propiedades completas para renderizado
        """
        pulsacion = self.calcular_pulsacion(tiempo)

        return {
            'posicion': self.posicion,
            'escala': self.escala * pulsacion,
            'color': self.get_color_final(),
            'brillo': self.brillo,
            'forma': self.forma,
            'bioluminiscente': self.bioluminiscente,
            'marchito': self.marchito,
            'tiene_manchas': self.tiene_manchas,
            'tipo': self.tipo,
            'id': self.id
        }

    def __repr__(self):
        return f"HongoDigital(tipo={self.tipo}, pos={self.posicion}, escala={self.escala:.2f})"


# Test del módulo
if __name__ == "__main__":
    print("=== OSMOTROFIA - Hongo Digital ===\n")

    # Crear hongos de diferentes tipos
    hongo_importante = HongoDigital('importante', posicion=(0, 0, 0))
    hongo_spam = HongoDigital('spam', posicion=(2, 0, 0))

    # Simular características de nutrientes
    from core.mapper import MapperBiologico

    mapper = MapperBiologico()

    # Actualizar con características
    carac_importante = mapper.mapear_tipo_email('importante', 50)
    hongo_importante.actualizar_por_nutriente(carac_importante)

    carac_spam = mapper.mapear_tipo_email('spam', 30)
    hongo_spam.actualizar_por_nutriente(carac_spam)

    # Simular ambiente
    ambiente = mapper.mapear_temperatura_cpu(75)
    hongo_importante.actualizar_por_ambiente(ambiente)
    hongo_spam.actualizar_por_ambiente(ambiente)

    # Obtener propiedades de render
    print("Hongo Importante:")
    props = hongo_importante.get_propiedades_render(tiempo=0)
    print(f"  Color: RGB({props['color']['r']:.2f}, {props['color']['g']:.2f}, {props['color']['b']:.2f})")
    print(f"  Escala: {props['escala']:.2f}")
    print(f"  Brillo: {props['brillo']:.2f}")
    print(f"  Bioluminiscente: {props['bioluminiscente']}\n")

    print("Hongo Spam:")
    props = hongo_spam.get_propiedades_render(tiempo=0)
    print(f"  Color: RGB({props['color']['r']:.2f}, {props['color']['g']:.2f}, {props['color']['b']:.2f})")
    print(f"  Escala: {props['escala']:.2f}")
    print(f"  Manchas: {props['tiene_manchas']}")
