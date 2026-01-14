"""
Osmotrofia - Sistema de Monitoreo
Captura parámetros del sistema para mapearlos a características de hongos
"""

import psutil
import platform
import time
from datetime import datetime

class MonitorSistema:
    def __init__(self):
        self.sistema_operativo = platform.system()
        
    def obtener_parametros_completos(self):
        """Obtiene todos los parámetros del sistema"""
        return {
            'timestamp': datetime.now().isoformat(),
            'hardware': self._obtener_hardware(),
            'software': self._obtener_software(),
            'rendimiento': self._obtener_rendimiento()
        }
    
    def _obtener_hardware(self):
        """Parámetros de hardware"""
        try:
            temperatura = self._obtener_temperatura()
        except:
            temperatura = {'cpu': 50}  # Valor por defecto si no se puede leer
            
        try:
            bateria = psutil.sensors_battery()
            bateria_info = {
                'porcentaje': bateria.percent if bateria else 100,
                'conectado': bateria.power_plugged if bateria else True
            }
        except:
            bateria_info = {'porcentaje': 100, 'conectado': True}
        
        return {
            'temperatura': temperatura,
            'bateria': bateria_info,
            'ventiladores': self._estado_ventiladores()
        }
    
    def _obtener_software(self):
        """Parámetros de software"""
        procesos = list(psutil.process_iter(['name', 'memory_percent']))
        
        return {
            'sistema_operativo': {
                'nombre': platform.system(),
                'version': platform.version(),
                'actualizado': self._verificar_actualizacion()
            },
            'procesos': {
                'total': len(procesos),
                'innecesarios': self._contar_procesos_innecesarios(procesos),
                'pesados': self._contar_procesos_pesados(procesos)
            },
            'seguridad': self._verificar_seguridad()
        }
    
    def _obtener_rendimiento(self):
        """Parámetros de rendimiento"""
        cpu = psutil.cpu_percent(interval=1)
        memoria = psutil.virtual_memory()
        disco = psutil.disk_usage('/')
        
        return {
            'cpu': {
                'uso_porcentaje': cpu,
                'nucleos': psutil.cpu_count(),
                'frecuencia': psutil.cpu_freq().current if psutil.cpu_freq() else 0
            },
            'ram': {
                'uso_porcentaje': memoria.percent,
                'total_gb': round(memoria.total / (1024**3), 2),
                'disponible_gb': round(memoria.available / (1024**3), 2)
            },
            'almacenamiento': {
                'uso_porcentaje': disco.percent,
                'total_gb': round(disco.total / (1024**3), 2),
                'libre_gb': round(disco.free / (1024**3), 2)
            }
        }
    
    def _obtener_temperatura(self):
        """Intenta obtener temperatura del sistema"""
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    # Buscar temperatura de CPU
                    for nombre, entradas in temps.items():
                        if 'coretemp' in nombre.lower() or 'cpu' in nombre.lower():
                            if entradas:
                                return {'cpu': entradas[0].current}
            # Si no se puede obtener, estimamos basado en uso de CPU
            cpu_uso = psutil.cpu_percent(interval=0.5)
            temp_estimada = 40 + (cpu_uso * 0.5)  # Estimación simple
            return {'cpu': round(temp_estimada, 1)}
        except:
            return {'cpu': 50}
    
    def _estado_ventiladores(self):
        """Estado de ventilación (simplificado)"""
        cpu_uso = psutil.cpu_percent()
        # Estimamos que ventiladores están activos si CPU > 60%
        return {
            'activos': cpu_uso > 60,
            'velocidad_estimada': 'alta' if cpu_uso > 80 else 'media' if cpu_uso > 60 else 'baja'
        }
    
    def _verificar_actualizacion(self):
        """Verifica si el SO parece actualizado (simplificado)"""
        # En un caso real, esto requeriría APIs específicas del SO
        return 'desconocido'
    
    def _contar_procesos_innecesarios(self, procesos):
        """Cuenta procesos que podrían ser innecesarios"""
        # Lista simple de procesos comunes innecesarios
        innecesarios = ['bloatware', 'toolbar', 'updater', 'helper']
        count = 0
        for proc in procesos:
            try:
                nombre = proc.info['name'].lower()
                if any(inn in nombre for inn in innecesarios):
                    count += 1
            except:
                pass
        return count
    
    def _contar_procesos_pesados(self, procesos):
        """Cuenta procesos que usan mucha memoria"""
        count = 0
        for proc in procesos:
            try:
                if proc.info['memory_percent'] and proc.info['memory_percent'] > 5:
                    count += 1
            except:
                pass
        return count
    
    def _verificar_seguridad(self):
        """Verifica estado básico de seguridad"""
        procesos = [p.info['name'].lower() for p in psutil.process_iter(['name'])]
        
        # Buscar procesos de antivirus comunes
        antivirus = ['defender', 'avast', 'avg', 'norton', 'mcafee', 'kaspersky']
        tiene_antivirus = any(av in str(procesos) for av in antivirus)
        
        return {
            'antivirus_activo': tiene_antivirus,
            'firewall': 'desconocido'  # Requeriría permisos admin para verificar
        }
    
    def calcular_salud_general(self, parametros):
        """Calcula un score de salud general (0-100)"""
        scores = []
        
        # Hardware
        temp_cpu = parametros['hardware']['temperatura']['cpu']
        if temp_cpu < 60:
            scores.append(100)
        elif temp_cpu < 80:
            scores.append(70)
        else:
            scores.append(30)
        
        # Batería
        bateria = parametros['hardware']['bateria']['porcentaje']
        scores.append(bateria)
        
        # CPU
        cpu = parametros['rendimiento']['cpu']['uso_porcentaje']
        scores.append(100 - cpu)
        
        # RAM
        ram = parametros['rendimiento']['ram']['uso_porcentaje']
        scores.append(100 - ram)
        
        # Almacenamiento
        disco = parametros['rendimiento']['almacenamiento']['uso_porcentaje']
        scores.append(100 - disco)
        
        return round(sum(scores) / len(scores), 1)


# Función de prueba
if __name__ == "__main__":
    monitor = MonitorSistema()
    params = monitor.obtener_parametros_completos()
    salud = monitor.calcular_salud_general(params)
    
    print("=== OSMOTROFIA - Monitor de Sistema ===")
    print(f"\nSalud General: {salud}%")
    print(f"\nCPU: {params['rendimiento']['cpu']['uso_porcentaje']}%")
    print(f"RAM: {params['rendimiento']['ram']['uso_porcentaje']}%")
    print(f"Disco: {params['rendimiento']['almacenamiento']['uso_porcentaje']}%")
    print(f"Temperatura CPU: {params['hardware']['temperatura']['cpu']}°C")
    print(f"Batería: {params['hardware']['bateria']['porcentaje']}%")