"""
Osmotrofia - Cliente OpenAI (DALL-E)
Genera imágenes usando DALL-E 3
"""

import os
import requests
from datetime import datetime
import base64

class OpenAIClient:
    def __init__(self, api_key=None):
        """Inicializa el cliente de OpenAI"""
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("API Key de OpenAI no encontrada. Define OPENAI_API_KEY en variables de entorno.")
        
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/images/generations"
        self.historial = []
    
    def generar_imagen(self, prompt, carpeta_salida='output'):
        """
        Genera una imagen usando DALL-E 3
        
        Args:
            prompt: Descripción detallada para la imagen
            carpeta_salida: Carpeta donde guardar las imágenes
        
        Returns:
            dict con información de la generación
        """
        try:
            print("🍄 Generando colonia de hongos con DALL-E 3...")
            print(f"📝 Prompt enviado ({len(prompt)} caracteres)")
            
            # Crear carpeta de salida si no existe
            os.makedirs(carpeta_salida, exist_ok=True)
            
            # Preparar el request a DALL-E
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # DALL-E 3 tiene límite de 4000 caracteres en el prompt
            if len(prompt) > 4000:
                print("⚠️  Prompt muy largo, recortando a 4000 caracteres...")
                prompt = prompt[:3997] + "..."
            
            data = {
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024",  # Opciones: 1024x1024, 1792x1024, 1024x1792
                "quality": "standard",  # "standard" o "hd"
                "response_format": "url"  # "url" o "b64_json"
            }
            
            # Hacer el request
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                revised_prompt = result['data'][0].get('revised_prompt', prompt)
                
                # Descargar la imagen
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archivo_imagen = os.path.join(carpeta_salida, f'hongos_{timestamp}.png')
                
                print("📥 Descargando imagen...")
                img_response = requests.get(image_url, timeout=30)
                
                if img_response.status_code == 200:
                    with open(archivo_imagen, 'wb') as f:
                        f.write(img_response.content)
                    
                    # Guardar el prompt
                    archivo_prompt = os.path.join(carpeta_salida, f'prompt_{timestamp}.txt')
                    with open(archivo_prompt, 'w', encoding='utf-8') as f:
                        f.write("=== PROMPT ORIGINAL ===\n\n")
                        f.write(prompt)
                        f.write("\n\n=== PROMPT REVISADO POR DALL-E ===\n\n")
                        f.write(revised_prompt)
                        f.write(f"\n\n=== URL DE IMAGEN ===\n\n")
                        f.write(image_url)
                    
                    resultado = {
                        'exito': True,
                        'timestamp': timestamp,
                        'archivo_imagen': archivo_imagen,
                        'archivo_prompt': archivo_prompt,
                        'url_imagen': image_url,
                        'revised_prompt': revised_prompt,
                        'mensaje': f'✅ Imagen generada y guardada en: {archivo_imagen}'
                    }
                    
                    self.historial.append(resultado)
                    
                    print(f"✅ Imagen guardada en: {archivo_imagen}")
                    print(f"📁 Prompt guardado en: {archivo_prompt}")
                    
                    return resultado
                else:
                    raise Exception(f"Error al descargar imagen: {img_response.status_code}")
            
            else:
                error_msg = response.json().get('error', {}).get('message', 'Error desconocido')
                raise Exception(f"Error de API: {response.status_code} - {error_msg}")
            
        except Exception as e:
            print(f"❌ Error al generar: {str(e)}")
            return {
                'exito': False,
                'error': str(e),
                'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
            }
    
    def generar_con_reintentos(self, prompt, max_intentos=3, carpeta_salida='output'):
        """Genera imagen con reintentos en caso de fallo"""
        import time
        
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
    print("=== PRUEBA DE OPENAI CLIENT ===")
    print("\nNOTA: Necesitas definir OPENAI_API_KEY en tu entorno")
    print("Ejemplo: export OPENAI_API_KEY='sk-...'")
    
    try:
        client = OpenAIClient()
        
        prompt_prueba = """Genera una imagen fotorealista de hongos marrones saludables 
        creciendo en un sustrato de madera. Iluminación natural, textura visible, 
        profundidad de campo. Vista macro."""
        
        resultado = client.generar_imagen(prompt_prueba)
        
        if resultado['exito']:
            print("\n✅ Prueba exitosa")
            print(f"Imagen: {resultado['archivo_imagen']}")
        else:
            print(f"\n❌ Error: {resultado.get('error', 'Desconocido')}")
            
    except ValueError as e:
        print(f"\n⚠️  {e}")
        print("\nPara configurar tu API key:")
        print("1. Obtén tu key en: https://platform.openai.com/api-keys")
        print("2. En tu terminal:")
        print("   Windows: set OPENAI_API_KEY=sk-...")
        print("   Mac/Linux: export OPENAI_API_KEY=sk-...")