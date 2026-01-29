"""
API Principal para Condonaciones
FastAPI application para gestión de condonaciones de crédito
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Optional
import uvicorn

from routers import condonaciones
from config.database import get_db

# Crear instancia de FastAPI
app = FastAPI(
    title="API Condonaciones Sparta Ledger",
    description="API para gestión de condonaciones de crédito",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Diccionario de mensajes HTTP estándar
HTTP_STATUS_MESSAGES = {
    200: "OK",
    400: "Bad Request",
    401: "Unauthorized",
    404: "Not Found",
    422: "Unprocessable Entity",
    500: "Internal Server Error"
}


# Manejador de errores HTTP generales (400, 401, 404, etc.)
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """
    Maneja todos los errores HTTPException y los formatea consistentemente
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "status_message": HTTP_STATUS_MESSAGES.get(exc.status_code, "Error"),
            "success": False,
            "mensaje": exc.detail
        }
    )


# Manejador de errores de validación (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Maneja errores de validación de Pydantic (422) y los traduce al español
    """
    errors = exc.errors()
    
    # Extraer el primer error para simplificar
    if errors:
        error = errors[0]
        field = error['loc'][-1] if error['loc'] else 'campo'
        error_type = error['type']
        input_value = error.get('input', '')
        
        # Traducir mensajes comunes
        mensajes = {
            'greater_than': f"El campo '{field}' debe ser mayor a {error.get('ctx', {}).get('gt', 0)}. Valor recibido: {input_value}",
            'less_than': f"El campo '{field}' debe ser menor a {error.get('ctx', {}).get('lt', 0)}. Valor recibido: {input_value}",
            'int_type': f"El campo '{field}' debe ser un número entero. Valor recibido: {input_value}",
            'string_type': f"El campo '{field}' debe ser texto. Valor recibido: {input_value}",
            'missing': f"El campo '{field}' es obligatorio y no fue proporcionado",
            'int_parsing': f"No se pudo convertir '{input_value}' a un número entero válido",
            'value_error': f"Valor inválido para el campo '{field}': {input_value}"
        }
        
        mensaje = mensajes.get(error_type, f"Error de validación en '{field}': {error.get('msg', 'Valor inválido')}")
    else:
        mensaje = "Error de validación en la solicitud"
    
    return JSONResponse(
        status_code=422,
        content={
            "status_code": 422,
            "status_message": "Unprocessable Entity",
            "success": False,
            "mensaje": mensaje,
            "detail": errors  # Incluir detalles técnicos para debugging
        }
    )


# Manejador de errores generales no capturados (500)
@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """
    Maneja errores no capturados y los convierte en respuestas 500 formateadas
    """
    return JSONResponse(
        status_code=500,
        content={
            "status_code": 500,
            "status_message": "Internal Server Error",
            "success": False,
            "mensaje": "Error interno del servidor. Por favor contacte al administrador.",
            "detail": str(exc)  # En producción, podrías querer ocultar esto
        }
    )


# Incluir routers
app.include_router(condonaciones.router, prefix="/api", tags=["condonaciones"])


@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "mensaje": "API Condonaciones Sparta Ledger",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Verificar estado de la API"""
    return {
        "status": "ok",
        "mensaje": "API funcionando correctamente"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
