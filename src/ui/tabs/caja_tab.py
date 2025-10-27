"""
Módulo de gestión de caja
Permite registrar movimientos de ingresos y egresos, y mantener control del flujo de efectivo
"""
import ttkbootstrap as tb
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
from ttkbootstrap import DateEntry
from src.ui.utils.ui_helpers import centrar_ventana, agregar_icono, configurar_navegacion_calendario


class CajaTab:
    """Pestaña de gestión de caja"""
    
    def __init__(self, parent_frame, controller, main_window):
        self.parent_frame = parent_frame
        self.controller = controller
        self.main_window = main_window
        
        # Variables de formulario
        self.setup_variables()
        
        # Crear interfaz
        self.create_ui()
    
    def setup_variables(self):
        """Inicializa las variables del formulario"""
        self.caja_tipo = tb.StringVar(value='EGRESO')
        self.caja_categoria = tb.StringVar(value='GASTO_OPERATIVO')
        self.caja_concepto = tb.StringVar()
        self.caja_monto = tb.DoubleVar(value=0.0)
    
    def create_ui(self):
        """Crea la interfaz de usuario de caja"""
        # Panel superior: Saldo actual
        self.crear_panel_saldo()
        
        # Formulario de movimientos
        self.crear_formulario()
        
        # Lista de movimientos
        self.crear_tabla()
    
    def crear_panel_saldo(self):
        """Crea el panel de saldo actual"""
        saldo_frame = tb.Labelframe(
            self.parent_frame,
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
    
    def crear_formulario(self):
        """Crea el formulario de registro de movimientos"""
        form_frame = tb.Labelframe(
            self.parent_frame,
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
        tipo_combo.bind('<<ComboboxSelected>>', self.actualizar_categorias)
        
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
        
        # Fila 3: Monto, Fecha y Botones
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
            command=self.registrar_movimiento,
            bootstyle="success",
            width=15
        ).pack(side='left', padx=5)
        
        tb.Button(
            row3,
            text="🧹 Limpiar",
            command=self.limpiar_formulario,
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
        
        # Configurar navegación de calendario
        self.main_window.root.after(100, lambda: configurar_navegacion_calendario(self.caja_fecha_entry))
    
    def crear_tabla(self):
        """Crea la tabla de historial de movimientos"""
        list_frame = tb.Labelframe(
            self.parent_frame,
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
        self.caja_busqueda.bind('<KeyRelease>', lambda e: self.refresh())
        
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
            command=self.filtrar_movimientos,
            bootstyle="info",
            width=12
        ).pack(side='left', padx=5)
        
        tb.Button(
            toolbar_frame,
            text="🔄 Todos",
            command=self.refresh,
            bootstyle="secondary",
            width=12
        ).pack(side='left', padx=5)
        
        # Treeview para movimientos
        tree_frame = tb.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Fecha', 'Tipo', 'Categoría', 'Venta #', 'Concepto', 'Monto', 'Saldo Anterior', 'Saldo Nuevo')
        self.caja_tree = tb.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=12
        )
        
        # Configurar columnas
        column_widths = {
            'ID': 50, 'Fecha': 100, 'Tipo': 80, 'Categoría': 100,
            'Venta #': 100, 'Concepto': 220, 'Monto': 120, 'Saldo Anterior': 120, 'Saldo Nuevo': 120
        }
        
        for col in columns:
            # Configurar encabezado con ordenamiento
            self.caja_tree.heading(col, text=col, 
                                  command=lambda c=col: self.sort_tree(c, False))
            
            # Configurar alineación: derecha para montos, izquierda para concepto, centro para el resto
            if col in ['Monto', 'Saldo Anterior', 'Saldo Nuevo']:
                anchor = 'e'  # Derecha (east)
            elif col == 'Concepto':
                anchor = 'w'  # Izquierda (west)
            else:
                anchor = 'center'
            
            # Ocultar columna "Venta #" (ancho 0)
            if col == 'Venta #':
                self.caja_tree.column(col, width=0, stretch=False)
            else:
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
        
        # Tags hover (versiones más claras para efecto hover)
        self.caja_tree.tag_configure('ingreso_hover', background='#e0f4e4', foreground='#155724')
        self.caja_tree.tag_configure('egreso_hover', background='#fce4e6', foreground='#721c24')
        
        # Variables para controlar hover
        self.last_hovered_item = None
        self.original_tag = None
        
        # Botones de acción debajo del tree
        actions_frame = tb.Frame(list_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        tb.Button(
            actions_frame,
            text="🗑️ Eliminar Movimiento Seleccionado",
            command=self.eliminar_movimiento,
            bootstyle="danger-outline",
            width=30
        ).pack(side='left', padx=5)
        
        tb.Label(
            actions_frame,
            text="💡 Doble clic en un movimiento para ver detalles",
            font=('Segoe UI', 9, 'italic'),
            bootstyle="secondary"
        ).pack(side='left', padx=20)
        
        # Bindings
        self.caja_tree.bind('<Double-1>', self.ver_detalle_movimiento)
        self.caja_tree.bind('<Motion>', self.on_tree_motion)
        self.caja_tree.bind('<Leave>', self.on_tree_leave)
        
        # Configurar navegación mejorada en calendarios
        self.main_window.root.after(100, lambda: configurar_navegacion_calendario(self.caja_fecha_inicio))
        self.main_window.root.after(100, lambda: configurar_navegacion_calendario(self.caja_fecha_fin))
        
        # Cargar datos iniciales
        self.refresh()
    
    # ========== MÉTODOS DE OPERACIONES ==========
    
    def actualizar_categorias(self, event=None):
        """Actualiza las categorías según el tipo seleccionado"""
        tipo = self.caja_tipo.get()
        if tipo == 'INGRESO':
            self.categoria_combo['values'] = ['APORTE_CAPITAL', 'OTRO']
            self.caja_categoria.set('APORTE_CAPITAL')
        else:  # EGRESO
            self.categoria_combo['values'] = ['GASTO_OPERATIVO', 'RETIRO_UTILIDAD', 'OTRO']
            self.caja_categoria.set('GASTO_OPERATIVO')
    
    def registrar_movimiento(self):
        """Registra un movimiento de caja"""
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
                self.limpiar_formulario()
                self.refresh()
            else:
                messagebox.showerror("Error", mensaje)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar movimiento: {str(e)}")
    
    def retiro_utilidades_rapido(self):
        """Acceso rápido para retiro de utilidades"""
        self.caja_tipo.set('EGRESO')
        self.actualizar_categorias()
        self.caja_categoria.set('RETIRO_UTILIDAD')
        self.caja_concepto.set('Retiro de utilidades')
        self.caja_monto.set(0.0)
    
    def aporte_capital_rapido(self):
        """Acceso rápido para aporte de capital"""
        self.caja_tipo.set('INGRESO')
        self.actualizar_categorias()
        self.caja_categoria.set('APORTE_CAPITAL')
        self.caja_concepto.set('Aporte de capital')
        self.caja_monto.set(0.0)
    
    def limpiar_formulario(self):
        """Limpia el formulario de caja"""
        self.caja_tipo.set('EGRESO')
        self.actualizar_categorias()
        self.caja_concepto.set('')
        self.caja_monto.set(0.0)
    
    def filtrar_movimientos(self):
        """Filtra movimientos por rango de fechas"""
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
            self.cargar_movimientos(movimientos)
            
            # Actualizar labels de resumen
            self.ingresos_label.config(text=f"↑ Ingresos: Q {resumen['total_ingresos']:,.2f}")
            self.egresos_label.config(text=f"↓ Egresos: Q {resumen['total_egresos']:,.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar: {str(e)}")
    
    def eliminar_movimiento(self):
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
                    self.refresh()
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
        detalle_window = tk.Toplevel(self.main_window.root)
        detalle_window.title("Detalles del Movimiento")
        detalle_window.geometry("650x500")
        detalle_window.transient(self.main_window.root)
        detalle_window.resizable(False, False)
        
        # Ocultar ventana temporalmente para evitar parpadeo
        detalle_window.withdraw()
        
        detalle_window.grab_set()
        agregar_icono(detalle_window)
        
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
        centrar_ventana(detalle_window)
        detalle_window.deiconify()
    
    def refresh(self):
        """Actualiza los datos de caja con filtro de búsqueda"""
        # Obtener saldo actual
        saldo = self.controller.obtener_saldo_caja()
        self.saldo_label.config(text=f"Q {saldo:,.2f}")
        
        # Cambiar color del saldo según si es positivo o negativo
        if saldo < 0:
            self.saldo_label.config(bootstyle="danger")  # Rojo para saldo negativo
        else:
            self.saldo_label.config(bootstyle="success")  # Verde para saldo positivo
        
        # Obtener movimientos
        movimientos = self.controller.obtener_movimientos_caja()
        
        # Aplicar filtro de búsqueda si existe
        if hasattr(self, 'caja_busqueda'):
            busqueda = self.caja_busqueda.get().lower()
            if busqueda:
                movimientos = [m for m in movimientos if 
                              busqueda in m['concepto'].lower() or 
                              busqueda in m['categoria'].lower() or
                              busqueda in m['tipo'].lower()]
        
        self.cargar_movimientos(movimientos)
        
        # Obtener resumen
        resumen = self.controller.obtener_resumen_caja()
        self.ingresos_label.config(text=f"↑ Ingresos: Q {resumen['total_ingresos']:,.2f}")
        self.egresos_label.config(text=f"↓ Egresos: Q {resumen['total_egresos']:,.2f}")
    
    def cargar_movimientos(self, movimientos):
        """Carga los movimientos en la tabla"""
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
            
            # Extraer número de venta del concepto si existe
            venta_num = ''
            concepto_limpio = mov['concepto']
            
            if 'Venta #' in mov['concepto']:
                try:
                    # Extraer "Venta #123 (REF000456)" del concepto
                    venta_parte = mov['concepto'].split('Venta #')[1]
                    if ' (' in venta_parte:
                        venta_num = venta_parte.split(' (')[0].strip()
                    elif ' -' in venta_parte:
                        venta_num = venta_parte.split(' -')[0].strip()
                    else:
                        venta_num = venta_parte.strip()
                except:
                    pass
            
            self.caja_tree.insert('', 'end', values=(
                mov['id'],
                fecha_formateada,
                mov['tipo'],
                mov['categoria'],
                venta_num if venta_num else '-',
                concepto_limpio,
                f"Q {mov['monto']:,.2f}",
                f"Q {mov['saldo_anterior']:,.2f}",
                f"Q {mov['saldo_nuevo']:,.2f}"
            ), tags=(tag,))
    
    def sort_tree(self, col, reverse):
        """Ordena la tabla de caja por columna"""
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
        self.caja_tree.heading(col, command=lambda: self.sort_tree(col, not reverse))
    
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

