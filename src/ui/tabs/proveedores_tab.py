"""
Módulo de gestión de proveedores
Permite crear, editar, buscar y listar proveedores
"""
import ttkbootstrap as tb
from tkinter import messagebox
from datetime import datetime


class ProveedoresTab:
    """Pestaña de gestión de proveedores"""
    
    def __init__(self, parent_frame, controller, main_window):
        self.parent_frame = parent_frame
        self.controller = controller
        self.main_window = main_window
        
        # Variables de formulario
        self.setup_variables()
        
        # Variables de control
        self.proveedor_seleccionado = None
        
        # Crear interfaz
        self.create_ui()
    
    def setup_variables(self):
        """Inicializa las variables del formulario"""
        self.proveedor_nombre = tb.StringVar()
        self.proveedor_nit = tb.StringVar()
        self.proveedor_direccion = tb.StringVar()
        self.proveedor_telefono = tb.StringVar()
        self.proveedor_busqueda = tb.StringVar()
    
    def create_ui(self):
        """Crea la interfaz de usuario de proveedores"""
        # Frame principal con dos paneles
        paned = tb.PanedWindow(self.parent_frame, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Formulario
        self.crear_formulario(paned)
        
        # Panel derecho - Lista de proveedores
        self.crear_tabla(paned)
    
    def crear_formulario(self, paned):
        """Crea el formulario de datos del proveedor"""
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
        
        tb.Label(form_inner, text="Dirección:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky='w', pady=5)
        tb.Entry(form_inner, textvariable=self.proveedor_direccion, width=40, font=("Segoe UI", 10)).grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        tb.Label(form_inner, text="Teléfono:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky='w', pady=5)
        tb.Entry(form_inner, textvariable=self.proveedor_telefono, width=40, font=("Segoe UI", 10)).grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        
        form_inner.columnconfigure(1, weight=1)
        
        # Botones
        button_frame = tb.Frame(form_inner)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tb.Button(button_frame, text="➕ Crear Proveedor", bootstyle="success", command=self.crear_proveedor).pack(side='left', padx=5)
        tb.Button(button_frame, text="✏️ Actualizar", bootstyle="warning", command=self.actualizar_proveedor).pack(side='left', padx=5)
        tb.Button(button_frame, text="🔄 Limpiar", bootstyle="secondary", command=self.limpiar_formulario).pack(side='left', padx=5)
    
    def crear_tabla(self, paned):
        """Crea la tabla de proveedores"""
        list_panel = tb.LabelFrame(paned, text="Lista de Proveedores", bootstyle="info")
        paned.add(list_panel, weight=2)
        
        # Barra de búsqueda
        search_frame = tb.Frame(list_panel)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tb.Label(search_frame, text="🔍 Buscar:", font=("Segoe UI", 10, "bold")).pack(side='left', padx=5)
        search_entry = tb.Entry(search_frame, textvariable=self.proveedor_busqueda, width=30, font=("Segoe UI", 10))
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.buscar_proveedores())
        
        tb.Button(search_frame, text="🔄 Mostrar Todos", bootstyle="info-outline", command=self.refresh).pack(side='left', padx=5)
        
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
        self.proveedores_tree.heading('ID', text='ID', command=lambda: self.sort_column('ID', False))
        self.proveedores_tree.heading('Nombre', text='Nombre', command=lambda: self.sort_column('Nombre', False))
        self.proveedores_tree.heading('NIT/DPI', text='NIT o DPI', command=lambda: self.sort_column('NIT/DPI', False))
        self.proveedores_tree.heading('Dirección', text='Dirección', command=lambda: self.sort_column('Dirección', False))
        self.proveedores_tree.heading('Teléfono', text='Teléfono', command=lambda: self.sort_column('Teléfono', False))
        self.proveedores_tree.heading('Fecha Registro', text='Fecha Registro', command=lambda: self.sort_column('Fecha Registro', False))
        
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
        
        # Cargar datos iniciales
        self.refresh()
    
    # ========== MÉTODOS DE OPERACIONES CRUD ==========
    
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
            self.limpiar_formulario()
            self.refresh()
            self.main_window.refresh_combos()
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
            self.limpiar_formulario()
            self.refresh()
            self.main_window.refresh_combos()
        else:
            messagebox.showerror("Error", mensaje)
    
    def on_proveedor_select(self, event):
        """Maneja la selección de un proveedor al hacer doble clic"""
        selection = self.proveedores_tree.selection()
        if selection:
            item = self.proveedores_tree.item(selection[0])
            values = item['values']
            
            self.proveedor_seleccionado = values[0]
            self.proveedor_nombre.set(values[1])
            self.proveedor_nit.set(values[2])
            self.proveedor_direccion.set(values[3])
            self.proveedor_telefono.set(values[4])
    
    def buscar_proveedores(self):
        """Busca proveedores por nombre o NIT"""
        busqueda = self.proveedor_busqueda.get()
        proveedores = self.controller.buscar_proveedor(busqueda)
        
        # Limpiar tabla
        for item in self.proveedores_tree.get_children():
            self.proveedores_tree.delete(item)
        
        # Llenar tabla
        for i, prov in enumerate(proveedores):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            fecha_formateada = self._formatear_fecha(prov['fecha_registro'])
            
            self.proveedores_tree.insert('', 'end', values=(
                prov['id'],
                prov['nombre'],
                prov['nit_dpi'],
                prov['direccion'],
                prov['telefono'],
                fecha_formateada
            ), tags=(tag,))
    
    def refresh(self):
        """Actualiza la lista de proveedores"""
        # Limpiar el treeview
        for item in self.proveedores_tree.get_children():
            self.proveedores_tree.delete(item)
        
        # Cargar proveedores
        proveedores = self.controller.obtener_proveedores()
        for i, prov in enumerate(proveedores):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            fecha_formateada = self._formatear_fecha(prov['fecha_registro'])
            
            self.proveedores_tree.insert('', 'end', values=(
                prov['id'],
                prov['nombre'],
                prov['nit_dpi'],
                prov['direccion'],
                prov['telefono'],
                fecha_formateada
            ), tags=(tag,))
    
    def limpiar_formulario(self):
        """Limpia el formulario de proveedores"""
        self.proveedor_nombre.set("")
        self.proveedor_nit.set("")
        self.proveedor_direccion.set("")
        self.proveedor_telefono.set("")
        self.proveedor_seleccionado = None
        self.proveedor_nombre_entry.focus()
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def sort_column(self, col, reverse):
        """Ordena la tabla por columna al hacer clic en el encabezado"""
        from ..utils import sort_treeview
        sort_treeview(self.proveedores_tree, col, reverse)
    
    def _formatear_fecha(self, fecha_str):
        """Formatea una fecha a dd/mm/yyyy"""
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
            return fecha_obj.strftime('%d/%m/%Y')
        except:
            return fecha_str.split()[0] if ' ' in fecha_str else fecha_str
