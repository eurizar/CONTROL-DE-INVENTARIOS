# Cómo Generar el Ejecutable

Este documento explica cómo generar el archivo ejecutable `.exe` del Sistema de Control de Inventarios.

## ⚠️ Nota Importante

El ejecutable **NO está incluido en el repositorio** debido a su tamaño (~70 MB). 

Si descargaste este proyecto desde GitHub, debes generar el ejecutable siguiendo estas instrucciones.

---

## 📋 Requisitos

- Python 3.7 o superior instalado
- Todas las dependencias instaladas (ver abajo)
- PyInstaller instalado

---

## 🚀 Pasos para Generar el Ejecutable

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TU-USUARIO/sistema-inventarios.git
cd sistema-inventarios
```

### 2. Crear Entorno Virtual (Recomendado)

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar PyInstaller

```bash
pip install pyinstaller
```

### 5. Generar el Ejecutable

**Windows:**
```bash
pyinstaller --name="Sistema_Inventarios" --onedir --windowed --icon=inventario.ico --add-data "inventario.ico;." main.py
```

**Linux/Mac:**
```bash
pyinstaller --name="Sistema_Inventarios" --onedir --windowed --icon=inventario.ico --add-data "inventario.ico:." main.py
```

### 6. Ubicación del Ejecutable

El ejecutable se generará en:
```
dist/Sistema_Inventarios/Sistema_Inventarios.exe
```

---

## 📦 Contenido Generado

Después de la compilación, tendrás:

```
dist/
└── Sistema_Inventarios/
    ├── Sistema_Inventarios.exe    (Ejecutable principal)
    ├── _internal/                  (Dependencias - NO ELIMINAR)
    └── [otros archivos]
```

---

## 🎯 Uso Rápido con Scripts Incluidos

### Windows

1. **Instalar todo automáticamente:**
   ```bash
   install.bat
   ```

2. **Ejecutar el programa (sin compilar):**
   ```bash
   run.bat
   ```

---

## 💡 Distribución

Para distribuir el programa:

1. Comprime **toda** la carpeta `dist/Sistema_Inventarios/`
2. Incluye: `.exe` + carpeta `_internal/`
3. Envía el archivo .ZIP
4. El usuario solo descomprime y ejecuta

---

## 🐛 Problemas Comunes

### Error: "No module named 'ttkbootstrap'"
```bash
pip install ttkbootstrap
```

### Error: "pyinstaller: command not found"
```bash
pip install pyinstaller
```

### El ejecutable no abre
- Verifica que Windows Defender no lo bloqueó
- Asegúrate de incluir la carpeta `_internal/`

---

## 📧 Soporte

Para problemas o dudas:
- **Email:** elizandrou@outlook.com
- **Autor:** Elizandro Urizar

---

## 📜 Licencia

© 2025 Elizandro Urizar. Todos los derechos reservados.

Ver `LICENSE.txt` para más información sobre uso comercial.
