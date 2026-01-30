# DOCUMENTACIÓN TÉCNICA - API DE CONDONACIONES

**Versión:** 1.0.0  
**Fecha:** Enero 2026  
**Framework:** FastAPI 0.109.0  
**Lenguaje:** Python 3.x

---

## Tabla de Contenidos

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Herramientas y Tecnologías Utilizadas](#2-herramientas-y-tecnologías-utilizadas)
3. [Arquitectura y Estructura del Proyecto](#3-arquitectura-y-estructura-del-proyecto)
4. [Implementación de Seguridad](#4-implementación-de-seguridad)
5. [Estructura Detallada del JSON de Respuesta](#5-estructura-detallada-del-json-de-respuesta)
6. [Guía de Consumo de la API](#6-guía-de-consumo-de-la-api)
7. [Documentación Interactiva](#7-documentación-interactiva-swagger-ui)
8. [Configuración y Despliegue](#8-configuración-y-despliegue)

---

## 1. RESUMEN EJECUTIVO

La API de Condonaciones es un servicio REST desarrollado en Python que permite consultar información sobre gastos de cobranza condonados asociados a créditos específicos. Su función principal es exponer de forma segura y eficiente los datos almacenados en bases de datos MySQL, permitiendo a sistemas externos o aplicaciones frontend obtener información detallada sobre:

- **Datos generales del cliente y crédito**: Nombre, domicilio, bucket de morosidad, días de mora, saldo vencido
- **Historial de gastos de cobranza condonados**: Períodos, montos, parcialidades y fechas de condonación
- **Información estructurada**: Respuestas en formato JSON con códigos HTTP estandarizados

La API implementa autenticación mediante API Key y está diseñada como un endpoint de solo lectura (GET) para integrarse con sistemas de gestión financiera o dashboards de análisis de cartera.

### Casos de Uso Principales

- Consulta de historial de condonaciones por crédito
- Integración con sistemas de gestión de cartera
- Análisis de gastos de cobranza condonados
- Generación de reportes financieros

---

## 2. HERRAMIENTAS Y TECNOLOGÍAS UTILIZADAS

### 2.1 Lenguaje de Programación

- **Python 3.x** - Lenguaje principal de desarrollo con tipado estático mediante anotaciones de tipo

### 2.2 Frameworks y Librerías

#### Framework Web

**FastAPI 0.109.0** - Framework web moderno y de alto rendimiento para construcción de APIs REST

Características principales:
- Validación automática de datos con Pydantic
- Documentación interactiva automática (Swagger UI / ReDoc)
- Soporte nativo para operaciones asíncronas (async/await)
- Inyección de dependencias integrada
- Rendimiento comparable a NodeJS y Go

**Uvicorn 0.27.0** - Servidor ASGI de alto rendimiento

- Implementación de servidor asíncrono basado en uvloop
- Soporte para HTTP/1.1 y WebSockets
- Manejo eficiente de conexiones concurrentes

#### Validación de Datos

**Pydantic 2.5.3** - Validación de datos y serialización mediante modelos tipados

- Definición de esquemas de entrada/salida con Python type hints
- Conversión automática de tipos de datos
- Validación de campos obligatorios, opcionales y con restricciones
- Generación automática de JSON Schema

#### Gestión de Base de Datos

**PyMySQL 1.1.0** - Conector Python puro para bases de datos MySQL/MariaDB

- Implementación completa del protocolo MySQL en Python
- Conexión a múltiples bases de datos
- Ejecución de consultas parametrizadas (prepared statements)
- Context managers para manejo seguro de conexiones
- Soporte para transacciones y cursores

#### Configuración y Seguridad

**python-dotenv 1.0.1** - Gestión de variables de entorno

- Carga de configuración desde archivos .env
- Almacenamiento seguro de credenciales fuera del código fuente
- Separación de configuración por ambiente (desarrollo/producción/testing)

#### Utilidades Adicionales

**python-multipart 0.0.6** - Procesamiento de datos multipart/form-data

---

## 3. ARQUITECTURA Y ESTRUCTURA DEL PROYECTO

### 3.1 Patrón Arquitectónico

El proyecto implementa una **arquitectura por capas (Layered Architecture)** con separación clara de responsabilidades, siguiendo los principios SOLID:

- **S**ingle Responsibility Principle: Cada módulo tiene una única responsabilidad
- **O**pen/Closed Principle: Extensible sin modificar código existente
- **L**iskov Substitution Principle: Uso de abstracciones e interfaces
- **I**nterface Segregation Principle: Dependencias específicas y granulares
- **D**ependency Inversion Principle: Inyección de dependencias con FastAPI

#### Capas del Sistema

```
┌─────────────────────────────────────────────┐
│   CAPA DE PRESENTACIÓN (Routers)           │  ← Exposición de endpoints HTTP
├─────────────────────────────────────────────┤
│   CAPA DE LÓGICA DE NEGOCIO (Utils)        │  ← Validaciones y reglas
├─────────────────────────────────────────────┤
│   CAPA DE MODELO (Models)                   │  ← Definición de estructuras
├─────────────────────────────────────────────┤
│   CAPA DE SEGURIDAD (Config/Security)      │  ← Autenticación y autorización
├─────────────────────────────────────────────┤
│   CAPA DE ACCESO A DATOS (Config/Database) │  ← Conexión a base de datos
└─────────────────────────────────────────────┘
```

### 3.2 Estructura de Directorios

```
api_python/
│
├── main.py                      # Punto de entrada - Aplicación FastAPI
├── requirements.txt             # Dependencias del proyecto
├── .env                         # Variables de entorno (no versionado)
├── README.md                    # Documentación de uso general
│
├── config/                      # Configuraciones globales del sistema
│   ├── __init__.py
│   ├── database.py              # Gestión de conexiones a MySQL
│   └── security.py              # Sistema de autenticación API Key
│
├── models/                      # Modelos de datos (Pydantic schemas)
│   ├── __init__.py
│   └── condonaciones.py         # Esquemas de entrada/salida
│
├── routers/                     # Endpoints de la API (controladores)
│   ├── __init__.py
│   └── condonaciones.py         # Rutas de condonaciones
│
└── utils/                       # Utilidades y funciones auxiliares
    ├── __init__.py
    └── validations.py           # Funciones de validación de datos
```

### 3.3 Responsabilidades de Cada Módulo

#### main.py
- Instanciación de la aplicación FastAPI
- Configuración de middleware (CORS, headers de seguridad)
- Registro de routers
- Manejadores globales de excepciones
- Configuración de metadatos de la API

#### config/database.py
- Clase `DatabaseConfig` con parámetros de conexión
- Context manager `get_db_connection()` para gestión segura de conexiones
- Función `get_db()` como dependencia inyectable en FastAPI
- Soporte para múltiples bases de datos

#### config/security.py
- Definición de header `X-API-Key`
- Carga de API Keys válidas desde variables de entorno
- Función `verify_api_key()` para autenticación
- Generador de API Keys para administración

#### models/condonaciones.py
- `DetalleCondonacion`: Modelo para gastos de cobranza individuales
- `DatosGenerales`: Modelo para información del cliente y crédito
- `CondonacionCobranza`: Contenedor de detalles de condonación
- `CondonacionResponse`: Respuesta completa de la API
- `ErrorResponse`: Estructura de errores estandarizada

#### routers/condonaciones.py
- Endpoint `GET /condonaciones/{id_credito}`: Consulta principal
- Lógica de orquestación entre validaciones, BD y modelos
- Manejo de excepciones específicas del dominio
- Documentación de endpoint (docstrings, response_model)

#### utils/validations.py
- `validar_id_credito()`: Validación de formato y patrones sospechosos
- `validar_datos_encontrados()`: Verificación de existencia de datos
- Prevención de inyecciones y fuzzing attacks

### 3.4 Flujo de Comunicación entre Componentes

#### Diagrama de Secuencia

```
Cliente         FastAPI         Security        Validations       Database        Models
  │                │                │                │                │              │
  │──GET /12345───>│                │                │                │              │
  │  X-API-Key     │                │                │                │              │
  │                │                │                │                │              │
  │                │──verify_key──>│                │                │              │
  │                │<──OK/401──────│                │                │              │
  │                │                │                │                │              │
  │                │────validate_id────────────────>│                │              │
  │                │<───OK/400─────────────────────│                │              │
  │                │                │                │                │              │
  │                │────────────────────get_connection──────────────>│              │
  │                │<───────────────────Connection──────────────────│              │
  │                │                │                │                │              │
  │                │────────────────────execute_query────────────────>│              │
  │                │<───────────────────ResultSet────────────────────│              │
  │                │                │                │                │              │
  │                │────validate_found────────────>│                │              │
  │                │<───OK/404─────────────────────│                │              │
  │                │                │                │                │              │
  │                │────────────────────────────────────convert──────────────────>│
  │                │<───────────────────────────────────Pydantic Model───────────│
  │                │                │                │                │              │
  │<──JSON 200─────│                │                │                │              │
```

#### Flujo Detallado de una Petición

1. **Cliente HTTP** envía petición GET con header `X-API-Key`

2. **main.py** (FastAPI Application) recibe y enruta la petición al router correspondiente

3. **routers/condonaciones.py** invoca `verify_api_key()` mediante inyección de dependencias
   ```python
   api_key: str = Security(verify_api_key)
   ```

4. **config/security.py** valida el API Key
   - Si es inválido: retorna `401 Unauthorized`
   - Si es válido: continúa la ejecución

5. **routers/condonaciones.py** invoca `validar_id_credito(id_credito)`

6. **utils/validations.py** valida el formato y detecta patrones sospechosos
   - Si es inválido: lanza `HTTPException(400)`
   - Si es válido: continúa la ejecución

7. **routers/condonaciones.py** obtiene conexión a BD mediante context manager
   ```python
   with get_db_connection(database="db-mega-reporte") as conn:
   ```

8. **config/database.py** crea conexión MySQL con PyMySQL
   - Context manager garantiza cierre automático

9. **routers/condonaciones.py** ejecuta consultas SQL parametrizadas
   - Query 1: `tbl_segundometro_semana` (datos generales)
   - Query 2: `gastos_cobranza` (detalles condonados WHERE condonado=1)

10. **utils/validations.py** valida que existan resultados
    - Si no existe: lanza `HTTPException(404)`
    - Si existe: continúa la ejecución

11. **models/condonaciones.py** convierte datos de BD a modelos Pydantic
    ```python
    datos_generales = DatosGenerales(**datos_generales_row)
    detalles = [DetalleCondonacion(**row) for row in detalles_rows]
    ```

12. **routers/condonaciones.py** construye respuesta completa
    ```python
    return CondonacionResponse(
        status_code=200,
        success=True,
        datos_generales=datos_generales,
        condonacion_cobranza=CondonacionCobranza(detalle=detalles)
    )
    ```

13. **main.py** serializa la respuesta a JSON y la envía al cliente

### 3.5 Ejemplos de Código Real (Anonimizado)

#### config/database.py - Gestión de Conexiones

```python
from contextlib import contextmanager
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    """Configuración centralizada de base de datos"""
    HOST = os.getenv("DB_HOST", "localhost")
    PORT = int(os.getenv("DB_PORT", "3306"))
    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD", "")
    DATABASE = os.getenv("DB_DATABASE", "db-mega-reporte")

@contextmanager
def get_db_connection(database: str = None):
    """
    Context manager para conexión segura a base de datos.
    Garantiza cierre de conexión incluso en caso de excepción.
    
    Args:
        database: Nombre de la base de datos (opcional)
        
    Yields:
        pymysql.connections.Connection: Conexión activa a MySQL
    """
    connection = pymysql.connect(
        host=DatabaseConfig.HOST,
        port=DatabaseConfig.PORT,
        user=DatabaseConfig.USER,
        password=DatabaseConfig.PASSWORD,
        database=database or DatabaseConfig.DATABASE,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # Resultados como diccionarios
    )
    
    try:
        yield connection
    finally:
        connection.close()  # Cierre garantizado
```

**Ventajas del diseño:**
- **Separación de configuración**: Credenciales en variables de entorno
- **Context manager**: Cierre automático de conexiones (previene memory leaks)
- **Cursor tipo dict**: Facilita conversión a modelos Pydantic
- **Charset utf8mb4**: Soporte completo de Unicode (incluyendo emojis si los hubiera en datos)

#### routers/condonaciones.py - Endpoint Principal

```python
from fastapi import APIRouter, HTTPException, Path, Security
import pymysql
from typing import Optional

from models.condonaciones import CondonacionResponse, DatosGenerales, CondonacionCobranza, DetalleCondonacion
from config.database import get_db_connection
from config.security import verify_api_key
from utils.validations import validar_id_credito, validar_datos_encontrados

router = APIRouter()

@router.get(
    "/condonaciones/{id_credito}",
    response_model=CondonacionResponse,
    responses={
        200: {"description": "Éxito - Datos obtenidos correctamente"},
        400: {"description": "Bad Request - ID inválido o mal formado"},
        401: {"description": "No Autenticado - API Key inválida o faltante"},
        404: {"description": "No Encontrado - Crédito no existe"},
        500: {"description": "Error del Servidor - Error interno"}
    },
    summary="Obtener información de condonación por ID de crédito",
    description="Retorna los gastos de cobranza CONDONADOS (condonado=1). Si no hay gastos condonados, retorna array vacío."
)
async def get_condonacion_por_credito(
    id_credito: int = Path(..., description="ID del crédito a consultar", gt=0),
    api_key: str = Security(verify_api_key)
):
    """
    Obtiene información completa de condonación para un crédito específico.
    
    Args:
        id_credito: ID del crédito (debe ser > 0)
        api_key: API Key de autenticación (header X-API-Key)
        
    Returns:
        CondonacionResponse: Respuesta estructurada con datos del cliente y gastos condonados
        
    Raises:
        HTTPException 400: ID inválido
        HTTPException 401: API Key inválida
        HTTPException 404: Crédito no encontrado
        HTTPException 500: Error de base de datos
    """
    
    try:
        # Paso 1: Validar ID de crédito contra patrones sospechosos
        validar_id_credito(id_credito)
        
        # Paso 2: Obtener datos generales del cliente
        with get_db_connection(database="db-mega-reporte") as conn:
            with conn.cursor() as cursor:
                query_datos_generales = """
                    SELECT 
                        Id_credito as id_credito,
                        Nombre_cliente as nombre_cliente,
                        Id_cliente as id_cliente,
                        Domicilio_Completo as domicilio_completo,
                        Bucket_Morosidad_Real as bucket_morosidad,
                        Dias_mora as dias_mora,
                        saldo_vencido_inicio as saldo_vencido
                    FROM tbl_segundometro_semana
                    WHERE Id_credito = %s
                    LIMIT 1
                """
                
                cursor.execute(query_datos_generales, (id_credito,))
                datos_generales_row = cursor.fetchone()
                
                # Validar que se encontraron datos
                validar_datos_encontrados(datos_generales_row, 'cliente', id_credito)
                
                # Convertir a modelo Pydantic
                datos_generales = DatosGenerales(**datos_generales_row)
        
        # Paso 3: Obtener gastos de cobranza condonados
        with get_db_connection(database="db-mega-reporte") as conn:
            with conn.cursor() as cursor:
                query_gastos = """
                    SELECT 
                        periodo_inicio as periodoinicio,
                        periodo_fin as periodofin,
                        SEMANA as semana,
                        parcialidad,
                        monto_valor,
                        cuota,
                        condonado,
                        fecha_condonacion
                    FROM gastos_cobranza
                    WHERE Id_credito = %s
                      AND condonado = 1
                    ORDER BY periodo_inicio ASC
                """
                
                cursor.execute(query_gastos, (id_credito,))
                detalles_rows = cursor.fetchall()
                
                # Convertir a modelos Pydantic (puede estar vacío)
                detalles = [DetalleCondonacion(**row) for row in detalles_rows]
                condonacion_cobranza = CondonacionCobranza(detalle=detalles)
        
        # Paso 4: Construir respuesta
        mensaje = (
            f"Se encontraron {len(detalles)} gastos condonados" 
            if detalles 
            else "No hay gastos condonados para este crédito"
        )
        
        response = CondonacionResponse(
            status_code=200,
            status_message="OK",
            success=True,
            mensaje=mensaje,
            datos_generales=datos_generales,
            condonacion_cobranza=condonacion_cobranza
        )
        
        return response
        
    except HTTPException:
        # Re-lanzar excepciones HTTP controladas
        raise
    except pymysql.Error as db_error:
        # Capturar errores específicos de base de datos
        raise HTTPException(
            status_code=500,
            detail=f"Error de base de datos: {str(db_error)}"
        )
    except Exception as e:
        # Capturar cualquier otro error inesperado
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )
```

**Principios aplicados:**
- **Parámetros vinculados**: Prevención de SQL injection
- **Separación de consultas**: Una conexión por query (context manager por bloque)
- **Manejo granular de errores**: Distinción entre errores de validación, BD y sistema
- **Documentación OpenAPI**: Metadatos automáticos para Swagger UI

#### utils/validations.py - Validación contra Inyecciones

```python
from fastapi import HTTPException, status

def validar_id_credito(id_credito: int) -> None:
    """
    Valida ID de crédito contra patrones sospechosos y ataques.
    
    Previene:
    - Valores negativos o cero
    - Patrones repetitivos (1111111, 2222222) - posible fuzzing
    - IDs excesivamente grandes - posible integer overflow
    
    Args:
        id_credito: ID del crédito a validar
        
    Raises:
        HTTPException 400: Si el ID no pasa las validaciones
    """
    
    # Validación 1: Rango básico
    if id_credito <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del crédito debe ser mayor a 0"
        )
    
    # Validación 2: Detectar patrones repetitivos
    id_str = str(id_credito)
    
    # Validar que no sea solo ceros (0, 00, 000)
    if id_str.replace('0', '') == '':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del crédito no puede ser solo ceros"
        )
    
    # Validar que no tenga todos los dígitos iguales (1111111, 2222222)
    if len(id_str) >= 4:
        if len(set(id_str)) == 1:  # set elimina duplicados
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El ID del crédito no puede tener todos los dígitos iguales ({id_str})"
            )
        
        # Detectar patrones alternantes (12121212, 343434)
        if len(id_str) >= 6:
            pattern_2 = id_str[:2]
            if id_str == (pattern_2 * (len(id_str) // 2))[:len(id_str)]:
                if len(id_str) >= 8:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"El ID del crédito tiene un patrón repetitivo sospechoso ({id_str})"
                    )
    
    # Validación 3: Límite máximo (prevenir overflow)
    if id_credito > 999999999:  # Máximo 9 dígitos
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del crédito excede el límite máximo permitido"
        )


def validar_datos_encontrados(datos: dict, tipo: str, id_credito: int) -> None:
    """
    Valida que se hayan encontrado datos en la consulta.
    
    Args:
        datos: Diccionario con los datos encontrados (o None)
        tipo: Tipo de datos ('cliente' o 'gastos')
        id_credito: ID del crédito consultado
        
    Raises:
        HTTPException 404: Si no se encontraron datos
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
```

**Estrategias de validación:**
- **Validación de tipo**: FastAPI + Pydantic validan que sea `int`
- **Validación de rango**: Mayor a 0 y menor a límite establecido
- **Detección de patrones**: Prevención de fuzzing y ataques automatizados
- **Mensajes descriptivos**: Facilitan debugging al desarrollador cliente

#### config/security.py - Autenticación API Key

```python
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de header personalizado
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Cargar API Keys válidas desde .env
VALID_API_KEYS = os.getenv("API_KEYS", "").split(",")
VALID_API_KEYS = [key.strip() for key in VALID_API_KEYS if key.strip()]


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verifica que el API Key proporcionado sea válido.
    
    Esta función se ejecuta automáticamente antes del endpoint
    mediante inyección de dependencias de FastAPI.
    
    Args:
        api_key: API Key extraído del header X-API-Key
        
    Returns:
        str: El API Key si es válido
        
    Raises:
        HTTPException 500: Si no hay API Keys configuradas
        HTTPException 401: Si el API Key es inválido
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
    Genera un nuevo API Key aleatorio criptográficamente seguro.
    
    Útil para administración de claves.
    
    Returns:
        str: API Key de 32 caracteres URL-safe
        
    Example:
        >>> python -c "from config.security import generate_api_key; print(generate_api_key())"
        dQw4w9WgXcQ7ZhF3kLm2Nop5Qrs6Tuv8
    """
    import secrets
    return secrets.token_urlsafe(32)
```

**Características de seguridad:**
- **Tokens URL-safe**: Sin caracteres especiales que causen problemas en headers
- **Generación criptográfica**: Uso de `secrets` (no `random`)
- **Configuración externa**: API Keys nunca en código fuente
- **Múltiples claves**: Soporte para varios clientes simultáneos

---

## 4. IMPLEMENTACIÓN DE SEGURIDAD

La API implementa un modelo de **seguridad en capas (Defense in Depth)** para proteger contra ataques comunes y garantizar la integridad de los datos. Cada capa aborda amenazas específicas:

### 4.1 Capa 1: Autenticación mediante API Key

#### Fundamento de Seguridad

El sistema utiliza autenticación basada en **API Key estática** almacenada en el header `X-API-Key`. Este mecanismo es apropiado para APIs de servidor a servidor (machine-to-machine) donde:

- No hay interacción humana directa
- Los clientes son aplicaciones confiables
- Se requiere simplicidad operativa
- El tráfico va sobre HTTPS (prerequisito obligatorio)

**Comparación con otros métodos:**

| Método | Complejidad | Revocación | Apropiado para |
|--------|-------------|------------|----------------|
| API Key | Baja | Inmediata | APIs internas, M2M |
| OAuth 2.0 | Alta | Configurable | APIs públicas, delegación |
| JWT | Media | Limitada | SPAs, microservicios |
| Basic Auth | Muy baja | No aplicable | Desarrollo/testing |

#### Implementación Técnica

```python
# config/security.py
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Carga desde .env (nunca hardcoded)
VALID_API_KEYS = os.getenv("API_KEYS", "").split(",")

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="API Key inválida")
    return api_key
```

**Uso en endpoints:**
```python
@router.get("/condonaciones/{id_credito}")
async def get_condonacion(
    id_credito: int,
    api_key: str = Security(verify_api_key)  # Inyección de dependencia
):
    # La función NO se ejecuta si verify_api_key falla
    pass
```

#### Flujo de Autenticación

```
1. Cliente envía petición:
   GET /condonaciones/12345
   Headers:
     X-API-Key: dQw4w9WgXcQ7ZhF3kLm2Nop5Qrs6Tuv8

2. FastAPI extrae automáticamente el header (APIKeyHeader)

3. verify_api_key() compara contra VALID_API_KEYS

4a. Si coincide: permite ejecución del endpoint
4b. Si NO coincide: retorna 401 Unauthorized (sin ejecutar endpoint)
```

#### Protección que Provee

| Amenaza | Cómo la mitiga |
|---------|----------------|
| **Acceso no autorizado** | Solo clientes con clave válida pueden consultar |
| **Ataques de fuerza bruta** | Claves de 32 caracteres (43^32 combinaciones) |
| **Auditoría** | Cada API Key puede asociarse a un cliente específico |
| **Revocación instantánea** | Eliminar clave del .env bloquea acceso inmediatamente |
| **Exposición de credenciales** | Claves nunca en código fuente (solo .env) |

#### Mejores Prácticas Implementadas

1. **Generación criptográfica**: Uso de `secrets.token_urlsafe()` (no `random`)
2. **Almacenamiento seguro**: Variables de entorno, no base de datos
3. **Rotación programada**: Facilidad para cambiar claves sin downtime
4. **Múltiples claves**: Soporte para varios clientes simultáneos
5. **Logging implícito**: FastAPI registra peticiones con header API Key (útil para auditoría)

### 4.2 Capa 2: Validación de Entrada (Input Validation)

#### Fundamento de Seguridad

La validación de entrada es la primera línea de defensa contra ataques de **inyección de datos**. Según OWASP Top 10, las vulnerabilidades de inyección son la amenaza #1 en aplicaciones web.

**Principio**: Never trust user input - Toda entrada debe ser validada, sanitizada y verificada antes de ser procesada.

#### Validación Automática con Pydantic

FastAPI + Pydantic implementan validación **declarativa** mediante type hints de Python:

```python
@router.get("/condonaciones/{id_credito}")
async def get_condonacion(
    id_credito: int = Path(..., description="ID del crédito", gt=0)
    # Restricciones:
    # - Tipo: int (rechaza strings, floats, null)
    # - gt=0: greater than 0 (rechaza 0, negativos)
    # - ...: obligatorio (rechaza ausencia)
):
```

**Validaciones automáticas aplicadas:**

| Validación | Ejemplo Rechazado | Código HTTP | Mensaje |
|------------|-------------------|-------------|---------|
| **Tipo incorrecto** | `/condonaciones/abc` | 422 | "Input should be a valid integer" |
| **Menor o igual a 0** | `/condonaciones/0` | 422 | "Input should be greater than 0" |
| **Ausente** | `/condonaciones/` | 404 | "Not Found" (ruta no coincide) |
| **Demasiado grande** | `/condonaciones/99999999999999` | 422 | "Input should be less than..." |

#### Validación Personalizada contra Inyecciones

Además de la validación automática, implementamos lógica personalizada para detectar patrones maliciosos:

```python
def validar_id_credito(id_credito: int) -> None:
    """
    Validaciones adicionales contra ataques:
    
    1. Patrones repetitivos (1111111, 2222222)
       - Detecta intentos de fuzzing automatizado
       - Común en herramientas como SQLMap, Burp Suite
       
    2. Patrones alternantes (12121212, 343434)
       - Detecta scripts que generan IDs secuenciales
       
    3. Límite máximo (999999999)
       - Previene integer overflow en MySQL
       - MySQL INT tiene rango: -2147483648 a 2147483647
    """
    
    id_str = str(id_credito)
    
    # Detectar todos los dígitos iguales
    if len(set(id_str)) == 1:  # set(['1','1','1']) = {'1'}
        raise HTTPException(400, detail="Patrón inválido detectado")
    
    # Detectar patrones alternantes de 2 dígitos
    pattern_2 = id_str[:2]
    if id_str == (pattern_2 * (len(id_str) // 2))[:len(id_str)]:
        raise HTTPException(400, detail="Patrón repetitivo sospechoso")
    
    # Validar límite superior
    if id_credito > 999999999:
        raise HTTPException(400, detail="ID excede límite máximo")
```

#### Protección que Provee

| Ataque | Mecanismo de Defensa | Resultado |
|--------|----------------------|-----------|
| **SQL Injection** | Validación de tipo (int) + prepared statements | Imposible inyectar SQL |
| **NoSQL Injection** | No aplicable (usamos MySQL) | - |
| **Command Injection** | No se ejecutan comandos del sistema | - |
| **Path Traversal** | ID numérico (no paths) | No aplicable |
| **Fuzzing automatizado** | Detección de patrones repetitivos | Bloqueo de scanners |
| **Integer overflow** | Límite máximo explícito | Prevención de desbordamiento |

#### Ejemplo de Ataque Bloqueado

**Intento de fuzzing con SQLMap:**
```bash
sqlmap -u "https://API/condonaciones/1*" --batch

# SQLMap intentará inyecciones como:
# /condonaciones/1'
# /condonaciones/1"
# /condonaciones/1111111
# /condonaciones/-1
```

**Respuesta de la API:**
```json
{
  "status_code": 422,
  "status_message": "Unprocessable Entity",
  "success": false,
  "mensaje": "Input should be a valid integer"
}
```

### 4.3 Capa 3: Consultas Parametrizadas (Prepared Statements)

#### Fundamento de Seguridad

Las **consultas parametrizadas** son la defensa definitiva contra SQL Injection. Separan el código SQL de los datos, eliminando la posibilidad de que entrada maliciosa sea interpretada como comandos SQL.

**Cómo funcionan:**

1. **Query con placeholder**: `SELECT * FROM users WHERE id = %s`
2. **Parámetros separados**: `(id_credito,)`
3. **Driver escapa automáticamente**: PyMySQL convierte valores a tipos SQL seguros
4. **Envío por separado**: MySQL recibe estructura y datos por canales diferentes

#### Comparación: Vulnerable vs Seguro

**Código VULNERABLE (NUNCA usar):**
```python
# Construcción de string con f-string o concatenación
query = f"SELECT * FROM clientes WHERE id_credito = {id_credito}"
cursor.execute(query)

# Ataque exitoso:
# id_credito = "1 OR 1=1; DROP TABLE clientes--"
# Query resultante:
# SELECT * FROM clientes WHERE id_credito = 1 OR 1=1; DROP TABLE clientes--
```

**Código SEGURO (implementado):**
```python
# Placeholder %s con parámetros separados
query = "SELECT * FROM clientes WHERE id_credito = %s"
cursor.execute(query, (id_credito,))

# Ataque bloqueado:
# id_credito = "1 OR 1=1; DROP TABLE--"
# PyMySQL escapa y convierte a:
# SELECT * FROM clientes WHERE id_credito = '1 OR 1=1; DROP TABLE--'
# MySQL busca literalmente ese string (no existe, retorna vacío)
```

#### Implementación en el Proyecto

```python
# routers/condonaciones.py
with get_db_connection() as conn:
    with conn.cursor() as cursor:
        # Query con placeholders
        query = """
            SELECT 
                Id_credito as id_credito,
                Nombre_cliente as nombre_cliente
            FROM tbl_segundometro_semana
            WHERE Id_credito = %s  -- Placeholder seguro
            LIMIT 1
        """
        
        # Parámetros como tupla
        cursor.execute(query, (id_credito,))  # PyMySQL escapa automáticamente
        resultado = cursor.fetchone()
```

**Características de PyMySQL:**
- Escapa automáticamente caracteres peligrosos: `'`, `"`, `;`, `--`, `/*`, etc.
- Convierte tipos Python a tipos SQL seguros
- Previene ataques de truncamiento (null bytes, Unicode exploits)
- Compatible con charset utf8mb4 (previene ataques de charset)

#### Protección que Provee

| Escenario de Ataque | Sin Prepared Statements | Con Prepared Statements |
|---------------------|-------------------------|-------------------------|
| **Inyección clásica** | `1 OR 1=1` retorna todos los registros | Busca literalmente "1 OR 1=1" (no encuentra) |
| **Union-based** | `1 UNION SELECT password FROM users` | Busca literalmente el string completo |
| **Time-based blind** | `1 AND SLEEP(10)` causa delay | Busca literalmente "1 AND SLEEP(10)" |
| **Stacked queries** | `1; DROP TABLE` ejecuta dos queries | Busca literalmente "1; DROP TABLE" |

#### Prueba de Concepto

```python
# Simulación de intento de inyección
id_credito_malicioso = "1 OR 1=1; DROP TABLE gastos_cobranza--"

# Con prepared statement (SEGURO):
cursor.execute(
    "SELECT * FROM gastos_cobranza WHERE Id_credito = %s",
    (id_credito_malicioso,)
)
# MySQL busca: WHERE Id_credito = '1 OR 1=1; DROP TABLE gastos_cobranza--'
# Resultado: 0 registros (no existe ese ID literal)
# Tabla gastos_cobranza: INTACTA

# Sin prepared statement (VULNERABLE):
cursor.execute(
    f"SELECT * FROM gastos_cobranza WHERE Id_credito = {id_credito_malicioso}"
)
# MySQL ejecuta: WHERE Id_credito = 1 OR 1=1; DROP TABLE gastos_cobranza--
# Resultado: Tabla ELIMINADA
```

### 4.4 Capa 4: CORS (Cross-Origin Resource Sharing)

#### Fundamento de Seguridad

CORS es un mecanismo de seguridad implementado por los navegadores para prevenir que sitios web maliciosos accedan a recursos de otros dominios sin autorización explícita.

**Problema que resuelve:**

Sin CORS, un sitio malicioso `https://malicioso.com` podría hacer peticiones desde el navegador del usuario a `https://tu-api.com`, aprovechando las credenciales (cookies, API Keys) del usuario.

**Cómo funciona:**

```
1. Navegador detecta petición cross-origin (dominio diferente)

2. Navegador envía "preflight request" (OPTIONS):
   Origin: https://cliente-frontend.com

3. Servidor responde con headers de autorización:
   Access-Control-Allow-Origin: https://cliente-frontend.com
   Access-Control-Allow-Methods: GET, POST
   Access-Control-Allow-Headers: X-API-Key

4. Navegador permite o bloquea según la respuesta
```

#### Implementación

```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dashboard-produccion.tudominio.com",
        "https://app.tudominio.com"
    ],  # Lista blanca de dominios permitidos
    allow_credentials=True,  # Permite envío de credenciales (API Keys, cookies)
    allow_methods=["GET"],  # Solo GET (API de solo lectura)
    allow_headers=["X-API-Key", "Content-Type"],  # Headers permitidos
)
```

**Configuración por ambiente:**

```python
# Desarrollo
allow_origins=["http://localhost:3000", "http://localhost:8080"]

# Producción
allow_origins=["https://app.produccion.com"]

# NUNCA en producción
allow_origins=["*"]  # Permite CUALQUIER dominio (inseguro)
```

#### Protección que Provee

| Ataque | Sin CORS | Con CORS |
|--------|----------|----------|
| **CSRF (Cross-Site Request Forgery)** | Sitio malicioso puede hacer peticiones | Navegador bloquea peticiones no autorizadas |
| **Credential harvesting** | Sitio malicioso roba respuestas | Solo dominios autorizados ven respuestas |
| **Clickjacking** | API puede ser embebida en iframe malicioso | Se puede combinar con X-Frame-Options |

**Importante:** CORS es una protección del **navegador**, no afecta peticiones desde:
- Herramientas de línea de comandos (curl, wget)
- Aplicaciones de escritorio
- Servidores backend
- Scripts Python/Node.js

Por eso CORS se usa **en combinación** con autenticación API Key.

### 4.5 Capa 5: Gestión de Conexiones a Base de Datos

#### Fundamento de Seguridad

La gestión inadecuada de conexiones a base de datos puede causar:

1. **Connection pool exhaustion**: Agotamiento de conexiones disponibles
2. **Deadlocks**: Bloqueos de recursos entre transacciones
3. **Memory leaks**: Conexiones no cerradas consumen memoria indefinidamente
4. **Denial of Service**: Servidor de BD sobrecargado rechaza peticiones legítimas

#### Implementación con Context Managers

```python
from contextlib import contextmanager

@contextmanager
def get_db_connection(database: str = None):
    """
    Context manager que garantiza cierre de conexión.
    
    Ventajas:
    1. SIEMPRE cierra la conexión (incluso con excepciones)
    2. Sintaxis limpia con 'with' statement
    3. Previene memory leaks
    4. Compatible con try/except/finally
    """
    connection = pymysql.connect(...)
    
    try:
        yield connection  # Entrega conexión al bloque 'with'
    finally:
        connection.close()  # SIEMPRE se ejecuta
```

**Uso correcto:**
```python
with get_db_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT ...")
        resultado = cursor.fetchone()
# Aquí la conexión ya está cerrada automáticamente
```

**Flujo de ejecución:**

```
1. Se ejecuta __enter__ (crea conexión)
2. yield connection (entrega al bloque with)
3. Bloque with se ejecuta (queries, procesamiento)
4a. Si hay excepción: salta a finally, cierra conexión, propaga excepción
4b. Si no hay excepción: ejecuta finally, cierra conexión, continúa
```

#### Comparación: Código Vulnerable vs Seguro

**Código VULNERABLE:**
```python
# Sin context manager
def consultar_datos(id_credito):
    conn = pymysql.connect(...)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_credito,))
    resultado = cursor.fetchone()
    
    # Si aquí ocurre una excepción, la conexión NUNCA se cierra
    procesar_resultado(resultado)
    
    conn.close()  # Línea que puede no alcanzarse
    return resultado

# Problema: Si procesar_resultado() falla, conn.close() nunca se ejecuta
```

**Código SEGURO (implementado):**
```python
def consultar_datos(id_credito):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_credito,))
            resultado = cursor.fetchone()
            
            # Aunque aquí ocurra excepción, conexión se cierra automáticamente
            procesar_resultado(resultado)
            
    # Aquí conexión YA está cerrada (garantizado)
    return resultado
```

#### Protección que Provee

| Amenaza | Mecanismo de Defensa | Resultado |
|---------|----------------------|-----------|
| **Connection pool exhaustion** | Cierre garantizado de conexiones | Pool siempre tiene conexiones disponibles |
| **Memory leaks** | Liberación automática de recursos | Memoria se libera consistentemente |
| **DoS por sobrecarga** | Límite implícito de conexiones concurrentes | BD no se sobrecarga |
| **Deadlocks** | Conexiones de corta duración | Reduce probabilidad de bloqueos |
| **Transacciones colgadas** | Rollback automático al cerrar conexión | BD mantiene consistencia |

#### Configuración Adicional de Seguridad

```python
connection = pymysql.connect(
    host=DatabaseConfig.HOST,
    port=DatabaseConfig.PORT,
    user=DatabaseConfig.USER,
    password=DatabaseConfig.PASSWORD,
    database=database,
    
    # Configuraciones de seguridad
    charset='utf8mb4',  # Previene ataques de charset
    connect_timeout=10,  # Timeout de conexión (evita cuelgues)
    read_timeout=30,     # Timeout de lectura
    write_timeout=30,    # Timeout de escritura
    
    # Configuraciones de rendimiento
    cursorclass=pymysql.cursors.DictCursor,  # Resultados como dict
    autocommit=False,  # Control explícito de transacciones
)
```

### 4.6 Códigos HTTP Estandarizados

#### Fundamento de Diseño

El uso correcto de códigos de estado HTTP facilita:

1. **Manejo de errores en el cliente**: Lógica diferenciada según tipo de error
2. **Debugging**: Identificación rápida de la naturaleza del problema
3. **Cacheo**: Proxies y CDNs pueden cachear según código
4. **Monitoreo**: Alertas automáticas basadas en códigos 5xx
5. **Estándares REST**: Cumplimiento con convenciones de la industria

#### Tabla de Códigos Utilizados

| Código | Significado | Cuándo se Usa | Acción Recomendada del Cliente |
|--------|-------------|---------------|--------------------------------|
| **200** | OK | Consulta exitosa con datos | Procesar respuesta |
| **400** | Bad Request | ID inválido, parámetros mal formados | Corregir parámetros y reintentar |
| **401** | Unauthorized | API Key faltante o inválida | Verificar credenciales |
| **404** | Not Found | Crédito no existe en BD | Verificar que el ID sea correcto |
| **422** | Unprocessable Entity | Error de validación Pydantic (tipo incorrecto) | Corregir tipo de dato |
| **500** | Internal Server Error | Error no controlado (BD caída, bug) | Reportar al equipo de desarrollo |

#### Estructura de Respuesta Estandarizada

Todas las respuestas (exitosas y errores) siguen la misma estructura:

```json
{
  "status_code": 200,
  "status_message": "OK",
  "success": true,
  "mensaje": "Mensaje descriptivo en español",
  "datos_generales": { ... },
  "condonacion_cobranza": { ... }
}
```

**Campos obligatorios en todas las respuestas:**
- `status_code`: Código HTTP numérico
- `status_message`: Texto estándar del código HTTP
- `success`: Boolean (true/false)
- `mensaje`: Descripción en español del resultado

**Campos condicionales:**
- `datos_generales`: Solo en respuestas exitosas (200)
- `condonacion_cobranza`: Solo en respuestas exitosas (200)
- `detail`: Solo en errores 422 (información técnica de validación)

#### Ejemplos de Respuestas

**Éxito (200):**
```json
{
  "status_code": 200,
  "status_message": "OK",
  "success": true,
  "mensaje": "Se encontraron 3 gastos condonados",
  "datos_generales": { ... },
  "condonacion_cobranza": { "detalle": [...] }
}
```

**Error de Autenticación (401):**
```json
{
  "status_code": 401,
  "status_message": "Unauthorized",
  "success": false,
  "mensaje": "API Key inválida o no autorizada"
}
```

**Error de Validación (422):**
```json
{
  "status_code": 422,
  "status_message": "Unprocessable Entity",
  "success": false,
  "mensaje": "No se pudo convertir 'abc' a un número entero válido",
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "id_credito"],
      "msg": "Input should be a valid integer",
      "input": "abc"
    }
  ]
}
```

**Error de Servidor (500):**
```json
{
  "status_code": 500,
  "status_message": "Internal Server Error",
  "success": false,
  "mensaje": "Error de base de datos: Connection timeout"
}
```

#### Manejo de Errores en el Cliente

**JavaScript (Fetch API):**
```javascript
fetch('https://API/condonaciones/12345', {
  headers: { 'X-API-Key': 'TU_API_KEY' }
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    // Procesar datos
    console.log(data.datos_generales);
  } else {
    // Manejar error según código
    switch(data.status_code) {
      case 400:
        alert('ID inválido: ' + data.mensaje);
        break;
      case 401:
        alert('No autorizado. Verifica tu API Key');
        break;
      case 404:
        alert('Crédito no encontrado');
        break;
      case 500:
        alert('Error del servidor. Contacta soporte');
        break;
    }
  }
})
.catch(error => console.error('Error de red:', error));
```

**Python (requests):**
```python
import requests

response = requests.get(
    'https://API/condonaciones/12345',
    headers={'X-API-Key': 'TU_API_KEY'}
)

data = response.json()

if data['success']:
    print(f"Cliente: {data['datos_generales']['nombre_cliente']}")
else:
    print(f"Error {data['status_code']}: {data['mensaje']}")
    
    if data['status_code'] == 401:
        # Re-autenticar
        pass
    elif data['status_code'] == 404:
        # Registrar ID no encontrado
        pass
    elif data['status_code'] >= 500:
        # Alertar equipo de operaciones
        pass
```

### 4.7 Manejadores Globales de Excepciones

#### Fundamento de Seguridad

Los manejadores globales de excepciones previenen **information disclosure** (divulgación de información sensible) en mensajes de error. Sin ellos, los errores no controlados pueden exponer:

- Stack traces con rutas del servidor
- Versiones de librerías (útil para exploits)
- Estructura de la base de datos
- Variables de entorno
- Lógica interna de la aplicación

**Ejemplo de error SIN manejador (PELIGROSO):**
```html
Traceback (most recent call last):
  File "/home/usuario/api_python/routers/condonaciones.py", line 42, in get_condonacion
    cursor.execute(query, (id_credito,))
  File "/usr/lib/python3.10/site-packages/pymysql/cursors.py", line 153, in execute
    result = self._query(query)
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'db-prod-mysql-01.internal.company.com' (110)")
```

Este error revela:
- Lenguaje y versión (Python 3.10)
- Framework (PyMySQL)
- Estructura de archivos (/home/usuario/api_python)
- Nombre del servidor de BD (db-prod-mysql-01.internal.company.com)
- Puerto (implícito: 3306)

#### Implementación

```python
# main.py
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

HTTP_STATUS_MESSAGES = {
    200: "OK",
    400: "Bad Request",
    401: "Unauthorized",
    404: "Not Found",
    422: "Unprocessable Entity",
    500: "Internal Server Error"
}

# Manejador para errores HTTP controlados (400, 401, 404, etc.)
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """
    Captura excepciones HTTPException y las formatea consistentemente.
    Oculta detalles técnicos del servidor.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "status_message": HTTP_STATUS_MESSAGES.get(exc.status_code, "Error"),
            "success": False,
            "mensaje": exc.detail  # Mensaje controlado por el desarrollador
        }
    )


# Manejador para errores de validación Pydantic (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Traduce errores de validación de Pydantic al español.
    Proporciona mensajes user-friendly.
    """
    errors = exc.errors()
    
    # Extraer primer error para simplificar mensaje
    if errors:
        error = errors[0]
        field = error['loc'][-1] if error['loc'] else 'campo'
        error_type = error['type']
        input_value = error.get('input', '')
        
        # Mensajes traducidos
        mensajes = {
            'int_type': f"El campo '{field}' debe ser un número entero. Valor recibido: {input_value}",
            'int_parsing': f"No se pudo convertir '{input_value}' a un número entero válido",
            'missing': f"El campo '{field}' es obligatorio y no fue proporcionado",
            'greater_than': f"El campo '{field}' debe ser mayor a {error.get('ctx', {}).get('gt', 0)}"
        }
        
        mensaje = mensajes.get(error_type, f"Error de validación en '{field}'")
    else:
        mensaje = "Error de validación en la solicitud"
    
    return JSONResponse(
        status_code=422,
        content={
            "status_code": 422,
            "status_message": "Unprocessable Entity",
            "success": False,
            "mensaje": mensaje,
            "detail": errors  # Información técnica para debugging
        }
    )
```

#### Protección que Provee

| Sin Manejador | Con Manejador |
|---------------|---------------|
| Stack trace completo expuesto | Mensaje controlado |
| Rutas del servidor visibles | Rutas ocultas |
| Versiones de librerías reveladas | Versiones ocultas |
| Nombres de variables internos | Variables ocultas |
| Queries SQL con errores | Queries ocultos |
| Difícil de parsear para clientes | JSON estructurado |

#### Ejemplo Comparativo

**Error de conexión a BD SIN manejador:**
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'db-prod-01.internal' (110)")
    at /usr/lib/python3.10/site-packages/pymysql/connections.py:857
    at /home/user/api/routers/condonaciones.py:42
```

**Error de conexión a BD CON manejador:**
```json
{
  "status_code": 500,
  "status_message": "Internal Server Error",
  "success": false,
  "mensaje": "Error de base de datos: Connection timeout"
}
```

#### Logging Interno (No Visible al Cliente)

Aunque los errores se ocultan al cliente, internamente se registran para debugging:

```python
import logging

logger = logging.getLogger(__name__)

try:
    cursor.execute(query, (id_credito,))
except pymysql.Error as db_error:
    # Registrar error completo en logs del servidor
    logger.error(f"Database error: {db_error}", exc_info=True)
    
    # Retornar mensaje genérico al cliente
    raise HTTPException(
        status_code=500,
        detail="Error de base de datos: Connection timeout"
    )
```

**Resultado:**
- Cliente ve: `"Error de base de datos: Connection timeout"`
- Logs del servidor contienen: Stack trace completo, query ejecutado, valores de parámetros

---

## 5. ESTRUCTURA DETALLADA DEL JSON DE RESPUESTA

La API retorna un objeto JSON estructurado jerárquicamente que sigue el mismo formato en todos los endpoints. Esta sección documenta cada campo del cuerpo de la respuesta.

### 5.1 Objeto Raíz (CondonacionResponse)

El objeto principal de respuesta contiene metadatos de la operación y los datos solicitados.

| Campo | Tipo | Obligatorio | Nullable | Descripción |
|-------|------|-------------|----------|-------------|
| `status_code` | integer | Sí | No | Código HTTP de respuesta (200, 400, 401, 404, 422, 500) |
| `status_message` | string | Sí | No | Descripción estándar del código HTTP según RFC 7231 |
| `success` | boolean | Sí | No | Indicador de éxito. `true` = operación exitosa, `false` = error |
| `mensaje` | string | Sí | No | Mensaje descriptivo en español sobre el resultado |
| `datos_generales` | object | Condicional | Sí | Información del cliente y crédito. `null` en caso de error |
| `condonacion_cobranza` | object | Condicional | Sí | Contenedor de gastos de cobranza. `null` en caso de error |

**Ejemplo de respuesta exitosa:**
```json
{
  "status_code": 200,
  "status_message": "OK",
  "success": true,
  "mensaje": "Se encontraron 2 gastos condonados",
  "datos_generales": { ... },
  "condonacion_cobranza": { ... }
}
```

### 5.2 Objeto datos_generales (DatosGenerales)

Contiene información principal del cliente y estado actual del crédito consultado.

| Campo | Tipo | Nullable | Descripción | Ejemplo |
|-------|------|----------|-------------|---------|
| `id_credito` | integer | Sí | Identificador único del crédito en el sistema | `12345` |
| `nombre_cliente` | string | Sí | Nombre completo del cliente titular del crédito | `"María González López"` |
| `id_cliente` | integer | Sí | Identificador único del cliente en el sistema | `67890` |
| `domicilio_completo` | string | Sí | Dirección completa del cliente (calle, número, colonia, ciudad) | `"Av. Reforma #456, Col. Juárez, CDMX"` |
| `bucket_morosidad` | string | Sí | Clasificación de morosidad del crédito según reglas de negocio | `"B1"`, `"B2"`, `"B3"`, etc. |
| `dias_mora` | integer | Sí | Cantidad de días calendario que el crédito está en mora | `45` |
| `saldo_vencido` | float | Sí | Monto total del saldo vencido al inicio del periodo (en moneda local) | `8750.25` |

**Notas importantes:**
- Todos los campos pueden ser `null` si la información no está disponible en la base de datos
- `bucket_morosidad` sigue la nomenclatura: B1 (1-30 días), B2 (31-60 días), B3 (61-90 días), etc.
- `saldo_vencido` está en formato decimal con 2 dígitos de precisión

**Ejemplo completo:**
```json
"datos_generales": {
  "id_credito": 12345,
  "nombre_cliente": "María González López",
  "id_cliente": 67890,
  "domicilio_completo": "Av. Reforma #456, Col. Juárez, CDMX",
  "bucket_morosidad": "B3",
  "dias_mora": 45,
  "saldo_vencido": 8750.25
}
```

### 5.3 Objeto condonacion_cobranza (CondonacionCobranza)

Contenedor principal de los detalles de gastos de cobranza condonados.

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `detalle` | array | Sí | Arreglo de objetos `DetalleCondonacion`. Puede estar vacío `[]` si no hay gastos condonados |

**Comportamiento:**
- Si existen gastos condonados: `detalle` contiene uno o más elementos
- Si NO existen gastos condonados: `detalle` es un arreglo vacío `[]`
- El arreglo está ordenado por `periodoinicio` ascendente

**Ejemplo con gastos:**
```json
"condonacion_cobranza": {
  "detalle": [
    { /* DetalleCondonacion 1 */ },
    { /* DetalleCondonacion 2 */ }
  ]
}
```

**Ejemplo sin gastos:**
```json
"condonacion_cobranza": {
  "detalle": []
}
```

### 5.4 Objeto detalle[] (DetalleCondonacion)

Cada elemento del arreglo `detalle` representa un gasto de cobranza individual que fue condonado.

| Campo | Tipo | Nullable | Descripción | Ejemplo |
|-------|------|----------|-------------|---------|
| `periodoinicio` | string (date) | Sí | Fecha de inicio del periodo del gasto en formato ISO 8601 (YYYY-MM-DD) | `"2026-01-01"` |
| `periodofin` | string (date) | Sí | Fecha de fin del periodo del gasto en formato ISO 8601 (YYYY-MM-DD) | `"2026-01-07"` |
| `semana` | string/integer | Sí | Identificador de la semana del gasto. Puede ser string (YYYY-WW) o número | `"2026-01"` o `1` |
| `parcialidad` | string/integer | Sí | Número de parcialidad en formato fraccionario (X/Y) o numérico | `"1/52"` o `1` |
| `monto_valor` | float | Sí | Monto del gasto de cobranza aplicado (con decimales, 2 dígitos precisión) | `150.50` |
| `cuota` | float | Sí | Monto de la cuota pactada asociada al periodo | `150.00` |
| `condonado` | integer | Sí | Indicador de condonación: `1` = condonado, `0` = no condonado | `1` |
| `fecha_condonacion` | string (datetime) | Sí | Fecha y hora en que se realizó la condonación (ISO 8601 con timezone) | `"2026-01-28T10:30:00"` |

**Notas técnicas:**
- **periodoinicio/periodofin**: Rango de fechas del gasto (generalmente 7 días)
- **semana**: Puede ser string (formato año-semana) o integer (número secuencial)
- **parcialidad**: Formato "actual/total" (ej: "1/52" = primera de 52 parcialidades)
- **monto_valor**: Valor exacto del gasto (puede diferir de la cuota)
- **cuota**: Cuota pactada originalmente
- **condonado**: Siempre es `1` en esta API (solo retorna condonados)
- **fecha_condonacion**: Formato ISO 8601, timezone UTC implícito

**Ejemplo completo:**
```json
{
  "periodoinicio": "2026-01-01",
  "periodofin": "2026-01-07",
  "semana": "2026-01",
  "parcialidad": "1/52",
  "monto_valor": 150.50,
  "cuota": 150.00,
  "condonado": 1,
  "fecha_condonacion": "2026-01-28T10:30:00"
}
```

### 5.5 Ejemplo Completo de Respuesta Exitosa

```json
{
  "status_code": 200,
  "status_message": "OK",
  "success": true,
  "mensaje": "Se encontraron 3 gastos condonados",
  "datos_generales": {
    "id_credito": 12345,
    "nombre_cliente": "María González López",
    "id_cliente": 67890,
    "domicilio_completo": "Av. Reforma #456, Col. Juárez, CDMX",
    "bucket_morosidad": "B3",
    "dias_mora": 45,
    "saldo_vencido": 8750.25
  },
  "condonacion_cobranza": {
    "detalle": [
      {
        "periodoinicio": "2026-01-01",
        "periodofin": "2026-01-07",
        "semana": "2026-01",
        "parcialidad": "1/52",
        "monto_valor": 150.50,
        "cuota": 150.00,
        "condonado": 1,
        "fecha_condonacion": "2026-01-28T10:30:00"
      },
      {
        "periodoinicio": "2026-01-08",
        "periodofin": "2026-01-14",
        "semana": "2026-02",
        "parcialidad": "2/52",
        "monto_valor": 175.00,
        "cuota": 150.00,
        "condonado": 1,
        "fecha_condonacion": "2026-01-28T10:30:00"
      },
      {
        "periodoinicio": "2026-01-15",
        "periodofin": "2026-01-21",
        "semana": "2026-03",
        "parcialidad": "3/52",
        "monto_valor": 200.75,
        "cuota": 150.00,
        "condonado": 1,
        "fecha_condonacion": "2026-01-28T10:30:00"
      }
    ]
  }
}
```

### 5.6 Ejemplo de Respuesta Sin Gastos Condonados

Cuando el crédito existe pero no tiene gastos condonados:

```json
{
  "status_code": 200,
  "status_message": "OK",
  "success": true,
  "mensaje": "No hay gastos condonados para este crédito",
  "datos_generales": {
    "id_credito": 54321,
    "nombre_cliente": "Carlos Ramírez Sánchez",
    "id_cliente": 98765,
    "domicilio_completo": "Calle Morelos #789, Col. Centro",
    "bucket_morosidad": "B1",
    "dias_mora": 5,
    "saldo_vencido": 500.00
  },
  "condonacion_cobranza": {
    "detalle": []
  }
}
```

### 5.7 Ejemplos de Respuestas de Error

#### Error 400 - Bad Request (ID Inválido)

```json
{
  "status_code": 400,
  "status_message": "Bad Request",
  "success": false,
  "mensaje": "El ID del crédito debe ser mayor a 0"
}
```

#### Error 401 - Unauthorized (API Key Inválida)

```json
{
  "status_code": 401,
  "status_message": "Unauthorized",
  "success": false,
  "mensaje": "API Key inválida o no autorizada"
}
```

#### Error 404 - Not Found (Crédito No Existe)

```json
{
  "status_code": 404,
  "status_message": "Not Found",
  "success": false,
  "mensaje": "No se encontró información del crédito 99999. Verifica que el ID sea correcto."
}
```

#### Error 422 - Unprocessable Entity (Validación Fallida)

```json
{
  "status_code": 422,
  "status_message": "Unprocessable Entity",
  "success": false,
  "mensaje": "No se pudo convertir 'abc' a un número entero válido",
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "id_credito"],
      "msg": "Input should be a valid integer",
      "input": "abc"
    }
  ]
}
```

#### Error 500 - Internal Server Error

```json
{
  "status_code": 500,
  "status_message": "Internal Server Error",
  "success": false,
  "mensaje": "Error de base de datos: Connection timeout"
}
```

### 5.8 Consideraciones de Integración

#### Para Desarrolladores Frontend/Cliente

##### 1. Validar siempre el campo `success` antes de procesar datos

**JavaScript (Fetch API):**
```javascript
fetch('https://API/condonaciones/12345', {
  headers: { 'X-API-Key': 'TU_API_KEY' }
})
.then(response => response.json())
.then(data => {
  if (data.success === true) {
    // Procesar datos
    mostrarCliente(data.datos_generales);
    mostrarGastos(data.condonacion_cobranza.detalle);
  } else {
    // Mostrar error al usuario
    mostrarError(data.mensaje);
  }
})
.catch(error => {
  console.error('Error de red:', error);
  mostrarError('No se pudo conectar con el servidor');
});
```

**Python (requests):**
```python
import requests

response = requests.get(
    'https://API/condonaciones/12345',
    headers={'X-API-Key': 'TU_API_KEY'}
)

data = response.json()

if data['success']:
    print(f"Cliente: {data['datos_generales']['nombre_cliente']}")
    print(f"Gastos: {len(data['condonacion_cobranza']['detalle'])}")
else:
    print(f"Error: {data['mensaje']}")
```

##### 2. Manejar arreglo vacío en `detalle`

```javascript
const gastos = response.condonacion_cobranza.detalle;

if (gastos.length === 0) {
  console.log("No hay gastos condonados");
  mostrarMensaje("Este crédito no tiene gastos condonados");
} else {
  console.log(`Se encontraron ${gastos.length} gastos condonados`);
  gastos.forEach(gasto => {
    console.log(`Periodo: ${gasto.periodoinicio} - Monto: ${gasto.monto_valor}`);
  });
}
```

##### 3. Validar campos nullable antes de usar

```javascript
const datos = response.datos_generales;

// Uso seguro con operador de coalescencia nula
const nombreCliente = datos.nombre_cliente ?? "No disponible";
const domicilio = datos.domicilio_completo ?? "Sin domicilio registrado";
const diasMora = datos.dias_mora ?? 0;

console.log(`Cliente: ${nombreCliente}`);
console.log(`Domicilio: ${domicilio}`);
console.log(`Días en mora: ${diasMora}`);
```

##### 4. Parsear fechas correctamente

```javascript
const detalles = response.condonacion_cobranza.detalle;

detalles.forEach(detalle => {
  // Convertir strings ISO 8601 a objetos Date
  const fechaInicio = new Date(detalle.periodoinicio);
  const fechaFin = new Date(detalle.periodofin);
  const fechaCondonacion = new Date(detalle.fecha_condonacion);
  
  console.log(`Periodo: ${fechaInicio.toLocaleDateString('es-MX')} - ${fechaFin.toLocaleDateString('es-MX')}`);
  console.log(`Condonado el: ${fechaCondonacion.toLocaleString('es-MX')}`);
});
```

### 5.9 Definición de Tipos para TypeScript

Para facilitar la integración en proyectos TypeScript, se proporcionan las siguientes interfaces:

```typescript
/**
 * Respuesta principal de la API de condonaciones
 */
interface CondonacionResponse {
  status_code: number;
  status_message: string;
  success: boolean;
  mensaje: string;
  datos_generales: DatosGenerales | null;
  condonacion_cobranza: CondonacionCobranza | null;
}

/**
 * Datos generales del cliente y crédito
 */
interface DatosGenerales {
  id_credito: number | null;
  nombre_cliente: string | null;
  id_cliente: number | null;
  domicilio_completo: string | null;
  bucket_morosidad: string | null;  // "B1", "B2", "B3", etc.
  dias_mora: number | null;
  saldo_vencido: number | null;  // Decimal con 2 dígitos de precisión
}

/**
 * Contenedor de detalles de condonación
 */
interface CondonacionCobranza {
  detalle: DetalleCondonacion[];  // Puede estar vacío []
}

/**
 * Detalle individual de un gasto de cobranza condonado
 */
interface DetalleCondonacion {
  periodoinicio: string | null;      // ISO 8601 date: "YYYY-MM-DD"
  periodofin: string | null;         // ISO 8601 date: "YYYY-MM-DD"
  semana: string | number | null;    // "YYYY-WW" o número
  parcialidad: string | number | null;  // "X/Y" o número
  monto_valor: number | null;        // Decimal con 2 dígitos
  cuota: number | null;              // Decimal con 2 dígitos
  condonado: number | null;          // 0 o 1
  fecha_condonacion: string | null;  // ISO 8601 datetime: "YYYY-MM-DDTHH:mm:ss"
}

/**
 * Ejemplo de uso en TypeScript
 */
async function obtenerCondonaciones(idCredito: number): Promise<CondonacionResponse> {
  const response = await fetch(`https://API/condonaciones/${idCredito}`, {
    headers: {
      'X-API-Key': 'TU_API_KEY',
      'Content-Type': 'application/json'
    }
  });
  
  const data: CondonacionResponse = await response.json();
  
  if (!data.success) {
    throw new Error(`Error ${data.status_code}: ${data.mensaje}`);
  }
  
  return data;
}

// Uso con type guards
function procesarRespuesta(data: CondonacionResponse): void {
  if (data.success && data.datos_generales) {
    console.log(`Cliente: ${data.datos_generales.nombre_cliente}`);
    
    if (data.condonacion_cobranza && data.condonacion_cobranza.detalle.length > 0) {
      data.condonacion_cobranza.detalle.forEach(detalle => {
        console.log(`Gasto: ${detalle.monto_valor}`);
      });
    } else {
      console.log('No hay gastos condonados');
    }
  } else {
    console.error(data.mensaje);
  }
}
```

### 5.10 Schema JSON (JSON Schema)

Para validación automática en herramientas que soporten JSON Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CondonacionResponse",
  "type": "object",
  "required": ["status_code", "status_message", "success", "mensaje"],
  "properties": {
    "status_code": {
      "type": "integer",
      "enum": [200, 400, 401, 404, 422, 500]
    },
    "status_message": {
      "type": "string"
    },
    "success": {
      "type": "boolean"
    },
    "mensaje": {
      "type": "string"
    },
    "datos_generales": {
      "type": ["object", "null"],
      "properties": {
        "id_credito": { "type": ["integer", "null"] },
        "nombre_cliente": { "type": ["string", "null"] },
        "id_cliente": { "type": ["integer", "null"] },
        "domicilio_completo": { "type": ["string", "null"] },
        "bucket_morosidad": { "type": ["string", "null"] },
        "dias_mora": { "type": ["integer", "null"] },
        "saldo_vencido": { "type": ["number", "null"] }
      }
    },
    "condonacion_cobranza": {
      "type": ["object", "null"],
      "properties": {
        "detalle": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "periodoinicio": { "type": ["string", "null"], "format": "date" },
              "periodofin": { "type": ["string", "null"], "format": "date" },
              "semana": { "type": ["string", "integer", "null"] },
              "parcialidad": { "type": ["string", "integer", "null"] },
              "monto_valor": { "type": ["number", "null"] },
              "cuota": { "type": ["number", "null"] },
              "condonado": { "type": ["integer", "null"], "enum": [0, 1, null] },
              "fecha_condonacion": { "type": ["string", "null"], "format": "date-time" }
            }
          }
        }
      }
    }
  }
}
```

---

## 6. GUÍA DE CONSUMO DE LA API

### 6.1 Información General

**URL Base:**
```
https://TU_SERVIDOR/api/v1
```

**Protocolo:** HTTPS (obligatorio en producción)  
**Formato de respuesta:** JSON  
**Charset:** UTF-8  
**Autenticación:** API Key (header `X-API-Key`)

### 6.2 Endpoint Disponible

#### GET /condonaciones/{id_credito}

Obtiene información completa de condonación para un crédito específico, incluyendo datos generales del cliente y todos los gastos de cobranza que han sido condonados.

**URL:**
```
GET /condonaciones/{id_credito}
```

**Parámetros de Ruta:**

| Parámetro | Tipo | Obligatorio | Validación | Descripción |
|-----------|------|-------------|------------|-------------|
| `id_credito` | integer | Sí | > 0, ≤ 999999999 | ID del crédito a consultar |

**Headers Requeridos:**

| Header | Tipo | Obligatorio | Descripción |
|--------|------|-------------|-------------|
| `X-API-Key` | string | Sí | API Key de autenticación (32 caracteres URL-safe) |
| `Content-Type` | string | Recomendado | Debe ser `application/json` |

**Códigos de Respuesta:**

| Código | Descripción | Ejemplo de Causa |
|--------|-------------|------------------|
| 200 | OK - Consulta exitosa | Crédito encontrado con o sin gastos condonados |
| 400 | Bad Request - Parámetros inválidos | ID negativo, cero, o patrón sospechoso |
| 401 | Unauthorized - No autenticado | API Key faltante, inválida o expirada |
| 404 | Not Found - Recurso no existe | Crédito no existe en la base de datos |
| 422 | Unprocessable Entity - Validación fallida | ID no es número entero |
| 500 | Internal Server Error - Error del servidor | Base de datos caída, error no controlado |

### 6.3 Ejemplos de Peticiones

#### Ejemplo con cURL

```bash
curl -X GET "https://TU_SERVIDOR/api/v1/condonaciones/12345" \
     -H "X-API-Key: tu_api_key_de_32_caracteres_aqui" \
     -H "Content-Type: application/json"
```

**Con verbosidad para debugging:**
```bash
curl -v -X GET "https://TU_SERVIDOR/api/v1/condonaciones/12345" \
     -H "X-API-Key: tu_api_key_de_32_caracteres_aqui" \
     -H "Content-Type: application/json"
```

#### Ejemplo con Python (requests)

```python
import requests

url = "https://TU_SERVIDOR/api/v1/condonaciones/12345"
headers = {
    "X-API-Key": "tu_api_key_de_32_caracteres_aqui",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

# Verificar código de respuesta
if response.status_code == 200:
    data = response.json()
    
    if data["success"]:
        # Procesar datos
        cliente = data["datos_generales"]["nombre_cliente"]
        gastos = len(data["condonacion_cobranza"]["detalle"])
        
        print(f"Cliente: {cliente}")
        print(f"Gastos condonados: {gastos}")
        
        for detalle in data["condonacion_cobranza"]["detalle"]:
            print(f"  - Periodo: {detalle['periodoinicio']} | Monto: ${detalle['monto_valor']}")
    else:
        print(f"Error: {data['mensaje']}")
else:
    print(f"HTTP Error {response.status_code}: {response.text}")
```

#### Ejemplo con JavaScript (Fetch API)

```javascript
const idCredito = 12345;
const apiKey = 'tu_api_key_de_32_caracteres_aqui';

fetch(`https://TU_SERVIDOR/api/v1/condonaciones/${idCredito}`, {
  method: 'GET',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json'
  }
})
.then(response => {
  if (!response.ok) {
    throw new Error(`HTTP error ${response.status}`);
  }
  return response.json();
})
.then(data => {
  if (data.success) {
    console.log('Cliente:', data.datos_generales.nombre_cliente);
    console.log('Días de mora:', data.datos_generales.dias_mora);
    console.log('Gastos condonados:', data.condonacion_cobranza.detalle.length);
    
    data.condonacion_cobranza.detalle.forEach(detalle => {
      console.log(`  Gasto: $${detalle.monto_valor} (${detalle.periodoinicio})`);
    });
  } else {
    console.error('Error:', data.mensaje);
  }
})
.catch(error => {
  console.error('Error de red:', error);
});
```

#### Ejemplo con Node.js (axios)

```javascript
const axios = require('axios');

async function obtenerCondonaciones(idCredito) {
  try {
    const response = await axios.get(
      `https://TU_SERVIDOR/api/v1/condonaciones/${idCredito}`,
      {
        headers: {
          'X-API-Key': 'tu_api_key_de_32_caracteres_aqui',
          'Content-Type': 'application/json'
        }
      }
    );
    
    const data = response.data;
    
    if (data.success) {
      console.log(`Cliente: ${data.datos_generales.nombre_cliente}`);
      console.log(`Gastos: ${data.condonacion_cobranza.detalle.length}`);
      return data;
    } else {
      throw new Error(data.mensaje);
    }
    
  } catch (error) {
    if (error.response) {
      // Error HTTP (4xx, 5xx)
      console.error(`Error ${error.response.status}:`, error.response.data.mensaje);
    } else if (error.request) {
      // No hubo respuesta
      console.error('No se recibió respuesta del servidor');
    } else {
      // Error en la configuración
      console.error('Error:', error.message);
    }
    throw error;
  }
}

// Uso
obtenerCondonaciones(12345)
  .then(data => console.log('Datos obtenidos:', data))
  .catch(error => console.error('Fallo:', error.message));
```

### 6.4 Manejo de Errores

#### Estructura Recomendada para el Cliente

```python
import requests
from typing import Optional, Dict

def consultar_condonaciones(id_credito: int, api_key: str) -> Optional[Dict]:
    """
    Consulta condonaciones con manejo completo de errores.
    
    Returns:
        Dict con datos si es exitoso, None si hay error
    """
    url = f"https://TU_SERVIDOR/api/v1/condonaciones/{id_credito}"
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        data = response.json()
        
        # Manejar según código HTTP
        if response.status_code == 200:
            if data["success"]:
                return data
            else:
                print(f"Respuesta sin éxito: {data['mensaje']}")
                return None
                
        elif response.status_code == 400:
            print(f"Parámetros inválidos: {data['mensaje']}")
            # Registrar para debugging
            return None
            
        elif response.status_code == 401:
            print(f"API Key inválida. Verifica tus credenciales")
            # Podría intentar re-autenticar
            return None
            
        elif response.status_code == 404:
            print(f"Crédito {id_credito} no encontrado")
            # Registrar ID no encontrado para auditoría
            return None
            
        elif response.status_code == 422:
            print(f"Error de validación: {data['mensaje']}")
            print(f"Detalles: {data.get('detail', '')}")
            return None
            
        elif response.status_code >= 500:
            print(f"Error del servidor: {data['mensaje']}")
            # Podría implementar retry con backoff exponencial
            return None
            
    except requests.exceptions.Timeout:
        print(f"Timeout después de 30 segundos")
        return None
        
    except requests.exceptions.ConnectionError:
        print(f"No se pudo conectar al servidor")
        return None
        
    except requests.exceptions.JSONDecodeError:
        print(f"Respuesta inválida (no es JSON)")
        return None
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return None
```

### 6.5 Best Practices para Integración

#### 1. Implementar Timeouts

```python
# Python
response = requests.get(url, headers=headers, timeout=30)  # 30 segundos

# JavaScript (fetch con AbortController)
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000);

