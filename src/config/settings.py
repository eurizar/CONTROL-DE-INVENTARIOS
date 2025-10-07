"""
Sistema de configuración persistente
Maneja la configuración de la aplicación, incluyendo el tema seleccionado.
"""
import json
import os

class Settings:
    """Clase para manejar la configuración de la aplicación"""
    
    CONFIG_FILE = "data/config.json"
    DEFAULT_CONFIG = {
        "theme": "superhero"
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
