"""
Sistema de configuración persistente
Maneja la configuración de la aplicación, incluyendo el tema seleccionado.
"""
import json
import os
import sys

class Settings:
    """Clase para manejar la configuración de la aplicación"""
    
    CONFIG_FILE = "data/config.json"
    DEFAULT_CONFIG = {
        "theme": "superhero",
        "db_path": "data/inventarios.db",
        "use_cloud_storage": False
    }
    
    @classmethod
    def _ensure_data_dir(cls):
        """Asegura que el directorio data existe"""
        os.makedirs("data", exist_ok=True)
    
    @classmethod
    def load_config(cls):
        """Carga la configuración desde el archivo JSON"""
        cls._ensure_data_dir()
        
        if not os.path.exists(cls.CONFIG_FILE):
            # Si no existe el archivo, crear con configuración por defecto
            cls.save_config(cls.DEFAULT_CONFIG)
            return cls.DEFAULT_CONFIG.copy()
        
        try:
            with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
            return cls.DEFAULT_CONFIG.copy()
    
    @classmethod
    def save_config(cls, config):
        """Guarda la configuración en el archivo JSON"""
        cls._ensure_data_dir()
        
        try:
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            return False
    
    @classmethod
    def get_theme(cls):
        """Obtiene el tema guardado"""
        config = cls.load_config()
        return config.get("theme", cls.DEFAULT_CONFIG["theme"])
    
    @classmethod
    def set_theme(cls, theme_name):
        """Guarda el tema seleccionado"""
        config = cls.load_config()
        config["theme"] = theme_name
        return cls.save_config(config)
    
    @classmethod
    def get_db_path(cls):
        """Obtiene la ruta de la base de datos"""
        config = cls.load_config()
        return config.get("db_path", cls.DEFAULT_CONFIG["db_path"])
    
    @classmethod
    def set_db_path(cls, db_path):
        """Guarda la ruta de la base de datos"""
        config = cls.load_config()
        config["db_path"] = db_path
        return cls.save_config(config)
    
    @classmethod
    def is_using_cloud_storage(cls):
        """Verifica si está usando almacenamiento en la nube"""
        config = cls.load_config()
        return config.get("use_cloud_storage", False)
    
    @classmethod
    def set_cloud_storage(cls, use_cloud):
        """Configura el uso de almacenamiento en la nube"""
        config = cls.load_config()
        config["use_cloud_storage"] = use_cloud
        return cls.save_config(config)
    
    @classmethod
    def detect_onedrive_path(cls):
        """Detecta automáticamente la ruta de OneDrive"""
        # Buscar en variables de entorno de Windows
        onedrive_paths = [
            os.environ.get('OneDrive'),
            os.environ.get('OneDriveCommercial'),
            os.environ.get('OneDriveConsumer'),
        ]
        
        # Filtrar rutas válidas
        for path in onedrive_paths:
            if path and os.path.exists(path):
                return path
        
        # Rutas comunes de OneDrive
        username = os.environ.get('USERNAME', '')
        common_paths = [
            f"C:\\Users\\{username}\\OneDrive",
            f"C:\\Users\\{username}\\OneDrive - ",  # OneDrive empresarial
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    @classmethod
    def get_suggested_onedrive_db_path(cls):
        """Sugiere una ruta de BD en OneDrive"""
        onedrive = cls.detect_onedrive_path()
        if onedrive:
            # Crear carpeta para el sistema
            app_folder = os.path.join(onedrive, "Sistema_Inventarios")
            return os.path.join(app_folder, "inventarios.db")
        return None