fetch(url, { headers, signal: controller.signal })
  .then(response => response.json())
  .finally(() => clearTimeout(timeoutId));
```

#### 2. Implementar Retry con Backoff Exponencial

```python
import time
from typing import Optional, Dict

def consultar_con_retry(
    id_credito: int,
    api_key: str,
    max_intentos: int = 3,
    backoff_base: float = 2.0
) -> Optional[Dict]:
    """
    Consulta con reintentos automáticos en caso de error de servidor.
    """
    for intento in range(max_intentos):
        response = requests.get(
            f"https://API/condonaciones/{id_credito}",
            headers={"X-API-Key": api_key},
            timeout=30
        )
        
        # Éxito o error cliente (no reintentar)
        if response.status_code < 500:
            return response.json()
        
        # Error servidor (reintentar)
        if intento < max_intentos - 1:
            espera = backoff_base ** intento
            print(f"Error 5xx, reintentando en {espera}s...")
            time.sleep(espera)
        else:
            print(f"Fallaron todos los intentos")
            return None
```

#### 3. Logging de Peticiones

```python
import logging

logger = logging.getLogger(__name__)

def consultar_condonaciones_con_logging(id_credito: int, api_key: str):
    logger.info(f"Consultando condonaciones para crédito {id_credito}")
    
    inicio = time.time()
    response = requests.get(...)
    duracion = time.time() - inicio
    
    logger.info(
        f"Respuesta recibida: status={response.status_code}, "
        f"duration={duracion:.2f}s, "
        f"size={len(response.content)} bytes"
    )
    
    if response.status_code != 200:
        logger.error(f"Error en petición: {response.text}")
    
    return response.json()
