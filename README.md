# Sistema de Control de Inventarios v2.0

Un sistema completo y moderno para la gestión de inventarios de productos desarrollado en Python con tkinter y ttkbootstrap.

## 🎨 Nuevo Diseño UI Mejorado

Esta versión incluye una interfaz completamente rediseñada con:
- ✨ **Diseño Moderno**: Interfaz actualizada con ttkbootstrap
- 🎨 **Temas Personalizables**: 18+ temas diferentes para elegir
- 📊 **Dashboard Visual**: Tarjetas informativas con métricas clave
- 🎯 **Iconos Intuitivos**: Emojis y símbolos para mejor navegación
- 🔍 **Búsqueda Integrada**: Filtrado rápido de productos
- 📱 **Responsive**: Diseño que se adapta a diferentes tamaños
- 🌈 **Colores Alternados**: Filas con colores para mejor lectura
- ⚠️ **Alertas Visuales**: Productos con stock bajo resaltados en rojo
<img width="1679" height="1000" alt="image" src="https://github.com/user-attachments/assets/26febc78-bea0-4925-8c38-eb38289b4e6f" />

## 🚀 Características

### Gestión de Productos
- ✅ Crear productos con precio de compra y porcentaje de ganancia
- ✅ Cálculo automático del precio de venta
- ✅ Actualización de información de productos
- ✅ Control de stock en tiempo real

### Control de Compras
- ✅ Registro de compras de mercadería
- ✅ Actualización automática del stock
- ✅ Historial completo de compras
- ✅ Cálculo de totales

### Control de Ventas
- ✅ Registro de ventas con validación de stock
- ✅ Reducción automática del inventario
- ✅ Historial completo de ventas
- ✅ Cálculo de ingresos

### Reportes Financieros
- ✅ Dashboard visual con tarjetas informativas
- ✅ Total de compras realizadas (con formato de miles)
- ✅ Total de ventas + ganancia (visualmente destacado)
- ✅ Saldo total en banco (ventas acumuladas)
- ✅ Valor actual del inventario (stock valorizado)
- ✅ Productos con stock bajo (alertas visuales en rojo)
- ✅ Gráficos y métricas de un vistazo

### Gestión de Base de Datos
- ✅ Base de datos SQLite local
- ✅ **☁️ Sincronización con OneDrive** (¡NUEVO!)
- ✅ Posibilidad de cargar/cambiar base de datos
- ✅ Uso compartido entre múltiples computadoras
- ✅ Exportación de reportes
- ✅ Backup automático
- ✅ **Cambio de temas en tiempo real**
- ✅ **Interfaz personalizable**

### ☁️ Sincronización Multi-Computadora (¡NUEVO!)
- ✅ **Configuración automática con OneDrive**
- ✅ **Detección automática de la carpeta OneDrive**
- ✅ **Sincronización en tiempo real** entre computadoras
- ✅ **Ubicación manual** compatible con Google Drive/Dropbox
- ✅ **Indicadores visuales** del estado de sincronización
- ✅ **Respaldo en la nube** automático
- 📖 [**Ver Guía Completa de OneDrive**](GUIA_ONEDRIVE.md)

## 🎨 Temas Disponibles

El sistema incluye múltiples temas modernos que puedes cambiar desde la pestaña de Configuración:

**Temas Claros:**
- Cosmo (predeterminado) - Moderno y limpio
- Flatly - Plano y minimalista
- Litera - Profesional
- Minty - Fresco y verde
- Lumen - Brillante
- Sandstone - Cálido
- Yeti - Clásico
- United - Corporativo
- Journal - Editorial

**Temas Oscuros:**
- Darkly - Oscuro elegante
- Superhero - Oscuro con acentos
- Solar - Tonos tierra oscuros
- Cyborg - Futurista
- Vapor - Synthwave

## 📁 Estructura del Proyecto

```
INVENTARIOS/
├── main.py                          # Archivo principal para ejecutar
├── config.py                        # Configuración del sistema
├── requirements.txt                 # Dependencias
├── README.md                        # Esta documentación
├── data/                           # Directorio para bases de datos
│   └── inventarios.db              # Base de datos principal (se crea automáticamente)
└── src/                           # Código fuente
    ├── controllers/               # Lógica de negocio
    │   └── inventario_controller.py
    ├── database/                  # Gestión de base de datos
    │   └── database_manager.py
    ├── models/                    # Modelos de datos
    │   └── models.py
    └── ui/                        # Interfaz gráfica
        └── main_window.py
```

## 🔧 Instalación y Uso

### Requisitos Previos
- Python 3.7 o superior
- tkinter (incluido con Python)
- ttkbootstrap (se instala automáticamente)
- sqlite3 (incluido con Python)

### Instalación
1. Clona o descarga el proyecto
2. Navega al directorio del proyecto
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecutar la Aplicación
```bash
python main.py
```

## 💰 Manejo de Moneda

El sistema utiliza **Quetzales (Q)** como moneda de referencia. Todos los montos se muestran con el símbolo Q pero puedes adaptarlo fácilmente en el archivo `config.py`.

## 📊 Funciones Principales

### 1. Gestión de Productos
- **Crear Producto**: Nombre, precio de compra, % de ganancia
- **Precio Automático**: Calcula el precio de venta automáticamente
- **Editar Producto**: Doble clic en la lista para editar

