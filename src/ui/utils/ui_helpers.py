"""
Funciones auxiliares para la interfaz de usuario.
Utilidades compartidas entre diferentes componentes de la aplicación.
"""

import os
import sys
import tkinter as tk
from datetime import datetime


def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no es PyInstaller, usar la ruta del directorio actual
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def sort_treeview(tree, col, reverse):
    """
    Ordena el treeview por columna (soporta texto, números, fechas y montos).
    
    Args:
        tree: Widget Treeview a ordenar
        col: Columna por la cual ordenar
        reverse: Boolean para orden inverso
    """
    try:
        data_list = [(tree.set(child, col), child) for child in tree.get_children('')]
        
        # Función para convertir valores para ordenamiento correcto
        def convert_value(val):
            # Intentar convertir fechas (formato dd/mm/yyyy)
            if '/' in str(val) and len(str(val).split('/')) == 3:
                try:
                    parts = str(val).split('/')
                    if len(parts[0]) <= 2:  # dd/mm/yyyy
                        return datetime.strptime(str(val), '%d/%m/%Y')
                except:
                    pass
            
            # Intentar convertir números (incluyendo montos con Q, comas, etc.)
            try:
                # Limpiar formato de moneda y comas
                clean_val = str(val).replace('Q', '').replace(',', '').strip()
                return float(clean_val)
            except:
                pass
            
            # Si no es fecha ni número, devolver como texto en minúsculas
            return str(val).lower()
        
        # Ordenar con la función de conversión
        data_list.sort(key=lambda x: convert_value(x[0]), reverse=reverse)
        
        # Reordenar los items en el tree
        for index, (val, child) in enumerate(data_list):
            tree.move(child, '', index)
        
        # Actualizar el comando del heading para alternar el orden
        tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))
    except Exception as e:
        # Si hay error, intentar ordenamiento simple
        try:
            data_list = [(tree.set(child, col), child) for child in tree.get_children('')]
            data_list.sort(reverse=reverse)
            for index, (val, child) in enumerate(data_list):
                tree.move(child, '', index)
            tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))
        except:
            pass


def centrar_ventana(ventana):
    """
    Centra una ventana en la pantalla.
    
    Args:
        ventana: Ventana de tkinter a centrar
    """
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()
    alto_ventana = ventana.winfo_height()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    
    ventana.geometry(f'+{x}+{y}')


def agregar_icono(ventana):
    """
    Agrega el icono de la aplicación a una ventana.
    
    Args:
        ventana: Ventana de tkinter a la que agregar el icono
    """
    try:
        icon_path = resource_path("inventario.ico")
        if os.path.exists(icon_path):
            ventana.iconbitmap(icon_path)
    except Exception as e:
        print(f"No se pudo cargar el icono: {e}")
        pass
    except:
        pass


def configurar_navegacion_calendario(date_entry):
    """
    Configura navegación mejorada por año en un DateEntry usando atajos de teclado.
    
    Atajos:
    - Ctrl + Arriba/Abajo: Cambiar año
    - Ctrl + Izquierda/Derecha: Cambiar mes
    
    Args:
        date_entry: Widget DateEntry a configurar
    """
    try:
        # Verificar si el campo está deshabilitado - NO modificar su estado si está disabled
        estado_actual = str(date_entry.entry.cget('state'))
        
        # Solo configurar si no está deshabilitado
        if estado_actual != 'disabled':
            # Permitir edición manual completa del campo de fecha
            date_entry.entry.configure(state='normal')
        
        def cambiar_año_rapido(event, delta):
            """Cambia el año con Ctrl+Arriba/Abajo"""
            try:
                fecha_actual = datetime.strptime(date_entry.entry.get(), '%d/%m/%Y')
                nueva_fecha = fecha_actual.replace(year=fecha_actual.year + delta)
                date_entry.entry.delete(0, tk.END)
                date_entry.entry.insert(0, nueva_fecha.strftime('%d/%m/%Y'))
                return "break"  # Evitar propagación del evento
            except:
                pass
                
        def cambiar_mes_rapido(event, delta):
            """Cambia el mes con Ctrl+Izquierda/Derecha"""
            try:
                from dateutil.relativedelta import relativedelta
                fecha_actual = datetime.strptime(date_entry.entry.get(), '%d/%m/%Y')
                nueva_fecha = fecha_actual + relativedelta(months=delta)
                date_entry.entry.delete(0, tk.END)
                date_entry.entry.insert(0, nueva_fecha.strftime('%d/%m/%Y'))
                return "break"
            except:
                # Si no está disponible dateutil, usar aproximación
                try:
                    from datetime import timedelta
                    fecha_actual = datetime.strptime(date_entry.entry.get(), '%d/%m/%Y')
                    nueva_fecha = fecha_actual + timedelta(days=30*delta)
                    date_entry.entry.delete(0, tk.END)
                    date_entry.entry.insert(0, nueva_fecha.strftime('%d/%m/%Y'))
                    return "break"
                except:
                    pass
        
        # Atajos de teclado
        # Ctrl + Arriba/Abajo para cambiar año
        date_entry.entry.bind('<Control-Up>', lambda e: cambiar_año_rapido(e, 1))
        date_entry.entry.bind('<Control-Down>', lambda e: cambiar_año_rapido(e, -1))
        
        # Ctrl + Izquierda/Derecha para cambiar mes
        date_entry.entry.bind('<Control-Left>', lambda e: cambiar_mes_rapido(e, -1))
        date_entry.entry.bind('<Control-Right>', lambda e: cambiar_mes_rapido(e, 1))
        
    except Exception as e:
        print(f"Error configurando navegación de calendario: {e}")
        pass
