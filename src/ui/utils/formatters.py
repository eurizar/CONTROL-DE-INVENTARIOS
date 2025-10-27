"""
Funciones de formateo para datos en la UI.
"""

from datetime import datetime
from typing import Optional


def formatear_fecha(fecha_str: str) -> str:
    """
    Formatea una fecha a formato dd/mm/yyyy.
    
    Args:
        fecha_str: Fecha en formato ISO o dd/mm/yyyy
        
    Returns:
        Fecha formateada en dd/mm/yyyy
    """
    try:
        # Intentar parsear formato ISO con hora
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
        return fecha_obj.strftime('%d/%m/%Y')
    except:
        try:
            # Intentar parsear formato ISO sin hora
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
            return fecha_obj.strftime('%d/%m/%Y')
        except:
            try:
                fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y %H:%M:%S')
                return fecha_obj.strftime('%d/%m/%Y')
            except:
                # Si ya está en formato correcto o no se puede parsear
                return fecha_str.split()[0] if ' ' in fecha_str else fecha_str


def formatear_fecha_hora(fecha_str: str) -> str:
    """
    Formatea una fecha con hora a formato dd/mm/yyyy HH:MM:SS.
    
    Args:
        fecha_str: Fecha en formato ISO
        
    Returns:
        Fecha formateada en dd/mm/yyyy HH:MM:SS
    """
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
        return fecha_obj.strftime('%d/%m/%Y %H:%M:%S')
    except:
        return fecha_str


def formatear_moneda(valor: float, simbolo: str = 'Q') -> str:
    """
    Formatea un valor como moneda.
    
    Args:
        valor: Valor numérico
        simbolo: Símbolo de la moneda
        
    Returns:
        Valor formateado como moneda (ej: "Q 1,234.56")
    """
    return f"{simbolo} {valor:,.2f}"


def formatear_porcentaje(valor: float) -> str:
    """
    Formatea un valor como porcentaje.
    
    Args:
        valor: Valor numérico
        
    Returns:
        Valor formateado como porcentaje (ej: "15.5%")
    """
    return f"{valor:.1f}%"
