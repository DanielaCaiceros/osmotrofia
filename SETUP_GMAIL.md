# 📧 Configuración de Gmail API para OSMOTROFIA

Esta guía te ayudará a configurar el acceso a Gmail para que OSMOTROFIA pueda leer tus emails y usarlos como "nutrientes" para la colonia fúngica.

**⚠️ NOTA:** Esto es opcional. Puedes usar OSMOTROFIA en modo demo sin Gmail.

---

## 🎯 Pasos de Configuración

### 1. Ir a Google Cloud Console

Abre tu navegador y ve a: https://console.cloud.google.com/

### 2. Crear un Proyecto

1. Click en el selector de proyectos (arriba a la izquierda)
2. Click en "Nuevo Proyecto"
3. Nombre del proyecto: `OSMOTROFIA` (o el que prefieras)
4. Click en "Crear"
5. Espera unos segundos a que se cree

### 3. Habilitar Gmail API

1. Selecciona tu proyecto recién creado
2. En el menú lateral, ve a: **APIs y servicios** → **Biblioteca**
3. Busca: `Gmail API`
4. Click en "Gmail API"
5. Click en "Habilitar"
6. Espera a que se habilite (puede tomar unos segundos)

### 4. Configurar Pantalla de Consentimiento OAuth

1. En el menú lateral: **APIs y servicios** → **Pantalla de consentimiento de OAuth**
2. Tipo de usuario: Selecciona **Externo**
3. Click en "Crear"

4. **Información de la aplicación:**
   - Nombre de la aplicación: `OSMOTROFIA`
   - Correo electrónico de asistencia: *tu email*
   - Logo de la aplicación: (opcional, puedes omitir)

5. **Dominios autorizados:** (dejar en blanco)

6. **Información de contacto del desarrollador:**
   - Email: *tu email*

7. Click en "Guardar y continuar"

8. **Alcances (Scopes):**
   - Click en "Añadir o quitar alcances"
   - Busca y selecciona: `Gmail API .../auth/gmail.readonly`
   - Click en "Actualizar"
   - Click en "Guardar y continuar"

9. **Usuarios de prueba:**
   - Click en "Añadir usuarios"
   - Ingresa tu email (el que usarás con OSMOTROFIA)
   - Click en "Añadir"
   - Click en "Guardar y continuar"

10. Click en "Volver al panel"

### 5. Crear Credenciales

1. En el menú lateral: **APIs y servicios** → **Credenciales**
2. Click en "Crear credenciales" (arriba)
3. Selecciona: **ID de cliente de OAuth 2.0**

4. **Tipo de aplicación:**
   - Selecciona: **Aplicación de escritorio**
   - Nombre: `OSMOTROFIA Desktop`

5. Click en "Crear"

6. Aparecerá un modal con "Cliente de OAuth creado"
   - Click en "Descargar JSON"
   - Guarda el archivo

7. **IMPORTANTE:** Renombra el archivo descargado a `credentials.json`

### 6. Colocar credentials.json

1. Mueve el archivo `credentials.json` a la raíz del proyecto OSMOTROFIA:

```bash
# Ejemplo (ajusta la ruta según dónde lo descargaste)
mv ~/Downloads/client_secret_*.json /ruta/a/osmotrofia/credentials.json
```

2. Verifica que esté en el lugar correcto:

```bash
cd /ruta/a/osmotrofia
ls -l credentials.json
```

Deberías ver el archivo listado.

---

## 🚀 Primer Uso

### 1. Ejecutar OSMOTROFIA con Gmail

```bash
python3 main.py
```

Selecciona: `[2] Modo Completo (con Gmail)`

### 2. Autorizar Acceso

1. Se abrirá tu navegador automáticamente
2. Si no se abre, copia y pega la URL que aparece en la terminal
3. Selecciona tu cuenta de Google
4. Verás una advertencia: "Google hasn't verified this app"
   - Click en "Advanced" (Avanzado)
   - Click en "Go to OSMOTROFIA (unsafe)" (Ir a OSMOTROFIA - no seguro)
   - **Nota:** Es seguro porque es tu propia aplicación
5. Revisa los permisos solicitados:
   - "Ver tus mensajes y configuración de correo electrónico"
6. Click en "Allow" (Permitir)

### 3. Autenticación Completada

1. Verás un mensaje: "The authentication flow has completed"
2. Vuelve a la terminal
3. OSMOTROFIA comenzará a leer tus emails
4. Se creará un archivo `token.pickle` (no lo compartas ni lo subas a git)

### 4. Usos Futuros

En ejecuciones posteriores, OSMOTROFIA usará `token.pickle` automáticamente. No necesitarás volver a autorizar.