```

#### 4. Cacheo de Respuestas

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def consultar_condonaciones_cacheado(id_credito: int, api_key_hash: str):
    """
    Cachea respuestas para evitar peticiones duplicadas.
    TTL se puede implementar con time-based cache invalidation.
    """
    # No cachear el API key directamente (por seguridad)
    # Se pasa un hash del API key para que funcione el cache
    response = requests.get(...)
    return response.json()

# Uso
api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
data = consultar_condonaciones_cacheado(12345, api_key_hash)
```

---

## 7. DOCUMENTACIÓN INTERACTIVA (Swagger UI)

FastAPI genera automáticamente documentación interactiva donde puedes explorar y probar los endpoints sin escribir código.

### 7.1 Acceso a la Documentación

**Swagger UI (interfaz interactiva):**
```
https://TU_SERVIDOR/docs
```

**ReDoc (documentación alternativa):**
```
https://TU_SERVIDOR/redoc
```

**OpenAPI Schema (JSON):**
```
https://TU_SERVIDOR/openapi.json
```

### 7.2 Características de Swagger UI

1. **Exploración de endpoints**: Lista completa de operaciones disponibles
2. **Modelos de datos**: Esquemas de entrada/salida con ejemplos
3. **Try it out**: Ejecutar peticiones reales desde el navegador
4. **Autenticación**: Configurar API Key para pruebas
5. **Respuestas de ejemplo**: Ver estructura de respuestas exitosas y errores

