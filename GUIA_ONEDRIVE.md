# 📘 Guía de Sincronización con OneDrive

## ☁️ ¿Qué es esta función?

La sincronización con OneDrive te permite usar el **Sistema de Inventarios** en **múltiples computadoras** compartiendo la misma base de datos. Todos los cambios se sincronizan automáticamente a través de OneDrive.

---

## ✅ Requisitos Previos

1. **OneDrive instalado y sincronizado** en todas las computadoras
2. **Cuenta de OneDrive** (personal o empresarial)
3. **Conexión a internet** (para la sincronización)
4. **Sistema de Inventarios instalado** en cada computadora

---

## 🚀 Configuración Inicial (Primera vez)

### Opción 1: Configuración Automática (Recomendada)

1. Abre el **Sistema de Inventarios**
2. Ve a la pestaña **⚙️ Configuración**
3. En la sección **☁️ Sincronización con OneDrive**, haz clic en:
   - **"☁️ Configurar BD en OneDrive"**
4. El sistema:
   - ✅ Detectará automáticamente tu carpeta de OneDrive
   - ✅ Creará una carpeta `Sistema_Inventarios`
   - ✅ Copiará tu base de datos actual (si existe)
   - ✅ Configurará todo automáticamente

### Opción 2: Configuración Manual

1. Abre el **Sistema de Inventarios**
2. Ve a la pestaña **⚙️ Configuración**
3. En la sección **☁️ Sincronización con OneDrive**, haz clic en:
   - **"📂 Seleccionar Ubicación Manual"**
4. Navega hasta tu carpeta de OneDrive
5. Crea o selecciona una carpeta para el sistema
6. Guarda o abre la base de datos

---

## 💻 Usar en Otra Computadora

### Paso 1: Instalar el Sistema
- Instala el **Sistema de Inventarios** en la segunda computadora
- Asegúrate de que **OneDrive esté sincronizado**

### Paso 2: Configurar la Base de Datos
1. Abre el programa
2. Ve a **⚙️ Configuración**
3. En **☁️ Sincronización con OneDrive**, haz clic en:
   - **"📂 Seleccionar Ubicación Manual"**
4. Selecciona **"SÍ"** (Seleccionar base de datos existente)
5. Navega a la carpeta de OneDrive
6. Busca: `OneDrive\Sistema_Inventarios\inventarios.db`
7. Abre el archivo

### Paso 3: ¡Listo!
- Ahora ambas computadoras usan la misma base de datos
- Los cambios se sincronizan automáticamente

---

## ⚠️ Advertencias Importantes

### 🔴 **NUNCA** abras el programa en 2 computadoras al mismo tiempo
- **Problema:** Puede causar conflictos en la base de datos
- **Solución:** Usa el programa en una computadora a la vez
- **Cierra el programa** antes de abrirlo en otra computadora

### 🟡 Espera la sincronización
- Antes de abrir el programa en otra computadora, espera a que OneDrive termine de sincronizar
- Verifica el icono de OneDrive en la bandeja del sistema (✅ = sincronizado)

### 🟡 Respaldo regular
- Aunque OneDrive guarda versiones anteriores, haz respaldos periódicos
- Ve a **⚙️ Configuración** → **📄 Exportar Resumen**

---

## 🔧 Solución de Problemas

### Problema: "OneDrive no detectado"
**Solución:**
1. Verifica que OneDrive esté instalado
2. Abre OneDrive y asegúrate de que esté sincronizado
3. Usa la opción **"📂 Seleccionar Ubicación Manual"**

### Problema: "Error al acceder a la base de datos"
**Solución:**
1. Cierra el programa en todas las computadoras
2. Espera 2-3 minutos para que OneDrive sincronice
3. Abre el programa solo en una computadora
4. Si persiste, restaura un respaldo

### Problema: "Datos duplicados o conflictos"
**Solución:**
1. OneDrive puede crear archivos de conflicto (`inventarios-DESKTOP-XXX.db`)
2. Identifica el archivo correcto (el más reciente)
3. Elimina los archivos duplicados
4. Mantén solo un archivo `inventarios.db`

---

## 📊 Ventajas y Limitaciones

### ✅ Ventajas
- ✨ Acceso desde múltiples computadoras
- 💾 Respaldo automático en la nube
- 🔄 Sincronización automática
- 🌐 Acceso desde cualquier lugar con OneDrive
- 📱 Visualización desde móvil (solo lectura)

### ⚠️ Limitaciones
- 🚫 No usar simultáneamente en 2+ computadoras
- 📶 Requiere internet para sincronizar
- ⏱️ Puede haber delay de sincronización (segundos/minutos)
- 💾 Depende de la velocidad de OneDrive

---

## 🎯 Mejores Prácticas

1. **Comunicación del equipo:**
   - Avisa cuando vayas a usar el sistema
   - Confirma que nadie más lo está usando

2. **Cierre correcto:**
   - Siempre cierra el programa correctamente (X o salir)
   - No apagues la computadora con el programa abierto

3. **Verificación de sincronización:**
   - Espera a ver el ícono verde ✅ en OneDrive
   - No abras en otra PC hasta que sincronice

4. **Respaldos periódicos:**
   - Exporta reportes semanalmente
   - Guarda copias de respaldo fuera de OneDrive

---

## 📞 Soporte

Para dudas o problemas:
- **Email:** elizandrou@outlook.com
- **GitHub:** https://github.com/eurizar/CONTROL-DE-INVENTARIOS

---

© 2025 Elizandro Urizar - Todos los derechos reservados
