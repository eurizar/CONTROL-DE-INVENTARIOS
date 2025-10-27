"""
Módulo de gestión de clientes
Permite crear, editar, buscar y listar clientes
"""
import ttkbootstrap as tb
from tkinter import messagebox
from datetime import datetime


class ClientesTab:
    """Pestaña de gestión de clientes"""
    
    def __init__(self, parent_frame, controller, main_window):
        self.parent_frame = parent_frame
        self.controller = controller
        self.main_window = main_window
        
        # Variables de formulario
        self.setup_variables()
        
        # Variables de control
        self.cliente_seleccionado = None
        
        # Crear interfaz
        self.create_ui()
    
    def setup_variables(self):
        """Inicializa las variables del formulario"""
        self.cliente_nombre = tb.StringVar()
        self.cliente_nit = tb.StringVar()
        self.cliente_direccion = tb.StringVar()
        self.cliente_telefono = tb.StringVar()
        self.cliente_busqueda = tb.StringVar()
    
    def create_ui(self):
        """Crea la interfaz de usuario de clientes"""
        # Frame principal con dos paneles
        paned = tb.PanedWindow(self.parent_frame, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Formulario
        self.crear_formulario(paned)
        
        # Panel derecho - Lista de clientes
        self.crear_tabla(paned)
    
    def crear_formulario(self, paned):
        """Crea el formulario de datos del cliente"""
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
        
        tb.Label(form_inner, text="Dirección:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky='w', pady=5)
        tb.Entry(form_inner, textvariable=self.cliente_direccion, width=40, font=("Segoe UI", 10)).grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        tb.Label(form_inner, text="Teléfono:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky='w', pady=5)
        tb.Entry(form_inner, textvariable=self.cliente_telefono, width=40, font=("Segoe UI", 10)).grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        
        form_inner.columnconfigure(1, weight=1)
        
        # Botones
        button_frame = tb.Frame(form_inner)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tb.Button(button_frame, text="➕ Crear Cliente", bootstyle="success", command=self.crear_cliente).pack(side='left', padx=5)
        tb.Button(button_frame, text="✏️ Actualizar", bootstyle="warning", command=self.actualizar_cliente).pack(side='left', padx=5)
        tb.Button(button_frame, text="🔄 Limpiar", bootstyle="secondary", command=self.limpiar_formulario).pack(side='left', padx=5)
    
    def crear_tabla(self, paned):
        """Crea la tabla de clientes"""
        list_panel = tb.LabelFrame(paned, text="Lista de Clientes", bootstyle="info")
        paned.add(list_panel, weight=2)
        
        # Barra de búsqueda
        search_frame = tb.Frame(list_panel)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tb.Label(search_frame, text="🔍 Buscar:", font=("Segoe UI", 10, "bold")).pack(side='left', padx=5)
        search_entry = tb.Entry(search_frame, textvariable=self.cliente_busqueda, width=30, font=("Segoe UI", 10))
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.buscar_clientes())
        
        tb.Button(search_frame, text="🔄 Mostrar Todos", bootstyle="info-outline", command=self.refresh).pack(side='left', padx=5)
        
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
        self.clientes_tree.heading('ID', text='ID', command=lambda: self.sort_column('ID', False))
        self.clientes_tree.heading('Nombre', text='Nombre', command=lambda: self.sort_column('Nombre', False))
        self.clientes_tree.heading('NIT/DPI', text='NIT o DPI', command=lambda: self.sort_column('NIT/DPI', False))
        self.clientes_tree.heading('Dirección', text='Dirección', command=lambda: self.sort_column('Dirección', False))
        self.clientes_tree.heading('Teléfono', text='Teléfono', command=lambda: self.sort_column('Teléfono', False))
        self.clientes_tree.heading('Fecha Registro', text='Fecha Registro', command=lambda: self.sort_column('Fecha Registro', False))
        
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
        
        # Cargar datos iniciales
        self.refresh()
    
    # ========== MÉTODOS DE OPERACIONES CRUD ==========
    
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
            self.limpiar_formulario()
            self.refresh()
            self.main_window.refresh_combos()
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
            self.limpiar_formulario()
            self.refresh()
            self.main_window.refresh_combos()
        else:
            messagebox.showerror("Error", mensaje)
    
    def on_cliente_select(self, event):
        """Maneja la selección de un cliente al hacer doble clic"""
        selection = self.clientes_tree.selection()
        if selection:
            item = self.clientes_tree.item(selection[0])
            values = item['values']
            
            self.cliente_seleccionado = values[0]
            self.cliente_nombre.set(values[1])
            self.cliente_nit.set(values[2])
            self.cliente_direccion.set(values[3])
            self.cliente_telefono.set(values[4])
    
    def buscar_clientes(self):
        """Busca clientes por nombre o NIT"""
        busqueda = self.cliente_busqueda.get()
        clientes = self.controller.buscar_cliente(busqueda)
        
        # Limpiar tabla
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        # Llenar tabla
        for i, cli in enumerate(clientes):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            fecha_formateada = self._formatear_fecha(cli['fecha_registro'])
            
            self.clientes_tree.insert('', 'end', values=(
                cli['id'],
                cli['nombre'],
                cli['nit_dpi'],
                cli['direccion'],
                cli['telefono'],
                fecha_formateada
            ), tags=(tag,))
    
    def refresh(self):
        """Actualiza la lista de clientes"""
        # Limpiar el treeview
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        # Cargar clientes
        clientes = self.controller.obtener_clientes()
        for i, cli in enumerate(clientes):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            fecha_formateada = self._formatear_fecha(cli['fecha_registro'])
            
            self.clientes_tree.insert('', 'end', values=(
                cli['id'],
                cli['nombre'],
                cli['nit_dpi'],
                cli['direccion'],
                cli['telefono'],
                fecha_formateada
            ), tags=(tag,))
    
    def limpiar_formulario(self):
        """Limpia el formulario de clientes"""
        self.cliente_nombre.set("")
        self.cliente_nit.set("")
        self.cliente_direccion.set("")
        self.cliente_telefono.set("")
        self.cliente_seleccionado = None
        self.cliente_nombre_entry.focus()
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def sort_column(self, col, reverse):
        """Ordena la tabla por columna al hacer clic en el encabezado"""
        from ..utils import sort_treeview
        sort_treeview(self.clientes_tree, col, reverse)
    
    def _formatear_fecha(self, fecha_str):
        """Formatea una fecha a dd/mm/yyyy"""
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
            return fecha_obj.strftime('%d/%m/%Y')
        except:
            return fecha_str.split()[0] if ' ' in fecha_str else fecha_str
