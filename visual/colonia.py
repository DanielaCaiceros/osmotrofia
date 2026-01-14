"""
Osmotrofia - Colonia de Hongos
Gestiona múltiples hongos digitales como ecosistema
"""

import random
import math
from visual.hongo_digital import HongoDigital
from core.mapper import MapperBiologico


class ColoniaHongos:
    """
    Gestiona una colonia completa de hongos digitales

    La colonia responde a:
    - Datos de Gmail (nutrientes)
    - Estado del sistema (ambiente)
    - Rendimiento (salud del ecosistema)
    """

    def __init__(self, radio_colonia=10):
        """
        Inicializa una colonia vacía

        Args:
            radio_colonia: Radio máximo de expansión de la colonia
        """
        self.hongos = []
        self.radio_colonia = radio_colonia
        self.mapper = MapperBiologico()

        # Estado global
        self.salud_ecosistema = None
        self.ambiente_actual = None

    def generar_desde_datos(self, params_sistema, params_gmail):
        """
        Genera/actualiza la colonia basándose en datos reales

        Args:
            params_sistema: Parámetros del sistema (de MonitorSistema)
            params_gmail: Nutrientes digitales (de MonitorGmail)
        """
        # Limpiar colonia anterior
        self.hongos = []

        # Calcular salud del ecosistema
        self.salud_ecosistema = self.mapper.calcular_salud_ecosistema(params_sistema)

        # Mapear condiciones ambientales
        temp_cpu = params_sistema['hardware']['temperatura']['cpu']
        bateria = params_sistema['hardware']['bateria']['porcentaje']
        cpu_uso = params_sistema['rendimiento']['cpu']['uso_porcentaje']
        ram_uso = params_sistema['rendimiento']['ram']['uso_porcentaje']
        disco_uso = params_sistema['rendimiento']['almacenamiento']['uso_porcentaje']

        self.ambiente_actual = {
            'temperatura': self.mapper.mapear_temperatura_cpu(temp_cpu),
            'humedad': self.mapper.mapear_bateria(bateria),
            'metabolismo': self.mapper.mapear_cpu_uso(cpu_uso),
            'ram': self.mapper.mapear_ram_uso(ram_uso),
            'disco': self.mapper.mapear_disco_uso(disco_uso)
        }

        # Generar hongos por tipo de email
        tipos_email = ['importante', 'spam', 'promociones', 'social']

        for tipo in tipos_email:
            cantidad = params_gmail.get(tipo, 0)

            # 1 hongo por cada 10 emails (ajustable)
            num_hongos = max(1, cantidad // 10)

            for i in range(num_hongos):
                self._crear_hongo(tipo, cantidad)

        # Aplicar bioluminiscencia a hongos si hay no leídos
        no_leidos = params_gmail.get('no_leidos', 0)
        if no_leidos > 0:
            self._aplicar_bioluminiscencia(no_leidos)

    def _crear_hongo(self, tipo_nutriente, cantidad_total):
        """
        Crea un hongo individual y lo coloca en la colonia

        Args:
            tipo_nutriente: Tipo de email
            cantidad_total: Cantidad total de emails de este tipo
        """
        # Posición basada en patrón de distribución
        posicion = self._calcular_posicion(tipo_nutriente)

        # Crear hongo
        hongo = HongoDigital(tipo_nutriente, posicion)

        # Aplicar características del nutriente
        carac_nutriente = self.mapper.mapear_tipo_email(tipo_nutriente, cantidad_total)
        hongo.actualizar_por_nutriente(carac_nutriente)

        # Aplicar condiciones ambientales
        if self.ambiente_actual:
            hongo.actualizar_por_ambiente(self.ambiente_actual['temperatura'])
            hongo.actualizar_por_ambiente(self.ambiente_actual['humedad'])
            hongo.actualizar_por_ram(self.ambiente_actual['ram'])
            hongo.actualizar_por_disco(self.ambiente_actual['disco'])

        self.hongos.append(hongo)

    def _calcular_posicion(self, tipo_nutriente):
        """
        Calcula posición para un hongo según su tipo y patrón de distribución

        Args:
            tipo_nutriente: Tipo de email

        Returns:
            tuple: (x, y, z) posición
        """
        # Patrón basado en disco (expansión territorial)
        if self.ambiente_actual and self.ambiente_actual['disco']['patron'] == 'circulo_de_hadas':
            # Distribución en anillo (mucho espacio)
            angulo = random.uniform(0, 2 * math.pi)
            radio = random.uniform(self.radio_colonia * 0.6, self.radio_colonia)
            x = radio * math.cos(angulo)
            y = radio * math.sin(angulo)

        elif self.ambiente_actual and self.ambiente_actual['disco']['patron'] == 'agrupado':
            # Distribución compacta
            angulo = random.uniform(0, 2 * math.pi)
            radio = random.uniform(0, self.radio_colonia * 0.5)
            x = radio * math.cos(angulo)
            y = radio * math.sin(angulo)

        elif self.ambiente_actual and self.ambiente_actual['disco']['patron'] == 'apretado':
            # Muy cerca del centro
            angulo = random.uniform(0, 2 * math.pi)
            radio = random.uniform(0, self.radio_colonia * 0.3)
            x = radio * math.cos(angulo)
            y = radio * math.sin(angulo)

        else:
            # Por defecto, distribución aleatoria
            x = random.uniform(-self.radio_colonia, self.radio_colonia)
            y = random.uniform(-self.radio_colonia, self.radio_colonia)

        # z siempre en el suelo (0) o ligeramente variable
        z = random.uniform(-0.1, 0.1)

        # Ajustar según tipo (hongos importantes al centro)
        if tipo_nutriente == 'importante':
            x *= 0.6
            y *= 0.6
        elif tipo_nutriente == 'spam':
            # Spam en periferia
            factor = 1.3
            x *= factor
            y *= factor

        return (x, y, z)

    def _aplicar_bioluminiscencia(self, no_leidos):
        """
        Aplica bioluminiscencia a algunos hongos

        Args:
            no_leidos: Número de emails no leídos
        """
        # Porcentaje de hongos que brillan
        porcentaje = min(no_leidos / 100, 0.5)  # Máximo 50% brillan
        num_brillantes = int(len(self.hongos) * porcentaje)

        # Seleccionar hongos al azar
        hongos_seleccionados = random.sample(self.hongos, min(num_brillantes, len(self.hongos)))

        for hongo in hongos_seleccionados:
            hongo.bioluminiscente = True
            hongo.brillo = 0.8

    def get_hongos_render(self, tiempo):
        """
        Obtiene propiedades de todos los hongos para renderizar

        Args:
            tiempo: Tiempo actual para animación

        Returns:
            list: Lista de dicts con propiedades de render
        """
        return [hongo.get_propiedades_render(tiempo) for hongo in self.hongos]

    def get_estadisticas(self):
        """
        Obtiene estadísticas de la colonia

        Returns:
            dict: Estadísticas
        """
        if not self.hongos:
            return {
                'total_hongos': 0,
                'tipos': {},
                'salud': None
            }

        # Contar por tipo
        tipos = {}
        for hongo in self.hongos:
            tipos[hongo.tipo] = tipos.get(hongo.tipo, 0) + 1

        # Contar bioluminiscentes
        bioluminiscentes = sum(1 for h in self.hongos if h.bioluminiscente)

        # Contar marchitos
        marchitos = sum(1 for h in self.hongos if h.marchito)

        return {
            'total_hongos': len(self.hongos),
            'tipos': tipos,
            'bioluminiscentes': bioluminiscentes,
            'marchitos': marchitos,
            'salud': self.salud_ecosistema
        }

    def __repr__(self):
        return f"ColoniaHongos(hongos={len(self.hongos)}, salud={self.salud_ecosistema})"


# Test del módulo
if __name__ == "__main__":
    print("=== OSMOTROFIA - Colonia de Hongos ===\n")

    # Simular datos
    params_sistema = {
        'hardware': {
            'temperatura': {'cpu': 65},
            'bateria': {'porcentaje': 75}
        },
        'rendimiento': {
            'cpu': {'uso_porcentaje': 45},
            'ram': {'uso_porcentaje': 60},
            'almacenamiento': {'uso_porcentaje': 70}
        }
    }

    params_gmail = {
        'importante': 50,
        'spam': 30,
        'promociones': 80,
        'social': 40,
        'no_leidos': 25
    }

    # Crear colonia
    colonia = ColoniaHongos(radio_colonia=10)
    colonia.generar_desde_datos(params_sistema, params_gmail)

    # Estadísticas
    stats = colonia.get_estadisticas()

    print(f"Total de hongos: {stats['total_hongos']}")
    print(f"Salud del ecosistema: {stats['salud']['nivel']} ({stats['salud']['salud_numerica']}%)")
    print(f"\nDistribución:")
    for tipo, cantidad in stats['tipos'].items():
        print(f"  {tipo}: {cantidad}")
    print(f"\nBioluminiscentes: {stats['bioluminiscentes']}")
    print(f"Marchitos: {stats['marchitos']}")

    # Mostrar algunos hongos
    print(f"\nPrimeros 3 hongos:")
    for i, hongo in enumerate(colonia.hongos[:3]):
        props = hongo.get_propiedades_render(tiempo=0)
        print(f"  {i+1}. {hongo.tipo}: pos={props['posicion']}, color=RGB({props['color']['r']:.2f}, {props['color']['g']:.2f}, {props['color']['b']:.2f})")
