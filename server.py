#!/usr/bin/env python3
"""
OSMOTROFIA - Servidor Backend
Provee datos del sistema y Gmail a través de API REST
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from monitor_sistemap import MonitorSistema
from core.mapper import MapperBiologico

# Intentar importar Gmail (opcional)
try:
    from core.monitor_gmail import MonitorGmail
    GMAIL_DISPONIBLE = True
except:
    GMAIL_DISPONIBLE = False

app = Flask(__name__, static_folder='web', static_url_path='')
CORS(app)  # Permitir CORS para desarrollo

# Instancias globales
monitor_sistema = MonitorSistema()
mapper = MapperBiologico()
monitor_gmail = None

if GMAIL_DISPONIBLE:
    try:
        monitor_gmail = MonitorGmail()
    except:
        print("⚠️  Gmail no configurado, usando modo demo")


@app.route('/')
def index():
    """Página principal"""
    return send_from_directory('web', 'index.html')


@app.route('/test')
def test_hongo():
    """Página de prueba con un solo hongo"""
    return send_from_directory('web', 'test-hongo.html')


@app.route('/api/estado')
def get_estado():
    """
    Endpoint principal que devuelve el estado completo del ecosistema

    Returns:
        JSON con todos los datos necesarios para la visualización
    """
    try:
        # 1. Obtener datos del sistema
        params_sistema = monitor_sistema.obtener_parametros_completos()
        salud_general = monitor_sistema.calcular_salud_general(params_sistema)

        # 2. Obtener datos de Gmail (o simulados)
        if monitor_gmail:
            try:
                params_gmail = monitor_gmail.obtener_nutrientes_digitales()
            except:
                params_gmail = _datos_gmail_demo()
        else:
            params_gmail = _datos_gmail_demo()

        # 3. Mapear a características fúngicas
        temp_cpu = params_sistema['hardware']['temperatura']['cpu']
        bateria = params_sistema['hardware']['bateria']['porcentaje']
        cpu_uso = params_sistema['rendimiento']['cpu']['uso_porcentaje']
        ram_uso = params_sistema['rendimiento']['ram']['uso_porcentaje']
        disco_uso = params_sistema['rendimiento']['almacenamiento']['uso_porcentaje']

        ambiente = {
            'temperatura': mapper.mapear_temperatura_cpu(temp_cpu),
            'humedad': mapper.mapear_bateria(bateria),
            'metabolismo': mapper.mapear_cpu_uso(cpu_uso),
            'ram': mapper.mapear_ram_uso(ram_uso),
            'disco': mapper.mapear_disco_uso(disco_uso)
        }

        salud_ecosistema = mapper.calcular_salud_ecosistema(params_sistema)

        # 4. Calcular nutrientes por tipo
        nutrientes = []

        tipos_email = {
            'importante': params_gmail.get('importante', 0),
            'spam': params_gmail.get('spam', 0),
            'promociones': params_gmail.get('promociones', 0),
            'social': params_gmail.get('social', 0)
        }

        for tipo, cantidad in tipos_email.items():
            if cantidad > 0:
                carac = mapper.mapear_tipo_email(tipo, cantidad)
                # Crear hongos: 1 por cada 10 emails
                num_hongos = max(1, cantidad // 10)

                for i in range(num_hongos):
                    nutrientes.append({
                        'tipo': tipo,
                        'cantidad': cantidad,
                        'caracteristicas': carac
                    })

        # 5. Datos de bioluminiscencia
        no_leidos = params_gmail.get('no_leidos', 0)
        bioluminiscencia = {
            'activa': no_leidos > 0,
            'intensidad': min(no_leidos / 100, 1.0),
            'porcentaje_hongos': min(no_leidos / 100, 0.5)
        }

        # 6. Construir respuesta
        response = {
            'timestamp': params_sistema['timestamp'],
            'sistema': {
                'cpu': {
                    'uso': cpu_uso,
                    'temperatura': temp_cpu,
                    'nucleos': params_sistema['rendimiento']['cpu']['nucleos']
                },
                'ram': {
                    'uso': ram_uso,
                    'total_gb': params_sistema['rendimiento']['ram']['total_gb'],
                    'disponible_gb': params_sistema['rendimiento']['ram']['disponible_gb']
                },
                'disco': {
                    'uso': disco_uso,
                    'total_gb': params_sistema['rendimiento']['almacenamiento']['total_gb'],
                    'libre_gb': params_sistema['rendimiento']['almacenamiento']['libre_gb']
                },
                'bateria': {
                    'porcentaje': bateria,
                    'conectado': params_sistema['hardware']['bateria']['conectado']
                }
            },
            'gmail': {
                'total': params_gmail.get('total', 0),
                'importante': params_gmail.get('importante', 0),
                'spam': params_gmail.get('spam', 0),
                'promociones': params_gmail.get('promociones', 0),
                'social': params_gmail.get('social', 0),
                'no_leidos': no_leidos
            },
            'ambiente': ambiente,
            'salud': {
                'general': salud_general,
                'ecosistema': salud_ecosistema
            },
            'nutrientes': nutrientes,
            'bioluminiscencia': bioluminiscencia
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error en /api/estado: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def _datos_gmail_demo():
    """Datos de Gmail simulados para modo demo"""
    return {
        'importante': 50,
        'spam': 30,
        'promociones': 100,
        'social': 40,
        'no_leidos': 25,
        'total': 220,
        'adjuntos_pesados': 15
    }


@app.route('/api/salud')
def get_salud():
    """Endpoint simple para verificar que el servidor funciona"""
    return jsonify({
        'status': 'ok',
        'gmail_disponible': GMAIL_DISPONIBLE,
        'mensaje': '🍄 OSMOTROFIA Backend funcionando'
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🍄 OSMOTROFIA - Servidor Backend")
    print("="*60)
    print(f"\nGmail: {'✅ Configurado' if GMAIL_DISPONIBLE else '⚠️  Modo demo'}")
    print("\n🌐 Servidor corriendo en: http://localhost:5050")
    print("📡 API disponible en: http://localhost:5050/api/estado")
    print("\n💡 Abre http://localhost:5050 en tu navegador")
    print("   Presiona Ctrl+C para detener\n")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=5050, debug=True)
