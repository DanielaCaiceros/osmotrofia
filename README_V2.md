# 🍄 OSMOTROFIA v2.0

> **Ecosistema Fúngico Digital VIVO**
> *Tu vida digital transformada en una colonia de hongos que respira*

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-green)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Three.js](https://img.shields.io/badge/three.js-0.160-orange)
![License](https://img.shields.io/badge/license-Art%20Project-purple)

</div>

---

## 🎯 ¿Qué es OSMOTROFIA v2.0?

Un proyecto artístico que visualiza tu ecosistema digital (sistema + emails) como una **colonia VIVA de hongos en 3D** que:

- 🌱 **Nacen y crecen** en tiempo real
- 💓 **Respiran** (pulsación orgánica)
- 🌀 **Se mueven** e inclinan
- ✨ **Brillan** con bioluminiscencia
- 😵 **Se marchitan** sin energía
- 💀 **Mueren y se reciclan**
- 🧬 **Evolucionan** continuamente

Todo basado en datos **REALES** de tu computadora y emails.

---

## ✨ Nuevo en v2.0

### 🎮 Interactividad 3D
- Rotación 360° con mouse
- Zoom y navegación libre
- Controles intuitivos

### 🧬 Ecosistema Vivo
- Cada hongo tiene **edad** y **energía**
- Ciclo de vida completo: nace → crece → marchita → muere
- **Reciclaje** automático de hongos muertos
- Evolución **continua** (no frame by frame)

### 💡 Efectos Visuales
- Bioluminiscencia **pulsante** en tiempo real
- Geometrías **procedurales** únicas
- Shaders de **brillo** y **humedad**
- Inclinación **orgánica**
- Respiración **suave**

### ⚡ Tiempo Real
- Conexión WebSocket al backend
- Actualización cada 5 segundos
- Reacción **inmediata** a cambios del sistema
- Sin lag, fluido a 60 FPS

---

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pip3 install flask flask-cors psutil

# 2. Iniciar servidor
python3 server.py

# 3. Abrir navegador
# http://localhost:5000
```

**¡Eso es todo!** 🎉

Ver guía detallada: [QUICKSTART_V2.md](QUICKSTART_V2.md)

---

## 📦 Arquitectura

```
┌──────────────────┐
│  Python Backend  │
│                  │
│  • Sistema       │
│  • Gmail         │
│  • Mapper        │
│  • Flask API     │
└────────┬─────────┘
         │ JSON
         │ HTTP
         ▼
┌──────────────────┐
│  Three.js 3D     │
│                  │
│  • Hongos Vivos  │
│  • Animaciones   │
│  • Shaders       │
│  • Física        │
└──────────────────┘
```

---

## 🧬 Mapeo Biológico

### Hardware → Ambiente

| Parámetro | Efecto Visual | Efecto en Hongos |
|-----------|---------------|------------------|
| **CPU Temp** | Color (azul→rojo) | Velocidad de crecimiento |
| **Batería** | Brillo superficie | Energía de hongos |
| **CPU Uso** | Velocidad animación | Metabolismo |
| **RAM** | Grosor del tallo | Capacidad de absorción |
| **Disco** | Distribución espacial | Hacinamiento |

### Emails → Nutrientes

| Tipo | Color | Forma | Energía |
|------|-------|-------|---------|
| **Importante** | 🔵 Azul/Violeta | Grande, redondeada | Alta |
| **Spam** | 🟢 Verde tóxico | Irregular, deforme | Baja |
| **Promociones** | 🟠 Naranja | Uniforme | Media |
| **Social** | 🟣 Púrpura | Agrupada | Media |
| **No leídos** | ✨ Bioluminiscente | + Brillo pulsante | - |

---

## 🎨 Ciclo de Vida

```
   NACIENDO (0-5s)
   ├─ Escala pequeña (0.1)
   ├─ Crecimiento rápido
   └─ Energía subiendo
         │
         ▼
      VIVO (5s-∞)
   ├─ Crecimiento lento
   ├─ Pulsación activa
   ├─ Reacciona a ambiente
   └─ Energía estable
         │
         ▼ (si energía < 30%)
    MARCHITO (variable)
   ├─ Pierde energía rápido
   ├─ Color se apaga
   ├─ Se encoge
   └─ Inclinación aumenta
         │
         ▼ (si energía ≈ 0%)
     MUERTO (3s)
   ├─ Colapsa (Y scale → 0.3)
   ├─ Deja de moverse
   └─ Marca para reciclaje
         │
         ▼
    ♻️ RECICLADO
   └─ Removido de escena
   └─ Memoria liberada
   └─ Nutrientes vuelven al ecosistema
```

---

## 💻 Estructura de Archivos

```
osmotrofia/
├── server.py                  # Servidor Flask
├── monitor_sistemap.py        # Monitor de sistema
│
├── core/
│   ├── monitor_gmail.py       # Gmail API
│   └── mapper.py              # Mapeo biológico
│
├── web/
│   ├── index.html             # Página principal
│   ├── css/
│   │   └── styles.css         # Estilos UI
│   └── js/
│       ├── main.js            # Entry point
│       ├── HongoVivo.js       # Clase hongo individual
│       └── ColoniaViva.js     # Gestión de colonia
│
└── docs/
    ├── QUICKSTART_V2.md       # Inicio rápido
    ├── README_V2.md           # Este archivo
    └── SETUP_GMAIL.md         # Configurar Gmail
```

---

## 🎮 Controles

### Cámara
- **Click izquierdo + arrastrar**: Rotar 360°
- **Scroll**: Zoom in/out
- **Click derecho + arrastrar**: Pan (mover)

### UI
- **⏸️ Pausar**: Congela la evolución
- **🔄 Resetear**: Reinicia colonia
- **📊 Stats**: Toggle panel estadísticas

### Atajos de Teclado
- `Space`: Pausar/Reanudar
- `R`: Resetear
- `S`: Toggle stats

---

## 📊 API Backend

### `GET /api/estado`

Retorna estado completo del ecosistema:

```json
{
  "timestamp": "2026-01-14T...",
  "sistema": {
    "cpu": { "uso": 45.2, "temperatura": 68.5 },
    "ram": { "uso": 70.3, "disponible_gb": 8.2 },
    "disco": { "uso": 75.1, "libre_gb": 125.3 },
    "bateria": { "porcentaje": 85, "conectado": true }
  },
  "gmail": {
    "total": 1250,
    "importante": 56,
    "spam": 23,
    "no_leidos": 42
  },
  "ambiente": {
    "temperatura": { "estado": "optimo", "color": {...} },
    "humedad": { "brillo": 0.85, ... },
    ...
  },
  "nutrientes": [
    {
      "tipo": "importante",
      "cantidad": 56,
      "caracteristicas": { "color": {...}, "tamano_final": 1.5 }
    }
  ],
  "bioluminiscencia": {
    "activa": true,
    "intensidad": 0.7
  }
}
```

### `GET /api/salud`

Health check simple:

```json
{
  "status": "ok",
  "gmail_disponible": false,
  "mensaje": "🍄 OSMOTROFIA Backend funcionando"
}
```

---

## 🔧 Configuración

### Gmail (Opcional)

1. Sigue [SETUP_GMAIL.md](SETUP_GMAIL.md)
2. Coloca `credentials.json` en raíz
3. Reinicia servidor

Sin Gmail, usa datos simulados automáticamente.

### Personalización

#### Cambiar frecuencia de actualización

`web/js/main.js`:
```javascript
const CONFIG = {
    updateInterval: 10000 // 10 segundos
};
```

#### Cambiar tamaño de colonia

```javascript
const CONFIG = {
    radioColonia: 15 // Más grande
};
```

#### Ajustar ciclo de vida

`web/js/HongoVivo.js`:
```javascript
estadoMarchito(dt) {
    this.energia -= dt * 0.2; // Más rápido
}
```

---

## 🐛 Troubleshooting

### Backend no inicia

```bash
# Verificar Python
python3 --version  # Debe ser 3.9+

# Reinstalar dependencias
pip3 install --upgrade flask flask-cors psutil
```

### Frontend no conecta

1. Verificar que servidor esté corriendo
2. Abrir consola navegador (F12)
3. Verificar URL API:
   ```
   http://localhost:5000/api/estado
   ```

### Performance baja

- Usar navegador moderno (Chrome, Edge, Firefox)
- Cerrar otras pestañas
- Reducir `radioColonia` a 8-10
- Aumentar `updateInterval` a 10000ms

### Hongos no aparecen

1. Consola navegador (F12) → buscar errores
2. Verificar backend responde JSON válido
3. Probar en modo incógnito (sin extensiones)

---

## 📚 Recursos

### Documentación
- [QUICKSTART_V2.md](QUICKSTART_V2.md) - Inicio rápido
- [SETUP_GMAIL.md](SETUP_GMAIL.md) - Configurar Gmail
- [RESUMEN.md](RESUMEN.md) - Detalles técnicos v1.0

### Tecnologías
- [Three.js](https://threejs.org/) - Librería 3D
- [Flask](https://flask.palletsprojects.com/) - Backend Python
- [Gmail API](https://developers.google.com/gmail/api) - Acceso a emails

### Inspiración
- Hongos saprófitos (Pleurotus, Agaricus)
- Bioluminiscencia (Omphalotus olearius)
- Círculos de hadas (fairy rings)
- Arte generativo (Processing, p5.js)

---

## 🎯 Roadmap

### v2.1 (Próximo)
- [ ] Sonido ambiental
- [ ] Partículas de esporas
- [ ] Micelio visible (red de conexiones)
- [ ] Más tipos de hongos

### v2.2
- [ ] VR support (WebXR)
- [ ] Exportar video/GIF
- [ ] Modo "instalación" (pantalla completa)
- [ ] Multi-usuario (comparar colonias)

### v3.0
- [ ] Otras fuentes de datos (Dropbox, Twitter)
- [ ] Machine learning (predicción de evolución)
- [ ] NFT generation
- [ ] API pública

---

## 🙏 Contribuciones

Este es un proyecto artístico/exploratorio abierto a contribuciones:

- 🐛 **Bugs**: Abre un issue
- ✨ **Features**: PRs bienvenidos
- 🎨 **Arte**: Comparte tus colonias
- 📚 **Docs**: Mejoras de documentación

---

## 📝 Licencia

Proyecto artístico libre. Usa, modifica y comparte como quieras.

---

## 💬 Créditos

**Concepto**: OSMOTROFIA - La descomposición digital como acto poético

**Desarrollo v2.0**: Ecosistema vivo con Three.js

**Inspiración**: La naturaleza transformadora de los hongos aplicada al mundo digital

---

<div align="center">

## 🍄 OSMOTROFIA v2.0 🍄

*"En la muerte digital, nace nueva vida"*

---

**[Inicio Rápido](QUICKSTART_V2.md)** • **[Setup Gmail](SETUP_GMAIL.md)** • **[Guías](docs/)**

---

🌱 v2.0 | 2026 | Powered by Three.js

</div>
