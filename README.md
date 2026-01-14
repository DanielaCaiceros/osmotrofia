# 🍄 OSMOTROFIA

> *Un ecosistema fúngico digital que descompone tu vida virtual*

**OSMOTROFIA** es un proyecto artístico/exploratorio que visualiza tu ecosistema digital personal (emails + recursos computacionales) como una colonia de hongos viva que descompone tus datos.

## 🎯 Concepto

Tu computadora es el **sustrato** donde crecen hongos digitales. Estos hongos se alimentan de tus emails y responden a las condiciones ambientales de tu sistema:

- **Temperatura (CPU)** → Color y velocidad de crecimiento
- **Humedad (Batería)** → Brillo y saturación
- **Metabolismo (Uso de CPU)** → Velocidad de animación
- **Capacidad de absorción (RAM)** → Grosor del micelio
- **Espacio territorial (Disco)** → Expansión de la colonia

### Tipos de Hongos (por tipo de email):

- 🔵 **Importantes** → Azul/violeta (nutrientes de alta calidad)
- 🟢 **Spam** → Verde amarillento (toxinas)
- 🟠 **Promociones** → Naranja brillante (nutrientes procesados)
- 🟣 **Social** → Púrpura claro
- 💡 **No leídos** → Bioluminiscentes (alimento sin procesar)

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd osmotrofia
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota:** Si quieres usar el visualizador 3D, descomenta la línea de `panda3d` en `requirements.txt`.

### 3. (Opcional) Configurar Gmail API

Para usar datos reales de Gmail:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto nuevo
3. Habilita la **Gmail API**
4. Crea credenciales OAuth 2.0
5. Descarga el archivo `credentials.json`
6. Colócalo en la raíz del proyecto (`osmotrofia/credentials.json`)

**Sin Gmail:** El proyecto funciona en modo demo con datos simulados.

## 🚀 Uso

### Ejecución simple:

```bash
python main.py
```

Esto abrirá un menú interactivo donde puedes elegir:

- **Modo Demo** (sin Gmail, usa datos simulados)
- **Modo Completo** (con Gmail, usa tus emails reales)

Y luego seleccionar visualización:

- **2D** (matplotlib - recomendado para empezar)
- **3D** (Panda3D - requiere instalación adicional)

### Ejecución de módulos individuales:

#### Probar monitor del sistema:

```bash
python monitor_sistemap.py
```

#### Probar monitor de Gmail:

```bash
python core/monitor_gmail.py
```

#### Probar mapper biológico:

```bash
python core/mapper.py
```

#### Probar visualizador 2D:

```bash
python visual/visualizador_2d.py
```

## 📁 Estructura del Proyecto

```
osmotrofia/
├── main.py                      # Punto de entrada principal
├── monitor_sistemap.py          # Monitor de sistema (CPU, RAM, disco, etc.)
│
├── core/                        # Módulos core
│   ├── monitor_gmail.py         # Obtiene datos de Gmail
│   └── mapper.py                # Mapea datos → características fúngicas
│
├── visual/                      # Módulos de visualización
│   ├── hongo_digital.py         # Clase de hongo individual
│   ├── colonia.py               # Gestión de colonia completa
│   ├── visualizador_2d.py       # Visualización 2D (matplotlib)
│   └── visualizador_3d.py       # Visualización 3D (Panda3D)
│
├── requirements.txt             # Dependencias
└── README.md                    # Este archivo
```

## 🧬 Mapeo Biológico Completo

### Condiciones Ambientales (Hardware)

| Parámetro Sistema | Característica Fúngica | Efecto Visual |
|-------------------|------------------------|---------------|
| **CPU (temp)** | Temperatura ambiente | Color: Frío=azul, Templado=beige, Caliente=naranja/rojo |
| **Batería** | Humedad del sustrato | Brillo: Alta=brillante, Baja=mate/agrietado |
| **CPU (uso)** | Metabolismo | Velocidad animación: Alta=rápido, Baja=lento |
| **RAM** | Absorción de nutrientes | Grosor micelio: Disponible=grueso, Saturado=fino |
| **Disco** | Espacio territorial | Patrón: Libre=disperso, Lleno=apiñado |

### Nutrientes (Emails)

| Tipo Email | Color | Forma | Energía |
|------------|-------|-------|---------|
| **Importante** | Azul/Violeta | Grande, redondeada | Alta |
| **Spam** | Verde amarillento | Irregular, deforme | Baja (tóxica) |
| **Promociones** | Naranja | Uniforme pero sin carácter | Media |
| **Social** | Púrpura claro | Agrupada | Media |
| **No leídos** | Bioluminiscente | (overlay) | Brillo |

### Salud del Ecosistema

| Salud | Color General | Actividad | Descripción |
|-------|---------------|-----------|-------------|
| **80-100%** | Vibrante | Alta | Ecosistema saludable |
| **60-79%** | Normal | Moderada | Ecosistema estable |
| **40-59%** | Desaturado | Baja | Ecosistema en riesgo |
| **20-39%** | Grisáceo | Muy baja | Crisis |
| **0-19%** | Negro/Gris | Casi nula | Colapso |

## 🎨 Ejemplos de Uso

### Ejemplo 1: Monitoreo Artístico

Ejecuta el proyecto periódicamente para ver cómo cambia tu "colonia digital" con el tiempo. ¿Más spam? Los hongos verdes tóxicos crecen. ¿CPU alta? Colores cálidos y movimiento acelerado.

### Ejemplo 2: Visualización de Salud Digital

Usa el proyecto como indicador visual de la salud de tu ecosistema digital. Una colonia marchita indica problemas (disco lleno, muchos procesos, CPU sobrecalentada).

### Ejemplo 3: Arte Generativo

Captura screenshots de diferentes estados y créalos como obra artística que representa tu vida digital.

## 🔧 Desarrollo y Personalización

### Ajustar parámetros de mapeo

Edita `core/mapper.py` para cambiar cómo se traducen los datos a características visuales.

### Cambiar colores y formas

Modifica las funciones en `MapperBiologico` para personalizar la estética.

### Añadir nuevos tipos de datos

Extiende `MonitorSistema` o `MonitorGmail` para capturar más datos y mapéalos en `mapper.py`.

### Crear nuevos visualizadores

Implementa tu propia clase heredando de `Visualizador2D` o creando desde cero.

## 🐛 Troubleshooting

### "Panda3D no está instalado"

El visualizador 3D es opcional. Puedes usar el 2D sin problemas, o instalar Panda3D:

```bash
pip install panda3d
```

### "credentials.json no encontrado"

Si no quieres configurar Gmail, simplemente usa el modo demo (opción 1 en el menú).

### "Error al obtener temperatura CPU"

En algunos sistemas (especialmente macOS), psutil no puede leer la temperatura. El proyecto usa una estimación basada en uso de CPU.

### La visualización 2D se cierra inmediatamente

Asegúrate de tener matplotlib instalado correctamente:

```bash
pip install matplotlib
```

## 📝 Licencia

Este es un proyecto artístico/exploratorio. Siéntete libre de modificarlo, extenderlo y crear tu propia versión.

## 🙏 Créditos

**Concepto:** OSMOTROFIA - La descomposición como acto poético de transformación digital.

**Inspiración Biológica:** Basado en características reales de hongos saprófitos (que descomponen materia orgánica).

---

*"En la muerte digital, nace nueva vida. Los hongos transforman lo que ya no necesitas en algo hermoso de contemplar."*

🍄 **OSMOTROFIA** - v1.0
