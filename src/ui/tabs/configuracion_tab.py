"""
Módulo de configuración del sistema
Gestión de base de datos, temas, OneDrive y configuraciones generales
"""
import ttkbootstrap as tb
from tkinter import messagebox, filedialog
import tkinter as tk
import os
from src.config.settings import Settings


class ConfiguracionTab:
    """Pestaña de configuración del sistema"""
    
    def __init__(self, parent_frame, controller, main_window):
        self.parent_frame = parent_frame
        self.controller = controller
        self.main_window = main_window
        
        # Crear interfaz
        self.create_ui()
    
    def create_ui(self):
        """Crea la interfaz de usuario de configuración"""
        # Frame contenedor para las dos columnas
        columns_container = tb.Frame(self.parent_frame, bootstyle="light")
        columns_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Columna izquierda
        self.crear_columna_izquierda(columns_container)
        
        # Columna derecha
        self.crear_columna_derecha(columns_container)
    
    def crear_columna_izquierda(self, container):
        """Crea la columna izquierda con gestión de BD, OneDrive y temas"""
        left_column = tb.Frame(container, bootstyle="light")
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Panel de base de datos
        self.crear_panel_base_datos(left_column)
        
        # Panel de OneDrive
        self.crear_panel_onedrive(left_column)
        
        # Panel de temas
        self.crear_panel_temas(left_column)
    
    def crear_panel_base_datos(self, container):
        """Crea el panel de gestión de base de datos"""
        db_frame = tb.Labelframe(
            container, 
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
    
    def crear_panel_onedrive(self, container):
        """Crea el panel de sincronización con OneDrive"""
        onedrive_frame = tb.Labelframe(
            container, 
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
    
    def crear_panel_temas(self, container):
        """Crea el panel de selección de temas"""
        theme_frame = tb.Labelframe(
            container, 
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
    
    def crear_columna_derecha(self, container):
        """Crea la columna derecha con información del sistema"""
        right_column = tb.Frame(container, bootstyle="light")
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
        
        # Contenido de información completo
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
    
    # ========== MÉTODOS DE GESTIÓN DE BASE DE DATOS ==========
    
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
                self.refresh()
                self.refresh_all_tabs()
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
                self.refresh()
                self.refresh_all_tabs()
            else:
                messagebox.showerror("Error", mensaje)
    
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
    
    # ========== MÉTODOS DE ONEDRIVE ==========
    
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
            self.refresh()
            self.refresh_all_tabs()
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
                self.refresh()
                self.refresh_all_tabs()
            else:
                messagebox.showerror("Error", mensaje)
    
    # ========== MÉTODO DE CAMBIO DE TEMA ==========
    
    def cambiar_tema(self, tema):
        """Cambia el tema de la aplicación"""
        try:
            # Cambiar el tema usando el root de main_window
            if hasattr(self.main_window, 'root') and hasattr(self.main_window.root, 'style'):
                self.main_window.root.style.theme_use(tema)
            
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
            if hasattr(self.main_window, 'setup_treeview_selection_style'):
                self.main_window.setup_treeview_selection_style()
            
            messagebox.showinfo("Tema Cambiado", f"Tema '{tema}' aplicado correctamente.\n\nReinicia la aplicación para ver todos los cambios.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cambiar el tema: {str(e)}")
    
    # ========== MÉTODO DE ACTUALIZACIÓN ==========
    
    def refresh(self):
        """Actualiza la información de configuración"""
        # Actualizar ruta de BD
        self.db_actual_label.config(text=self.controller.db.db_path)
        
        # Actualizar estado de OneDrive
        current_db = Settings.get_db_path()
        is_cloud = Settings.is_using_cloud_storage()
        
        if is_cloud:
            estado_text = f"🌐 Nube\n{current_db[:50]}..."
            estado_style = "success"
        else:
            estado_text = f"💻 Local\n{current_db[:50]}..."
            estado_style = "secondary"
        
        self.estado_cloud_label.config(text=estado_text, bootstyle=estado_style)
    
    def refresh_all_tabs(self):
        """Refresca todos los tabs de la aplicación después de cambiar BD"""
        # Llamar al refresh de main_window si existe
        if hasattr(self.main_window, 'refresh_all_data'):
            self.main_window.refresh_all_data()
