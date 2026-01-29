"""
Utilidades de validación
"""

import re
from fastapi import HTTPException, status


def validar_id_credito(id_credito: int) -> None:
    """
    Valida que el ID de crédito sea válido y no tenga patrones sospechosos.
    
    Args:
        id_credito: ID del crédito a validar
        
    Raises:
        HTTPException: Si el ID no es válido
    """
    
    # Validar que no sea 0
    if id_credito <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del crédito debe ser mayor a 0"
        )
    
    # Convertir a string para validar patrones
    id_str = str(id_credito)
    
    # Validar que no sea solo ceros (0, 00, 000, etc.)
    if id_str.replace('0', '') == '':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del crédito no puede ser solo ceros"
        )
    
    # Validar que no tenga patrones repetitivos (1111111, 2222222, etc.)
    if len(id_str) >= 4:  # Solo validar si tiene 4 o más dígitos
        # Verificar si todos los dígitos son iguales
        if len(set(id_str)) == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El ID del crédito no puede tener todos los dígitos iguales ({id_str})"
            )
        
        # Verificar patrones alternantes como 12121212, 343434, etc.
        if len(id_str) >= 6:
            # Verificar patrón de 2 dígitos repetidos
            pattern_2 = id_str[:2]
            if id_str == (pattern_2 * (len(id_str) // 2))[:len(id_str)]:
                if len(id_str) >= 8:  # Solo rechazar si es muy largo
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"El ID del crédito tiene un patrón repetitivo sospechoso ({id_str})"
                    )
            
            # Verificar patrón de 3 dígitos repetidos
            if len(id_str) >= 9:
                pattern_3 = id_str[:3]
                if id_str == (pattern_3 * (len(id_str) // 3))[:len(id_str)]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"El ID del crédito tiene un patrón repetitivo sospechoso ({id_str})"
                    )
    
    # Validar que no sea demasiado grande (opcional)
    if id_credito > 999999999:  # Máximo 9 dígitos
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del crédito excede el límite máximo permitido"
        )


def validar_datos_encontrados(datos: dict, tipo: str, id_credito: int) -> None:
    """
    Valida que se hayan encontrado datos en la consulta.
    
    Args:
        datos: Diccionario con los datos encontrados
        tipo: Tipo de datos ('cliente' o 'gastos')
        id_credito: ID del crédito consultado
        
    Raises:
        HTTPException: Si no se encontraron datos
    """
    
    if not datos:
        if tipo == 'cliente':
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró información del crédito {id_credito}. Verifica que el ID sea correcto."
            )
        elif tipo == 'gastos':
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron gastos de cobranza para el crédito {id_credito}."
            )

