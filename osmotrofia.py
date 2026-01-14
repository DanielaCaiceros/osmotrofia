"""
OSMOTROFIA - Visualización de Computadora como Colonia de Hongos
Aplicación principal que integra todos los componentes
"""

import os
import sys
import time
from datetime import datetime
import json

from monitor_sistema import MonitorSistema
from generador_prompt import GeneradorPrompt
from gemini_client import GeminiClient


class Osmotrofia:
    def __init__(self, api_key=None):
        """Inicializa la aplicación Osmotrofia"""
        print("🍄 Iniciando OSMOTROFIA...")
        
        self.monitor = MonitorSistema()
        self.generador = GeneradorPrompt()
        self.gemini = GeminiClient(api_key)
        
        self.carpeta_salida = 'osmotrofia_output'
        os.makedirs(self.carpeta_salida, exist_ok=True)
        
        print("✅ Sistema inicializado correctamente\n")
    
    def analizar_sistema(self):
        """Analiza el estado actual del sistema"""
        print("🔍 Analizando sistema...")
        parametros = self.monitor.obtener_parametros_completos()
        salud = self.monitor.calcular_salud_general(parametros)
        
        print(f"\n📊 ESTADO DEL SISTEMA")
        print("=" * 50)
        print(f"Salud General: {salud}% {'🟢' if salud > 70 else '🟡' if salud > 40 else '🔴'}")
        print(f"\nHardware:")
        print(f"  • Temperatura CPU: {parametros['hardware']['temperatura']['cpu']}°C")
        print(f"  • Batería: {parametros['hardware']['bateria']['porcentaje']}%")
        print(f"\nRendimiento:")
        print(f"  • CPU: {parametros['rendimiento']['cpu']['uso_porcentaje']}%")
        print(f"  • RAM: {parametros['rendimiento']['ram']['uso_porcentaje']}%")
        print(f"  • Almacenamiento: {parametros['rendimiento']['almacenamiento']['uso_porcentaje']}%")
        print("=" * 50)
        
        return parametros, salud
    
    def generar_visualizacion(self, guardar_datos=True):
        """Genera la visualización completa"""
        # Analizar sistema
        parametros, salud = self.analizar_sistema()
        
        # Generar prompt
        print("\n🎨 Generando descripción de hongos...")
        prompt = self.generador.generar_prompt_completo(parametros, salud)
        
        # Guardar datos si se solicita
        if guardar_datos:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_datos = os.path.join(self.carpeta_salida, f'datos_{timestamp}.json')
            
            datos_completos = {
                'timestamp': timestamp,
                'parametros': parametros,
                'salud_general': salud,
                'prompt': prompt
            }
            
            with open(archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos_completos, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Datos guardados en: {archivo_datos}")
        
        # Generar con Gemini
        print("\n🤖 Enviando a Gemini...")
        resultado = self.gemini.generar_con_reintentos(prompt, carpeta_salida=self.carpeta_salida)
        
        return resultado
    
    def modo_monitoreo_continuo(self, intervalo_minutos=5):
        """Monitorea continuamente y genera visualizaciones periódicas"""
        print(f"\n🔄 MODO MONITOREO CONTINUO")
        print(f"Generando visualización cada {intervalo_minutos} minutos")
        print("Presiona Ctrl+C para detener\n")
        
        try:
            iteracion = 1
            while True:
                print(f"\n{'='*60}")
                print(f"ITERACIÓN #{iteracion} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}")
                
                self.generar_visualizacion()
                
                print(f"\n⏳ Esperando {intervalo_minutos} minutos hasta la próxima generación...")
                print(f"   (Próxima ejecución aproximadamente a las {self._calcular_proxima_hora(intervalo_minutos)})")
                
                time.sleep(intervalo_minutos * 60)
                iteracion += 1
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoreo detenido por el usuario")
            print(f"Total de iteraciones completadas: {iteracion - 1}")
    
    def _calcular_proxima_hora(self, minutos):
        """Calcula la hora aproximada de la próxima ejecución"""
        from datetime import datetime, timedelta
        proxima = datetime.now() + timedelta(minutes=minutos)
        return proxima.strftime('%H:%M:%S')
    
    def mostrar_menu(self):
        """Muestra el menú interactivo"""
        while True:
            print("\n" + "="*60)
            print("🍄 OSMOTROFIA - Menú Principal")
            print("="*60)
            print("1. Analizar sistema (sin generar imagen)")
            print("2. Generar visualización única")
            print("3. Modo monitoreo continuo")
            print("4. Ver historial de generaciones")
            print("5. Salir")
            print("="*60)
            
            opcion = input("\nSelecciona una opción (1-5): ").strip()
            
            if opcion == '1':
                self.analizar_sistema()
                input("\nPresiona Enter para continuar...")
                
            elif opcion == '2':
                resultado = self.generar_visualizacion()
                if resultado['exito']:
                    print("\n✅ Visualización generada exitosamente")
                else:
                    print(f"\n❌ Error: {resultado.get('error', 'Desconocido')}")
                input("\nPresiona Enter para continuar...")
                
            elif opcion == '3':
                intervalo = input("Intervalo en minutos (default: 5): ").strip()
                try:
                    intervalo = int(intervalo) if intervalo else 5
                    self.modo_monitoreo_continuo(intervalo)
                except ValueError:
                    print("❌ Intervalo inválido, usando 5 minutos")
                    self.modo_monitoreo_continuo(5)
                    
            elif opcion == '4':
                historial = self.gemini.obtener_historial()
                if historial:
                    print(f"\n📜 Historial ({len(historial)} generaciones):")
                    for i, gen in enumerate(historial, 1):
                        print(f"\n{i}. {gen['timestamp']}")
                        print(f"   Estado: {'✅ Exitoso' if gen['exito'] else '❌ Fallido'}")
                        if gen['exito']:
                            print(f"   Archivo: {gen['archivo_prompt']}")
                else:
                    print("\n📜 No hay generaciones en el historial")
                input("\nPresiona Enter para continuar...")
                
            elif opcion == '5':
                print("\n👋 ¡Hasta pronto!")
                break
                
            else:
                print("\n❌ Opción inválida")
                time.sleep(1)


def main():
    """Función principal"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║                    🍄 OSMOTROFIA 🍄                      ║
    ║                                                           ║
    ║          Visualización de Computadora como Hongos        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Verificar API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("⚠️  GEMINI_API_KEY no encontrada en variables de entorno")
        print("\nOpciones:")
        print("1. Configurar ahora (temporal)")
        print("2. Salir y configurar manualmente")
        
        opcion = input("\nSelecciona (1-2): ").strip()
        
        if opcion == '1':
            api_key = input("Ingresa tu API key de Gemini: ").strip()
            if not api_key:
                print("❌ API key vacía. Saliendo...")
                return
        else:
            print("\nPara configurar tu API key:")
            print("1. Obtén tu key en: https://aistudio.google.com/app/apikey")
            print("2. Configúrala:")
            print("   Windows: set GEMINI_API_KEY=tu_key_aqui")
            print("   Mac/Linux: export GEMINI_API_KEY=tu_key_aqui")
            return
    
    try:
        app = Osmotrofia(api_key)
        app.mostrar_menu()
        
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()