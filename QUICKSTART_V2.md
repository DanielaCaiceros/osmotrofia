# 🍄 OSMOTROFIA v2.0 - Inicio Rápido

> **Ecosistema Fúngico Digital VIVO con Three.js**

## 🚀 Inicio en 3 Pasos

### Paso 1: Instalar Dependencias

```bash
pip3 install flask flask-cors psutil
```

### Paso 2: Iniciar el Servidor

```bash
python3 server.py
```

Verás algo como:
```
============================================================
🍄 OSMOTROFIA - Servidor Backend
============================================================

Gmail: ⚠️  Modo demo

🌐 Servidor corriendo en: http://localhost:5000
📡 API disponible en: http://localhost:5000/api/estado

💡 Abre http://localhost:5000 en tu navegador
   Presiona Ctrl+C para detener

============================================================
```

### Paso 3: Abrir en el Navegador

Abre tu navegador en:
```
http://localhost:5000
```

**¡Eso es todo!** Verás tu colonia fúngica viva en 3D. 🎉

---

## 🎮 Controles

### Cámara
- **Click izquierdo + arrastrar**: Rotar
- **Scroll**: Zoom
- **Click derecho + arrastrar**: Mover (pan)

### Botones
- **⏸️ Pausar**: Pausa la evolución
- **🔄 Resetear**: Reinicia la colonia
- **📊 Stats**: Muestra/oculta panel de estadísticas

---

## 🎨 ¿Qué Estás Viendo?

### Hongos Vivos
Cada hongo:
- 🌱 **Nace** pequeño
- 📈 **Crece** gradualmente
- 💓 **Respira** (pulsa suavemente)
- 🌀 **Se inclina** orgánicamente
- 😵 **Se marchita** si le falta energía
- 💀 **Muere** y es reciclado

### Colores

| Color | Significado |
|-------|-------------|
| 🔵 Azul/Violeta | Emails importantes (nutrientes de calidad) |
| 🟢 Verde amarillento | Spam (toxinas) |
| 🟠 Naranja | Promociones (nutrientes procesados) |
| 🟣 Púrpura | Emails sociales |
| ✨ Brillantes | Emails no leídos (bioluminiscencia) |

### Comportamientos en Tiempo Real

La colonia reacciona a tu sistema:

| Condición | Efecto en la Colonia |
|-----------|---------------------|
| 🔥 CPU caliente (>70°C) | Crecimiento acelerado, colores cálidos |
| ❄️ CPU fría (<50°C) | Crecimiento lento, colores fríos |
| 🔋 Batería baja | Superficie mate, hongos pierden energía |
| 🔋 Batería alta | Superficie brillante, hongos saludables |
| 💾 RAM saturada | Tallos delgados, hongos se marchitan |
| 💿 Disco lleno | Colonia apretada, hongos deformados |
| 📧 Muchos no leídos | Más hongos brillan |
| ☣️ Mucho spam | Más hongos verdes tóxicos |

---

## 📊 Interfaz

### Panel de Sistema
Muestra en tiempo real:
- CPU, RAM, Disco
- Temperatura
- Batería

### Panel de Gmail
- Total de emails
- Importantes, Spam
- No leídos

### Panel de Colonia
- Hongos vivos
- Hongos marchitos
- Hongos bioluminiscentes
- Salud del ecosistema

---

## 🔧 Configuración Avanzada

### Usar Gmail Real (Opcional)

1. Sigue la guía en [SETUP_GMAIL.md](SETUP_GMAIL.md)
2. Coloca `credentials.json` en la raíz
3. Reinicia el servidor

El sistema detectará Gmail automáticamente.

### Ajustar Frecuencia de Actualización

Edita `web/js/main.js`:

```javascript
const CONFIG = {
    backendURL: 'http://localhost:5000',
    updateInterval: 5000, // Cambiar a 10000 para 10 segundos
    radioColonia: 12
};
```

### Cambiar Radio de la Colonia

```javascript
radioColonia: 15  // Colonia más grande
```

