"""
Osmotrofia - Mapper Biológico
Traduce datos del sistema y Gmail a características fúngicas realistas
"""

import math


class MapperBiologico:
    """
    Mapea parámetros digitales a características biológicas de hongos

    CONCEPTO: Tu computadora es el "sustrato" que el hongo descompone
    - Hardware = Condiciones ambientales (temperatura, humedad, oxígeno)
    - Emails = Nutrientes para descomponer
    - Rendimiento = Salud del ecosistema
    """

    @staticmethod
    def mapear_temperatura_cpu(temp_cpu):
        """
        Temperatura CPU → Color y velocidad de crecimiento

        Args:
            temp_cpu: Temperatura en °C

        Returns:
            dict: {color, velocidad_crecimiento, estado}
        """
        if temp_cpu < 50:
            return {
                'color': {'r': 0.6, 'g': 0.8, 'b': 0.9},  # Azul fresco
                'velocidad_crecimiento': 0.5,
                'estado': 'frio',
                'textura': 'humeda_suave',
                'descripcion': 'Ambiente fresco - Crecimiento lento y denso'
            }
        elif temp_cpu < 70:
            return {
                'color': {'r': 0.8, 'g': 0.7, 'b': 0.5},  # Beige templado
                'velocidad_crecimiento': 1.0,
                'estado': 'optimo',
                'textura': 'normal',
                'descripcion': 'Ambiente óptimo - Crecimiento equilibrado'
            }
        elif temp_cpu < 85:
            return {
                'color': {'r': 0.9, 'g': 0.5, 'b': 0.2},  # Naranja cálido
                'velocidad_crecimiento': 1.5,
                'estado': 'caliente',
                'textura': 'seca_rapida',
                'descripcion': 'Ambiente caliente - Crecimiento acelerado'
            }
        else:
            return {
                'color': {'r': 0.8, 'g': 0.2, 'b': 0.1},  # Rojo extremo
                'velocidad_crecimiento': 2.0,
                'estado': 'extremo',
                'textura': 'carbonizada',
                'descripcion': 'Estrés térmico - Crecimiento errático y necrosis'
            }

    @staticmethod
    def mapear_bateria(porcentaje_bateria):
        """
        Batería → Humedad del sustrato

        Args:
            porcentaje_bateria: 0-100

        Returns:
            dict: {humedad, brillo, saturacion}
        """
        humedad_normalizada = porcentaje_bateria / 100.0

        if porcentaje_bateria >= 80:
            return {
                'humedad': humedad_normalizada,
                'brillo': 0.8,
                'saturacion': 1.0,
                'superficie': 'brillante_con_gotas',
                'descripcion': 'Sustrato muy húmedo - Superficie brillante'
            }
        elif porcentaje_bateria >= 50:
            return {
                'humedad': humedad_normalizada,
                'brillo': 0.5,
                'saturacion': 0.8,
                'superficie': 'semi_mate',
                'descripcion': 'Humedad óptima - Superficie balanceada'
            }
        elif porcentaje_bateria >= 20:
            return {
                'humedad': humedad_normalizada,
                'brillo': 0.2,
                'saturacion': 0.5,
                'superficie': 'mate_seca',
                'descripcion': 'Sustrato seco - Superficie opaca'
            }
        else:
            return {
                'humedad': humedad_normalizada,
                'brillo': 0.0,
                'saturacion': 0.2,
                'superficie': 'agrietada',
                'descripcion': 'Deshidratación crítica - Superficie agrietada'
            }

    @staticmethod
    def mapear_cpu_uso(porcentaje_cpu):
        """
        Uso de CPU → Metabolismo/Actividad enzimática

        Args:
            porcentaje_cpu: 0-100

        Returns:
            dict: {metabolismo, velocidad_animacion, intensidad}
        """
        if porcentaje_cpu < 30:
            return {
                'metabolismo': 'bajo',
                'velocidad_animacion': 0.5,
                'intensidad': 0.3,
                'respiracion': 'lenta',
                'descripcion': 'Reposo - Metabolismo bajo'
            }
        elif porcentaje_cpu < 60:
            return {
                'metabolismo': 'normal',
                'velocidad_animacion': 1.0,
                'intensidad': 0.6,
                'respiracion': 'normal',
                'descripcion': 'Activo - Metabolismo normal'
            }
        elif porcentaje_cpu < 90:
            return {
                'metabolismo': 'alto',
                'velocidad_animacion': 1.5,
                'intensidad': 0.9,
                'respiracion': 'acelerada',
                'esporas_flotantes': True,
                'descripcion': 'Descomposición activa - Metabolismo alto'
            }
        else:
            return {
                'metabolismo': 'hiper',
                'velocidad_animacion': 2.0,
                'intensidad': 1.0,
                'respiracion': 'frenetica',
                'esporas_flotantes': True,
                'estres_visible': True,
                'descripcion': 'Hiperactividad - Estrés metabólico'
            }

    @staticmethod
    def mapear_ram_uso(porcentaje_ram):
        """
        Uso de RAM → Capacidad de absorción de nutrientes

        Args:
            porcentaje_ram: 0-100

        Returns:
            dict: {absorcion, densidad_micelio, porosidad}
        """
        ram_disponible = 100 - porcentaje_ram

        if ram_disponible >= 60:
            return {
                'absorcion': 'alta',
                'densidad_micelio': 1.0,
                'porosidad': 0.8,
                'red_hifas': 'muy_desarrollada',
                'descripcion': 'Alta capacidad - Micelio muy desarrollado'
            }
        elif ram_disponible >= 30:
            return {
                'absorcion': 'media',
                'densidad_micelio': 0.6,
                'porosidad': 0.5,
                'red_hifas': 'normal',
                'descripcion': 'Capacidad normal - Micelio presente'
            }
        elif ram_disponible >= 10:
            return {
                'absorcion': 'baja',
                'densidad_micelio': 0.3,
                'porosidad': 0.2,
                'red_hifas': 'delgada',
                'descripcion': 'Saturación - Micelio delgado'
            }
        else:
            return {
                'absorcion': 'critica',
                'densidad_micelio': 0.1,
                'porosidad': 0.0,
                'red_hifas': 'cortada',
                'manchas_negras': True,
                'descripcion': 'Sobrecarga - Micelio cortado, toxinas acumuladas'
            }

    @staticmethod
    def mapear_disco_uso(porcentaje_disco):
        """
        Uso de disco → Espacio territorial

        Args:
            porcentaje_disco: 0-100

        Returns:
            dict: {expansion, distribucion, densidad}
        """
        disco_disponible = 100 - porcentaje_disco

        if disco_disponible >= 50:
            return {
                'expansion': 'amplia',
                'distribucion': 'dispersa',
                'patron': 'circulo_de_hadas',
                'densidad_colonia': 0.3,
                'descripcion': 'Mucho espacio - Colonia expandida'
            }
        elif disco_disponible >= 20:
            return {
                'expansion': 'media',
                'distribucion': 'compacta',
                'patron': 'agrupado',
                'densidad_colonia': 0.6,
                'descripcion': 'Espacio limitado - Colonia compacta'
            }
        elif disco_disponible >= 5:
            return {
                'expansion': 'limitada',
                'distribucion': 'hacinada',
                'patron': 'apretado',
                'densidad_colonia': 0.9,
                'hongos_deformados': True,
                'descripcion': 'Hacinamiento - Competencia por espacio'
            }
        else:
            return {
                'expansion': 'critica',
                'distribucion': 'atrofiada',
                'patron': 'colapsado',
                'densidad_colonia': 1.0,
                'hongos_muriendo': True,
                'descripcion': 'Sin espacio - Hongos atrofiados y muriendo'
            }

    @staticmethod
    def mapear_tipo_email(tipo_email, cantidad):
        """
        Tipo de email → Características del hongo individual

        Args:
            tipo_email: 'importante', 'spam', 'promociones', etc.
            cantidad: Número de emails de este tipo

        Returns:
            dict: {color, forma, tamano, textura}
        """
        mapeo = {
            'importante': {
                'color': {'r': 0.3, 'g': 0.4, 'b': 0.9},  # Azul/violeta
                'forma': 'redondeada_grande',
                'calidad': 'alta',
                'superficie': 'lisa_brillante',
                'tamano_base': 1.0,
                'energia': 'alta',
                'descripcion': 'Nutriente de alta calidad - Azul violeta'
            },
            'spam': {
                'color': {'r': 0.6, 'g': 0.8, 'b': 0.2},  # Verde amarillento
                'forma': 'irregular_deforme',
                'calidad': 'toxica',
                'superficie': 'rugosa_manchada',
                'tamano_base': 0.6,
                'energia': 'baja',
                'descripcion': 'Toxina - Verde amarillento enfermo'
            },
            'promociones': {
                'color': {'r': 0.9, 'g': 0.6, 'b': 0.1},  # Naranja brillante
                'forma': 'uniforme_sin_caracter',
                'calidad': 'procesada',
                'superficie': 'lisa_plastica',
                'tamano_base': 0.8,
                'energia': 'media',
                'descripcion': 'Nutriente procesado - Naranja artificial'
            },
            'social': {
                'color': {'r': 0.7, 'g': 0.5, 'b': 0.8},  # Púrpura claro
                'forma': 'agrupada',
                'calidad': 'media',
                'superficie': 'normal',
                'tamano_base': 0.7,
                'energia': 'media',
                'descripcion': 'Nutriente social - Púrpura claro'
            },
            'no_leidos': {
                'bioluminiscencia': True,
                'brillo_intensidad': 0.8,
                'halo': True,
                'pulsacion': 'rapida',
                'descripcion': 'Alimento sin procesar - Bioluminiscente'
            }
        }

        caracteristicas = mapeo.get(tipo_email, mapeo['importante'])

        # Ajustar tamaño según cantidad
        if 'tamano_base' in caracteristicas:
            factor_cantidad = min(1 + (cantidad / 100), 2.0)
            caracteristicas['tamano_final'] = caracteristicas['tamano_base'] * factor_cantidad

        return caracteristicas

    @staticmethod
    def calcular_salud_ecosistema(params_sistema):
        """
        Calcula la salud general del ecosistema fúngico

        Args:
            params_sistema: Parámetros del sistema completos

        Returns:
            dict: Estado global del ecosistema
        """
        # Extraer valores
        temp = params_sistema['hardware']['temperatura']['cpu']
        bateria = params_sistema['hardware']['bateria']['porcentaje']
        cpu = params_sistema['rendimiento']['cpu']['uso_porcentaje']
        ram = params_sistema['rendimiento']['ram']['uso_porcentaje']
        disco = params_sistema['rendimiento']['almacenamiento']['uso_porcentaje']

        # Calcular scores individuales
        scores = []

        # Temperatura (óptimo: 50-70°C)
        if 50 <= temp <= 70:
            scores.append(100)
        elif 40 <= temp < 50 or 70 < temp <= 80:
            scores.append(70)
        else:
            scores.append(30)

        # Batería
        scores.append(bateria)

        # CPU (óptimo: bajo uso)
        scores.append(100 - cpu)

        # RAM (óptimo: bajo uso)
        scores.append(100 - ram)

        # Disco (óptimo: bajo uso)
        scores.append(100 - disco)

        # Promedio
        salud = sum(scores) / len(scores)

        # Mapear a estado
        if salud >= 80:
            estado = {
                'nivel': 'excelente',
                'color_general': 'vibrante',
                'actividad': 'alta',
                'reproduccion': 'activa',
                'descripcion': 'Ecosistema saludable - Colonia vibrante'
            }
        elif salud >= 60:
            estado = {
                'nivel': 'bueno',
                'color_general': 'normal',
                'actividad': 'moderada',
                'reproduccion': 'presente',
                'descripcion': 'Ecosistema estable - Colonia funcional'
            }
        elif salud >= 40:
            estado = {
                'nivel': 'regular',
                'color_general': 'desaturado',
                'actividad': 'baja',
                'reproduccion': 'limitada',
                'descripcion': 'Ecosistema en riesgo - Problemas visibles'
            }
        elif salud >= 20:
            estado = {
                'nivel': 'malo',
                'color_general': 'grisaceo',
                'actividad': 'muy_baja',
                'reproduccion': 'nula',
                'plagas': True,
                'descripcion': 'Ecosistema en crisis - Colonia deteriorada'
            }
        else:
            estado = {
                'nivel': 'critico',
                'color_general': 'negro_gris',
                'actividad': 'casi_nula',
                'reproduccion': 'nula',
                'partes_muertas': True,
                'descripcion': 'Colapso del ecosistema - Colonia moribunda'
            }

        estado['salud_numerica'] = round(salud, 1)
        return estado


# Test del módulo
if __name__ == "__main__":
    print("=== OSMOTROFIA - Mapper Biológico ===\n")

    # Ejemplos de mapeo
    mapper = MapperBiologico()

    print("1. Temperatura CPU: 75°C")
    temp_map = mapper.mapear_temperatura_cpu(75)
    print(f"   → {temp_map['descripcion']}")
    print(f"   Color: RGB({temp_map['color']['r']}, {temp_map['color']['g']}, {temp_map['color']['b']})")
    print(f"   Velocidad: {temp_map['velocidad_crecimiento']}x\n")

    print("2. Batería: 45%")
    bat_map = mapper.mapear_bateria(45)
    print(f"   → {bat_map['descripcion']}")
    print(f"   Brillo: {bat_map['brillo']}\n")

    print("3. Uso CPU: 85%")
    cpu_map = mapper.mapear_cpu_uso(85)
    print(f"   → {cpu_map['descripcion']}")
    print(f"   Velocidad animación: {cpu_map['velocidad_animacion']}x\n")

    print("4. Email importante (x50)")
    email_map = mapper.mapear_tipo_email('importante', 50)
    print(f"   → {email_map['descripcion']}")
    print(f"   Tamaño: {email_map.get('tamano_final', 1.0)}\n")
