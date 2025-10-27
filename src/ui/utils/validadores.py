"""
Funciones de validación para datos de entrada.
"""

import re
from typing import Tuple


def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida un correo electrónico.
    
    Args:
        email: Correo a validar
        
    Returns:
        Tupla (es_valido, mensaje)
    """
    if not email:
        return True, ""  # Email opcional
    
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(patron, email):
        return True, ""
    return False, "Formato de email inválido"


def validar_telefono(telefono: str) -> Tuple[bool, str]:
    """
    Valida un número de teléfono guatemalteco.
    
    Args:
        telefono: Teléfono a validar
        
    Returns:
        Tupla (es_valido, mensaje)
    """
    if not telefono:
        return True, ""  # Teléfono opcional
    
    # Limpiar formato
    telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
    
    # Validar que tenga 8 dígitos (Guatemala)
    if len(telefono_limpio) == 8 and telefono_limpio.isdigit():
        return True, ""
    return False, "El teléfono debe tener 8 dígitos"


def validar_nit(nit: str) -> Tuple[bool, str]:
    """
    Valida un NIT/DPI guatemalteco.
    
    Args:
        nit: NIT o DPI a validar
        
    Returns:
        Tupla (es_valido, mensaje)
    """
    if not nit:
        return False, "El NIT/DPI es obligatorio"
    
    # Aceptar "CF" para consumidor final
    if nit.upper() == "CF":
        return True, ""
    
    # Validar que sea numérico o con guiones
    nit_limpio = re.sub(r'[\s\-]', '', nit)
    
    if nit_limpio.isdigit():
        return True, ""
    
    return False, "NIT/DPI inválido (use números o 'CF')"


def validar_precio(precio: str) -> Tuple[bool, str]:
    """
    Valida un precio.
    
    Args:
        precio: Precio a validar
        
    Returns:
        Tupla (es_valido, mensaje)
    """
    try:
        valor = float(precio)
        if valor <= 0:
            return False, "El precio debe ser mayor a 0"
        return True, ""
    except:
        return False, "Precio inválido"


def validar_cantidad(cantidad: str) -> Tuple[bool, str]:
    """
    Valida una cantidad.
    
    Args:
        cantidad: Cantidad a validar
        
    Returns:
        Tupla (es_valido, mensaje)
    """
    try:
        valor = int(cantidad)
        if valor <= 0:
            return False, "La cantidad debe ser mayor a 0"
        return True, ""
    except:
        return False, "Cantidad inválida"
