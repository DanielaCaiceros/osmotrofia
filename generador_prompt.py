"""
Osmotrofia - Generador de Prompts
Traduce parámetros técnicos a características biológicas de hongos
"""

class GeneradorPrompt:
    def __init__(self):
        self.mapeo_colores = {
            'optimo': ['marrones naturales', 'beige', 'dorado suave', 'blanco cremoso'],
            'caliente': ['rojo', 'naranja', 'amarillo intenso'],
            'frio': ['azul glacial', 'blanco escarcha', 'gris plateado'],
            'critico': ['negro carbón', 'rojo intenso', 'naranja fuego'],
            'enfermo': ['púrpura', 'verde neón', 'amarillo enfermizo'],
            'seco': ['marrón seco', 'beige pálido', 'gris polvo'],
            'humedo': ['verde musgo', 'marrón oscuro húmedo']
        }
    
    def generar_prompt_completo(self, parametros, salud_general):
        """Genera el prompt completo para Gemini"""
        
        # Análisis de condiciones
        condiciones = self._analizar_condiciones(parametros, salud_general)
        
        # Construcción del prompt
        prompt = f"""Genera una imagen fotorealista de una colonia de hongos que representa el estado actual de una computadora.

PARÁMETROS BIOLÓGICOS A REPRESENTAR:

**TEMPERATURA Y AMBIENTE**
{condiciones['temperatura']['descripcion']}
- Colores dominantes: {', '.join(condiciones['temperatura']['colores'])}
- Textura: {condiciones['temperatura']['textura']}

**HIDRATACIÓN (Batería: {parametros['hardware']['bateria']['porcentaje']}%)**
{condiciones['hidratacion']['descripcion']}
- Estado de los hongos: {condiciones['hidratacion']['estado']}

**OXIGENACIÓN (Ventilación)**
{condiciones['ventilacion']['descripcion']}
- Densidad: {condiciones['ventilacion']['densidad']}

**DENSIDAD POBLACIONAL (RAM: {parametros['rendimiento']['ram']['uso_porcentaje']}%)**
{condiciones['densidad']['descripcion']}
- Distribución: {condiciones['densidad']['distribucion']}

**ESPACIO VITAL (Almacenamiento: {parametros['rendimiento']['almacenamiento']['uso_porcentaje']}%)**
{condiciones['espacio']['descripcion']}
- Crecimiento: {condiciones['espacio']['crecimiento']}

**METABOLISMO (CPU: {parametros['rendimiento']['cpu']['uso_porcentaje']}%)**
{condiciones['metabolismo']['descripcion']}
- Intensidad visual: {condiciones['metabolismo']['intensidad']}

**SALUD GENERAL DEL ECOSISTEMA: {salud_general}%**
{condiciones['salud']['descripcion']}

ESTILO VISUAL:
- Fotografía macro de alta calidad, iluminación natural difusa
- Textura realista de hongos con detalles visibles (lamelas, poros, esporas)
- Profundidad de campo para dar sensación tridimensional
- Ambiente orgánico y natural, como un bosque microscópico
- Sin texto, sin números, solo la representación visual pura

COMPOSICIÓN:
- Vista cenital o lateral de la colonia
- Fondo de sustrato orgánico (tierra, madera, material en descomposición)
- Múltiples especies de hongos si hay variedad de condiciones
- Atmósfera coherente con las condiciones descritas

La imagen debe sentirse VIVA y representar visualmente el estado de salud de la computadora a través de la metáfora de los hongos."""

        return prompt
    
    def _analizar_condiciones(self, params, salud):
        """Analiza parámetros y genera descripciones biológicas"""
        condiciones = {}
        
        # TEMPERATURA
        temp = params['hardware']['temperatura']['cpu']
        if temp < 50:
            condiciones['temperatura'] = {
                'descripcion': 'Ambiente frío, hongos con escarcha visible, crecimiento lento y conservativo.',
                'colores': self.mapeo_colores['frio'],
                'textura': 'superficie cristalizada, con pequeños cristales de hielo'
            }
        elif temp < 70:
            condiciones['temperatura'] = {
                'descripcion': 'Temperatura óptima, hongos saludables con colores naturales y vibrantes.',
                'colores': self.mapeo_colores['optimo'],
                'textura': 'superficie suave y ligeramente húmeda, natural'
            }
        elif temp < 85:
            condiciones['temperatura'] = {
                'descripcion': 'Ambiente caliente, hongos con tonos cálidos, crecimiento acelerado.',
                'colores': self.mapeo_colores['caliente'],
                'textura': 'superficie seca, bordes ligeramente deshidratados'
            }
        else:
            condiciones['temperatura'] = {
                'descripcion': 'TEMPERATURA CRÍTICA: hongos chamuscados, áreas quemadas, vapor visible.',
                'colores': self.mapeo_colores['critico'],
                'textura': 'superficie agrietada y ennegrecida, con señales de daño térmico'
            }
        
        # HIDRATACIÓN (Batería)
        bateria = params['hardware']['bateria']['porcentaje']
        if bateria > 80:
            condiciones['hidratacion'] = {
                'descripcion': 'Alta hidratación, hongos turgentes y brillantes.',
                'estado': 'cuerpos fructíferos llenos, con brillo de humedad'
            }
        elif bateria > 50:
            condiciones['hidratacion'] = {
                'descripcion': 'Hidratación moderada, hongos en estado normal.',
                'estado': 'apariencia estándar saludable'
            }
        elif bateria > 20:
            condiciones['hidratacion'] = {
                'descripcion': 'Baja hidratación, hongos comenzando a marchitarse.',
                'estado': 'colores ligeramente apagados, pérdida de turgencia'
            }
        else:
            condiciones['hidratacion'] = {
                'descripcion': 'Deshidratación crítica, hongos secos y agrietados.',
                'estado': 'superficie craquelada, esporas flotando en el aire'
            }
        
        # VENTILACIÓN
        cpu_uso = params['rendimiento']['cpu']['uso_porcentaje']
        if cpu_uso < 30:
            condiciones['ventilacion'] = {
                'descripcion': 'Excelente ventilación, hongos aireados y porosos.',
                'densidad': 'estructuras abiertas con lamelas visibles'
            }
        elif cpu_uso < 70:
            condiciones['ventilacion'] = {
                'descripcion': 'Ventilación adecuada, crecimiento saludable.',
                'densidad': 'textura estándar, bien oxigenados'
            }
        else:
            condiciones['ventilacion'] = {
                'descripcion': 'Ventilación limitada, hongos densos y compactos.',
                'densidad': 'moho compacto, falta de oxígeno visible'
            }
        
        # DENSIDAD POBLACIONAL (RAM)
        ram = params['rendimiento']['ram']['uso_porcentaje']
        if ram < 40:
            condiciones['densidad'] = {
                'descripcion': 'Baja densidad, hongos espaciados con mucho sustrato visible.',
                'distribucion': 'colonias individuales bien separadas'
            }
        elif ram < 70:
            condiciones['densidad'] = {
                'descripcion': 'Densidad moderada, colonia establecida.',
                'distribucion': 'hongos agrupados pero con espacio entre ellos'
            }
        else:
            condiciones['densidad'] = {
                'descripcion': 'Alta densidad, hongos apiñados y compitiendo por espacio.',
                'distribucion': 'sobrepoblación, hongos creciendo unos sobre otros'
            }
        
        # ESPACIO VITAL (Almacenamiento)
        disco = params['rendimiento']['almacenamiento']['uso_porcentaje']
        if disco < 50:
            condiciones['espacio'] = {
                'descripcion': 'Amplio espacio disponible, territorio expandido.',
                'crecimiento': 'hongos pueden crecer libremente en todas direcciones'
            }
        elif disco < 80:
            condiciones['espacio'] = {
                'descripcion': 'Espacio moderado, colonia establecida con límites.',
                'crecimiento': 'crecimiento vertical, optimizando espacio'
            }
        else:
            condiciones['espacio'] = {
                'descripcion': 'Espacio crítico, hongos fosilizados en capas.',
                'crecimiento': 'estratificación visible, sin espacio para nuevos brotes'
            }
        
        # METABOLISMO (CPU)
        if cpu_uso < 30:
            condiciones['metabolismo'] = {
                'descripcion': 'Metabolismo en reposo, colonia dormida.',
                'intensidad': 'tonos pasteles suaves, sin actividad visible'
            }
        elif cpu_uso < 70:
            condiciones['metabolismo'] = {
                'descripcion': 'Metabolismo activo, crecimiento visible.',
                'intensidad': 'colores saturados, señales de vida activa'
            }
        else:
            condiciones['metabolismo'] = {
                'descripcion': 'Metabolismo acelerado, actividad intensa.',
                'intensidad': 'colores brillantes pulsantes, energía visible'
            }
        
        # SALUD GENERAL
        if salud > 80:
            condiciones['salud'] = {
                'descripcion': 'Ecosistema saludable y próspero, sin señales de estrés.'
            }
        elif salud > 60:
            condiciones['salud'] = {
                'descripcion': 'Ecosistema moderadamente saludable, algunas áreas de estrés.'
            }
        elif salud > 40:
            condiciones['salud'] = {
                'descripcion': 'Ecosistema bajo estrés, señales visibles de deterioro.'
            }
        else:
            condiciones['salud'] = {
                'descripcion': 'Ecosistema crítico, colonia en peligro con múltiples problemas.'
            }
        
        return condiciones


# Función de prueba
if __name__ == "__main__":
    # Datos de ejemplo
    params_ejemplo = {
        'hardware': {
            'temperatura': {'cpu': 75},
            'bateria': {'porcentaje': 45}
        },
        'rendimiento': {
            'cpu': {'uso_porcentaje': 65},
            'ram': {'uso_porcentaje': 70},
            'almacenamiento': {'uso_porcentaje': 85}
        }
    }
    
    generador = GeneradorPrompt()
    prompt = generador.generar_prompt_completo(params_ejemplo, 62)
    
    print("=== PROMPT GENERADO ===")
    print(prompt)