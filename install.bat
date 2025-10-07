@echo off
echo ========================================
echo Sistema de Control de Inventarios
echo Instalador automatico v1.0
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

echo Python detectado correctamente.
echo.

echo Creando entorno virtual...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Instalacion completada exitosamente!
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo 1. Ejecuta: run.bat
echo 2. O manualmente: .venv\Scripts\python.exe main.py
echo.

echo Creando carpeta de datos...
if not exist "data" mkdir data

echo Creando acceso directo...
echo @echo off > run.bat
echo echo Iniciando Sistema de Inventarios... >> run.bat
echo .venv\Scripts\python.exe main.py >> run.bat
echo pause >> run.bat

echo.
echo ¡Listo! Usa 'run.bat' para iniciar la aplicacion.
pause
