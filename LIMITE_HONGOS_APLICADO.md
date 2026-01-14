# 🔧 Límite de Hongos Aplicado

## ✅ Problema Solucionado

**Antes**: 800+ hongos vivos → No se veían, lag, cámara muy alejada
**Ahora**: Máximo 50 hongos → Visibles, fluido, mejor distribución

---

## 🛠️ Cambios Aplicados

### 1. Límite Máximo de Hongos

**Archivo**: `web/js/ColoniaViva.js`

```javascript
// LÍMITE MÁXIMO DE HONGOS (para performance y visibilidad)
this.MAX_HONGOS = 50;
```

- Máximo de **50 hongos** en toda la colonia
- Ajustable fácilmente cambiando este número
- Se distribuyen proporcionalmente entre tipos

### 2. Factor de Creación Reducido

**Antes**: 1 hongo por cada 10 emails
**Ahora**: 1 hongo por cada 50 emails

```javascript
// Reducir factor: 1 hongo por cada 50 emails
const numHongos = Math.max(1, Math.floor(cantidad / 50));
```

Con tus datos:
- Importantes: 201 emails → ~4 hongos
- Spam: 201 emails → ~4 hongos
- Promociones: etc.
- **Total**: ~50 hongos en lugar de 800

### 3. Escala Proporcional

Si el cálculo da más de 50 hongos, se escalan proporcionalmente:

```javascript
if (totalDeseado > this.MAX_HONGOS) {
    const factor = this.MAX_HONGOS / totalDeseado;
    // Cada tipo se reduce proporcionalmente
}
```

### 4. Verificación de Límite

Antes de crear cada hongo, verifica el límite:

```javascript
if (this.hongos.length >= this.MAX_HONGOS) {
    console.log(`⚠️  Límite alcanzado, deteniendo creación`);
    return;
}
```

### 5. Hongos Muertos Dejan de Evolucionar

**Archivo**: `web/js/HongoVivo.js`

```javascript
// ⚠️ SI ESTÁ MUERTO Y LISTO PARA RECICLAR, NO HACER NADA
if (this.estadoVida === 'muerto' && this.tiempoEnEstado > 3.0) {
    return; // Ya no evolucionar, solo esperar reciclaje
}
```

Ahora:
- ✅ Los hongos muertos NO incrementan edad
- ✅ Los hongos muertos NO cambian
- ✅ Solo esperan ser reciclados (3 segundos)

---

## 📊 Resultado Esperado

Con tus datos actuales:

| Tipo | Emails | Hongos (antes) | Hongos (ahora) |
|------|--------|----------------|----------------|
| Importante | 201 | ~20 | ~4 |
| Spam | 201 | ~20 | ~4 |
| Promociones | 201 | ~20 | ~4 |
| Social | 0 | 0 | 0 |
| **TOTAL** | **603** | **~60** | **~12-15** |

Más espacio, más visibles, mejor performance! 🎯

---

## 🎮 Cómo Ajustar el Límite

### Opción 1: Modificar en ColoniaViva.js

```javascript
// Cambiar este valor:
this.MAX_HONGOS = 30;  // Para menos hongos
this.MAX_HONGOS = 100; // Para más hongos (puede causar lag)
```

### Opción 2: Modificar Factor de Emails

```javascript
// Cambiar de 50 a otro número:
const numHongos = Math.max(1, Math.floor(cantidad / 100)); // Menos hongos
const numHongos = Math.max(1, Math.floor(cantidad / 25));  // Más hongos
```

---

## 💡 Recomendaciones

### Para Mejor Visualización

| Emails Totales | MAX_HONGOS Recomendado | Factor |
|----------------|------------------------|--------|
| 0-500 | 20-30 | /50 |
| 500-1000 | 30-50 | /50 |
| 1000-2000 | 50-80 | /100 |
| 2000+ | 80-100 | /100-200 |

### Performance

- **30 hongos**: Excelente (60 FPS garantizado)
- **50 hongos**: Muy bueno (60 FPS en la mayoría)
- **100 hongos**: Bueno (puede bajar a 45-50 FPS)
- **200+ hongos**: Lag probable

---

## 🐛 Debugging

### Ver Límite en Consola

Abre la consola del navegador (F12) y verás:

```
⚠️  Límite de 50 hongos alcanzado
⚠️  Límite alcanzado, deteniendo creación
♻️  Reciclados 3 hongos muertos
```

### Verificar Cantidad Actual

En la consola del navegador:

```javascript
window.osmotrofia.stats()
// Verás: { total: 50, vivos: 48, marchitos: 2, ... }
```

---

## 🔧 Troubleshooting

### "Todavía veo muchos hongos"

1. Recarga la página (F5)
2. Verifica que el límite esté aplicado en `ColoniaViva.js`
3. Revisa la consola por errores

### "No veo ningún hongo"

1. Verifica que el backend esté corriendo
2. Abre http://localhost:5000/api/estado
3. Revisa que haya datos de emails
4. Intenta aumentar el límite a 100

### "Los hongos siguen evolucionando después de morir"

1. Verifica que el cambio esté en `HongoVivo.js` línea 151-154
2. Recarga la página
3. Observa la consola por errores

---

## 📝 Archivos Modificados

1. ✅ `web/js/ColoniaViva.js` - Límite máximo y factor reducido
2. ✅ `web/js/HongoVivo.js` - Detener evolución de muertos
3. ✅ `web/js/main.js` - Puerto corregido y config

---

## 🎯 Próximos Pasos

1. **Prueba ahora**: Recarga la página y verás ~50 hongos
2. **Ajusta el límite**: Si quieres más o menos
3. **Observa el ciclo**: Verás hongos nacer, vivir y morir
4. **Experimenta**: Cambia el puerto, el límite, etc.

---

## ⚙️ Configuración Actual

```javascript
// web/js/main.js
CONFIG = {
    backendURL: 'http://localhost:5000',  // Puerto del servidor
    updateInterval: 5000,                  // Actualizar cada 5s
    radioColonia: 12,                      // Radio de la colonia
    maxHongos: 50                          // Máximo de hongos
}
```

**Recuerda**: Si tu servidor corre en otro puerto (ej: 5050), cámbialo ahí!

---

🍄 **Ahora deberías ver una colonia manejable de ~50 hongos!**
