"""
Sistema de Control de Inventarios v2.0
=======================================

Archivo principal para iniciar la aplicación de gestión de inventarios.

Autor: Elizandro Urizar
Email: elizandrou@outlook.com
Fecha: Octubre 2025
Versión: 2.0

© 2025 Elizandro Urizar. Todos los derechos reservados.

SOFTWARE PROPIETARIO - Uso Personal Gratuito
Uso comercial requiere licencia pagada.
Contacto para licencias: elizandrou@outlook.com
"""
import sys
import os
import json

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.ui.main_window import MainWindow
    
    def main():
        """Función principal de la aplicación"""
        print("Iniciando Sistema de Control de Inventarios...")
        print("Versión 1.0")
        print("=" * 50)
        
        # Crear y ejecutar la aplicación
        app = MainWindow()
        app.run()
        
        print("Aplicación cerrada correctamente.")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrate de que todas las dependencias estén instaladas.")
    print("Ejecuta: pip install tkinter ttkbootstrap")
    sys.exit(1)

except Exception as e:
    print(f"Error inesperado: {e}")
    sys.exit(1)

class Settings:
    """Maneja la configuración de la aplicación"""
    
    def __init__(self):
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        self.config_file = os.path.join(self.config_dir, 'config.json')
        self.config = self.load_config()
    
    def load_config(self):
        """Carga la configuración desde el archivo"""
        # Crear directorio si no existe
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Si el archivo no existe, crear configuración por defecto
        if not os.path.exists(self.config_file):
            default_config = {
                'theme': 'cosmo',
                'window_size': '1400x850'
            }
            self.save_config(default_config)
            return default_config
        
        # Cargar configuración existente
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
            return {'theme': 'cosmo', 'window_size': '1400x850'}
    
    def save_config(self, config=None):
        """Guarda la configuración en el archivo"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
    
    def get_theme(self):
        """Obtiene el tema guardado"""
        return self.config.get('theme', 'cosmo')
    
    def set_theme(self, theme):
        """Guarda el tema seleccionado"""
        self.config['theme'] = theme
        self.save_config()
