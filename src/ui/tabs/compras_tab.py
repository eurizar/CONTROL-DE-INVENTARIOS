"""
Módulo de gestión de compras
Permite registrar compras de mercadería a proveedores con control de vencimientos
"""
import ttkbootstrap as tb
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
from ttkbootstrap import DateEntry
from src.ui.utils.ui_helpers import centrar_ventana, agregar_icono, configurar_navegacion_calendario


class ComprasTab:
    """Pestaña de gestión de compras"""
    
    def __init__(self, parent_frame, controller, main_window):
        self.parent_frame = parent_frame
        self.controller = controller
        self.main_window = main_window
        
        # Variables de formulario
        self.setup_variables()
        
        # Variables de control
        self.compra_proveedor_id = None
        self.compra_producto_id = None
        
        # Crear interfaz
        self.create_ui()
    
    def setup_variables(self):
        """Inicializa las variables del formulario"""
        self.compra_proveedor_busqueda = tb.StringVar()
        self.compra_no_documento = tb.StringVar()
        self.compra_producto_busqueda = tb.StringVar()
        self.compra_cantidad = tb.IntVar(value=0)
        self.compra_precio = tb.DoubleVar(value=0.0)
        self.compra_es_perecedero = tb.BooleanVar(value=False)
        self.compra_fecha_vencimiento = tb.StringVar()
        self.mismo_documento = tb.BooleanVar(value=False)  # Nuevo: mantener mismo documento
    
    def create_ui(self):
        """Crea la interfaz de usuario de compras"""
        # Formulario de compras
        self.crear_formulario()
        
        # Lista de compras
        self.crear_tabla()
    
    def crear_formulario(self):
        """Crea el formulario de registro de compras"""
        form_frame = tb.Labelframe(
            self.parent_frame,
            text="📥 Registrar Compra de Mercadería",
            padding=20,
            bootstyle="success"
        )
        form_frame.pack(fill='x', padx=15, pady=15)
        
        # FILA 1: Proveedor y No. Documento
        tb.Label(form_frame, text="Proveedor: *", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=8)
        
        prov_search_frame = tb.Frame(form_frame)
        prov_search_frame.grid(row=0, column=1, padx=10, pady=8, sticky='ew')
        
        self.compra_proveedor_entry = tb.Entry(
            prov_search_frame,
            textvariable=self.compra_proveedor_busqueda,
            width=30,
            font=('Segoe UI', 10)
        )
        self.compra_proveedor_entry.pack(side='left', fill='x', expand=True)
        self.compra_proveedor_entry.bind('<KeyRelease>', self.autocompletar_proveedor)
        
        tb.Button(
            prov_search_frame,
            text="🔍",
            command=self.buscar_proveedor,
            bootstyle="info-outline",
            width=3
        ).pack(side='left', padx=5)
        
        # Check para indicar proveedor seleccionado
        self.compra_proveedor_label = tb.Label(prov_search_frame, text="", font=('Segoe UI', 12), bootstyle="success")
        self.compra_proveedor_label.pack(side='left', padx=5)
        
        tb.Label(form_frame, text="No. Documento: *", font=('Segoe UI', 10, 'bold')).grid(row=0, column=2, sticky='w', padx=(50, 10), pady=8)
        
        doc_frame = tb.Frame(form_frame)
        doc_frame.grid(row=0, column=3, padx=10, pady=8, sticky='ew')
        
        tb.Entry(doc_frame, textvariable=self.compra_no_documento, width=30, font=('Segoe UI', 10)).pack(side='left')
        
        tb.Checkbutton(
            doc_frame,
            text="Mismo documento",
            variable=self.mismo_documento,
            bootstyle="info-round-toggle"
        ).pack(side='left', padx=10)
        
        # FILA 2: Producto y Cantidad
        tb.Label(form_frame, text="Producto: *", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=10, pady=8)
        
        prod_search_frame = tb.Frame(form_frame)
        prod_search_frame.grid(row=1, column=1, padx=10, pady=8, sticky='ew')
        
        self.compra_producto_entry = tb.Entry(
            prod_search_frame,
            textvariable=self.compra_producto_busqueda,
            width=30,
            font=('Segoe UI', 10)
        )
        self.compra_producto_entry.pack(side='left', fill='x', expand=True)
        self.compra_producto_entry.bind('<KeyRelease>', self.autocompletar_producto)
        
        tb.Button(
            prod_search_frame,
            text="🔍",
            command=self.buscar_producto,
            bootstyle="info-outline",
            width=3
        ).pack(side='left', padx=5)
        
        # Check para indicar producto seleccionado
        self.compra_producto_label = tb.Label(prod_search_frame, text="", font=('Segoe UI', 12), bootstyle="success")
        self.compra_producto_label.pack(side='left', padx=5)
        
        tb.Label(form_frame, text="Cantidad: *", font=('Segoe UI', 10, 'bold')).grid(row=1, column=2, sticky='w', padx=(50, 10), pady=8)
        tb.Entry(form_frame, textvariable=self.compra_cantidad, width=8, font=('Segoe UI', 10)).grid(row=1, column=3, padx=10, pady=8, sticky='w')
        
        # FILA 3: Precio y Fecha
        tb.Label(form_frame, text="Precio Unitario (Q):", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=10, pady=8)
        
        self.compra_precio_entry = tb.Entry(
            form_frame,
            textvariable=self.compra_precio,
            width=18,
            font=('Segoe UI', 10),
            state='readonly'
        )
        self.compra_precio_entry.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        
        tb.Label(form_frame, text="Fecha: *", font=('Segoe UI', 10, 'bold')).grid(row=2, column=2, sticky='w', padx=(50, 10), pady=8)
        
        self.compra_fecha_cal = DateEntry(
            form_frame,
            dateformat='%d/%m/%Y',
            width=18,
            bootstyle="success",
            firstweekday=0,
            startdate=None
        )
        self.compra_fecha_cal.grid(row=2, column=3, padx=10, pady=8, sticky='w')
        
        # FILA 4: Perecedero y Vencimiento
        self.compra_perecedero_check = tb.Checkbutton(
            form_frame,
            text="¿Es perecedero?",
            variable=self.compra_es_perecedero,
            command=self.toggle_vencimiento,
            bootstyle="success-round-toggle"
        )
        self.compra_perecedero_check.grid(row=3, column=0, sticky='w', padx=10, pady=8)
        
        tb.Label(form_frame, text="Fecha Vencimiento:", font=('Segoe UI', 10, 'bold')).grid(row=3, column=2, sticky='w', padx=(50, 10), pady=8)
        
        self.compra_vencimiento_cal = DateEntry(
            form_frame,
            dateformat='%d/%m/%Y',
            width=18,
            bootstyle="warning",
            firstweekday=0,
            startdate=None
        )
        self.compra_vencimiento_cal.grid(row=3, column=3, padx=10, pady=8, sticky='w')
        self.compra_vencimiento_cal.entry.configure(state='disabled')
        self.compra_vencimiento_cal.button.configure(state='disabled')
        
        # FILA 5: Total y nota
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
        self.compra_cantidad.trace('w', self.calcular_total)
        self.compra_precio.trace('w', self.calcular_total)
        
        # Botón registrar
        tb.Button(
            form_frame,
            text="✅ Registrar Compra",
            command=self.registrar_compra,
            bootstyle="success",
            width=25
        ).grid(row=5, column=0, columnspan=4, pady=15)
        
        # Configurar navegación de calendarios
        self.main_window.root.after(100, lambda: configurar_navegacion_calendario(self.compra_fecha_cal))
        self.main_window.root.after(100, lambda: configurar_navegacion_calendario(self.compra_vencimiento_cal))
    
    def crear_tabla(self):
        """Crea la tabla de historial de compras"""
        list_frame = tb.Labelframe(
            self.parent_frame,
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
        self.compra_search.bind('<KeyRelease>', lambda e: self.refresh())
        
        tb.Label(
            search_frame,
            text="Busca por: Proveedor, Producto, No. Doc o Fecha",
            font=('Segoe UI', 8, 'italic'),
            bootstyle="secondary"
        ).pack(side='left', padx=10)
        
        # Treeview
        tree_frame = tb.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Proveedor', 'No. Doc', 'Producto', 'Cantidad', 'Precio Unit.', 'Total', 'Fecha', 'Vencimiento')
        self.compras_tree = tb.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        column_widths = {
            'ID': 50, 'Proveedor': 150, 'No. Doc': 100, 'Producto': 150,
            'Cantidad': 80, 'Precio Unit.': 100, 'Total': 100, 'Fecha': 150, 'Vencimiento': 120
        }
        
        for col in columns:
            self.compras_tree.heading(col, text=col, command=lambda c=col: self.main_window.sort_treeview(self.compras_tree, c, False))
            anchor = 'center' if col not in ['Producto', 'Proveedor', 'No. Doc'] else 'w'
            self.compras_tree.column(col, width=column_widths[col], anchor=anchor)
        
        scrollbar_y = tb.Scrollbar(tree_frame, orient='vertical', command=self.compras_tree.yview, bootstyle="success-round")
        scrollbar_x = tb.Scrollbar(tree_frame, orient='horizontal', command=self.compras_tree.xview, bootstyle="success-round")
        self.compras_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.compras_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Tags de colores
        self.compras_tree.tag_configure('evenrow', background='#f0f0f0')
        self.compras_tree.tag_configure('oddrow', background='#ffffff')
        self.compras_tree.tag_configure('vencido', background='#ff6b6b', foreground='white')
        self.compras_tree.tag_configure('critico', background='#ffa502', foreground='black')
        self.compras_tree.tag_configure('advertencia', background='#ffd93d', foreground='black')
        
        # Tags hover (versiones más claras para efecto hover)
        self.compras_tree.tag_configure('vencido_hover', background='#ff8585', foreground='white')
        self.compras_tree.tag_configure('critico_hover', background='#ffb733', foreground='black')
        self.compras_tree.tag_configure('advertencia_hover', background='#ffe066', foreground='black')
        
        # Variables para controlar hover
        self.last_hovered_item = None
        self.original_tag = None
        
        # Eventos
        self.compras_tree.bind('<Button-3>', lambda e: self.main_window.mostrar_menu_compras(e))
        self.compras_tree.bind('<Double-1>', lambda e: self.editar_compra_perecedero())
        self.compras_tree.bind('<Motion>', self.on_tree_motion)
        self.compras_tree.bind('<Leave>', self.on_tree_leave)
        
        # Botones adicionales
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
        
        # Cargar datos iniciales
        self.refresh()
    
    # ========== MÉTODOS DE OPERACIONES ==========
    
    def toggle_vencimiento(self):
        """Habilita o deshabilita el campo de fecha de vencimiento"""
        if self.compra_es_perecedero.get():
            self.compra_vencimiento_cal.entry.configure(state='normal')
            self.compra_vencimiento_cal.button.configure(state='normal')
        else:
            self.compra_vencimiento_cal.entry.configure(state='disabled')
            self.compra_vencimiento_cal.button.configure(state='disabled')
            self.compra_fecha_vencimiento.set('')
    
    def calcular_total(self, *args):
        """Calcula el total de la compra"""
        try:
            cantidad = self.compra_cantidad.get()
            precio = self.compra_precio.get()
            total = cantidad * precio
            self.compra_total_label.config(text=f"Total: Q {total:,.2f}")
        except:
            self.compra_total_label.config(text="Total: Q 0.00")
    
    def registrar_compra(self):
        """Registra una nueva compra"""
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
            
            # Obtener fecha y hora
            fecha_cal = self.compra_fecha_cal.entry.get()
            hora_actual = datetime.now().strftime('%H:%M:%S')
            fecha_manual = f"{fecha_cal} {hora_actual}"
            
            # Obtener producto para usar su precio
            producto = self.controller.obtener_producto_por_id(self.compra_producto_id)
            if not producto:
                messagebox.showerror("Error", "Producto no encontrado")
                return
            
            precio = producto['precio_compra']
            
            # Datos de vencimiento
            es_perecedero = self.compra_es_perecedero.get()
            fecha_vencimiento = None
            
            if es_perecedero:
                fecha_vencimiento = self.compra_vencimiento_cal.entry.get()
                if not fecha_vencimiento:
                    messagebox.showwarning("Advertencia", "La fecha de vencimiento es obligatoria para productos perecederos")
                    return
            
            exito, mensaje = self.controller.registrar_compra(
                self.compra_producto_id, cantidad, precio, self.compra_proveedor_id,
                no_documento, fecha_manual, es_perecedero, fecha_vencimiento
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.refresh()
                self.main_window.refresh_productos()
                self.main_window.refresh_caja()
                self.main_window.actualizar_resumen()
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def editar_compra_perecedero(self):
        """Edita el estado de perecedero de una compra"""
        # Verificar selección
        seleccion = self.compras_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una compra para editar")
            return
        
        # Obtener datos
        item = self.compras_tree.item(seleccion[0])
        valores = item['values']
        compra_id = valores[0]
        producto_nombre = valores[3]
        vencimiento_actual = valores[8]
        
        es_perecedero_actual = vencimiento_actual != "No perecedero"
        
        # Crear diálogo
        dialog = tk.Toplevel(self.main_window.root)
        dialog.title("Editar Estado de Perecedero")
        dialog.geometry("500x300")
        dialog.transient(self.main_window.root)
        dialog.withdraw()
        dialog.grab_set()
        agregar_icono(dialog)
        
        main_frame = tb.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        tb.Label(
            main_frame,
            text=f"✏️ Editar: {producto_nombre}",
            font=('Segoe UI', 12, 'bold'),
            bootstyle="primary"
        ).pack(pady=(0, 20))
        
        es_perecedero_var = tk.BooleanVar(value=es_perecedero_actual)
        
        def toggle_venc():
            if es_perecedero_var.get():
                venc_cal.entry.configure(state='normal')
                venc_cal.button.configure(state='normal')
            else:
                venc_cal.entry.configure(state='disabled')
                venc_cal.button.configure(state='disabled')
        
        tb.Checkbutton(
            main_frame,
            text="¿Es producto perecedero?",
            variable=es_perecedero_var,
            bootstyle="success-round-toggle",
            command=toggle_venc
        ).pack(anchor='w', pady=10)
        
        fecha_frame = tb.Frame(main_frame)
        fecha_frame.pack(fill='x', pady=10)
        
        tb.Label(fecha_frame, text="Fecha de Vencimiento:", font=('Segoe UI', 10, 'bold')).pack(side='left', padx=(0, 10))
        
        venc_cal = DateEntry(
            fecha_frame,
            dateformat='%d/%m/%Y',
            width=18,
            bootstyle="warning",
            firstweekday=0
        )
        venc_cal.pack(side='left')
        
        if es_perecedero_actual and vencimiento_actual != "No perecedero":
            try:
                fecha_venc = vencimiento_actual.split()[0]
                venc_cal.entry.delete(0, 'end')
                venc_cal.entry.insert(0, fecha_venc)
            except:
                pass
        
        toggle_venc()
        
        def guardar():
            es_p = es_perecedero_var.get()
            fecha_v = venc_cal.entry.get() if es_p else None
            
            if es_p and not fecha_v:
                messagebox.showwarning("Advertencia", "Debe ingresar una fecha de vencimiento")
                return
            
            exito, mensaje = self.controller.actualizar_compra_perecedero(compra_id, es_p, fecha_v)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                dialog.destroy()
                self.refresh()
            else:
                messagebox.showerror("Error", mensaje)
        
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(side='bottom', fill='x', pady=(20, 0))
        
        tb.Button(btn_frame, text="💾 Guardar", command=guardar, bootstyle="success", width=15).pack(side='left', padx=5)
        tb.Button(btn_frame, text="❌ Cancelar", command=dialog.destroy, bootstyle="secondary", width=15).pack(side='left', padx=5)
        
        centrar_ventana(dialog)
        dialog.deiconify()
    
    def refresh(self):
        """Actualiza la lista de compras"""
        # Limpiar treeview
        for item in self.compras_tree.get_children():
            self.compras_tree.delete(item)
        
        # Obtener búsqueda
        texto_busqueda = self.compra_search.get().strip().lower()
        
        # Cargar compras
        compras = self.controller.obtener_compras()
        for i, compra in enumerate(compras):
            # Aplicar filtro
            if texto_busqueda:
                proveedor = compra.get('proveedor_nombre', '').lower()
                producto = compra['producto_nombre'].lower()
                no_doc = compra.get('no_documento', '').lower()
                fecha = compra['fecha'].lower()
                
                if (texto_busqueda not in proveedor and
                    texto_busqueda not in producto and
                    texto_busqueda not in no_doc and
                    texto_busqueda not in fecha):
                    continue
            
            # Formatear fecha
            fecha_str = compra['fecha']
            try:
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
            except:
                try:
                    fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y %H:%M:%S')
                    fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
                except:
                    fecha_formateada = fecha_str.split()[0] if ' ' in fecha_str else fecha_str
            
            # Determinar color según vencimiento
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            vencimiento_texto = "No perecedero"
            
            if compra.get('es_perecedero', 0) == 1 and compra.get('fecha_vencimiento'):
                fecha_venc = compra['fecha_vencimiento']
                vencimiento_texto = fecha_venc
                
                try:
                    fecha_venc_obj = datetime.strptime(fecha_venc, '%d/%m/%Y')
                    hoy = datetime.now()
                    dias_restantes = (fecha_venc_obj - hoy).days
                    
                    if dias_restantes < 0:
                        tag = 'vencido'
                        vencimiento_texto = f"{fecha_venc} ⚠️ VENCIDO"
                    elif dias_restantes <= 7:
                        tag = 'critico'
                        vencimiento_texto = f"{fecha_venc} ({dias_restantes}d)"
                    elif dias_restantes <= 30:
                        tag = 'advertencia'
                        vencimiento_texto = f"{fecha_venc} ({dias_restantes}d)"
                except:
                    pass
            
            self.compras_tree.insert('', 'end', values=(
                compra['id'],
                compra.get('proveedor_nombre', '[Sin Proveedor]'),
                compra.get('no_documento', ''),
                compra['producto_nombre'],
                f"{compra['cantidad']:,}",
                f"Q {compra['precio_unitario']:,.2f}",
                f"Q {compra['total']:,.2f}",
                fecha_formateada,
                vencimiento_texto
            ), tags=(tag,))
    
    def limpiar_formulario(self):
        """Limpia el formulario de compras"""
        self.compra_cantidad.set(0)
        self.compra_precio.set(0)
        
        # Solo limpiar No. Documento si NO está marcado "Mismo documento"
        if not self.mismo_documento.get():
            self.compra_no_documento.set("")
        
        self.compra_producto_busqueda.set("")
        self.compra_proveedor_busqueda.set("")
        self.compra_producto_label.config(text="")
        self.compra_proveedor_label.config(text="")
        self.compra_es_perecedero.set(False)
        self.compra_fecha_vencimiento.set("")
        self.compra_vencimiento_cal.entry.configure(state='disabled')
        self.compra_vencimiento_cal.button.configure(state='disabled')
        self.compra_producto_id = None
        self.compra_proveedor_id = None
        self.compra_producto_entry.focus()  # Cambio: enfocar producto, no proveedor
    
    # ========== MÉTODOS DE BÚSQUEDA Y AUTOCOMPLETADO ==========
    
    def autocompletar_proveedor(self, event):
        """Autocompletado para proveedor en compras"""
        texto = self.compra_proveedor_busqueda.get()
        
        if hasattr(self, 'proveedor_listbox') and self.proveedor_listbox.winfo_exists():
            self.proveedor_listbox.destroy()
        
        if len(texto) < 2:
            return
        
        proveedores = self.controller.buscar_proveedor(texto)
        
        if not proveedores:
            return
        
        x = self.compra_proveedor_entry.winfo_rootx()
        y = self.compra_proveedor_entry.winfo_rooty() + self.compra_proveedor_entry.winfo_height()
        width = self.compra_proveedor_entry.winfo_width()
        
        self.proveedor_listbox = tk.Listbox(
            self.main_window.root,
            height=min(5, len(proveedores)),
            width=width // 8,
            font=('Segoe UI', 10)
        )
        self.proveedor_listbox.place(x=x - self.main_window.root.winfo_rootx(), 
                                     y=y - self.main_window.root.winfo_rooty())
        
        for prov in proveedores[:10]:
            self.proveedor_listbox.insert('end', f"{prov['nombre']} - {prov['nit_dpi']}")
        
        def seleccionar_proveedor(event=None):
            if self.proveedor_listbox.curselection():
                idx = self.proveedor_listbox.curselection()[0]
                seleccion = self.proveedor_listbox.get(idx)
                self.compra_proveedor_busqueda.set(seleccion)
                self.compra_proveedor_id = proveedores[idx]['id']
                self.compra_proveedor_label.config(text="✓", bootstyle="success")
                self.proveedor_listbox.destroy()
        
        self.proveedor_listbox.bind('<<ListboxSelect>>', seleccionar_proveedor)
        self.proveedor_listbox.bind('<Return>', seleccionar_proveedor)
        self.proveedor_listbox.bind('<Escape>', lambda e: self.proveedor_listbox.destroy())
        
        if event.keysym == 'Down':
            self.proveedor_listbox.focus_set()
            self.proveedor_listbox.selection_set(0)
    
    def autocompletar_producto(self, event):
        """Autocompletado para producto en compras"""
        texto = self.compra_producto_busqueda.get()
        
        if hasattr(self, 'producto_compra_listbox') and self.producto_compra_listbox.winfo_exists():
            self.producto_compra_listbox.destroy()
        
        if len(texto) < 2:
            return
        
        productos = self.controller.obtener_productos()
        productos_filtrados = [
            p for p in productos 
            if texto.lower() in p['nombre'].lower() or 
               (p.get('codigo') and texto.lower() in p['codigo'].lower())
        ]
        
        if not productos_filtrados:
            return
        
        x = self.compra_producto_entry.winfo_rootx()
        y = self.compra_producto_entry.winfo_rooty() + self.compra_producto_entry.winfo_height()
        width = self.compra_producto_entry.winfo_width()
        
        self.producto_compra_listbox = tk.Listbox(
            self.main_window.root,
            height=min(5, len(productos_filtrados)),
            width=width // 8,
            font=('Segoe UI', 10)
        )
        self.producto_compra_listbox.place(x=x - self.main_window.root.winfo_rootx(), 
                                           y=y - self.main_window.root.winfo_rooty())
        
        for prod in productos_filtrados[:10]:
            codigo_txt = f"[{prod.get('codigo', 'S/C')}] " if prod.get('codigo') else ""
            self.producto_compra_listbox.insert('end', f"{codigo_txt}{prod['nombre']} - Q{prod['precio_compra']:.2f}")
        
        def seleccionar_producto(event=None):
            if self.producto_compra_listbox.curselection():
                idx = self.producto_compra_listbox.curselection()[0]
                prod = productos_filtrados[idx]
                codigo_txt = f"[{prod.get('codigo', 'S/C')}] " if prod.get('codigo') else ""
                self.compra_producto_busqueda.set(f"{codigo_txt}{prod['nombre']}")
                self.compra_producto_id = prod['id']
                self.compra_precio.set(prod['precio_compra'])
                self.compra_producto_label.config(text="✓", bootstyle="success")
                self.producto_compra_listbox.destroy()
        
        self.producto_compra_listbox.bind('<<ListboxSelect>>', seleccionar_producto)
        self.producto_compra_listbox.bind('<Return>', seleccionar_producto)
        self.producto_compra_listbox.bind('<Escape>', lambda e: self.producto_compra_listbox.destroy())
        
        if event.keysym == 'Down':
            self.producto_compra_listbox.focus_set()
            self.producto_compra_listbox.selection_set(0)
    
    def buscar_proveedor(self):
        """Abre diálogo para buscar proveedor"""
        from ..utils import centrar_ventana, agregar_icono
        
        busqueda = self.main_window.pedir_texto("Buscar Proveedor", "Ingrese nombre o NIT del proveedor:")
        if not busqueda:
            return
            
        proveedores = self.controller.buscar_proveedor(busqueda)
        
        if not proveedores:
            messagebox.showinfo("Sin resultados", "No se encontraron proveedores con ese criterio")
            return
        
        dialog = tk.Toplevel(self.main_window.root)
        dialog.title("Seleccionar Proveedor")
        dialog.geometry("850x550")
        dialog.transient(self.main_window.root)
        dialog.withdraw()
        dialog.grab_set()
        agregar_icono(dialog)
        
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
                self.compra_proveedor_label.config(text="✓", bootstyle="success")
                dialog.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un proveedor")
        
        button_frame = tb.Frame(frame)
        button_frame.pack(pady=10)
        tb.Button(button_frame, text="✓ Seleccionar", command=seleccionar, bootstyle="success", width=15).pack()
        
        tree.bind('<Double-1>', lambda e: seleccionar())
        centrar_ventana(dialog)
        dialog.deiconify()
    
    def buscar_producto(self):
        """Abre diálogo para buscar producto"""
        from ..utils import centrar_ventana, agregar_icono
        
        busqueda = self.main_window.pedir_texto("Buscar Producto", "Ingrese código o nombre del producto:")
        if not busqueda:
            return
            
        productos = self.controller.obtener_productos_activos()
        productos_filtrados = [p for p in productos if 
                              busqueda.lower() in p['nombre'].lower() or 
                              busqueda.lower() in str(p.get('codigo', '')).lower()]
        
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
            columns=('ID', 'Código', 'Nombre', 'Precio Compra', 'Stock'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=13
        )
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Código', text='Código')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Precio Compra', text='Precio Compra')
        tree.heading('Stock', text='Stock Actual')
        
        tree.column('ID', width=50, anchor='center')
        tree.column('Código', width=150, anchor='w')
        tree.column('Nombre', width=300, anchor='w')
        tree.column('Precio Compra', width=120, anchor='e')
        tree.column('Stock', width=100, anchor='center')
        
        for prod in productos_filtrados:
            tree.insert('', 'end', values=(
                prod['id'],
                prod.get('codigo', 'S/C'),
                prod['nombre'],
                f"Q {prod['precio_compra']:,.2f}",
                f"{prod['stock_actual']:,}"
            ))
        
        tree.pack(fill='both', expand=True)
        
        def seleccionar():
            seleccion = tree.selection()
            if seleccion:
                item = tree.item(seleccion[0])
                values = item['values']
                prod = [p for p in productos_filtrados if p['id'] == values[0]][0]
                self.compra_producto_id = prod['id']
                codigo_txt = f"[{prod.get('codigo', 'S/C')}] " if prod.get('codigo') else ""
                self.compra_producto_busqueda.set(f"{codigo_txt}{prod['nombre']}")
                self.compra_precio.set(prod['precio_compra'])
                self.compra_producto_label.config(text="✓", bootstyle="success")
                dialog.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un producto")
        
        button_frame = tb.Frame(frame)
        button_frame.pack(pady=10)
        tb.Button(button_frame, text="✓ Seleccionar", command=seleccionar, bootstyle="success", width=15).pack()
        
        tree.bind('<Double-1>', lambda e: seleccionar())
        centrar_ventana(dialog)
        dialog.deiconify()
    
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
