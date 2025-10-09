"""
Controlador principal para el sistema de inventarios
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from src.database.database_manager import DatabaseManager
from src.models.models import Producto, Compra, Venta, ResumenInventario

class InventarioController:
    def eliminar_producto(self, producto_id: int) -> tuple:
        """Elimina un producto y sus movimientos relacionados"""
        try:
            exito = self.db.eliminar_producto(producto_id)
            if exito:
                return True, "Producto eliminado correctamente."
            else:
                return False, "No se pudo eliminar el producto."
        except Exception as e:
            return False, f"Error al eliminar producto: {str(e)}"
    def __init__(self, db_path: str = "data/inventarios.db"):
        self.db = DatabaseManager(db_path)
    
    # GESTIÓN DE PRODUCTOS
    def crear_producto(self, codigo: str, nombre: str, categoria: str, precio_compra: float, porcentaje_ganancia: float, marca: str = '', color: str = '', tamaño: str = '') -> Tuple[bool, str]:
        """Crea un nuevo producto con datos adicionales del SKU"""
        try:
            if not nombre.strip():
                return False, "El nombre del producto no puede estar vacío"
            
            if precio_compra <= 0:
                return False, "El precio de compra debe ser mayor a 0"
            
            if porcentaje_ganancia < 0:
                return False, "El porcentaje de ganancia no puede ser negativo"
            
            producto_id = self.db.crear_producto(codigo.strip() if codigo else "", nombre.strip(), categoria.strip() if categoria else "", precio_compra, porcentaje_ganancia, marca.strip(), color.strip(), tamaño.strip())
            return True, f"Producto creado con ID: {producto_id}"
        
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "Ya existe un producto con ese código"
            return False, f"Error al crear producto: {str(e)}"
    
    def obtener_productos(self) -> List[Dict]:
        """Obtiene todos los productos"""
        return self.db.obtener_productos()
    
    def obtener_producto_por_id(self, producto_id: int) -> Optional[Dict]:
        """Obtiene un producto por su ID"""
        return self.db.obtener_producto_por_id(producto_id)
    
    def actualizar_producto(self, producto_id: int, codigo: str, nombre: str, categoria: str, precio_compra: float, porcentaje_ganancia: float, marca: str = '', color: str = '', tamaño: str = '') -> Tuple[bool, str]:
        """Actualiza un producto existente con datos adicionales del SKU"""
        try:
            if not nombre.strip():
                return False, "El nombre del producto no puede estar vacío"
            
            if precio_compra <= 0:
                return False, "El precio de compra debe ser mayor a 0"
            
            if porcentaje_ganancia < 0:
                return False, "El porcentaje de ganancia no puede ser negativo"
            
            filas_afectadas = self.db.actualizar_producto(producto_id, codigo.strip() if codigo else "", nombre.strip(), categoria.strip() if categoria else "", precio_compra, porcentaje_ganancia, marca.strip(), color.strip(), tamaño.strip())
            
            if filas_afectadas > 0:
                return True, "Producto actualizado correctamente"
            else:
                return False, "No se pudo actualizar el producto"
        
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "Ya existe un producto con ese código"
            return False, f"Error al actualizar producto: {str(e)}"
    
    def cambiar_estado_producto(self, producto_id: int, activo: bool) -> Tuple[bool, str]:
        """Cambia el estado activo/inactivo de un producto"""
        try:
            # Verificar que el producto existe
            producto = self.db.obtener_producto_por_id(producto_id)
            if not producto:
                return False, "Producto no encontrado"
            
            # Cambiar estado
            exito = self.db.cambiar_estado_producto(producto_id, activo)
            
            if exito:
                estado_texto = "activado" if activo else "desactivado"
                return True, f"Producto {estado_texto} correctamente"
            else:
                return False, "No se pudo cambiar el estado del producto"
        
        except Exception as e:
            return False, f"Error al cambiar estado: {str(e)}"
    
    def obtener_productos_activos(self) -> List[Dict]:
        """Obtiene solo los productos activos"""
        return self.db.obtener_productos_activos()
    
    def obtener_productos_inactivos(self) -> List[Dict]:
        """Obtiene solo los productos inactivos"""
        return self.db.obtener_productos_inactivos()
    
    # GESTIÓN DE COMPRAS
    def registrar_compra(self, producto_id: int, cantidad: int, precio_unitario: float,
                        proveedor_id: int, no_documento: str, fecha_manual: str,
                        es_perecedero: bool = False, fecha_vencimiento: str = None) -> Tuple[bool, str]:
        """
        Registra una nueva compra de mercadería
        fecha_manual debe estar en formato 'dd/mm/yyyy HH:MM:SS' o 'dd/mm/yyyy'
        es_perecedero: True si el producto tiene fecha de vencimiento
        fecha_vencimiento: Fecha en formato 'dd/mm/yyyy' (obligatorio si es_perecedero=True)
        """
        try:
            if cantidad <= 0:
                return False, "La cantidad debe ser mayor a 0"
            
            if precio_unitario <= 0:
                return False, "El precio unitario debe ser mayor a 0"
            
            if not no_documento.strip():
                return False, "El número de documento es obligatorio"
            
            # Validar vencimiento si es perecedero
            if es_perecedero and not fecha_vencimiento:
                return False, "La fecha de vencimiento es obligatoria para productos perecederos"
            
            # Verificar que el producto existe
            producto = self.db.obtener_producto_por_id(producto_id)
            if not producto:
                return False, "Producto no encontrado"
            
            # Verificar que el proveedor existe
            proveedor = self.db.obtener_proveedor_por_id(proveedor_id)
            if not proveedor:
                return False, "Proveedor no encontrado"
            
            compra_id = self.db.registrar_compra(producto_id, cantidad, precio_unitario,
                                                proveedor_id, no_documento, fecha_manual,
                                                es_perecedero, fecha_vencimiento)
            return True, f"Compra registrada con ID: {compra_id}"
        
        except Exception as e:
            return False, f"Error al registrar compra: {str(e)}"
    
    def obtener_compras(self) -> List[Dict]:
        """Obtiene todas las compras"""
        return self.db.obtener_compras()
    
    def obtener_productos_proximos_vencer(self, dias_limite: int = 30) -> List[Dict]:
        """Obtiene productos perecederos próximos a vencer"""
        return self.db.obtener_productos_proximos_vencer(dias_limite)
    
    def actualizar_compra_perecedero(self, compra_id: int, es_perecedero: bool, fecha_vencimiento: str = None) -> Tuple[bool, str]:
        """Actualiza el estado de perecedero de una compra"""
        try:
            if es_perecedero and not fecha_vencimiento:
                return False, "La fecha de vencimiento es obligatoria para productos perecederos"
            
            exito = self.db.actualizar_compra_perecedero(compra_id, es_perecedero, fecha_vencimiento)
            if exito:
                return True, "Compra actualizada exitosamente"
            else:
                return False, "Error al actualizar la compra"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # GESTIÓN DE VENTAS
    def registrar_venta(self, producto_id: int, cantidad: int, precio_unitario: float,
                       cliente_id: int, fecha_manual: str) -> Tuple[bool, str]:
        """
        Registra una nueva venta
        fecha_manual debe estar en formato 'dd/mm/yyyy HH:MM:SS' o 'dd/mm/yyyy'
        El número de referencia se genera automáticamente
        """
        try:
            if cantidad <= 0:
                return False, "La cantidad debe ser mayor a 0"
            
            if precio_unitario <= 0:
                return False, "El precio unitario debe ser mayor a 0"
            
            # Verificar que el cliente existe
            cliente = self.db.obtener_cliente_por_id(cliente_id)
            if not cliente:
                return False, "Cliente no encontrado"
            
            exito, mensaje = self.db.registrar_venta(producto_id, cantidad, precio_unitario,
                                                     cliente_id, fecha_manual)
            return exito, mensaje
        
        except Exception as e:
            return False, f"Error al registrar venta: {str(e)}"
    
    def obtener_ventas(self) -> List[Dict]:
        """Obtiene todas las ventas"""
        return self.db.obtener_ventas()
    
    # GESTIÓN DE PROVEEDORES
    def crear_proveedor(self, nombre: str, nit_dpi: str, direccion: str, telefono: str = "") -> Tuple[bool, str]:
        """Crea un nuevo proveedor"""
        try:
            if not nombre.strip():
                return False, "El nombre del proveedor es obligatorio"
            
            if not nit_dpi.strip():
                return False, "El NIT o DPI es obligatorio"
            
            if not direccion.strip():
                return False, "La dirección es obligatoria"
            
            proveedor_id = self.db.crear_proveedor(nombre.strip(), nit_dpi.strip(), 
                                                   direccion.strip(), telefono.strip())
            return True, f"Proveedor creado con ID: {proveedor_id}"
        
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "Ya existe un proveedor con ese NIT o DPI"
            return False, f"Error al crear proveedor: {str(e)}"
    
    def obtener_proveedores(self) -> List[Dict]:
        """Obtiene todos los proveedores"""
        return self.db.obtener_proveedores()
    
    def obtener_proveedor_por_id(self, proveedor_id: int) -> Optional[Dict]:
        """Obtiene un proveedor por su ID"""
        return self.db.obtener_proveedor_por_id(proveedor_id)
    
    def buscar_proveedor(self, busqueda: str) -> List[Dict]:
        """Busca proveedores por nombre o NIT"""
        if not busqueda.strip():
            return self.obtener_proveedores()
        return self.db.buscar_proveedor(busqueda.strip())
    
    def actualizar_proveedor(self, proveedor_id: int, nombre: str, nit_dpi: str, 
                           direccion: str, telefono: str = "") -> Tuple[bool, str]:
        """Actualiza un proveedor existente"""
        try:
            if not nombre.strip():
                return False, "El nombre del proveedor es obligatorio"
            
            if not nit_dpi.strip():
                return False, "El NIT o DPI es obligatorio"
            
            if not direccion.strip():
                return False, "La dirección es obligatoria"
            
            filas_afectadas = self.db.actualizar_proveedor(proveedor_id, nombre.strip(), 
                                                          nit_dpi.strip(), direccion.strip(), 
                                                          telefono.strip())
            
            if filas_afectadas > 0:
                return True, "Proveedor actualizado correctamente"
            else:
                return False, "No se pudo actualizar el proveedor"
        
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "Ya existe un proveedor con ese NIT o DPI"
            return False, f"Error al actualizar proveedor: {str(e)}"
    
    # GESTIÓN DE CLIENTES
    def crear_cliente(self, nombre: str, nit_dpi: str, direccion: str, telefono: str = "") -> Tuple[bool, str]:
        """Crea un nuevo cliente"""
        try:
            if not nombre.strip():
                return False, "El nombre del cliente es obligatorio"
            
            if not nit_dpi.strip():
                return False, "El NIT o DPI es obligatorio"
            
            if not direccion.strip():
                return False, "La dirección es obligatoria"
            
            cliente_id = self.db.crear_cliente(nombre.strip(), nit_dpi.strip(), 
                                              direccion.strip(), telefono.strip())
            return True, f"Cliente creado con ID: {cliente_id}"
        
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "Ya existe un cliente con ese NIT o DPI"
            return False, f"Error al crear cliente: {str(e)}"
    
    def obtener_clientes(self) -> List[Dict]:
        """Obtiene todos los clientes"""
        return self.db.obtener_clientes()
    
    def obtener_cliente_por_id(self, cliente_id: int) -> Optional[Dict]:
        """Obtiene un cliente por su ID"""
        return self.db.obtener_cliente_por_id(cliente_id)
    
    def buscar_cliente(self, busqueda: str) -> List[Dict]:
        """Busca clientes por nombre o NIT"""
        if not busqueda.strip():
            return self.obtener_clientes()
        return self.db.buscar_cliente(busqueda.strip())
    
    def actualizar_cliente(self, cliente_id: int, nombre: str, nit_dpi: str, 
                          direccion: str, telefono: str = "") -> Tuple[bool, str]:
        """Actualiza un cliente existente"""
        try:
            if not nombre.strip():
                return False, "El nombre del cliente es obligatorio"
            
            if not nit_dpi.strip():
                return False, "El NIT o DPI es obligatorio"
            
            if not direccion.strip():
                return False, "La dirección es obligatoria"
            
            filas_afectadas = self.db.actualizar_cliente(cliente_id, nombre.strip(), 
                                                        nit_dpi.strip(), direccion.strip(), 
                                                        telefono.strip())
            
            if filas_afectadas > 0:
                return True, "Cliente actualizado correctamente"
            else:
                return False, "No se pudo actualizar el cliente"
        
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "Ya existe un cliente con ese NIT o DPI"
            return False, f"Error al actualizar cliente: {str(e)}"
    
    # REPORTES Y RESÚMENES
    def obtener_resumen_inventario(self) -> Dict:
        """Obtiene un resumen completo del inventario"""
        return self.db.obtener_resumen_inventario()
    
    def obtener_productos_con_stock_bajo(self, limite: int = 5) -> List[Dict]:
        """Obtiene productos con stock bajo (solo activos)"""
        productos = self.db.obtener_productos_activos()  # Solo productos activos
        return [p for p in productos if p['stock_actual'] <= limite]
    
    def obtener_movimientos_stock(self, producto_id: int = None) -> List[Dict]:
        """Obtiene los movimientos de stock"""
        return self.db.obtener_movimientos_stock(producto_id)
    
    def calcular_ganancia_producto(self, producto_id: int) -> Dict:
        """Calcula la ganancia de un producto específico"""
        try:
            # Obtener todas las compras del producto
            compras = [c for c in self.db.obtener_compras() if c['producto_id'] == producto_id]
            total_comprado = sum(c['total'] for c in compras)
            cantidad_comprada = sum(c['cantidad'] for c in compras)
            
            # Obtener todas las ventas del producto
            ventas = [v for v in self.db.obtener_ventas() if v['producto_id'] == producto_id]
            total_vendido = sum(v['total'] for v in ventas)
            cantidad_vendida = sum(v['cantidad'] for v in ventas)
            
            ganancia = total_vendido - (cantidad_vendida * (total_comprado / cantidad_comprada if cantidad_comprada > 0 else 0))
            
            return {
                'producto_id': producto_id,
                'total_comprado': total_comprado,
                'cantidad_comprada': cantidad_comprada,
                'total_vendido': total_vendido,
                'cantidad_vendida': cantidad_vendida,
                'ganancia': ganancia,
                'porcentaje_ganancia': (ganancia / total_comprado * 100) if total_comprado > 0 else 0
            }
        
        except Exception as e:
            return {
                'error': f"Error al calcular ganancia: {str(e)}"
            }
    
    # GESTIÓN DE BASE DE DATOS
    def cambiar_base_datos(self, nueva_ruta: str) -> Tuple[bool, str]:
        """Cambia la base de datos activa"""
        try:
            if self.db.cambiar_base_datos(nueva_ruta):
                return True, f"Base de datos cambiada a: {nueva_ruta}"
            else:
                return False, "No se pudo cambiar la base de datos"
        except Exception as e:
            return False, f"Error al cambiar base de datos: {str(e)}"
    
    def exportar_resumen(self) -> str:
        """Exporta un resumen completo del inventario"""
        try:
            resumen = self.obtener_resumen_inventario()
            productos = self.obtener_productos()
            
            texto_resumen = f"""
