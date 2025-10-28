"""
Sistema de Control de Inventarios v2.0 - Ventana Principal
============================================================

Ventana principal del sistema de inventarios con interfaz gráfica moderna.

Autor: Elizandro Urizar
Email: elizandrou@outlook.com
© 2025 Elizandro Urizar. Todos los derechos reservados.

SOFTWARE PROPIETARIO - Uso Personal Gratuito / Licencia Comercial Disponible
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import os
import sys
import locale

# Función para obtener la ruta correcta de recursos (PyInstaller compatible)
def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no es PyInstaller, usar la ruta del directorio actual
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Configurar locale en español para los calendarios
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'es')
        except:
            pass  # Si no funciona, usar el locale por defecto

# Agregar el directorio raíz al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.controllers.inventario_controller import InventarioController
from src.config.settings import Settings

# Importar utilidades compartidas de UI
from src.ui.utils import sort_treeview, centrar_ventana, agregar_icono, configurar_navegacion_calendario

# Importar los módulos refactorizados
from src.ui.tabs.ventas_tab import VentasTab
from src.ui.tabs.compras_tab import ComprasTab
from src.ui.tabs.productos_tab import ProductosTab
from src.ui.tabs.clientes_tab import ClientesTab
from src.ui.tabs.proveedores_tab import ProveedoresTab
from src.ui.tabs.caja_tab import CajaTab
from src.ui.tabs.reportes_tab import ReportesTab
from src.ui.tabs.configuracion_tab import ConfiguracionTab

class MainWindow:
    def __init__(self, usuario=None, root=None):
        # Guardar información del usuario autenticado
        self.usuario_actual = usuario
        
        # Cargar el tema guardado
        tema_guardado = Settings.get_theme()
        
        # Usar la raíz existente o crear una nueva
        if root is not None:
            self.root = root
            self.root.deiconify()  # Mostrar la ventana oculta
            # Limpiar el contenido anterior
            for widget in self.root.winfo_children():
                widget.destroy()
        else:
            # Usar ttkbootstrap para un diseño moderno
            self.root = tb.Window(themename=tema_guardado)
        
        # Configurar título con nombre de usuario
        titulo = "Sistema de Control de Inventarios"
        if self.usuario_actual:
            titulo += f" - Usuario: {self.usuario_actual['nombre_completo']}"
        self.root.title(titulo)
        
        # Ocultar ventana temporalmente para evitar parpadeo al centrar
        self.root.withdraw()
        
        # Configurar tamaño
        ancho_ventana = 1500
        alto_ventana = 900
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}")
        
        # Configurar icono
        try:
            icon_path = resource_path("inventario.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")
            pass  # Si no encuentra el icono, continuar sin él
        
        # Configurar estilo
        self.root.resizable(True, True)
        self.root.minsize(1200, 700)
        
        # Calcular posición centrada
        self.root.update_idletasks()
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.root.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')
        
        # Inicializar controlador
        self.controller = InventarioController()
        
        # Variables para los formularios
        self.setup_variables()
        
        # Configurar estilos de selección para Treeviews
        self.setup_treeview_selection_style()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Cargar datos iniciales
        self.refresh_all_data()
        
        # Mostrar ventana ya centrada (evita parpadeo)
        self.root.deiconify()
    
    def setup_variables(self):
        """Configura las variables para los formularios"""
        # Variables para producto
        self.producto_codigo = tk.StringVar()
        self.producto_nombre = tk.StringVar()
        self.producto_categoria = tk.StringVar()
        self.producto_precio_compra = tk.DoubleVar()
        self.producto_ganancia = tk.DoubleVar()
        self.producto_precio_venta_manual = tk.DoubleVar()
        self.producto_tipo_calculo = tk.StringVar(value="precio")  # 'precio' por defecto (antes 'porcentaje')
        
        # Variables para proveedor
        self.proveedor_nombre = tk.StringVar()
        self.proveedor_nit = tk.StringVar()
        self.proveedor_direccion = tk.StringVar()
        self.proveedor_telefono = tk.StringVar()
        self.proveedor_busqueda = tk.StringVar()
        
        # Variables para cliente
        self.cliente_nombre = tk.StringVar()
        self.cliente_nit = tk.StringVar()
        self.cliente_direccion = tk.StringVar()
        self.cliente_telefono = tk.StringVar()
        self.cliente_busqueda = tk.StringVar()
        
        # Variables para compra
        self.compra_cantidad = tk.IntVar()
        self.compra_precio = tk.DoubleVar()
        self.compra_no_documento = tk.StringVar()
        self.compra_fecha = tk.StringVar()
        self.compra_producto_busqueda = tk.StringVar()
        self.compra_proveedor_busqueda = tk.StringVar()
        self.compra_es_perecedero = tk.BooleanVar(value=False)
        self.compra_fecha_vencimiento = tk.StringVar()
        
        # Variables para venta
        self.venta_cantidad = tk.IntVar(value=1)  # Iniciar en 1 por defecto
        self.venta_precio = tk.DoubleVar()
        self.venta_fecha = tk.StringVar()
        self.venta_producto_busqueda = tk.StringVar()
        self.venta_cliente_busqueda = tk.StringVar()
        self.venta_cliente_nit = tk.StringVar()  # Campo para NIT/DPI o CF
        self.venta_cliente_direccion = tk.StringVar()  # Campo para Dirección
        self.venta_cliente_telefono = tk.StringVar()  # Campo para Teléfono
        
        # Variables para caja
        self.caja_tipo = tk.StringVar(value='EGRESO')
        self.caja_categoria = tk.StringVar(value='GASTO_OPERATIVO')
        self.caja_concepto = tk.StringVar()
        self.caja_monto = tk.DoubleVar()
        
        # Variable para producto seleccionado
        self.producto_seleccionado = None
        self.proveedor_seleccionado = None
        self.cliente_seleccionado = None
        self.compra_producto_id = None
        self.compra_proveedor_id = None
        self.venta_producto_id = None
        self.venta_cliente_id = None
        
        # Variables para el carrito de ventas
        self.carrito_ventas = []  # Lista de productos en el carrito
        
        # Variables para guardar datos del generador SKU
        self.sku_data = {
            'nombre': '',
            'categoria': '',
            'marca': '',
            'color': '',
            'tamaño': '',
            'dibujo': '',
            'cod_color': ''
        }
        
        # Banderas para lazy loading (optimización)
        self.tabs_loaded = {
            'productos': False,
            'proveedores': False,
            'clientes': False,
            'compras': False,
            'ventas': False,
            'caja': False,
            'reportes': False
        }
    
    def get_theme_hover_color(self, theme_name):
        """Retorna el color de hover apropiado según el tema activo"""
        theme_colors = {
            'cosmo': '#2780e3',      # Azul Cosmo
            'flatly': '#4a5568',     # Gris oscuro para Flatly
            'minty': '#78c2ad',      # Verde menta Minty
            'yeti': '#008cba',       # Azul Yeti
        }
        return theme_colors.get(theme_name.lower(), '#0078d4')  # Default azul
    
    def setup_treeview_selection_style(self):
        """Configura el estilo de selección para todos los Treeviews"""
        style = tb.Style()
        
        # Obtener el tema actual
        current_theme = self.root.style.theme.name
        hover_color = self.get_theme_hover_color(current_theme)
        
        # Configurar colores de selección según el tema - MÁS VISIBLES
        theme_selection_colors = {
            'cosmo': '#2780e3',      # Azul Cosmo
            'flatly': '#5a6c7d',     # Gris más oscuro para Flatly
            'minty': '#4CAF50',      # Verde más fuerte para Minty
            'yeti': '#007ba7',       # Azul más oscuro Yeti
        }
        
        bg_color = theme_selection_colors.get(current_theme.lower(), '#0078d4')
        
        # Configurar el estilo de selección para Treeview - MÁS VISIBLE
        style.map('Treeview',
            background=[('selected', bg_color), ('active', bg_color)],
            foreground=[('selected', 'white'), ('active', 'white')]
        )
        
        # Asegurar que el foco también sea visible
        style.configure('Treeview',
            fieldbackground='white',
            background='white'
        )
    
    def centrar_ventana(self, ventana):
        """Centra una ventana en la pantalla (delegado a utilidades)"""
        centrar_ventana(ventana)
    
    def agregar_icono(self, ventana):
        """Agrega el icono a una ventana (delegado a utilidades)"""
        agregar_icono(ventana)
    
    def configurar_navegacion_calendario(self, date_entry):
        """Configura navegación mejorada por año en un DateEntry (delegado a utilidades)"""
        configurar_navegacion_calendario(date_entry)
    
    def crear_tooltip(self, widget, texto):
        """Crea un tooltip para un widget"""
        def mostrar_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=texto, background="#ffffe0", 
                           relief='solid', borderwidth=1, 
                           font=('Segoe UI', 9), justify='left', padx=5, pady=5)
            label.pack()
            
            def ocultar_tooltip(event=None):
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', ocultar_tooltip, add='+')
            tooltip.bind('<Leave>', ocultar_tooltip)
            
            # Auto-ocultar después de 4 segundos
            tooltip.after(4000, tooltip.destroy)
        
        def ocultar_si_existe(event):
            if hasattr(widget, 'tooltip'):
                try:
                    widget.tooltip.destroy()
                except:
                    pass
        
        widget.bind('<Enter>', lambda e: [ocultar_si_existe(e), mostrar_tooltip(e)])
    
    def agregar_controles_año(self, date_entry):
        """Agrega controles de navegación por año al calendario abierto"""
        # Ya no se usa - mantenido para compatibilidad
        pass
    
    def inyectar_botones_año(self, header_frame, date_entry, toplevel):
        """Inyecta botones de navegación por año en el header del calendario"""
        # Ya no se usa - mantenido para compatibilidad
        pass
    
    def cambiar_año_calendario(self, date_entry, delta):
        """Cambia el año del calendario"""
        # Ya no se usa - mantenido para compatibilidad
        pass
    
    def seleccionar_rango_fechas(self, titulo="Seleccionar Rango de Fechas"):
        """Muestra un diálogo para seleccionar rango de fechas"""
        from ttkbootstrap import DateEntry
        from datetime import datetime, timedelta
        
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
        dialog.geometry("500x280")
        dialog.transient(self.root)
        
        # Ocultar ventana temporalmente para evitar parpadeo
        dialog.withdraw()
        
        dialog.grab_set()
        self.agregar_icono(dialog)
        
        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (280 // 2)
        dialog.geometry(f'500x280+{x}+{y}')
        
        # Mostrar ventana ya centrada
        dialog.deiconify()
        
        resultado = {'aceptado': False, 'fecha_inicio': None, 'fecha_fin': None}
        
        # Frame principal
        frame = tb.Frame(dialog, padding=20)
        frame.pack(fill='both', expand=True)
        
        tb.Label(
            frame, 
            text="Seleccione el rango de fechas para el reporte:",
            font=('Segoe UI', 11, 'bold')
        ).pack(pady=(0, 20))
        
        # Frame para fechas
        dates_frame = tb.Frame(frame)
        dates_frame.pack(pady=10)
        
        # Fecha inicio
        tb.Label(dates_frame, text="Fecha Inicio:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=10)
        fecha_inicio_cal = DateEntry(
            dates_frame,
            dateformat='%d/%m/%Y',
            firstweekday=0,
            width=18,
            startdate=datetime.now() - timedelta(days=30)  # 30 días atrás por defecto
        )
        fecha_inicio_cal.grid(row=0, column=1, padx=10, pady=10)
        
        # Fecha fin
        tb.Label(dates_frame, text="Fecha Fin:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=5, pady=10)
        fecha_fin_cal = DateEntry(
            dates_frame,
            dateformat='%d/%m/%Y',
            firstweekday=0,
            width=18,
            startdate=datetime.now()  # Hoy por defecto
        )
        fecha_fin_cal.grid(row=1, column=1, padx=10, pady=10)
        
        # Botones
        btn_frame = tb.Frame(frame)
        btn_frame.pack(pady=20)
        
        def aceptar():
            resultado['aceptado'] = True
            resultado['fecha_inicio'] = fecha_inicio_cal.entry.get()
            resultado['fecha_fin'] = fecha_fin_cal.entry.get()
            dialog.destroy()
        
        def cancelar():
            dialog.destroy()
        
        tb.Button(
            btn_frame,
            text="✓ Aceptar",
            command=aceptar,
            bootstyle="success",
            width=15
        ).pack(side='left', padx=5)
        
        tb.Button(
            btn_frame,
            text="✗ Cancelar",
            command=cancelar,
            bootstyle="secondary",
            width=15
        ).pack(side='left', padx=5)
        
        # Configurar navegación mejorada en calendarios
        dialog.after(100, lambda: self.configurar_navegacion_calendario(fecha_inicio_cal))
        dialog.after(100, lambda: self.configurar_navegacion_calendario(fecha_fin_cal))
        
        dialog.wait_window()
        return resultado
    
    def pedir_texto(self, titulo, mensaje):
        """Muestra un diálogo de entrada centrado"""
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
        dialog.geometry("400x190")
        dialog.transient(self.root)
        
        # Ocultar ventana temporalmente para evitar parpadeo
        dialog.withdraw()
        
        dialog.grab_set()
        self.agregar_icono(dialog)
        
        resultado = tk.StringVar()
        
        # Frame principal
        frame = tb.Frame(dialog, padding=20)
        frame.pack(fill='both', expand=True)
        
        # Mensaje
        tb.Label(frame, text=mensaje, font=('Segoe UI', 10)).pack(pady=(0, 15))
        
        # Entry
        entry = tb.Entry(frame, textvariable=resultado, width=40, font=('Segoe UI', 10))
        entry.pack(pady=10)
        entry.focus()
        
        # Frame para botones
        btn_frame = tb.Frame(frame)
        btn_frame.pack(pady=15)
        
        valor_retorno = [None]
        
        def aceptar(event=None):
            valor_retorno[0] = resultado.get()
            dialog.destroy()
        
        def cancelar():
            valor_retorno[0] = None
            dialog.destroy()
        
        tb.Button(btn_frame, text="OK", command=aceptar, bootstyle="primary", width=10).pack(side='left', padx=5)
        tb.Button(btn_frame, text="Cancel", command=cancelar, bootstyle="secondary", width=10).pack(side='left', padx=5)
        
        # Bind Enter key
        entry.bind('<Return>', aceptar)
        
        # Centrar diálogo
        self.centrar_ventana(dialog)
        
        # Mostrar ventana ya centrada
        dialog.deiconify()
        
        # Esperar a que se cierre
        dialog.wait_window()
        
        return valor_retorno[0]
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Crear frame principal con color de fondo
        main_container = tb.Frame(self.root, bootstyle="light")
        main_container.pack(fill='both', expand=True)
        
        # Crear barra de título personalizada
        self.create_header(main_container)
        
        # Crear notebook principal con estilo mejorado
        self.notebook = tb.Notebook(main_container, bootstyle="primary")
        self.notebook.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Binding para lazy loading (optimización de rendimiento)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Configurar estilos de fuente para las tablas
        style = tb.Style()
        current_theme = self.root.style.theme.name
        
        # Configurar estilos unificados para todas las tablas (todos los temas)
        style.configure("Treeview", 
                       font=("Segoe UI", 10), 
                       rowheight=30)
        
        style.configure("Treeview.Heading", 
                       font=("Segoe UI", 9, "bold"), 
                       relief="raised", 
                       borderwidth=2,
                       padding=5)
        
        # Configurar efecto hover con color del tema activo
        hover_color = self.get_theme_hover_color(current_theme)
        style.map("Treeview", background=[("selected", hover_color)], foreground=[("selected", "white")])
        
        # Crear las pestañas usando las clases refactorizadas
        self.crear_tabs_refactorizados()
        
        # Configurar efecto hover para todas las tablas
        self.setup_hover_effects()
    
    def crear_tabs_refactorizados(self):
        """Crea todas las pestañas usando las clases refactorizadas"""
        # Crear frames para cada tab
        self.productos_frame = tb.Frame(self.notebook, bootstyle="light")
        self.proveedores_frame = tb.Frame(self.notebook, bootstyle="light")
        self.clientes_frame = tb.Frame(self.notebook, bootstyle="light")
        self.compras_frame = tb.Frame(self.notebook, bootstyle="light")
        self.ventas_frame = tb.Frame(self.notebook, bootstyle="light")
        self.caja_frame = tb.Frame(self.notebook, bootstyle="light")
        self.reportes_frame = tb.Frame(self.notebook, bootstyle="light")
        self.config_frame = tb.Frame(self.notebook, bootstyle="light")
        
        # Agregar tabs al notebook
        self.notebook.add(self.productos_frame, text="📦 Productos")
        self.notebook.add(self.proveedores_frame, text="🏭 Proveedores")
        self.notebook.add(self.clientes_frame, text="👥 Clientes")
        self.notebook.add(self.compras_frame, text="🛒 Compras")
        self.notebook.add(self.ventas_frame, text="💰 Ventas")
        self.notebook.add(self.caja_frame, text="💵 Caja")
        self.notebook.add(self.reportes_frame, text="📊 Reportes")
        self.notebook.add(self.config_frame, text="⚙️ Configuración")
        
        # Instanciar las clases de tabs
        self.productos_tab = ProductosTab(self.productos_frame, self.controller, self)
        self.proveedores_tab = ProveedoresTab(self.proveedores_frame, self.controller, self)
        self.clientes_tab = ClientesTab(self.clientes_frame, self.controller, self)
        self.compras_tab = ComprasTab(self.compras_frame, self.controller, self)
        self.ventas_tab = VentasTab(self.ventas_frame, self.controller, self)
        self.caja_tab = CajaTab(self.caja_frame, self.controller, self)
        self.reportes_tab = ReportesTab(self.reportes_frame, self.controller, self)
        self.configuracion_tab = ConfiguracionTab(self.config_frame, self.controller, self)
        
        # Mantener referencias a los treeviews para hover effects
        self.productos_tree = self.productos_tab.productos_tree
        self.proveedores_tree = self.proveedores_tab.proveedores_tree
        self.clientes_tree = self.clientes_tab.clientes_tree
        self.compras_tree = self.compras_tab.compras_tree
        self.ventas_tree = self.ventas_tab.ventas_tree
        self.caja_tree = self.caja_tab.caja_tree
        self.stock_tree = self.reportes_tab.stock_tree
    
    def setup_hover_effects(self):
        """Configura efecto hover ligero para todas las tablas"""
        # Lista de todas las tablas en el sistema
        tables = [
            self.productos_tree,
            self.proveedores_tree,
            self.clientes_tree,
            self.compras_tree,
            self.ventas_tree,
            self.caja_tree,
            self.stock_tree
        ]
        
        for tree in tables:
            # Variable para rastrear el último item hover
            tree._last_hover = None
            tree._last_hover_tags = None
            # Eventos de mouse
            tree.bind('<Motion>', lambda e, t=tree: self.on_tree_hover(e, t))
            tree.bind('<Leave>', lambda e, t=tree: self.on_tree_leave(e, t))
            
            # Configurar tag de hover con borde
            tree.tag_configure('hover_effect', background='', foreground='')
    
    def on_tree_hover(self, event, tree):
        """Aplica efecto hover sutil a la fila bajo el cursor"""
        item = tree.identify_row(event.y)
        
        # Si cambió de fila, restaurar la anterior
        if hasattr(tree, '_last_hover') and tree._last_hover and tree._last_hover != item:
            # Restaurar tags originales
            if hasattr(tree, '_last_hover_tags') and tree._last_hover_tags:
                tree.item(tree._last_hover, tags=tree._last_hover_tags)
        
        if item:
            # Guardar tags actuales
            current_tags = tree.item(item, 'tags')
            tree._last_hover_tags = current_tags
            
            # Verificar si tiene color especial y aplicar versión hover
            if current_tags:
                tags_list = list(current_tags)
                hover_applied = False
                
                # Mapeo de tags a sus versiones hover
                hover_map = {
                    'vencido': 'vencido_hover',
                    'critico': 'critico_hover',
                    'advertencia': 'advertencia_hover',
                    'alert_stock': 'alert_stock_hover',
                    'alert_vencido': 'alert_vencido_hover',
                    'alert_critico': 'alert_critico_hover',
                    'alert_advertencia': 'alert_advertencia_hover'
                }
                
                # Buscar y reemplazar con versión hover
                for i, tag in enumerate(tags_list):
                    if tag in hover_map:
                        tags_list[i] = hover_map[tag]
                        hover_applied = True
                        break
                
                if hover_applied:
                    tree.item(item, tags=tuple(tags_list))
                else:
                    # Para filas sin color especial: aplicar selección azul
                    tree.selection_set(item)
            else:
                # Sin tags: aplicar selección azul
                tree.selection_set(item)
            
            # Cambiar cursor para indicar interactividad
            tree.config(cursor='hand2')
            tree._last_hover = item
        else:
            tree.config(cursor='')
    
    def on_tree_leave(self, event, tree):
        """Limpia selección al salir del área de la tabla"""
        if hasattr(tree, '_last_hover') and tree._last_hover:
            # Restaurar tags originales
            if hasattr(tree, '_last_hover_tags') and tree._last_hover_tags:
                tree.item(tree._last_hover, tags=tree._last_hover_tags)
            tree.selection_remove(tree._last_hover)
            tree._last_hover = None
            tree._last_hover_tags = None
            tree.config(cursor='')
    
    def create_header(self, parent):
        """Crea la barra de título superior"""
        header = tb.Frame(parent, bootstyle="primary")
        header.pack(fill='x', padx=15, pady=15)
        
        # Título principal
        title_label = tb.Label(
            header, 
            text="💼 SISTEMA DE CONTROL DE INVENTARIOS - MARTELIZ SHOP",
            font=('Segoe UI', 24, 'bold'),
            bootstyle="inverse-primary"
        )
        title_label.pack(side='left', padx=10, pady=10)
        
        # Frame para botones de acción rápida
        quick_actions = tb.Frame(header, bootstyle="primary")
        quick_actions.pack(side='right', padx=10)
        
        tb.Button(
            quick_actions,
            text="🔄 Actualizar",
            command=self.refresh_all_data,
            bootstyle="info",
            width=14
        ).pack(side='left', padx=5)
        
        tb.Button(
            quick_actions,
            text="📊 Resumen",
            command=self.ir_a_reportes,
            bootstyle="info-outline",
            width=12
        ).pack(side='left', padx=5)
        
        tb.Button(
            quick_actions,
            text="🚪 Salir",
            command=self.salir_sistema,
            bootstyle="danger",
            width=10
        ).pack(side='left', padx=5)
    
    # FUNCIÓN OBSOLETA: create_productos_tab() - Movido a src/ui/tabs/productos_tab.py
    
    # FUNCIÓN OBSOLETA: create_compras_tab() - Movido a src/ui/tabs/compras_tab.py
    
    def create_compras_tab_OBSOLETO(self):
        """Crea la pestaña de gestión de productos"""
        self.productos_frame = tb.Frame(self.notebook, bootstyle="light")
        self.notebook.add(self.productos_frame, text="📦 Productos")
        
        # BOTÓN PRINCIPAL: INGRESAR NUEVO PRODUCTO (prominente al inicio)
        boton_nuevo_frame = tb.Frame(self.productos_frame)
        boton_nuevo_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        tb.Button(
            boton_nuevo_frame,
            text="➕ INGRESAR NUEVO PRODUCTO",
            command=self.abrir_generador_sku,
            bootstyle="success",
            width=35,
            cursor="hand2"
        ).pack(side='left', padx=5)
        
        tb.Label(
            boton_nuevo_frame,
            text="← Comience aquí para agregar productos con código SKU automático",
            font=('Segoe UI', 9, 'italic'),
            bootstyle="secondary"
        ).pack(side='left', padx=10)
        
        # Frame para formulario de productos OPTIMIZADO
        form_frame = tb.Labelframe(
            self.productos_frame, 
            text="✏️ Gestión de Productos", 
            padding=15,
            bootstyle="primary"
        )
        form_frame.pack(fill='x', padx=15, pady=15)
        
        # FILA 1: Código y Nombre
        tb.Label(
            form_frame, 
            text="Código:",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        # Campo de código (solo lectura, se genera automáticamente)
        self.codigo_entry = tb.Entry(
            form_frame, 
            textvariable=self.producto_codigo, 
            width=32,
            font=('Segoe UI', 11, 'bold'),
            state='disabled',
            cursor='arrow'
        )
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tb.Label(
            form_frame, 
            text="Nombre:",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=0, column=2, sticky='w', padx=(20, 5), pady=5)
        
        self.producto_nombre_entry = tb.Entry(
            form_frame, 
            textvariable=self.producto_nombre, 
            width=30,
            font=('Segoe UI', 10),
            state='readonly',
            cursor='arrow'
        )
        self.producto_nombre_entry.grid(row=0, column=3, padx=5, pady=5, sticky='ew')
        # Configurar colores para que sea visible pero claramente no editable
        self.producto_nombre_entry.configure(foreground='#2c3e50', background='#ecf0f1')
        
        # FILA 2: Precio Compra y Categoría
        tb.Label(
            form_frame, 
            text="Precio por Unidad (Q):",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        
        entry_precio_compra = tb.Entry(
            form_frame, 
            textvariable=self.producto_precio_compra, 
            width=15,
            font=('Segoe UI', 10)
        )
        entry_precio_compra.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        entry_precio_compra.bind('<KeyRelease>', lambda e: self.calcular_precio_desde_ganancia() if self.producto_tipo_calculo.get() == "porcentaje" else self.calcular_ganancia_desde_precio())
        
        tb.Label(
            form_frame, 
            text="Categoría:",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=1, column=2, sticky='w', padx=(20, 5), pady=5)
        
        self.producto_categoria_entry = tb.Entry(
            form_frame, 
            textvariable=self.producto_categoria, 
            width=30,
            font=('Segoe UI', 10),
            state='readonly',
            cursor='arrow'
        )
        self.producto_categoria_entry.grid(row=1, column=3, padx=5, pady=5, sticky='ew')
        # Configurar colores para que sea visible pero claramente no editable
        self.producto_categoria_entry.configure(foreground='#2c3e50', background='#ecf0f1')
        
        # FILA 3: Radio buttons de método de cálculo
        tb.Label(
            form_frame, 
            text="Calcular por:",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        
        radio_frame = tb.Frame(form_frame)
        radio_frame.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky='w')
        
        # CAMBIADO: Precio Venta primero, luego % Ganancia
        tb.Radiobutton(
            radio_frame,
            text="Precio Venta",
            variable=self.producto_tipo_calculo,
            value="precio",
            command=self.cambiar_tipo_calculo,
            bootstyle="info"
        ).pack(side='left', padx=5)
        
        tb.Radiobutton(
            radio_frame,
            text="% Ganancia",
            variable=self.producto_tipo_calculo,
            value="porcentaje",
            command=self.cambiar_tipo_calculo,
            bootstyle="info"
        ).pack(side='left', padx=5)
        
        # FILA 4: % Ganancia y Precio de Venta Calculado
        self.label_ganancia = tb.Label(
            form_frame, 
            text="% Ganancia:",
            font=('Segoe UI', 10, 'bold')
        )
        self.label_ganancia.grid(row=3, column=0, sticky='w', padx=5, pady=5)
        
        self.entry_ganancia = tb.Entry(
            form_frame, 
            textvariable=self.producto_ganancia, 
            width=15,
            font=('Segoe UI', 10)
        )
        self.entry_ganancia.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.entry_ganancia.bind('<KeyRelease>', self.calcular_precio_desde_ganancia)
        
        # Precio de venta calculado (a la derecha)
        self.precio_venta_label = tb.Label(
            form_frame, 
            text="Precio de Venta: Q 0.00",
            font=('Segoe UI', 10, 'bold'),
            bootstyle="success"
        )
        self.precio_venta_label.grid(row=3, column=2, sticky='w', padx=(20, 10), pady=5)
        
        # Monto de ganancia (a la derecha del precio de venta)
        self.monto_ganancia_label = tb.Label(
            form_frame, 
            text="Ganancia: Q 0.00",
            font=('Segoe UI', 10, 'bold'),
            bootstyle="warning"
        )
        self.monto_ganancia_label.grid(row=3, column=3, sticky='w', padx=(10, 5), pady=5)
        
        # Campo de Precio de Venta Manual (oculto inicialmente)
        self.label_precio_venta_manual = tb.Label(
            form_frame, 
            text="Precio Venta (Q):",
            font=('Segoe UI', 10, 'bold')
        )
        
        self.entry_precio_venta_manual = tb.Entry(
            form_frame, 
            textvariable=self.producto_precio_venta_manual, 
            width=15,
            font=('Segoe UI', 10)
        )
        self.entry_precio_venta_manual.bind('<KeyRelease>', self.calcular_ganancia_desde_precio)
        
        # Configurar grid para expandir columnas
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=2)
        
        # Bind para calcular precio de venta automáticamente
        self.producto_precio_compra.trace('w', self.calcular_precio_venta)
        self.producto_ganancia.trace('w', self.calcular_precio_venta)
        
        # IMPORTANTE: Llamar a cambiar_tipo_calculo para establecer la vista inicial correcta
        self.cambiar_tipo_calculo()
        
        # FILA 5: TODOS LOS BOTONES EN UNA SOLA LÍNEA (versión simplificada)
        buttons_frame = tb.Frame(form_frame)
        buttons_frame.grid(row=4, column=0, columnspan=4, pady=(10, 5), sticky='ew')
        
        # Botones de acción principales
        tb.Button(
            buttons_frame, 
            text="➕ Crear", 
            command=self.crear_producto,
            bootstyle="success",
            width=12
        ).pack(side='left', padx=3)
        
        tb.Button(
            buttons_frame, 
            text="🔄 Actualizar", 
            command=self.actualizar_producto,
            bootstyle="warning",
            width=12
        ).pack(side='left', padx=3)
        
        tb.Button(
            buttons_frame, 
            text="🗑️ Limpiar", 
            command=self.limpiar_formulario_producto,
            bootstyle="secondary-outline",
            width=12
        ).pack(side='left', padx=3)
        
        # Espacio entre grupos
        tb.Label(buttons_frame, text="  |  ").pack(side='left', padx=5)
        
        # Botones de estado
        tb.Button(
            buttons_frame, 
            text="⛔ Inactivo", 
            command=self.desactivar_producto,
            bootstyle="danger-outline",
            width=12
        ).pack(side='left', padx=3)
        
        tb.Button(
            buttons_frame, 
            text="✅ Activar", 
            command=self.activar_producto,
            bootstyle="success-outline",
            width=12
        ).pack(side='left', padx=3)
        
        # Espacio entre grupos
        tb.Label(buttons_frame, text="  |  ").pack(side='left', padx=5)
        
        # Filtros
        tb.Label(buttons_frame, text="Mostrar:", font=('Segoe UI', 9, 'bold')).pack(side='left', padx=5)
        
        self.producto_filtro = tb.StringVar(value='activos')
        
        tb.Radiobutton(
            buttons_frame,
            text="Activos",
            variable=self.producto_filtro,
            value="activos",
            command=self.refresh_productos,
            bootstyle="success"
        ).pack(side='left', padx=2)
        
        tb.Radiobutton(
            buttons_frame,
            text="Inactivos",
            variable=self.producto_filtro,
            value="inactivos",
            command=self.refresh_productos,
            bootstyle="danger"
        ).pack(side='left', padx=2)
        
        tb.Radiobutton(
            buttons_frame,
            text="Todos",
            variable=self.producto_filtro,
            value="todos",
            command=self.refresh_productos,
            bootstyle="info"
        ).pack(side='left', padx=2)
        
        # Botón "Ver Detalles del Producto"
        tb.Button(
            buttons_frame,
            text="👁️ Ver Detalles",
            command=self.ver_detalles_producto,
            bootstyle="info-outline",
            width=15
        ).pack(side='right', padx=5)
        
        # Lista de productos con diseño mejorado
        list_frame = tb.Labelframe(
            self.productos_frame, 
            text="📋 Lista de Productos", 
            padding=15,
            bootstyle="info"
        )
        list_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Frame para búsqueda
        search_frame = tb.Frame(list_frame)
        search_frame.pack(fill='x', pady=(0, 10))
        
        tb.Label(search_frame, text="🔍 Buscar:", font=('Segoe UI', 10)).pack(side='left', padx=5)
        self.producto_search = tb.Entry(search_frame, width=30)
        self.producto_search.pack(side='left', padx=5)
        self.producto_search.bind('<KeyRelease>', lambda e: self.refresh_productos())
        
        # Treeview para productos con estilo mejorado
        tree_frame = tb.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Código', 'Nombre', 'Categoría', 'Marca', 'Color', 'Tamaño', 'Precio Compra', 'Ganancia %', 'Ganancia Q', 'Precio Venta', 'Stock', 'Estado')
        self.productos_tree = tb.Treeview(
            tree_frame, 
            columns=columns, 
            show='headings', 
            height=15
        )
        
        # Configurar columnas con mejor ancho
        column_widths = {'ID': 50, 'Código': 90, 'Nombre': 200, 'Categoría': 120, 'Marca': 80, 'Color': 80, 'Tamaño': 80, 'Precio Compra': 110, 'Ganancia %': 90, 'Ganancia Q': 100, 'Precio Venta': 110, 'Stock': 70, 'Estado': 80}
        for col in columns:
            self.productos_tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(self.productos_tree, c, False))
            self.productos_tree.column(col, width=column_widths[col], anchor='center' if col not in ['Nombre', 'Código', 'Categoría'] else 'w')
        
        # Scrollbars
        scrollbar_y = tb.Scrollbar(tree_frame, orient='vertical', command=self.productos_tree.yview, bootstyle="primary-round")
        scrollbar_x = tb.Scrollbar(tree_frame, orient='horizontal', command=self.productos_tree.xview, bootstyle="primary-round")
        self.productos_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.productos_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Bind para seleccionar producto para edición (doble clic)
        self.productos_tree.bind('<Double-1>', self.seleccionar_producto)
        
        # Bind para menú contextual con clic derecho
        self.productos_tree.bind('<Button-3>', self.mostrar_menu_contextual_producto)
        
        # Ocultar la columna "Ganancia %" (no eliminarla para no afectar índices)
        self.productos_tree.column('Ganancia %', width=0, stretch=False)
        
        # Agregar colores alternados a las filas
        self.productos_tree.tag_configure('evenrow', background='#f0f0f0')
        self.productos_tree.tag_configure('oddrow', background='#ffffff')
        self.productos_tree.tag_configure('lowstock', background='#ffcccc', foreground='#cc0000')
        self.productos_tree.tag_configure('inactivo', background='#d3d3d3', foreground='#666666')  # Gris para productos inactivos
    
    def create_compras_tab(self):
        """Crea la pestaña de gestión de compras"""
        from ttkbootstrap.dialogs import Querybox
        from ttkbootstrap import DateEntry
        
        self.compras_frame = tb.Frame(self.notebook, bootstyle="light")
        self.notebook.add(self.compras_frame, text="🛒 Compras")
        
        # Frame para formulario de compras con diseño mejorado
        form_frame = tb.Labelframe(
            self.compras_frame, 
            text="📥 Registrar Compra de Mercadería", 
            padding=20,
            bootstyle="success"
        )
        form_frame.pack(fill='x', padx=15, pady=15)
        
        # Grid para formulario - Fila 1: PROVEEDOR
        tb.Label(
            form_frame, 
            text="Proveedor: *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=0, column=0, sticky='w', padx=10, pady=8)
        
        # Frame para búsqueda de proveedor
        prov_search_frame = tb.Frame(form_frame)
        prov_search_frame.grid(row=0, column=1, padx=10, pady=8, sticky='ew')
        
        self.compra_proveedor_entry = tb.Entry(
            prov_search_frame, 
            textvariable=self.compra_proveedor_busqueda, 
            width=30,
            font=('Segoe UI', 10)
        )
        self.compra_proveedor_entry.pack(side='left', fill='x', expand=True)
        self.compra_proveedor_entry.bind('<KeyRelease>', self.autocompletar_proveedor_compra)
        
        tb.Button(
            prov_search_frame, 
            text="🔍", 
            command=self.buscar_proveedor_compra,
            bootstyle="info-outline",
            width=3
        ).pack(side='left', padx=5)
        
        self.compra_proveedor_label = tb.Label(
            prov_search_frame, 
            text="",
            font=('Segoe UI', 8),
            bootstyle="success"
        )
        self.compra_proveedor_label.pack(side='left', padx=5)
        
        # Fila 1: NO. DOCUMENTO
        tb.Label(
            form_frame, 
            text="No. Documento: *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=0, column=2, sticky='w', padx=10, pady=8)
        
        tb.Entry(
            form_frame, 
            textvariable=self.compra_no_documento, 
            width=20,
            font=('Segoe UI', 10)
        ).grid(row=0, column=3, padx=10, pady=8, sticky='ew')
        
        # Fila 2: PRODUCTO
        tb.Label(
            form_frame, 
            text="Producto: *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=1, column=0, sticky='w', padx=10, pady=8)
        
        # Frame para búsqueda de producto
        prod_search_frame = tb.Frame(form_frame)
        prod_search_frame.grid(row=1, column=1, padx=10, pady=8, sticky='ew')
        
        self.compra_producto_entry = tb.Entry(
            prod_search_frame, 
            textvariable=self.compra_producto_busqueda, 
            width=30,
            font=('Segoe UI', 10)
        )
        self.compra_producto_entry.pack(side='left', fill='x', expand=True)
        self.compra_producto_entry.bind('<KeyRelease>', self.autocompletar_producto_compra)
        
        tb.Button(
            prod_search_frame, 
            text="🔍", 
            command=self.buscar_producto_compra,
            bootstyle="info-outline",
            width=3
        ).pack(side='left', padx=5)
        
        self.compra_producto_label = tb.Label(
            prod_search_frame, 
            text="",
            font=('Segoe UI', 8),
            bootstyle="success"
        )
        self.compra_producto_label.pack(side='left', padx=5)
        
        # Fila 2: CANTIDAD
        tb.Label(
            form_frame, 
            text="Cantidad: *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=1, column=2, sticky='w', padx=10, pady=8)
        
        tb.Entry(
            form_frame, 
            textvariable=self.compra_cantidad, 
            width=20,
            font=('Segoe UI', 10)
        ).grid(row=1, column=3, padx=10, pady=8, sticky='ew')
        
        # Fila 3: PRECIO Y FECHA
        tb.Label(
            form_frame, 
            text="Precio Unitario (Q):",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=2, column=0, sticky='w', padx=10, pady=8)
        
        self.compra_precio_entry = tb.Entry(
            form_frame, 
            textvariable=self.compra_precio, 
            width=18,
            font=('Segoe UI', 10),
            state='readonly'
        )
        self.compra_precio_entry.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        
        tb.Label(
            form_frame, 
            text="Fecha: *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=2, column=2, sticky='w', padx=10, pady=8)
        
        self.compra_fecha_cal = DateEntry(
            form_frame,
            dateformat='%d/%m/%Y',
            width=18,
            bootstyle="success",
            firstweekday=0,  # Lunes como primer día
            startdate=None
        )
        self.compra_fecha_cal.grid(row=2, column=3, padx=10, pady=8, sticky='w')
        
        # Fila 3: PERECEDERO Y VENCIMIENTO
        self.compra_perecedero_check = tb.Checkbutton(
            form_frame,
            text="¿Es perecedero?",
            variable=self.compra_es_perecedero,
            command=self.toggle_vencimiento_compra,
            bootstyle="success-round-toggle"
        )
        self.compra_perecedero_check.grid(row=3, column=0, sticky='w', padx=10, pady=8)
        
        tb.Label(
            form_frame, 
            text="Fecha Vencimiento:",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=3, column=2, sticky='w', padx=10, pady=8)
        
        self.compra_vencimiento_cal = DateEntry(
            form_frame,
            dateformat='%d/%m/%Y',
            width=18,
            bootstyle="warning",
            firstweekday=0,
            startdate=None
        )
        self.compra_vencimiento_cal.grid(row=3, column=3, padx=10, pady=8, sticky='w')
        # Deshabilitar por defecto (entrada y botón)
        self.compra_vencimiento_cal.entry.configure(state='disabled')
        self.compra_vencimiento_cal.button.configure(state='disabled')
        
        # Fila 4: Etiqueta precio y Total
        tb.Label(
            form_frame, 
            text="(Se usa el precio del producto)",
            font=('Segoe UI', 8),
            bootstyle="secondary"
        ).grid(row=4, column=0, columnspan=2, sticky='w', padx=10, pady=0)
        
        self.compra_total_label = tb.Label(
            form_frame, 
            text="Total: Q 0.00",
            font=('Segoe UI', 14, 'bold'),
            bootstyle="success"
        )
        self.compra_total_label.grid(row=4, column=2, columnspan=2, sticky='w', padx=10, pady=8)
        
        # Configurar grid
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        
        # Bind para calcular total
        self.compra_cantidad.trace('w', self.calcular_total_compra)
        self.compra_precio.trace('w', self.calcular_total_compra)
        
        # Botón para registrar compra
        tb.Button(
            form_frame, 
            text="✅ Registrar Compra", 
            command=self.registrar_compra,
            bootstyle="success",
            width=25
        ).grid(row=5, column=0, columnspan=4, pady=15)
        
        # Lista de compras con diseño mejorado
        list_frame = tb.Labelframe(
            self.compras_frame, 
            text="📜 Historial de Compras", 
            padding=15,
            bootstyle="info"
        )
        list_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Frame para búsqueda
        search_frame = tb.Frame(list_frame)
        search_frame.pack(fill='x', pady=(0, 10))
        
        tb.Label(search_frame, text="🔍 Buscar:", font=('Segoe UI', 10)).pack(side='left', padx=5)
        self.compra_search = tb.Entry(search_frame, width=40)
        self.compra_search.pack(side='left', padx=5)
        self.compra_search.bind('<KeyRelease>', lambda e: self.refresh_compras())
        
        tb.Label(search_frame, text="Busca por: Proveedor, Producto, No. Doc o Fecha", 
                font=('Segoe UI', 8, 'italic'), bootstyle="secondary").pack(side='left', padx=10)
        
        # Treeview
        tree_frame = tb.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Proveedor', 'No. Doc', 'Producto', 'Cantidad', 'Precio Unit.', 'Total', 'Fecha', 'Vencimiento')
        self.compras_tree = tb.Treeview(
            tree_frame, 
            columns=columns, 
            show='headings', 
            height=15
        )
        
        column_widths = {'ID': 50, 'Proveedor': 150, 'No. Doc': 100, 'Producto': 150, 
                        'Cantidad': 80, 'Precio Unit.': 100, 'Total': 100, 'Fecha': 150, 'Vencimiento': 120}
        for col in columns:
            self.compras_tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(self.compras_tree, c, False))
            self.compras_tree.column(col, width=column_widths[col], anchor='center' if col not in ['Producto', 'Proveedor', 'No. Doc'] else 'w')
        
        scrollbar_y = tb.Scrollbar(tree_frame, orient='vertical', command=self.compras_tree.yview, bootstyle="success-round")
        scrollbar_x = tb.Scrollbar(tree_frame, orient='horizontal', command=self.compras_tree.xview, bootstyle="success-round")
        self.compras_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.compras_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Colores alternados
        self.compras_tree.tag_configure('evenrow', background='#f0f0f0')
        self.compras_tree.tag_configure('oddrow', background='#ffffff')
        
        # Colores para vencimientos
        self.compras_tree.tag_configure('vencido', background='#ff6b6b', foreground='white')  # Rojo fuerte
        self.compras_tree.tag_configure('critico', background='#ffa502', foreground='black')  # Naranja (1-7 días)
        self.compras_tree.tag_configure('advertencia', background='#ffd93d', foreground='black')  # Amarillo (8-30 días)
        
        # Colores hover (más oscuros) para efecto al pasar el mouse
        self.compras_tree.tag_configure('vencido_hover', background='#e85555', foreground='white')
        self.compras_tree.tag_configure('critico_hover', background='#e69500', foreground='black')
        self.compras_tree.tag_configure('advertencia_hover', background='#e8c130', foreground='black')
        
        # Agregar binding de click derecho para ver detalles del producto
        self.compras_tree.bind('<Button-3>', self.mostrar_menu_compras)
        
        # Botón para editar compra
        btn_frame = tb.Frame(list_frame)
        btn_frame.pack(fill='x', pady=10)
        
        tb.Button(
            btn_frame,
            text="✏️ Editar Estado Perecedero",
            command=self.editar_compra_perecedero,
            bootstyle="info",
            width=30
        ).pack(side='left', padx=5)
        
        tb.Label(
            btn_frame,
            text="💡 Doble clic en una compra para editarla",
            font=('Segoe UI', 9),
            bootstyle="secondary"
        ).pack(side='left', padx=10)
        
        # Bind para doble clic
        self.compras_tree.bind('<Double-1>', lambda e: self.editar_compra_perecedero())
        
        # Configurar navegación mejorada en calendarios después de un pequeño delay
        self.root.after(100, lambda: self.configurar_navegacion_calendario(self.compra_fecha_cal))
        self.root.after(100, lambda: self.configurar_navegacion_calendario(self.compra_vencimiento_cal))
    
    def create_ventas_tab(self):
        """Crea la pestaña de gestión de ventas"""
        from ttkbootstrap import DateEntry
        
        self.ventas_frame = tb.Frame(self.notebook, bootstyle="light")
        self.notebook.add(self.ventas_frame, text="💰 Ventas")
        
        # Frame principal dividido en dos secciones
        main_container = tb.Frame(self.ventas_frame)
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # ===== SECCIÓN SUPERIOR: FORMULARIO Y CARRITO =====
        top_section = tb.Frame(main_container)
        top_section.pack(fill='both', expand=False, pady=(0, 10))
        
        # Formulario izquierdo
        form_frame = tb.Labelframe(
            top_section,
            text="💵 Agregar Productos al Carrito",
            padding=15,
            bootstyle="warning"
        )
        form_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # CLIENTE (solo una vez para toda la venta)
        tb.Label(
            form_frame,
            text="Cliente: *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        cli_search_frame = tb.Frame(form_frame)
        cli_search_frame.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        
        self.venta_cliente_entry = tb.Entry(
            cli_search_frame,
            textvariable=self.venta_cliente_busqueda,
            width=25,
            font=('Segoe UI', 9)
        )
        self.venta_cliente_entry.pack(side='left', fill='x', expand=True)
        self.venta_cliente_entry.bind('<KeyRelease>', self.autocompletar_cliente_venta)
        
        tb.Button(
            cli_search_frame,
            text="🔍",
            command=self.buscar_cliente_venta,
            bootstyle="info-outline",
            width=3
        ).pack(side='left', padx=2)
        
        self.venta_cliente_label = tb.Label(
            cli_search_frame,
            text="",
            font=('Segoe UI', 8),
            bootstyle="success"
        )
        self.venta_cliente_label.pack(side='left', padx=5)
        
        # NIT/DPI o CF
        tb.Label(
            form_frame,
            text="NIT o DPI (CF): *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        
        self.venta_cliente_nit_entry = tb.Entry(
            form_frame,
            textvariable=self.venta_cliente_nit,
            width=25,
            font=('Segoe UI', 9)
        )
        self.venta_cliente_nit_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        
        # DIRECCIÓN
        tb.Label(
            form_frame,
            text="Dirección:",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=1, column=3, sticky='w', padx=5, pady=5)
        
        self.venta_cliente_direccion_entry = tb.Entry(
            form_frame,
            textvariable=self.venta_cliente_direccion,
            width=30,
            font=('Segoe UI', 9)
        )
        self.venta_cliente_direccion_entry.grid(row=1, column=4, padx=5, pady=5, sticky='w')
        
        # TELÉFONO
        tb.Label(
            form_frame,
            text="Teléfono:",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        
        self.venta_cliente_telefono_entry = tb.Entry(
            form_frame,
            textvariable=self.venta_cliente_telefono,
            width=25,
            font=('Segoe UI', 9)
        )
        self.venta_cliente_telefono_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        
        # FECHA
        tb.Label(
            form_frame,
            text="Fecha: *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=0, column=3, sticky='w', padx=5, pady=5)
        
        self.venta_fecha_cal = DateEntry(
            form_frame,
            dateformat='%d/%m/%Y',
            width=15,
            bootstyle="warning",
            firstweekday=0,
            startdate=None
        )
        self.venta_fecha_cal.grid(row=0, column=4, padx=5, pady=5, sticky='w')
        
        # Separador
        tb.Separator(form_frame, orient='horizontal').grid(row=3, column=0, columnspan=5, sticky='ew', pady=8)
        
        # PRODUCTO
        tb.Label(
            form_frame,
            text="Producto: *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=4, column=0, sticky='w', padx=5, pady=5)
        
        prod_search_frame = tb.Frame(form_frame)
        prod_search_frame.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        
        self.venta_producto_entry = tb.Entry(
            prod_search_frame,
            textvariable=self.venta_producto_busqueda,
            width=40,
            font=('Segoe UI', 9)
        )
        self.venta_producto_entry.pack(side='left', fill='x', expand=True)
        self.venta_producto_entry.bind('<KeyRelease>', self.autocompletar_producto_venta)
        
        tb.Button(
            prod_search_frame,
            text="🔍",
            command=self.buscar_producto_venta,
            bootstyle="info-outline",
            width=3
        ).pack(side='left', padx=2)
        
        self.venta_producto_label = tb.Label(
            prod_search_frame,
            text="",
            font=('Segoe UI', 8),
            bootstyle="success"
        )
        self.venta_producto_label.pack(side='left', padx=5)
        
        # FILA 5: CANTIDAD Y PRECIO
        tb.Label(
            form_frame,
            text="Cant.: *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=5, column=0, sticky='w', padx=5, pady=5)
        
        self.venta_cantidad_entry = tb.Entry(
            form_frame,
            textvariable=self.venta_cantidad,
            width=10,
            font=('Segoe UI', 9)
        )
        self.venta_cantidad_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        
        # PRECIO
        tb.Label(
            form_frame,
            text="Precio (Q): *",
            font=('Segoe UI', 10, 'bold')
        ).grid(row=5, column=2, sticky='w', padx=5, pady=5)
        
        self.venta_precio_entry = tb.Entry(
            form_frame,
            textvariable=self.venta_precio,
            width=12,
            font=('Segoe UI', 9),
            state='readonly'
        )
        self.venta_precio_entry.grid(row=5, column=3, padx=5, pady=5, sticky='w')
        
        # FILA 6: Stock disponible - MÁS VISIBLE Y CON COLORES
        stock_frame = tb.Frame(form_frame)
        stock_frame.grid(row=6, column=0, columnspan=4, sticky='ew', padx=5, pady=8)
        
        self.stock_label = tb.Label(
            stock_frame,
            text="📦 Stock Disponible: 0",
            font=('Segoe UI', 11, 'bold'),
            bootstyle="info"
        )
        self.stock_label.pack(anchor='w')
        
        # Espaciador invisible para bajar los botones
        spacer = tb.Label(form_frame, text="")
        spacer.grid(row=7, column=0, columnspan=4, pady=62)
        
        # Frame para botones (Agregar y Limpiar) - Alineado con botones del carrito
        botones_frame = tb.Frame(form_frame)
        botones_frame.grid(row=8, column=0, columnspan=4, pady=(10, 6))  # Cambiado a row=8
        
        # Botón Agregar al Carrito
        tb.Button(
            botones_frame,
            text="🛒 Agregar al Carrito",
            command=self.agregar_al_carrito,
            bootstyle="success",
            width=20
        ).pack(side='left', padx=5)
        
        # Botón Limpiar Formulario
        tb.Button(
            botones_frame,
            text="🧹 Limpiar",
            command=self.limpiar_formulario_carrito,
            bootstyle="secondary-outline",
            width=15
        ).pack(side='left', padx=5)
        
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        
        # ===== CARRITO (derecha) =====
        carrito_frame = tb.Labelframe(
            top_section,
            text="🛒 Carrito de Compras",
            padding=10,
            bootstyle="success"
        )
        carrito_frame.pack(side='left', fill='both', expand=True)
        
        # Tabla del carrito
        carrito_tree_frame = tb.Frame(carrito_frame)
        carrito_tree_frame.pack(fill='both', expand=True)
        
        carrito_cols = ('Producto', 'Cantidad', 'Precio', 'Subtotal')
        self.carrito_tree = tb.Treeview(
            carrito_tree_frame,
            columns=carrito_cols,
            show='headings',
            height=7
        )
        
        carrito_widths = {'Producto': 180, 'Cantidad': 80, 'Precio': 100, 'Subtotal': 100}
        for col in carrito_cols:
            self.carrito_tree.heading(col, text=col)
            self.carrito_tree.column(col, width=carrito_widths[col], 
                                    anchor='e' if col != 'Producto' else 'w')
        
        scrollbar_carrito = tb.Scrollbar(carrito_tree_frame, orient='vertical', 
                                        command=self.carrito_tree.yview)
        self.carrito_tree.configure(yscrollcommand=scrollbar_carrito.set)
        
        self.carrito_tree.pack(side='left', fill='both', expand=True)
        scrollbar_carrito.pack(side='left', fill='y')
        
        # Total del carrito
        total_frame = tb.Frame(carrito_frame)
        total_frame.pack(fill='x', pady=10)
        
        tb.Label(
            total_frame,
            text="TOTAL:",
            font=('Segoe UI', 14, 'bold')
        ).pack(side='left', padx=10)
        
        self.carrito_total_label = tb.Label(
            total_frame,
            text="Q 0.00",
            font=('Segoe UI', 16, 'bold'),
            bootstyle="success"
        )
        self.carrito_total_label.pack(side='left')
        
        # Botones del carrito
        btn_carrito_frame = tb.Frame(carrito_frame)
        btn_carrito_frame.pack(fill='x', pady=5)
        
        tb.Button(
            btn_carrito_frame,
            text="❌ Quitar Seleccionado",
            command=self.quitar_del_carrito,
            bootstyle="danger",
            width=25
        ).pack(side='left', padx=5)
        
        tb.Button(
            btn_carrito_frame,
            text="🗑️ Limpiar Carrito",
            command=self.limpiar_carrito,
            bootstyle="warning",
            width=20
        ).pack(side='left', padx=5)
        
        tb.Button(
            btn_carrito_frame,
            text="✅ Finalizar Venta",
            command=self.finalizar_venta,
            bootstyle="success",
            width=20
        ).pack(side='left', padx=5)
        
        # ===== SECCIÓN INFERIOR: HISTORIAL DE VENTAS =====
        list_frame = tb.Labelframe(
            main_container,
            text="📜 Historial de Ventas",
            padding=10,
            bootstyle="info"
        )
        list_frame.pack(fill='both', expand=True)
        
        # Frame para búsqueda
        search_frame = tb.Frame(list_frame)
        search_frame.pack(fill='x', pady=(0, 10))
        
        tb.Label(search_frame, text="🔍 Buscar:", font=('Segoe UI', 10)).pack(side='left', padx=5)
        self.venta_search = tb.Entry(search_frame, width=40)
        self.venta_search.pack(side='left', padx=5)
        self.venta_search.bind('<KeyRelease>', lambda e: self.refresh_ventas())
        
        tb.Label(search_frame, text="Busca por: Cliente, NIT/DPI, Ref. No. o Fecha",
                font=('Segoe UI', 8, 'italic'), bootstyle="secondary").pack(side='left', padx=10)
        
        # Treeview
        tree_frame = tb.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('Ref. No.', 'NIT/DPI', 'Cliente', 'Productos', 'Total', 'Fecha', 'Estado')
        self.ventas_tree = tb.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=12
        )
        
        column_widths = {'Ref. No.': 120, 'NIT/DPI': 110, 'Cliente': 180, 'Productos': 100, 
                        'Total': 120, 'Fecha': 150, 'Estado': 100}
        for col in columns:
            self.ventas_tree.heading(col, text=col, 
                                    command=lambda c=col: self.sort_treeview(self.ventas_tree, c, False))
            self.ventas_tree.column(col, width=column_widths[col], 
                                   anchor='center' if col not in ['Cliente', 'Ref. No.', 'NIT/DPI'] else 'w')
        
        scrollbar_y = tb.Scrollbar(tree_frame, orient='vertical', 
                                  command=self.ventas_tree.yview, bootstyle="warning-round")
        scrollbar_x = tb.Scrollbar(tree_frame, orient='horizontal', 
                                  command=self.ventas_tree.xview, bootstyle="warning-round")
        self.ventas_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.ventas_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Colores alternados
        self.ventas_tree.tag_configure('evenrow', background='#f0f0f0')
        self.ventas_tree.tag_configure('oddrow', background='#ffffff')
        
        # Binding para ver detalles
        self.ventas_tree.bind('<Double-Button-1>', self.ver_detalle_venta)
        self.ventas_tree.bind('<Button-3>', self.mostrar_menu_ventas)
        
        # Configurar navegación en calendario
        self.root.after(100, lambda: self.configurar_navegacion_calendario(self.venta_fecha_cal))
    
    def create_caja_tab(self):
        """Crea la pestaña de gestión de caja"""
        from ttkbootstrap.widgets import DateEntry
        
        self.caja_frame = tb.Frame(self.notebook, bootstyle="light")
        self.notebook.add(self.caja_frame, text="💰 Caja")
        
        # Panel superior: Saldo actual
        saldo_frame = tb.Labelframe(
            self.caja_frame,
            text="💵 Saldo Actual de Caja",
            padding=20,
            bootstyle="success"
        )
        saldo_frame.pack(fill='x', padx=15, pady=15)
        
        self.saldo_label = tb.Label(
            saldo_frame,
            text="Q 0.00",
            font=('Segoe UI', 36, 'bold'),
            bootstyle="success"
        )
        self.saldo_label.pack()
        
        # Resumen rápido
        resumen_quick_frame = tb.Frame(saldo_frame)
        resumen_quick_frame.pack(fill='x', pady=(10, 0))
        
        self.ingresos_label = tb.Label(
            resumen_quick_frame,
            text="↑ Ingresos: Q 0.00",
            font=('Segoe UI', 12),
            bootstyle="success"
        )
        self.ingresos_label.pack(side='left', padx=20)
        
        self.egresos_label = tb.Label(
            resumen_quick_frame,
            text="↓ Egresos: Q 0.00",
            font=('Segoe UI', 12),
            bootstyle="danger"
        )
        self.egresos_label.pack(side='left', padx=20)
        
        # Formulario de movimientos
        form_frame = tb.Labelframe(
            self.caja_frame,
            text="➕ Registrar Movimiento de Caja",
            padding=20,
            bootstyle="primary"
        )
        form_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Fila 1: Tipo y Categoría
        row1 = tb.Frame(form_frame)
        row1.pack(fill='x', pady=5)
        
        tb.Label(row1, text="Tipo:", font=('Segoe UI', 10, 'bold')).pack(side='left', padx=(0, 10))
        tipo_combo = tb.Combobox(
            row1,
            textvariable=self.caja_tipo,
            values=['INGRESO', 'EGRESO'],
            state='readonly',
            width=15,
            font=('Segoe UI', 10)
        )
        tipo_combo.pack(side='left', padx=(0, 30))
        tipo_combo.bind('<<ComboboxSelected>>', self.actualizar_categorias_caja)
        
        tb.Label(row1, text="Categoría:", font=('Segoe UI', 10, 'bold')).pack(side='left', padx=(0, 10))
        self.categoria_combo = tb.Combobox(
            row1,
            textvariable=self.caja_categoria,
            values=['GASTO_OPERATIVO', 'RETIRO_UTILIDAD', 'OTRO'],
            state='readonly',
            width=25,
            font=('Segoe UI', 10)
        )
        self.categoria_combo.pack(side='left')
        
        # Fila 2: Concepto
        row2 = tb.Frame(form_frame)
        row2.pack(fill='x', pady=5)
        
        tb.Label(row2, text="Concepto:", font=('Segoe UI', 10, 'bold')).pack(side='left', padx=(0, 10))
        tb.Entry(
            row2,
            textvariable=self.caja_concepto,
            width=60,
            font=('Segoe UI', 10)
        ).pack(side='left', fill='x', expand=True)
        
        # Fila 3: Monto, Fecha y Botones (todo en una fila para ahorrar espacio)
        row3 = tb.Frame(form_frame)
        row3.pack(fill='x', pady=5)
        
        tb.Label(row3, text="Monto (Q):", font=('Segoe UI', 10, 'bold')).pack(side='left', padx=(0, 10))
        tb.Entry(
            row3,
            textvariable=self.caja_monto,
            width=15,
            font=('Segoe UI', 10)
        ).pack(side='left', padx=(0, 20))
        
        tb.Label(row3, text="Fecha:", font=('Segoe UI', 10, 'bold')).pack(side='left', padx=(0, 10))
        self.caja_fecha_entry = DateEntry(
            row3,
            dateformat='%d/%m/%Y',
            firstweekday=0,
            width=15,
            startdate=None
        )
        self.caja_fecha_entry.pack(side='left', padx=(0, 20))
        
        # Botones en la misma fila
        tb.Button(
            row3,
            text="💰 Registrar",
            command=self.registrar_movimiento_caja,
            bootstyle="success",
            width=15
        ).pack(side='left', padx=5)
        
        tb.Button(
            row3,
            text="🧹 Limpiar",
            command=self.limpiar_form_caja,
            bootstyle="secondary-outline",
            width=12
        ).pack(side='left', padx=5)
        
        tb.Button(
            row3,
            text="💸 Retiro Utilidad",
            command=self.retiro_utilidades_rapido,
            bootstyle="warning-outline",
            width=16
        ).pack(side='left', padx=5)
        
        tb.Button(
            row3,
            text="💵 Aporte Capital",
            command=self.aporte_capital_rapido,
            bootstyle="info-outline",
            width=16
        ).pack(side='left', padx=5)
        
        # Lista de movimientos
        list_frame = tb.Labelframe(
            self.caja_frame,
            text="📋 Historial de Movimientos de Caja",
            padding=15,
            bootstyle="info"
        )
        list_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Barra de herramientas superior
        toolbar_frame = tb.Frame(list_frame)
        toolbar_frame.pack(fill='x', pady=(0, 10))
        
        # Búsqueda
        tb.Label(toolbar_frame, text="🔍 Buscar:", font=('Segoe UI', 10, 'bold')).pack(side='left', padx=5)
        self.caja_busqueda = tb.Entry(toolbar_frame, width=30, font=('Segoe UI', 10))
        self.caja_busqueda.pack(side='left', padx=5)
        self.caja_busqueda.bind('<KeyRelease>', lambda e: self.refresh_caja())
        
        # Filtros de fecha
        tb.Label(toolbar_frame, text="📅 Desde:", font=('Segoe UI', 10)).pack(side='left', padx=(20, 5))
        self.caja_fecha_inicio = DateEntry(
            toolbar_frame,
            dateformat='%d/%m/%Y',
            firstweekday=0,
            width=12,
            startdate=None
        )
        self.caja_fecha_inicio.pack(side='left', padx=5)
        
        tb.Label(toolbar_frame, text="Hasta:", font=('Segoe UI', 10)).pack(side='left', padx=5)
        self.caja_fecha_fin = DateEntry(
            toolbar_frame,
            dateformat='%d/%m/%Y',
            firstweekday=0,
            width=12,
            startdate=None
        )
        self.caja_fecha_fin.pack(side='left', padx=5)
        
        tb.Button(
            toolbar_frame,
            text="🔍 Filtrar",
            command=self.filtrar_movimientos_caja,
            bootstyle="info",
            width=12
        ).pack(side='left', padx=5)
        
        tb.Button(
            toolbar_frame,
            text="🔄 Todos",
            command=self.refresh_caja,
            bootstyle="secondary",
            width=12
        ).pack(side='left', padx=5)
        
        # Treeview para movimientos
        tree_frame = tb.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Fecha', 'Tipo', 'Categoría', 'Concepto', 'Monto', 'Saldo Anterior', 'Saldo Nuevo')
        self.caja_tree = tb.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=12
        )
        
        # Configurar columnas
        column_widths = {
            'ID': 50, 'Fecha': 100, 'Tipo': 80, 'Categoría': 140,
            'Concepto': 280, 'Monto': 120, 'Saldo Anterior': 120, 'Saldo Nuevo': 120
        }
        
        for col in columns:
            # Configurar encabezado con ordenamiento
            self.caja_tree.heading(col, text=col, 
                                  command=lambda c=col: self.sort_caja_tree(c, False))
            
            # Configurar alineación: derecha para montos, izquierda para concepto, centro para el resto
            if col in ['Monto', 'Saldo Anterior', 'Saldo Nuevo']:
                anchor = 'e'  # Derecha (east)
            elif col == 'Concepto':
                anchor = 'w'  # Izquierda (west)
            else:
                anchor = 'center'
            
            self.caja_tree.column(col, width=column_widths[col], anchor=anchor)
        
        # Scrollbars
        scrollbar_y = tb.Scrollbar(tree_frame, orient='vertical', command=self.caja_tree.yview)
        scrollbar_x = tb.Scrollbar(tree_frame, orient='horizontal', command=self.caja_tree.xview)
        self.caja_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.caja_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Colores alternados y por tipo
        self.caja_tree.tag_configure('ingreso', background='#d4edda', foreground='#155724')
        self.caja_tree.tag_configure('egreso', background='#f8d7da', foreground='#721c24')
        self.caja_tree.tag_configure('evenrow', background='#f8f9fa')
        self.caja_tree.tag_configure('oddrow', background='#ffffff')
        
        # Botones de acción debajo del tree
        actions_frame = tb.Frame(list_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        tb.Button(
            actions_frame,
            text="🗑️ Eliminar Movimiento Seleccionado",
            command=self.eliminar_movimiento_caja,
            bootstyle="danger-outline",
            width=30
        ).pack(side='left', padx=5)
        
        tb.Label(
            actions_frame,
            text="💡 Doble clic en un movimiento para ver detalles",
            font=('Segoe UI', 9, 'italic'),
            bootstyle="secondary"
        ).pack(side='left', padx=20)
        
        # Bind para doble clic (ver detalles)
        self.caja_tree.bind('<Double-1>', self.ver_detalle_movimiento)
        
        # Configurar navegación mejorada en calendarios
        self.root.after(100, lambda: self.configurar_navegacion_calendario(self.caja_fecha_entry))
        self.root.after(100, lambda: self.configurar_navegacion_calendario(self.caja_fecha_inicio))
        self.root.after(100, lambda: self.configurar_navegacion_calendario(self.caja_fecha_fin))
    
    def create_reportes_tab(self):
        """Crea la pestaña de reportes y resúmenes"""
        self.reportes_frame = tb.Frame(self.notebook, bootstyle="light")
        self.notebook.add(self.reportes_frame, text="📊 Reportes")
        
        # Contenedor principal con scroll
        main_container = tb.Frame(self.reportes_frame)
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Frame para tarjetas de resumen (estilo dashboard moderno)
        cards_frame = tb.Frame(main_container)
        cards_frame.pack(fill='x', pady=(0, 15))
        
        # Crear tarjetas de métricas
        # Fila 1
        row1 = tb.Frame(cards_frame)
        row1.pack(fill='x', pady=(0, 10))
        
        # Tarjeta: Total Compras
        card1 = tb.Labelframe(row1, text="🛒 Total Compras", bootstyle="info", padding=15)
        card1.pack(side='left', fill='both', expand=True, padx=5)
        
        self.total_compras_label = tb.Label(
            card1, 
            text="Q 0.00",
            font=('Segoe UI', 20, 'bold'),
            bootstyle="info"
        )
        self.total_compras_label.pack()
        
        tb.Label(card1, text="Inversión en mercadería", font=('Segoe UI', 9)).pack()
        
        # Tarjeta: Total Ventas
        card2 = tb.Labelframe(row1, text="💰 Total Ventas", bootstyle="success", padding=15)
        card2.pack(side='left', fill='both', expand=True, padx=5)
        
        self.total_ventas_label = tb.Label(
            card2, 
            text="Q 0.00",
            font=('Segoe UI', 20, 'bold'),
            bootstyle="success"
        )
        self.total_ventas_label.pack()
        
        tb.Label(card2, text="Ingresos generados", font=('Segoe UI', 9)).pack()
        
        # Tarjeta: Ganancia
        card3 = tb.Labelframe(row1, text="📈 Ganancia Bruta", bootstyle="warning", padding=15)
        card3.pack(side='left', fill='both', expand=True, padx=5)
        
        self.ganancia_label = tb.Label(
            card3, 
            text="Q 0.00",
            font=('Segoe UI', 20, 'bold'),
            bootstyle="warning"
        )
        self.ganancia_label.pack()
        
        tb.Label(card3, text="Beneficio obtenido", font=('Segoe UI', 9)).pack()
        
        # Fila 2
        row2 = tb.Frame(cards_frame)
        row2.pack(fill='x')
        
        # Tarjeta: Valor Inventario
        card4 = tb.Labelframe(row2, text="📦 Valor Inventario", bootstyle="primary", padding=15)
        card4.pack(side='left', fill='both', expand=True, padx=5)
        
        self.valor_inventario_label = tb.Label(
            card4, 
            text="Q 0.00",
            font=('Segoe UI', 20, 'bold'),
            bootstyle="primary"
        )
        self.valor_inventario_label.pack()
        
        tb.Label(card4, text="Valor actual del stock", font=('Segoe UI', 9)).pack()
        
        # Tarjeta: Saldo Banco
        card5 = tb.Labelframe(row2, text="🏦 Saldo en Banco", bootstyle="secondary", padding=15)
        card5.pack(side='left', fill='both', expand=True, padx=5)
        
        self.saldo_banco_label = tb.Label(
            card5, 
            text="Q 0.00",
            font=('Segoe UI', 20, 'bold'),
            bootstyle="secondary"
        )
        self.saldo_banco_label.pack()
        
        tb.Label(card5, text="Dinero de ventas", font=('Segoe UI', 9)).pack()
        
        # Tarjeta vacía para balance
        card6 = tb.Frame(row2)
        card6.pack(side='left', fill='both', expand=True, padx=5)
        
        # Frame para botones de exportación
        export_frame = tb.Labelframe(
            main_container, 
            text="📥 Exportar Reportes a Excel", 
            padding=15,
            bootstyle="success"
        )
        export_frame.pack(fill='x', pady=(0, 15))
        
        export_buttons = tb.Frame(export_frame)
        export_buttons.pack()
        
        tb.Button(
            export_buttons,
            text="📊 Exportar Resumen General",
            command=self.exportar_reporte_general,
            bootstyle="success-outline",
            width=28
        ).pack(side='left', padx=5, pady=5)
        
        tb.Button(
            export_buttons,
            text="🛒 Exportar Compras",
            command=self.exportar_reporte_compras,
            bootstyle="info-outline",
            width=28
        ).pack(side='left', padx=5, pady=5)
        
        tb.Button(
            export_buttons,
            text="💰 Exportar Ventas",
            command=self.exportar_reporte_ventas,
            bootstyle="warning-outline",
            width=28
        ).pack(side='left', padx=5, pady=5)
        
        # Segunda fila de botones
        export_buttons2 = tb.Frame(export_frame)
        export_buttons2.pack(pady=(5, 0))
        
        tb.Button(
            export_buttons2,
            text="📦 Exportar Productos Completo",
            command=self.exportar_productos_completo,
            bootstyle="primary-outline",
            width=35
        ).pack(side='left', padx=5, pady=5)
        
        tb.Button(
            export_buttons2,
            text="🏦 Exportar Movimientos Caja",
            command=self.exportar_reporte_caja,
            bootstyle="secondary-outline",
            width=28
        ).pack(side='left', padx=5, pady=5)
        
        # Frame para productos con stock bajo y alertas de vencimiento
        stock_frame = tb.Labelframe(
            main_container, 
            text="Alertas del Sistema", 
            padding=15,
            bootstyle="danger"
        )
        stock_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview mejorado
        tree_frame = tb.Frame(stock_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('Tipo Alerta', 'Código', 'Producto', 'Estado', 'Valor', 'Acción Recomendada')
        self.stock_tree = tb.Treeview(
            tree_frame, 
            columns=columns, 
            show='headings', 
            height=10
        )
        
        # Configurar estilo para filas más visibles
        style = tb.Style()
        style.configure('alert.Treeview', rowheight=30, font=('Segoe UI', 10))
        self.stock_tree.configure(style='alert.Treeview')
        
        column_widths = {
            'Tipo Alerta': 150, 
            'Código': 100,
            'Producto': 200, 
            'Estado': 150, 
            'Valor': 150,
            'Acción Recomendada': 250
        }
        for col in columns:
            self.stock_tree.heading(col, text=col, anchor='center', command=lambda c=col: self.sort_treeview(self.stock_tree, c, False))
            self.stock_tree.column(col, width=column_widths[col], 
                                  anchor='center' if col not in ['Producto', 'Acción Recomendada', 'Tipo Alerta', 'Código'] else 'w')
        
        # Configurar estilo de headers
        style.configure('alert.Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        
        scrollbar_y = tb.Scrollbar(tree_frame, orient='vertical', command=self.stock_tree.yview, bootstyle="danger-round")
        scrollbar_x = tb.Scrollbar(tree_frame, orient='horizontal', command=self.stock_tree.xview, bootstyle="danger-round")
        self.stock_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.stock_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Colores para diferentes alertas
        self.stock_tree.tag_configure('alert_stock', background='#ffcccc', foreground='#cc0000')
        self.stock_tree.tag_configure('alert_vencido', background='#ff6b6b', foreground='white')
        self.stock_tree.tag_configure('alert_critico', background='#ffa502', foreground='black')
        self.stock_tree.tag_configure('alert_advertencia', background='#ffd93d', foreground='black')
        
        # Colores hover (más oscuros) para efecto al pasar el mouse
        self.stock_tree.tag_configure('alert_stock_hover', background='#ffb3b3', foreground='#cc0000')
        self.stock_tree.tag_configure('alert_vencido_hover', background='#e85555', foreground='white')
        self.stock_tree.tag_configure('alert_critico_hover', background='#e69500', foreground='black')
        self.stock_tree.tag_configure('alert_advertencia_hover', background='#e8c130', foreground='black')
        
        # Agregar binding de click derecho para ver detalles del producto
        self.stock_tree.bind('<Button-3>', self.mostrar_menu_alertas)
    
    def create_configuracion_tab(self):
        """Crea la pestaña de configuración"""
        # Frame principal sin scroll general
        self.config_frame = tb.Frame(self.notebook, bootstyle="light")
        self.notebook.add(self.config_frame, text="⚙️ Configuración")
        
        # ==================== DISEÑO EN DOS COLUMNAS ====================
        
        # Frame contenedor para las dos columnas
        columns_container = tb.Frame(self.config_frame, bootstyle="light")
        columns_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # ========== COLUMNA IZQUIERDA ==========
        left_column = tb.Frame(columns_container, bootstyle="light")
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Frame para gestión de base de datos
        db_frame = tb.Labelframe(
            left_column, 
            text="💾 Gestión de Base de Datos", 
            padding=20,
            bootstyle="secondary"
        )
        db_frame.pack(fill='x', pady=(0, 15))
        
        tb.Label(
            db_frame, 
            text="Base de datos actual:",
            font=('Segoe UI', 10, 'bold')
        ).pack(anchor='w', pady=(0, 5))
        
        self.db_actual_label = tb.Label(
            db_frame, 
            text=self.controller.db.db_path,
            font=('Segoe UI', 9),
            bootstyle="info"
        )
        self.db_actual_label.pack(anchor='w', pady=(0, 15))
        
        buttons_db_frame = tb.Frame(db_frame)
        buttons_db_frame.pack(fill='x', pady=10)
        
        tb.Button(
            buttons_db_frame, 
            text="📂 Cargar BD", 
            command=self.cargar_base_datos,
            bootstyle="primary",
            width=18
        ).pack(side='left', padx=5)
        
        tb.Button(
            buttons_db_frame, 
            text="➕ Nueva BD", 
            command=self.nueva_base_datos,
            bootstyle="success",
            width=18
        ).pack(side='left', padx=5)
        
        tb.Button(
            buttons_db_frame, 
            text="📄 Exportar", 
            command=self.exportar_resumen,
            bootstyle="info",
            width=18
        ).pack(side='left', padx=5)
        
        # Frame para OneDrive
        onedrive_frame = tb.Labelframe(
            left_column, 
            text="☁️ Sincronización con OneDrive", 
            padding=20,
            bootstyle="secondary"
        )
        onedrive_frame.pack(fill='x', pady=(0, 15))
        
        # Información sobre OneDrive
        info_onedrive = tb.Label(
            onedrive_frame, 
            text="Sincroniza la BD entre múltiples PCs.\n⚠️ OneDrive debe estar sincronizado.",
            font=('Segoe UI', 9),
            bootstyle="info",
            wraplength=500
        )
        info_onedrive.pack(anchor='w', pady=(0, 10))
        
        # Detectar OneDrive
        onedrive_path = Settings.detect_onedrive_path()
        if onedrive_path:
            status_text = f"✅ OneDrive: {onedrive_path[:40]}..."
            status_style = "success"
        else:
            status_text = "❌ OneDrive no detectado"
            status_style = "danger"
        
        tb.Label(
            onedrive_frame, 
            text=status_text,
            font=('Segoe UI', 9, 'bold'),
            bootstyle=status_style
        ).pack(anchor='w', pady=(0, 10))
        
        # Botones de OneDrive
        buttons_onedrive = tb.Frame(onedrive_frame)
        buttons_onedrive.pack(fill='x', pady=10)
        
        tb.Button(
            buttons_onedrive, 
            text="☁️ Configurar OneDrive", 
            command=self.configurar_onedrive,
            bootstyle="primary",
            width=25
        ).pack(side='left', padx=5)
        
        tb.Button(
            buttons_onedrive, 
            text="📂 Ubicación Manual", 
            command=self.seleccionar_ubicacion_manual,
            bootstyle="info",
            width=25
        ).pack(side='left', padx=5)
        
        # Estado actual
        current_db = Settings.get_db_path()
        is_cloud = Settings.is_using_cloud_storage()
        
        if is_cloud:
            estado_text = f"🌐 Nube\n{current_db[:50]}..."
            estado_style = "success"
        else:
            estado_text = f"💻 Local\n{current_db[:50]}..."
            estado_style = "secondary"
        
        self.estado_cloud_label = tb.Label(
            onedrive_frame, 
            text=estado_text,
            font=('Segoe UI', 8),
            bootstyle=estado_style
        )
        self.estado_cloud_label.pack(anchor='w', pady=(10, 0))
        
        # Frame para temas
        theme_frame = tb.Labelframe(
            left_column, 
            text="🎨 Tema de la Aplicación", 
            padding=20,
            bootstyle="secondary"
        )
        theme_frame.pack(fill='x', pady=(0, 15))
        
        tb.Label(
            theme_frame, 
            text="Selecciona un tema:",
            font=('Segoe UI', 10, 'bold')
        ).pack(anchor='w', pady=(0, 10))
        
        # Temas disponibles
        themes_list = ['cosmo', 'flatly', 'minty', 'yeti']
        
        themes_buttons = tb.Frame(theme_frame)
        themes_buttons.pack(fill='x')
        
        # Crear una sola fila con los 4 temas
        row = tb.Frame(themes_buttons)
        row.pack(fill='x', pady=5)
        
        for theme in themes_list:
            tb.Button(
                row, 
                text=theme.capitalize(), 
                command=lambda t=theme: self.cambiar_tema(t),
                bootstyle="outline",
                width=13
            ).pack(side='left', padx=3)
        
        # ========== COLUMNA DERECHA ==========
        right_column = tb.Frame(columns_container, bootstyle="light")
        right_column.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        # Frame de información del sistema CON SCROLL
        info_frame = tb.Labelframe(
            right_column,
            text="ℹ️ Información del Sistema",
            padding=15,
            bootstyle="secondary"
        )
        info_frame.pack(fill='both', expand=True)
        
        # Canvas y scrollbar para el contenido
        canvas_info = tk.Canvas(info_frame, highlightthickness=0, bg='white')
        scrollbar_info = tb.Scrollbar(info_frame, orient="vertical", command=canvas_info.yview, bootstyle="secondary-round")
        info_content_frame = tb.Frame(canvas_info, bootstyle="light")
        
        info_content_frame.bind(
            "<Configure>",
            lambda e: canvas_info.configure(scrollregion=canvas_info.bbox("all"))
        )
        
        # Crear ventana con ancho dinámico
        window_id = canvas_info.create_window((0, 0), window=info_content_frame, anchor="nw")
        
        # Función para ajustar el ancho del frame interno al canvas
        def configure_canvas_width(event):
            canvas_width = event.width
            canvas_info.itemconfig(window_id, width=canvas_width)
        
        canvas_info.bind('<Configure>', configure_canvas_width)
        canvas_info.configure(yscrollcommand=scrollbar_info.set)
        
        # Habilitar scroll con la rueda del mouse
        def _on_mousewheel_info(event):
            canvas_info.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas_info.bind_all("<MouseWheel>", _on_mousewheel_info)
        canvas_info.pack(side="left", fill="both", expand=True)
        scrollbar_info.pack(side="right", fill="y")
        
        # Contenido de información completo (versión original restaurada)
        info_text = """🏢 Sistema de Control de Inventarios v2.0

