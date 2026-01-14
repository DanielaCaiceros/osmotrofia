#!/usr/bin/env python3
"""
OSMOTROFIA - Demo Rápido
Prueba rápida del sistema sin menú interactivo
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from monitor_sistemap import MonitorSistema
from visual.colonia import ColoniaHongos
from visual.visualizador_2d import Visualizador2D


def main():
    print("🍄 OSMOTROFIA - Demo Rápido\n")

    # 1. Obtener datos del sistema
    print("📊 Obteniendo datos del sistema...")
    monitor = MonitorSistema()
    params_sistema = monitor.obtener_parametros_completos()
    salud = monitor.calcular_salud_general(params_sistema)

    print(f"\n✅ Datos obtenidos:")
    print(f"  Salud General: {salud}%")
    print(f"  CPU: {params_sistema['rendimiento']['cpu']['uso_porcentaje']}%")
    print(f"  RAM: {params_sistema['rendimiento']['ram']['uso_porcentaje']}%")
    print(f"  Disco: {params_sistema['rendimiento']['almacenamiento']['uso_porcentaje']}%")
    print(f"  Temp CPU: {params_sistema['hardware']['temperatura']['cpu']}°C")
    print(f"  Batería: {params_sistema['hardware']['bateria']['porcentaje']}%")

    # 2. Datos de Gmail simulados
    params_gmail = {
        'importante': 10,
        'spam': 150,
        'promociones': 10,
        'social': 100,
        'no_leidos': 45,
        'total': 35,
        'adjuntos_pesados': 20
    }

    print(f"\n📧 Datos de Gmail (simulados):")
    print(f"  Total: {params_gmail['total']}")
    print(f"  Importantes: {params_gmail['importante']}")
    print(f"  Spam: {params_gmail['spam']}")
    print(f"  No leídos: {params_gmail['no_leidos']}")

    # 3. Generar colonia
    print("\n🌱 Generando colonia fúngica...")
    colonia = ColoniaHongos(radio_colonia=12)
    colonia.generar_desde_datos(params_sistema, params_gmail)

    stats = colonia.get_estadisticas()
    print(f"\n✅ Colonia generada:")
    print(f"  Total hongos: {stats['total_hongos']}")
    print(f"  Salud: {stats['salud']['nivel']} ({stats['salud']['salud_numerica']}%)")
    print(f"  Estado: {stats['salud']['descripcion']}")

    print(f"\n  Distribución:")
    for tipo, cantidad in stats['tipos'].items():
        print(f"    {tipo}: {cantidad} hongos")

    print(f"\n  Bioluminiscentes: {stats['bioluminiscentes']}")
    print(f"  Marchitos: {stats['marchitos']}")

    # 4. Visualizar
    print("\n🎨 Abriendo visualización 2D...")
    print("   (Cierra la ventana para salir)\n")

    viz = Visualizador2D(colonia)
    viz.mostrar_estatico()

    print("\n✅ Demo completado!")
    print("👋 ¡Hasta luego!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
