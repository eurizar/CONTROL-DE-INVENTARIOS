"""
Gestor de base de datos para el sistema de inventarios
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = None):
        """
        Inicializa el gestor de base de datos.
        Si db_path es None, usa la ruta configurada en Settings.
        """
        if db_path is None:
            # Importar Settings aquí para evitar importación circular
            from src.config.settings import Settings
            db_path = Settings.get_db_path()
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos con todas las tablas necesarias"""
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla de proveedores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS proveedores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    nit_dpi TEXT NOT NULL UNIQUE,
                    direccion TEXT NOT NULL,
                    telefono TEXT,
                    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    nit_dpi TEXT NOT NULL UNIQUE,
                    direccion TEXT,
                    telefono TEXT,
                    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de productos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE,
                    nombre TEXT NOT NULL UNIQUE,
                    categoria TEXT,
                    precio_compra REAL NOT NULL,
                    porcentaje_ganancia REAL NOT NULL,
                    precio_venta REAL NOT NULL,
                    stock_actual INTEGER DEFAULT 0,
                    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Agregar columna categoria si no existe (para bases de datos existentes)
            try:
                cursor.execute('ALTER TABLE productos ADD COLUMN categoria TEXT')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            # Agregar columna monto_ganancia si no existe
            try:
                cursor.execute('ALTER TABLE productos ADD COLUMN monto_ganancia REAL DEFAULT 0')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            # Agregar columnas para datos del SKU (marca, color, tamaño)
            try:
                cursor.execute('ALTER TABLE productos ADD COLUMN marca TEXT')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            try:
                cursor.execute('ALTER TABLE productos ADD COLUMN color TEXT')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            try:
                cursor.execute('ALTER TABLE productos ADD COLUMN tamaño TEXT')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            # Agregar columnas adicionales del generador SKU (dibujo, cod_color)
            try:
                cursor.execute('ALTER TABLE productos ADD COLUMN dibujo TEXT')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            try:
                cursor.execute('ALTER TABLE productos ADD COLUMN cod_color TEXT')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            # Tabla de compras
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS compras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER,
                    proveedor_id INTEGER,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL NOT NULL,
                    total REAL NOT NULL,
                    no_documento TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    FOREIGN KEY (producto_id) REFERENCES productos (id),
                    FOREIGN KEY (proveedor_id) REFERENCES proveedores (id)
                )
            ''')
            
            # Tabla de ventas (encabezado) - NUEVA ESTRUCTURA
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referencia_no TEXT NOT NULL UNIQUE,
                    cliente_id INTEGER,
                    fecha TEXT NOT NULL,
                    total REAL NOT NULL,
                    estado TEXT DEFAULT 'Emitido',
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                )
            ''')
            
            # Tabla de detalle de ventas (productos individuales) - NUEVA
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ventas_detalle (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venta_id INTEGER NOT NULL,
                    producto_id INTEGER,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (venta_id) REFERENCES ventas (id) ON DELETE CASCADE,
                    FOREIGN KEY (producto_id) REFERENCES productos (id)
                )
            ''')
            
            # Tabla de movimientos de stock
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movimientos_stock (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER,
                    tipo TEXT NOT NULL, -- 'entrada' o 'salida'
                    cantidad INTEGER NOT NULL,
                    motivo TEXT NOT NULL, -- 'compra', 'venta', 'ajuste'
                    fecha TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (producto_id) REFERENCES productos (id)
                )
            ''')
            
            # Tabla de movimientos de caja
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movimientos_caja (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL, -- 'INGRESO' o 'EGRESO'
                    categoria TEXT NOT NULL, -- 'VENTA', 'COMPRA', 'RETIRO_UTILIDAD', 'GASTO_OPERATIVO', 'APORTE_CAPITAL'
                    concepto TEXT NOT NULL,
                    monto REAL NOT NULL,
                    saldo_anterior REAL NOT NULL,
                    saldo_nuevo REAL NOT NULL,
                    fecha TEXT NOT NULL,
                    usuario TEXT DEFAULT 'Sistema'
                )
            ''')
            
            # Agregar columnas de vencimiento a compras si no existen
            try:
                cursor.execute('ALTER TABLE compras ADD COLUMN es_perecedero INTEGER DEFAULT 0')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            try:
                cursor.execute('ALTER TABLE compras ADD COLUMN fecha_vencimiento TEXT')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            # Agregar columna activo a productos si no existe (para productos descontinuados)
            try:
                cursor.execute('ALTER TABLE productos ADD COLUMN activo INTEGER DEFAULT 1')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            # Agregar columna cantidad_disponible para método PEPS
            try:
                cursor.execute('ALTER TABLE compras ADD COLUMN cantidad_disponible INTEGER')
                # Inicializar cantidad_disponible = cantidad para compras existentes
                cursor.execute('UPDATE compras SET cantidad_disponible = cantidad WHERE cantidad_disponible IS NULL')
            except sqlite3.OperationalError:
                pass  # La columna ya existe
            
            # MIGRACIÓN: Verificar si hay datos en la tabla ventas antigua
            # Si existe la columna producto_id en ventas, significa que es la estructura antigua
            try:
                cursor.execute("SELECT producto_id FROM ventas LIMIT 1")
                # Si llega aquí, la tabla tiene estructura antigua - necesita migración
                # Verificar si hay datos
                cursor.execute("SELECT COUNT(*) FROM ventas")
                count = cursor.fetchone()[0]
                
                if count > 0:
                    # Hay datos, hacer migración completa
                    self._migrar_ventas_a_nueva_estructura(cursor)
                else:
                    # No hay datos, solo actualizar estructura
                    print("Actualizando estructura de tabla ventas (sin datos)...")
                    cursor.execute("DROP TABLE ventas")
                    cursor.execute('''
                        CREATE TABLE ventas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            referencia_no TEXT NOT NULL UNIQUE,
                            cliente_id INTEGER,
                            fecha TEXT NOT NULL,
                            total REAL NOT NULL,
                            estado TEXT DEFAULT 'Emitido',
                            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                        )
                    ''')
            except sqlite3.OperationalError:
                # La columna producto_id no existe, es la nueva estructura
                # Verificar si falta la columna estado
                try:
                    cursor.execute("SELECT estado FROM ventas LIMIT 1")
                except sqlite3.OperationalError:
                    # Falta columna estado, agregarla
                    try:
                        cursor.execute("ALTER TABLE ventas ADD COLUMN estado TEXT DEFAULT 'Emitido'")
                        print("Columna 'estado' agregada a la tabla ventas")
                    except sqlite3.OperationalError:
                        pass  # Ya existe
            
            conn.commit()
    
    def _migrar_ventas_a_nueva_estructura(self, cursor):
        """Migra ventas de la estructura antigua (un producto por venta) a la nueva (encabezado + detalle)"""
        try:
            # Verificar si ya existe la tabla ventas_detalle
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ventas_detalle'")
            if not cursor.fetchone():
                return  # No hay tabla detalle, no migrar aún
            
            # Verificar si hay datos para migrar
            cursor.execute("SELECT COUNT(*) as count FROM ventas")
            count_result = cursor.fetchone()
            if not count_result or count_result[0] == 0:
                return  # No hay ventas para migrar
            
            # Obtener todas las ventas antiguas agrupadas por referencia_no
            cursor.execute("""
                SELECT referencia_no, cliente_id, fecha, 
                       producto_id, cantidad, precio_unitario, total
                FROM ventas
                ORDER BY referencia_no, id
            """)
            ventas_antiguas = cursor.fetchall()
            
            if not ventas_antiguas:
                return
            
            # Renombrar tabla antigua
            cursor.execute("ALTER TABLE ventas RENAME TO ventas_old")
            
            # Crear nueva tabla ventas (encabezado)
            cursor.execute('''
                CREATE TABLE ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referencia_no TEXT NOT NULL UNIQUE,
                    cliente_id INTEGER,
                    fecha TEXT NOT NULL,
                    total REAL NOT NULL,
                    estado TEXT DEFAULT 'Emitido',
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                )
            ''')
            
            # Agrupar ventas por referencia_no
            ventas_agrupadas = {}
            for row in ventas_antiguas:
                ref_no = str(row[0])  # referencia_no como string
                if ref_no not in ventas_agrupadas:
                    ventas_agrupadas[ref_no] = {
                        'cliente_id': row[1],
                        'fecha': row[2],
                        'productos': [],
                        'total': 0
                    }
                ventas_agrupadas[ref_no]['productos'].append({
                    'producto_id': row[3],
                    'cantidad': row[4],
                    'precio_unitario': row[5],
                    'subtotal': row[6]
                })
                ventas_agrupadas[ref_no]['total'] += row[6]
            
            # Insertar en nueva estructura
            for ref_no, venta_data in ventas_agrupadas.items():
                # Insertar encabezado
                cursor.execute("""
                    INSERT INTO ventas (referencia_no, cliente_id, fecha, total, estado)
                    VALUES (?, ?, ?, ?, 'Emitido')
                """, (ref_no, venta_data['cliente_id'], venta_data['fecha'], venta_data['total']))
                
                venta_id = cursor.lastrowid
                
                # Insertar detalles
                for producto in venta_data['productos']:
                    cursor.execute("""
                        INSERT INTO ventas_detalle (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                        VALUES (?, ?, ?, ?, ?)
                    """, (venta_id, producto['producto_id'], producto['cantidad'], 
                          producto['precio_unitario'], producto['subtotal']))
            
            # Opcional: Eliminar tabla antigua (comentar si quieres mantener backup)
            # cursor.execute("DROP TABLE ventas_old")
            
            print(f"✅ Migración completada: {len(ventas_agrupadas)} ventas migradas a nueva estructura")
            
        except Exception as e:
            print(f"⚠️ Error en migración de ventas: {e}")
            # No hacer rollback, solo reportar el error
    
    # MÉTODOS PARA PROVEEDORES
    def crear_proveedor(self, nombre: str, nit_dpi: str, direccion: str, telefono: str = "") -> int:
        """Crea un nuevo proveedor"""
        query = '''
            INSERT INTO proveedores (nombre, nit_dpi, direccion, telefono)
            VALUES (?, ?, ?, ?)
        '''
        return self.execute_insert(query, (nombre, nit_dpi, direccion, telefono))
    
    def obtener_proveedores(self) -> List[Dict]:
        """Obtiene todos los proveedores"""
        query = 'SELECT * FROM proveedores ORDER BY nombre'
        return self.execute_query(query)
    
    def obtener_proveedor_por_id(self, proveedor_id: int) -> Optional[Dict]:
        """Obtiene un proveedor por su ID"""
        query = 'SELECT * FROM proveedores WHERE id = ?'
        resultado = self.execute_query(query, (proveedor_id,))
        return resultado[0] if resultado else None
    
    def buscar_proveedor(self, busqueda: str) -> List[Dict]:
        """Busca proveedores por nombre o NIT"""
        query = '''
            SELECT * FROM proveedores 
            WHERE nombre LIKE ? OR nit_dpi LIKE ?
            ORDER BY nombre
        '''
        patron = f'%{busqueda}%'
        return self.execute_query(query, (patron, patron))
    
    def actualizar_proveedor(self, proveedor_id: int, nombre: str, nit_dpi: str, direccion: str, telefono: str = ""):
        """Actualiza un proveedor"""
        query = '''
            UPDATE proveedores 
            SET nombre = ?, nit_dpi = ?, direccion = ?, telefono = ?
            WHERE id = ?
        '''
        return self.execute_update(query, (nombre, nit_dpi, direccion, telefono, proveedor_id))
    
    # MÉTODOS PARA CLIENTES
    def crear_cliente(self, nombre: str, nit_dpi: str, direccion: str, telefono: str = "") -> int:
        """Crea un nuevo cliente"""
        query = '''
            INSERT INTO clientes (nombre, nit_dpi, direccion, telefono)
            VALUES (?, ?, ?, ?)
        '''
        return self.execute_insert(query, (nombre, nit_dpi, direccion, telefono))
    
    def obtener_clientes(self) -> List[Dict]:
        """Obtiene todos los clientes"""
        query = 'SELECT * FROM clientes ORDER BY nombre'
        return self.execute_query(query)
    
    def obtener_cliente_por_id(self, cliente_id: int) -> Optional[Dict]:
        """Obtiene un cliente por su ID"""
        query = 'SELECT * FROM clientes WHERE id = ?'
        resultado = self.execute_query(query, (cliente_id,))
        return resultado[0] if resultado else None
    
    def buscar_cliente(self, busqueda: str) -> List[Dict]:
        """Busca clientes por nombre o NIT"""
        query = '''
            SELECT * FROM clientes 
            WHERE nombre LIKE ? OR nit_dpi LIKE ?
            ORDER BY nombre
        '''
        patron = f'%{busqueda}%'
        return self.execute_query(query, (patron, patron))
    
    def actualizar_cliente(self, cliente_id: int, nombre: str, nit_dpi: str, direccion: str, telefono: str = ""):
        """Actualiza un cliente"""
        query = '''
            UPDATE clientes 
            SET nombre = ?, nit_dpi = ?, direccion = ?, telefono = ?
            WHERE id = ?
        '''
        return self.execute_update(query, (nombre, nit_dpi, direccion, telefono, cliente_id))
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Ejecuta una consulta SELECT y devuelve los resultados"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Ejecuta una consulta INSERT y devuelve el ID del registro insertado"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Ejecuta una consulta UPDATE y devuelve el número de filas afectadas"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    # MÉTODOS PARA PRODUCTOS
    def crear_producto(self, codigo: str, nombre: str, categoria: str, precio_compra: float, porcentaje_ganancia: float, marca: str = '', color: str = '', tamaño: str = '', dibujo: str = '', cod_color: str = '') -> int:
        """Crea un nuevo producto con datos adicionales del SKU completo"""
        precio_venta = round(precio_compra * (1 + porcentaje_ganancia / 100), 2)
        monto_ganancia = round(precio_venta - precio_compra, 2)
        query = '''
            INSERT INTO productos (codigo, nombre, categoria, precio_compra, porcentaje_ganancia, precio_venta, monto_ganancia, marca, color, tamaño, dibujo, cod_color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_insert(query, (codigo, nombre, categoria, precio_compra, porcentaje_ganancia, precio_venta, monto_ganancia, marca, color, tamaño, dibujo, cod_color))
    
    def obtener_productos(self) -> List[Dict]:
        """Obtiene todos los productos ordenados por ID ascendente"""
        query = 'SELECT * FROM productos ORDER BY id ASC'
        return self.execute_query(query)

    def eliminar_producto(self, producto_id: int) -> bool:
        """Elimina un producto por su ID (mantiene historial de compras/ventas)"""
        try:
            # Solo eliminar movimientos de stock y el producto
            # Las compras y ventas se mantienen para historial
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM movimientos_stock WHERE producto_id = ?', (producto_id,))
                cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False
    
    def obtener_producto_por_id(self, producto_id: int) -> Optional[Dict]:
        """Obtiene un producto por su ID"""
        query = 'SELECT * FROM productos WHERE id = ?'
        resultado = self.execute_query(query, (producto_id,))
        return resultado[0] if resultado else None
    
    def actualizar_producto(self, producto_id: int, codigo: str, nombre: str, categoria: str, precio_compra: float, porcentaje_ganancia: float, marca: str = '', color: str = '', tamaño: str = '', dibujo: str = '', cod_color: str = ''):
        """Actualiza un producto con datos adicionales del SKU completo"""
        precio_venta = round(precio_compra * (1 + porcentaje_ganancia / 100), 2)
        monto_ganancia = round(precio_venta - precio_compra, 2)
        query = '''
            UPDATE productos 
            SET codigo = ?, nombre = ?, categoria = ?, precio_compra = ?, porcentaje_ganancia = ?, precio_venta = ?, monto_ganancia = ?, marca = ?, color = ?, tamaño = ?, dibujo = ?, cod_color = ?
            WHERE id = ?
        '''
        return self.execute_update(query, (codigo, nombre, categoria, precio_compra, porcentaje_ganancia, precio_venta, monto_ganancia, marca, color, tamaño, dibujo, cod_color, producto_id))
    
    def actualizar_stock(self, producto_id: int, nuevo_stock: int):
        """Actualiza el stock de un producto"""
        query = 'UPDATE productos SET stock_actual = ? WHERE id = ?'
        return self.execute_update(query, (nuevo_stock, producto_id))
    
    def cambiar_estado_producto(self, producto_id: int, activo: bool) -> bool:
        """Cambia el estado activo/inactivo de un producto"""
        query = 'UPDATE productos SET activo = ? WHERE id = ?'
        return self.execute_update(query, (1 if activo else 0, producto_id))
    
    def obtener_productos_activos(self) -> List[Dict]:
        """Obtiene solo los productos activos"""
        query = 'SELECT * FROM productos WHERE activo = 1 ORDER BY nombre'
        return self.execute_query(query)
    
    def obtener_productos_inactivos(self) -> List[Dict]:
        """Obtiene solo los productos inactivos"""
        query = 'SELECT * FROM productos WHERE activo = 0 ORDER BY nombre'
        return self.execute_query(query)
    
    # MÉTODOS PARA COMPRAS
    def registrar_compra(self, producto_id: int, cantidad: int, precio_unitario: float,
                         proveedor_id: int, no_documento: str, fecha_manual: str,
                         es_perecedero: bool = False, fecha_vencimiento: str = None) -> int:
        """
        Registra una compra y actualiza el stock
        fecha_manual debe estar en formato 'dd/mm/yyyy HH:MM:SS' o 'dd/mm/yyyy'
        es_perecedero: True si el producto tiene fecha de vencimiento
        fecha_vencimiento: Fecha en formato 'dd/mm/yyyy' (solo si es_perecedero=True)
        """
        total = round(cantidad * precio_unitario, 2)
        
        # Insertar compra
        query_compra = '''
            INSERT INTO compras (producto_id, cantidad, precio_unitario, total, fecha, proveedor_id, no_documento,
                               es_perecedero, fecha_vencimiento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        compra_id = self.execute_insert(query_compra, (producto_id, cantidad, precio_unitario, total, 
                                                       fecha_manual, proveedor_id, no_documento,
                                                       1 if es_perecedero else 0, fecha_vencimiento))
        
        # Actualizar stock
        producto = self.obtener_producto_por_id(producto_id)
        if producto:
            nuevo_stock = producto['stock_actual'] + cantidad
            self.actualizar_stock(producto_id, nuevo_stock)
            
            # Registrar movimiento de stock
            self.registrar_movimiento_stock(producto_id, 'entrada', cantidad, 'compra')
            
            # NOTA: El movimiento de caja se registra ahora en inventario_controller.py
            # para tener un control centralizado de los movimientos de caja
        
        return compra_id
    
    def obtener_compras(self) -> List[Dict]:
        """Obtiene todas las compras con información del producto y proveedor"""
        query = '''
            SELECT c.*, 
                   COALESCE(p.nombre, '[Producto Eliminado - ID: ' || c.producto_id || ']') as producto_nombre,
                   COALESCE(pr.nombre, '[Proveedor Eliminado]') as proveedor_nombre,
                   COALESCE(pr.nit_dpi, '') as proveedor_nit,
                   COALESCE(c.es_perecedero, 0) as es_perecedero,
                   c.fecha_vencimiento
            FROM compras c
            LEFT JOIN productos p ON c.producto_id = p.id
            LEFT JOIN proveedores pr ON c.proveedor_id = pr.id
            ORDER BY c.id ASC
        '''
        return self.execute_query(query)
    
    def obtener_productos_proximos_vencer(self, dias_limite: int = 30) -> List[Dict]:
        """
        Obtiene productos perecederos próximos a vencer (solo productos activos)
        Considera solo la cantidad disponible según PEPS
        dias_limite: Número de días para considerar como 'próximo a vencer'
        """
        query = '''
            SELECT c.*, 
                   p.nombre as producto_nombre,
                   pr.nombre as proveedor_nombre,
                   COALESCE(c.cantidad_disponible, c.cantidad) as disponible
            FROM compras c
            INNER JOIN productos p ON c.producto_id = p.id
            LEFT JOIN proveedores pr ON c.proveedor_id = pr.id
            WHERE c.es_perecedero = 1 
              AND c.fecha_vencimiento IS NOT NULL
              AND p.activo = 1
              AND COALESCE(c.cantidad_disponible, c.cantidad) > 0
        '''
        resultados = self.execute_query(query)
        
        # Calcular días restantes en Python (más confiable con formato dd/mm/yyyy)
        from datetime import datetime
        productos_filtrados = []
        
        for compra in resultados:
            try:
                fecha_venc = datetime.strptime(compra['fecha_vencimiento'], '%d/%m/%Y')
                hoy = datetime.now()
                dias_restantes = (fecha_venc - hoy).days
                
                # Incluir productos vencidos (días negativos) y próximos a vencer
                if dias_restantes <= dias_limite:
                    compra['dias_restantes'] = dias_restantes
                    productos_filtrados.append(compra)
            except:
                continue
        
        # Ordenar por días restantes (más urgente primero)
        productos_filtrados.sort(key=lambda x: x['dias_restantes'])
        return productos_filtrados
    
    def actualizar_compra_perecedero(self, compra_id: int, es_perecedero: bool, fecha_vencimiento: str = None) -> bool:
        """
        Actualiza el estado de perecedero y fecha de vencimiento de una compra
        """
        try:
            query = '''
                UPDATE compras 
                SET es_perecedero = ?, fecha_vencimiento = ?
                WHERE id = ?
            '''
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (1 if es_perecedero else 0, fecha_vencimiento, compra_id))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar compra: {e}")
            return False
    
    # MÉTODOS PARA VENTAS
    # MÉTODOS PARA VENTAS (NUEVO SISTEMA CON CARRITO)
    def registrar_venta_con_carrito(self, cliente_id: int, productos_carrito: List[Dict], fecha_manual: str) -> Tuple[bool, str]:
        """
        Registra una venta con múltiples productos (carrito de compras)
        productos_carrito: Lista de diccionarios con {producto_id, cantidad, precio_unitario}
        fecha_manual debe estar en formato 'dd/mm/yyyy HH:MM:SS' o 'dd/mm/yyyy'
        """
        if not productos_carrito:
            return False, "El carrito está vacío"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Validar stock para todos los productos antes de proceder
                for item in productos_carrito:
                    cursor.execute('SELECT nombre, stock_actual FROM productos WHERE id = ?', (item['producto_id'],))
                    producto = cursor.fetchone()
                    if not producto:
                        return False, f"Producto ID {item['producto_id']} no encontrado"
                    
                    if producto[1] < item['cantidad']:
                        return False, f"Stock insuficiente para {producto[0]}. Disponible: {producto[1]}"
                
                # Obtener el siguiente número de referencia
                cursor.execute('SELECT MAX(id) FROM ventas')
                max_id = cursor.fetchone()[0]
                siguiente_num = (max_id + 1) if max_id else 1
                referencia_no = f"REF{siguiente_num:06d}"
                
                # Calcular total general
                total_general = sum(item['cantidad'] * item['precio_unitario'] for item in productos_carrito)
                total_general = round(total_general, 2)
                
                # Insertar encabezado de venta
                cursor.execute('''
                    INSERT INTO ventas (referencia_no, cliente_id, fecha, total, estado)
                    VALUES (?, ?, ?, ?, 'Emitido')
                ''', (referencia_no, cliente_id, fecha_manual, total_general))
                
                venta_id = cursor.lastrowid
                
                # Lista para el concepto de movimiento de caja
                productos_nombres = []
                
                # Procesar cada producto del carrito
                for item in productos_carrito:
                    producto_id = item['producto_id']
                    cantidad = item['cantidad']
                    precio_unitario = item['precio_unitario']
                    subtotal = round(cantidad * precio_unitario, 2)
                    
                    # Obtener nombre del producto
                    cursor.execute('SELECT nombre, stock_actual FROM productos WHERE id = ?', (producto_id,))
                    producto_data = cursor.fetchone()
                    producto_nombre = producto_data[0]
                    stock_actual = producto_data[1]
                    
                    # Insertar detalle de venta
                    cursor.execute('''
                        INSERT INTO ventas_detalle (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (venta_id, producto_id, cantidad, precio_unitario, subtotal))
                    
                    # Aplicar PEPS para descontar de compras más antiguas (dentro del mismo cursor)
                    cursor.execute('''
                        SELECT id, cantidad, COALESCE(cantidad_disponible, cantidad) as disponible
                        FROM compras 
                        WHERE producto_id = ? AND COALESCE(cantidad_disponible, cantidad) > 0
                        ORDER BY fecha ASC
                    ''', (producto_id,))
                    compras = cursor.fetchall()
                    
                    cantidad_restante = cantidad
                    for compra in compras:
                        if cantidad_restante <= 0:
                            break
                        
                        compra_id, cantidad_compra, disponible = compra
                        
                        if disponible >= cantidad_restante:
                            nueva_disponible = disponible - cantidad_restante
                            cursor.execute('UPDATE compras SET cantidad_disponible = ? WHERE id = ?',
                                         (nueva_disponible, compra_id))
                            cantidad_restante = 0
                        else:
                            cursor.execute('UPDATE compras SET cantidad_disponible = 0 WHERE id = ?',
                                         (compra_id,))
                            cantidad_restante -= disponible
                    
                    # Actualizar stock total del producto
                    nuevo_stock = stock_actual - cantidad
                    cursor.execute('UPDATE productos SET stock_actual = ? WHERE id = ?', (nuevo_stock, producto_id))
                    print(f"DEBUG: Producto {producto_nombre} - Stock anterior: {stock_actual}, Vendido: {cantidad}, Nuevo stock: {nuevo_stock}")
                    
                    # Registrar movimiento de stock
                    cursor.execute('''
                        INSERT INTO movimientos_stock (producto_id, tipo, cantidad, motivo)
                        VALUES (?, 'salida', ?, 'venta')
                    ''', (producto_id, cantidad))
                    
                    # Agregar nombre para el concepto
                    productos_nombres.append(producto_nombre)
                
                # NOTA: El movimiento de caja se registra ahora en inventario_controller.py
                # para tener un control centralizado de los movimientos de caja
                
                conn.commit()
                
                return True, f"✅ Venta registrada exitosamente\n\n📋 Referencia: {referencia_no}\n🆔 ID: {venta_id}\n🛒 Productos: {len(productos_carrito)}\n💰 Total: Q {total_general:,.2f}"
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False, f"Error al registrar venta: {str(e)}"
    
    # Método antiguo mantenido para compatibilidad (llama al nuevo método)
    def registrar_venta(self, producto_id: int, cantidad: int, precio_unitario: float,
                       cliente_id: int, fecha_manual: str) -> Tuple[bool, str]:
        """
        MÉTODO LEGACY: Registra una venta de un solo producto
        Internamente usa el nuevo sistema de carrito con un solo item
        """
        carrito = [{
            'producto_id': producto_id,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario
        }]
        return self.registrar_venta_con_carrito(cliente_id, carrito, fecha_manual)
    
    def aplicar_peps(self, producto_id: int, cantidad_vendida: int):
        """
        Aplica el método PEPS (Primeras Entradas, Primeras Salidas)
        Descuenta la cantidad vendida de las compras más antiguas primero
        """
        # Obtener compras del producto ordenadas por fecha (más antiguas primero)
        # Solo compras con cantidad disponible > 0
        query = '''
            SELECT id, cantidad, COALESCE(cantidad_disponible, cantidad) as disponible
            FROM compras 
            WHERE producto_id = ? AND COALESCE(cantidad_disponible, cantidad) > 0
            ORDER BY fecha ASC
        '''
        compras = self.execute_query(query, (producto_id,))
        
        cantidad_restante = cantidad_vendida
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Descontar de las compras más antiguas
            for compra in compras:
                if cantidad_restante <= 0:
                    break
                
                disponible = compra['disponible']
                
                if disponible >= cantidad_restante:
                    # Esta compra tiene suficiente para cubrir lo restante
                    nueva_disponible = disponible - cantidad_restante
                    cursor.execute(
                        'UPDATE compras SET cantidad_disponible = ? WHERE id = ?',
                        (nueva_disponible, compra['id'])
                    )
                    cantidad_restante = 0
                else:
                    # Esta compra se agota completamente
                    cursor.execute(
                        'UPDATE compras SET cantidad_disponible = 0 WHERE id = ?',
                        (compra['id'],)
                    )
                    cantidad_restante -= disponible
            
            conn.commit()
    
    def obtener_siguiente_referencia(self) -> str:
        """Genera el siguiente número de referencia para ventas"""
        query = '''
            SELECT MAX(CAST(SUBSTR(referencia_no, 4) AS INTEGER)) as max_num
            FROM ventas 
            WHERE referencia_no LIKE 'REF%'
        '''
        resultado = self.execute_query(query)
        
        if resultado and resultado[0].get('max_num'):
            ultimo_num = resultado[0]['max_num']
            siguiente_num = ultimo_num + 1
        else:
            siguiente_num = 1
        
        return f"REF{siguiente_num:06d}"  # REF000001, REF000002, etc.
    
    def obtener_ventas(self) -> List[Dict]:
        """Obtiene todas las ventas con información del cliente y detalles de productos"""
        query = '''
            SELECT v.id, v.referencia_no, v.cliente_id, v.fecha, v.total, v.estado,
                   COALESCE(c.nombre, '[Cliente Eliminado]') as cliente_nombre,
                   COALESCE(c.nit_dpi, '') as cliente_nit
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            ORDER BY v.id DESC
        '''
        ventas = self.execute_query(query)
        
        # Obtener detalles de cada venta
        for venta in ventas:
            query_detalle = '''
                SELECT vd.*, 
                       COALESCE(p.nombre, '[Producto Eliminado]') as producto_nombre,
                       COALESCE(p.codigo, '') as producto_codigo
                FROM ventas_detalle vd
                LEFT JOIN productos p ON vd.producto_id = p.id
                WHERE vd.venta_id = ?
                ORDER BY vd.id
            '''
            detalles = self.execute_query(query_detalle, (venta['id'],))
            venta['detalles'] = detalles
            
            # Agregar conteo de productos
            venta['cantidad_productos'] = len(detalles)
            
        return ventas
    
    def obtener_venta_por_id(self, venta_id: int) -> Optional[Dict]:
        """Obtiene una venta específica con todos sus detalles"""
        query = '''
            SELECT v.*, 
                   COALESCE(c.nombre, '[Cliente Eliminado]') as cliente_nombre,
                   COALESCE(c.nit_dpi, '') as cliente_nit,
                   COALESCE(c.direccion, '') as cliente_direccion,
                   COALESCE(c.telefono, '') as cliente_telefono
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE v.id = ?
        '''
        resultado = self.execute_query(query, (venta_id,))
        
        if not resultado:
            return None
        
        venta = resultado[0]
        
        # Obtener detalles
        query_detalle = '''
            SELECT vd.*, 
                   COALESCE(p.nombre, '[Producto Eliminado]') as producto_nombre,
                   COALESCE(p.codigo, '') as producto_codigo
            FROM ventas_detalle vd
            LEFT JOIN productos p ON vd.producto_id = p.id
            WHERE vd.venta_id = ?
        '''
        venta['detalles'] = self.execute_query(query_detalle, (venta_id,))
        
        return venta
    
    def anular_venta(self, venta_id: int) -> tuple:
        """
        Anula una venta:
        1. Cambia el estado a 'Anulado'
        2. Devuelve los productos al inventario
        3. Registra movimientos de stock
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar que la venta existe y no está anulada
            cursor.execute('SELECT estado FROM ventas WHERE id = ?', (venta_id,))
            resultado = cursor.fetchone()
            
            if not resultado:
                return False, "Venta no encontrada"
            
            if resultado[0] == 'Anulado':
                return False, "La venta ya está anulada"
            
            # Obtener detalles de la venta para devolver productos
            cursor.execute('''
                SELECT producto_id, cantidad 
                FROM ventas_detalle 
                WHERE venta_id = ?
            ''', (venta_id,))
            
            detalles = cursor.fetchall()
            
            # Devolver productos al inventario
            for producto_id, cantidad in detalles:
                # Aumentar stock
                cursor.execute('''
                    UPDATE productos 
                    SET stock_actual = stock_actual + ? 
                    WHERE id = ?
                ''', (cantidad, producto_id))
                
                # Registrar movimiento de stock
                cursor.execute('''
                    INSERT INTO movimientos_stock (producto_id, tipo, cantidad, motivo, fecha)
                    VALUES (?, 'entrada', ?, 'Devolución por anulación de venta', datetime('now', 'localtime'))
                ''', (producto_id, cantidad))
            
            # Cambiar estado de la venta a Anulado
            cursor.execute('''
                UPDATE ventas 
                SET estado = 'Anulado'
                WHERE id = ?
            ''', (venta_id,))
            
            conn.commit()
            return True, f"Venta anulada exitosamente. {len(detalles)} productos devueltos al inventario."
            
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            return False, f"Error al anular venta: {str(e)}"
        finally:
            if conn:
                conn.close()
    
    # MÉTODOS PARA MOVIMIENTOS DE STOCK
    def registrar_movimiento_stock(self, producto_id: int, tipo: str, cantidad: int, motivo: str):
        """Registra un movimiento de stock"""
        query = '''
            INSERT INTO movimientos_stock (producto_id, tipo, cantidad, motivo)
            VALUES (?, ?, ?, ?)
        '''
        return self.execute_insert(query, (producto_id, tipo, cantidad, motivo))
    
    def obtener_movimientos_stock(self, producto_id: int = None) -> List[Dict]:
        """Obtiene los movimientos de stock"""
        if producto_id:
            query = '''
                SELECT m.*, p.nombre as producto_nombre
                FROM movimientos_stock m
                JOIN productos p ON m.producto_id = p.id
                WHERE m.producto_id = ?
                ORDER BY m.fecha DESC
            '''
            return self.execute_query(query, (producto_id,))
        else:
            query = '''
                SELECT m.*, p.nombre as producto_nombre
                FROM movimientos_stock m
                JOIN productos p ON m.producto_id = p.id
                ORDER BY m.fecha DESC
            '''
            return self.execute_query(query)
    
    # MÉTODOS PARA REPORTES
    def obtener_total_compras(self) -> float:
        """Obtiene el total de todas las compras"""
        query = 'SELECT COALESCE(SUM(total), 0) as total FROM compras'
        resultado = self.execute_query(query)
        return resultado[0]['total'] if resultado else 0
    
    def obtener_total_ventas(self) -> float:
        """Obtiene el total de todas las ventas activas (no anuladas)"""
        query = "SELECT COALESCE(SUM(total), 0) as total FROM ventas WHERE estado != 'Anulado'"
        resultado = self.execute_query(query)
        return resultado[0]['total'] if resultado else 0
    
    def obtener_resumen_inventario(self) -> Dict:
        """Obtiene un resumen completo del inventario"""
        total_compras = self.obtener_total_compras()
        total_ventas = self.obtener_total_ventas()
        
        # GANANCIA BRUTA REAL: Suma de (precio_venta - precio_compra) * cantidad vendida
        # Solo considerar ventas no anuladas
        query_ganancia = '''
            SELECT COALESCE(SUM((vd.precio_unitario - p.precio_compra) * vd.cantidad), 0) as ganancia_bruta
            FROM ventas_detalle vd
            INNER JOIN ventas v ON vd.venta_id = v.id
            INNER JOIN productos p ON vd.producto_id = p.id
            WHERE v.estado != 'Anulado'
        '''
        resultado_ganancia = self.execute_query(query_ganancia)
        ganancia_bruta = resultado_ganancia[0]['ganancia_bruta'] if resultado_ganancia else 0
        
        # Valor actual del inventario (stock * precio_compra)
        query_inventario = '''
            SELECT COALESCE(SUM(p.stock_actual * p.precio_compra), 0) as valor_inventario
            FROM productos p
        '''
        resultado = self.execute_query(query_inventario)
        valor_inventario = resultado[0]['valor_inventario'] if resultado else 0
        
        # Saldo en banco = Saldo actual de caja (ingresos - egresos reales)
        saldo_banco = self.obtener_saldo_caja()
        
        return {
            'total_compras': total_compras,
            'total_ventas': total_ventas,
            'ganancia_bruta': ganancia_bruta,
            'valor_inventario': valor_inventario,
            'saldo_banco': saldo_banco
        }
    
    # MÉTODOS PARA MOVIMIENTOS DE CAJA
    def obtener_saldo_caja(self) -> float:
        """Obtiene el saldo actual de caja"""
        query = '''
            SELECT saldo_nuevo FROM movimientos_caja 
            ORDER BY id DESC LIMIT 1
        '''
        resultado = self.execute_query(query)
        return resultado[0]['saldo_nuevo'] if resultado else 0.0
    
    def registrar_movimiento_caja(self, tipo: str, categoria: str, concepto: str, 
                                   monto: float, fecha: str, usuario: str = 'Sistema') -> int:
        """Registra un movimiento de caja"""
        saldo_anterior = self.obtener_saldo_caja()
        
        if tipo == 'INGRESO':
            saldo_nuevo = saldo_anterior + monto
        else:  # EGRESO
            saldo_nuevo = saldo_anterior - monto
        
        query = '''
            INSERT INTO movimientos_caja 
            (tipo, categoria, concepto, monto, saldo_anterior, saldo_nuevo, fecha, usuario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_insert(query, (tipo, categoria, concepto, monto, 
                                           saldo_anterior, saldo_nuevo, fecha, usuario))
    
    def obtener_movimientos_caja(self, fecha_inicio: str = None, fecha_fin: str = None) -> List[Dict]:
        """Obtiene los movimientos de caja, opcionalmente filtrados por rango de fechas"""
        if fecha_inicio and fecha_fin:
            # Las fechas vienen en formato yyyy-mm-dd desde el filtro
            # La fecha en BD está en formato dd/mm/yyyy HH:MM:SS
            # Necesitamos convertir para comparar correctamente
            query = '''
                SELECT * FROM movimientos_caja 
                WHERE date(substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)) 
                BETWEEN date(?) AND date(?)
                ORDER BY id DESC
            '''
            return self.execute_query(query, (fecha_inicio, fecha_fin))
        else:
            query = 'SELECT * FROM movimientos_caja ORDER BY id DESC LIMIT 100'
            return self.execute_query(query)
    
    def obtener_resumen_caja(self, fecha_inicio: str = None, fecha_fin: str = None) -> Dict:
        """Obtiene un resumen de los movimientos de caja"""
        if fecha_inicio and fecha_fin:
            # Las fechas vienen en formato yyyy-mm-dd desde el filtro
            # La fecha en BD está en formato dd/mm/yyyy HH:MM:SS
            query_ingresos = '''
                SELECT COALESCE(SUM(monto), 0) as total 
                FROM movimientos_caja 
                WHERE tipo = 'INGRESO' 
                AND date(substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)) 
                BETWEEN date(?) AND date(?)
            '''
            query_egresos = '''
                SELECT COALESCE(SUM(monto), 0) as total 
                FROM movimientos_caja 
                WHERE tipo = 'EGRESO'
                AND date(substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)) 
                BETWEEN date(?) AND date(?)
            '''
            ingresos = self.execute_query(query_ingresos, (fecha_inicio, fecha_fin))
            egresos = self.execute_query(query_egresos, (fecha_inicio, fecha_fin))
        else:
            query_ingresos = '''
                SELECT COALESCE(SUM(monto), 0) as total 
                FROM movimientos_caja 
                WHERE tipo = 'INGRESO'
            '''
            query_egresos = '''
                SELECT COALESCE(SUM(monto), 0) as total 
                FROM movimientos_caja 
                WHERE tipo = 'EGRESO'
            '''
            ingresos = self.execute_query(query_ingresos)
            egresos = self.execute_query(query_egresos)
        
        total_ingresos = ingresos[0]['total'] if ingresos else 0
        total_egresos = egresos[0]['total'] if egresos else 0
        saldo_actual = self.obtener_saldo_caja()
        
        return {
            'total_ingresos': total_ingresos,
            'total_egresos': total_egresos,
            'saldo_actual': saldo_actual,
            'diferencia': total_ingresos - total_egresos
        }
    
    def eliminar_movimiento_caja(self, movimiento_id: int) -> bool:
        """Elimina un movimiento de caja por su ID"""
        query = 'DELETE FROM movimientos_caja WHERE id = ?'
        return self.execute_update(query, (movimiento_id,))
    
    def cambiar_base_datos(self, nueva_ruta: str) -> bool:
        """Cambia la ruta de la base de datos"""
        try:
            if os.path.exists(nueva_ruta):
                self.db_path = nueva_ruta
                return True
            else:
                # Si no existe, crear nueva base de datos
                self.db_path = nueva_ruta
                self.init_database()
                return True
        except Exception as e:
            print(f"Error al cambiar base de datos: {e}")
            return False
