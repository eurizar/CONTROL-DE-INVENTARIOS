# 🔐 Credenciales de Login

## Sistema de Control de Inventarios v2.0

### Usuario por Defecto

Al iniciar la aplicación por primera vez, se crea automáticamente un usuario administrador:

- **Usuario:** `Marteliz`
- **Contraseña:** `Admin`
- **Rol:** Administrador

### Iniciar Sesión

1. Ejecuta la aplicación con `python main.py` o el ejecutable
2. Se abrirá la ventana de login
3. Ingresa las credenciales:
   - Usuario: **Marteliz**
   - Contraseña: **Admin**
4. Presiona "INGRESAR" o presiona Enter
5. Si las credenciales son correctas, se abrirá la aplicación principal

### Características del Login

✅ **Autenticación segura** - Verificación de usuario y contraseña en base de datos
✅ **Mostrar/Ocultar contraseña** - Checkbox para visualizar la contraseña
✅ **Registro de accesos** - Se guarda la fecha y hora del último acceso
✅ **Usuario en título** - El nombre del usuario aparece en el título de la ventana principal
✅ **Interfaz moderna** - Diseño limpio y profesional con ttkbootstrap

### Gestión de Usuarios

Los usuarios se almacenan en la tabla `usuarios` de la base de datos `data/inventarios.db`

#### Campos de Usuario:
- `id` - Identificador único
- `usuario` - Nombre de usuario (único)
- `contrasena` - Contraseña (texto plano por ahora)
- `nombre_completo` - Nombre completo del usuario
- `rol` - Rol del usuario (admin, usuario, etc.)
- `activo` - Estado del usuario (1=activo, 0=inactivo)
- `fecha_creacion` - Fecha de creación de la cuenta
- `ultimo_acceso` - Última fecha y hora de inicio de sesión

### Agregar Nuevos Usuarios

Para agregar usuarios adicionales, puedes:

1. **Opción 1: Directamente en la base de datos**
   ```sql
   INSERT INTO usuarios (usuario, contrasena, nombre_completo, rol)
   VALUES ('nombre_usuario', 'contraseña', 'Nombre Completo', 'usuario');
   ```

2. **Opción 2: Usar el método del DatabaseManager**
   ```python
   from src.database.database_manager import DatabaseManager
   
   db = DatabaseManager()
   db.crear_usuario(
       usuario='nombre_usuario',
       contrasena='contraseña',
       nombre_completo='Nombre Completo',
       rol='usuario'
   )
   ```

### Seguridad

⚠️ **IMPORTANTE**: Actualmente las contraseñas se almacenan en texto plano. 
Para producción, se recomienda:
- Implementar hash de contraseñas (bcrypt, argon2, etc.)
- Agregar límite de intentos fallidos
- Implementar recuperación de contraseña
- Agregar autenticación de dos factores (2FA)

### Roles de Usuario

- **admin** - Acceso completo al sistema
- **usuario** - Acceso limitado (a implementar permisos específicos)

---

© 2025 Elizandro Urizar - elizandrou@outlook.com
