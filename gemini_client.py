"""
Osmotrofia - Cliente Gemini
Maneja la comunicación con la API de Gemini para generar imágenes
"""

import google.generativeai as genai
import os
from datetime import datetime
import time

class GeminiClient:
    def __init__(self, api_key=None):
        """Inicializa el cliente de Gemini"""
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("API Key de Gemini no encontrada. Define GEMINI_API_KEY en variables de entorno.")
        
        genai.configure(api_key=api_key)
        
        # Configurar el modelo para generación de imágenes
        # Nota: Gemini actualmente genera imágenes a través de Imagen 3
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        self.historial = []
    
    def generar_imagen(self, prompt, carpeta_salida='output'):
        """
        Genera una imagen basada en el prompt
        
        Args:
            prompt: Descripción detallada para la imagen
            carpeta_salida: Carpeta donde guardar las imágenes
        
        Returns:
            dict con información de la generación
        """
        try:
            print("🍄 Generando colonia de hongos...")
            print(f"📝 Prompt enviado ({len(prompt)} caracteres)")
            
            # Crear carpeta de salida si no existe
            os.makedirs(carpeta_salida, exist_ok=True)
            
            # IMPORTANTE: Gemini 2.0 actualmente no genera imágenes directamente
            # Usamos el modelo de texto para generar una descripción mejorada
            # que luego podría usarse con Imagen 3 (cuando esté disponible en API)
            
            response = self.model.generate_content(
                f"""Basándote en esta descripción de una colonia de hongos, genera una descripción 
                aún más detallada y visual para un generador de imágenes AI. Enfócate en detalles 
                microscópicos, texturas, iluminación y composición:

{prompt}

Responde SOLO con la descripción mejorada, sin explicaciones adicionales."""
            )
            
            descripcion_mejorada = response.text
            
            # Guardar el prompt y la respuesta
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_prompt = os.path.join(carpeta_salida, f'prompt_{timestamp}.txt')
            
            with open(archivo_prompt, 'w', encoding='utf-8') as f:
                f.write("=== PROMPT ORIGINAL ===\n\n")
                f.write(prompt)
                f.write("\n\n=== DESCRIPCIÓN MEJORADA ===\n\n")
                f.write(descripcion_mejorada)
            
            resultado = {
                'exito': True,
                'timestamp': timestamp,
                'archivo_prompt': archivo_prompt,
                'descripcion_mejorada': descripcion_mejorada,
                'mensaje': 'Descripción generada exitosamente. Usa esta descripción con un generador de imágenes como Midjourney, DALL-E o Stable Diffusion.'
            }
            
            self.historial.append(resultado)
            
            print("✅ Descripción generada exitosamente")
            print(f"📁 Guardado en: {archivo_prompt}")
            
            return resultado
            
        except Exception as e:
            print(f"❌ Error al generar: {str(e)}")
            return {
                'exito': False,
                'error': str(e),
                'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
            }
    
    def generar_con_reintentos(self, prompt, max_intentos=3, carpeta_salida='output'):
        """Genera imagen con reintentos en caso de fallo"""
        for intento in range(max_intentos):
            print(f"Intento {intento + 1}/{max_intentos}")
            resultado = self.generar_imagen(prompt, carpeta_salida)
            
            if resultado['exito']:
                return resultado
            
            if intento < max_intentos - 1:
                tiempo_espera = (intento + 1) * 5
                print(f"⏳ Esperando {tiempo_espera}s antes de reintentar...")
                time.sleep(tiempo_espera)
        
        return resultado
    
    def obtener_historial(self):
        """Retorna el historial de generaciones"""
        return self.historial


# Función de prueba
if __name__ == "__main__":
    # Esta es una prueba básica
    print("=== PRUEBA DE GEMINI CLIENT ===")
    print("\nNOTA: Necesitas definir GEMINI_API_KEY en tu entorno")
    print("Ejemplo: export GEMINI_API_KEY='tu_api_key_aqui'")
    
    try:
        client = GeminiClient()
        
        prompt_prueba = """Genera una imagen fotorealista de hongos marrones saludables 
        creciendo en un sustrato de madera. Iluminación natural, textura visible, 
        profundidad de campo. Vista macro."""
        
        resultado = client.generar_imagen(prompt_prueba)
        
        if resultado['exito']:
            print("\n✅ Prueba exitosa")
            print(f"Descripción mejorada:\n{resultado['descripcion_mejorada'][:200]}...")
        else:
            print(f"\n❌ Error: {resultado.get('error', 'Desconocido')}")
            
    except ValueError as e:
        print(f"\n⚠️  {e}")
        print("\nPara configurar tu API key:")
        print("1. Obtén tu key en: https://aistudio.google.com/app/apikey")
        print("2. En tu terminal:")
        print("   Windows: set GEMINI_API_KEY=tu_key_aqui")
        print("   Mac/Linux: export GEMINI_API_KEY=tu_key_aqui")