✨ Características Principales:
  • Gestión completa de productos con cálculo automático de precios
  • Control de stock en tiempo real
  • Registro detallado de compras y ventas con fechas
  • Sistema de vencimientos para productos perecederos
  • Alertas visuales con código de colores
  • Reportes financieros visuales y detallados
  • Exportación de reportes a Excel con filtros de fecha
  • Base de datos SQLite local confiable
  • Sincronización con OneDrive (Nuevo!)
  • Interfaz moderna e intuitiva con ttkbootstrap
  • Temas personalizables con persistencia
  • Búsqueda y filtrado de productos
  • Validaciones inteligentes de datos
  • Gestión de caja con movimientos detallados

🎨 Código de Colores:

📦 INVENTARIO (Stock):
  🔴 Stock Bajo (≤5 unidades) - Color: Rosa claro (#ffcccc)
     Indica que necesita reabastecimiento

🛒 COMPRAS (Vencimientos):
  🔴 VENCIDO (fecha ya pasó) - Color: Rojo (#ff6b6b)
     Acción: Revisar y gestionar producto
  
  🟠 CRÍTICO (1-7 días) - Color: Naranja (#ffa502)
     Acción: Vender con urgencia o promocionar
  
  🟡 ADVERTENCIA (8-30 días) - Color: Amarillo (#ffd93d)
     Acción: Monitorear y planificar ventas
  
  ⚪ NORMAL (>30 días o no perecedero) - Sin color especial

💰 CAJA (Movimientos):
  🟢 INGRESO: Verde  |  🔴 EGRESO: Rojo  |  🔴 Saldo Negativo: Rojo

💰 Moneda: Quetzales (Q)
👨‍💻 Desarrollado por: Elizandro Urizar
🛠️ Tecnologías: Python, tkinter, ttkbootstrap, SQLite, pandas, openpyxl
📅 Versión: 2.0 - Octubre 2025
        """
        
        info_label = tb.Label(
            info_content_frame, 
            text=info_text, 
            justify='left',
            font=('Segoe UI', 9),
            wraplength=900
        )
        info_label.pack(anchor='w', padx=15, pady=15, fill='both', expand=True)
    
    def cambiar_tema(self, tema):
        """Cambia el tema de la aplicación"""
        try:
            self.root.style.theme_use(tema)
            
            # Guardar el tema seleccionado
            Settings.set_theme(tema)
            
            # Reaplicar estilos unificados para todas las tablas
            style = tb.Style()
            style.configure("Treeview", 
                           font=("Segoe UI", 10), 
                           rowheight=30)
            
            style.configure("Treeview.Heading", 
                           font=("Segoe UI", 9, "bold"), 
                           relief="raised", 
                           borderwidth=2,
                           padding=5)
            
            # Reaplicar efecto hover con el color del nuevo tema
            self.setup_treeview_selection_style()
            
            messagebox.showinfo("Tema Cambiado", f"Tema '{tema}' aplicado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cambiar el tema: {str(e)}")
    
    def sort_treeview(self, tree, col, reverse):
        """Ordena el treeview por columna (delegado a utilidades)"""
        sort_treeview(tree, col, reverse)
    
    # MÉTODOS DE CÁLCULO Y ACTUALIZACIÓN - DELEGADOS A productos_tab.py
    def cambiar_tipo_calculo(self):
        """Delegador: Cambia entre cálculo por porcentaje o precio directo"""
        if hasattr(self, 'productos_tab'):
            self.productos_tab.cambiar_tipo_calculo()
    
    def calcular_precio_desde_ganancia(self, event=None):
        """Delegador: Calcula el precio de venta desde el % de ganancia"""
        if hasattr(self, 'productos_tab'):
            self.productos_tab.calcular_precio_desde_ganancia(event)
    
    def calcular_ganancia_desde_precio(self, event=None):
        """Delegador: Calcula el % de ganancia desde el precio de venta"""
        if hasattr(self, 'productos_tab'):
            self.productos_tab.calcular_ganancia_desde_precio(event)
    
    def abrir_generador_sku(self):
        """Delegador: Abre ventana para generar código SKU automáticamente"""
        if hasattr(self, 'productos_tab'):
            self.productos_tab.abrir_generador_sku()
    
    def toggle_vencimiento_compra(self):
        """Habilita o deshabilita el campo de fecha de vencimiento"""
        if self.compra_es_perecedero.get():
            self.compra_vencimiento_cal.entry.configure(state='normal')
            self.compra_vencimiento_cal.button.configure(state='normal')
        else:
            self.compra_vencimiento_cal.entry.configure(state='disabled')
            self.compra_vencimiento_cal.button.configure(state='disabled')
            # Limpiar la fecha si se desmarca
            self.compra_fecha_vencimiento.set('')
    
    def calcular_total_compra(self, *args):
        """Calcula el total de la compra"""
        try:
            cantidad = self.compra_cantidad.get()
            precio = self.compra_precio.get()
            total = round(cantidad * precio, 2)
            self.compra_total_label.config(text=f"Total: Q {total:,.2f}")
        except:
            self.compra_total_label.config(text="Total: Q 0.00")
    
    def calcular_total_venta(self, *args):
        """Calcula el total de la venta"""
        try:
            cantidad = self.venta_cantidad.get()
            precio = self.venta_precio.get()
            total = round(cantidad * precio, 2)
            self.venta_total_label.config(text=f"Total: Q {total:,.2f}")
        except:
            self.venta_total_label.config(text="Total: Q 0.00")
    
    def actualizar_info_venta(self, event=None):
        """Actualiza la información cuando se selecciona un producto para venta (YA NO SE USA - búsqueda ahora)"""
        pass
    
    def actualizar_precio_compra(self, event=None):
        """Actualiza el precio de compra automáticamente (YA NO SE USA - búsqueda ahora)"""
        pass
    
    # MÉTODO abrir_generador_sku() MIGRADO A productos_tab.py
    
    # MÉTODOS DE ACCIÓN
    def crear_producto(self):
        """Crea un nuevo producto"""
        try:
            codigo = self.producto_codigo.get().strip()
            nombre = self.producto_nombre.get().strip()
            categoria = self.producto_categoria.get().strip()
            precio_compra = self.producto_precio_compra.get()
            ganancia = self.producto_ganancia.get()
            
            # Extraer TODOS los datos del SKU
            marca = self.sku_data.get('marca', '')
            color = self.sku_data.get('color', '')
            tamaño = self.sku_data.get('tamaño', '')
            dibujo = self.sku_data.get('dibujo', '')
            cod_color = self.sku_data.get('cod_color', '')
            
            exito, mensaje = self.controller.crear_producto(codigo, nombre, categoria, precio_compra, ganancia, marca, color, tamaño, dibujo, cod_color)
            
            if exito:
                # Extraer el ID del producto del mensaje
                import re
                match = re.search(r'ID:\s*(\d+)', mensaje)
                if match and codigo.endswith('-000'):
                    producto_id = int(match.group(1))
                    # Actualizar el código con el ID real
                    nuevo_codigo = codigo.replace('-000', f'-{producto_id:03d}')
                    # Actualizar el producto con el código correcto
                    self.controller.actualizar_producto(
                        producto_id, nuevo_codigo, nombre, categoria, 
                        precio_compra, ganancia, marca, color, tamaño, dibujo, cod_color
                    )
                    mensaje = f"Producto creado exitosamente\nCódigo: {nuevo_codigo}"
                
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario_producto_tab()
                self.refresh_productos()
                self.refresh_combos()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def actualizar_producto(self):
        """Actualiza un producto existente"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un producto para actualizar")
            return
        
        try:
            codigo = self.producto_codigo.get().strip()
            nombre = self.producto_nombre.get().strip()
            categoria = self.producto_categoria.get().strip()
            precio_compra = self.producto_precio_compra.get()
            ganancia = self.producto_ganancia.get()
            
            # Extraer TODOS los datos del SKU
            marca = self.sku_data.get('marca', '')
            color = self.sku_data.get('color', '')
            tamaño = self.sku_data.get('tamaño', '')
            dibujo = self.sku_data.get('dibujo', '')
            cod_color = self.sku_data.get('cod_color', '')
            
            exito, mensaje = self.controller.actualizar_producto(
                self.producto_seleccionado, codigo, nombre, categoria, precio_compra, ganancia, marca, color, tamaño, dibujo, cod_color
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario_producto_tab()
                self.refresh_productos()
                self.refresh_combos()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    # MÉTODOS DE AUTOCOMPLETADO
    def autocompletar_proveedor_compra(self, event):
        """Autocompletado tipo Google para proveedor en compras"""
        texto = self.compra_proveedor_busqueda.get()
        
        # Destruir listbox anterior si existe
        if hasattr(self, 'proveedor_listbox') and self.proveedor_listbox.winfo_exists():
            self.proveedor_listbox.destroy()
        
        if len(texto) < 2:
            return
        
        # Buscar proveedores que coincidan
        proveedores = self.controller.buscar_proveedor(texto)
        
        if not proveedores:
            return
        
        # Crear listbox flotante debajo del entry
        x = self.compra_proveedor_entry.winfo_rootx()
        y = self.compra_proveedor_entry.winfo_rooty() + self.compra_proveedor_entry.winfo_height()
        width = self.compra_proveedor_entry.winfo_width()
        
        self.proveedor_listbox = tk.Listbox(
            self.root,
            height=min(5, len(proveedores)),
            width=width // 8,
            font=('Segoe UI', 10)
        )
        self.proveedor_listbox.place(x=x - self.root.winfo_rootx(), 
                                     y=y - self.root.winfo_rooty())
        
        # Llenar con sugerencias
        for prov in proveedores[:10]:  # Máximo 10 sugerencias
            self.proveedor_listbox.insert('end', f"{prov['nombre']} - {prov['nit_dpi']}")
        
        # Eventos del listbox
        def seleccionar_proveedor(event=None):
            if self.proveedor_listbox.curselection():
                idx = self.proveedor_listbox.curselection()[0]
                seleccion = self.proveedor_listbox.get(idx)
                self.compra_proveedor_busqueda.set(seleccion)
                self.compra_proveedor_id = proveedores[idx]['id']
                self.compra_proveedor_label.config(text="✓ Seleccionado", bootstyle="success")
                self.proveedor_listbox.destroy()
        
        self.proveedor_listbox.bind('<<ListboxSelect>>', seleccionar_proveedor)
        self.proveedor_listbox.bind('<Return>', seleccionar_proveedor)
        self.proveedor_listbox.bind('<Escape>', lambda e: self.proveedor_listbox.destroy())
        
        # Permitir navegación con teclado
        if event.keysym == 'Down':
            self.proveedor_listbox.focus_set()
            self.proveedor_listbox.selection_set(0)
    
    def autocompletar_producto_compra(self, event):
        """Autocompletado tipo Google para producto en compras"""
        texto = self.compra_producto_busqueda.get()
        
        # Destruir listbox anterior si existe
        if hasattr(self, 'producto_compra_listbox') and self.producto_compra_listbox.winfo_exists():
            self.producto_compra_listbox.destroy()
        
        if len(texto) < 2:
            return
        
        # Buscar productos por código o nombre
        productos = self.controller.obtener_productos()
        productos_filtrados = [
            p for p in productos 
            if texto.lower() in p['nombre'].lower() or 
               (p.get('codigo') and texto.lower() in p['codigo'].lower())
        ]
        
        if not productos_filtrados:
            return
        
        # Crear listbox flotante
        x = self.compra_producto_entry.winfo_rootx()
        y = self.compra_producto_entry.winfo_rooty() + self.compra_producto_entry.winfo_height()
        width = self.compra_producto_entry.winfo_width()
        
        self.producto_compra_listbox = tk.Listbox(
            self.root,
            height=min(5, len(productos_filtrados)),
            width=width // 8,
            font=('Segoe UI', 10)
        )
        self.producto_compra_listbox.place(x=x - self.root.winfo_rootx(), 
                                           y=y - self.root.winfo_rooty())
        
        # Llenar con sugerencias
        for prod in productos_filtrados[:10]:
            codigo_txt = f"[{prod.get('codigo', 'S/C')}] " if prod.get('codigo') else ""
            self.producto_compra_listbox.insert('end', f"{codigo_txt}{prod['nombre']} - Q{prod['precio_compra']:.2f}")
        
        # Eventos del listbox
        def seleccionar_producto(event=None):
            if self.producto_compra_listbox.curselection():
                idx = self.producto_compra_listbox.curselection()[0]
                prod = productos_filtrados[idx]
                codigo_txt = f"[{prod.get('codigo', 'S/C')}] " if prod.get('codigo') else ""
                self.compra_producto_busqueda.set(f"{codigo_txt}{prod['nombre']}")
                self.compra_producto_id = prod['id']
                self.compra_precio.set(prod['precio_compra'])
                self.compra_producto_label.config(text=f"✓ Precio: Q{prod['precio_compra']:.2f}", bootstyle="success")
                self.producto_compra_listbox.destroy()
        
        self.producto_compra_listbox.bind('<<ListboxSelect>>', seleccionar_producto)
        self.producto_compra_listbox.bind('<Return>', seleccionar_producto)
        self.producto_compra_listbox.bind('<Escape>', lambda e: self.producto_compra_listbox.destroy())
        
        if event.keysym == 'Down':
            self.producto_compra_listbox.focus_set()
            self.producto_compra_listbox.selection_set(0)
    
    def autocompletar_cliente_venta(self, event):
        """Autocompletado tipo Google para cliente en ventas"""
        texto = self.venta_cliente_busqueda.get()
        
        # Destruir listbox anterior si existe
        if hasattr(self, 'cliente_venta_listbox_window') and self.cliente_venta_listbox_window.winfo_exists():
            self.cliente_venta_listbox_window.destroy()
        
        if len(texto) < 2:
            return
        
        # Buscar clientes que coincidan
        clientes = self.controller.buscar_cliente(texto)
        
        if not clientes:
            return
        
        # Forzar actualización del widget para obtener posición real
        self.venta_cliente_entry.update_idletasks()
        self.root.update_idletasks()
        
        # Obtener coordenadas absolutas en pantalla
        x = self.venta_cliente_entry.winfo_rootx()
        y = self.venta_cliente_entry.winfo_rooty()
        height = self.venta_cliente_entry.winfo_height()
        width = self.venta_cliente_entry.winfo_width()
        
        # Si el widget no está renderizado correctamente, usar valores por defecto
        if width <= 1 or height <= 1:
            # ⚙️ EDITABLE: Ancho del listbox (en pixels)
            width = 350
            # ⚙️ EDITABLE: Altura del Entry para calcular posición (en pixels)
            # Si el listbox aparece muy arriba, AUMENTA este valor (ej: 40, 45, 50)
            # Si aparece muy abajo, DISMINUYE este valor (ej: 30, 25, 20)
            height = 80
        
        # Crear ventana Toplevel independiente
        self.cliente_venta_listbox_window = tk.Toplevel(self.root)
        self.cliente_venta_listbox_window.wm_overrideredirect(True)  # Sin bordes
        self.cliente_venta_listbox_window.wm_attributes('-topmost', True)  # Siempre encima
        
        # Posicionar EXACTAMENTE DEBAJO del Entry
        listbox_height = min(150, len(clientes) * 30)  # Altura dinámica
        # ⚙️ EDITABLE: Ajuste de posición
        # VERTICAL (Y): Para bajar más → y+height+5, y+height+10, etc.
        #               Para subir → y+height-5, y+height-10, etc.
        # HORIZONTAL (X): Para mover a la DERECHA → x+5, x+10, x+15, etc.
        #                 Para mover a la IZQUIERDA → x-5, x-10, x-15, etc.
        self.cliente_venta_listbox_window.geometry(f"{width}x{listbox_height}+{x+119}+{y+height}")
        
        # Frame con borde para mejor apariencia
        frame = tb.Frame(self.cliente_venta_listbox_window, bootstyle="default")
        frame.pack(fill='both', expand=True)
        
        # Crear Listbox dentro del frame con mejor estilo
        self.cliente_venta_listbox = tk.Listbox(
            frame,
            height=min(5, len(clientes)),
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=0,
            bg='white',
            fg='black',
            selectbackground='#0078d4',
            selectforeground='white',
            activestyle='none',
            highlightthickness=1,
            highlightcolor='#0078d4',
            highlightbackground='#cccccc'
        )
        self.cliente_venta_listbox.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Llenar con sugerencias
        for cli in clientes[:10]:
            self.cliente_venta_listbox.insert('end', f"{cli['nombre']} - {cli['nit_dpi']}")
        
        # Eventos del listbox
        def seleccionar_cliente(event=None):
            if self.cliente_venta_listbox.curselection():
                idx = self.cliente_venta_listbox.curselection()[0]
                seleccion = self.cliente_venta_listbox.get(idx)
                self.venta_cliente_busqueda.set(clientes[idx]['nombre'])
                self.venta_cliente_nit.set(clientes[idx]['nit_dpi'])  # Actualizar campo NIT
                self.venta_cliente_id = clientes[idx]['id']
                self.venta_cliente_label.config(text=f"✓ {clientes[idx]['nombre']}", bootstyle="success")
                self.cliente_venta_listbox_window.destroy()
        
        def cerrar_listbox(event=None):
            if self.cliente_venta_listbox_window.winfo_exists():
                self.cliente_venta_listbox_window.destroy()
        
        self.cliente_venta_listbox.bind('<<ListboxSelect>>', seleccionar_cliente)
        self.cliente_venta_listbox.bind('<Return>', seleccionar_cliente)
        self.cliente_venta_listbox.bind('<Escape>', cerrar_listbox)
        
        # Cerrar si se hace clic fuera
        self.cliente_venta_listbox_window.bind('<FocusOut>', cerrar_listbox)
        
        # Permitir navegación con teclado
        if event.keysym == 'Down':
            self.cliente_venta_listbox.focus_set()
            self.cliente_venta_listbox.selection_set(0)
    
    def autocompletar_producto_venta(self, event):
        """Autocompletado tipo Google para producto en ventas"""
        texto = self.venta_producto_busqueda.get()
        
        # Destruir listbox anterior si existe
        if hasattr(self, 'producto_venta_listbox_window') and self.producto_venta_listbox_window.winfo_exists():
            self.producto_venta_listbox_window.destroy()
        
        if len(texto) < 2:
            return
        
        # Buscar productos por código o nombre
        productos = self.controller.obtener_productos()
        productos_filtrados = [
            p for p in productos 
            if texto.lower() in p['nombre'].lower() or 
               (p.get('codigo') and texto.lower() in p['codigo'].lower())
        ]
        
        if not productos_filtrados:
            return
        
        # Forzar actualización del widget para obtener posición real
        self.venta_producto_entry.update_idletasks()
        self.root.update_idletasks()
        
        # Obtener coordenadas absolutas en pantalla
        x = self.venta_producto_entry.winfo_rootx()
        y = self.venta_producto_entry.winfo_rooty()
        height = self.venta_producto_entry.winfo_height()
        width = self.venta_producto_entry.winfo_width()
        
        # Si el widget no está renderizado correctamente, usar valores por defecto
        if width <= 1 or height <= 1:
            # ⚙️ EDITABLE: Ancho del listbox (en pixels)
            width = 500
            # ⚙️ EDITABLE: Altura del Entry para calcular posición (en pixels)
            # Si el listbox aparece muy arriba, AUMENTA este valor (ej: 40, 45, 50)
            # Si aparece muy abajo, DISMINUYE este valor (ej: 30, 25, 20)
            height = 139
        
        # Crear ventana Toplevel independiente
        self.producto_venta_listbox_window = tk.Toplevel(self.root)
        self.producto_venta_listbox_window.wm_overrideredirect(True)  # Sin bordes
        self.producto_venta_listbox_window.wm_attributes('-topmost', True)  # Siempre encima
        
        # Posicionar EXACTAMENTE DEBAJO del Entry
        listbox_height = min(150, len(productos_filtrados) * 30)  # Altura dinámica
        # ⚙️ EDITABLE: Ajuste de posición
        # VERTICAL (Y): Para bajar más → y+height+5, y+height+10, etc.
        #               Para subir → y+height-5, y+height-10, etc.
        # HORIZONTAL (X): Para mover a la DERECHA → x+5, x+10, x+15, etc.
        #                 Para mover a la IZQUIERDA → x-5, x-10, x-15, etc.
        self.producto_venta_listbox_window.geometry(f"{width}x{listbox_height}+{x+119}+{y+height}")
        
        # Frame con borde para mejor apariencia
        frame = tb.Frame(self.producto_venta_listbox_window, bootstyle="default")
        frame.pack(fill='both', expand=True)
        
        # Crear Listbox dentro del frame con mejor estilo
        self.producto_venta_listbox = tk.Listbox(
            frame,
            height=min(5, len(productos_filtrados)),
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=0,
            bg='white',
            fg='black',
            selectbackground='#0078d4',
            selectforeground='white',
            activestyle='none',
            highlightthickness=1,
            highlightcolor='#0078d4',
            highlightbackground='#cccccc'
        )
        self.producto_venta_listbox.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Llenar con sugerencias
        for prod in productos_filtrados[:10]:
            codigo_txt = f"[{prod.get('codigo', 'S/C')}] " if prod.get('codigo') else ""
            self.producto_venta_listbox.insert('end', 
                f"{codigo_txt}{prod['nombre']} - Q{prod['precio_venta']:.2f} (Stock: {prod['stock_actual']})")
        
        # Eventos del listbox
        def seleccionar_producto(event=None):
            if self.producto_venta_listbox.curselection():
                idx = self.producto_venta_listbox.curselection()[0]
                prod = productos_filtrados[idx]
                codigo_txt = f"[{prod.get('codigo', 'S/C')}] " if prod.get('codigo') else ""
                self.venta_producto_busqueda.set(f"{codigo_txt}{prod['nombre']}")
                self.venta_producto_id = prod['id']
                self.venta_precio.set(prod['precio_venta'])
                self.venta_producto_label.config(
                    text=f"✓ Q{prod['precio_venta']:.2f}", 
                    bootstyle="success"
                )
                # Actualizar el stock visible con colores
                stock = prod['stock_actual']
                if stock > 10:
                    color = "success"
                    texto = f"📦 Stock Disponible: {stock} ✓"
                elif stock > 0:
                    color = "warning"
                    texto = f"⚠️ Stock Bajo: {stock}"
                else:
                    color = "danger"
                    texto = f"❌ SIN STOCK"
                
                self.stock_label.config(
                    text=texto,
                    bootstyle=color
                )
                self.producto_venta_listbox_window.destroy()
        
        def cerrar_listbox(event=None):
            if self.producto_venta_listbox_window.winfo_exists():
                self.producto_venta_listbox_window.destroy()
        
        self.producto_venta_listbox.bind('<<ListboxSelect>>', seleccionar_producto)
        self.producto_venta_listbox.bind('<Return>', seleccionar_producto)
        self.producto_venta_listbox.bind('<Escape>', cerrar_listbox)
        
        # Cerrar si se hace clic fuera
        self.producto_venta_listbox_window.bind('<FocusOut>', cerrar_listbox)
        
        # Permitir navegación con teclado
        if event.keysym == 'Down':
            self.producto_venta_listbox.focus_set()
            self.producto_venta_listbox.selection_set(0)
    
    def buscar_proveedor_compra(self):
        """Abre diálogo para buscar proveedor"""
        busqueda = self.pedir_texto("Buscar Proveedor", "Ingrese nombre o NIT del proveedor:")
        if busqueda:
            proveedores = self.controller.buscar_proveedor(busqueda)
            
            if not proveedores:
                messagebox.showinfo("Sin resultados", "No se encontraron proveedores con ese criterio")
                return
            
            # Crear ventana de selección
            dialog = tk.Toplevel(self.root)
            dialog.title("Seleccionar Proveedor")
            dialog.geometry("700x400")
            dialog.transient(self.root)
            
            # Ocultar ventana temporalmente para evitar parpadeo
            dialog.withdraw()
            
            dialog.grab_set()
            self.agregar_icono(dialog)
            
            self.centrar_ventana(dialog)
            
            # Mostrar ventana ya centrada
            dialog.deiconify()
            
            # Lista de proveedores
            frame = tb.Frame(dialog, padding=10)
            frame.pack(fill='both', expand=True)
            
            tb.Label(frame, text="Seleccione un proveedor:", font=('Segoe UI', 11, 'bold')).pack(pady=5)
            
            tree_frame = tb.Frame(frame)
            tree_frame.pack(fill='both', expand=True, pady=10)
            
            scrollbar = tb.Scrollbar(tree_frame)
            scrollbar.pack(side='right', fill='y')
            
            tree = tb.Treeview(
                tree_frame,
                columns=('ID', 'Nombre', 'NIT', 'Dirección', 'Teléfono'),
                show='headings',
                yscrollcommand=scrollbar.set
            )
            scrollbar.config(command=tree.yview)
            
            tree.heading('ID', text='ID')
            tree.heading('Nombre', text='Nombre')
            tree.heading('NIT', text='NIT/DPI')
            tree.heading('Dirección', text='Dirección')
            tree.heading('Teléfono', text='Teléfono')
            
            tree.column('ID', width=50, anchor='center')
            tree.column('Nombre', width=200, anchor='w')
            tree.column('NIT', width=100, anchor='center')
            tree.column('Dirección', width=200, anchor='w')
            tree.column('Teléfono', width=100, anchor='center')
            
            for prov in proveedores:
                tree.insert('', 'end', values=(
                    prov['id'],
                    prov['nombre'],
                    prov['nit_dpi'],
                    prov['direccion'],
                    prov['telefono']
                ))
            
            tree.pack(fill='both', expand=True)
            
            def seleccionar():
                seleccion = tree.selection()
                if seleccion:
                    item = tree.item(seleccion[0])
                    values = item['values']
                    self.compra_proveedor_id = values[0]
                    self.compra_proveedor_busqueda.set(values[1])
                    self.compra_proveedor_label.config(text=f"✓ {values[1]} ({values[2]})")
                    dialog.destroy()
                else:
                    messagebox.showwarning("Advertencia", "Seleccione un proveedor")
            
            tb.Button(frame, text="Seleccionar", command=seleccionar, bootstyle="success").pack(pady=5)
            
            tree.bind('<Double-1>', lambda e: seleccionar())
    
    def buscar_producto_compra(self):
        """Abre diálogo para buscar producto"""
        busqueda = self.pedir_texto("Buscar Producto", "Ingrese código o nombre del producto:")
        if busqueda:
            # Obtener solo productos activos
            productos = self.controller.obtener_productos_activos()
            # Filtrar por código o nombre
            productos_filtrados = [p for p in productos if 
                                  busqueda.lower() in p['nombre'].lower() or 
                                  busqueda.lower() in str(p.get('codigo', '')).lower()]
            
            if not productos_filtrados:
                messagebox.showinfo("Sin resultados", "No se encontraron productos con ese criterio")
                return
            
            # Crear ventana de selección
            dialog = tk.Toplevel(self.root)
            dialog.title("Seleccionar Producto")
            dialog.geometry("800x400")
            dialog.transient(self.root)
            dialog.grab_set()
            self.agregar_icono(dialog)
            self.centrar_ventana(dialog)
            
            # Lista de productos
            frame = tb.Frame(dialog, padding=10)
            frame.pack(fill='both', expand=True)
            
            tb.Label(frame, text="Seleccione un producto:", font=('Segoe UI', 11, 'bold')).pack(pady=5)
            
            tree_frame = tb.Frame(frame)
            tree_frame.pack(fill='both', expand=True, pady=10)
            
            scrollbar = tb.Scrollbar(tree_frame)
            scrollbar.pack(side='right', fill='y')
            
            tree = tb.Treeview(
                tree_frame,
                columns=('ID', 'Código', 'Nombre', 'Precio', 'Stock'),
                show='headings',
                yscrollcommand=scrollbar.set
            )
            scrollbar.config(command=tree.yview)
            
            tree.heading('ID', text='ID')
            tree.heading('Código', text='Código')
            tree.heading('Nombre', text='Nombre')
            tree.heading('Precio', text='Precio Compra')
            tree.heading('Stock', text='Stock')
            
            tree.column('ID', width=50, anchor='center')
            tree.column('Código', width=100, anchor='w')
            tree.column('Nombre', width=300, anchor='w')
            tree.column('Precio', width=120, anchor='center')
            tree.column('Stock', width=80, anchor='center')
            
            for prod in productos_filtrados:
                tree.insert('', 'end', values=(
                    prod['id'],
                    prod.get('codigo', ''),
                    prod['nombre'],
                    f"Q {prod['precio_compra']:,.2f}",
                    prod['stock_actual']
                ))
            
            tree.pack(fill='both', expand=True)
            
            def seleccionar():
                seleccion = tree.selection()
                if seleccion:
                    item = tree.item(seleccion[0])
                    values = item['values']
                    producto_id = values[0]
                    producto = self.controller.obtener_producto_por_id(producto_id)
                    
                    self.compra_producto_id = producto_id
                    self.compra_producto_busqueda.set(values[2])
                    self.compra_producto_label.config(text=f"✓ {values[2]}")
                    self.compra_precio.set(producto['precio_compra'])
                    dialog.destroy()
                else:
                    messagebox.showwarning("Advertencia", "Seleccione un producto")
            
            tb.Button(frame, text="Seleccionar", command=seleccionar, bootstyle="success").pack(pady=5)
            
            tree.bind('<Double-1>', lambda e: seleccionar())
    
    def buscar_cliente_venta(self):
        """Abre diálogo para buscar cliente"""
        busqueda = self.pedir_texto("Buscar Cliente", "Ingrese nombre o NIT del cliente:")
        if busqueda:
            clientes = self.controller.buscar_cliente(busqueda)
            
            if not clientes:
                messagebox.showinfo("Sin resultados", "No se encontraron clientes con ese criterio")
                return
            
            # Crear ventana de selección
            dialog = tk.Toplevel(self.root)
            dialog.title("Seleccionar Cliente")
            dialog.geometry("700x400")
            dialog.transient(self.root)
            dialog.grab_set()
            self.agregar_icono(dialog)
            self.centrar_ventana(dialog)
            
            # Lista de clientes
            frame = tb.Frame(dialog, padding=10)
            frame.pack(fill='both', expand=True)
            
            tb.Label(frame, text="Seleccione un cliente:", font=('Segoe UI', 11, 'bold')).pack(pady=5)
            
            tree_frame = tb.Frame(frame)
            tree_frame.pack(fill='both', expand=True, pady=10)
            
            scrollbar = tb.Scrollbar(tree_frame)
            scrollbar.pack(side='right', fill='y')
            
            tree = tb.Treeview(
                tree_frame,
                columns=('ID', 'Nombre', 'NIT', 'Dirección', 'Teléfono'),
                show='headings',
                yscrollcommand=scrollbar.set
            )
            scrollbar.config(command=tree.yview)
            
            tree.heading('ID', text='ID')
            tree.heading('Nombre', text='Nombre')
            tree.heading('NIT', text='NIT/DPI')
            tree.heading('Dirección', text='Dirección')
            tree.heading('Teléfono', text='Teléfono')
            
            tree.column('ID', width=50, anchor='center')
            tree.column('Nombre', width=200, anchor='w')
            tree.column('NIT', width=100, anchor='center')
            tree.column('Dirección', width=200, anchor='w')
            tree.column('Teléfono', width=100, anchor='center')
            
            for cli in clientes:
                tree.insert('', 'end', values=(
                    cli['id'],
                    cli['nombre'],
                    cli['nit_dpi'],
                    cli['direccion'],
                    cli['telefono']
                ))
            
            tree.pack(fill='both', expand=True)
            
            def seleccionar():
                seleccion = tree.selection()
                if seleccion:
                    item = tree.item(seleccion[0])
                    values = item['values']
                    self.venta_cliente_id = values[0]
                    self.venta_cliente_busqueda.set(values[1])
                    self.venta_cliente_nit.set(values[2])  # Actualizar campo NIT
                    self.venta_cliente_label.config(text=f"✓ {values[1]} ({values[2]})")
                    dialog.destroy()
                else:
                    messagebox.showwarning("Advertencia", "Seleccione un cliente")
            
            tb.Button(frame, text="Seleccionar", command=seleccionar, bootstyle="success").pack(pady=5)
            
            tree.bind('<Double-1>', lambda e: seleccionar())
    
    def guardar_cliente_rapido(self):
        """Diálogo rápido para agregar un nuevo cliente durante la venta"""
        # Obtener el texto actual del campo de búsqueda como nombre sugerido
        nombre_sugerido = self.venta_cliente_busqueda.get().strip()
        # Obtener el NIT/DPI si ya fue ingresado
        nit_sugerido = self.venta_cliente_nit.get().strip()
        # Obtener la dirección si ya fue ingresada
        direccion_sugerida = self.venta_cliente_direccion.get().strip()
        
        # Crear ventana de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("💾 Agregar Cliente Rápido")
        
        # Calcular posición centrada
        width = 450
        height = 320  # Aumentado para incluir dirección
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.agregar_icono(dialog)
        
        # Frame principal
        main_frame = tb.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        tb.Label(main_frame, text="Complete los datos del cliente:", 
                font=('Segoe UI', 11, 'bold')).pack(pady=(0, 15))
        
        # Campos del formulario
        form = tb.Frame(main_frame)
        form.pack(fill='x', pady=10)
        
        # Nombre
        tb.Label(form, text="Nombre: *", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky='w', pady=8, padx=5)
        nombre_var = tk.StringVar(value=nombre_sugerido)
        nombre_entry = tb.Entry(form, textvariable=nombre_var, width=30, font=('Segoe UI', 10))
        nombre_entry.grid(row=0, column=1, pady=8, padx=5, sticky='ew')
        nombre_entry.focus()
        
        # NIT/DPI o CF
        tb.Label(form, text="NIT o DPI (CF): *", font=('Segoe UI', 10, 'bold')).grid(
            row=1, column=0, sticky='w', pady=8, padx=5)
        nit_var = tk.StringVar(value=nit_sugerido)
        nit_entry = tb.Entry(form, textvariable=nit_var, width=30, font=('Segoe UI', 10))
        nit_entry.grid(row=1, column=1, pady=8, padx=5, sticky='ew')
        
        # Dirección (opcional)
        tb.Label(form, text="Dirección:", font=('Segoe UI', 10)).grid(
            row=2, column=0, sticky='w', pady=8, padx=5)
        direccion_var = tk.StringVar(value=direccion_sugerida)
        direccion_entry = tb.Entry(form, textvariable=direccion_var, width=30, font=('Segoe UI', 10))
        direccion_entry.grid(row=2, column=1, pady=8, padx=5, sticky='ew')
        
        # Teléfono (opcional)
        tb.Label(form, text="Teléfono:", font=('Segoe UI', 10)).grid(
            row=3, column=0, sticky='w', pady=8, padx=5)
        telefono_var = tk.StringVar()
        telefono_entry = tb.Entry(form, textvariable=telefono_var, width=30, font=('Segoe UI', 10))
        telefono_entry.grid(row=3, column=1, pady=8, padx=5, sticky='ew')
        
        form.columnconfigure(1, weight=1)
        
        # Función para guardar
        def guardar():
            nombre = nombre_var.get().strip()
            nit = nit_var.get().strip()
            telefono = telefono_var.get().strip()
            direccion = direccion_var.get().strip()
            
            # Validaciones
            if not nombre:
                messagebox.showwarning("Advertencia", "El nombre es obligatorio")
                nombre_entry.focus()
                return
            
            if not nit:
                messagebox.showwarning("Advertencia", "El NIT/DPI o CF es obligatorio")
                nit_entry.focus()
                return
            
            # Guardar cliente
            exito, mensaje = self.controller.crear_cliente(nombre, nit, direccion, telefono)
            
            if exito:
                # Buscar el cliente recién creado para obtener su ID
                clientes = self.controller.buscar_cliente(nombre)
                if clientes:
                    # Tomar el último cliente (el recién creado)
                    nuevo_cliente = clientes[-1]
                    self.venta_cliente_id = nuevo_cliente['id']
                    self.venta_cliente_busqueda.set(nuevo_cliente['nombre'])
                    self.venta_cliente_nit.set(nuevo_cliente['nit_dpi'])  # Actualizar campo NIT
                    self.venta_cliente_direccion.set(nuevo_cliente.get('direccion', ''))  # Actualizar campo Dirección
                    self.venta_cliente_label.config(text=f"✓ {nuevo_cliente['nombre']} ({nuevo_cliente['nit_dpi']})")
                
                messagebox.showinfo("Éxito", f"✅ {mensaje}\n\nCliente seleccionado para la venta.")
                self.refresh_clientes()  # Actualizar lista de clientes
                dialog.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        # Botones
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(fill='x', pady=(15, 0))
        
        tb.Button(btn_frame, text="Cancelar", command=dialog.destroy, 
                 bootstyle="secondary", width=15).pack(side='left', padx=5)
        tb.Button(btn_frame, text="💾 Guardar y Seleccionar", command=guardar, 
                 bootstyle="success", width=25).pack(side='right', padx=5)
        
        # Enter para guardar
        dialog.bind('<Return>', lambda e: guardar())
    
    def buscar_producto_venta(self):
        """Abre diálogo para buscar producto"""
        busqueda = self.pedir_texto("Buscar Producto", "Ingrese código o nombre del producto:")
        if busqueda:
            # Obtener solo productos activos
            productos = self.controller.obtener_productos_activos()
            # Filtrar por código o nombre
            productos_filtrados = [p for p in productos if 
                                  busqueda.lower() in p['nombre'].lower() or 
                                  busqueda.lower() in str(p.get('codigo', '')).lower()]
            
            if not productos_filtrados:
                messagebox.showinfo("Sin resultados", "No se encontraron productos con ese criterio")
                return
            
            # Crear ventana de selección
            dialog = tk.Toplevel(self.root)
            dialog.title("Seleccionar Producto")
            dialog.geometry("800x400")
            dialog.transient(self.root)
            dialog.grab_set()
            self.agregar_icono(dialog)
            self.centrar_ventana(dialog)
            
            # Lista de productos
            frame = tb.Frame(dialog, padding=10)
            frame.pack(fill='both', expand=True)
            
            tb.Label(frame, text="Seleccione un producto:", font=('Segoe UI', 11, 'bold')).pack(pady=5)
            
            tree_frame = tb.Frame(frame)
            tree_frame.pack(fill='both', expand=True, pady=10)
            
            scrollbar = tb.Scrollbar(tree_frame)
            scrollbar.pack(side='right', fill='y')
            
            tree = tb.Treeview(
                tree_frame,
                columns=('ID', 'Código', 'Nombre', 'Precio Venta', 'Stock'),
                show='headings',
                yscrollcommand=scrollbar.set
            )
            scrollbar.config(command=tree.yview)
            
            tree.heading('ID', text='ID')
            tree.heading('Código', text='Código')
            tree.heading('Nombre', text='Nombre')
            tree.heading('Precio Venta', text='Precio Venta')
            tree.heading('Stock', text='Stock')
            
            tree.column('ID', width=50, anchor='center')
            tree.column('Código', width=100, anchor='w')
            tree.column('Nombre', width=300, anchor='w')
            tree.column('Precio Venta', width=120, anchor='center')
            tree.column('Stock', width=80, anchor='center')
            
            for prod in productos_filtrados:
                tree.insert('', 'end', values=(
                    prod['id'],
                    prod.get('codigo', ''),
                    prod['nombre'],
                    f"Q {prod['precio_venta']:,.2f}",
                    prod['stock_actual']
                ))
            
            tree.pack(fill='both', expand=True)
            
            def seleccionar():
                seleccion = tree.selection()
                if seleccion:
                    item = tree.item(seleccion[0])
                    values = item['values']
                    producto_id = values[0]
                    producto = self.controller.obtener_producto_por_id(producto_id)
                    
                    self.venta_producto_id = producto_id
                    self.venta_producto_busqueda.set(values[2])
                    self.venta_producto_label.config(text=f"✓ {values[2]}")
                    self.venta_precio.set(producto['precio_venta'])
                    
                    # Actualizar stock con colores
                    stock = producto['stock_actual']
                    if stock > 10:
                        color = "success"
                        texto = f"📦 Stock Disponible: {stock:,} ✓"
                    elif stock > 0:
                        color = "warning"
                        texto = f"⚠️ Stock Bajo: {stock:,}"
                    else:
                        color = "danger"
                        texto = f"❌ SIN STOCK"
                    
                    self.stock_label.config(text=texto, bootstyle=color)
                    dialog.destroy()
                else:
                    messagebox.showwarning("Advertencia", "Seleccione un producto")
            
            tb.Button(frame, text="Seleccionar", command=seleccionar, bootstyle="success").pack(pady=5)
            
            tree.bind('<Double-1>', lambda e: seleccionar())
    
    def registrar_compra(self):
        """Registra una nueva compra"""
        from datetime import datetime
        try:
            # Validar proveedor
            if not self.compra_proveedor_id:
                messagebox.showwarning("Advertencia", "Busque y seleccione un proveedor")
                return
            
            # Validar número de documento
            no_documento = self.compra_no_documento.get().strip()
            if not no_documento:
                messagebox.showwarning("Advertencia", "Ingrese el número de documento")
                return
            
            # Validar producto
            if not self.compra_producto_id:
                messagebox.showwarning("Advertencia", "Busque y seleccione un producto")
                return
            
            cantidad = self.compra_cantidad.get()
            
            # Validar cantidad
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            # Obtener fecha del calendario y agregar hora actual
            fecha_cal = self.compra_fecha_cal.entry.get()  # formato dd/mm/yyyy
            hora_actual = datetime.now().strftime('%H:%M:%S')
            fecha_manual = f"{fecha_cal} {hora_actual}"
            
            # Obtener el producto para usar su precio de compra (precio fijo)
            producto = self.controller.obtener_producto_por_id(self.compra_producto_id)
            if not producto:
                messagebox.showerror("Error", "Producto no encontrado")
                return
            
            # Usar el precio de compra del producto (precio fijo)
            precio = producto['precio_compra']
            
            # Obtener datos de vencimiento
            es_perecedero = self.compra_es_perecedero.get()
            fecha_vencimiento = None
            
            if es_perecedero:
                fecha_vencimiento = self.compra_vencimiento_cal.entry.get()  # formato dd/mm/yyyy
                if not fecha_vencimiento:
                    messagebox.showwarning("Advertencia", "La fecha de vencimiento es obligatoria para productos perecederos")
                    return
            
            exito, mensaje = self.controller.registrar_compra(
                self.compra_producto_id, cantidad, precio, self.compra_proveedor_id, 
                no_documento, fecha_manual, es_perecedero, fecha_vencimiento
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                # Limpiar formulario
                self.compra_cantidad.set(0)
                self.compra_precio.set(0)
                self.compra_no_documento.set("")
                self.compra_producto_busqueda.set("")
                self.compra_proveedor_busqueda.set("")
                self.compra_producto_label.config(text="")
                self.compra_proveedor_label.config(text="")
                self.compra_es_perecedero.set(False)
                self.compra_fecha_vencimiento.set("")
                self.compra_vencimiento_cal.configure(state='disabled')
                self.compra_producto_id = None
                self.compra_proveedor_id = None
                self.refresh_compras()
                self.refresh_productos()
                self.refresh_caja()  # Actualizar tabla de caja
                self.actualizar_resumen()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def editar_compra_perecedero(self):
        """Edita el estado de perecedero de una compra"""
        from ttkbootstrap import DateEntry
        
        # Verificar que haya una compra seleccionada
        seleccion = self.compras_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una compra para editar")
            return
        
        # Obtener datos de la compra seleccionada
        item = self.compras_tree.item(seleccion[0])
        valores = item['values']
        compra_id = valores[0]
        producto_nombre = valores[3]
        vencimiento_actual = valores[8]
        
        # Determinar estado actual
        es_perecedero_actual = vencimiento_actual != "No perecedero"
        
        # Crear ventana de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Estado de Perecedero")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        
        # Ocultar ventana temporalmente para evitar parpadeo
        dialog.withdraw()
        
        dialog.grab_set()
        self.agregar_icono(dialog)
        
        # Frame principal
        main_frame = tb.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        tb.Label(
            main_frame,
            text=f"✏️ Editar: {producto_nombre}",
            font=('Segoe UI', 12, 'bold'),
            bootstyle="primary"
        ).pack(pady=(0, 20))
        
        # Variables
        es_perecedero_var = tk.BooleanVar(value=es_perecedero_actual)
        fecha_vencimiento_var = tk.StringVar()
        
        # Checkbox perecedero
        tb.Checkbutton(
            main_frame,
            text="¿Es producto perecedero?",
            variable=es_perecedero_var,
            bootstyle="success-round-toggle",
            command=lambda: toggle_venc()
        ).pack(anchor='w', pady=10)
        
        # Frame para fecha
        fecha_frame = tb.Frame(main_frame)
        fecha_frame.pack(fill='x', pady=10)
        
        tb.Label(
            fecha_frame,
            text="Fecha de Vencimiento:",
            font=('Segoe UI', 10, 'bold')
        ).pack(side='left', padx=(0, 10))
        
        venc_cal = DateEntry(
            fecha_frame,
            dateformat='%d/%m/%Y',
            width=18,
            bootstyle="warning",
            firstweekday=0,
            startdate=None
        )
        venc_cal.pack(side='left')
        
        # Si ya tiene fecha, ponerla
        if es_perecedero_actual and vencimiento_actual != "No perecedero":
            try:
                # Extraer solo la fecha si tiene formato "DD/MM/YYYY (Xd)"
                fecha_limpia = vencimiento_actual.split()[0] if ' ' in vencimiento_actual else vencimiento_actual
                if '⚠️' in fecha_limpia:
                    fecha_limpia = fecha_limpia.split()[0]
                venc_cal.entry.delete(0, 'end')
                venc_cal.entry.insert(0, fecha_limpia)
            except:
                pass
        
        def toggle_venc():
            if es_perecedero_var.get():
                venc_cal.entry.configure(state='normal')
                venc_cal.button.configure(state='normal')
            else:
                venc_cal.entry.configure(state='disabled')
                venc_cal.button.configure(state='disabled')
        
        # Estado inicial
        toggle_venc()
        
        # Botones
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        def guardar():
            es_perecedero = es_perecedero_var.get()
            fecha_venc = venc_cal.entry.get() if es_perecedero else None
            
            exito, mensaje = self.controller.actualizar_compra_perecedero(
                compra_id, es_perecedero, fecha_venc
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.refresh_compras()
                dialog.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        tb.Button(
            btn_frame,
            text="💾 Guardar",
            command=guardar,
            bootstyle="success",
            width=15
        ).pack(side='left', padx=5)
        
        tb.Button(
            btn_frame,
            text="❌ Cancelar",
            command=dialog.destroy,
            bootstyle="secondary",
            width=15
        ).pack(side='left', padx=5)
        
        # Configurar navegación mejorada en calendario
        dialog.after(100, lambda: self.configurar_navegacion_calendario(venc_cal))
        
        # Centrar y mostrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f'500x300+{x}+{y}')
        dialog.deiconify()
    
    # FUNCIONES DEL CARRITO DE VENTAS
    def agregar_al_carrito(self):
        """Agrega un producto al carrito de ventas"""
        try:
            # Validar producto
            if not self.venta_producto_id:
                messagebox.showwarning("Advertencia", "Busque y seleccione un producto")
                return
            
            cantidad = self.venta_cantidad.get()
            precio = self.venta_precio.get()
            
            # Validar cantidad
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            # Validar precio
            if precio <= 0:
                messagebox.showwarning("Advertencia", "El precio debe ser mayor a 0")
                return
            
            # Obtener información del producto
            producto = self.controller.obtener_producto_por_id(self.venta_producto_id)
            if not producto:
                messagebox.showerror("Error", "Producto no encontrado")
                return
            
            # Validar stock
            if producto['stock_actual'] < cantidad:
                messagebox.showwarning("Stock Insuficiente", 
                                      f"Stock disponible: {producto['stock_actual']}\n"
                                      f"Cantidad solicitada: {cantidad}")
                return
            
            # Verificar si el producto ya está en el carrito
            for item in self.carrito_ventas:
                if item['producto_id'] == self.venta_producto_id:
                    # Actualizar cantidad
                    nueva_cantidad = item['cantidad'] + cantidad
                    if producto['stock_actual'] < nueva_cantidad:
                        messagebox.showwarning("Stock Insuficiente",
                                              f"Ya tiene {item['cantidad']} en el carrito.\n"
                                              f"Stock disponible: {producto['stock_actual']}")
                        return
                    item['cantidad'] = nueva_cantidad
                    item['subtotal'] = item['cantidad'] * item['precio_unitario']
                    self.actualizar_tabla_carrito()
                    self.limpiar_formulario_producto()
                    messagebox.showinfo("Producto Actualizado", 
                                       f"Cantidad actualizada a {nueva_cantidad} unidades")
                    return
            
            # Agregar nuevo producto al carrito
            self.carrito_ventas.append({
                'producto_id': self.venta_producto_id,
                'nombre': producto['nombre'],
                'cantidad': cantidad,
                'precio_unitario': precio,
                'subtotal': cantidad * precio
            })
            
            self.actualizar_tabla_carrito()
            self.limpiar_formulario_producto()
            messagebox.showinfo("Producto Agregado", f"{producto['nombre']} agregado al carrito")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar al carrito: {str(e)}")
    
    def actualizar_tabla_carrito(self):
        """Actualiza la tabla visual del carrito"""
        # Limpiar tabla
        for item in self.carrito_tree.get_children():
            self.carrito_tree.delete(item)
        
        # Calcular total
        total = 0
        
        # Llenar tabla
        for item in self.carrito_ventas:
            self.carrito_tree.insert('', 'end', values=(
                item['nombre'][:30],  # Limitar nombre
                item['cantidad'],
                f"Q {item['precio_unitario']:,.2f}",
                f"Q {item['subtotal']:,.2f}"
            ))
            total += item['subtotal']
        
        # Actualizar etiqueta de total
        self.carrito_total_label.config(text=f"Q {total:,.2f}")
    
    def quitar_del_carrito(self):
        """Quita el producto seleccionado del carrito"""
        seleccion = self.carrito_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto del carrito")
            return
        
        # Obtener índice del item seleccionado
        item_index = self.carrito_tree.index(seleccion[0])
        
        # Eliminar del carrito
        producto_nombre = self.carrito_ventas[item_index]['nombre']
        del self.carrito_ventas[item_index]
        
        self.actualizar_tabla_carrito()
        messagebox.showinfo("Producto Eliminado", f"{producto_nombre} eliminado del carrito")
    
    def limpiar_carrito(self):
        """Limpia completamente el carrito"""
        if not self.carrito_ventas:
            messagebox.showinfo("Carrito Vacío", "El carrito ya está vacío")
            return
        
        respuesta = messagebox.askyesno("Confirmar", 
                                        "¿Está seguro de limpiar todo el carrito?")
        if respuesta:
            self.carrito_ventas = []
            self.actualizar_tabla_carrito()
            messagebox.showinfo("Carrito Limpiado", "Todos los productos fueron eliminados")
    
    def limpiar_formulario_producto(self):
        """Limpia solo los campos de producto, cantidad y precio (MANTIENE cliente y fecha)"""
        # Resetear ID de producto
        self.venta_producto_id = None
        
        # Limpiar labels
        self.venta_producto_label.config(text="")
        self.stock_label.config(text="📦 Stock Disponible: 0", bootstyle="info")
        
        # Limpiar campo PRODUCTO visualmente
        if hasattr(self, 'venta_producto_entry'):
            self.venta_producto_entry.delete(0, 'end')
        self.venta_producto_busqueda.set("")
        
        # Limpiar campo CANTIDAD
        if hasattr(self, 'venta_cantidad_entry'):
            self.venta_cantidad_entry.delete(0, 'end')
            self.venta_cantidad_entry.insert(0, "0")
        self.venta_cantidad.set(0)
        
        # Limpiar campo PRECIO (readonly - cambiar estado temporalmente)
        if hasattr(self, 'venta_precio_entry'):
            self.venta_precio_entry.config(state='normal')  # Habilitar temporalmente
            self.venta_precio_entry.delete(0, 'end')
            self.venta_precio_entry.insert(0, "0")
            self.venta_precio_entry.config(state='readonly')  # Volver a readonly
        self.venta_precio.set(0)
        
        # Destruir listbox de autocompletar si existe
        if hasattr(self, 'producto_venta_listbox'):
            try:
                if self.producto_venta_listbox.winfo_exists():
                    self.producto_venta_listbox.destroy()
            except:
                pass  # El listbox ya fue destruido
        
        # Enfocar el campo de producto para facilitar nueva búsqueda
        if hasattr(self, 'venta_producto_entry'):
            self.venta_producto_entry.focus_set()
    
    def limpiar_formulario_carrito(self):
        """Limpia TODO el formulario del carrito (incluyendo cliente y fecha)"""
        # Limpiar cliente
        self.venta_cliente_busqueda.set("")
        self.venta_cliente_label.config(text="")
        self.venta_cliente_id = None
        
        # Limpiar productos
        self.limpiar_formulario_producto()
        
        # Limpiar carrito
        self.carrito_ventas = []
        self.actualizar_tabla_carrito()
        
        # Restablecer fecha a hoy (usando DateEntry)
        from datetime import date
        self.venta_fecha_cal.entry.delete(0, 'end')
        self.venta_fecha_cal.entry.insert(0, date.today().strftime('%d/%m/%Y'))
        
        messagebox.showinfo("Formulario Limpiado", "Todos los campos han sido limpiados")
    
    def limpiar_todo_formulario_ventas(self):
        """Limpia TODO el formulario de ventas (cliente, productos, carrito) EXCEPTO fecha"""
        # Limpiar cliente
        self.venta_cliente_busqueda.set("")
        self.venta_cliente_nit.set("")  # Limpiar campo NIT
        self.venta_cliente_direccion.set("")  # Limpiar campo Dirección
        self.venta_cliente_telefono.set("")  # Limpiar campo Teléfono
        self.venta_cliente_label.config(text="")
        self.venta_cliente_id = None
        
        # Limpiar productos
        self.limpiar_formulario_producto()
        
        # Limpiar carrito
        self.carrito_ventas = []
        self.actualizar_tabla_carrito()
        
        # Mensaje de confirmación
        messagebox.showinfo("Formulario Limpiado", "Todos los campos han sido limpiados\n(Fecha conservada)")

    
    def finalizar_venta(self):
        """Finaliza la venta registrando todos los productos del carrito"""
        from datetime import datetime
        try:
            # Validar que haya datos de cliente
            nombre = self.venta_cliente_busqueda.get().strip()
            nit = self.venta_cliente_nit.get().strip()
            
            if not nombre or not nit:
                messagebox.showwarning("Advertencia", "Debe ingresar al menos el Nombre y NIT/DPI del cliente")
                return
            
            # Si no hay cliente_id, significa que se escribió manualmente (NO se guardó con 💾)
            # En este caso, la venta se registra SIN guardar el cliente en la base de datos
            # Solo se usa como información temporal de la venta
            
            if not self.venta_cliente_id:
                # Cliente nuevo - Se guardará automáticamente en la base de datos
                messagebox.showinfo(
                    "Cliente Nuevo",
                    f"Se guardará el cliente en la base de datos:\n\n"
                    f"Nombre: {nombre}\n"
                    f"NIT/DPI: {nit}\n\n"
                    f"El cliente estará disponible para futuras ventas."
                )
                # Guardar cliente automáticamente
                direccion = self.venta_cliente_direccion.get().strip()
                telefono = self.venta_cliente_telefono.get().strip()
                
                exito, mensaje = self.controller.crear_cliente(nombre, nit, direccion, telefono)
                if exito:
                    # Buscar el cliente recién creado
                    clientes = self.controller.buscar_cliente(nombre)
                    if clientes:
                        nuevo_cliente = clientes[-1]
                        self.venta_cliente_id = nuevo_cliente['id']
                else:
                    messagebox.showerror("Error", f"No se pudo registrar el cliente: {mensaje}")
                    return
            
            # Validar carrito
            if not self.carrito_ventas:
                messagebox.showwarning("Advertencia", "El carrito está vacío")
                return
            
            # Confirmar venta
            total = sum(item['subtotal'] for item in self.carrito_ventas)
            respuesta = messagebox.askyesno("Confirmar Venta",
                                           f"¿Confirmar venta?\n\n"
                                           f"Cliente: {self.venta_cliente_label.cget('text')}\n"
                                           f"Productos: {len(self.carrito_ventas)}\n"
                                           f"Total: Q {total:,.2f}")
            
            if not respuesta:
                return
            
            # Obtener fecha del calendario y agregar hora actual
            fecha_cal = self.venta_fecha_cal.entry.get()  # formato dd/mm/yyyy
            hora_actual = datetime.now().strftime('%H:%M:%S')
            fecha_manual = f"{fecha_cal} {hora_actual}"
            
            # Registrar venta con carrito
            exito, mensaje = self.controller.registrar_venta_con_carrito(
                self.venta_cliente_id,
                self.carrito_ventas,
                fecha_manual
            )
            
            if exito:
                messagebox.showinfo("Venta Exitosa", mensaje)
                
                # Limpiar carrito, formulario de productos Y datos del cliente
                self.carrito_ventas = []
                self.actualizar_tabla_carrito()
                self.limpiar_formulario_producto()
                
                # Limpiar datos del cliente para la siguiente venta
                self.venta_cliente_busqueda.set("")
                self.venta_cliente_nit.set("")
                self.venta_cliente_direccion.set("")
                self.venta_cliente_telefono.set("")
                self.venta_cliente_label.config(text="")
                self.venta_cliente_id = None
                
                # Actualizar tablas
                self.refresh_ventas()
                self.refresh_productos()
                self.refresh_caja()
                self.actualizar_resumen()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def registrar_venta(self):
        """Registra una nueva venta (MÉTODO LEGACY - ahora usa carrito)"""
        from datetime import datetime
        try:
            # Validar cliente
            if not self.venta_cliente_id:
                messagebox.showwarning("Advertencia", "Busque y seleccione un cliente")
                return
            
            # Validar producto
            if not self.venta_producto_id:
                messagebox.showwarning("Advertencia", "Busque y seleccione un producto")
                return
            
            cantidad = self.venta_cantidad.get()
            precio = self.venta_precio.get()
            
            # Validar cantidad
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            # Validar precio
            if precio <= 0:
                messagebox.showwarning("Advertencia", "El precio debe ser mayor a 0")
                return
            
            # Obtener fecha del calendario y agregar hora actual
            fecha_cal = self.venta_fecha_cal.entry.get()  # formato dd/mm/yyyy
            hora_actual = datetime.now().strftime('%H:%M:%S')
            fecha_manual = f"{fecha_cal} {hora_actual}"
            
            exito, mensaje = self.controller.registrar_venta(
                self.venta_producto_id, cantidad, precio, self.venta_cliente_id, fecha_manual
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                # Limpiar formulario
                self.venta_cantidad.set(0)
                self.venta_precio.set(0)
                self.venta_producto_busqueda.set("")
                self.venta_cliente_busqueda.set("")
                self.venta_producto_label.config(text="")
                self.venta_cliente_label.config(text="")
                self.stock_label.config(text="📦 Stock Disponible: 0")
                self.venta_producto_id = None
                self.venta_cliente_id = None
                self.refresh_ventas()
                self.refresh_productos()
                self.refresh_caja()  # Actualizar tabla de caja
                self.actualizar_resumen()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def ver_detalle_venta(self, event=None):
        """Muestra los detalles completos de una venta (todos los productos)"""
        seleccion = self.ventas_tree.selection()
        if not seleccion:
            return
        
        try:
            item = self.ventas_tree.item(seleccion[0])
            valores = item['values']
            venta_id = int(valores[0].split('REF')[1])  # Extraer ID de la referencia
            
            # Obtener venta completa con detalles
            venta = self.controller.obtener_venta_por_id(venta_id)
            
            if not venta:
                messagebox.showerror("Error", "No se pudo obtener la información de la venta")
                return
            
            # Crear ventana de detalles
            dialog = tk.Toplevel(self.root)
            dialog.title(f"📋 Detalle de Venta - {venta['referencia_no']}")
            
            # Calcular posición centrada ANTES de mostrar la ventana
            width = 700
            height = 600
            x = (dialog.winfo_screenwidth() // 2) - (width // 2)
            y = (dialog.winfo_screenheight() // 2) - (height // 2)
            dialog.geometry(f'{width}x{height}+{x}+{y}')
            
            dialog.transient(self.root)
            dialog.grab_set()
            self.agregar_icono(dialog)
            
            # Frame principal
            main_frame = tb.Frame(dialog, padding=20)
            main_frame.pack(fill='both', expand=True)
            
            # Información general
            info_frame = tb.Labelframe(main_frame, text="Información General", padding=15)
            info_frame.pack(fill='x', pady=(0, 10))
            
            tb.Label(info_frame, text=f"Referencia: {venta['referencia_no']}", 
                    font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=2)
            tb.Label(info_frame, text=f"Cliente: {venta['cliente_nombre']}", 
                    font=('Segoe UI', 10)).pack(anchor='w', pady=2)
            
            # Mostrar NIT/DPI si está disponible
            nit_dpi = venta.get('cliente_nit', '').strip()
            if nit_dpi:
                tb.Label(info_frame, text=f"NIT/DPI: {nit_dpi}", 
                        font=('Segoe UI', 10)).pack(anchor='w', pady=2)
            
            tb.Label(info_frame, text=f"Fecha: {venta['fecha']}", 
                    font=('Segoe UI', 10)).pack(anchor='w', pady=2)
            tb.Label(info_frame, text=f"Estado: {venta['estado']}", 
                    font=('Segoe UI', 10)).pack(anchor='w', pady=2)
            
            # Productos vendidos
            productos_frame = tb.Labelframe(main_frame, text="Productos Vendidos", padding=15)
            productos_frame.pack(fill='both', expand=True, pady=(0, 10))
            
            # Tabla de productos
            tree_frame = tb.Frame(productos_frame)
            tree_frame.pack(fill='both', expand=True)
            
            cols = ('Producto', 'Cantidad', 'Precio Unit.', 'Subtotal')
            detalle_tree = tb.Treeview(tree_frame, columns=cols, show='headings', height=6)
            
            for col in cols:
                detalle_tree.heading(col, text=col)
                detalle_tree.column(col, width=150 if col == 'Producto' else 120, 
                                   anchor='w' if col == 'Producto' else 'e')
            
            scrollbar = tb.Scrollbar(tree_frame, orient='vertical', command=detalle_tree.yview)
            detalle_tree.configure(yscrollcommand=scrollbar.set)
            
            detalle_tree.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Llenar tabla con productos
            for detalle in venta['detalles']:
                detalle_tree.insert('', 'end', values=(
                    detalle['producto_nombre'],
                    detalle['cantidad'],
                    f"Q {detalle['precio_unitario']:,.2f}",
                    f"Q {detalle['subtotal']:,.2f}"
                ))
            
            # Total
            total_frame = tb.Frame(main_frame)
            total_frame.pack(fill='x')
            
            tb.Label(total_frame, text="TOTAL:", 
                    font=('Segoe UI', 14, 'bold')).pack(side='left', padx=10)
            tb.Label(total_frame, text=f"Q {venta['total']:,.2f}", 
                    font=('Segoe UI', 16, 'bold'), bootstyle="success").pack(side='left')
            
            # Botón cerrar
            tb.Button(main_frame, text="Cerrar", command=dialog.destroy, 
                     bootstyle="secondary", width=15).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalles: {str(e)}")
    
    def mostrar_menu_contextual_producto(self, event):
        """Registra una nueva venta"""
        from datetime import datetime
        try:
            # Validar cliente
            if not self.venta_cliente_id:
                messagebox.showwarning("Advertencia", "Busque y seleccione un cliente")
                return
            
            # Validar producto
            if not self.venta_producto_id:
                messagebox.showwarning("Advertencia", "Busque y seleccione un producto")
                return
            
            cantidad = self.venta_cantidad.get()
            precio = self.venta_precio.get()
            
            # Validar cantidad
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            # Validar precio
            if precio <= 0:
                messagebox.showwarning("Advertencia", "El precio debe ser mayor a 0")
                return
            
            # Obtener fecha del calendario y agregar hora actual
            fecha_cal = self.venta_fecha_cal.entry.get()  # formato dd/mm/yyyy
            hora_actual = datetime.now().strftime('%H:%M:%S')
            fecha_manual = f"{fecha_cal} {hora_actual}"
            
            exito, mensaje = self.controller.registrar_venta(
                self.venta_producto_id, cantidad, precio, self.venta_cliente_id, fecha_manual
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                # Limpiar formulario
                self.venta_cantidad.set(0)
                self.venta_precio.set(0)
                self.venta_producto_busqueda.set("")
                self.venta_cliente_busqueda.set("")
                self.venta_producto_label.config(text="")
                self.venta_cliente_label.config(text="")
                self.stock_label.config(text="📦 Stock Disponible: 0")
                self.venta_producto_id = None
                self.venta_cliente_id = None
                self.refresh_ventas()
                self.refresh_productos()
                self.refresh_caja()  # Actualizar tabla de caja
                self.actualizar_resumen()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def mostrar_menu_contextual_producto(self, event):
        """Muestra un menú contextual al hacer clic derecho en un producto"""
        # Identificar en qué fila se hizo clic
        item = self.productos_tree.identify_row(event.y)
        
        if not item:
            return
        
        # Seleccionar la fila donde se hizo clic derecho
        self.productos_tree.selection_set(item)
        self.productos_tree.focus(item)
        
        # Obtener datos del producto
        valores = self.productos_tree.item(item)['values']
        producto_nombre = valores[2] if len(valores) > 2 else "Producto"
        
        # Crear menú contextual
        menu = tk.Menu(self.root, tearoff=0)
        
        menu.add_command(
            label=f"👁️  Ver Detalles de '{producto_nombre[:30]}...'",
            command=lambda: self.ver_detalles_desde_menu(item),
            font=('Segoe UI', 10, 'bold')
        )
        
        menu.add_separator()
        
        menu.add_command(
            label="✏️  Editar Producto",
            command=lambda: self.editar_desde_menu(item),
            font=('Segoe UI', 10)
        )
        
        menu.add_separator()
        
        menu.add_command(
            label="🔴  Desactivar Producto",
            command=self.desactivar_producto,
            font=('Segoe UI', 10)
        )
        
        menu.add_command(
            label="🟢  Activar Producto",
            command=self.activar_producto,
            font=('Segoe UI', 10)
        )
        
        # Mostrar el menú en la posición del cursor
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def ver_detalles_desde_menu(self, item):
        """Ver detalles desde el menú contextual"""
        try:
            # El item ya está seleccionado, obtener sus datos
            valores = self.productos_tree.item(item)['values']
            producto_id = valores[0]
            
            # Obtener el producto completo de la base de datos
            producto = self.controller.obtener_producto_por_id(producto_id)
            
            if producto:
                # Usar la función reutilizable
                self.mostrar_ventana_detalles(producto)
            else:
                messagebox.showerror("Error", "No se pudo obtener la información del producto")
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalles: {str(e)}")
    
    def editar_desde_menu(self, item):
        """Editar producto desde el menú contextual - Abre el generador SKU para edición"""
        try:
            # El item ya está seleccionado, obtener sus datos
            valores = self.productos_tree.item(item)['values']
            producto_id = int(valores[0])
            producto = self.controller.obtener_producto_por_id(producto_id)
            
            if producto:
                # Guardar ID para edición
                self.producto_seleccionado = producto_id
                
                # Cargar datos SKU en la estructura temporal
                self.sku_data = {
                    'nombre': producto.get('nombre', ''),
                    'categoria': producto.get('categoria', ''),
                    'marca': producto.get('marca', ''),
                    'color': producto.get('color', ''),
                    'tamaño': producto.get('tamaño', ''),
                    'dibujo': producto.get('dibujo', ''),
                    'cod_color': producto.get('cod_color', '')
                }
                
                # Cargar también al formulario principal (para mantener sincronizado)
                self.producto_codigo.set(producto.get('codigo', ''))
                self.producto_nombre.set(producto['nombre'])
                self.producto_categoria.set(producto.get('categoria', ''))
                self.producto_precio_compra.set(producto['precio_compra'])
                self.producto_ganancia.set(producto['porcentaje_ganancia'])
                self.producto_precio_venta_manual.set(producto['precio_venta'])
                self.producto_tipo_calculo.set("porcentaje")
                self.cambiar_tipo_calculo()
                
                # Abrir el generador SKU con los datos cargados
                self.abrir_generador_sku()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar producto para edición: {str(e)}")
    
    def on_producto_click(self, event):
        """Maneja el clic simple para seleccionar un producto visualmente"""
        # Este método asegura que el producto se marque como seleccionado
        # El Treeview ya maneja la selección automáticamente, este bind es solo para asegurar
        pass
    
    def seleccionar_producto(self, event):
        """Selecciona un producto de la lista para edición (doble clic) - Abre el generador SKU"""
        try:
            seleccion = self.productos_tree.selection()
            if seleccion:
                item = self.productos_tree.item(seleccion[0])
                producto_id = int(item['values'][0])
                producto = self.controller.obtener_producto_por_id(producto_id)
                
                if producto:
                    # Guardar ID para edición
                    self.producto_seleccionado = producto_id
                    
                    # Cargar datos SKU en la estructura temporal
                    self.sku_data = {
                        'nombre': producto.get('nombre', ''),
                        'categoria': producto.get('categoria', ''),
                        'marca': producto.get('marca', ''),
                        'color': producto.get('color', ''),
                        'tamaño': producto.get('tamaño', ''),
                        'dibujo': producto.get('dibujo', ''),
                        'cod_color': producto.get('cod_color', '')
                    }
                    
                    # Cargar también al formulario principal (para mantener sincronizado)
                    self.producto_codigo.set(producto.get('codigo', ''))
                    self.producto_nombre.set(producto['nombre'])
                    self.producto_categoria.set(producto.get('categoria', ''))
                    self.producto_precio_compra.set(producto['precio_compra'])
                    self.producto_ganancia.set(producto['porcentaje_ganancia'])
                    self.producto_precio_venta_manual.set(producto['precio_venta'])
                    self.producto_tipo_calculo.set("porcentaje")
                    self.cambiar_tipo_calculo()
                    
                    # Abrir el generador SKU con los datos cargados
                    self.abrir_generador_sku()
        except:
            pass
    
    def cargar_datos_sku_desde_bd(self, producto):
        """Carga los datos SKU desde la base de datos directamente"""
        try:
            # Cargar TODOS los datos reales desde la BD
            self.sku_data = {
                'nombre': producto.get('nombre', ''),
                'categoria': producto.get('categoria', ''),
                'marca': producto.get('marca', ''),
                'color': producto.get('color', ''),
                'tamaño': producto.get('tamaño', ''),
                'dibujo': producto.get('dibujo', ''),
                'cod_color': producto.get('cod_color', '')
            }
                        
        except Exception as e:
            # En caso de error, cargar valores vacíos
            self.sku_data = {
                'nombre': producto.get('nombre', ''),
                'categoria': producto.get('categoria', ''),
                'marca': '',
                'color': '',
                'tamaño': '',
                'dibujo': '',
                'cod_color': ''
            }
    
    def parsear_codigo_sku(self, codigo, nombre, categoria):
        """Parsea un código SKU y extrae los componentes para el generador (DEPRECADO - usar cargar_datos_sku_desde_bd)"""
        try:
            # Limpiar datos actuales
            self.sku_data = {
                'nombre': '',
                'categoria': '',
                'marca': '',
                'color': '',
                'tamaño': '',
                'dibujo': '',
                'cod_color': ''
            }
            
            # Si el código tiene el formato esperado (partes separadas por -)
            if '-' in codigo:
                partes = codigo.split('-')
                
                # Intentar reconstruir los datos desde el código
                # Formato: NOMBRE-CATEGORIA-MARCA-COLOR-CODCOLOR-TAMAÑO-DIBUJO-CORRELATIVO
                if len(partes) >= 2:
                    self.sku_data['nombre'] = nombre  # Usar el nombre completo del producto
                    self.sku_data['categoria'] = categoria  # Usar la categoría completa
                    
                    # Intentar identificar las partes restantes
                    idx = 2
                    if len(partes) > idx and len(partes[idx]) == 3:
                        self.sku_data['marca'] = partes[idx]
                        idx += 1
                    
                    if len(partes) > idx and len(partes[idx]) == 3:
                        self.sku_data['color'] = partes[idx]
                        idx += 1
                    
                    # Código de color (puede tener longitud variable)
                    if len(partes) > idx and len(partes[idx]) > 0 and partes[idx][0].isalpha():
                        self.sku_data['cod_color'] = partes[idx]
                        idx += 1
                    
                    if len(partes) > idx and len(partes[idx]) == 3:
                        self.sku_data['tamaño'] = partes[idx]
                        idx += 1
                    
                    if len(partes) > idx and len(partes[idx]) == 3:
                        self.sku_data['dibujo'] = partes[idx]
            else:
                # Si no tiene formato SKU, solo guardar nombre y categoría
                self.sku_data['nombre'] = nombre
                self.sku_data['categoria'] = categoria
                
        except Exception as e:
            # En caso de error, solo usar nombre y categoría
            self.sku_data = {
                'nombre': nombre,
                'categoria': categoria,
                'marca': '',
                'color': '',
                'tamaño': '',
                'dibujo': '',
                'cod_color': ''
            }
    
    def mostrar_menu_compras(self, event):
        """Muestra menú contextual en la tabla de compras"""
        # Identificar el item clickeado
        item = self.compras_tree.identify_row(event.y)
        if item:
            # Seleccionar el item
            self.compras_tree.selection_set(item)
            self.compras_tree.focus(item)
            
            # Obtener los valores de la fila
            valores = self.compras_tree.item(item)['values']
            if len(valores) >= 4:  # Asegurar que hay datos
                compra_id = valores[0]  # ID de la compra
                producto_nombre = valores[3]  # Nombre del producto
                
                # Buscar la compra completa para obtener el producto_id
                compras = self.controller.obtener_compras()
                compra = next((c for c in compras if c['id'] == compra_id), None)
                
                if compra and compra.get('producto_id'):
                    producto_id = compra['producto_id']
                    producto = self.controller.obtener_producto_por_id(producto_id)
                    
                    if producto:
                        # Crear menú contextual
                        menu = tk.Menu(self.root, tearoff=0)
                        menu.add_command(label="👁️ Ver Detalles del Producto", 
                                       command=lambda: self.mostrar_ventana_detalles(producto))
                        
                        # Mostrar menú en la posición del mouse
                        menu.post(event.x_root, event.y_root)
    
    def mostrar_menu_ventas(self, event):
        """Muestra menú contextual en la tabla de ventas"""
        # Identificar el item clickeado
        item = self.ventas_tree.identify_row(event.y)
        if item:
            # Seleccionar el item
            self.ventas_tree.selection_set(item)
            self.ventas_tree.focus(item)
            
            # Obtener el código del producto de la fila
            valores = self.ventas_tree.item(item)['values']
            if len(valores) >= 3:  # Asegurar que hay datos
                codigo_producto = valores[2]  # Columna 'Código' (producto_codigo)
                
                if codigo_producto:
                    # Buscar el producto por código
                    productos = self.controller.obtener_productos()
                    producto = next((p for p in productos if p['codigo'] == codigo_producto), None)
                    
                    if producto:
                        # Crear menú contextual
                        menu = tk.Menu(self.root, tearoff=0)
                        menu.add_command(label="👁️ Ver Detalles del Producto", 
                                       command=lambda: self.mostrar_ventana_detalles(producto))
                        
                        # Mostrar menú en la posición del mouse
                        menu.post(event.x_root, event.y_root)
    
    def mostrar_menu_alertas(self, event):
        """Muestra menú contextual en la tabla de alertas"""
        # Identificar el item clickeado
        item = self.stock_tree.identify_row(event.y)
        if item:
            # Seleccionar el item
            self.stock_tree.selection_set(item)
            self.stock_tree.focus(item)
            
            # Obtener el código del producto de la fila
            valores = self.stock_tree.item(item)['values']
            if len(valores) >= 2:  # Asegurar que hay datos
                codigo_producto = valores[1]  # Columna 'Código'
                
                # Buscar el producto por código
                productos = self.controller.obtener_productos()
                producto = next((p for p in productos if p['codigo'] == codigo_producto), None)
                
                if producto:
                    # Crear menú contextual
                    menu = tk.Menu(self.root, tearoff=0)
                    menu.add_command(label="👁️ Ver Detalles del Producto", 
                                   command=lambda: self.ver_detalles_producto_por_codigo(codigo_producto))
                    
                    # Mostrar menú en la posición del mouse
                    menu.post(event.x_root, event.y_root)
    
    def ver_detalles_producto_por_codigo(self, codigo):
        """Abre la ventana de detalles de un producto dado su código"""
        try:
            productos = self.controller.obtener_productos()
            producto = next((p for p in productos if p['codigo'] == codigo), None)
            
            if producto:
                self.mostrar_ventana_detalles(producto)
            else:
                messagebox.showwarning("Advertencia", f"No se encontró el producto con código: {codigo}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar producto: {str(e)}")
    
    def mostrar_ventana_detalles(self, producto):
        """Muestra la ventana de detalles de un producto (reutilizable)"""
        if not producto:
            messagebox.showerror("Error", "No se pudo obtener la información del producto")
            return
        
        # Crear ventana modal (oculta primero para evitar parpadeo)
        detalle_window = tk.Toplevel(self.root)
        detalle_window.withdraw()  # Ocultar temporalmente
        detalle_window.title(f"📋 Detalles del Producto - {producto['nombre']}")
        detalle_window.geometry("550x650")
        detalle_window.resizable(False, False)
        detalle_window.transient(self.root)
        detalle_window.grab_set()
        
        # Agregar icono
        try:
            icon_path = resource_path("inventario.ico")
            if os.path.exists(icon_path):
                detalle_window.iconbitmap(icon_path)
        except:
            pass
        
        # Frame principal con scroll
        main_frame = ttk.Frame(detalle_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y Scrollbar
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=500)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Ajustar ancho del canvas cuando cambie el tamaño
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Habilitar scroll con mousewheel en toda la ventana
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_mousewheel(event=None):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def unbind_mousewheel(event=None):
            canvas.unbind_all("<MouseWheel>")
        
        # Bind cuando el mouse entra/sale de la ventana
        detalle_window.bind('<Enter>', bind_mousewheel)
        detalle_window.bind('<Leave>', unbind_mousewheel)
        
        # === SECCIÓN 1: INFORMACIÓN BÁSICA ===
        frame_basico = ttk.LabelFrame(scrollable_frame, text="📌 Información Básica", padding="15")
        frame_basico.pack(fill=tk.X, padx=10, pady=10)
        
        info_basica = [
            ("🆔 ID:", str(producto['id'])),
            ("🏷️ Código SKU:", producto.get('codigo', 'N/A')),
            ("📦 Nombre:", producto['nombre']),
            ("📂 Categoría:", producto.get('categoria', 'N/A')),
            ("🔘 Estado:", "🟢 Activo" if producto.get('activo', 1) == 1 else "🔴 Inactivo")
        ]
        
        for i, (label, valor) in enumerate(info_basica):
            ttk.Label(frame_basico, text=label, font=('Segoe UI', 10, 'bold')).grid(row=i, column=0, sticky="w", pady=5)
            ttk.Label(frame_basico, text=valor, font=('Segoe UI', 10)).grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        # === SECCIÓN 2: DATOS SKU ===
        frame_sku = ttk.LabelFrame(scrollable_frame, text="🏭 Datos del SKU", padding="15")
        frame_sku.pack(fill=tk.X, padx=10, pady=10)
        
        datos_sku = [
            ("🏢 Marca:", producto.get('marca', 'N/A')),
            ("🎨 Color:", producto.get('color', 'N/A')),
            ("📏 Tamaño:", producto.get('tamaño', 'N/A')),
            ("🖼️ Dibujo:", producto.get('dibujo', 'N/A')),
            ("🔢 Código Color:", producto.get('cod_color', 'N/A'))
        ]
        
        for i, (label, valor) in enumerate(datos_sku):
            ttk.Label(frame_sku, text=label, font=('Segoe UI', 10, 'bold')).grid(row=i, column=0, sticky="w", pady=5)
            ttk.Label(frame_sku, text=valor, font=('Segoe UI', 10)).grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        # === SECCIÓN 3: INFORMACIÓN FINANCIERA ===
        frame_financiero = ttk.LabelFrame(scrollable_frame, text="💰 Información Financiera", padding="15")
        frame_financiero.pack(fill=tk.X, padx=10, pady=10)
        
        precio_compra = float(producto['precio_compra'])
        precio_venta = float(producto['precio_venta'])
        ganancia_unitaria = precio_venta - precio_compra
        porcentaje_ganancia = float(producto['porcentaje_ganancia'])
        
        info_financiera = [
            ("💵 Precio de Compra:", f"Q {precio_compra:,.2f}"),
            ("💲 Precio de Venta:", f"Q {precio_venta:,.2f}"),
            ("📈 Porcentaje de Ganancia:", f"{porcentaje_ganancia:.2f}%"),
            ("💎 Ganancia Unitaria:", f"Q {ganancia_unitaria:,.2f}")
        ]
        
        for i, (label, valor) in enumerate(info_financiera):
            ttk.Label(frame_financiero, text=label, font=('Segoe UI', 10, 'bold')).grid(row=i, column=0, sticky="w", pady=5)
            valor_label = ttk.Label(frame_financiero, text=valor, font=('Segoe UI', 10))
            valor_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            if "Ganancia" in label:
                valor_label.config(foreground="green")
        
        # === SECCIÓN 4: INVENTARIO ===
        frame_inventario = ttk.LabelFrame(scrollable_frame, text="📊 Información de Inventario", padding="15")
        frame_inventario.pack(fill=tk.X, padx=10, pady=10)
        
        stock_actual = producto.get('stock_actual', 0)
        valor_inventario = stock_actual * precio_compra
        valor_venta_total = stock_actual * precio_venta
        
        info_inventario = [
            ("📦 Stock Actual:", f"{stock_actual} unidades"),
            ("💰 Valor en Inventario:", f"Q {valor_inventario:,.2f}"),
            ("💵 Valor de Venta Total:", f"Q {valor_venta_total:,.2f}")
        ]
        
        for i, (label, valor) in enumerate(info_inventario):
            ttk.Label(frame_inventario, text=label, font=('Segoe UI', 10, 'bold')).grid(row=i, column=0, sticky="w", pady=5)
            ttk.Label(frame_inventario, text=valor, font=('Segoe UI', 10)).grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón de cerrar
        btn_frame = ttk.Frame(detalle_window)
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        ttk.Button(
            btn_frame,
            text="❌ Cerrar",
            command=lambda: [unbind_mousewheel(), detalle_window.destroy()],
            width=15
        ).pack()
        
        # Centrar ventana
        self.centrar_ventana(detalle_window)
        
        # Mostrar ventana centrada
        detalle_window.deiconify()
    
    def limpiar_formulario_producto_tab(self):
        """Limpia el formulario de productos (TAB PRODUCTOS)"""
        self.producto_codigo.set("")
        self.producto_nombre.set("")
        self.producto_categoria.set("")
        self.producto_precio_compra.set(0)
        self.producto_ganancia.set(0)
        self.producto_precio_venta_manual.set(0)
        self.producto_seleccionado = None
        
        # Limpiar datos guardados del SKU
        self.sku_data = {
            'nombre': '',
            'categoria': '',
            'marca': '',
            'color': '',
            'tamaño': '',
            'dibujo': '',
            'cod_color': ''
        }
        
        # IMPORTANTE: Establecer el tipo de cálculo ANTES de llamar a cambiar_tipo_calculo
        self.producto_tipo_calculo.set("precio")  # Mantener 'precio' por defecto
        
        # Ahora sí, actualizar la vista
        self.cambiar_tipo_calculo()  # Resetear la vista
        
        # Actualizar etiquetas
        self.precio_venta_label.config(text="Precio de Venta: Q 0.00")
        self.monto_ganancia_label.config(text="Ganancia: Q 0.00")
    
    
    def ver_detalles_producto(self):
        """Muestra una ventana con todos los detalles del producto seleccionado incluyendo datos SKU"""
        # Obtener selección
        selection = self.productos_tree.selection()
        
        if not selection:
            messagebox.showinfo("💡 Cómo ver detalles de productos", 
                "Forma de ver los detalles de un producto:\n\n" +
                "🖱️ OPCIÓN 1: Clic Derecho\n" +
                "   • Haga clic derecho sobre cualquier producto\n" +
                "   • Seleccione '👁️ Ver Detalles' en el menú\n\n"
                "💡 Tip: Doble clic en una fila para editarla directamente")
            return
        
        try:
            item = self.productos_tree.item(selection[0])
            producto_id = item['values'][0]
            
            # Obtener datos completos del producto desde la BD
            producto = self.controller.obtener_producto_por_id(producto_id)
            
            if not producto:
                messagebox.showerror("Error", "No se pudo obtener la información del producto")
                return
            
            # Crear ventana de detalles
            dialog = tk.Toplevel(self.root)
            dialog.title(f"👁️ Detalles del Producto - {producto['nombre']}")
            dialog.geometry("650x750")
            dialog.transient(self.root)
            dialog.withdraw()
            dialog.grab_set()
            self.agregar_icono(dialog)
            
            # Frame principal con scroll
            main_frame = tb.Frame(dialog, padding=20)
            main_frame.pack(fill='both', expand=True)
            
            # Canvas con scrollbar
            canvas = tk.Canvas(main_frame, highlightthickness=0)
            scrollbar = tb.Scrollbar(main_frame, orient="vertical", command=canvas.yview, bootstyle="primary-round")
            content_frame = tb.Frame(canvas)
            
            content_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=content_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Habilitar scroll con rueda del mouse
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Título principal
            tb.Label(
                content_frame,
                text="📦 INFORMACIÓN COMPLETA DEL PRODUCTO",
                font=('Segoe UI', 16, 'bold'),
                bootstyle="primary"
            ).pack(pady=(0, 20))
            
            # === INFORMACIÓN BÁSICA ===
            info_basica = tb.Labelframe(
                content_frame,
                text="📋 Información Básica",
                padding=15,
                bootstyle="info"
            )
            info_basica.pack(fill='x', pady=(0, 15))
            
            # Función helper para crear fila de información
            def crear_fila_info(parent, label, valor, row):
                tb.Label(
                    parent,
                    text=f"{label}:",
                    font=('Segoe UI', 10, 'bold'),
                    anchor='e'
                ).grid(row=row, column=0, sticky='e', padx=(10, 15), pady=8)
                
                tb.Label(
                    parent,
                    text=str(valor) if valor else 'N/A',
                    font=('Segoe UI', 10),
                    anchor='w'
                ).grid(row=row, column=1, sticky='w', padx=(0, 10), pady=8)
            
            crear_fila_info(info_basica, "ID", producto['id'], 0)
            crear_fila_info(info_basica, "Código SKU", producto.get('codigo', 'N/A'), 1)
            crear_fila_info(info_basica, "Nombre", producto['nombre'], 2)
            crear_fila_info(info_basica, "Categoría", producto.get('categoria', 'N/A'), 3)
            crear_fila_info(info_basica, "Estado", "ACTIVO" if producto.get('activo', 1) == 1 else "INACTIVO", 4)
            
            info_basica.columnconfigure(0, minsize=150)
            info_basica.columnconfigure(1, weight=1)
            
            # === DATOS DEL SKU ===
            sku_frame = tb.Labelframe(
                content_frame,
                text="🏷️ Datos del Código SKU",
                padding=15,
                bootstyle="success"
            )
            sku_frame.pack(fill='x', pady=(0, 15))
            
            crear_fila_info(sku_frame, "🏭 Marca", producto.get('marca', 'N/A'), 0)
            crear_fila_info(sku_frame, "🎨 Color", producto.get('color', 'N/A'), 1)
            crear_fila_info(sku_frame, "📏 Tamaño", producto.get('tamaño', 'N/A'), 2)
            crear_fila_info(sku_frame, "🎭 Dibujo", producto.get('dibujo', 'N/A'), 3)
            crear_fila_info(sku_frame, "🔢 Código de Color", producto.get('cod_color', 'N/A'), 4)
            
            sku_frame.columnconfigure(0, minsize=150)
            sku_frame.columnconfigure(1, weight=1)
            
            # === INFORMACIÓN FINANCIERA ===
            financiera_frame = tb.Labelframe(
                content_frame,
                text="💰 Información Financiera",
                padding=15,
                bootstyle="warning"
            )
            financiera_frame.pack(fill='x', pady=(0, 15))
            
            precio_compra = producto['precio_compra']
            porcentaje_ganancia = producto['porcentaje_ganancia']
            precio_venta = producto['precio_venta']
            monto_ganancia = producto.get('monto_ganancia', precio_venta - precio_compra)
            
            crear_fila_info(financiera_frame, "Precio de Compra", f"Q {precio_compra:,.2f}", 0)
            crear_fila_info(financiera_frame, "Porcentaje de Ganancia", f"{porcentaje_ganancia:.2f}%", 1)
            crear_fila_info(financiera_frame, "Monto de Ganancia", f"Q {monto_ganancia:,.2f}", 2)
            crear_fila_info(financiera_frame, "Precio de Venta", f"Q {precio_venta:,.2f}", 3)
            
            financiera_frame.columnconfigure(0, minsize=150)
            financiera_frame.columnconfigure(1, weight=1)
            
            # === INVENTARIO ===
            inventario_frame = tb.Labelframe(
                content_frame,
                text="📦 Inventario",
                padding=15,
                bootstyle="secondary"
            )
            inventario_frame.pack(fill='x', pady=(0, 15))
            
            stock_actual = producto.get('stock_actual', 0)
            stock_color = "danger" if stock_actual <= 5 else "success"
            
            tb.Label(
                inventario_frame,
                text="Stock Actual:",
                font=('Segoe UI', 10, 'bold'),
                anchor='e'
            ).grid(row=0, column=0, sticky='e', padx=(10, 15), pady=8)
            
            tb.Label(
                inventario_frame,
                text=f"{stock_actual:,} unidades",
                font=('Segoe UI', 12, 'bold'),
                bootstyle=stock_color,
                anchor='w'
            ).grid(row=0, column=1, sticky='w', padx=(0, 10), pady=8)
            
            if stock_actual <= 5:
                tb.Label(
                    inventario_frame,
                    text="⚠️ Stock bajo - Requiere reabastecimiento",
                    font=('Segoe UI', 9),
                    bootstyle="danger"
                ).grid(row=1, column=0, columnspan=2, pady=(0, 5))
            
            inventario_frame.columnconfigure(0, minsize=150)
            inventario_frame.columnconfigure(1, weight=1)
            
            # Botón cerrar
            tb.Button(
                content_frame,
                text="✓ Cerrar",
                command=dialog.destroy,
                bootstyle="primary",
                width=20
            ).pack(pady=(15, 0))
            
            # Centrar y mostrar
            self.centrar_ventana(dialog)
            dialog.deiconify()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalles: {str(e)}")
    
    def desactivar_producto(self):
        """Marca un producto como inactivo"""
        # Asegurarse de que el foco esté en el Treeview
        self.productos_tree.focus_set()
        
        # Obtener selección con múltiples intentos
        selection = self.productos_tree.selection()
        
        # Si no hay selección, intentar obtener el item con foco
        if not selection:
            focused_item = self.productos_tree.focus()
            if focused_item:
                selection = (focused_item,)
        
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto haciendo clic en una fila de la tabla")
            return
        
        try:
            item = self.productos_tree.item(selection[0])
            if not item or 'values' not in item or len(item['values']) < 3:
                messagebox.showwarning("Advertencia", "No se pudo obtener la información del producto")
                return
                
            producto_id = item['values'][0]
            producto_nombre = item['values'][2]
            
            # Confirmar
            if messagebox.askyesno("Confirmar", 
                f"¿Está seguro de marcar como INACTIVO el producto:\n\n'{producto_nombre}'?\n\n" +
                "El producto no aparecerá en compras ni ventas, pero conservará su historial."):
                
                exito, mensaje = self.controller.cambiar_estado_producto(producto_id, False)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.refresh_productos()
                    self.refresh_alertas()  # Actualizar alertas para quitar productos inactivos
                    self.limpiar_formulario_producto_tab()
                else:
                    messagebox.showerror("Error", mensaje)
        except Exception as e:
            # Error silencioso - el producto ya fue procesado correctamente
            pass
    
    def activar_producto(self):
        """Marca un producto como activo"""
        # Asegurarse de que el foco esté en el Treeview
        self.productos_tree.focus_set()
        
        # Obtener selección con múltiples intentos
        selection = self.productos_tree.selection()
        
        # Si no hay selección, intentar obtener el item con foco
        if not selection:
            focused_item = self.productos_tree.focus()
            if focused_item:
                selection = (focused_item,)
        
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto haciendo clic en una fila de la tabla")
            return
        
        try:
            item = self.productos_tree.item(selection[0])
            if not item or 'values' not in item or len(item['values']) < 3:
                messagebox.showwarning("Advertencia", "No se pudo obtener la información del producto")
                return
                
            producto_id = item['values'][0]
            producto_nombre = item['values'][2]
            
            exito, mensaje = self.controller.cambiar_estado_producto(producto_id, True)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.refresh_productos()
                self.refresh_alertas()  # Actualizar alertas para mostrar productos activos
                self.limpiar_formulario_producto_tab()
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            # Error silencioso - el producto ya fue procesado correctamente
            pass
    
    def create_proveedores_tab(self):
        """Crea la pestaña de gestión de proveedores"""
        proveedores_frame = tb.Frame(self.notebook)
        self.notebook.add(proveedores_frame, text="👥 Proveedores")
        
        # Frame principal con dos paneles
        paned = tb.PanedWindow(proveedores_frame, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Formulario
        form_panel = tb.LabelFrame(paned, text="Datos del Proveedor", bootstyle="primary")
        paned.add(form_panel, weight=1)
        
        form_inner = tb.Frame(form_panel)
        form_inner.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Campos del formulario
        tb.Label(form_inner, text="Nombre: *", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky='w', pady=5)
        self.proveedor_nombre_entry = tb.Entry(form_inner, textvariable=self.proveedor_nombre, width=40, font=("Segoe UI", 10))
        self.proveedor_nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        tb.Label(form_inner, text="NIT o DPI: *", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky='w', pady=5)
        tb.Entry(form_inner, textvariable=self.proveedor_nit, width=40, font=("Segoe UI", 10)).grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        tb.Label(form_inner, text="Dirección: *", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky='w', pady=5)
        tb.Entry(form_inner, textvariable=self.proveedor_direccion, width=40, font=("Segoe UI", 10)).grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        tb.Label(form_inner, text="Teléfono:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky='w', pady=5)
        tb.Entry(form_inner, textvariable=self.proveedor_telefono, width=40, font=("Segoe UI", 10)).grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        
        form_inner.columnconfigure(1, weight=1)
        
        # Botones
        button_frame = tb.Frame(form_inner)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tb.Button(button_frame, text="➕ Crear Proveedor", bootstyle="success", command=self.crear_proveedor).pack(side='left', padx=5)
        tb.Button(button_frame, text="✏️ Actualizar", bootstyle="warning", command=self.actualizar_proveedor).pack(side='left', padx=5)
        tb.Button(button_frame, text="🔄 Limpiar", bootstyle="secondary", command=self.limpiar_form_proveedor).pack(side='left', padx=5)
        
        # Panel derecho - Lista de proveedores
        list_panel = tb.LabelFrame(paned, text="Lista de Proveedores", bootstyle="info")
        paned.add(list_panel, weight=2)
        
        # Barra de búsqueda
        search_frame = tb.Frame(list_panel)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tb.Label(search_frame, text="🔍 Buscar:", font=("Segoe UI", 10, "bold")).pack(side='left', padx=5)
        search_entry = tb.Entry(search_frame, textvariable=self.proveedor_busqueda, width=30, font=("Segoe UI", 10))
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.buscar_proveedores())
        
        tb.Button(search_frame, text="🔄 Mostrar Todos", bootstyle="info-outline", command=self.refresh_proveedores).pack(side='left', padx=5)
        
        # Tabla
        tree_frame = tb.Frame(list_panel)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tb.Scrollbar(tree_frame, bootstyle="primary-round")
        scrollbar.pack(side='right', fill='y')
        
        self.proveedores_tree = tb.Treeview(
            tree_frame,
            columns=('ID', 'Nombre', 'NIT/DPI', 'Dirección', 'Teléfono', 'Fecha Registro'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=15
        )
        
        scrollbar.config(command=self.proveedores_tree.yview)
        
        # Configurar columnas
        self.proveedores_tree.heading('ID', text='ID')
        self.proveedores_tree.heading('Nombre', text='Nombre')
        self.proveedores_tree.heading('NIT/DPI', text='NIT o DPI')
        self.proveedores_tree.heading('Dirección', text='Dirección')
        self.proveedores_tree.heading('Teléfono', text='Teléfono')
        self.proveedores_tree.heading('Fecha Registro', text='Fecha Registro')
        
        self.proveedores_tree.column('ID', width=50, anchor='center')
        self.proveedores_tree.column('Nombre', width=200, anchor='w')
        self.proveedores_tree.column('NIT/DPI', width=120, anchor='center')
        self.proveedores_tree.column('Dirección', width=250, anchor='w')
        self.proveedores_tree.column('Teléfono', width=100, anchor='center')
        self.proveedores_tree.column('Fecha Registro', width=150, anchor='center')
        
        self.proveedores_tree.pack(fill='both', expand=True)
        
        # Evento de doble clic para editar
        self.proveedores_tree.bind('<Double-Button-1>', self.on_proveedor_select)
        
        # Alternancia de colores
        self.proveedores_tree.tag_configure('evenrow', background='#f0f0f0')
        self.proveedores_tree.tag_configure('oddrow', background='white')
    
    def create_clientes_tab(self):
        """Crea la pestaña de gestión de clientes"""
        clientes_frame = tb.Frame(self.notebook)
        self.notebook.add(clientes_frame, text="👤 Clientes")
        
        # Frame principal con dos paneles
        paned = tb.PanedWindow(clientes_frame, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Formulario
        form_panel = tb.LabelFrame(paned, text="Datos del Cliente", bootstyle="primary")
        paned.add(form_panel, weight=1)
        
        form_inner = tb.Frame(form_panel)
        form_inner.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Campos del formulario
        tb.Label(form_inner, text="Nombre: *", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky='w', pady=5)
        self.cliente_nombre_entry = tb.Entry(form_inner, textvariable=self.cliente_nombre, width=40, font=("Segoe UI", 10))
        self.cliente_nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        tb.Label(form_inner, text="NIT o DPI: *", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky='w', pady=5)
        tb.Entry(form_inner, textvariable=self.cliente_nit, width=40, font=("Segoe UI", 10)).grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        tb.Label(form_inner, text="Dirección: *", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky='w', pady=5)
        tb.Entry(form_inner, textvariable=self.cliente_direccion, width=40, font=("Segoe UI", 10)).grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        tb.Label(form_inner, text="Teléfono:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky='w', pady=5)
        tb.Entry(form_inner, textvariable=self.cliente_telefono, width=40, font=("Segoe UI", 10)).grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        
        form_inner.columnconfigure(1, weight=1)
        
        # Botones
        button_frame = tb.Frame(form_inner)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tb.Button(button_frame, text="➕ Crear Cliente", bootstyle="success", command=self.crear_cliente).pack(side='left', padx=5)
        tb.Button(button_frame, text="✏️ Actualizar", bootstyle="warning", command=self.actualizar_cliente).pack(side='left', padx=5)
        tb.Button(button_frame, text="🔄 Limpiar", bootstyle="secondary", command=self.limpiar_form_cliente).pack(side='left', padx=5)
        
        # Panel derecho - Lista de clientes
        list_panel = tb.LabelFrame(paned, text="Lista de Clientes", bootstyle="info")
        paned.add(list_panel, weight=2)
        
        # Barra de búsqueda
        search_frame = tb.Frame(list_panel)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tb.Label(search_frame, text="🔍 Buscar:", font=("Segoe UI", 10, "bold")).pack(side='left', padx=5)
        search_entry = tb.Entry(search_frame, textvariable=self.cliente_busqueda, width=30, font=("Segoe UI", 10))
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.buscar_clientes())
        
        tb.Button(search_frame, text="🔄 Mostrar Todos", bootstyle="info-outline", command=self.refresh_clientes).pack(side='left', padx=5)
        
        # Tabla
        tree_frame = tb.Frame(list_panel)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tb.Scrollbar(tree_frame, bootstyle="primary-round")
        scrollbar.pack(side='right', fill='y')
        
        self.clientes_tree = tb.Treeview(
            tree_frame,
            columns=('ID', 'Nombre', 'NIT/DPI', 'Dirección', 'Teléfono', 'Fecha Registro'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=15
        )
        
        scrollbar.config(command=self.clientes_tree.yview)
        
        # Configurar columnas
        self.clientes_tree.heading('ID', text='ID')
        self.clientes_tree.heading('Nombre', text='Nombre')
        self.clientes_tree.heading('NIT/DPI', text='NIT o DPI')
        self.clientes_tree.heading('Dirección', text='Dirección')
        self.clientes_tree.heading('Teléfono', text='Teléfono')
        self.clientes_tree.heading('Fecha Registro', text='Fecha Registro')
        
        self.clientes_tree.column('ID', width=50, anchor='center')
        self.clientes_tree.column('Nombre', width=200, anchor='w')
        self.clientes_tree.column('NIT/DPI', width=120, anchor='center')
        self.clientes_tree.column('Dirección', width=250, anchor='w')
        self.clientes_tree.column('Teléfono', width=100, anchor='center')
        self.clientes_tree.column('Fecha Registro', width=150, anchor='center')
        
        self.clientes_tree.pack(fill='both', expand=True)
        
        # Evento de doble clic para editar
        self.clientes_tree.bind('<Double-Button-1>', self.on_cliente_select)
        
        # Alternancia de colores
        self.clientes_tree.tag_configure('evenrow', background='#f0f0f0')
        self.clientes_tree.tag_configure('oddrow', background='white')
    
    # MÉTODOS DE PROVEEDORES
    def crear_proveedor(self):
        """Crea un nuevo proveedor"""
        exito, mensaje = self.controller.crear_proveedor(
            self.proveedor_nombre.get(),
            self.proveedor_nit.get(),
            self.proveedor_direccion.get(),
            self.proveedor_telefono.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_form_proveedor()
            self.refresh_proveedores()
            self.refresh_combos()
        else:
            messagebox.showerror("Error", mensaje)
    
    def actualizar_proveedor(self):
        """Actualiza el proveedor seleccionado"""
        if not self.proveedor_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para actualizar")
            return
        
        exito, mensaje = self.controller.actualizar_proveedor(
            self.proveedor_seleccionado,
            self.proveedor_nombre.get(),
            self.proveedor_nit.get(),
            self.proveedor_direccion.get(),
            self.proveedor_telefono.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_form_proveedor()
            self.refresh_proveedores()
            self.refresh_combos()
        else:
            messagebox.showerror("Error", mensaje)
    
    def on_proveedor_select(self, event):
        """Maneja la selección de un proveedor"""
        selection = self.proveedores_tree.selection()
        if selection:
            item = self.proveedores_tree.item(selection[0])
            values = item['values']
            
            self.proveedor_seleccionado = values[0]
            self.proveedor_nombre.set(values[1])
            self.proveedor_nit.set(values[2])
            self.proveedor_direccion.set(values[3])
            self.proveedor_telefono.set(values[4])
    
    def limpiar_form_proveedor(self):
        """Limpia el formulario de proveedores"""
        self.proveedor_nombre.set("")
        self.proveedor_nit.set("")
        self.proveedor_direccion.set("")
        self.proveedor_telefono.set("")
        self.proveedor_seleccionado = None
    
    def buscar_proveedores(self):
        """Busca proveedores por nombre o NIT"""
        from datetime import datetime
        busqueda = self.proveedor_busqueda.get()
        proveedores = self.controller.buscar_proveedor(busqueda)
        
        # Limpiar tabla
        for item in self.proveedores_tree.get_children():
            self.proveedores_tree.delete(item)
        
        # Llenar tabla
        for i, prov in enumerate(proveedores):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            # Formatear fecha a dd/mm/yyyy
            fecha_str = prov['fecha_registro']
            try:
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
            except:
                fecha_formateada = fecha_str.split()[0] if ' ' in fecha_str else fecha_str
            
            self.proveedores_tree.insert('', 'end', values=(
                prov['id'],
                prov['nombre'],
                prov['nit_dpi'],
                prov['direccion'],
                prov['telefono'],
                fecha_formateada
            ), tags=(tag,))
    
    # MÉTODOS DE CLIENTES
    def crear_cliente(self):
        """Crea un nuevo cliente"""
        exito, mensaje = self.controller.crear_cliente(
            self.cliente_nombre.get(),
            self.cliente_nit.get(),
            self.cliente_direccion.get(),
            self.cliente_telefono.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_form_cliente()
            self.refresh_clientes()
            self.refresh_combos()
        else:
            messagebox.showerror("Error", mensaje)
    
    def actualizar_cliente(self):
        """Actualiza el cliente seleccionado"""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para actualizar")
            return
        
        exito, mensaje = self.controller.actualizar_cliente(
            self.cliente_seleccionado,
            self.cliente_nombre.get(),
            self.cliente_nit.get(),
            self.cliente_direccion.get(),
            self.cliente_telefono.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_form_cliente()
            self.refresh_clientes()
            self.refresh_combos()
        else:
            messagebox.showerror("Error", mensaje)
    
    def on_cliente_select(self, event):
        """Maneja la selección de un cliente"""
        selection = self.clientes_tree.selection()
        if selection:
            item = self.clientes_tree.item(selection[0])
            values = item['values']
            
            self.cliente_seleccionado = values[0]
            self.cliente_nombre.set(values[1])
            self.cliente_nit.set(values[2])
            self.cliente_direccion.set(values[3])
            self.cliente_telefono.set(values[4])
    
    def limpiar_form_cliente(self):
        """Limpia el formulario de clientes"""
        self.cliente_nombre.set("")
        self.cliente_nit.set("")
        self.cliente_direccion.set("")
        self.cliente_telefono.set("")
        self.cliente_seleccionado = None
    
    def buscar_clientes(self):
        """Busca clientes por nombre o NIT"""
        from datetime import datetime
        busqueda = self.cliente_busqueda.get()
        clientes = self.controller.buscar_cliente(busqueda)
        
        # Limpiar tabla
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        # Llenar tabla
        for i, cli in enumerate(clientes):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            # Formatear fecha a dd/mm/yyyy
            fecha_str = cli['fecha_registro']
            try:
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
            except:
                fecha_formateada = fecha_str.split()[0] if ' ' in fecha_str else fecha_str
            
            self.clientes_tree.insert('', 'end', values=(
                cli['id'],
                cli['nombre'],
                cli['nit_dpi'],
                cli['direccion'],
                cli['telefono'],
                fecha_formateada
            ), tags=(tag,))
    
    # MÉTODOS DE ACTUALIZACIÓN DE DATOS
    def refresh_productos(self):
        """Actualiza la lista de productos - Delegado al tab refactorizado"""
        if hasattr(self, 'productos_tab'):
            self.productos_tab.refresh()
    
    def refresh_compras(self):
        """Actualiza la lista de compras - Delegado al tab refactorizado"""
        if hasattr(self, 'compras_tab'):
            self.compras_tab.refresh()
    
    def refresh_ventas(self):
        """Actualiza la lista de ventas - Delegado al tab refactorizado"""
        if hasattr(self, 'ventas_tab'):
            self.ventas_tab.refresh()
    
    def refresh_combos(self):
        """Actualiza los combos (YA NO SE USA - ahora usa búsqueda)"""
        pass
    
    def actualizar_resumen(self):
        """Actualiza el resumen financiero - Delegado al tab de Reportes"""
        if hasattr(self, 'reportes_tab'):
            self.reportes_tab.actualizar_metricas()
    
    def ir_a_reportes(self):
        """Navega a la pestaña de Reportes y actualiza los datos"""
        # Actualizar primero los datos
        self.actualizar_resumen()
        # Cambiar a la pestaña de Reportes (índice 6)
        self.notebook.select(6)
    
    def salir_sistema(self):
        """Cierra la aplicación con confirmación"""
        # Crear diálogo personalizado con icono
        dialog = tk.Toplevel(self.root)
        dialog.title("Salir del Sistema")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.resizable(False, False)
        
        # Ocultar ventana temporalmente
        dialog.withdraw()
        
        dialog.grab_set()
        self.agregar_icono(dialog)
        
        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f'400x200+{x}+{y}')
        
        # Mostrar ventana ya centrada
        dialog.deiconify()
        
        resultado = {'salir': False}
        
        # Frame principal
        frame = tb.Frame(dialog, padding=20)
        frame.pack(fill='both', expand=True)
        
        # Icono y mensaje
        mensaje_frame = tb.Frame(frame)
        mensaje_frame.pack(pady=(10, 20))
        
        # Icono de advertencia
        tb.Label(
            mensaje_frame,
            text="⚠️",
            font=('Segoe UI', 40)
        ).pack(side='left', padx=(0, 15))
        
        # Texto
        text_frame = tb.Frame(mensaje_frame)
        text_frame.pack(side='left')
        
        tb.Label(
            text_frame,
            text="¿Estás seguro que deseas cerrar la aplicación?",
            font=('Segoe UI', 10, 'bold'),
            wraplength=250
        ).pack(anchor='w')
        
        tb.Label(
            text_frame,
            text="Todos los datos están guardados.",
            font=('Segoe UI', 9),
            foreground='gray'
        ).pack(anchor='w', pady=(5, 0))
        
        # Botones
        btn_frame = tb.Frame(frame)
        btn_frame.pack(pady=(10, 0))
        
        def confirmar_salir():
            resultado['salir'] = True
            dialog.destroy()
        
        def cancelar():
            dialog.destroy()
        
        tb.Button(
            btn_frame,
            text="Sí, Salir",
            command=confirmar_salir,
            bootstyle="danger",
            width=12
        ).pack(side='left', padx=5)
        
        tb.Button(
            btn_frame,
            text="Cancelar",
            command=cancelar,
            bootstyle="secondary",
            width=12
        ).pack(side='left', padx=5)
        
        # Esperar a que se cierre el diálogo
        dialog.wait_window()
        
        # Si confirmó, cerrar la aplicación
        if resultado['salir']:
            self.root.quit()
    
    def refresh_stock_bajo(self):
        """Actualiza la lista de alertas: stock bajo y productos próximos a vencer"""
        from datetime import datetime
        
        # Limpiar el treeview
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        # 1. PRODUCTOS CON STOCK BAJO (solo activos)
        productos_bajo = self.controller.obtener_productos_con_stock_bajo(5)
        productos_activos_bajo = [p for p in productos_bajo if p.get('activo', 1) == 1]
        
        for producto in productos_activos_bajo:
            self.stock_tree.insert('', 'end', values=(
                'Stock Bajo',
                producto.get('codigo', ''),
                producto['nombre'],
                'Muy bajo',
                f"{producto['stock_actual']} unidades",
                'Realizar pedido de reabastecimiento'
            ), tags=('alert_stock',))
        
        # 2. PRODUCTOS PRÓXIMOS A VENCER (agrupar por producto, mostrar solo la más próxima)
        productos_vencer = self.controller.obtener_productos_proximos_vencer(30)
        
        # Filtrar solo productos activos
        productos_vencer_activos = []
        for compra in productos_vencer:
            producto = self.controller.obtener_producto_por_id(compra['producto_id'])
            if producto and producto.get('activo', 1) == 1:
                productos_vencer_activos.append(compra)
        
        # Agrupar por producto_id y quedarnos solo con la compra más próxima a vencer de cada producto
        productos_agrupados = {}
        for compra in productos_vencer_activos:
            producto_id = compra['producto_id']
            if producto_id not in productos_agrupados:
                productos_agrupados[producto_id] = compra
            else:
                # Comparar fechas y quedarnos con la más próxima
                try:
                    fecha_actual = datetime.strptime(compra['fecha_vencimiento'], '%d/%m/%Y')
                    fecha_guardada = datetime.strptime(productos_agrupados[producto_id]['fecha_vencimiento'], '%d/%m/%Y')
                    if fecha_actual < fecha_guardada:
                        productos_agrupados[producto_id] = compra
                except:
                    pass
        
        # Mostrar solo la compra más próxima a vencer de cada producto
        for compra in productos_agrupados.values():
            try:
                # Calcular días restantes
                fecha_venc = compra['fecha_vencimiento']
                fecha_venc_obj = datetime.strptime(fecha_venc, '%d/%m/%Y')
                hoy = datetime.now()
                dias_restantes = (fecha_venc_obj - hoy).days
                
                # Determinar tipo, estado, valor, acción y tag según días restantes
                if dias_restantes < 0:
                    tipo = 'VENCIDO'
                    estado = 'Ya venció'
                    valor = f"Hace {abs(dias_restantes)} días"
                    accion = 'RETIRAR INMEDIATAMENTE del inventario'
                    tag = 'alert_vencido'
                elif dias_restantes <= 7:
                    tipo = 'CRITICO'
                    estado = 'Vence muy pronto'
                    valor = f"{dias_restantes} días restantes"
                    accion = 'Vender urgentemente o retirar'
                    tag = 'alert_critico'
                elif dias_restantes <= 30:
                    tipo = 'ADVERTENCIA'
                    estado = 'Próximo a vencer'
                    valor = f"{dias_restantes} días restantes"
                    accion = 'Planificar venta prioritaria'
                    tag = 'alert_advertencia'
                else:
                    continue  # No mostrar si tiene más de 30 días
                
                # Obtener stock actual del producto
                producto = self.controller.obtener_producto_por_id(compra['producto_id'])
                stock_actual = producto['stock_actual'] if producto else 0
                producto_codigo = producto.get('codigo', '') if producto else ''
                
                # Solo mostrar si hay stock disponible
                if stock_actual > 0:
                    # Insertar en el TreeView
                    self.stock_tree.insert('', 'end', values=(
                        tipo,
                        producto_codigo,
                        compra['producto_nombre'],
                        estado,
                        valor,
                        accion
                    ), tags=(tag,))
                
            except Exception as e:
                print(f"Error al procesar vencimiento: {e}")
                continue
    
    def refresh_proveedores(self):
        """Actualiza la lista de proveedores - Delegado al tab refactorizado"""
        if hasattr(self, 'proveedores_tab'):
            self.proveedores_tab.refresh()
    
    def refresh_clientes(self):
        """Actualiza la lista de clientes - Delegado al tab refactorizado"""
        if hasattr(self, 'clientes_tab'):
            self.clientes_tab.refresh()
    
    # MÉTODOS DE CAJA
    def actualizar_categorias_caja(self, event=None):
        """Actualiza las categorías según el tipo seleccionado"""
        tipo = self.caja_tipo.get()
        if tipo == 'INGRESO':
            self.categoria_combo['values'] = ['APORTE_CAPITAL', 'OTRO']
            self.caja_categoria.set('APORTE_CAPITAL')
        else:  # EGRESO
            self.categoria_combo['values'] = ['GASTO_OPERATIVO', 'RETIRO_UTILIDAD', 'OTRO']
            self.caja_categoria.set('GASTO_OPERATIVO')
    
    def registrar_movimiento_caja(self):
        """Registra un movimiento de caja"""
        from datetime import datetime
        
        try:
            # Validar campos
            if not self.caja_concepto.get().strip():
                messagebox.showwarning("Advertencia", "Debe ingresar un concepto")
                return
            
            if self.caja_monto.get() <= 0:
                messagebox.showwarning("Advertencia", "El monto debe ser mayor a 0")
                return
            
            # Obtener fecha seleccionada y agregar hora actual
            fecha_cal = self.caja_fecha_entry.entry.get()
            hora_actual = datetime.now().strftime('%H:%M:%S')
            fecha_completa = f"{fecha_cal} {hora_actual}"
            
            # Registrar movimiento
            exito, mensaje = self.controller.registrar_movimiento_caja(
                self.caja_tipo.get(),
                self.caja_categoria.get(),
                self.caja_concepto.get(),
                self.caja_monto.get(),
                fecha_completa
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_form_caja()
                self.refresh_caja()
            else:
                messagebox.showerror("Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar movimiento: {str(e)}")
    
    def retiro_utilidades_rapido(self):
        """Acceso rápido para retiro de utilidades"""
        self.caja_tipo.set('EGRESO')
        self.actualizar_categorias_caja()
        self.caja_categoria.set('RETIRO_UTILIDAD')
        self.caja_concepto.set('Retiro de utilidades')
        self.caja_monto.set(0.0)
    
    def aporte_capital_rapido(self):
        """Acceso rápido para aporte de capital"""
        self.caja_tipo.set('INGRESO')
        self.actualizar_categorias_caja()
        self.caja_categoria.set('APORTE_CAPITAL')
        self.caja_concepto.set('Aporte de capital')
        self.caja_monto.set(0.0)
    
    def limpiar_form_caja(self):
        """Limpia el formulario de caja"""
        self.caja_tipo.set('EGRESO')
        self.actualizar_categorias_caja()
        self.caja_concepto.set('')
        self.caja_monto.set(0.0)
    
    def filtrar_movimientos_caja(self):
        """Filtra movimientos por rango de fechas"""
        from datetime import datetime
        
        fecha_inicio = self.caja_fecha_inicio.entry.get()
        fecha_fin = self.caja_fecha_fin.entry.get()
        
        # Convertir fechas de dd/mm/yyyy a yyyy-mm-dd para SQL
        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio, '%d/%m/%Y')
            fecha_fin_obj = datetime.strptime(fecha_fin, '%d/%m/%Y')
            
            fecha_inicio_sql = fecha_inicio_obj.strftime('%Y-%m-%d')
            fecha_fin_sql = fecha_fin_obj.strftime('%Y-%m-%d')
            
            # Obtener movimientos filtrados
            movimientos = self.controller.obtener_movimientos_caja(fecha_inicio_sql, fecha_fin_sql)
            resumen = self.controller.obtener_resumen_caja(fecha_inicio_sql, fecha_fin_sql)
            
            # Actualizar tabla
            self.cargar_movimientos_caja(movimientos)
            
            # Actualizar labels de resumen
            self.ingresos_label.config(text=f"↑ Ingresos: Q {resumen['total_ingresos']:,.2f}")
            self.egresos_label.config(text=f"↓ Egresos: Q {resumen['total_egresos']:,.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar: {str(e)}")
    
    def eliminar_movimiento_caja(self):
        """Elimina un movimiento de caja seleccionado"""
        seleccion = self.caja_tree.selection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un movimiento para eliminar")
            return
        
        # Obtener datos del movimiento
        item = self.caja_tree.item(seleccion[0])
        valores = item['values']
        movimiento_id = valores[0]
        concepto = valores[4]
        monto = valores[5]
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar este movimiento?\n\n"
            f"ID: {movimiento_id}\n"
            f"Concepto: {concepto}\n"
            f"Monto: {monto}\n\n"
            f"⚠️ ADVERTENCIA: Esta acción no se puede deshacer y afectará el saldo de caja."
        )
        
        if respuesta:
            try:
                exito, mensaje = self.controller.eliminar_movimiento_caja(movimiento_id)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.refresh_caja()
                else:
                    messagebox.showerror("Error", mensaje)
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar movimiento: {str(e)}")
    
    def ver_detalle_movimiento(self, event):
        """Muestra los detalles completos de un movimiento al hacer doble clic"""
        seleccion = self.caja_tree.selection()
        
        if not seleccion:
            return
        
        # Obtener datos del movimiento
        item = self.caja_tree.item(seleccion[0])
        valores = item['values']
        
        # Crear ventana de detalles
        detalle_window = tk.Toplevel(self.root)
        detalle_window.title("Detalles del Movimiento")
        detalle_window.geometry("650x500")
        detalle_window.transient(self.root)
        detalle_window.resizable(False, False)
        
        # Ocultar ventana temporalmente para evitar parpadeo
        detalle_window.withdraw()
        
        detalle_window.grab_set()
        self.agregar_icono(detalle_window)
        
        # Frame para canvas y scrollbars (contenido)
        container = tb.Frame(detalle_window)
        container.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Canvas con scrollbar horizontal solamente
        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar_x = tb.Scrollbar(container, orient="horizontal", command=canvas.xview, bootstyle="primary-round")
        
        scrollable_frame = tb.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar_x.set)
        
        # Frame principal (dentro del scroll)
        main_frame = tb.Frame(scrollable_frame, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        tb.Label(
            main_frame,
            text="📋 Detalles del Movimiento de Caja",
            font=('Segoe UI', 14, 'bold'),
            bootstyle="primary"
        ).pack(pady=(0, 15))
        
        # Información del movimiento
        info_frame = tb.Frame(main_frame)
        info_frame.pack(fill='both', expand=True, padx=10)
        
        campos = [
            ("ID:", valores[0]),
            ("Fecha:", valores[1]),
            ("Tipo:", valores[2]),
            ("Categoría:", valores[3]),
            ("Concepto:", valores[4]),
            ("Monto:", valores[5]),
            ("Saldo Anterior:", valores[6]),
            ("Saldo Nuevo:", valores[7])
        ]
        
        for i, (label, valor) in enumerate(campos):
            # Label
            tb.Label(
                info_frame,
                text=label,
                font=('Segoe UI', 11, 'bold'),
                bootstyle="secondary"
            ).grid(row=i, column=0, sticky='w', pady=6, padx=5)
            
            # Valor - Si es concepto y es largo, usar Text widget con scroll
            if label == "Concepto:" and len(str(valor)) > 60:
                text_widget = tk.Text(
                    info_frame,
                    height=3,
                    width=50,
                    wrap='word',
                    font=('Segoe UI', 10),
                    relief='solid',
                    borderwidth=1
                )
                text_widget.insert('1.0', str(valor))
                text_widget.configure(state='disabled')
                text_widget.grid(row=i, column=1, sticky='ew', pady=6, padx=10)
                
                # Scrollbar para el concepto
                text_scroll = tb.Scrollbar(info_frame, orient='vertical', command=text_widget.yview, bootstyle="secondary-round")
                text_widget.configure(yscrollcommand=text_scroll.set)
                text_scroll.grid(row=i, column=2, sticky='ns', pady=6)
            else:
                # Valor normal
                valor_label = tb.Label(
                    info_frame,
                    text=str(valor),
                    font=('Segoe UI', 11),
                    bootstyle="primary" if label in ["Monto:", "Saldo Nuevo:"] else "dark"
                )
                valor_label.grid(row=i, column=1, sticky='w', pady=6, padx=10, columnspan=2)
        
        # Configurar peso de las columnas
        info_frame.columnconfigure(1, weight=1)
        
        # Empaquetar canvas y scrollbar
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Separador visual
        tb.Separator(detalle_window, bootstyle="secondary").pack(fill='x')
        
        # Frame para botón fijo en la parte inferior (FUERA del scroll)
        btn_frame = tb.Frame(detalle_window, padding=10)
        btn_frame.pack(fill='x', side='bottom')
        
        tb.Button(
            btn_frame,
            text="✓ Cerrar",
            command=detalle_window.destroy,
            bootstyle="secondary",
            width=25
        ).pack()
        
        # Habilitar scroll con rueda del mouse (para scroll horizontal con shift+rueda)
        def _on_mousewheel(event):
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_enter(event):
            canvas.bind_all("<Shift-MouseWheel>", _on_mousewheel)
        
        def _on_leave(event):
            canvas.unbind_all("<Shift-MouseWheel>")
        
        canvas.bind("<Enter>", _on_enter)
        canvas.bind("<Leave>", _on_leave)
        detalle_window.bind("<Destroy>", lambda e: canvas.unbind_all("<Shift-MouseWheel>") if canvas.winfo_exists() else None)
        
        # Centrar ventana después de crear todo el contenido
        detalle_window.update_idletasks()
        x = (detalle_window.winfo_screenwidth() // 2) - (650 // 2)
        y = (detalle_window.winfo_screenheight() // 2) - (500 // 2)
        detalle_window.geometry(f'650x500+{x}+{y}')
        
        # Mostrar ventana ya centrada
        detalle_window.deiconify()
    
    def refresh_caja(self):
        """Actualiza los datos de caja - Delegado al tab refactorizado"""
        if hasattr(self, 'caja_tab'):
            self.caja_tab.refresh()
    
    def cargar_movimientos_caja(self, movimientos):
        """Carga los movimientos en la tabla"""
        from datetime import datetime
        
        # Limpiar tabla
        for item in self.caja_tree.get_children():
            self.caja_tree.delete(item)
        
        # Llenar tabla
        for mov in movimientos:
            # Formatear fecha a dd/mm/yyyy
            fecha_str = mov['fecha']
            try:
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
            except:
                try:
                    fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y %H:%M:%S')
                    fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
                except:
                    fecha_formateada = fecha_str.split()[0] if ' ' in fecha_str else fecha_str
            
            tag = 'ingreso' if mov['tipo'] == 'INGRESO' else 'egreso'
            
            self.caja_tree.insert('', 'end', values=(
                mov['id'],
                fecha_formateada,
                mov['tipo'],
                mov['categoria'],
                mov['concepto'],
                f"Q {mov['monto']:,.2f}",
                f"Q {mov['saldo_anterior']:,.2f}",
                f"Q {mov['saldo_nuevo']:,.2f}"
            ), tags=(tag,))
    
    def sort_caja_tree(self, col, reverse):
        """Ordena la tabla de caja por columna"""
        from datetime import datetime
        
        # Obtener todos los elementos
        items = [(self.caja_tree.set(item, col), item) for item in self.caja_tree.get_children('')]
        
        # Función de ordenamiento según el tipo de columna
        def sort_key(item):
            value = item[0]
            
            # Para ID, convertir a entero
            if col == 'ID':
                try:
                    return int(value)
                except:
                    return 0
            
            # Para Fecha, convertir a datetime
            elif col == 'Fecha':
                try:
                    return datetime.strptime(value, '%d/%m/%Y')
                except:
                    return datetime.min
            
            # Para montos, extraer el número
            elif col in ['Monto', 'Saldo Anterior', 'Saldo Nuevo']:
                try:
                    # Quitar "Q " y convertir
                    num_str = value.replace('Q ', '').replace(',', '')
                    return float(num_str)
                except:
                    return 0.0
            
            # Para el resto, ordenamiento alfabético
            else:
                return value.lower()
        
        # Ordenar
        items.sort(key=sort_key, reverse=reverse)
        
        # Reorganizar elementos en el treeview
        for index, (val, item) in enumerate(items):
            self.caja_tree.move(item, '', index)
        
        # Cambiar el comando del heading para invertir el orden la próxima vez
        self.caja_tree.heading(col, command=lambda: self.sort_caja_tree(col, not reverse))
    
    def refresh_all_data(self):
        """Actualiza todos los datos de la interfaz (con lazy loading)"""
        # Solo cargar datos esenciales al inicio
        self.refresh_productos()  # Pestaña por defecto
        self.tabs_loaded['productos'] = True
        
        self.actualizar_resumen()  # Resumen importante al inicio
        self.tabs_loaded['reportes'] = True
        
        # Las demás pestañas se cargarán cuando se acceda a ellas
    
    def on_tab_changed(self, event):
        """Maneja el cambio de pestaña para lazy loading."""
        try:
            # Obtener índice de la pestaña seleccionada
            tab_index = self.notebook.index(self.notebook.select())
            
            # Mapeo de índices a nombres y métodos de actualización
            tab_map = {
                0: ('productos', self.refresh_productos),
                1: ('proveedores', self.refresh_proveedores),
                2: ('clientes', self.refresh_clientes),
                3: ('compras', self.refresh_compras),
                4: ('ventas', self.refresh_ventas),
                5: ('caja', self.refresh_caja),
                6: ('reportes', self.actualizar_resumen)
            }
            
            # Si la pestaña está en el mapeo
            if tab_index in tab_map:
                tab_name, refresh_method = tab_map[tab_index]
                
                # Siempre refrescar la pestaña de caja (puede tener cambios desde compras/ventas)
                if tab_name == 'caja':
                    refresh_method()
                    self.tabs_loaded[tab_name] = True
                # Solo cargar si NO ha sido cargada antes para otras pestañas
                elif not self.tabs_loaded.get(tab_name, False):
                    refresh_method()
                    self.tabs_loaded[tab_name] = True
                    
        except Exception as e:
            # Silenciar errores para no interrumpir la navegación
            pass
    
    # MÉTODOS DE CONFIGURACIÓN
    def cargar_base_datos(self):
        """Carga una base de datos existente"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar Base de Datos",
            filetypes=[("Base de datos SQLite", "*.db"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            exito, mensaje = self.controller.cambiar_base_datos(archivo)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.db_actual_label.config(text=archivo)
                self.refresh_all_data()
            else:
                messagebox.showerror("Error", mensaje)
    
    def nueva_base_datos(self):
        """Crea una nueva base de datos"""
        archivo = filedialog.asksaveasfilename(
            title="Nueva Base de Datos",
            defaultextension=".db",
            filetypes=[("Base de datos SQLite", "*.db"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            exito, mensaje = self.controller.cambiar_base_datos(archivo)
            if exito:
                messagebox.showinfo("Éxito", "Nueva base de datos creada correctamente")
                self.db_actual_label.config(text=archivo)
                self.refresh_all_data()
            else:
                messagebox.showerror("Error", mensaje)
    
    def configurar_onedrive(self):
        """Configura la base de datos en OneDrive automáticamente"""
        onedrive_path = Settings.detect_onedrive_path()
        
        if not onedrive_path:
            messagebox.showerror(
                "Error", 
                "No se pudo detectar OneDrive en este equipo.\n\n"
                "Asegúrate de que OneDrive esté instalado y sincronizado.\n"
                "Usa 'Seleccionar Ubicación Manual' si lo prefieres."
            )
            return
        
        # Crear carpeta para el sistema en OneDrive
        app_folder = os.path.join(onedrive_path, "Sistema_Inventarios")
        
        try:
            os.makedirs(app_folder, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la carpeta en OneDrive:\n{str(e)}")
            return
        
        # Ruta de la nueva BD en OneDrive
        nueva_db_path = os.path.join(app_folder, "inventarios.db")
        
        # Verificar si ya existe una BD en OneDrive
        if os.path.exists(nueva_db_path):
            respuesta = messagebox.askyesno(
                "Base de Datos Existente",
                f"Se encontró una base de datos existente en OneDrive:\n{nueva_db_path}\n\n"
                "¿Deseas usar esta base de datos?\n\n"
                "SÍ = Usar la BD existente en OneDrive\n"
                "NO = Copiar la BD actual a OneDrive (sobrescribirá la existente)"
            )
            
            if not respuesta:
                # Copiar BD actual a OneDrive
                try:
                    import shutil
                    shutil.copy2(self.controller.db.db_path, nueva_db_path)
                    messagebox.showinfo("Éxito", "Base de datos copiada a OneDrive correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo copiar la base de datos:\n{str(e)}")
                    return
        else:
            # Preguntar si copiar la BD actual
            if os.path.exists(self.controller.db.db_path):
                copiar = messagebox.askyesno(
                    "Copiar Base de Datos",
                    "¿Deseas copiar tu base de datos actual a OneDrive?\n\n"
                    "SÍ = Copiar datos existentes\n"
                    "NO = Crear nueva base de datos vacía en OneDrive"
                )
                
                if copiar:
                    try:
                        import shutil
                        shutil.copy2(self.controller.db.db_path, nueva_db_path)
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo copiar la base de datos:\n{str(e)}")
                        return
        
        # Cambiar a la nueva ruta
        exito, mensaje = self.controller.cambiar_base_datos(nueva_db_path)
        
        if exito:
            Settings.set_db_path(nueva_db_path)
            Settings.set_cloud_storage(True)
            
            messagebox.showinfo(
                "¡Éxito!", 
                f"Base de datos configurada en OneDrive correctamente.\n\n"
                f"Ruta: {nueva_db_path}\n\n"
                f"Ahora puedes instalar el programa en otras computadoras\n"
                f"y usar esta misma ruta para compartir los datos."
            )
            
            # Actualizar interfaz
            self.db_actual_label.config(text=nueva_db_path)
            self.actualizar_estado_cloud()
            self.refresh_all_data()
        else:
            messagebox.showerror("Error", mensaje)
    
    def seleccionar_ubicacion_manual(self):
        """Permite seleccionar manualmente la ubicación de la BD"""
        # Preguntar si quiere crear nueva o seleccionar existente
        opciones = messagebox.askyesnocancel(
            "Seleccionar Base de Datos",
            "¿Qué deseas hacer?\n\n"
            "SÍ = Seleccionar base de datos existente\n"
            "NO = Crear nueva base de datos\n"
            "CANCELAR = Volver"
        )
        
        if opciones is None:  # Cancelar
            return
        elif opciones:  # Seleccionar existente
            archivo = filedialog.askopenfilename(
                title="Seleccionar Base de Datos",
                filetypes=[("Base de datos SQLite", "*.db"), ("Todos los archivos", "*.*")],
                initialdir=Settings.detect_onedrive_path() or os.path.expanduser("~")
            )
        else:  # Crear nueva
            archivo = filedialog.asksaveasfilename(
                title="Nueva Base de Datos",
                defaultextension=".db",
                initialfile="inventarios.db",
                filetypes=[("Base de datos SQLite", "*.db"), ("Todos los archivos", "*.*")],
                initialdir=Settings.detect_onedrive_path() or os.path.expanduser("~")
            )
        
        if archivo:
            # Si la nueva ubicación no tiene BD, copiar la actual
            if not os.path.exists(archivo):
                copiar = messagebox.askyesno(
                    "Copiar Datos",
                    "¿Deseas copiar tu base de datos actual a esta ubicación?\n\n"
                    "SÍ = Copiar datos existentes\n"
                    "NO = Crear base de datos vacía"
                )
                
                if copiar and os.path.exists(self.controller.db.db_path):
                    try:
                        import shutil
                        shutil.copy2(self.controller.db.db_path, archivo)
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo copiar:\n{str(e)}")
                        return
            
            # Cambiar a la nueva ubicación
            exito, mensaje = self.controller.cambiar_base_datos(archivo)
            
            if exito:
                Settings.set_db_path(archivo)
                
                # Detectar si está en la nube
                es_nube = "onedrive" in archivo.lower() or "google drive" in archivo.lower() or "dropbox" in archivo.lower()
                Settings.set_cloud_storage(es_nube)
                
                messagebox.showinfo("Éxito", f"Base de datos configurada correctamente:\n{archivo}")
                
                # Actualizar interfaz
                self.db_actual_label.config(text=archivo)
                self.actualizar_estado_cloud()
                self.refresh_all_data()
            else:
                messagebox.showerror("Error", mensaje)
    
    def actualizar_estado_cloud(self):
        """Actualiza el label de estado de la nube"""
        current_db = Settings.get_db_path()
        is_cloud = Settings.is_using_cloud_storage()
        
        if is_cloud:
            estado_text = f"🌐 Usando almacenamiento en la nube\nRuta: {current_db}"
            estado_style = "success"
        else:
            estado_text = f"💻 Usando almacenamiento local\nRuta: {current_db}"
            estado_style = "secondary"
        
        if hasattr(self, 'estado_cloud_label'):
            self.estado_cloud_label.config(text=estado_text, bootstyle=estado_style)
    
    def exportar_reporte_general(self):
        """Exporta el reporte general completo a Excel"""
        from datetime import datetime
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        archivo = filedialog.asksaveasfilename(
            title="Exportar Reporte General",
            defaultextension=".xlsx",
            initialfile=f"Reporte_General_{fecha_actual}.xlsx",
            filetypes=[("Archivo Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                import pandas as pd
                from datetime import datetime
                
                # Obtener resumen completo del inventario (ahora con cálculos correctos)
                resumen = self.controller.obtener_resumen_inventario()
                
                # Crear DataFrame de resumen
                resumen_data = {
                    'Concepto': ['Total Compras', 'Total Ventas', 'Ganancia Bruta', 'Valor Inventario', 'Saldo en Banco'],
                    'Monto (Q)': [
                        f"Q {resumen['total_compras']:,.2f}",
                        f"Q {resumen['total_ventas']:,.2f}",
                        f"Q {resumen['ganancia_bruta']:,.2f}",
                        f"Q {resumen['valor_inventario']:,.2f}",
                        f"Q {resumen['saldo_banco']:,.2f}"
                    ]
                }
                df_resumen = pd.DataFrame(resumen_data)
                
                # Productos con stock bajo (solo activos)
                productos = self.controller.obtener_productos()
                productos_bajo = [p for p in productos if p['stock_actual'] <= 5 and p.get('activo', 1) == 1]
                if productos_bajo:
                    # Agregar columna de estado
                    for p in productos_bajo:
                        p['estado'] = 'ACTIVO' if p.get('activo', 1) == 1 else 'INACTIVO'
                df_stock_bajo = pd.DataFrame(productos_bajo) if productos_bajo else pd.DataFrame()
                
                # Exportar a Excel con múltiples hojas
                with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                    df_resumen.to_excel(writer, sheet_name='Resumen General', index=False)
                    if not df_stock_bajo.empty:
                        df_stock_bajo.to_excel(writer, sheet_name='Stock Bajo', index=False)
                
                messagebox.showinfo("Éxito", f"Reporte general exportado a:\n{archivo}")
            except ImportError:
                messagebox.showerror("Error", "Se requiere instalar 'pandas' y 'openpyxl' para exportar a Excel.\nEjecute: pip install pandas openpyxl")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el reporte: {str(e)}")
    
    def exportar_productos_completo(self):
        """Exporta todos los productos con todos sus detalles a Excel"""
        from datetime import datetime
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        archivo = filedialog.asksaveasfilename(
            title="Exportar Productos Completo",
            defaultextension=".xlsx",
            initialfile=f"Productos_Completo_{fecha_actual}.xlsx",
            filetypes=[("Archivo Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                import pandas as pd
                
                # Obtener todos los productos
                productos = self.controller.obtener_productos()
                
                if not productos:
                    messagebox.showwarning("Aviso", "No hay productos registrados para exportar.")
                    return
                
                # Preparar datos para exportar
                datos_exportar = []
                for p in productos:
                    datos_exportar.append({
                        'ID': p.get('id', ''),
                        'Código SKU': p.get('codigo', ''),
                        'Nombre': p.get('nombre', ''),
                        'Categoría': p.get('categoria', ''),
                        'Marca': p.get('marca', ''),
                        'Color': p.get('color', ''),
                        'Tamaño': p.get('tamaño', ''),
                        'Dibujo': p.get('dibujo', ''),
                        'Código Color': p.get('cod_color', ''),
                        'Stock Actual': p.get('stock_actual', 0),
                        'Precio Compra (Q)': f"{p.get('precio_compra', 0):.2f}",
                        'Precio Venta (Q)': f"{p.get('precio_venta', 0):.2f}",
                        '% Ganancia': f"{p.get('porcentaje_ganancia', 0):.2f}",
                        'Estado': 'ACTIVO' if p.get('activo', 1) == 1 else 'INACTIVO'
                    })
                
                # Crear DataFrame
                df = pd.DataFrame(datos_exportar)
                
                # Exportar a Excel
                with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Productos', index=False)
                    
                    # Ajustar ancho de columnas
                    worksheet = writer.sheets['Productos']
                    for idx, col in enumerate(df.columns, 1):
                        max_length = max(
                            df[col].astype(str).apply(len).max(),
                            len(col)
                        )
                        worksheet.column_dimensions[chr(64 + idx)].width = min(max_length + 2, 50)
                
                messagebox.showinfo("Éxito", f"Productos exportados exitosamente a:\n{archivo}\n\nTotal de productos: {len(productos)}")
            except ImportError:
                messagebox.showerror("Error", "Se requiere instalar 'pandas' y 'openpyxl' para exportar a Excel.\nEjecute: pip install pandas openpyxl")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar los productos: {str(e)}")
    
    def exportar_reporte_compras(self):
        """Exporta todas las compras a Excel con filtro de fechas"""
        from datetime import datetime
        
        # Mostrar diálogo de selección de fechas
        rango = self.seleccionar_rango_fechas("Filtrar Compras por Fecha")
        
        if not rango['aceptado']:
            return  # Usuario canceló
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        archivo = filedialog.asksaveasfilename(
            title="Exportar Reporte de Compras",
            defaultextension=".xlsx",
            initialfile=f"Reporte_Compras_{fecha_actual}.xlsx",
            filetypes=[("Archivo Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                import pandas as pd
                from datetime import datetime as dt
                
                compras = self.controller.obtener_compras()
                
                if not compras:
                    messagebox.showwarning("Aviso", "No hay compras registradas para exportar.")
                    return
                
                # Convertir fechas del rango
                fecha_inicio = dt.strptime(rango['fecha_inicio'], '%d/%m/%Y')
                fecha_fin = dt.strptime(rango['fecha_fin'], '%d/%m/%Y')
                
                # Filtrar compras por rango de fechas
                compras_filtradas = []
                for compra in compras:
                    try:
                        # Intentar varios formatos de fecha
                        fecha_str = compra['fecha']
                        try:
                            fecha_compra = dt.strptime(fecha_str, '%d/%m/%Y %H:%M:%S')
                        except:
                            try:
                                fecha_compra = dt.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                            except:
                                fecha_compra = dt.strptime(fecha_str.split()[0], '%d/%m/%Y')
                        
                        if fecha_inicio <= fecha_compra <= fecha_fin:
                            compras_filtradas.append(compra)
                    except:
                        pass  # Ignorar fechas con formato incorrecto
                
                if not compras_filtradas:
                    messagebox.showwarning("Aviso", f"No hay compras en el rango seleccionado:\n{rango['fecha_inicio']} - {rango['fecha_fin']}")
                    return
                
                # Preparar datos para exportación
                datos = []
                total_general = 0
                for compra in compras_filtradas:
                    # Determinar estado de vencimiento
                    estado_vencimiento = 'N/A'
                    fecha_vencimiento_texto = 'N/A'
                    
                    if compra.get('es_perecedero') == 1 and compra.get('fecha_vencimiento'):
                        fecha_vencimiento_texto = compra['fecha_vencimiento']
                        try:
                            fecha_venc = dt.strptime(compra['fecha_vencimiento'], '%d/%m/%Y')
                            hoy = dt.now()
                            dias_restantes = (fecha_venc - hoy).days
                            
                            if dias_restantes < 0:
                                estado_vencimiento = f'VENCIDO (hace {abs(dias_restantes)} días)'
                            elif dias_restantes <= 7:
                                estado_vencimiento = f'CRITICO ({dias_restantes} días)'
                            elif dias_restantes <= 30:
                                estado_vencimiento = f'ADVERTENCIA ({dias_restantes} días)'
                            else:
                                estado_vencimiento = f'OK ({dias_restantes} días)'
                        except:
                            estado_vencimiento = 'Error en fecha'
                    
                    # Formatear fecha para mostrar
                    fecha_mostrar = compra['fecha']
                    try:
                        fecha_obj = dt.strptime(compra['fecha'], '%d/%m/%Y %H:%M:%S')
                        fecha_mostrar = fecha_obj.strftime('%d/%m/%Y')
                    except:
                        try:
                            fecha_obj = dt.strptime(compra['fecha'], '%Y-%m-%d %H:%M:%S')
                            fecha_mostrar = fecha_obj.strftime('%d/%m/%Y')
                        except:
                            fecha_mostrar = compra['fecha'].split()[0] if ' ' in compra['fecha'] else compra['fecha']
                    
                    datos.append({
                        'ID': compra['id'],
                        'Fecha': fecha_mostrar,
                        'Producto': compra.get('producto_nombre', 'N/A'),
                        'Proveedor': compra.get('proveedor_nombre', 'N/A'),
                        'Cantidad': compra['cantidad'],
                        'Precio Unitario': f"Q {compra['precio_unitario']:,.2f}",
                        'Total': f"Q {compra['total']:,.2f}",
                        'Vencimiento': fecha_vencimiento_texto,
                        'Estado': estado_vencimiento
                    })
                    total_general += compra['total']
                
                df = pd.DataFrame(datos)
                
                # Agregar fila de total
                df.loc[len(df)] = ['', '', '', '', '', 'TOTAL:', f"Q {total_general:,.2f}", '', '']
                
                df.to_excel(archivo, index=False, sheet_name='Compras')
                
                messagebox.showinfo("Éxito", f"Reporte de compras exportado:\n{archivo}\n\n{len(compras_filtradas)} compras encontradas\nTotal: Q {total_general:,.2f}")
            except ImportError:
                messagebox.showerror("Error", "Se requiere instalar 'pandas' y 'openpyxl' para exportar a Excel.\nEjecute: pip install pandas openpyxl")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el reporte: {str(e)}")
    
    def exportar_reporte_ventas(self):
        """Exporta todas las ventas a Excel con filtro de fechas"""
        from datetime import datetime
        
        # Mostrar diálogo de selección de fechas
        rango = self.seleccionar_rango_fechas("Filtrar Ventas por Fecha")
        
        if not rango['aceptado']:
            return  # Usuario canceló
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        archivo = filedialog.asksaveasfilename(
            title="Exportar Reporte de Ventas",
            defaultextension=".xlsx",
            initialfile=f"Reporte_Ventas_{fecha_actual}.xlsx",
            filetypes=[("Archivo Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                import pandas as pd
                from datetime import datetime as dt
                
                ventas = self.controller.obtener_ventas()
                
                if not ventas:
                    messagebox.showwarning("Aviso", "No hay ventas registradas para exportar.")
                    return
                
                # Convertir fechas del rango
                fecha_inicio = dt.strptime(rango['fecha_inicio'], '%d/%m/%Y')
                fecha_fin = dt.strptime(rango['fecha_fin'], '%d/%m/%Y')
                
                # Filtrar ventas por rango de fechas
                ventas_filtradas = []
                for venta in ventas:
                    try:
                        # Intentar varios formatos de fecha
                        fecha_str = venta['fecha']
                        try:
                            fecha_venta = dt.strptime(fecha_str, '%d/%m/%Y %H:%M:%S')
                        except:
                            try:
                                fecha_venta = dt.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                            except:
                                fecha_venta = dt.strptime(fecha_str.split()[0], '%d/%m/%Y')
                        
                        if fecha_inicio <= fecha_venta <= fecha_fin:
                            ventas_filtradas.append(venta)
                    except:
                        pass  # Ignorar fechas con formato incorrecto
                
                if not ventas_filtradas:
                    messagebox.showwarning("Aviso", f"No hay ventas en el rango seleccionado:\n{rango['fecha_inicio']} - {rango['fecha_fin']}")
                    return
                
                # Preparar datos para exportación
                datos = []
                total_general = 0
                for venta in ventas_filtradas:
                    # Formatear fecha para mostrar
                    fecha_mostrar = venta['fecha']
                    try:
                        fecha_obj = dt.strptime(venta['fecha'], '%d/%m/%Y %H:%M:%S')
                        fecha_mostrar = fecha_obj.strftime('%d/%m/%Y')
                    except:
                        try:
                            fecha_obj = dt.strptime(venta['fecha'], '%Y-%m-%d %H:%M:%S')
                            fecha_mostrar = fecha_obj.strftime('%d/%m/%Y')
                        except:
                            fecha_mostrar = venta['fecha'].split()[0] if ' ' in venta['fecha'] else venta['fecha']
                    
                    datos.append({
                        'ID': venta['id'],
                        'Fecha': fecha_mostrar,
                        'Producto': venta.get('producto_nombre', 'N/A'),
                        'Cliente': venta.get('cliente_nombre', 'N/A'),
                        'Cantidad': venta['cantidad'],
                        'Precio Unitario': f"Q {venta['precio_unitario']:,.2f}",
                        'Total': f"Q {venta['total']:,.2f}"
                    })
                    total_general += venta['total']
                
                df = pd.DataFrame(datos)
                
                # Agregar fila de total
                df.loc[len(df)] = ['', '', '', '', '', 'TOTAL:', f"Q {total_general:,.2f}"]
                
                df.to_excel(archivo, index=False, sheet_name='Ventas')
                
                messagebox.showinfo("Éxito", f"Reporte de ventas exportado:\n{archivo}\n\n{len(ventas_filtradas)} ventas encontradas\nTotal: Q {total_general:,.2f}")
            except ImportError:
                messagebox.showerror("Error", "Se requiere instalar 'pandas' y 'openpyxl' para exportar a Excel.\nEjecute: pip install pandas openpyxl")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el reporte: {str(e)}")
    
    def exportar_reporte_caja(self):
        """Exporta todos los movimientos de caja a Excel con filtro de fechas"""
        from datetime import datetime
        
        # Mostrar diálogo de selección de fechas
        rango = self.seleccionar_rango_fechas("Filtrar Movimientos de Caja por Fecha")
        
        if not rango['aceptado']:
            return  # Usuario canceló
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        archivo = filedialog.asksaveasfilename(
            title="Exportar Reporte de Caja",
            defaultextension=".xlsx",
            initialfile=f"Reporte_Movimientos_Caja_{fecha_actual}.xlsx",
            filetypes=[("Archivo Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                import pandas as pd
                from datetime import datetime as dt
                
                movimientos = self.controller.obtener_movimientos_caja()
                
                if not movimientos:
                    messagebox.showwarning("Aviso", "No hay movimientos de caja registrados para exportar.")
                    return
                
                # Convertir fechas del rango
                fecha_inicio = dt.strptime(rango['fecha_inicio'], '%d/%m/%Y')
                fecha_fin = dt.strptime(rango['fecha_fin'], '%d/%m/%Y')
                
                # Filtrar movimientos por rango de fechas
                movimientos_filtrados = []
                for mov in movimientos:
                    try:
                        # Intentar varios formatos de fecha
                        fecha_str = mov['fecha']
                        try:
                            fecha_mov = dt.strptime(fecha_str, '%d/%m/%Y %H:%M:%S')
                        except:
                            try:
                                fecha_mov = dt.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                            except:
                                fecha_mov = dt.strptime(fecha_str.split()[0], '%d/%m/%Y')
                        
                        if fecha_inicio <= fecha_mov <= fecha_fin:
                            movimientos_filtrados.append(mov)
                    except:
                        pass  # Ignorar fechas con formato incorrecto
                
                if not movimientos_filtrados:
                    messagebox.showwarning("Aviso", f"No hay movimientos en el rango seleccionado:\n{rango['fecha_inicio']} - {rango['fecha_fin']}")
                    return
                
                # Preparar datos para exportación
                datos = []
                total_ingresos = 0
                total_egresos = 0
                
                for mov in movimientos_filtrados:
                    # Formatear fecha para mostrar
                    fecha_mostrar = mov['fecha']
                    try:
                        fecha_obj = dt.strptime(mov['fecha'], '%d/%m/%Y %H:%M:%S')
                        fecha_mostrar = fecha_obj.strftime('%d/%m/%Y')
                    except:
                        try:
                            fecha_obj = dt.strptime(mov['fecha'], '%Y-%m-%d %H:%M:%S')
                            fecha_mostrar = fecha_obj.strftime('%d/%m/%Y')
                        except:
                            fecha_mostrar = mov['fecha'].split()[0] if ' ' in mov['fecha'] else mov['fecha']
                    
                    datos.append({
                        'ID': mov['id'],
                        'Fecha': fecha_mostrar,
                        'Tipo': mov['tipo'],
                        'Categoría': mov.get('categoria', 'N/A'),
                        'Concepto': mov['concepto'],
                        'Monto': f"Q {mov['monto']:,.2f}"
                    })
                    
                    if mov['tipo'].upper() == 'INGRESO':
                        total_ingresos += mov['monto']
                    else:
                        total_egresos += mov['monto']
                
                df = pd.DataFrame(datos)
                
                # Agregar filas de totales (6 columnas: ID, Fecha, Tipo, Categoría, Concepto, Monto)
                df.loc[len(df)] = ['', '', '', '', '', '']
                df.loc[len(df)] = ['', '', '', '', 'Total Ingresos:', f"Q {total_ingresos:,.2f}"]
                df.loc[len(df)] = ['', '', '', '', 'Total Egresos:', f"Q {total_egresos:,.2f}"]
                df.loc[len(df)] = ['', '', '', '', 'Saldo:', f"Q {(total_ingresos - total_egresos):,.2f}"]
                
                df.to_excel(archivo, index=False, sheet_name='Movimientos Caja')
                
                messagebox.showinfo("Éxito", f"Reporte de caja exportado:\n{archivo}\n\n{len(movimientos_filtrados)} movimientos encontrados\nIngresos: Q {total_ingresos:,.2f}\nEgresos: Q {total_egresos:,.2f}\nSaldo: Q {(total_ingresos - total_egresos):,.2f}")
            except ImportError:
                messagebox.showerror("Error", "Se requiere instalar 'pandas' y 'openpyxl' para exportar a Excel.\nEjecute: pip install pandas openpyxl")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el reporte: {str(e)}")
    
    def exportar_resumen(self):
        """Exporta un resumen completo a un archivo de texto"""
        archivo = filedialog.asksaveasfilename(
            title="Exportar Resumen",
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                resumen = self.controller.exportar_resumen()
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(resumen)
                messagebox.showinfo("Éxito", f"Resumen exportado a: {archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el resumen: {str(e)}")
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
