"""
Modelos de datos para el sistema de inventarios
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Producto:
    """Modelo para un producto en el inventario"""
    id: Optional[int]
    nombre: str
    precio_compra: float
    porcentaje_ganancia: float
    precio_venta: float
    stock_actual: int
    fecha_creacion: Optional[datetime] = None
    
    def calcular_precio_venta(self) -> float:
        """Calcula el precio de venta basado en el precio de compra y ganancia"""
        return self.precio_compra * (1 + self.porcentaje_ganancia / 100)
    
    def to_dict(self) -> dict:
        """Convierte el producto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio_compra': self.precio_compra,
            'porcentaje_ganancia': self.porcentaje_ganancia,
            'precio_venta': self.precio_venta,
            'stock_actual': self.stock_actual,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

@dataclass
class Compra:
    """Modelo para una compra de mercadería"""
    id: Optional[int]
    producto_id: int
    cantidad: int
    precio_unitario: float
    total: float
    fecha: Optional[datetime] = None
    producto_nombre: Optional[str] = None
    
    def calcular_total(self) -> float:
        """Calcula el total de la compra"""
        return self.cantidad * self.precio_unitario

@dataclass
class Venta:
    """Modelo para una venta"""
    id: Optional[int]
    producto_id: int
    cantidad: int
    precio_unitario: float
    total: float
    fecha: Optional[datetime] = None
    producto_nombre: Optional[str] = None
    
    def calcular_total(self) -> float:
        """Calcula el total de la venta"""
        return self.cantidad * self.precio_unitario

@dataclass
class MovimientoStock:
    """Modelo para un movimiento de stock"""
    id: Optional[int]
    producto_id: int
    tipo: str  # 'entrada' o 'salida'
    cantidad: int
    motivo: str  # 'compra', 'venta', 'ajuste'
    fecha: Optional[datetime] = None
    producto_nombre: Optional[str] = None

@dataclass
class ResumenInventario:
    """Modelo para el resumen del inventario"""
    total_compras: float
    total_ventas: float
    ganancia_bruta: float
    valor_inventario: float
    saldo_banco: float
    
    def get_ganancia_porcentaje(self) -> float:
        """Calcula el porcentaje de ganancia sobre las compras"""
        if self.total_compras > 0:
            return (self.ganancia_bruta / self.total_compras) * 100
        return 0
