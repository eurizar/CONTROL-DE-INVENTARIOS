"""
Módulo de gestión de productos
Permite crear, editar, activar/desactivar y listar productos del inventario
"""
import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox
import re


class ProductosTab:
    """Pestaña de gestión de productos"""
    
    def __init__(self, parent_frame, controller, main_window):
        self.parent_frame = parent_frame
        self.controller = controller
        self.main_window = main_window
        
        # Variables de formulario
        self.setup_variables()
        
        # Variables de control
        self.producto_seleccionado = None
        self.sku_data = {}
        
        # Crear interfaz
        self.create_ui()
    
    def setup_variables(self):
        """Inicializa las variables del formulario"""
        self.producto_codigo = tb.StringVar()
        self.producto_nombre = tb.StringVar()
        self.producto_categoria = tb.StringVar()
        self.producto_precio_compra = tb.DoubleVar()
        self.producto_ganancia = tb.DoubleVar()
        self.producto_precio_venta_manual = tb.DoubleVar()
        self.producto_tipo_calculo = tb.StringVar(value="precio")
        self.producto_filtro = tb.StringVar(value='activos')
    
    def create_ui(self):
        """Crea la interfaz de usuario de productos"""
        # BOTÓN PRINCIPAL: INGRESAR NUEVO PRODUCTO
        boton_nuevo_frame = tb.Frame(self.parent_frame)
        boton_nuevo_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        tb.Button(
            boton_nuevo_frame,
            text="➕ INGRESAR NUEVO PRODUCTO",
            command=lambda: self.abrir_generador_sku(),
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
        
        # Formulario de productos
        self.crear_formulario()
        
        # Lista de productos
        self.crear_tabla()
        
        # Sincronizar campos con el tipo de cálculo por defecto
        self.cambiar_tipo_calculo()
    
    def crear_formulario(self):
        """Crea el formulario de gestión de productos"""
        form_frame = tb.Labelframe(
            self.parent_frame,
            text="✏️ Gestión de Productos",
            padding=15,
            bootstyle="primary"
        )
        form_frame.pack(fill='x', padx=15, pady=15)
        
        # FILA 1: Código y Nombre
        tb.Label(form_frame, text="Código:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        self.codigo_entry = tb.Entry(
            form_frame,
            textvariable=self.producto_codigo,
            width=32,
            font=('Segoe UI', 11, 'bold'),
            state='disabled',
            cursor='arrow'
        )
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tb.Label(form_frame, text="Nombre:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=2, sticky='w', padx=(20, 5), pady=5)
        
        self.producto_nombre_entry = tb.Entry(
            form_frame,
            textvariable=self.producto_nombre,
            width=30,
            font=('Segoe UI', 10),
            state='readonly',
            cursor='arrow'
        )
        self.producto_nombre_entry.grid(row=0, column=3, padx=5, pady=5, sticky='ew')
        self.producto_nombre_entry.configure(foreground='#2c3e50', background='#ecf0f1')
        
        # FILA 2: Precio Compra y Categoría
        tb.Label(form_frame, text="Precio por Unidad (Q):", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        
        entry_precio_compra = tb.Entry(form_frame, textvariable=self.producto_precio_compra, width=15, font=('Segoe UI', 10))
        entry_precio_compra.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        entry_precio_compra.bind('<KeyRelease>', lambda e: self.calcular_precio_desde_ganancia() if self.producto_tipo_calculo.get() == "porcentaje" else self.calcular_ganancia_desde_precio())
        
        tb.Label(form_frame, text="Categoría:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=2, sticky='w', padx=(20, 5), pady=5)
        
        self.producto_categoria_entry = tb.Entry(
            form_frame,
            textvariable=self.producto_categoria,
            width=30,
            font=('Segoe UI', 10),
            state='readonly',
            cursor='arrow'
        )
        self.producto_categoria_entry.grid(row=1, column=3, padx=5, pady=5, sticky='ew')
        self.producto_categoria_entry.configure(foreground='#2c3e50', background='#ecf0f1')
        
        # FILA 3: Radio buttons de método de cálculo
        tb.Label(form_frame, text="Calcular por:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        
        radio_frame = tb.Frame(form_frame)
        radio_frame.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky='w')
        
        tb.Radiobutton(
            radio_frame,
            text="Precio Venta",
            variable=self.producto_tipo_calculo,
            value="precio",
            command=lambda: self.cambiar_tipo_calculo(),
            bootstyle="info"
        ).pack(side='left', padx=5)
        
        tb.Radiobutton(
            radio_frame,
            text="% Ganancia",
            variable=self.producto_tipo_calculo,
            value="porcentaje",
            command=lambda: self.cambiar_tipo_calculo(),
            bootstyle="info"
        ).pack(side='left', padx=5)
        
        # FILA 4: % Ganancia y Precio de Venta Calculado
        self.label_ganancia = tb.Label(form_frame, text="% Ganancia:", font=('Segoe UI', 10, 'bold'))
        self.label_ganancia.grid(row=3, column=0, sticky='w', padx=5, pady=5)
        
        self.entry_ganancia = tb.Entry(form_frame, textvariable=self.producto_ganancia, width=15, font=('Segoe UI', 10))
        self.entry_ganancia.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.entry_ganancia.bind('<KeyRelease>', lambda e: self.calcular_precio_desde_ganancia())
        
        self.precio_venta_label = tb.Label(form_frame, text="Precio de Venta: Q 0.00", font=('Segoe UI', 10, 'bold'), bootstyle="success")
        self.precio_venta_label.grid(row=3, column=2, sticky='w', padx=(20, 10), pady=5)
        
        self.monto_ganancia_label = tb.Label(form_frame, text="Ganancia: Q 0.00", font=('Segoe UI', 10, 'bold'), bootstyle="warning")
        self.monto_ganancia_label.grid(row=3, column=3, sticky='w', padx=(10, 5), pady=5)
        
        # Campo de Precio de Venta Manual (oculto inicialmente)
        self.label_precio_venta_manual = tb.Label(form_frame, text="Precio Venta (Q):", font=('Segoe UI', 10, 'bold'))
        
        self.entry_precio_venta_manual = tb.Entry(form_frame, textvariable=self.producto_precio_venta_manual, width=15, font=('Segoe UI', 10))
        self.entry_precio_venta_manual.bind('<KeyRelease>', lambda e: self.calcular_ganancia_desde_precio())
        
        # Configurar grid
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=2)
        
        # Bind para calcular precio de venta automáticamente
        self.producto_precio_compra.trace('w', lambda *args: self.calcular_precio_venta(*args))
        self.producto_ganancia.trace('w', lambda *args: self.calcular_precio_venta(*args))
        
        # FILA 5: Botones
        self.crear_botones(form_frame)
    
    def crear_botones(self, form_frame):
        """Crea los botones de acción"""
        buttons_frame = tb.Frame(form_frame)
        buttons_frame.grid(row=4, column=0, columnspan=4, pady=(10, 5), sticky='ew')
        
        # Botones de acción principales
        tb.Button(buttons_frame, text="➕ Crear", command=self.crear_producto, bootstyle="success", width=12).pack(side='left', padx=3)
        tb.Button(buttons_frame, text="🔄 Actualizar", command=self.actualizar_producto, bootstyle="warning", width=12).pack(side='left', padx=3)
        tb.Button(buttons_frame, text="🗑️ Limpiar", command=self.limpiar_formulario, bootstyle="secondary-outline", width=12).pack(side='left', padx=3)
        
        # Espacio
        tb.Label(buttons_frame, text="  |  ").pack(side='left', padx=5)
        
        # Botones de estado
        tb.Button(buttons_frame, text="⛔ Inactivo", command=self.desactivar_producto, bootstyle="danger-outline", width=12).pack(side='left', padx=3)
        tb.Button(buttons_frame, text="✅ Activar", command=self.activar_producto, bootstyle="success-outline", width=12).pack(side='left', padx=3)
        
        # Espacio
        tb.Label(buttons_frame, text="  |  ").pack(side='left', padx=5)
        
        # Filtros
        tb.Label(buttons_frame, text="Mostrar:", font=('Segoe UI', 9, 'bold')).pack(side='left', padx=5)
        
        tb.Radiobutton(buttons_frame, text="Activos", variable=self.producto_filtro, value="activos", command=self.refresh, bootstyle="success").pack(side='left', padx=2)
        tb.Radiobutton(buttons_frame, text="Inactivos", variable=self.producto_filtro, value="inactivos", command=self.refresh, bootstyle="danger").pack(side='left', padx=2)
        tb.Radiobutton(buttons_frame, text="Todos", variable=self.producto_filtro, value="todos", command=self.refresh, bootstyle="info").pack(side='left', padx=2)
        
        # Botón ver detalles
        tb.Button(buttons_frame, text="👁️ Ver Detalles", command=lambda: self.main_window.ver_detalles_producto(), bootstyle="info-outline", width=15).pack(side='right', padx=5)
    
    def crear_tabla(self):
        """Crea la tabla de productos"""
        list_frame = tb.Labelframe(
            self.parent_frame,
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
        self.producto_search.bind('<KeyRelease>', lambda e: self.refresh())
        
        # Treeview para productos
        tree_frame = tb.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Código', 'Nombre', 'Categoría', 'Marca', 'Color', 'Tamaño', 'Precio Compra', 'Ganancia %', 'Ganancia Q', 'Precio Venta', 'Stock', 'Estado')
        self.productos_tree = tb.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        column_widths = {
            'ID': 50, 'Código': 90, 'Nombre': 200, 'Categoría': 120,
            'Marca': 80, 'Color': 80, 'Tamaño': 80, 'Precio Compra': 110,
            'Ganancia %': 90, 'Ganancia Q': 100, 'Precio Venta': 110,
            'Stock': 70, 'Estado': 80
        }
        
        for col in columns:
            self.productos_tree.heading(col, text=col, command=lambda c=col: self.main_window.sort_treeview(self.productos_tree, c, False))
            anchor = 'center' if col not in ['Nombre', 'Código', 'Categoría'] else 'w'
            self.productos_tree.column(col, width=column_widths[col], anchor=anchor)
        
        # Scrollbars
        scrollbar_y = tb.Scrollbar(tree_frame, orient='vertical', command=self.productos_tree.yview, bootstyle="primary-round")
        scrollbar_x = tb.Scrollbar(tree_frame, orient='horizontal', command=self.productos_tree.xview, bootstyle="primary-round")
        self.productos_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.productos_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Eventos
        self.productos_tree.bind('<Double-1>', self.seleccionar_producto)
        self.productos_tree.bind('<Button-3>', self.mostrar_menu_contextual_producto)
        
        # Ocultar columna "Ganancia %"
        self.productos_tree.column('Ganancia %', width=0, stretch=False)
        
        # Tags de colores
        self.productos_tree.tag_configure('evenrow', background='#f0f0f0')
        self.productos_tree.tag_configure('oddrow', background='#ffffff')
        self.productos_tree.tag_configure('lowstock', background='#ffcccc', foreground='#cc0000')
        self.productos_tree.tag_configure('inactivo', background='#d3d3d3', foreground='#666666')
        
        # Cargar datos iniciales
        self.refresh()
    
    # ========== MÉTODOS DE CÁLCULO ==========
    
    def calcular_precio_venta(self, *args):
        """Calcula el precio de venta automáticamente"""
        try:
            precio_compra = self.producto_precio_compra.get()
            ganancia = self.producto_ganancia.get()
            precio_venta = round(precio_compra * (1 + ganancia / 100), 2)
            self.precio_venta_label.config(text=f"Precio de Venta: Q {precio_venta:,.2f}")
        except:
            self.precio_venta_label.config(text="Precio de Venta: Q 0.00")
    
    def cambiar_tipo_calculo(self):
        """Cambia entre cálculo por porcentaje o precio directo"""
        if self.producto_tipo_calculo.get() == "porcentaje":
            # Mostrar campo de % Ganancia
            self.label_ganancia.grid(row=3, column=0, sticky='w', padx=5, pady=5)
            self.entry_ganancia.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
            # Ocultar campo de Precio Venta
            self.label_precio_venta_manual.grid_forget()
            self.entry_precio_venta_manual.grid_forget()
            # Recalcular
            self.calcular_precio_desde_ganancia()
        else:
            # Ocultar campo de % Ganancia
            self.label_ganancia.grid_forget()
            self.entry_ganancia.grid_forget()
            # Mostrar campo de Precio Venta en la misma posición
            self.label_precio_venta_manual.grid(row=3, column=0, sticky='w', padx=5, pady=5)
            self.entry_precio_venta_manual.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
            # Recalcular
            self.calcular_ganancia_desde_precio()
    
    def calcular_precio_desde_ganancia(self, event=None):
        """Calcula el precio de venta desde el % de ganancia"""
        try:
            precio_compra = self.producto_precio_compra.get()
            ganancia = self.producto_ganancia.get()
            if precio_compra > 0:
                precio_venta = round(precio_compra * (1 + ganancia / 100), 2)
                monto_ganancia = round(precio_venta - precio_compra, 2)
                self.precio_venta_label.config(text=f"Precio de Venta: Q {precio_venta:,.2f}")
                self.monto_ganancia_label.config(text=f"Ganancia: {ganancia:.2f}% - Q {monto_ganancia:,.2f}")
                # Actualizar también el campo manual por si cambian
                self.producto_precio_venta_manual.set(precio_venta)
        except:
            self.precio_venta_label.config(text="Precio de Venta: Q 0.00")
            self.monto_ganancia_label.config(text="Ganancia: Q 0.00")
    
    def calcular_ganancia_desde_precio(self, event=None):
        """Calcula el % de ganancia desde el precio de venta"""
        try:
            precio_compra = self.producto_precio_compra.get()
            precio_venta = self.producto_precio_venta_manual.get()
            if precio_compra > 0 and precio_venta > 0:
                ganancia = round(((precio_venta - precio_compra) / precio_compra) * 100, 2)
                monto_ganancia = round(precio_venta - precio_compra, 2)
                self.producto_ganancia.set(ganancia)
                self.precio_venta_label.config(text=f"Precio de Venta: Q {precio_venta:,.2f}")
                self.monto_ganancia_label.config(text=f"Ganancia: {ganancia:.2f}% - Q {monto_ganancia:,.2f}")
        except:
            self.precio_venta_label.config(text="Precio de Venta: Q 0.00")
            self.monto_ganancia_label.config(text="Ganancia: Q 0.00")
    
    # ========== GENERADOR DE SKU ==========
    
    def abrir_generador_sku(self):
        """Abre ventana para generar código SKU automáticamente"""
        from tkinter import messagebox
        from src.ui.utils import centrar_ventana, agregar_icono
        
        dialog = tk.Toplevel(self.main_window.root)
        dialog.title("🏷️ Generador de Código SKU - Ingreso de Productos")
        dialog.geometry("750x680")
        dialog.transient(self.main_window.root)
        dialog.withdraw()
        dialog.grab_set()
        agregar_icono(dialog)
        
        # Frame principal con scroll
        main_frame = tb.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        tb.Label(
            main_frame,
            text="🏷️ Generador Automático de Código SKU",
            font=('Segoe UI', 14, 'bold'),
            bootstyle="primary"
        ).pack(pady=(0, 5))
        
        # Descripción
        tb.Label(
            main_frame,
            text="Complete los campos necesarios para generar un código único y descriptivo",
            font=('Segoe UI', 9),
            bootstyle="secondary",
            justify='center'
        ).pack(pady=(0, 10))
        
        # Frame para campos
        canvas_frame = tb.Frame(main_frame)
        canvas_frame.pack(fill='both', expand=True, pady=10)
        
        # Variables para los campos - CARGAR DATOS GUARDADOS
        sku_vars = {
            'nombre': tk.StringVar(value=self.sku_data.get('nombre', '')),
            'categoria': tk.StringVar(value=self.sku_data.get('categoria', '')),
            'marca': tk.StringVar(value=self.sku_data.get('marca', '')),
            'color': tk.StringVar(value=self.sku_data.get('color', '')),
            'tamaño': tk.StringVar(value=self.sku_data.get('tamaño', '')),
            'dibujo': tk.StringVar(value=self.sku_data.get('dibujo', '')),
            'cod_color': tk.StringVar(value=self.sku_data.get('cod_color', ''))
        }
        
        # Crear campos de entrada
        campos = [
            ('Nombre del Producto:', 'nombre', 'Ejemplo: BRILLOS CON LLAVERO', True),
            ('Categoría:', 'categoria', 'Ejemplo: Labial', True),
            ('Marca:', 'marca', 'Ejemplo: Guess', False),
            ('Color:', 'color', 'Ejemplo: ROJO', False),
            ('Tamaño:', 'tamaño', 'Ejemplo: Mediano', False),
            ('Dibujo:', 'dibujo', 'Ejemplo: Gato', False),
            ('Código de Color:', 'cod_color', 'Ejemplo: R20 (se mantiene completo)', False)
        ]
        
        for idx, (label, key, placeholder, required) in enumerate(campos):
            field_frame = tb.Frame(canvas_frame)
            field_frame.pack(fill='x', pady=4)
            
            label_text = f"{label} {'*' if required else ''}"
            label_widget = tb.Label(
                field_frame,
                text=label_text,
                font=('Segoe UI', 10, 'bold' if required else 'normal'),
                anchor='e'
            )
            label_widget.grid(row=0, column=0, sticky='e', padx=(0, 10), ipadx=5)
            
            entry = tb.Entry(
                field_frame,
                textvariable=sku_vars[key],
                width=30,
                font=('Segoe UI', 10)
            )
            entry.grid(row=0, column=1, sticky='w', padx=5)
            
            tb.Label(
                field_frame,
                text=placeholder,
                font=('Segoe UI', 8, 'italic'),
                bootstyle="secondary",
                anchor='w'
            ).grid(row=0, column=2, sticky='w', padx=5)
            
            field_frame.columnconfigure(0, minsize=180)
            field_frame.columnconfigure(1, minsize=280)
            
            sku_vars[key].trace('w', lambda *args: actualizar_preview())
        
        # Separador
        tb.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Preview del SKU generado
        preview_frame = tb.Labelframe(
            main_frame,
            text="📋 Vista Previa del Código SKU",
            padding=10,
            bootstyle="success"
        )
        preview_frame.pack(fill='x', pady=5)
        
        sku_preview_var = tk.StringVar(value="Complete los campos para generar el código...")
        sku_preview_label = tb.Label(
            preview_frame,
            textvariable=sku_preview_var,
            font=('Segoe UI', 12, 'bold'),
            bootstyle="success",
            wraplength=650
        )
        sku_preview_label.pack(pady=3)
        
        tb.Label(
            preview_frame,
            text="📌 El -000 se reemplazará con el ID del producto al guardarlo",
            font=('Segoe UI', 8, 'italic'),
            bootstyle="warning"
        ).pack(pady=2)
        
        def generar_codigo_sku():
            """Genera el código SKU basado en los campos con correlativo basado en ID"""
            partes = []
            
            for key in ['nombre', 'categoria', 'marca', 'color', 'tamaño', 'dibujo', 'cod_color']:
                valor = sku_vars[key].get().strip().upper()
                if valor:
                    if key == 'cod_color':
                        partes.append(valor)
                    else:
                        palabras = valor.split()
                        if palabras:
                            if len(palabras) == 1:
                                partes.append(palabras[0][:3])
                            else:
                                partes.append(palabras[0][:3])
            
            if partes:
                codigo_base = '-'.join(partes)
                
                if self.producto_seleccionado:
                    codigo_actual = self.producto_codigo.get().strip()
                    if codigo_actual:
                        partes_actual = codigo_actual.split('-')
                        if partes_actual and len(partes_actual) > 1:
                            ultima_parte = partes_actual[-1]
                            if ultima_parte.isdigit() and len(ultima_parte) == 3:
                                return f"{codigo_base}-{ultima_parte}"
                
                return f"{codigo_base}-000"
            return ""
        
        def actualizar_preview():
            """Actualiza la vista previa del SKU"""
            codigo = generar_codigo_sku()
            if codigo:
                sku_preview_var.set(codigo)
            else:
                sku_preview_var.set("Complete los campos para generar el código...")
        
        def aceptar_y_continuar():
            """Acepta los datos del formulario y continúa en el formulario principal"""
            nombre = sku_vars['nombre'].get().strip()
            categoria = sku_vars['categoria'].get().strip()
            
            if not nombre:
                messagebox.showwarning("⚠️ Campo Requerido", "Debe completar el campo 'Nombre del Producto'")
                return
            
            if not categoria:
                messagebox.showwarning("⚠️ Campo Requerido", "Debe completar el campo 'Categoría'")
                return
            
            codigo = generar_codigo_sku()
            if codigo:
                for key in sku_vars:
                    self.sku_data[key] = sku_vars[key].get()
                
                self.codigo_entry.config(state='normal')
                self.producto_codigo.set(codigo)
                self.codigo_entry.config(state='disabled')
                
                self.producto_nombre.set(sku_vars['nombre'].get())
                self.producto_categoria.set(sku_vars['categoria'].get())
                
                dialog.destroy()
                
                self.main_window.notebook.select(0)
                
                messagebox.showinfo("✅ Datos Aceptados", 
                    f"Código SKU generado: {codigo}\n\n"
                    "Complete los campos de precio y ganancia, luego presione:\n"
                    "• '➕ Crear' para nuevo producto\n"
                    "• '🔄 Actualizar' para guardar cambios")
            else:
                messagebox.showwarning("⚠️ Campos Incompletos", "Complete al menos el Nombre y la Categoría para generar el código")
        
        def actualizar_producto_desde_generador():
            """Carga los datos del generador SKU al formulario principal para editar precios"""
            nombre = sku_vars['nombre'].get().strip()
            categoria = sku_vars['categoria'].get().strip()
            
            if not nombre:
                messagebox.showwarning("⚠️ Campo Requerido", "Debe completar el campo 'Nombre del Producto'")
                return
            
            if not categoria:
                messagebox.showwarning("⚠️ Campo Requerido", "Debe completar el campo 'Categoría'")
                return
            
            if not self.producto_seleccionado:
                messagebox.showwarning("⚠️ Sin Producto", "No hay un producto seleccionado para actualizar.\n\nUse 'Aceptar y Continuar' para crear uno nuevo.")
                return
            
            codigo = generar_codigo_sku()
            if codigo:
                # Guardar datos SKU
                for key in sku_vars:
                    self.sku_data[key] = sku_vars[key].get()
                
                # Actualizar campos en el formulario principal
                self.codigo_entry.config(state='normal')
                self.producto_codigo.set(codigo)
                self.codigo_entry.config(state='disabled')
                
                self.producto_nombre.set(sku_vars['nombre'].get())
                self.producto_categoria.set(sku_vars['categoria'].get())
                
                # Cerrar diálogo
                dialog.destroy()
                
                # Cambiar a la pestaña de productos
                self.main_window.notebook.select(0)
                
                # Mostrar mensaje informativo
                messagebox.showinfo("✅ Datos Actualizados", 
                    f"Código SKU actualizado: {codigo}\n\n"
                    "Los datos del producto han sido cargados en el formulario.\n\n"
                    "Puede modificar:\n"
                    "• Precio de Compra\n"
                    "• % Ganancia / Precio de Venta\n\n"
                    "Luego presione '🔄 Actualizar' para guardar los cambios.")
        
        def limpiar_campos_sku():
            """Limpia todos los campos del generador"""
            for key in sku_vars:
                sku_vars[key].set('')
            actualizar_preview()
        
        # Actualizar preview inicial si hay datos
        actualizar_preview()
        
        # Botones
        buttons_frame = tb.Frame(main_frame)
        buttons_frame.pack(pady=10)
        
        if self.producto_seleccionado:
            tb.Button(
                buttons_frame,
                text="🔄 Actualizar Producto",
                command=actualizar_producto_desde_generador,
                bootstyle="success",
                width=25
            ).pack(side='left', padx=5)
        else:
            tb.Button(
                buttons_frame,
                text="✅ Aceptar y Continuar",
                command=aceptar_y_continuar,
                bootstyle="success",
                width=25
            ).pack(side='left', padx=5)
        
        tb.Button(
            buttons_frame,
            text="🗑️ Limpiar Campos",
            command=limpiar_campos_sku,
            bootstyle="warning",
            width=20
        ).pack(side='left', padx=5)
        
        tb.Button(
            buttons_frame,
            text="✗ Cancelar",
            command=dialog.destroy,
            bootstyle="secondary",
            width=20
        ).pack(side='left', padx=5)
        
        # Centrar y mostrar
        centrar_ventana(dialog)
        dialog.deiconify()
    
    # ========== MÉTODOS DE OPERACIONES CRUD ==========
    
    def crear_producto(self):
        """Crea un nuevo producto"""
        try:
            codigo = self.producto_codigo.get().strip()
            nombre = self.producto_nombre.get().strip()
            categoria = self.producto_categoria.get().strip()
            precio_compra = self.producto_precio_compra.get()
            ganancia = self.producto_ganancia.get()
            
            # Extraer datos del SKU
            marca = self.sku_data.get('marca', '')
            color = self.sku_data.get('color', '')
            tamaño = self.sku_data.get('tamaño', '')
            dibujo = self.sku_data.get('dibujo', '')
            cod_color = self.sku_data.get('cod_color', '')
            
            exito, mensaje = self.controller.crear_producto(
                codigo, nombre, categoria, precio_compra, ganancia,
                marca, color, tamaño, dibujo, cod_color
            )
            
            if exito:
                # Actualizar código con ID real si es necesario
                match = re.search(r'ID:\s*(\d+)', mensaje)
                if match and codigo.endswith('-000'):
                    producto_id = int(match.group(1))
                    nuevo_codigo = codigo.replace('-000', f'-{producto_id:03d}')
                    self.controller.actualizar_producto(
                        producto_id, nuevo_codigo, nombre, categoria,
                        precio_compra, ganancia, marca, color, tamaño, dibujo, cod_color
                    )
                    mensaje = f"Producto creado exitosamente\nCódigo: {nuevo_codigo}"
                
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.refresh()
                self.main_window.refresh_combos()
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
            
            # Extraer datos del SKU
            marca = self.sku_data.get('marca', '')
            color = self.sku_data.get('color', '')
            tamaño = self.sku_data.get('tamaño', '')
            dibujo = self.sku_data.get('dibujo', '')
            cod_color = self.sku_data.get('cod_color', '')
            
            exito, mensaje = self.controller.actualizar_producto(
                self.producto_seleccionado, codigo, nombre, categoria,
                precio_compra, ganancia, marca, color, tamaño, dibujo, cod_color
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.refresh()
                self.main_window.refresh_combos()
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def seleccionar_producto(self, event):
        """Selecciona un producto de la lista para edición (doble clic)"""
        try:
            seleccion = self.productos_tree.selection()
            if seleccion:
                item = self.productos_tree.item(seleccion[0])
                producto_id = int(item['values'][0])
                producto = self.controller.obtener_producto_por_id(producto_id)
                
                if producto:
                    # Guardar ID para edición
                    self.producto_seleccionado = producto_id
                    
                    # Cargar datos SKU
                    self.sku_data = {
                        'nombre': producto.get('nombre', ''),
                        'categoria': producto.get('categoria', ''),
                        'marca': producto.get('marca', ''),
                        'color': producto.get('color', ''),
                        'tamaño': producto.get('tamaño', ''),
                        'dibujo': producto.get('dibujo', ''),
                        'cod_color': producto.get('cod_color', '')
                    }
                    
                    # Cargar al formulario
                    self.producto_codigo.set(producto.get('codigo', ''))
                    self.producto_nombre.set(producto['nombre'])
                    self.producto_categoria.set(producto.get('categoria', ''))
                    self.producto_precio_compra.set(producto['precio_compra'])
                    self.producto_ganancia.set(producto['porcentaje_ganancia'])
                    self.producto_precio_venta_manual.set(producto['precio_venta'])
                    self.producto_tipo_calculo.set("precio")
                    self.cambiar_tipo_calculo()
                    
                    # Abrir generador SKU
                    self.abrir_generador_sku()
        except:
            pass
    
    def desactivar_producto(self):
        """Marca un producto como inactivo"""
        self.productos_tree.focus_set()
        selection = self.productos_tree.selection()
        
        if not selection:
            focused_item = self.productos_tree.focus()
            if focused_item:
                selection = (focused_item,)
        
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto")
            return
        
        try:
            item = self.productos_tree.item(selection[0])
            if not item or 'values' not in item or len(item['values']) < 3:
                messagebox.showwarning("Advertencia", "No se pudo obtener la información del producto")
                return
            
            producto_id = item['values'][0]
            producto_nombre = item['values'][2]
            
            if messagebox.askyesno("Confirmar",
                f"¿Está seguro de marcar como INACTIVO el producto:\n\n'{producto_nombre}'?\n\n" +
                "El producto no aparecerá en compras ni ventas."):
                
                exito, mensaje = self.controller.desactivar_producto(producto_id)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.refresh()
                else:
                    messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def activar_producto(self):
        """Marca un producto como activo"""
        self.productos_tree.focus_set()
        selection = self.productos_tree.selection()
        
        if not selection:
            focused_item = self.productos_tree.focus()
            if focused_item:
                selection = (focused_item,)
        
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto")
            return
        
        try:
            item = self.productos_tree.item(selection[0])
            if not item or 'values' not in item or len(item['values']) < 3:
                messagebox.showwarning("Advertencia", "No se pudo obtener la información del producto")
                return
            
            producto_id = item['values'][0]
            producto_nombre = item['values'][2]
            
            if messagebox.askyesno("Confirmar",
                f"¿Está seguro de ACTIVAR el producto:\n\n'{producto_nombre}'?"):
                
                exito, mensaje = self.controller.activar_producto(producto_id)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.refresh()
                else:
                    messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def refresh(self):
        """Actualiza la lista de productos"""
        # Limpiar el treeview
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        
        # Cargar productos según filtro
        filtro = self.producto_filtro.get()
        
        if filtro == 'activos':
            productos = self.controller.obtener_productos_activos()
        elif filtro == 'inactivos':
            productos = self.controller.obtener_productos_inactivos()
        else:
            productos = self.controller.obtener_productos()
        
        # Filtrar por búsqueda
        busqueda = self.producto_search.get().lower()
        if busqueda:
            productos = [p for p in productos if busqueda in p['nombre'].lower()]
        
        # Llenar tabla
        for i, producto in enumerate(productos):
            tags = []
            activo = producto.get('activo', 1)
            
            # Determinar tags
            if activo == 0:
                tags = ['inactivo']
            elif producto['stock_actual'] <= 5:
                tags = ['lowstock']
            else:
                tags = ['evenrow' if i % 2 == 0 else 'oddrow']
            
            # Calcular monto de ganancia
            monto_ganancia = producto.get('monto_ganancia', 0)
            if monto_ganancia == 0 or monto_ganancia is None:
                monto_ganancia = round(producto['precio_venta'] - producto['precio_compra'], 2)
            
            estado_texto = "ACTIVO" if activo == 1 else "INACTIVO"
            
            self.productos_tree.insert('', 'end', values=(
                producto['id'],
                producto.get('codigo', ''),
                producto['nombre'],
                producto.get('categoria', ''),
                producto.get('marca', ''),
                producto.get('color', ''),
                producto.get('tamaño', ''),
                f"Q {producto['precio_compra']:,.2f}",
                f"{producto['porcentaje_ganancia']:.2f}%",
                f"Q {monto_ganancia:,.2f}",
                f"Q {producto['precio_venta']:,.2f}",
                f"{producto['stock_actual']:,}",
                estado_texto
            ), tags=tags)
    
    def limpiar_formulario(self):
        """Limpia el formulario de productos"""
        self.producto_codigo.set("")
        self.producto_nombre.set("")
        self.producto_categoria.set("")
        self.producto_precio_compra.set(0)
        self.producto_ganancia.set(0)
        self.producto_precio_venta_manual.set(0)
        self.producto_seleccionado = None
        self.sku_data = {}
        
        # Limpiar los labels de precio de venta y ganancia
        self.precio_venta_label.config(text="Precio de Venta: Q 0.00")
        self.monto_ganancia_label.config(text="Ganancia: Q 0.00")
    
    # ========== MENÚ CONTEXTUAL ==========
    
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
        import tkinter as tk
        menu = tk.Menu(self.main_window.root, tearoff=0)
        
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
                # Llamar al método de main_window que muestra los detalles
                self.main_window.mostrar_ventana_detalles(producto)
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
                self.producto_tipo_calculo.set("precio")  # Por defecto mostrar precio
                self.cambiar_tipo_calculo()
                
                # Abrir el generador SKU con los datos cargados
                self.abrir_generador_sku()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar producto para edición: {str(e)}")

