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

### 📌 **IMPORTANTE: ¿Misma cuenta o cuenta diferente de OneDrive?**

#### **Escenario A: Misma Cuenta de OneDrive en Ambas PCs** ⭐ (Más Fácil)

Si ambas computadoras usan **la misma cuenta de OneDrive**:

**Paso 1:** Instalar el Sistema en la segunda PC
- Instala el **Sistema de Inventarios** en la segunda computadora
- Asegúrate de que **OneDrive esté sincronizado** con la misma cuenta

**Paso 2:** Configurar la Base de Datos
1. Abre el programa
2. Ve a **⚙️ Configuración**
3. En **☁️ Sincronización con OneDrive**, haz clic en:
   - **"📂 Seleccionar Ubicación Manual"**
4. Selecciona **"SÍ"** (Seleccionar base de datos existente)
5. Navega a la carpeta de OneDrive
6. Busca: `OneDrive\Sistema_Inventarios\inventarios.db`
7. Abre el archivo

**Paso 3:** ¡Listo!
- Ahora ambas computadoras usan la misma base de datos
- Los cambios se sincronizan automáticamente

---

#### **Escenario B: Cuentas Diferentes de OneDrive** 🔄 (Requiere Compartir)

Si cada computadora tiene **su propia cuenta de OneDrive**, necesitas compartir la carpeta:

##### **👤 En la Computadora Principal (Tu cuenta):**

1. **Configurar BD en OneDrive** (si aún no lo has hecho)
   - Abre el Sistema de Inventarios
   - Ve a **⚙️ Configuración** → **"☁️ Configurar BD en OneDrive"**

2. **Compartir la Carpeta con tu Amigo**
   - Abre el **Explorador de Archivos**
   - Navega a: `OneDrive\Sistema_Inventarios`
   - **Click derecho** en la carpeta → **"Compartir"** o **"Share"**
   - Ingresa el **email de tu amigo** (su cuenta Microsoft/OneDrive)
   - Selecciona permisos: **"Puede editar"** ⚠️ (MUY IMPORTANTE)
   - Click en **"Enviar"** o **"Send"**

3. **Confirmar que se Compartió**
   - Tu amigo recibirá un email de invitación
   - Verificar que tenga permisos de edición

##### **👥 En la Computadora del Amigo (Otra cuenta):**

1. **Aceptar la Invitación**
   - Revisar el email de invitación de OneDrive
   - Click en **"Abrir"** o **"Open"**
   - Se abrirá OneDrive en el navegador mostrando la carpeta compartida

2. **Agregar a Mi OneDrive**
   - En el navegador (OneDrive web), buscar la carpeta `Sistema_Inventarios`
   - Click derecho (o botón "...") → **"Agregar acceso directo a Mi OneDrive"**
   - Esto agregará la carpeta a su OneDrive local

3. **Esperar Sincronización**
   - Abrir la aplicación de OneDrive en la PC
   - Esperar a que la carpeta compartida se sincronice (ícono ✅)
   - La carpeta aparecerá en su OneDrive local

4. **Configurar el Sistema de Inventarios**
   - Descargar e instalar el Sistema de Inventarios
   - Abrir el programa
   - Ir a **⚙️ Configuración**
   - Click en **"📂 Seleccionar Ubicación Manual"**
   - Seleccionar **"SÍ"** (Seleccionar base de datos existente)
   - Navegar a la carpeta sincronizada:
     - Puede estar en: `OneDrive\Sistema_Inventarios\inventarios.db`
     - O en: `OneDrive\Compartido conmigo\Sistema_Inventarios\inventarios.db`
   - Abrir el archivo `inventarios.db`

5. **¡Listo!**
   - Ahora ambos usan la misma base de datos
   - Los cambios se sincronizan entre las dos cuentas

##### **⚠️ REGLAS CRÍTICAS con Cuentas Diferentes:**

🔴 **NUNCA usar el programa al mismo tiempo**
- Coordinar quién lo usa y cuándo
- Crear un sistema de turnos

🟡 **Comunicación constante**
- Usar WhatsApp, Telegram, etc. para avisar
- Ejemplo: "Voy a usar el sistema ahora" → "Ok, yo ya terminé, espera 2 minutos"

🟢 **Esperar sincronización completa**
- Después de cerrar el programa, esperar **2-3 minutos**
- Verificar ícono de OneDrive (debe estar ✅)
- Solo entonces el otro usuario puede abrir

---

#### **Escenario C: Cuenta Compartida del Negocio** 🏢 (Recomendado para Empresas)

Si es para un negocio formal, considera crear una cuenta específica:

1. **Crear cuenta Microsoft del negocio**
   - Email: `inventario.negocio@outlook.com` (ejemplo)
   - Contraseña compartida entre usuarios autorizados

2. **Configurar OneDrive en ambas PCs**
   - Iniciar sesión con la misma cuenta en ambas computadoras
   - OneDrive sincronizará automáticamente

3. **Ventajas:**
   - ✅ No necesitas compartir carpetas
   - ✅ Más fácil de gestionar
   - ✅ Datos del negocio separados de cuentas personales
   - ✅ Mejor control de acceso

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