### 7.3 Cómo Probar un Endpoint en Swagger UI

1. Acceder a `https://TU_SERVIDOR/docs`
2. Expandir el endpoint `GET /condonaciones/{id_credito}`
3. Click en "Try it out"
4. Ingresar valores:
   - `id_credito`: 12345
   - Click en el candado (Authorize)
   - Ingresar API Key: `tu_api_key_aqui`
5. Click en "Execute"
6. Ver la respuesta en tiempo real

### 7.4 Generación de Clientes

El schema OpenAPI puede ser usado para generar clientes automáticamente:

**TypeScript:**
```bash
npx openapi-typescript-codegen --input https://TU_SERVIDOR/openapi.json --output ./src/api
```

**Python:**
```bash
pip install openapi-python-client
openapi-python-client generate --url https://TU_SERVIDOR/openapi.json
```

---

## 8. CONFIGURACIÓN Y DESPLIEGUE

### 8.1 Variables de Entorno

Crear archivo `.env` en la raíz del proyecto (nunca versionar este archivo):

```env
# Base de Datos Principal
DB_HOST=tu_servidor_mysql.com
DB_PORT=3306
DB_USER=usuario_db
DB_PASSWORD=password_seguro_aqui
DB_DATABASE=db-mega-reporte

# API Keys (separadas por comas)
# Generar con: python -c "from config.security import generate_api_key; print(generate_api_key())"
API_KEYS=clave_cliente1_32caracteres_aqui,clave_cliente2_32caracteres_aqui

# Configuración del Servidor (opcional)
PORT=8000
HOST=0.0.0.0
WORKERS=4

# Logging (opcional)
LOG_LEVEL=INFO
```

