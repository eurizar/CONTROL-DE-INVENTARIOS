"""
Módulo de pestañas (tabs) del sistema de inventario.
Cada tab representa una sección principal de la aplicación.
"""

from .ventas_tab import VentasTab
from .compras_tab import ComprasTab
from .productos_tab import ProductosTab
from .clientes_tab import ClientesTab
from .proveedores_tab import ProveedoresTab
from .caja_tab import CajaTab

__all__ = [
    'VentasTab',
    'ComprasTab',
    'ProductosTab',
    'ClientesTab',
    'ProveedoresTab',
    'CajaTab'
]