### 2. Compras de Mercadería
- Selecciona el producto
- Ingresa cantidad y precio de compra
- El stock se actualiza automáticamente
- Registra fecha de ingreso

### 3. Registro de Ventas
- Selecciona el producto (muestra stock disponible)
- Ingresa cantidad a vender
- Valida stock disponible
- Actualiza inventario y banco

### 4. Reportes
- **Total Compras**: Suma de toda la mercadería comprada
- **Total Ventas + Ganancia**: Ingresos totales
- **Saldo Banco**: Dinero acumulado por ventas
- **Valor Inventario**: Valor actual del stock
- **Stock Bajo**: Productos que necesitan reposición

## 🗃️ Base de Datos

El sistema utiliza SQLite con las siguientes tablas:
- `productos`: Información de productos
- `compras`: Registro de compras
- `ventas`: Registro de ventas
- `movimientos_stock`: Historial de movimientos

## 🔄 Backup y Restauración

- **Cargar BD**: Carga una base de datos existente
- **Nueva BD**: Crea una nueva base de datos vacía
- **Exportar**: Genera un reporte completo en texto

## 🎨 Interfaz de Usuario

La interfaz está organizada en pestañas con diseño moderno:

1. **📦 Productos**: Gestión completa de productos con búsqueda
   - Formulario con campos validados
   - Cálculo automático de precio de venta
   - Lista ordenable con colores alternados
   - Alertas visuales para stock bajo

2. **🛒 Compras**: Registro de compras de mercadería
   - Selector de productos
   - Cálculo automático de totales
   - Historial completo con fechas

3. **💰 Ventas**: Registro de ventas
   - Validación de stock disponible
   - Indicador visual de stock
   - Actualización automática de inventario

4. **📊 Reportes**: Dashboard con métricas visuales
   - Tarjetas informativas coloridas
   - Totales con formato de miles
   - Alertas de productos con stock bajo

5. **⚙️ Configuración**: Gestión y personalización
   - Cambio de base de datos
   - Selección de temas
   - Exportación de reportes
   - Información del sistema

## 🚀 Características Avanzadas

- **Validaciones Inteligentes**: Controles de stock, precios válidos, etc.
- **Cálculos Automáticos**: Precios de venta, totales, ganancias
- **Historial Completo**: Todos los movimientos quedan registrados
- **Interfaz Moderna**: Diseño actualizado con ttkbootstrap
- **Búsqueda Rápida**: Filtra productos al escribir
- **Ordenamiento**: Haz clic en las columnas para ordenar
- **Colores Alternados**: Filas con colores para mejor lectura
- **Alertas Visuales**: Productos con stock bajo en rojo
- **Temas Personalizables**: Más de 18 temas para elegir
- **Responsive**: Se adapta a diferentes tamaños de ventana
- **Escalabilidad**: Fácil de expandir y modificar
- **Formato de Miles**: Números grandes con separadores de miles

## 🔧 Personalización

Puedes modificar:
- **Moneda**: Cambia el símbolo en `config.py`
- **Límite Stock Bajo**: Ajusta el umbral de stock mínimo
- **Colores y Tema**: Modifica la interfaz en `main_window.py`
- **Reportes**: Personaliza los formatos de exportación

## 📝 Notas Importantes

1. La base de datos se crea automáticamente la primera vez
2. Todos los precios incluyen cálculo automático de ganancia
3. El stock se actualiza en tiempo real
4. Las validaciones previenen errores comunes
5. Los reportes se actualizan automáticamente

## 🆘 Soporte

Si encuentras algún problema:
1. Verifica que Python esté instalado correctamente
2. Asegúrate de que tkinter esté disponible
3. Revisa los mensajes de error en la consola
4. Verifica los permisos de escritura en el directorio

---

## 📜 Licencia y Derechos de Autor

**© 2025 Elizandro Urizar. Todos los derechos reservados.**

### ⚠️ SOFTWARE PROPIETARIO

Este software es **propiedad exclusiva del autor** y está protegido por derechos de autor.

**USO PERMITIDO:**
- ✅ **Uso Personal**: Gratuito para uso individual sin fines de lucro
- ✅ **Uso Comercial**: Disponible para pequeños negocios mediante licencia pagada

**ESTÁ PROHIBIDO SIN LICENCIA:**
- ❌ Revender o redistribuir el software
- ❌ Uso comercial sin licencia adquirida
- ❌ Modificar y distribuir como propio
- ❌ Eliminar avisos de copyright
- ❌ Uso en múltiples negocios con una sola licencia

### 💼 Licencia Comercial

Si deseas usar este sistema en tu negocio:
- 📦 **Licencia disponible** para pequeños y medianos negocios
- 💰 **Costo accesible** según necesidades
- 🔧 **Soporte incluido** en algunas modalidades
- 📞 **Contacto directo** con el desarrollador

### 📧 Contacto y Adquisición

Para adquirir licencia comercial o consultas:

**Autor:** Elizandro Urizar  
**Email:** elizandrou@outlook.com

*Toda copia, modificación o uso comercial sin licencia constituye una violación de los derechos de autor.*

---

¡Disfruta usando tu sistema de inventarios! 🎉