---

## 🐛 Problemas Comunes

### "ModuleNotFoundError: No module named 'flask'"

```bash
pip3 install flask flask-cors
```

### El servidor no inicia

Asegúrate de estar en el directorio correcto:

```bash
cd /ruta/a/osmotrofia
python3 server.py
```

### "Connection refused" en el navegador

1. Verifica que el servidor esté corriendo
2. Comprueba la URL: `http://localhost:5000`
3. Revisa que el puerto 5000 no esté ocupado

### Los hongos no aparecen

1. Abre la consola del navegador (F12)
2. Revisa errores de JavaScript
3. Verifica que el backend esté respondiendo:
   ```
   http://localhost:5000/api/estado
   ```

### "CORS error"

Ya está configurado con `flask-cors`. Si persiste:

```bash
pip3 install --upgrade flask-cors
```

---

## 🎯 Funcionalidades Nuevas v2.0

### ✨ Ciclo de Vida Completo
- Los hongos nacen, crecen, se marchitan y mueren
- Reciclaje automático de hongos muertos
- Cada hongo tiene edad y energía

### 🧬 Evolución Continua
- Crecimiento orgánico en tiempo real
- Inclinación dinámica
- Pulsación (respiración)
- Mutaciones suaves

### 💡 Bioluminiscencia Pulsante
- Los hongos brillan cuando hay emails no leídos
- Intensidad varía según cantidad
- Efecto de pulso realista

### 🎨 Geometrías Procedurales
- Cada hongo es único
- Deformación orgánica
- Textura natural

### ⚡ Reacción en Tiempo Real
- La colonia responde inmediatamente a cambios del sistema
- Animaciones fluidas
- Transiciones suaves

---

## 🔍 Debugging

### Consola del Navegador

Abre la consola (F12) y usa:

```javascript
// Ver datos actuales
window.osmotrofia.datos()

// Ver estadísticas de la colonia
window.osmotrofia.stats()

// Pausar/reanudar
window.osmotrofia.pausar()
window.osmotrofia.reanudar()
```

### Logs del Servidor

El servidor muestra logs en la terminal:
- Conexiones del navegador
- Errores de API
- Estado de Gmail

---

## 📝 Comparación v1.0 vs v2.0

| Feature | v1.0 (Python/Matplotlib) | v2.0 (Three.js) |
|---------|--------------------------|-----------------|
| Visualización | 2D estática | 3D interactiva |
| Animación | Frame por frame | Tiempo real continuo |
| Ciclo de vida | No | Sí (completo) |
| Interactividad | Limitada | Cámara 360°, zoom |
| Performance | Lenta | Rápida (WebGL) |
| Compartir | Instalar Python | Solo navegador |
| Evolución | No | Sí (continua) |
| Bioluminiscencia | Estática | Pulsante |

---

## 🌟 Próximos Pasos

1. ✅ Ejecuta el demo
2. 🎮 Experimenta con los controles
3. 📊 Observa cómo cambia con tu uso del sistema
4. 🔧 Configura Gmail para datos reales
5. 🎨 Personaliza colores y comportamientos

---

## 💡 Tips

### Para Observar Evolución
1. Deja el navegador abierto
2. Usa tu computadora normalmente
3. Observa cómo la colonia reacciona

### Para Performance
- Cierra otros programas
- Usa navegador moderno (Chrome, Firefox, Edge)
- Desactiva extensiones pesadas

### Para Capturar
- Screenshot: botón PrtScn
- Video: usa OBS o grabador de pantalla
- Perfecto para arte digital o instalaciones

---

## 🆘 Ayuda

- **Guía completa**: [README.md](README.md)
- **Setup Gmail**: [SETUP_GMAIL.md](SETUP_GMAIL.md)
- **Resumen técnico**: [RESUMEN.md](RESUMEN.md)

---

🍄 **¡Disfruta tu ecosistema fúngico digital vivo!**

*"La vida digital transformada en arte orgánico"*