=== RESUMEN DEL INVENTARIO ===
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

TOTALES GENERALES:
- Total Compras: Q {resumen['total_compras']:.2f}
- Total Ventas: Q {resumen['total_ventas']:.2f}
- Ganancia Bruta: Q {resumen['ganancia_bruta']:.2f}
- Valor Inventario Actual: Q {resumen['valor_inventario']:.2f}
- Saldo en Banco: Q {resumen['saldo_banco']:.2f}

PRODUCTOS EN INVENTARIO:
"""
            for producto in productos:
                texto_resumen += f"""
- {producto['nombre']}:
  * Precio Compra: Q {producto['precio_compra']:.2f}
  * Ganancia: {producto['porcentaje_ganancia']:.1f}%
  * Precio Venta: Q {producto['precio_venta']:.2f}
  * Stock Actual: {producto['stock_actual']} unidades
"""
            
            return texto_resumen
        
        except Exception as e:
            return f"Error al generar resumen: {str(e)}"
    
    # GESTIÓN DE CAJA
    def obtener_saldo_caja(self) -> float:
        """Obtiene el saldo actual de caja"""
        return self.db.obtener_saldo_caja()
    
    def registrar_movimiento_caja(self, tipo: str, categoria: str, concepto: str, 
                                   monto: float, fecha_manual: str = None) -> Tuple[bool, str]:
        """Registra un movimiento manual de caja"""
        try:
            if not concepto.strip():
                return False, "El concepto no puede estar vacío"
            
            if monto <= 0:
                return False, "El monto debe ser mayor a 0"
            
            if tipo not in ['INGRESO', 'EGRESO']:
                return False, "El tipo debe ser INGRESO o EGRESO"
            
            # Si no se proporciona fecha, usar la actual
            if not fecha_manual:
                fecha_manual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            
            movimiento_id = self.db.registrar_movimiento_caja(tipo, categoria, concepto, 
                                                              monto, fecha_manual)
            return True, f"Movimiento registrado correctamente (ID: {movimiento_id})"
        
        except Exception as e:
            return False, f"Error al registrar movimiento: {str(e)}"
    
    def obtener_movimientos_caja(self, fecha_inicio: str = None, fecha_fin: str = None) -> List[Dict]:
        """Obtiene los movimientos de caja"""
        return self.db.obtener_movimientos_caja(fecha_inicio, fecha_fin)
    
    def obtener_resumen_caja(self, fecha_inicio: str = None, fecha_fin: str = None) -> Dict:
        """Obtiene el resumen de movimientos de caja"""
        return self.db.obtener_resumen_caja(fecha_inicio, fecha_fin)
    
    def eliminar_movimiento_caja(self, movimiento_id: int) -> Tuple[bool, str]:
        """Elimina un movimiento de caja"""
        try:
            self.db.eliminar_movimiento_caja(movimiento_id)
            return True, "Movimiento eliminado correctamente"
        except Exception as e:
            return False, f"Error al eliminar movimiento: {str(e)}"