---

## 🔒 Seguridad y Privacidad

### ¿Qué datos accede OSMOTROFIA?

OSMOTROFIA solo lee:
- Cantidad de emails en cada categoría (importante, spam, etc.)
- Cantidad de emails no leídos
- Cantidad de adjuntos grandes

**NO lee:**
- Contenido de los emails
- Asuntos
- Remitentes
- Destinatarios
- Ningún dato sensible

### ¿Dónde se guardan mis datos?

- Los datos **NO** se envían a ningún servidor externo
- Todo se procesa **localmente** en tu computadora
- Los conteos se usan **solo** para generar la visualización
- No se guarda ningún historial de emails

### Archivos Sensibles

Estos archivos contienen información sensible y **NO** deben compartirse:

- `credentials.json` - Credenciales OAuth2
- `token.pickle` - Token de acceso

**Ya están en `.gitignore`** para que no se suban accidentalmente a git.

---

## 🛠️ Troubleshooting

### Error: "credentials.json no encontrado"

**Solución:** Asegúrate de que `credentials.json` esté en la raíz del proyecto:

```bash
ls -l credentials.json
```

Si no aparece, repite el paso 6 de la configuración.

### Error: "invalid_grant" al autorizar

**Solución:** El token expiró. Elimina el token y vuelve a autorizar:

```bash
rm token.pickle
python3 main.py
```

Selecciona modo completo y vuelve a autorizar.

### Error: "Access blocked: OSMOTROFIA has not completed the Google verification process"

**Solución:**

1. Ve a Google Cloud Console → Pantalla de consentimiento OAuth
2. Asegúrate de haber agregado tu email en "Usuarios de prueba"
3. El estado debe ser "En producción" o "Testing"

### La autorización no se completa

**Solución:**

1. Cierra el navegador
2. Elimina `token.pickle`
3. Vuelve a ejecutar y copia manualmente la URL si no se abre el navegador

### No puedo encontrar Gmail API en la biblioteca

**Solución:**

1. Asegúrate de haber seleccionado tu proyecto en Google Cloud Console
2. Verifica que estés en la sección correcta: APIs y servicios → Biblioteca
3. Usa el buscador para encontrar "Gmail API"

---

## 🧪 Verificar que Funciona

### Test Rápido

```bash
python3 core/monitor_gmail.py
```

Si todo está correcto, verás:

```
=== OSMOTROFIA - Monitor de Gmail ===

Nutrientes digitales detectados:
  📧 Total emails: 1234
  ⭐ Importantes: 56
  ☣️  Spam: 12
  🛍️  Promociones: 234
  👥 Social: 89
  💡 No leídos: 45
  📎 Adjuntos pesados: 23
```

---

## 📝 Notas Adicionales

### Límites de la API

Gmail API tiene límites de uso:
- 1,000,000,000 cuotas por día (más que suficiente)
- OSMOTROFIA hace muy pocas llamadas (~10 por ejecución)

### Revocar Acceso

Si quieres revocar el acceso de OSMOTROFIA a tu Gmail:

1. Ve a: https://myaccount.google.com/permissions
2. Busca "OSMOTROFIA"
3. Click en "Remover acceso"
4. Elimina `token.pickle` de tu proyecto

### Usar con Múltiples Cuentas

Para usar OSMOTROFIA con diferentes cuentas de Gmail:

1. Renombra `token.pickle` a `token_cuenta1.pickle`
2. Ejecuta OSMOTROFIA de nuevo
3. Autoriza con la segunda cuenta
4. Para alternar entre cuentas, renombra los archivos de token

---

## ✅ Checklist de Configuración

- [ ] Proyecto creado en Google Cloud Console
- [ ] Gmail API habilitada
- [ ] Pantalla de consentimiento configurada
- [ ] Usuario de prueba agregado (tu email)
- [ ] Credenciales OAuth creadas
- [ ] `credentials.json` descargado
- [ ] `credentials.json` renombrado correctamente
- [ ] `credentials.json` en la raíz del proyecto
- [ ] Primera autorización completada
- [ ] `token.pickle` generado
- [ ] Test ejecutado con éxito

---

## 🆘 ¿Necesitas Ayuda?

Si tienes problemas con la configuración:

1. Revisa esta guía paso a paso
2. Verifica que todos los archivos estén en su lugar
3. Usa el modo demo mientras tanto: `python3 demo_rapido.py`
4. Consulta la documentación oficial de Gmail API: https://developers.google.com/gmail/api

---

🍄 **Una vez configurado, OSMOTROFIA usará tus datos reales de Gmail para crear una colonia fúngica personalizada!**
