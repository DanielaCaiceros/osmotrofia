#!/usr/bin/env python3
"""
OSMOTROFIA - Sistema de Visualización Fúngica Digital

Un proyecto artístico que visualiza tu ecosistema digital (emails + sistema)
como una colonia de hongos que descompone tus datos.

Concepto:
- Tu computadora es el "sustrato" donde crece el hongo
- Tus emails son los "nutrientes" que descompone
- El hardware define las condiciones ambientales
- La salud del sistema se refleja en la salud de la colonia
"""

import sys
import os

# Añadir directorio actual al path para imports
sys.path.insert(0, os.path.dirname(__file__))

from monitor_sistemap import MonitorSistema
from core.monitor_gmail import MonitorGmail
from visual.colonia import ColoniaHongos
from visual.visualizador_2d import Visualizador2D

# Intentar importar visualizador 3D
try:
    from visual.visualizador_3d import iniciar_visualizador_3d
    TIENE_3D = True
except ImportError:
    TIENE_3D = False


def mostrar_banner():
    """Muestra banner ASCII"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║    ██████╗ ███████╗███╗   ███╗ ██████╗████████╗██████╗   ║
║   ██╔═══██╗██╔════╝████╗ ████║██╔═══██╗╚══██╔══╝██╔══██╗  ║
║   ██║   ██║███████╗██╔████╔██║██║   ██║   ██║   ██████╔╝  ║
║   ██║   ██║╚════██║██║╚██╔╝██║██║   ██║   ██║   ██╔══██╗  ║
║   ╚██████╔╝███████║██║ ╚═╝ ██║╚██████╔╝   ██║   ██║  ██║  ║
║    ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝  ║
║                   R  O  F  I  A                           ║
║                                                           ║
║           Ecosistema Fúngico Digital v1.0                ║
║       Descomponiendo tu vida digital desde 2026          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def modo_demo():
    """Modo demo sin Gmail (solo datos del sistema)"""
    print("\n🍄 MODO DEMO - Solo datos del sistema\n")

    # Obtener datos del sistema
    monitor_sistema = MonitorSistema()
    params_sistema = monitor_sistema.obtener_parametros_completos()

    # Datos de Gmail simulados
    params_gmail = {
        'importante': 50,
        'spam': 30,
        'promociones': 100,
        'social': 40,
        'no_leidos': 25,
        'total': 220,
        'adjuntos_pesados': 15
    }

    print("📊 Datos del Sistema:")
    print(f"  CPU: {params_sistema['rendimiento']['cpu']['uso_porcentaje']}%")
    print(f"  RAM: {params_sistema['rendimiento']['ram']['uso_porcentaje']}%")
    print(f"  Disco: {params_sistema['rendimiento']['almacenamiento']['uso_porcentaje']}%")
    print(f"  Temperatura: {params_sistema['hardware']['temperatura']['cpu']}°C")
    print(f"  Batería: {params_sistema['hardware']['bateria']['porcentaje']}%")

    print("\n📧 Datos de Gmail (simulados):")
    print(f"  Total: {params_gmail['total']}")
    print(f"  Importantes: {params_gmail['importante']}")
    print(f"  Spam: {params_gmail['spam']}")
    print(f"  No leídos: {params_gmail['no_leidos']}")

    return params_sistema, params_gmail


def modo_completo():
    """Modo completo con Gmail"""
    print("\n🍄 MODO COMPLETO - Sistema + Gmail\n")

    # Obtener datos del sistema
    print("📊 Obteniendo datos del sistema...")
    monitor_sistema = MonitorSistema()
    params_sistema = monitor_sistema.obtener_parametros_completos()

    # Obtener datos de Gmail
    print("📧 Conectando con Gmail...")
    try:
        monitor_gmail = MonitorGmail()
        params_gmail = monitor_gmail.obtener_nutrientes_digitales()
        print("✅ Conectado a Gmail")
    except FileNotFoundError as e:
        print(f"\n⚠️  {e}")
        print("\nUsando modo demo en su lugar...\n")
        return modo_demo()
    except Exception as e:
        print(f"\n⚠️  Error al conectar con Gmail: {e}")
        print("\nUsando modo demo en su lugar...\n")
        return modo_demo()

    print("\n📊 Datos del Sistema:")
    print(f"  CPU: {params_sistema['rendimiento']['cpu']['uso_porcentaje']}%")
    print(f"  RAM: {params_sistema['rendimiento']['ram']['uso_porcentaje']}%")
    print(f"  Disco: {params_sistema['rendimiento']['almacenamiento']['uso_porcentaje']}%")
    print(f"  Temperatura: {params_sistema['hardware']['temperatura']['cpu']}°C")
    print(f"  Batería: {params_sistema['hardware']['bateria']['porcentaje']}%")

    print("\n📧 Datos de Gmail:")
    print(f"  Total: {params_gmail['total']}")
    print(f"  Importantes: {params_gmail['importante']}")
    print(f"  Spam: {params_gmail['spam']}")
    print(f"  No leídos: {params_gmail['no_leidos']}")

    return params_sistema, params_gmail


def generar_colonia(params_sistema, params_gmail):
    """Genera la colonia de hongos"""
    print("\n🌱 Generando colonia fúngica...")

    colonia = ColoniaHongos(radio_colonia=12)
    colonia.generar_desde_datos(params_sistema, params_gmail)

    stats = colonia.get_estadisticas()

    print(f"\n✅ Colonia generada:")
    print(f"  Total de hongos: {stats['total_hongos']}")
    print(f"  Salud del ecosistema: {stats['salud']['nivel']} ({stats['salud']['salud_numerica']}%)")
    print(f"  Estado: {stats['salud']['descripcion']}")
    print(f"\n  Distribución:")
    for tipo, cantidad in stats['tipos'].items():
        print(f"    - {tipo}: {cantidad}")

    return colonia


def visualizar(colonia, modo='2d'):
    """Visualiza la colonia"""
    if modo == '3d':
        if not TIENE_3D:
            print("\n⚠️  Visualizador 3D no disponible (Panda3D no instalado)")
            print("   Usando visualizador 2D en su lugar...\n")
            modo = '2d'
        else:
            print("\n🎨 Iniciando visualización 3D...")
            print("   (Esto puede tomar unos segundos...)\n")
            iniciar_visualizador_3d(colonia)
            return

    # Modo 2D
    print("\n🎨 Iniciando visualización 2D...")
    print("   Cierra la ventana para salir.\n")
    viz = Visualizador2D(colonia)
    viz.mostrar_estatico()


def menu_principal():
    """Menú interactivo"""
    mostrar_banner()

    print("\nSelecciona un modo:\n")
    print("  [1] Modo Demo (sin Gmail)")
    print("  [2] Modo Completo (con Gmail)")
    print("  [q] Salir\n")

    opcion = input("→ Opción: ").strip().lower()

    if opcion == 'q':
        print("\n👋 ¡Hasta luego!\n")
        sys.exit(0)
    elif opcion == '1':
        params_sistema, params_gmail = modo_demo()
    elif opcion == '2':
        params_sistema, params_gmail = modo_completo()
    else:
        print("\n⚠️  Opción inválida. Usando modo demo.\n")
        params_sistema, params_gmail = modo_demo()

    # Generar colonia
    colonia = generar_colonia(params_sistema, params_gmail)

    # Seleccionar visualización
    print("\n\nSelecciona visualización:\n")
    print("  [1] 2D (matplotlib - recomendado)")
    if TIENE_3D:
        print("  [2] 3D (Panda3D)")
    print("  [s] Solo mostrar estadísticas")
    print("  [q] Salir\n")

    viz_opcion = input("→ Opción: ").strip().lower()

    if viz_opcion == 'q':
        print("\n👋 ¡Hasta luego!\n")
        sys.exit(0)
    elif viz_opcion == 's':
        print("\n✅ Estadísticas mostradas arriba.")
        print("\n👋 ¡Hasta luego!\n")
        sys.exit(0)
    elif viz_opcion == '2' and TIENE_3D:
        visualizar(colonia, modo='3d')
    else:
        visualizar(colonia, modo='2d')


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por el usuario")
        print("👋 ¡Hasta luego!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
