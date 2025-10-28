"""
Ventana de Login para el Sistema de Control de Inventarios
"""
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.database.database_manager import DatabaseManager
from src.config.settings import Settings
from datetime import datetime
import os
import sys


def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, funciona para dev y para PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class LoginWindow:
    """Ventana de autenticación de usuarios"""
    
    def __init__(self, parent=None):
        # Cargar el tema guardado
        tema_guardado = Settings.get_theme()
        
        # Si no hay parent, crear una nueva ventana raíz
        if parent is None:
            self.root = ttk.Window(themename=tema_guardado)
            self.es_ventana_principal = True
        else:
            self.root = ttk.Toplevel(parent)
            self.es_ventana_principal = False
        
        # Ocultar ventana temporalmente para evitar parpadeo al centrar
        self.root.withdraw()
            
        self.root.title("Login")
        self.root.geometry("450x625")
        self.root.resizable(False, False)
        
        # Configurar icono
        try:
            icon_path = resource_path("inventario.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"No se pudo cargar el icono en login: {e}")
            pass  # Si no encuentra el icono, continuar sin él
        
        # Variable para almacenar el usuario autenticado
        self.usuario_autenticado = None
        
        # Inicializar base de datos
        self.db = DatabaseManager()
        
        # Configurar la ventana
        self.setup_ui()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Mostrar ventana ya centrada (evita parpadeo)
        self.root.deiconify()
        
        # Vincular Enter para hacer login
        self.root.bind('<Return>', lambda e: self.verificar_credenciales())
        
        # Hacer la ventana modal
        if not self.es_ventana_principal:
            self.root.transient(parent)
            self.root.grab_set()
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Logo o título
        titulo_frame = ttk.Frame(main_frame)
        titulo_frame.pack(pady=(0, 30))
        
        # Icono de usuario grande
        ttk.Label(
            titulo_frame,
            text="🔐",
            font=("Segoe UI", 60)
        ).pack()
        
        ttk.Label(
            titulo_frame,
            text="Sistema de Control de Inventarios",
            font=("Segoe UI", 16, "bold"),
            bootstyle="primary"
        ).pack(pady=(10, 5))
        
        ttk.Label(
            titulo_frame,
            text="Versión 2.0",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        ).pack()
        
        # Frame del formulario
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=BOTH, expand=YES, pady=20)
        
        # Campo de usuario
        ttk.Label(
            form_frame,
            text="Usuario:",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor=W, pady=(0, 5))
        
        self.entry_usuario = ttk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            bootstyle="primary"
        )
        self.entry_usuario.pack(fill=X, pady=(0, 20), ipady=8)
        self.entry_usuario.focus()
        
        # Campo de contraseña
        ttk.Label(
            form_frame,
            text="Contraseña:",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor=W, pady=(0, 5))
        
        self.entry_contrasena = ttk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            show="●",
            bootstyle="primary"
        )
        self.entry_contrasena.pack(fill=X, pady=(0, 10), ipady=8)
        
        # Checkbox mostrar contraseña
        self.var_mostrar = tk.BooleanVar()
        ttk.Checkbutton(
            form_frame,
            text="Mostrar contraseña",
            variable=self.var_mostrar,
            command=self.toggle_password,
            bootstyle="primary-round-toggle"
        ).pack(anchor=W, pady=(0, 30))
        
        # Frame para botones en la misma línea
        botones_frame = ttk.Frame(form_frame)
        botones_frame.pack(pady=(0, 10))
        
        # Botón de login
        self.btn_login = ttk.Button(
            botones_frame,
            text="INGRESAR",
            command=self.verificar_credenciales,
            bootstyle="primary",
            width=15
        )
        self.btn_login.pack(side=LEFT, padx=5, ipady=8)
        
        # Botón de cancelar/salir
        ttk.Button(
            botones_frame,
            text="Cancelar",
            command=self.root.quit,
            bootstyle="danger",
            width=15
        ).pack(side=LEFT, padx=5, ipady=8)
        
        # Footer con información
        footer_frame = ttk.Frame(form_frame)
        footer_frame.pack(pady=(30, 0))
        
        ttk.Label(
            footer_frame,
            text="© 2025 Elizandro Urizar",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack()
    
    def toggle_password(self):
        """Muestra u oculta la contraseña"""
        if self.var_mostrar.get():
            self.entry_contrasena.config(show="")
        else:
            self.entry_contrasena.config(show="●")
    
    def verificar_credenciales(self):
        """Verifica las credenciales del usuario"""
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        
        # Validar campos vacíos
        if not usuario:
            messagebox.showwarning(
                "Campo requerido",
                "Por favor ingresa tu usuario",
                parent=self.root
            )
            self.entry_usuario.focus()
            return
        
        if not contrasena:
            messagebox.showwarning(
                "Campo requerido",
                "Por favor ingresa tu contraseña",
                parent=self.root
            )
            self.entry_contrasena.focus()
            return
        
        # Verificar credenciales en la base de datos
        usuario_data = self.db.verificar_usuario(usuario, contrasena)
        
        if usuario_data:
            self.usuario_autenticado = usuario_data
            # Mostrar ventana de bienvenida personalizada con icono
            self.mostrar_bienvenida(usuario_data['nombre_completo'])
            # Cerrar solo esta ventana
            if self.es_ventana_principal:
                self.root.quit()
            else:
                self.root.destroy()
        else:
            messagebox.showerror(
                "Acceso denegado",
                "Usuario o contraseña incorrectos.\n\nPor favor verifica tus credenciales.",
                parent=self.root
            )
            self.entry_contrasena.delete(0, END)
            self.entry_usuario.focus()
    
    def mostrar_bienvenida(self, nombre_completo):
        """Muestra una ventana de bienvenida personalizada con icono"""
        # Crear ventana de diálogo personalizada
        dialog = ttk.Toplevel(self.root)
        dialog.title("Acceso concedido")
        
        # Ocultar ventana temporalmente para evitar parpadeo al centrar
        dialog.withdraw()
        
        dialog.geometry("390x230")
        dialog.resizable(False, False)
        
        # Agregar icono del sistema
        try:
            icon_path = resource_path("inventario.ico")
            if os.path.exists(icon_path):
                dialog.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Centrar el diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (390 // 2)
        y = (dialog.winfo_screenheight() // 2) - (230 // 2)
        dialog.geometry(f'390x230+{x}+{y}')
        
        # Hacer modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Contenido
        main_frame = ttk.Frame(dialog, padding=40)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Mensaje de bienvenida
        ttk.Label(
            main_frame,
            text="¡Bienvenido!",
            font=("Segoe UI", 18, "bold"),
            foreground="#212529"
        ).pack(pady=(50, 30))
        
        # Botón Aceptar
        btn_aceptar = ttk.Button(
            main_frame,
            text="Aceptar",
            command=dialog.destroy,
            bootstyle="success",
            width=20
        )
        btn_aceptar.pack(ipady=10)
        # Configurar fuente en negrita
        btn_aceptar.configure(style='success.TButton')
        try:
            from tkinter import font as tkfont
            btn_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
            btn_aceptar.configure(font=btn_font)
        except:
            pass
        
        # Mostrar ventana ya centrada (evita parpadeo)
        dialog.deiconify()
        
        # Esperar a que se cierre el diálogo
        dialog.wait_window()
    
    def run(self):
        """Ejecuta el loop principal de la ventana"""
        if self.es_ventana_principal:
            self.root.mainloop()
        else:
            self.root.wait_window()
        return self.usuario_autenticado


if __name__ == "__main__":
    login = LoginWindow()
    usuario = login.run()
    if usuario:
        print(f"Usuario autenticado: {usuario}")
    else:
        print("Login cancelado")
