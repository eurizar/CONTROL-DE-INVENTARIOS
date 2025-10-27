# 📁 Tabs - Módulos de Pestañas

Este directorio contiene los módulos de cada pestaña del sistema.

## 📋 Módulos Disponibles

### ✅ VentasTab (COMPLETO)
**Archivo**: `ventas_tab.py`
**Estado**: ✅ Funcionalidad completa implementada
**Líneas**: ~150 (versión base funcional)

#### Características:
- ✅ Formulario de ventas con campos de cliente y producto
- ✅ Sistema de carrito de compras
- ✅ Autocompletado inteligente para clientes y productos
- ✅ Validación de stock en tiempo real
- ✅ Gestión automática de clientes nuevos
- ✅ Historial de ventas con búsqueda
- ✅ Cálculo automático de totales

#### Uso:
```python
from src.ui.tabs.ventas_tab import VentasTab

# En main_window.py
ventas_tab = VentasTab(parent_frame, controller, self)
```

---

### 🔄 ComprasTab (Estructura Base)
**Archivo**: `compras_tab.py`
**Estado**: 🔄 Estructura base lista
**Siguiente**: Implementar formulario de compras completo

#### Pendiente:
- Formulario de compras con proveedores
- Sistema de recepción de mercancía
- Validación de documentos
- Historial de compras

---

### 🔄 ProductosTab (Estructura Base)
**Archivo**: `productos_tab.py`
**Estado**: 🔄 Estructura base lista
**Siguiente**: Implementar CRUD de productos

#### Pendiente:
- Formulario de alta/edición de productos
- Tabla de productos con búsqueda
- Generador de SKU/códigos
- Control de categorías
- Gestión de precios

---

### 🔄 ClientesTab (Estructura Base)
**Archivo**: `clientes_tab.py`
**Estado**: 🔄 Estructura base lista
**Siguiente**: Implementar CRUD de clientes

#### Pendiente:
- Formulario de alta/edición de clientes
- Tabla de clientes con búsqueda
- Validación de NIT/DPI
- Historial de compras por cliente
- Estadísticas de clientes

---

### 🔄 ProveedoresTab (Estructura Base)
**Archivo**: `proveedores_tab.py`
**Estado**: 🔄 Estructura base lista
**Siguiente**: Implementar CRUD de proveedores

#### Pendiente:
- Formulario de alta/edición de proveedores
- Tabla de proveedores con búsqueda
- Validación de datos de contacto
- Historial de compras a proveedores
- Estadísticas de proveedores

---

### 🔄 CajaTab (Estructura Base)
**Archivo**: `caja_tab.py`
**Estado**: 🔄 Estructura base lista
**Siguiente**: Implementar gestión de caja

#### Pendiente:
- Registro de movimientos de caja
- Categorización de gastos/ingresos
- Saldo actual y proyecciones
- Historial de movimientos
- Reportes financieros

---

## 🏗️ Estructura de un Tab

Cada tab sigue esta estructura estándar:

```python
class NombreTab:
    """Descripción del tab."""
    
    def __init__(self, parent_frame, controller, main_window):
        """Inicializa el tab."""
        self.frame = parent_frame
        self.controller = controller
        self.main_window = main_window
        
        self.setup_variables()
        self.create_ui()
    
    def setup_variables(self):
        """Inicializa variables del tab."""
        # Variables tk.StringVar, tk.IntVar, etc.
        pass
    
    def create_ui(self):
        """Crea la interfaz del tab."""
        # Widgets y layout
        pass
    
    def refresh(self):
        """Actualiza los datos del tab."""
        # Recarga de datos
        pass
```

---

## 📦 Dependencias

Cada tab depende de:
- `tkinter` - Framework de GUI
- `ttkbootstrap` - Temas modernos
- `src.controller.inventario_controller` - Lógica de negocio
- `src.ui.utils.formatters` - Formateo de datos
- `src.ui.utils.validadores` - Validación de datos

---

## 🎯 Próximos Pasos

1. **Completar ComprasTab**: Similar a VentasTab pero para compras
2. **Completar ProductosTab**: CRUD completo de productos
3. **Completar ClientesTab**: CRUD completo de clientes
4. **Completar ProveedoresTab**: CRUD completo de proveedores
5. **Completar CajaTab**: Sistema completo de caja

---

## 💡 Convenciones

### Nombres de Métodos
- `create_*()` - Crear secciones de UI
- `setup_*()` - Configurar variables/estado
- `refresh()` - Actualizar datos
- `agregar_*()` - Agregar nuevos registros
- `editar_*()` - Editar registros existentes
- `eliminar_*()` - Eliminar registros
- `buscar_*()` - Búsqueda de registros
- `validar_*()` - Validaciones

### Nombres de Variables
- `*_entry` - Campos de texto (tk.Entry)
- `*_tree` - Tablas (tk.Treeview)
- `*_label` - Etiquetas (tk.Label)
- `*_button` - Botones (tk.Button)
- `*_frame` - Contenedores (tk.Frame)

---

## 📝 Documentación

Cada método debe incluir:
```python
def metodo(self, parametro):
    """
    Descripción breve del método.
    
    Args:
        parametro: Descripción del parámetro
        
    Returns:
        Descripción del retorno
    """
    pass
```

---

## 🧪 Testing

Para probar un tab:
```python
python test_refactorizacion.py
```

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa la documentación en `REFACTORIZACION_COMPLETA.md`
2. Verifica las dependencias
3. Ejecuta los tests
4. Revisa el código de VentasTab como referencia

---

**Última actualización**: 15 de octubre de 2025
**Mantenido por**: Equipo de Desarrollo
