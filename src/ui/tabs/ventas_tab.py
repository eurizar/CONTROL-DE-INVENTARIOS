"""
Tab de Ventas - Sistema de Control de Inventarios

Gestiona el proceso de ventas con carrito de compras.
"""

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap import DateEntry
from datetime import datetime
import os


class VentasTab:
    """Tab para gestión de ventas con carrito."""
    
    def __init__(self, parent_frame, controller, main_window):
        self.frame = parent_frame
        self.controller = controller
        self.main_window = main_window
        
        # Inicializar variables
        self.setup_variables()
        
        # Crear interfaz
        self.create_ui()
        
    def setup_variables(self):
        """Inicializa las variables del tab."""
        # Variables del cliente
        self.venta_cliente_id = None
        self.venta_cliente_busqueda = tk.StringVar()
        self.venta_cliente_nit = tk.StringVar()
        self.venta_cliente_direccion = tk.StringVar()
        self.venta_cliente_telefono = tk.StringVar()
        
        # Variables del producto
        self.venta_producto_id = None
        self.venta_producto_busqueda = tk.StringVar()
        self.venta_cantidad = tk.IntVar(value=1)
        self.venta_precio = tk.DoubleVar()
        self.venta_precio_original = tk.DoubleVar()
        
        # Variables de descuento
        self.aplicar_descuento = tk.BooleanVar(value=False)
        self.venta_descuento = tk.DoubleVar(value=0)
        
        # Carrito de ventas
        self.carrito_ventas = []
    
    def create_ui(self):
        """Crea la interfaz del tab de ventas."""
        # Contenedor principal
        main_container = tb.Frame(self.frame)
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Sección superior: Formulario y Carrito
        top_section = tb.Frame(main_container)
        top_section.pack(fill='both', expand=False, pady=(0, 10))
        
        self.crear_formulario(top_section)
        self.crear_carrito(top_section)
        
        # Sección inferior: Historial
        self.crear_historial(main_container)
    
    def crear_formulario(self, parent):
        """Crea el formulario de productos."""
        form_frame = tb.Labelframe(
            parent,
            text="💵 Agregar Productos al Carrito",
            padding=15,
            bootstyle="warning"
        )
        form_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Fila 0 - Cliente y Fecha
        tb.Label(form_frame, text="Cliente: *", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky='w', padx=5, pady=5
        )
        
        cli_search_frame = tb.Frame(form_frame)
        cli_search_frame.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        
        self.venta_cliente_entry = tb.Entry(
            cli_search_frame,
            textvariable=self.venta_cliente_busqueda,
            width=25,
            font=('Segoe UI', 10)
        )
        self.venta_cliente_entry.pack(side='left', fill='x', expand=True)
        self.venta_cliente_entry.bind('<KeyRelease>', self.autocompletar_cliente)
        
        tb.Button(
            cli_search_frame,
            text="🔍",
            command=self.buscar_cliente,
            bootstyle="info-outline",
            width=3
        ).pack(side='left', padx=2)
        
        self.venta_cliente_label = tb.Label(
            cli_search_frame,
            text="",
            font=('Segoe UI', 11),
            bootstyle="success"
        )
        self.venta_cliente_label.pack(side='left', padx=5)
        
        tb.Label(form_frame, text="Fecha: *", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=3, sticky='w', padx=5, pady=5
        )
        self.venta_fecha_cal = DateEntry(
            form_frame,
            dateformat='%d/%m/%Y',
            width=14,
            bootstyle="warning"
        )
        self.venta_fecha_cal.grid(row=0, column=4, padx=5, pady=5, sticky='w')
        
        # Fila 1 - NIT y Dirección
        tb.Label(form_frame, text="NIT o DPI (CF): *", font=('Segoe UI', 10, 'bold')).grid(
            row=1, column=0, sticky='w', padx=5, pady=5
        )
        self.venta_cliente_nit_entry = tb.Entry(
            form_frame,
            textvariable=self.venta_cliente_nit,
            width=22,
            font=('Segoe UI', 10)
        )
        self.venta_cliente_nit_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        
        tb.Label(form_frame, text="Dirección:", font=('Segoe UI', 10, 'bold')).grid(
            row=1, column=3, sticky='w', padx=5, pady=5
        )
        self.venta_cliente_direccion_entry = tb.Entry(
            form_frame,
            textvariable=self.venta_cliente_direccion,
            width=28,
            font=('Segoe UI', 10)
        )
        self.venta_cliente_direccion_entry.grid(row=1, column=4, padx=5, pady=5, sticky='w')
        
        # Fila 2 - Teléfono y guardar cliente
        tb.Label(form_frame, text="Teléfono:", font=('Segoe UI', 10, 'bold')).grid(
            row=2, column=0, sticky='w', padx=5, pady=5
        )
        self.venta_cliente_telefono_entry = tb.Entry(
            form_frame,
            textvariable=self.venta_cliente_telefono,
            width=20,
            font=('Segoe UI', 10)
        )
        self.venta_cliente_telefono_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        
        tb.Button(
            form_frame,
            text="💾 Guardar Cliente",
            command=self.guardar_cliente_rapido,
            bootstyle="info-outline",
            width=19
        ).grid(row=2, column=3, columnspan=2, padx=5, pady=5, sticky='w')
        
        # Separador
        tb.Separator(form_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=5, sticky='ew', pady=10
        )
        
        # Fila 4 - Producto
        tb.Label(form_frame, text="Producto: *", font=('Segoe UI', 10, 'bold')).grid(
            row=4, column=0, sticky='w', padx=5, pady=5
        )
        
        prod_search_frame = tb.Frame(form_frame)
        prod_search_frame.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        
        self.venta_producto_entry = tb.Entry(
            prod_search_frame,
            textvariable=self.venta_producto_busqueda,
            width=38,
            font=('Segoe UI', 10)
        )
        self.venta_producto_entry.pack(side='left', fill='x', expand=True)
        self.venta_producto_entry.bind('<KeyRelease>', self.autocompletar_producto)
        
        tb.Button(
            prod_search_frame,
            text="🔍",
            command=self.buscar_producto,
            bootstyle="info-outline",
            width=3
        ).pack(side='left', padx=2)
        
        self.venta_producto_label = tb.Label(
            prod_search_frame,
            text="",
            font=('Segoe UI', 11),
            bootstyle="success"
        )
        self.venta_producto_label.pack(side='left', padx=5)
        
        # Fila 5 - Cantidad / Precio
        tb.Label(form_frame, text="Cant.: *", font=('Segoe UI', 10, 'bold')).grid(
            row=5, column=0, sticky='w', padx=5, pady=5
        )
        self.venta_cantidad_entry = tb.Entry(
            form_frame,
            textvariable=self.venta_cantidad,
            width=12,
            font=('Segoe UI', 10)
        )
        self.venta_cantidad_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        
        tb.Label(form_frame, text="Precio (Q): *", font=('Segoe UI', 10, 'bold')).grid(
            row=5, column=2, sticky='w', padx=5, pady=5
        )
        self.venta_precio_entry = tb.Entry(
            form_frame,
            textvariable=self.venta_precio,
            width=14,
            font=('Segoe UI', 10),
            state='readonly'
        )
        self.venta_precio_entry.grid(row=5, column=3, padx=5, pady=5, sticky='w')
        self.venta_precio.trace_add('write', self.on_precio_change)
        
        # Fila 6 - Descuento
        self.descuento_check = tb.Checkbutton(
            form_frame,
            text="💰 Aplicar Descuento",
            variable=self.aplicar_descuento,
            command=self.toggle_descuento,
            bootstyle="warning-round-toggle"
        )
        self.descuento_check.grid(row=6, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        descuento_frame = tb.Frame(form_frame)
        descuento_frame.grid(row=6, column=2, columnspan=3, sticky='w', padx=5, pady=5)
        
        tb.Label(descuento_frame, text="Desc %:", font=('Segoe UI', 10)).pack(side='left', padx=(0, 5))
        self.venta_descuento_entry = tb.Entry(
            descuento_frame,
            textvariable=self.venta_descuento,
            width=10,
            font=('Segoe UI', 10),
            state='disabled'
        )
        self.venta_descuento_entry.pack(side='left', padx=(0, 5))
        self.venta_descuento_entry.bind('<KeyRelease>', self.calcular_precio_con_descuento)
        
        tb.Label(descuento_frame, text="→", font=('Segoe UI', 10)).pack(side='left', padx=5)
        tb.Label(descuento_frame, text="Precio Final:", font=('Segoe UI', 10, 'bold')).pack(
            side='left', padx=(0, 5)
        )
        self.precio_final_label = tb.Label(
            descuento_frame,
            text="Q 0.00",
            font=('Segoe UI', 10, 'bold'),
            bootstyle="success"
        )
        self.precio_final_label.pack(side='left')
        
        # Stock disponible (fila 7)
        stock_frame = tb.Frame(form_frame)
        stock_frame.grid(row=7, column=0, columnspan=5, sticky='ew', padx=5, pady=8)
        
        self.stock_label = tb.Label(
            stock_frame,
            text="📦 Stock Disponible: 0",
            font=('Segoe UI', 11, 'bold'),
            bootstyle="info"
        )
        self.stock_label.pack(anchor='w')
        
        # Espaciador
        tb.Label(form_frame, text="").grid(row=8, column=0, columnspan=5, pady=5)
        
        # Botones (fila 9)
        botones_frame = tb.Frame(form_frame)
        botones_frame.grid(row=9, column=0, columnspan=5, pady=(5, 0))
        
        tb.Button(
            botones_frame,
            text="🛒 Agregar al Carrito",
            command=self.agregar_al_carrito,
            bootstyle="success",
            width=22
        ).pack(side='left', padx=5)
        
        tb.Button(
            botones_frame,
            text="🧹 Limpiar",
            command=self.limpiar_formulario_carrito,
            bootstyle="secondary-outline",
            width=18
        ).pack(side='left', padx=5)
        
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        
    def crear_carrito(self, parent):
        """Crea el carrito de compras."""
        carrito_frame = tb.Labelframe(
            parent,
            text="🛒 Carrito de Compras",
            padding=10,
            bootstyle="success"
        )
        carrito_frame.pack(side='left', fill='both', expand=True)
        
        # Tabla del carrito
        carrito_tree_frame = tb.Frame(carrito_frame)
        carrito_tree_frame.pack(fill='both', expand=True)
        
        carrito_cols = ('Producto', 'Cantidad', 'P. Original', 'Desc %', 'P. Final', 'Subtotal')
        self.carrito_tree = tb.Treeview(
            carrito_tree_frame,
            columns=carrito_cols,
            show='headings',
            height=7
        )
        
        # Configurar encabezados y anchos
        self.carrito_tree.heading('Producto', text='Producto')
        self.carrito_tree.heading('Cantidad', text='Cant.')
        self.carrito_tree.heading('P. Original', text='P. Orig.')
        self.carrito_tree.heading('Desc %', text='Desc %')
        self.carrito_tree.heading('P. Final', text='P. Final')
        self.carrito_tree.heading('Subtotal', text='Subtotal')
        
        self.carrito_tree.column('Producto', width=120, minwidth=80, anchor='w', stretch=True)
        self.carrito_tree.column('Cantidad', width=55, minwidth=50, anchor='center', stretch=False)
        self.carrito_tree.column('P. Original', width=75, minwidth=70, anchor='e', stretch=False)
        self.carrito_tree.column('Desc %', width=60, minwidth=55, anchor='center', stretch=False)
        self.carrito_tree.column('P. Final', width=75, minwidth=70, anchor='e', stretch=False)
        self.carrito_tree.column('Subtotal', width=85, minwidth=80, anchor='e', stretch=False)
        
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
        
    def crear_historial(self, parent):
        """Crea el historial de ventas."""
        list_frame = tb.Labelframe(
            parent,
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
        self.venta_search.bind('<KeyRelease>', lambda e: self.refresh())
        
        tb.Label(search_frame, text="Busca por: Cliente, NIT/DPI, Ref. No. o Fecha",
                font=('Segoe UI', 8, 'italic'), bootstyle="secondary").pack(side='left', padx=10)
        
        # Treeview con scrollbars
        tree_frame = tb.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('Ref. No.', 'NIT/DPI', 'Cliente', 'Productos', 'Total', 'Fecha', 'Estado')
        self.ventas_tree = tb.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=8
        )
        
        column_widths = {'Ref. No.': 100, 'NIT/DPI': 100, 'Cliente': 180, 'Productos': 150, 
                        'Total': 100, 'Fecha': 120, 'Estado': 100}
        for col in columns:
            self.ventas_tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.ventas_tree.column(col, width=column_widths[col], 
                                   anchor='center' if col not in ['Cliente', 'Productos'] else 'w')
        
        scrollbar_y = tb.Scrollbar(tree_frame, orient='vertical', 
                                  command=self.ventas_tree.yview, bootstyle="info-round")
        scrollbar_x = tb.Scrollbar(tree_frame, orient='horizontal', 
                                  command=self.ventas_tree.xview, bootstyle="info-round")
        self.ventas_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.ventas_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Colores alternados
        self.ventas_tree.tag_configure('evenrow', background='#f0f0f0')
        self.ventas_tree.tag_configure('oddrow', background='#ffffff')
        
        # Tags hover
        self.ventas_tree.tag_configure('evenrow_hover', background='#e0e0e0')
        self.ventas_tree.tag_configure('oddrow_hover', background='#f0f0f0')
        
        # Variables para controlar hover
        self.last_hovered_item = None
        self.original_tag = None
        
        # Bindings
        self.ventas_tree.bind('<Double-Button-1>', self.ver_detalle_venta)
        self.ventas_tree.bind('<Button-3>', self.mostrar_menu_contextual_venta)
        self.ventas_tree.bind('<Motion>', self.on_tree_motion)
        self.ventas_tree.bind('<Leave>', self.on_tree_leave)
        
    # ===== MÉTODOS DE AUTOCOMPLETADO =====
    
    def autocompletar_cliente(self, event):
        """Autocompletado para cliente."""
        texto = self.venta_cliente_busqueda.get()
        
        # Destruir listbox anterior
        if hasattr(self, 'cliente_listbox_window') and self.cliente_listbox_window.winfo_exists():
            self.cliente_listbox_window.destroy()
        
        if len(texto) < 2:
            return
        
        # Buscar clientes
        clientes = self.controller.buscar_cliente(texto)
        if not clientes:
            return
        
        # Obtener posición del entry
        self.venta_cliente_entry.update_idletasks()
        self.main_window.root.update_idletasks()
        
        x = self.venta_cliente_entry.winfo_rootx()
        y = self.venta_cliente_entry.winfo_rooty()
        height = self.venta_cliente_entry.winfo_height()
        width = self.venta_cliente_entry.winfo_width()
        
        if width <= 1 or height <= 1:
            width = 350
            height = 80
        
        # Crear ventana de autocompletado
        self.cliente_listbox_window = tk.Toplevel(self.main_window.root)
        self.cliente_listbox_window.wm_overrideredirect(True)
        self.cliente_listbox_window.wm_attributes('-topmost', True)
        
        listbox_height = min(150, len(clientes) * 30)
        self.cliente_listbox_window.geometry(f"{width}x{listbox_height}+{x+0}+{y+height}")
        
        frame = tb.Frame(self.cliente_listbox_window, bootstyle="default")
        frame.pack(fill='both', expand=True)
        
        self.cliente_listbox = tk.Listbox(
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
        self.cliente_listbox.pack(fill='both', expand=True, padx=1, pady=1)
        
        for cli in clientes[:10]:
            self.cliente_listbox.insert('end', f"{cli['nombre']} - {cli['nit_dpi']}")
        
        def seleccionar(event=None):
            if self.cliente_listbox.curselection():
                idx = self.cliente_listbox.curselection()[0]
                self.venta_cliente_busqueda.set(clientes[idx]['nombre'])
                self.venta_cliente_nit.set(clientes[idx]['nit_dpi'])
                self.venta_cliente_direccion.set(clientes[idx]['direccion'])
                self.venta_cliente_telefono.set(clientes[idx]['telefono'])
                self.venta_cliente_id = clientes[idx]['id']
                self.venta_cliente_label.config(text="✓", bootstyle="success")
                self.cliente_listbox_window.destroy()
        
        def cerrar(event=None):
            if self.cliente_listbox_window.winfo_exists():
                self.cliente_listbox_window.destroy()
        
        self.cliente_listbox.bind('<<ListboxSelect>>', seleccionar)
        self.cliente_listbox.bind('<Return>', seleccionar)
        self.cliente_listbox.bind('<Escape>', cerrar)
        self.cliente_listbox_window.bind('<FocusOut>', cerrar)
        
        if event.keysym == 'Down':
            self.cliente_listbox.focus_set()
            self.cliente_listbox.selection_set(0)
        
    def autocompletar_producto(self, event):
        """Autocompletado para producto."""
        texto = self.venta_producto_busqueda.get()
        
        # Destruir listbox anterior
        if hasattr(self, 'producto_listbox_window') and self.producto_listbox_window.winfo_exists():
            self.producto_listbox_window.destroy()
        
        if len(texto) < 2:
            return
        
        # Buscar productos
        productos = self.controller.obtener_productos()
        productos_filtrados = [
            p for p in productos 
            if texto.lower() in p['nombre'].lower() or 
               (p.get('codigo') and texto.lower() in p['codigo'].lower()) or
               (p.get('categoria') and texto.lower() in p['categoria'].lower())
        ]
        
        if not productos_filtrados:
            return
        
        # Obtener posición del entry
        self.venta_producto_entry.update_idletasks()
        self.main_window.root.update_idletasks()
        
        x = self.venta_producto_entry.winfo_rootx()
        y = self.venta_producto_entry.winfo_rooty()
        height = self.venta_producto_entry.winfo_height()
        width = self.venta_producto_entry.winfo_width()
        
        if width <= 1 or height <= 1:
            width = 500
            height = 139
        
        # Crear ventana de autocompletado
        self.producto_listbox_window = tk.Toplevel(self.main_window.root)
        self.producto_listbox_window.wm_overrideredirect(True)
        self.producto_listbox_window.wm_attributes('-topmost', True)
        
        listbox_height = min(150, len(productos_filtrados) * 30)
        self.producto_listbox_window.geometry(f"{width}x{listbox_height}+{x+0}+{y+height}")
        
        frame = tb.Frame(self.producto_listbox_window, bootstyle="default")
        frame.pack(fill='both', expand=True)
        
        self.producto_listbox = tk.Listbox(
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
        self.producto_listbox.pack(fill='both', expand=True, padx=1, pady=1)
        
        for prod in productos_filtrados[:10]:
            codigo_txt = f"[{prod.get('codigo', 'S/C')}] " if prod.get('codigo') else ""
            self.producto_listbox.insert('end', 
                f"{codigo_txt}{prod['nombre']} - Q{prod['precio_venta']:.2f} (Stock: {prod['stock_actual']})")
        
        def seleccionar(event=None):
            if self.producto_listbox.curselection():
                idx = self.producto_listbox.curselection()[0]
                prod = productos_filtrados[idx]
                codigo_txt = f"[{prod.get('codigo', 'S/C')}] " if prod.get('codigo') else ""
                self.venta_producto_busqueda.set(f"{codigo_txt}{prod['nombre']}")
                self.venta_producto_id = prod['id']
                self.venta_precio.set(prod['precio_venta'])
                self.venta_precio_original.set(prod['precio_venta'])  # Guardar precio original
                self.venta_producto_label.config(text="✓", bootstyle="success")
                
                # Resetear descuento al seleccionar nuevo producto
                self.aplicar_descuento.set(False)
                self.venta_descuento.set(0)
                self.toggle_descuento()
                
                # Actualizar stock
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
                
                self.stock_label.config(text=texto, bootstyle=color)
                self.producto_listbox_window.destroy()
        
        def cerrar(event=None):
            if self.producto_listbox_window.winfo_exists():
                self.producto_listbox_window.destroy()
        
        self.producto_listbox.bind('<<ListboxSelect>>', seleccionar)
        self.producto_listbox.bind('<Return>', seleccionar)
        self.producto_listbox.bind('<Escape>', cerrar)
        self.producto_listbox_window.bind('<FocusOut>', cerrar)
        
        if event.keysym == 'Down':
            self.producto_listbox.focus_set()
            self.producto_listbox.selection_set(0)
    
    # ===== MÉTODOS DE DESCUENTO =====
    
    def toggle_descuento(self):
        """Activa o desactiva los campos de descuento."""
        if self.aplicar_descuento.get():
            # Activar descuento
            self.venta_descuento_entry.config(state='normal')
            self.venta_precio_entry.config(state='normal')  # Permitir editar precio directamente
            
            # Guardar precio original
            if self.venta_precio.get() > 0:
                self.venta_precio_original.set(self.venta_precio.get())
                self.actualizar_precio_final()
        else:
            # Desactivar descuento
            self.venta_descuento_entry.config(state='disabled')
            self.venta_precio_entry.config(state='readonly')
            self.venta_descuento.set(0)
            
            # Restaurar precio original si existe
            if self.venta_precio_original.get() > 0:
                self.venta_precio.set(self.venta_precio_original.get())
            
            self.precio_final_label.config(text="Q 0.00")
    
    def calcular_precio_con_descuento(self, event=None):
        """Calcula el precio final basado en el descuento porcentual."""
        try:
            descuento = self.venta_descuento.get()
            
            # Validar rango de descuento
            if descuento < 0:
                self.venta_descuento.set(0)
                descuento = 0
            elif descuento > 100:
                self.venta_descuento.set(100)
                descuento = 100
            
            # Calcular nuevo precio
            if self.venta_precio_original.get() > 0:
                precio_original = self.venta_precio_original.get()
                precio_con_descuento = precio_original * (1 - descuento / 100)
                self.venta_precio.set(round(precio_con_descuento, 2))
                self.actualizar_precio_final()
        except Exception as e:
            # Si hay error al calcular, resetear
            if self.venta_precio_original.get() > 0:
                self.venta_precio.set(self.venta_precio_original.get())
                self.actualizar_precio_final()
    
    def actualizar_precio_final(self):
        """Actualiza la etiqueta de precio final."""
        try:
            precio = self.venta_precio.get()
            if precio > 0:
                # Validar que el precio con descuento no sea mayor al original
                if self.aplicar_descuento.get() and self.venta_precio_original.get() > 0:
                    if precio > self.venta_precio_original.get():
                        # Restaurar al precio original si intenta poner un precio mayor
                        self.venta_precio.set(self.venta_precio_original.get())
                        precio = self.venta_precio_original.get()
                        messagebox.showwarning("Precio Inválido", 
                                             f"El precio con descuento no puede ser mayor al precio original.\n\n"
                                             f"Precio original: Q {self.venta_precio_original.get():,.2f}")
                
                self.precio_final_label.config(text=f"Q {precio:,.2f}")
            else:
                self.precio_final_label.config(text="Q 0.00")
        except:
            self.precio_final_label.config(text="Q 0.00")
    
    def on_precio_change(self, *args):
        """Callback cuando cambia el precio (para actualizar el precio final)."""
        if self.aplicar_descuento.get():
            # Usar after para evitar conflictos con trace
            self.frame.after(100, self.actualizar_precio_final)
    
    # ===== MÉTODOS DE BÚSQUEDA =====
    
    def buscar_cliente(self):
        """Abre diálogo para buscar cliente."""
        from ..utils import centrar_ventana, agregar_icono
        
        busqueda = self.main_window.pedir_texto("Buscar Cliente", "Ingrese nombre o NIT del cliente:")
        if not busqueda:
            return
            
        clientes = self.controller.buscar_cliente(busqueda)
        
        if not clientes:
            messagebox.showinfo("Sin resultados", "No se encontraron clientes con ese criterio")
            return
        
        dialog = tk.Toplevel(self.main_window.root)
        dialog.title("Seleccionar Cliente")
        dialog.geometry("850x550")
        dialog.transient(self.main_window.root)
        dialog.withdraw()
        dialog.grab_set()
        agregar_icono(dialog)
        
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
            yscrollcommand=scrollbar.set,
            height=13
        )
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Nombre', text='Nombre')
        tree.heading('NIT', text='NIT/DPI')
        tree.heading('Dirección', text='Dirección')
        tree.heading('Teléfono', text='Teléfono')
        
        tree.column('ID', width=50, anchor='center')
        tree.column('Nombre', width=250, anchor='w')
        tree.column('NIT', width=120, anchor='center')
        tree.column('Dirección', width=250, anchor='w')
        tree.column('Teléfono', width=120, anchor='center')
        
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
                self.venta_cliente_nit.set(values[2])
                self.venta_cliente_direccion.set(values[3])
                self.venta_cliente_telefono.set(values[4])
                self.venta_cliente_label.config(text="✓", bootstyle="success")
                dialog.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un cliente")
        
        button_frame = tb.Frame(frame)
        button_frame.pack(pady=10)
        tb.Button(button_frame, text="✓ Seleccionar", command=seleccionar, bootstyle="success", width=15).pack()
        
        tree.bind('<Double-1>', lambda e: seleccionar())
        centrar_ventana(dialog)
        dialog.deiconify()
    
    def guardar_cliente_rapido(self):
        """Guarda un nuevo cliente con los datos del formulario."""
        nombre = self.venta_cliente_busqueda.get().strip()
        nit = self.venta_cliente_nit.get().strip()
        direccion = self.venta_cliente_direccion.get().strip()
        telefono = self.venta_cliente_telefono.get().strip()
        
        if not nombre:
            messagebox.showwarning("Advertencia", "Ingrese el nombre del cliente")
            return
        
        if not nit:
            messagebox.showwarning("Advertencia", "Ingrese el NIT o DPI del cliente")
            return
        
        # Verificar que no sea "Consumidor Final" en cualquier variación
        consumidor_final_variants = ['cf', 'consumidor final']
        nombre_lower = nombre.lower().strip()
        nit_lower = nit.lower().strip()
        
        if nombre_lower in consumidor_final_variants or nit_lower in consumidor_final_variants:
            messagebox.showerror("Error", 
                               "No está permitido guardar clientes como 'Consumidor Final'.\n\n"
                               "Este es un cliente especial del sistema que no debe duplicarse.")
            return
        
        # Validar que el NIT no sea solo letras (debe tener al menos un número)
        if nit.isalpha():
            messagebox.showwarning("NIT Inválido", 
                                 "El NIT no puede contener únicamente letras.\n"
                                 "Debe incluir al menos un número.")
            return
        
        # Verificar si el cliente ya existe por NIT exacto
        todos_clientes = self.controller.obtener_clientes()
        cliente_existente = next((c for c in todos_clientes if c['nit_dpi'].strip().upper() == nit.strip().upper()), None)
        
        if cliente_existente:
            messagebox.showwarning("Cliente Existente", 
                              f"El cliente con NIT '{nit}' ya está registrado.\n\n"
                              f"Nombre: {cliente_existente['nombre']}\n"
                              f"Dirección: {cliente_existente['direccion']}\n"
                              f"Teléfono: {cliente_existente['telefono']}")
            return
        
        # Confirmar guardado
        if messagebox.askyesno("Confirmar", f"¿Guardar cliente '{nombre}' en la base de datos?"):
            resultado = self.controller.crear_cliente(nombre, nit, direccion, telefono)
            if resultado['exito']:
                self.venta_cliente_id = resultado['id']
                messagebox.showinfo("Éxito", f"Cliente '{nombre}' guardado correctamente")
                self.venta_cliente_label.config(text="✓", bootstyle="success")
                
                # Actualizar tabla de clientes si existe
                if hasattr(self.main_window, 'clientes_tab'):
                    self.main_window.clientes_tab.refresh()
            else:
                messagebox.showerror("Error", resultado['mensaje'])
    
    def buscar_producto(self):
        """Abre diálogo para buscar producto."""
        from ..utils import centrar_ventana, agregar_icono
        
        busqueda = self.main_window.pedir_texto("Buscar Producto", "Ingrese código, nombre o categoría del producto:")
        if not busqueda:
            return
            
        productos = self.controller.obtener_productos_activos()
        productos_filtrados = [p for p in productos if 
                              busqueda.lower() in p['nombre'].lower() or 
                              busqueda.lower() in str(p.get('codigo', '')).lower() or
                              busqueda.lower() in str(p.get('categoria', '')).lower()]
        
        if not productos_filtrados:
            messagebox.showinfo("Sin resultados", "No se encontraron productos con ese criterio")
            return
        
        dialog = tk.Toplevel(self.main_window.root)
        dialog.title("Seleccionar Producto")
        dialog.geometry("900x550")
        dialog.transient(self.main_window.root)
        dialog.withdraw()
        dialog.grab_set()
        agregar_icono(dialog)
        
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
            yscrollcommand=scrollbar.set,
            height=13
        )
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Código', text='Código')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Precio Venta', text='Precio Venta')
        tree.heading('Stock', text='Stock')
        
        tree.column('ID', width=50, anchor='center')
        tree.column('Código', width=120, anchor='w')
        tree.column('Nombre', width=350, anchor='w')
        tree.column('Precio Venta', width=120, anchor='center')
        tree.column('Stock', width=100, anchor='center')
        
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
                self.venta_producto_label.config(text="✓", bootstyle="success")
                self.venta_precio.set(producto['precio_venta'])
                self.venta_precio_original.set(producto['precio_venta'])  # Guardar precio original
                
                # Resetear descuento al seleccionar nuevo producto
                self.aplicar_descuento.set(False)
                self.venta_descuento.set(0)
                self.toggle_descuento()
                
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
        
        button_frame = tb.Frame(frame)
        button_frame.pack(pady=10)
        tb.Button(button_frame, text="✓ Seleccionar", command=seleccionar, bootstyle="success", width=15).pack()
        
        tree.bind('<Double-1>', lambda e: seleccionar())
        centrar_ventana(dialog)
        dialog.deiconify()
    
    # ===== MÉTODOS DEL CARRITO =====
    
    def agregar_al_carrito(self):
        """Agrega un producto al carrito."""
        try:
            if not self.venta_producto_id:
                messagebox.showwarning("Advertencia", "Busque y seleccione un producto")
                return
            
            cantidad = self.venta_cantidad.get()
            precio = self.venta_precio.get()
            
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            if precio <= 0:
                messagebox.showwarning("Advertencia", "El precio debe ser mayor a 0")
                return
            
            # Validar que si hay descuento aplicado, el precio no sea mayor al original
            if self.aplicar_descuento.get() and self.venta_precio_original.get() > 0:
                if precio > self.venta_precio_original.get():
                    messagebox.showwarning("Precio Inválido",
                                         f"El precio con descuento no puede ser mayor al precio original.\n\n"
                                         f"Precio original: Q {self.venta_precio_original.get():,.2f}\n"
                                         f"Precio ingresado: Q {precio:,.2f}")
                    return
            
            # Obtener producto
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
            
            # Verificar si ya está en el carrito
            for item in self.carrito_ventas:
                if item['producto_id'] == self.venta_producto_id:
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
            
            # Agregar nuevo producto
            self.carrito_ventas.append({
                'producto_id': self.venta_producto_id,
                'nombre': producto['nombre'],
                'cantidad': cantidad,
                'precio_unitario': precio,
                'precio_original': self.venta_precio_original.get() if self.venta_precio_original.get() > 0 else precio,
                'descuento_aplicado': self.aplicar_descuento.get(),
                'descuento_porcentaje': self.venta_descuento.get() if self.aplicar_descuento.get() else 0,
                'subtotal': cantidad * precio
            })
            
            self.actualizar_tabla_carrito()
            self.limpiar_formulario_producto()
            messagebox.showinfo("Producto Agregado", f"{producto['nombre']} agregado al carrito")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar al carrito: {str(e)}")
    
    def actualizar_tabla_carrito(self):
        """Actualiza la tabla del carrito."""
        # Limpiar tabla
        for item in self.carrito_tree.get_children():
            self.carrito_tree.delete(item)
        
        # Calcular total
        total = 0
        
        # Llenar tabla
        for item in self.carrito_ventas:
            # Obtener información de descuento
            precio_original = item.get('precio_original', item['precio_unitario'])
            descuento_porcentaje = item.get('descuento_porcentaje', 0)
            descuento_aplicado = item.get('descuento_aplicado', False)
            
            # Formatear descuento
            if descuento_aplicado and descuento_porcentaje > 0:
                descuento_str = f"{descuento_porcentaje:.1f}%"
            else:
                descuento_str = "-"
            
            self.carrito_tree.insert('', 'end', values=(
                item['nombre'][:30],
                item['cantidad'],
                f"Q {precio_original:,.2f}",
                descuento_str,
                f"Q {item['precio_unitario']:,.2f}",
                f"Q {item['subtotal']:,.2f}"
            ))
            total += item['subtotal']
        
        # Actualizar total
        self.carrito_total_label.config(text=f"Q {total:,.2f}")
    
    def quitar_del_carrito(self):
        """Quita el producto seleccionado del carrito."""
        seleccion = self.carrito_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto del carrito")
            return
        
        item_index = self.carrito_tree.index(seleccion[0])
        producto_nombre = self.carrito_ventas[item_index]['nombre']
        del self.carrito_ventas[item_index]
        
        self.actualizar_tabla_carrito()
        messagebox.showinfo("Producto Eliminado", f"{producto_nombre} eliminado del carrito")
    
    def limpiar_carrito(self):
        """Limpia todo el carrito."""
        if not self.carrito_ventas:
            messagebox.showinfo("Carrito Vacío", "El carrito ya está vacío")
            return
        
        respuesta = messagebox.askyesno("Confirmar", 
                                        "¿Está seguro de limpiar todo el carrito?")
        if respuesta:
            self.carrito_ventas = []
            self.actualizar_tabla_carrito()
            messagebox.showinfo("Carrito Limpiado", "Todos los productos fueron eliminados")
    
    def mostrar_ventana_pago(self, total):
        """Muestra ventana para ingresar el monto pagado y calcular cambio."""
        from ..utils import centrar_ventana, agregar_icono
        
        # Variables para resultado
        resultado = {'confirmar': False, 'monto_pagado': 0, 'cambio': 0}
        
        # Crear ventana
        dialog = tk.Toplevel(self.main_window.root)
        dialog.title("Total a Pagar")
        dialog.geometry("450x450")
        dialog.transient(self.main_window.root)
        dialog.withdraw()  # Ocultar mientras se construye
        dialog.grab_set()
        dialog.resizable(False, False)
        agregar_icono(dialog)
        
        # Frame principal
        main_frame = tb.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Total a pagar (grande y destacado)
        total_frame = tb.Labelframe(main_frame, text="Total a Pagar", padding=15, bootstyle="info")
        total_frame.pack(fill='x', pady=(0, 15))
        
        tb.Label(
            total_frame,
            text=f"Q {total:,.2f}",
            font=('Segoe UI', 28, 'bold'),
            bootstyle="info"
        ).pack()
        
        # Monto recibido
        pago_frame = tb.Labelframe(main_frame, text="Monto Recibido del Cliente", padding=15)
        pago_frame.pack(fill='x', pady=(0, 15))
        
        monto_var = tk.DoubleVar(value=total)
        
        monto_entry = tb.Entry(
            pago_frame,
            textvariable=monto_var,
            font=('Segoe UI', 20, 'bold'),
            justify='center'
        )
        monto_entry.pack(fill='x', pady=5)
        monto_entry.select_range(0, tk.END)
        monto_entry.focus()
        
        # Cambio a devolver
        cambio_frame = tb.Labelframe(main_frame, text="Cambio a Devolver", padding=15, bootstyle="success")
        cambio_frame.pack(fill='x', pady=(0, 15))
        
        cambio_label = tb.Label(
            cambio_frame,
            text="Q 0.00",
            font=('Segoe UI', 24, 'bold'),
            bootstyle="success"
        )
        cambio_label.pack()
        
        def calcular_cambio(*args):
            """Calcula el cambio automáticamente."""
            try:
                monto_pagado = monto_var.get()
                cambio = monto_pagado - total
                
                if cambio >= 0:
                    cambio_label.config(text=f"Q {cambio:,.2f}", bootstyle="success")
                else:
                    cambio_label.config(text=f"Q {cambio:,.2f} (Falta)", bootstyle="danger")
            except:
                cambio_label.config(text="Q 0.00")
        
        # Actualizar cambio al escribir
        monto_var.trace_add('write', calcular_cambio)
        calcular_cambio()  # Calcular inicial
        
        def confirmar():
            """Confirma el pago."""
            try:
                monto_pagado = monto_var.get()
                
                if monto_pagado < total:
                    messagebox.showwarning("Monto Insuficiente", 
                                         f"El monto recibido (Q {monto_pagado:,.2f}) es menor que el total (Q {total:,.2f}).\n\n"
                                         f"Falta: Q {total - monto_pagado:,.2f}")
                    return
                
                cambio = monto_pagado - total
                resultado['confirmar'] = True
                resultado['monto_pagado'] = monto_pagado
                resultado['cambio'] = cambio
                dialog.destroy()
            except:
                messagebox.showerror("Error", "Ingrese un monto válido")
        
        def cancelar():
            """Cancela la operación."""
            resultado['confirmar'] = False
            dialog.destroy()
        
        # Botones
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(fill='x')
        
        tb.Button(
            btn_frame,
            text="✓ Confirmar Pago",
            command=confirmar,
            bootstyle="success",
            width=18
        ).pack(side='left', padx=5, expand=True, fill='x')
        
        tb.Button(
            btn_frame,
            text="✗ Cancelar",
            command=cancelar,
            bootstyle="danger-outline",
            width=15
        ).pack(side='left', padx=5, expand=True, fill='x')
        
        # Enter para confirmar
        monto_entry.bind('<Return>', lambda e: confirmar())
        dialog.bind('<Escape>', lambda e: cancelar())
        
        centrar_ventana(dialog)
        dialog.deiconify()  # Mostrar después de construir
        dialog.wait_window()
        
        return resultado
    
    def finalizar_venta(self):
        """Finaliza la venta."""
        try:
            nombre = self.venta_cliente_busqueda.get().strip()
            nit = self.venta_cliente_nit.get().strip()
            
            if not nombre or not nit:
                messagebox.showwarning("Advertencia", "Debe ingresar al menos el Nombre y NIT/DPI del cliente")
                return
            
            # Si no hay cliente_id, buscar si existe o crear cliente automáticamente
            if not self.venta_cliente_id:
                # Primero buscar si el cliente ya existe por NIT
                todos_clientes = self.controller.obtener_clientes()
                cliente_existente = next((c for c in todos_clientes if c['nit_dpi'].strip().upper() == nit.strip().upper()), None)
                
                if cliente_existente:
                    # El cliente ya existe (ej: Consumidor Final), usarlo
                    self.venta_cliente_id = cliente_existente['id']
                else:
                    # Es un cliente nuevo, guardarlo
                    messagebox.showinfo(
                        "Cliente Nuevo",
                        f"Se guardará el cliente en la base de datos:\n\n"
                        f"Nombre: {nombre}\nNIT/DPI: {nit}\n\n"
                        f"El cliente estará disponible para futuras ventas."
                    )
                    direccion = self.venta_cliente_direccion.get().strip()
                    telefono = self.venta_cliente_telefono.get().strip()
                    
                    exito, mensaje = self.controller.crear_cliente(nombre, nit, direccion, telefono)
                    if exito:
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
            
            # Calcular total
            total = sum(item['subtotal'] for item in self.carrito_ventas)
            
            # Mostrar ventana de pago y cambio
            resultado_pago = self.mostrar_ventana_pago(total)
            
            if not resultado_pago['confirmar']:
                return
            
            # Guardar información de pago
            monto_pagado = resultado_pago['monto_pagado']
            cambio = resultado_pago['cambio']
            
            # Obtener fecha
            fecha_cal = self.venta_fecha_cal.entry.get()
            hora_actual = datetime.now().strftime('%H:%M:%S')
            fecha_manual = f"{fecha_cal} {hora_actual}"
            
            # Registrar venta
            exito, mensaje = self.controller.registrar_venta_con_carrito(
                self.venta_cliente_id,
                self.carrito_ventas,
                fecha_manual
            )
            
            if exito:
                # Mostrar información de pago
                mensaje_completo = (
                    f"{mensaje}\n\n"
                    f"💰 Total: Q {total:,.2f}\n"
                    f"💵 Pagado: Q {monto_pagado:,.2f}\n"
                    f"💸 Cambio: Q {cambio:,.2f}"
                )
                messagebox.showinfo("Venta Exitosa", mensaje_completo)
                
                # Limpiar todo
                self.carrito_ventas = []
                self.actualizar_tabla_carrito()
                self.limpiar_formulario_producto()
                
                # Limpiar datos del cliente
                self.venta_cliente_busqueda.set("")
                self.venta_cliente_nit.set("")
                self.venta_cliente_direccion.set("")
                self.venta_cliente_telefono.set("")
                self.venta_cliente_label.config(text="")
                self.venta_cliente_id = None
                
                # Actualizar tablas
                self.refresh()
                if hasattr(self.main_window, 'refresh_productos'):
                    self.main_window.refresh_productos()
                if hasattr(self.main_window, 'refresh_caja'):
                    self.main_window.refresh_caja()
                if hasattr(self.main_window, 'actualizar_resumen'):
                    self.main_window.actualizar_resumen()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    # ===== MÉTODOS DE LIMPIEZA =====
    
    def limpiar_formulario_producto(self):
        """Limpia solo los campos de producto."""
        self.venta_producto_id = None
        self.venta_producto_busqueda.set("")
        self.venta_cantidad.set(1)
        self.venta_precio.set(0)
        self.venta_precio_original.set(0)
        self.venta_descuento.set(0)
        self.aplicar_descuento.set(False)
        self.toggle_descuento()
        self.venta_producto_label.config(text="")
        self.stock_label.config(text="📦 Stock Disponible: 0", bootstyle="info")
    
    def sort_column(self, col):
        """Ordena la tabla por la columna seleccionada."""
        from ..utils import sort_treeview
        sort_treeview(self.ventas_tree, col, False)
    
    def limpiar_formulario_carrito(self):
        """Limpia el formulario completo (cliente, productos y carrito)."""
        # Limpiar datos del cliente
        self.venta_cliente_busqueda.set("")
        self.venta_cliente_nit.set("")
        self.venta_cliente_direccion.set("")
        self.venta_cliente_telefono.set("")
        self.venta_cliente_label.config(text="")
        self.venta_cliente_id = None
        
        # Limpiar formulario de producto
        self.limpiar_formulario_producto()
        
        # Limpiar carrito
        self.carrito_ventas = []
        self.actualizar_tabla_carrito()
    
    # ===== MÉTODOS DE DATOS =====
    
    def refresh(self):
        """Actualiza la lista de ventas."""
        # Limpiar treeview
        for item in self.ventas_tree.get_children():
            self.ventas_tree.delete(item)
        
        # Obtener búsqueda
        texto_busqueda = self.venta_search.get().strip().lower() if hasattr(self, 'venta_search') else ''
        
        # Cargar ventas
        ventas = self.controller.obtener_ventas()
        for i, venta in enumerate(ventas):
            # Aplicar filtro
            if texto_busqueda:
                ref_no = str(venta.get('referencia_no', venta['id'])).lower()
                cliente = venta.get('cliente_nombre', '').lower()
                nit_dpi = venta.get('cliente_nit', '').lower()
                fecha = str(venta.get('fecha', '')).lower()
                
                productos_match = False
                if 'detalles' in venta:
                    for detalle in venta['detalles']:
                        if texto_busqueda in detalle.get('producto_nombre', '').lower():
                            productos_match = True
                            break
                
                if (texto_busqueda not in ref_no and 
                    texto_busqueda not in cliente and
                    texto_busqueda not in nit_dpi and
                    texto_busqueda not in fecha and
                    not productos_match):
                    continue
            
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            
            # Formatear fecha
            fecha_str = venta['fecha']
            try:
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
            except:
                try:
                    fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y %H:%M:%S')
                    fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
                except:
                    fecha_formateada = fecha_str.split()[0] if ' ' in fecha_str else fecha_str
            
            # Resumen de productos
            if 'detalles' in venta and len(venta['detalles']) > 0:
                if len(venta['detalles']) == 1:
                    productos_str = venta['detalles'][0]['producto_nombre']
                else:
                    productos_str = f"{len(venta['detalles'])} productos"
            else:
                productos_str = venta.get('producto_nombre', 'N/A')
            
            # NIT/DPI
            nit_dpi = venta.get('cliente_nit', '').strip() or '-'
            
            self.ventas_tree.insert('', 'end', values=(
                venta.get('referencia_no', f"REF{venta['id']}"),
                nit_dpi,
                venta.get('cliente_nombre', '[Sin Cliente]'),
                productos_str,
                f"Q {venta['total']:,.2f}",
                fecha_formateada,
                venta.get('estado', 'COMPLETADA')
            ), tags=(tag,))
    
    def ver_detalle_venta(self, event):
        """Muestra los detalles completos de una venta."""
        from ..utils import centrar_ventana, agregar_icono
        
        seleccion = self.ventas_tree.selection()
        if not seleccion:
            return
        
        try:
            item = self.ventas_tree.item(seleccion[0])
            valores = item['values']
            ref_no = valores[0]
            
            # Extraer ID de la referencia (formato: REF00001)
            venta_id = int(ref_no.replace('REF', ''))
            
            # Obtener venta completa con detalles
            venta = self.controller.obtener_venta_por_id(venta_id)
            
            if not venta:
                messagebox.showerror("Error", "No se pudo obtener la información de la venta")
                return
            
            # Crear ventana de detalles
            dialog = tk.Toplevel(self.main_window.root)
            dialog.title(f"📋 Detalle de Venta - {venta['referencia_no']}")
            dialog.geometry("850x700")
            dialog.transient(self.main_window.root)
            dialog.withdraw()  # Ocultar mientras se construye
            dialog.grab_set()
            agregar_icono(dialog)
            
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
            
            cols = ('Producto', 'Cantidad', 'Precio Orig.', 'Desc %', 'Precio Final', 'Subtotal')
            detalle_tree = tb.Treeview(tree_frame, columns=cols, show='headings', height=5)
            
            detalle_tree.heading('Producto', text='Producto')
            detalle_tree.heading('Cantidad', text='Cant.')
            detalle_tree.heading('Precio Orig.', text='Precio Orig.')
            detalle_tree.heading('Desc %', text='Desc %')
            detalle_tree.heading('Precio Final', text='Precio Final')
            detalle_tree.heading('Subtotal', text='Subtotal')
            
            detalle_tree.column('Producto', width=250, anchor='w')
            detalle_tree.column('Cantidad', width=70, anchor='center')
            detalle_tree.column('Precio Orig.', width=100, anchor='e')
            detalle_tree.column('Desc %', width=70, anchor='center')
            detalle_tree.column('Precio Final', width=100, anchor='e')
            detalle_tree.column('Subtotal', width=100, anchor='e')
            
            scrollbar = tb.Scrollbar(tree_frame, orient='vertical', command=detalle_tree.yview)
            detalle_tree.configure(yscrollcommand=scrollbar.set)
            
            detalle_tree.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Llenar tabla con productos
            for detalle in venta['detalles']:
                # Obtener producto para comparar precio original
                producto = self.controller.obtener_producto_por_id(detalle['producto_id'])
                precio_venta_actual = producto['precio_venta'] if producto else detalle['precio_unitario']
                precio_pagado = detalle['precio_unitario']
                
                # Calcular si hubo descuento
                if precio_pagado < precio_venta_actual:
                    descuento_porcentaje = ((precio_venta_actual - precio_pagado) / precio_venta_actual) * 100
                    precio_original_str = f"Q {precio_venta_actual:,.2f}"
                    descuento_str = f"{descuento_porcentaje:.1f}%"
                else:
                    precio_original_str = f"Q {precio_pagado:,.2f}"
                    descuento_str = "-"
                
                detalle_tree.insert('', 'end', values=(
                    detalle['producto_nombre'],
                    detalle['cantidad'],
                    precio_original_str,
                    descuento_str,
                    f"Q {precio_pagado:,.2f}",
                    f"Q {detalle['subtotal']:,.2f}"
                ))
            
            # Información de Pago
            pago_frame = tb.Labelframe(main_frame, text="💰 Información de Pago", padding=15, bootstyle="success")
            pago_frame.pack(fill='x', pady=(0, 10))
            
            # Grid para info de pago
            pago_info = tb.Frame(pago_frame)
            pago_info.pack(fill='x')
            
            # Total
            tb.Label(pago_info, text="Total:", font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=3)
            tb.Label(pago_info, text=f"Q {venta['total']:,.2f}", font=('Segoe UI', 11)).grid(row=0, column=1, sticky='w', padx=5, pady=3)
            
            # Monto Pagado (si está disponible)
            monto_pagado = venta.get('monto_pagado', None)
            if monto_pagado is not None and monto_pagado > 0:
                tb.Label(pago_info, text="Pagado:", font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', padx=5, pady=3)
                tb.Label(pago_info, text=f"Q {monto_pagado:,.2f}", font=('Segoe UI', 11)).grid(row=1, column=1, sticky='w', padx=5, pady=3)
                
                # Cambio (si está disponible)
                cambio = venta.get('cambio', 0)
                tb.Label(pago_info, text="Cambio:", font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, sticky='w', padx=5, pady=3)
                tb.Label(pago_info, text=f"Q {cambio:,.2f}", font=('Segoe UI', 11), bootstyle="success").grid(row=2, column=1, sticky='w', padx=5, pady=3)
            
            # Botones
            btn_frame = tb.Frame(main_frame)
            btn_frame.pack(pady=10)
            
            # Botón Generar PDF
            tb.Button(
                btn_frame,
                text="📄 Generar PDF",
                command=lambda: self.generar_pdf_venta(venta),
                bootstyle="info",
                width=18
            ).pack(side='left', padx=5)
            
            # Botón Anular (solo si no está anulada)
            if venta['estado'] != 'Anulado':
                tb.Button(
                    btn_frame, 
                    text="🚫 Anular Venta", 
                    command=lambda: self.anular_venta_desde_detalle(venta_id, dialog),
                    bootstyle="danger",
                    width=18
                ).pack(side='left', padx=5)
            
            tb.Button(
                btn_frame, 
                text="Cerrar", 
                command=dialog.destroy, 
                bootstyle="secondary", 
                width=15
            ).pack(side='left', padx=5)
            
            centrar_ventana(dialog)
            dialog.deiconify()  # Mostrar después de construir
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalles: {str(e)}")
    
    def mostrar_menu_contextual_venta(self, event):
        """Muestra menú contextual al hacer clic derecho en una venta."""
        # Seleccionar el item bajo el cursor
        item = self.ventas_tree.identify_row(event.y)
        if item:
            self.ventas_tree.selection_set(item)
            
            # Obtener estado de la venta
            valores = self.ventas_tree.item(item)['values']
            estado = valores[4] if len(valores) > 4 else ""
            
            # Crear menú contextual
            menu = tk.Menu(self.main_window.root, tearoff=0)
            menu.add_command(label="👁️ Ver Detalle", command=lambda: self.ver_detalle_venta(None))
            
            # Solo mostrar opción de anular si no está anulada
            if estado != "Anulado":
                menu.add_separator()
                menu.add_command(label="🚫 Anular Venta", command=self.anular_venta_seleccionada)
            
            # Mostrar menú
            menu.post(event.x_root, event.y_root)
    
    def anular_venta_seleccionada(self):
        """Anula la venta seleccionada desde el menú contextual."""
        seleccion = self.ventas_tree.selection()
        if not seleccion:
            return
        
        try:
            item = self.ventas_tree.item(seleccion[0])
            valores = item['values']
            ref_no = valores[0]
            
            # Extraer ID de la referencia
            venta_id = int(ref_no.replace('REF', ''))
            
            self.anular_venta(venta_id)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al anular venta: {str(e)}")
    
    def anular_venta_desde_detalle(self, venta_id, dialog):
        """Anula la venta desde la ventana de detalle."""
        if self.anular_venta(venta_id):
            dialog.destroy()
    
    def anular_venta(self, venta_id):
        """Anula una venta y devuelve productos al inventario."""
        try:
            # Obtener información de la venta
            venta = self.controller.obtener_venta_por_id(venta_id)
            
            if not venta:
                messagebox.showerror("Error", "No se encontró la venta")
                return False
            
            # Verificar si ya está anulada
            if venta['estado'] == 'Anulado':
                messagebox.showwarning("Advertencia", "Esta venta ya está anulada")
                return False
            
            # Confirmar anulación
            respuesta = messagebox.askyesno(
                "Confirmar Anulación",
                f"¿Está seguro de anular la venta {venta['referencia_no']}?\n\n"
                f"Cliente: {venta['cliente_nombre']}\n"
                f"Total: Q {venta['total']:,.2f}\n\n"
                f"Esta acción:\n"
                f"• Cambiará el estado a 'Anulado'\n"
                f"• Devolverá los productos al inventario\n"
                f"• Restará el monto de la caja\n\n"
                f"¿Desea continuar?",
                icon='warning'
            )
            
            if not respuesta:
                return False
            
            # Anular venta en el controlador
            exito, mensaje = self.controller.anular_venta(venta_id)
            
            if exito:
                messagebox.showinfo("Venta Anulada", 
                                  f"La venta {venta['referencia_no']} ha sido anulada exitosamente.\n\n"
                                  f"{mensaje}")
                
                # Actualizar tablas
                self.refresh()
                if hasattr(self.main_window, 'refresh_productos'):
                    self.main_window.refresh_productos()
                if hasattr(self.main_window, 'refresh_caja'):
                    self.main_window.refresh_caja()
                if hasattr(self.main_window, 'actualizar_resumen'):
                    self.main_window.actualizar_resumen()
                
                return True
            else:
                messagebox.showerror("Error", f"No se pudo anular la venta:\n{mensaje}")
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al anular venta: {str(e)}")
            return False
    
    def generar_pdf_venta(self, venta):
        """Genera un PDF con el detalle de la venta."""
        try:
            from tkinter import filedialog
            from ..utils.pdf_generator import PDFGenerator
            import subprocess
            import platform
            from pathlib import Path
            
            # Diálogo para seleccionar ubicación y nombre del archivo
            nombre_sugerido = f"Recibo_{venta['referencia_no']}.pdf"
            ruta_inicial = str(Path.home() / "Documents")
            
            archivo_salida = filedialog.asksaveasfilename(
                title="Guardar Recibo PDF",
                initialdir=ruta_inicial,
                initialfile=nombre_sugerido,
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if not archivo_salida:  # Usuario canceló
                return
            
            # Configurar información de la empresa
            # TODO: Estos datos deberían venir de una configuración
            generador = PDFGenerator(
                empresa_nombre="MARTELIZ SHOP",
                # empresa_nit="1234567-8",
                empresa_direccion="Cobán, Alta Verapaz",
                empresa_telefono="+502 3987-7846",
                empresa_email="martelizshop@gmail.com",
                logo_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "Logo", "Logo.png")
            )
            
            # Generar PDF
            exito, mensaje = generador.generar_factura_venta(venta, archivo_salida)
            
            if exito:
                # Preguntar si desea abrir el archivo
                respuesta = messagebox.askyesno(
                    "PDF Generado",
                    f"PDF generado exitosamente:\n\n{archivo_salida}\n\n¿Desea abrir el archivo?",
                    icon='info'
                )
                
                if respuesta:
                    # Abrir PDF con el visor predeterminado
                    if platform.system() == 'Windows':
                        os.startfile(archivo_salida)
                    elif platform.system() == 'Darwin':  # macOS
                        subprocess.run(['open', archivo_salida])
                    else:  # Linux
                        subprocess.run(['xdg-open', archivo_salida])
            else:
                messagebox.showerror("Error", f"No se pudo generar el PDF:\n{mensaje}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")
    
    def on_tree_motion(self, event):
        """Maneja el efecto hover sobre las filas del treeview"""
        tree = event.widget
        item = tree.identify_row(event.y)
        
        if item != self.last_hovered_item:
            # Restaurar el tag original del item anterior
            if self.last_hovered_item and self.original_tag:
                tree.item(self.last_hovered_item, tags=(self.original_tag,))
            
            # Aplicar hover al nuevo item
            if item:
                current_tags = tree.item(item, 'tags')
                if current_tags:
                    self.original_tag = current_tags[0]
                    hover_tag = f"{self.original_tag}_hover"
                    tree.item(item, tags=(hover_tag,))
                else:
                    self.original_tag = None
            
            self.last_hovered_item = item
    
    def on_tree_leave(self, event):
        """Restaura el tag original cuando el mouse sale del treeview"""
        if self.last_hovered_item and self.original_tag:
            event.widget.item(self.last_hovered_item, tags=(self.original_tag,))
            self.last_hovered_item = None
            self.original_tag = None
