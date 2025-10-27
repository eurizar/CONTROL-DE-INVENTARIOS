"""
Módulo de ventanas de diálogo del sistema de inventario.
Contiene ventanas emergentes para funcionalidades específicas.
"""

from .venta_detalle import VentaDetalleDialog
from .cliente_dialogo import ClienteDialogo
from .producto_dialogo import ProductoDialogo

__all__ = [
    'VentaDetalleDialog',
    'ClienteDialogo',
    'ProductoDialogo'
]
