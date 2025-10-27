"""
Módulo de reportes y estadísticas
Muestra resúmenes financieros, alertas de stock y vencimientos, y permite exportar reportes
"""
import ttkbootstrap as tb
from tkinter import messagebox, filedialog
import tkinter as tk
from datetime import datetime, timedelta
from ttkbootstrap import DateEntry
from src.ui.utils.ui_helpers import sort_treeview, centrar_ventana, agregar_icono


class ReportesTab:
    """Pestaña de reportes y estadísticas"""
    
    def __init__(self, parent_frame, controller, main_window):
        self.parent_frame = parent_frame
        self.controller = controller
        self.main_window = main_window
        
        # Crear interfaz
        self.create_ui()
    
    def create_ui(self):
        """Crea la interfaz de usuario de reportes"""
        # Contenedor principal
        main_container = tb.Frame(self.parent_frame)
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Panel de métricas
        self.crear_tarjetas_metricas(main_container)
        
        # Botones de exportación
        self.crear_panel_exportacion(main_container)
        
        # Panel de alertas
        self.crear_panel_alertas(main_container)
    
    def crear_tarjetas_metricas(self, container):
        """Crea las tarjetas de métricas financieras"""
        cards_frame = tb.Frame(container)
        cards_frame.pack(fill='x', pady=(0, 15))
        
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
    
    def crear_panel_exportacion(self, container):
        """Crea el panel de botones de exportación"""
        export_frame = tb.Labelframe(
            container, 
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
    
    def crear_panel_alertas(self, container):
        """Crea el panel de alertas de stock y vencimientos"""
        stock_frame = tb.Labelframe(
            container, 
            text="⚠️ Alertas del Sistema", 
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
            self.stock_tree.heading(col, text=col, anchor='center', 
                                   command=lambda c=col: sort_treeview(self.stock_tree, c, False))
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
        
        # Tags hover (versiones más claras para efecto hover)
        self.stock_tree.tag_configure('alert_stock_hover', background='#ffdddd', foreground='#cc0000')
        self.stock_tree.tag_configure('alert_vencido_hover', background='#ff8585', foreground='white')
        self.stock_tree.tag_configure('alert_critico_hover', background='#ffb733', foreground='black')
        self.stock_tree.tag_configure('alert_advertencia_hover', background='#ffe066', foreground='black')
        
        # Variables para controlar hover
        self.last_hovered_item = None
        self.original_tag = None
        
        # Agregar bindings
        self.stock_tree.bind('<Button-3>', lambda e: self.main_window.mostrar_menu_alertas(e))
        self.stock_tree.bind('<Motion>', self.on_tree_motion)
        self.stock_tree.bind('<Leave>', self.on_tree_leave)
        
        # Cargar alertas iniciales
        self.refresh()
    
    def refresh(self):
        """Actualiza los datos de reportes y alertas"""
        # Actualizar métricas
        self.actualizar_metricas()
        
        # Actualizar alertas
        self.actualizar_alertas()
    
    def actualizar_metricas(self):
        """Actualiza las tarjetas de métricas"""
        # Obtener resumen completo del inventario
        resumen = self.controller.obtener_resumen_inventario()
        
        # Actualizar labels con datos del resumen
        self.total_compras_label.config(text=f"Q {resumen['total_compras']:,.2f}")
        self.total_ventas_label.config(text=f"Q {resumen['total_ventas']:,.2f}")
        self.ganancia_label.config(text=f"Q {resumen['ganancia_bruta']:,.2f}")
        self.valor_inventario_label.config(text=f"Q {resumen['valor_inventario']:,.2f}")
        self.saldo_banco_label.config(text=f"Q {resumen['saldo_banco']:,.2f}")
        
        # Actualizar también las alertas
        self.actualizar_alertas()
    
    def actualizar_alertas(self):
        """Actualiza la tabla de alertas"""
        # Limpiar tabla
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        # Obtener productos con stock bajo
        productos_bajo_stock = self.controller.obtener_productos_con_stock_bajo()
        
        for producto in productos_bajo_stock:
            self.stock_tree.insert('', 'end', values=(
                '⚠️ STOCK BAJO',
                producto.get('codigo', ''),
                producto['nombre'],
                f"Stock: {producto['stock_actual']} unidades",
                f"Mínimo: {producto.get('stock_minimo', 5)}",
                'Realizar compra urgente'
            ), tags=('alert_stock',))
        
        # Obtener productos próximos a vencer
        from datetime import datetime, timedelta
        
        compras = self.controller.obtener_compras()
        hoy = datetime.now()
        
        for compra in compras:
            if compra.get('es_perecedero', 0) == 1 and compra.get('fecha_vencimiento'):
                try:
                    fecha_venc = datetime.strptime(compra['fecha_vencimiento'], '%d/%m/%Y')
                    dias_restantes = (fecha_venc - hoy).days
                    
                    if dias_restantes < 0:
                        tag = 'alert_vencido'
                        estado = f"VENCIDO hace {abs(dias_restantes)} días"
                        accion = "Revisar y gestionar producto"
                    elif dias_restantes <= 7:
                        tag = 'alert_critico'
                        estado = f"Vence en {dias_restantes} días"
                        accion = "Vender con urgencia o promocionar"
                    elif dias_restantes <= 30:
                        tag = 'alert_advertencia'
                        estado = f"Vence en {dias_restantes} días"
                        accion = "Monitorear y planificar ventas"
                    else:
                        continue  # No mostrar si es > 30 días
                    
                    producto = self.controller.obtener_producto_por_id(compra['producto_id'])
                    if producto:
                        self.stock_tree.insert('', 'end', values=(
                            '📅 VENCIMIENTO',
                            producto.get('codigo', 'N/A'),
                            producto['nombre'],
                            estado,
                            compra['fecha_vencimiento'],
                            accion
                        ), tags=(tag,))
                except:
                    pass
    
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
    
    # ========== MÉTODOS DE EXPORTACIÓN ==========
    
    def seleccionar_rango_fechas(self, titulo="Seleccionar Rango de Fechas"):
        """Muestra un diálogo para seleccionar rango de fechas"""
        dialog = tk.Toplevel(self.main_window.root)
        dialog.title(titulo)
        dialog.geometry("500x280")
        dialog.transient(self.main_window.root)
        dialog.withdraw()
        dialog.grab_set()
        agregar_icono(dialog)
        
        # Centrar diálogo
        centrar_ventana(dialog)
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
        
        # Calcular primer día del mes actual
        hoy = datetime.now()
        primer_dia_mes = datetime(hoy.year, hoy.month, 1)
        
        # Fecha inicio (primer día del mes actual)
        tb.Label(dates_frame, text="Fecha Inicio:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=10)
        fecha_inicio_cal = DateEntry(
            dates_frame,
            dateformat='%d/%m/%Y',
            firstweekday=0,
            width=18
        )
        fecha_inicio_cal.set_date(primer_dia_mes)
        fecha_inicio_cal.grid(row=0, column=1, padx=10, pady=10)
        
        # Fecha fin (hoy)
        tb.Label(dates_frame, text="Fecha Fin:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=5, pady=10)
        fecha_fin_cal = DateEntry(
            dates_frame,
            dateformat='%d/%m/%Y',
            firstweekday=0,
            width=18
        )
        fecha_fin_cal.set_date(hoy)
        fecha_fin_cal.grid(row=1, column=1, padx=10, pady=10)
        
        # Botones
        btn_frame = tb.Frame(frame)
        btn_frame.pack(pady=20)
        
        def aceptar():
            try:
                # Obtener las fechas correctamente del DateEntry
                fecha_inicio_obj = fecha_inicio_cal.entry.get()
                fecha_fin_obj = fecha_fin_cal.entry.get()
                
                # Validar que las fechas estén en formato correcto
                datetime.strptime(fecha_inicio_obj, '%d/%m/%Y')
                datetime.strptime(fecha_fin_obj, '%d/%m/%Y')
                
                resultado['aceptado'] = True
                resultado['fecha_inicio'] = fecha_inicio_obj
                resultado['fecha_fin'] = fecha_fin_obj
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Las fechas deben estar en formato DD/MM/AAAA")
        
        def cancelar():
            dialog.destroy()
        
        tb.Button(btn_frame, text="✓ Aceptar", command=aceptar, bootstyle="success", width=12).pack(side='left', padx=5)
        tb.Button(btn_frame, text="✗ Cancelar", command=cancelar, bootstyle="danger-outline", width=12).pack(side='left', padx=5)
        
        self.main_window.root.wait_window(dialog)
        return resultado
    
    def exportar_reporte_general(self):
        """Exporta el reporte general completo a Excel con estado de vencimientos"""
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
                from datetime import datetime as dt
                
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
                    for p in productos_bajo:
                        p['estado'] = 'ACTIVO' if p.get('activo', 1) == 1 else 'INACTIVO'
                df_stock_bajo = pd.DataFrame(productos_bajo) if productos_bajo else pd.DataFrame()
                
                # Estado de vencimientos
                compras = self.controller.obtener_compras()
                vencimientos = []
                for compra in compras:
                    if compra.get('es_perecedero') == 1 and compra.get('fecha_vencimiento'):
                        try:
                            fecha_venc = dt.strptime(compra['fecha_vencimiento'], '%d/%m/%Y')
                            hoy = dt.now()
                            dias_restantes = (fecha_venc - hoy).days
                            
                            estado_vencimiento = ''
                            if dias_restantes < 0:
                                estado_vencimiento = f'VENCIDO (hace {abs(dias_restantes)} días)'
                            elif dias_restantes <= 7:
                                estado_vencimiento = f'CRITICO ({dias_restantes} días)'
                            elif dias_restantes <= 30:
                                estado_vencimiento = f'ADVERTENCIA ({dias_restantes} días)'
                            else:
                                estado_vencimiento = f'OK ({dias_restantes} días)'
                            
                            vencimientos.append({
                                'Producto': compra.get('producto_nombre', 'N/A'),
                                'Proveedor': compra.get('proveedor_nombre', 'N/A'),
                                'Cantidad': compra['cantidad'],
                                'Fecha Vencimiento': compra['fecha_vencimiento'],
                                'Días Restantes': dias_restantes,
                                'Estado': estado_vencimiento
                            })
                        except:
                            pass
                
                # Ordenar por días restantes (vencidos y críticos primero)
                vencimientos.sort(key=lambda x: x['Días Restantes'])
                df_vencimientos = pd.DataFrame(vencimientos) if vencimientos else pd.DataFrame()
                
                # Exportar a Excel con múltiples hojas
                with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                    df_resumen.to_excel(writer, sheet_name='Resumen General', index=False)
                    if not df_vencimientos.empty:
                        df_vencimientos.to_excel(writer, sheet_name='Estado Vencimientos', index=False)
                    if not df_stock_bajo.empty:
                        df_stock_bajo.to_excel(writer, sheet_name='Stock Bajo', index=False)
                
                messagebox.showinfo("Éxito", f"Reporte general exportado a:\n{archivo}\n\n{len(vencimientos)} productos con control de vencimiento")
            except ImportError:
                messagebox.showerror("Error", "Se requiere instalar 'pandas' y 'openpyxl' para exportar a Excel.\nEjecute: pip install pandas openpyxl")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el reporte: {str(e)}")
    
    def exportar_productos_completo(self):
        """Exporta todos los productos con todos sus detalles a Excel"""
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
                
                productos = self.controller.obtener_productos()
                
                if not productos:
                    messagebox.showwarning("Aviso", "No hay productos registrados para exportar.")
                    return
                
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
                
                df = pd.DataFrame(datos_exportar)
                
                with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Productos', index=False)
                    worksheet = writer.sheets['Productos']
                    for idx, col in enumerate(df.columns, 1):
                        max_length = max(df[col].astype(str).apply(len).max(), len(col))
                        worksheet.column_dimensions[chr(64 + idx)].width = min(max_length + 2, 50)
                
                messagebox.showinfo("Éxito", f"Productos exportados exitosamente a:\n{archivo}\n\nTotal de productos: {len(productos)}")
            except ImportError:
                messagebox.showerror("Error", "Se requiere instalar 'pandas' y 'openpyxl' para exportar a Excel.\nEjecute: pip install pandas openpyxl")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar los productos: {str(e)}")
    
    def exportar_reporte_compras(self):
        """Exporta todas las compras a Excel con filtro de fechas"""
        rango = self.seleccionar_rango_fechas("Filtrar Compras por Fecha")
        
        if not rango['aceptado']:
            return
        
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
                
                fecha_inicio = dt.strptime(rango['fecha_inicio'], '%d/%m/%Y')
                fecha_fin = dt.strptime(rango['fecha_fin'], '%d/%m/%Y')
                # Ajustar fecha_fin para incluir todo el día
                fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)
                
                compras_filtradas = []
                for compra in compras:
                    try:
                        fecha_str = compra['fecha']
                        fecha_compra = None
                        
                        # Intentar múltiples formatos de fecha
                        formatos = [
                            '%d/%m/%Y %H:%M:%S',
                            '%Y-%m-%d %H:%M:%S',
                            '%d/%m/%Y',
                            '%Y-%m-%d'
                        ]
                        
                        for formato in formatos:
                            try:
                                fecha_compra = dt.strptime(fecha_str, formato)
                                break
                            except ValueError:
                                continue
                        
                        # Si aún no se pudo parsear, intentar solo la parte de la fecha
                        if fecha_compra is None and ' ' in fecha_str:
                            try:
                                fecha_compra = dt.strptime(fecha_str.split()[0], '%d/%m/%Y')
                            except:
                                try:
                                    fecha_compra = dt.strptime(fecha_str.split()[0], '%Y-%m-%d')
                                except:
                                    pass
                        
                        if fecha_compra and fecha_inicio <= fecha_compra <= fecha_fin:
                            compras_filtradas.append(compra)
                    except Exception as e:
                        # Si hay error, omitir esta compra
                        continue
                
                if not compras_filtradas:
                    messagebox.showwarning("Aviso", f"No hay compras en el rango seleccionado:\n{rango['fecha_inicio']} - {rango['fecha_fin']}")
                    return
                
                datos = []
                total_general = 0
                for compra in compras_filtradas:
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
                df.loc[len(df)] = ['', '', '', '', '', 'TOTAL:', f"Q {total_general:,.2f}", '', '']
                df.to_excel(archivo, index=False, sheet_name='Compras')
                
                messagebox.showinfo("Éxito", f"Reporte de compras exportado:\n{archivo}\n\n{len(compras_filtradas)} compras encontradas\nTotal: Q {total_general:,.2f}")
            except ImportError:
                messagebox.showerror("Error", "Se requiere instalar 'pandas' y 'openpyxl' para exportar a Excel.\nEjecute: pip install pandas openpyxl")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el reporte: {str(e)}")
    
    def exportar_reporte_ventas(self):
        """Exporta todas las ventas a Excel con filtro de fechas"""
        rango = self.seleccionar_rango_fechas("Filtrar Ventas por Fecha")
        
        if not rango['aceptado']:
            return
        
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
                
                fecha_inicio = dt.strptime(rango['fecha_inicio'], '%d/%m/%Y')
                fecha_fin = dt.strptime(rango['fecha_fin'], '%d/%m/%Y')
                # Ajustar fecha_fin para incluir todo el día
                fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)
                
                ventas_filtradas = []
                for venta in ventas:
                    try:
                        fecha_str = venta['fecha']
                        fecha_venta = None
                        
                        # Intentar múltiples formatos de fecha
                        formatos = [
                            '%d/%m/%Y %H:%M:%S',
                            '%Y-%m-%d %H:%M:%S',
                            '%d/%m/%Y',
                            '%Y-%m-%d'
                        ]
                        
                        for formato in formatos:
                            try:
                                fecha_venta = dt.strptime(fecha_str, formato)
                                break
                            except ValueError:
                                continue
                        
                        # Si aún no se pudo parsear, intentar solo la parte de la fecha
                        if fecha_venta is None and ' ' in fecha_str:
                            try:
                                fecha_venta = dt.strptime(fecha_str.split()[0], '%d/%m/%Y')
                            except:
                                try:
                                    fecha_venta = dt.strptime(fecha_str.split()[0], '%Y-%m-%d')
                                except:
                                    pass
                        
                        if fecha_venta and fecha_inicio <= fecha_venta <= fecha_fin:
                            ventas_filtradas.append(venta)
                    except Exception as e:
                        # Si hay error, omitir esta venta
                        continue
                
                if not ventas_filtradas:
                    messagebox.showwarning("Aviso", f"No hay ventas en el rango seleccionado:\n{rango['fecha_inicio']} - {rango['fecha_fin']}")
                    return
                
                # Exportar el detalle de cada venta (con todos los productos)
                datos = []
                total_general = 0
                for venta in ventas_filtradas:
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
                    
                    # Agregar cada producto de la venta como una fila separada
                    for detalle in venta.get('detalles', []):
                        datos.append({
                            'ID Venta': venta['id'],
                            'Referencia': venta.get('referencia_no', 'N/A'),
                            'Fecha': fecha_mostrar,
                            'Cliente': venta.get('cliente_nombre', 'N/A'),
                            'Producto': detalle.get('producto_nombre', 'N/A'),
                            'Cantidad': detalle['cantidad'],
                            'Precio Unitario': f"Q {detalle['precio_unitario']:,.2f}",
                            'Subtotal': f"Q {detalle['subtotal']:,.2f}",
                            'Estado': venta.get('estado', 'N/A')
                        })
                    
                    total_general += venta['total']
                
                df = pd.DataFrame(datos)
                
                # Agregar fila de total
                fila_total = {
                    'ID Venta': '',
                    'Referencia': '',
                    'Fecha': '',
                    'Cliente': '',
                    'Producto': '',
                    'Cantidad': '',
                    'Precio Unitario': 'TOTAL:',
                    'Subtotal': f"Q {total_general:,.2f}",
                    'Estado': ''
                }
                df = pd.concat([df, pd.DataFrame([fila_total])], ignore_index=True)
                
                df.to_excel(archivo, index=False, sheet_name='Ventas')
                
                messagebox.showinfo("Éxito", f"Reporte de ventas exportado:\n{archivo}\n\n{len(ventas_filtradas)} ventas encontradas\nTotal: Q {total_general:,.2f}")
            except ImportError:
                messagebox.showerror("Error", "Se requiere instalar 'pandas' y 'openpyxl' para exportar a Excel.\nEjecute: pip install pandas openpyxl")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el reporte: {str(e)}")
    
    def exportar_reporte_caja(self):
        """Exporta todos los movimientos de caja a Excel con filtro de fechas"""
        rango = self.seleccionar_rango_fechas("Filtrar Movimientos de Caja por Fecha")
        
        if not rango['aceptado']:
            return
        
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
                
                fecha_inicio = dt.strptime(rango['fecha_inicio'], '%d/%m/%Y')
                fecha_fin = dt.strptime(rango['fecha_fin'], '%d/%m/%Y')
                # Ajustar fecha_fin para incluir todo el día
                fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)
                
                movimientos_filtrados = []
                for mov in movimientos:
                    try:
                        fecha_str = mov['fecha']
                        fecha_mov = None
                        
                        # Intentar múltiples formatos de fecha
                        formatos = [
                            '%d/%m/%Y %H:%M:%S',
                            '%Y-%m-%d %H:%M:%S',
                            '%d/%m/%Y',
                            '%Y-%m-%d'
                        ]
                        
                        for formato in formatos:
                            try:
                                fecha_mov = dt.strptime(fecha_str, formato)
                                break
                            except ValueError:
                                continue
                        
                        # Si aún no se pudo parsear, intentar solo la parte de la fecha
                        if fecha_mov is None and ' ' in fecha_str:
                            try:
                                fecha_mov = dt.strptime(fecha_str.split()[0], '%d/%m/%Y')
                            except:
                                try:
                                    fecha_mov = dt.strptime(fecha_str.split()[0], '%Y-%m-%d')
                                except:
                                    pass
                        
                        if fecha_mov and fecha_inicio <= fecha_mov <= fecha_fin:
                            movimientos_filtrados.append(mov)
                    except Exception as e:
                        # Si hay error, omitir este movimiento
                        continue
                
                if not movimientos_filtrados:
                    messagebox.showwarning("Aviso", f"No hay movimientos en el rango seleccionado:\n{rango['fecha_inicio']} - {rango['fecha_fin']}")
                    return
                
                datos = []
                total_ingresos = 0
                total_egresos = 0
                
                for mov in movimientos_filtrados:
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