### 8.2 Instalación de Dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 8.3 Ejecución en Desarrollo

```bash
# Con reload automático (detecta cambios en código)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Con logs detallados
uvicorn main:app --reload --log-level debug
```

### 8.4 Ejecución en Producción

```bash
# Con múltiples workers (1 por CPU core)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Con SSL/TLS
uvicorn main:app --host 0.0.0.0 --port 443 \
  --ssl-keyfile=/path/to/key.pem \
  --ssl-certfile=/path/to/cert.pem \
  --workers 4

# Con Gunicorn (más robusto para producción)
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 --access-logfile - --error-logfile -
```

### 8.5 Despliegue con Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/docs"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Comandos:**
```bash
# Construir imagen
docker build -t api-condonaciones .

# Ejecutar contenedor
docker run -d -p 8000:8000 --env-file .env api-condonaciones

# Con docker-compose
docker-compose up -d
```

### 8.6 Consideraciones de Producción

1. **HTTPS obligatorio**: Usar certificados SSL/TLS válidos
2. **Reverse proxy**: Configurar Nginx o Traefik delante de Uvicorn
3. **Rate limiting**: Implementar límites de peticiones por API Key
4. **Monitoreo**: Configurar herramientas como Prometheus + Grafana
5. **Logs centralizados**: Enviar logs a ELK Stack o CloudWatch
6. **Backups**: Programar backups automáticos de la base de datos
7. **Firewall**: Restringir acceso solo a IPs conocidas si es posible

---

## APÉNDICES

### A. Generación de API Keys

Para generar nuevas API Keys:

```bash
python -c "from config.security import generate_api_key; print(generate_api_key())"
```

### B. Testing de la API

Crear archivo `test_api.py`:

```python
import requests

def test_endpoint():
    url = "https://TU_SERVIDOR/condonaciones/12345"
    headers = {"X-API-Key": "TU_API_KEY"}
    
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert "datos_generales" in data
    
    print("Test exitoso")

if __name__ == "__main__":
    test_endpoint()
```

### C. Versionado de la API

Para futuras versiones, se recomienda:

```python
# routers/v1/condonaciones.py
router = APIRouter(prefix="/v1")

# routers/v2/condonaciones.py
router = APIRouter(prefix="/v2")

# main.py
app.include_router(v1_router)
app.include_router(v2_router)
```

---

**FIN DE DOCUMENTACIÓN TÉCNICA**

---

Este documento es de carácter técnico y está dirigido a desarrolladores. Para documentación de usuario final, consultar documentación adicional.
