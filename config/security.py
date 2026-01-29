"""
Sistema de Seguridad y Autenticación
"""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de API Keys
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Cargar API Keys válidas desde .env (separadas por comas)
VALID_API_KEYS = os.getenv("API_KEYS", "").split(",")
VALID_API_KEYS = [key.strip() for key in VALID_API_KEYS if key.strip()]


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verifica que el API Key proporcionado sea válido.
    
    Args:
        api_key: API Key del header X-API-Key
        
    Returns:
        El API Key si es válido
        
    Raises:
        HTTPException: Si el API Key es inválido o no existe
    """
    if not VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No hay API Keys configuradas en el servidor"
        )
    
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida o no autorizada"
        )
    
    return api_key


def generate_api_key() -> str:
    """
    Genera un nuevo API Key aleatorio.
    Útil para crear nuevas claves.
    
    Returns:
        Un API Key de 32 caracteres
    """
    import secrets
    return secrets.token_urlsafe(32)


# Para generar un nuevo API Key, ejecuta:
# python -c "from config.security import generate_api_key; print(generate_api_key())"
