# MANUAL TÉCNICO DE CONSUMO PARA LA API DE CONDONACIONES

---

## Información del Documento

| Campo | Valor |
|-------|-------|
| **Fecha de elaboración** | 30 / Enero / 2026 |
| **Fecha de actualización** | 30 / Enero / 2026 |
| **No. de revisión** | 1.0 |
| **Versión** | 1.0.0 |
| **Responsable** | Desarrollo de Software |

---

## Tabla de Contenido

1. [Objetivo](#objetivo)
2. [Descripción General](#descripción-general)
3. [Endpoint Principal](#endpoint-principal)
4. [Autenticación](#autenticación)
5. [Parámetros de Entrada](#parámetros-de-entrada)
6. [Respuesta Exitosa (HTTP 200)](#respuesta-exitosa-http-200)
7. [Códigos de Estado HTTP](#códigos-de-estado-http)
8. [Prueba Técnica desde Postman](#prueba-técnica-desde-postman)
9. [Consideraciones Técnicas](#consideraciones-técnicas)

---

## Objetivo

Permitir consultar los **gastos de cobranza condonados** de un crédito específico mediante su `id_credito`. Esta API devuelve información detallada del cliente, estado del crédito y el historial completo de condonaciones realizadas, facilitando la integración con sistemas externos de gestión de cartera y cobranza.

---

## Descripción General

Esta API REST proporciona acceso seguro y estructurado a la información de condonaciones de gastos de cobranza. Fue diseñada bajo arquitectura limpia utilizando **FastAPI**, con separación clara de responsabilidades y validación robusta de datos.

**Características principales:**
- Autenticación basada en API Key personalizada
- Respuestas estandarizadas con estructura JSON consistente
- Validación automática de parámetros con mensajes de error en español
- Consultas optimizadas a base de datos MySQL
- Documentación interactiva automática (Swagger/OpenAPI)

---

## Endpoint Principal

### Consultar Condonaciones por ID de Crédito

| Propiedad | Valor |
|-----------|-------|
| **Método HTTP** | `GET` |
| **Ruta** | `/api/condonaciones/{id_credito}` |
| **URL Base** | `http://localhost:8000` (desarrollo) |
| **URL Completa** | `http://localhost:8000/api/condonaciones/{id_credito}` |
| **Protocolo** | HTTP/HTTPS |
| **Content-Type** | `application/json` |
| **Autenticación** | API Key en header `X-API-Key` |

### Estructura de la URL

```
http://localhost:8000/api/condonaciones/{id_credito}
                       └─ Path Parameter (requerido)
```

**Ejemplo:**
```
GET http://localhost:8000/api/condonaciones/12345
```

---

## Autenticación

La API utiliza un sistema de autenticación basado en **API Key** que debe enviarse en cada solicitud.

### Header de Autenticación

```http
X-API-Key: {TU_API_KEY}
```

### Ejemplo de Header Completo

```http
X-API-Key: sparta_ledger_2026_secure_key_v1
Content-Type: application/json
```

### ⚠️ Notas Importantes

- El API Key es **obligatorio** en todas las solicitudes
- Si el API Key es inválido o falta, recibirás un error `401 Unauthorized`
- Los API Keys son validados contra una lista segura configurada en el servidor
- **Para obtener tu API Key de producción**, contacta al equipo de desarrollo

### Configuración de API Keys

Los API Keys válidos se configuran en el archivo `.env`:

```env
API_KEYS=sparta_ledger_2026_secure_key_v1,otro_key_valido
```

---

## Parámetros de Entrada

### Path Parameters

| Parámetro | Tipo | Requerido | Descripción | Validaciones |
|-----------|------|-----------|-------------|--------------|
| `id_credito` | `integer` | ✅ Sí | Identificador único del crédito a consultar | - Debe ser un número entero<br>- Debe ser mayor a 0<br>- No puede estar vacío |

### Ejemplo de URL con Parámetro

```
GET /api/condonaciones/12345
                        └─ id_credito = 12345
```

### Validaciones Aplicadas

1. **Tipo de dato**: El `id_credito` debe ser un número entero
2. **Valor mínimo**: Debe ser mayor a 0
3. **Formato**: No se aceptan valores negativos, decimales, texto o nulos

### Ejemplos de Valores

✅ **Válidos:**
- `12345`
- `1`
- `999999`

❌ **Inválidos:**
- `0` (menor o igual a 0)
- `-123` (negativo)
- `12.5` (decimal)
- `"abc"` (texto)
- `null` (nulo)

---

## Respuesta Exitosa (HTTP 200)

### Estructura de la Respuesta

```json
{
  "status_code": 200,
  "status_message": "OK",
  "success": true,
  "mensaje": "Datos obtenidos correctamente",
  "datos_generales": {
    "id_credito": 12345,
    "nombre_cliente": "Juan Pérez García",
    "id_cliente": 67890,
    "domicilio_completo": "Calle Principal #123, Col. Centro",
    "bucket_morosidad": "B2",
    "dias_mora": 15,
    "saldo_vencido": 3500.00
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
        "monto_valor": 150.50,
        "cuota": 150.00,
        "condonado": 1,
        "fecha_condonacion": "2026-01-28T10:30:00"
      }
    ]
  }
}
```

### Descripción de Campos

#### Nivel Superior

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `status_code` | `integer` | Código HTTP de la respuesta (200 = éxito) |
| `status_message` | `string` | Descripción del código HTTP ("OK", "Bad Request", etc.) |
| `success` | `boolean` | Indica si la operación fue exitosa (`true`) o no (`false`) |
| `mensaje` | `string` | Mensaje descriptivo del resultado de la operación |
| `datos_generales` | `object` | Información general del cliente y crédito |
| `condonacion_cobranza` | `object` | Contenedor de los detalles de condonación |

#### Objeto: datos_generales

| Campo | Tipo | Descripción | Puede ser nulo |
|-------|------|-------------|----------------|
| `id_credito` | `integer` | Identificador único del crédito | No |
| `nombre_cliente` | `string` | Nombre completo del cliente | Sí |
| `id_cliente` | `integer` | Identificador único del cliente | Sí |
| `domicilio_completo` | `string` | Dirección completa del cliente | Sí |
| `bucket_morosidad` | `string` | Categoría de morosidad (B1, B2, B3, etc.) | Sí |
| `dias_mora` | `integer` | Número de días en mora | Sí |
| `saldo_vencido` | `float` | Monto total del saldo vencido | Sí |

#### Objeto: condonacion_cobranza.detalle[]

| Campo | Tipo | Descripción | Puede ser nulo |
|-------|------|-------------|----------------|
| `periodoinicio` | `date` | Fecha de inicio del periodo de cobranza | Sí |
| `periodofin` | `date` | Fecha de fin del periodo de cobranza | Sí |
| `semana` | `string/integer` | Identificador de la semana | Sí |
| `parcialidad` | `string/integer` | Número de parcialidad (ej: "1/52") | Sí |
| `monto_valor` | `float` | Monto del gasto de cobranza condonado | Sí |
| `cuota` | `float` | Valor de la cuota asociada | Sí |
| `condonado` | `integer` | Marca de condonación (1 = condonado) | Sí |
| `fecha_condonacion` | `datetime` | Fecha y hora en que se realizó la condonación | Sí |

### Caso: Sin Gastos de Cobranza Condonados

Si el crédito existe pero **no tiene gastos de cobranza condonados**, la respuesta será:

```json
{
  "status_code": 200,
  "status_message": "OK",
  "success": true,
  "mensaje": "Crédito encontrado, pero no tiene gastos de cobranza condonados",
  "datos_generales": {
    "id_credito": 12345,
    "nombre_cliente": "Juan Pérez García",
    "id_cliente": 67890,
    "domicilio_completo": "Calle Principal #123, Col. Centro",
    "bucket_morosidad": "B2",
    "dias_mora": 15,
    "saldo_vencido": 3500.00
  },
  "condonacion_cobranza": {
    "detalle": []
  }
}
```

---

## Códigos de Estado HTTP

La API utiliza códigos de estado HTTP estándar para indicar el resultado de las operaciones.

| Código | Mensaje | Descripción | Cuándo Ocurre |
|--------|---------|-------------|---------------|
| **200** | OK | Solicitud exitosa | El crédito fue encontrado y se retornaron los datos (con o sin condonaciones) |
| **400** | Bad Request | Solicitud inválida | El `id_credito` es inválido (negativo, texto, decimal, etc.) |
| **401** | Unauthorized | No autenticado | API Key faltante, inválido o no autorizado |
| **404** | Not Found | No encontrado | El crédito con el `id_credito` especificado no existe en la base de datos |
| **422** | Unprocessable Entity | Entidad no procesable | Error de validación en los parámetros (formato incorrecto) |
| **500** | Internal Server Error | Error interno del servidor | Error inesperado en el servidor o base de datos |

### Ejemplos de Respuestas de Error

#### Error 400 - Bad Request

```json
{
  "status_code": 400,
  "status_message": "Bad Request",
  "success": false,
  "mensaje": "El ID de crédito debe ser mayor a 0"
}
```

#### Error 401 - Unauthorized

```json
{
  "status_code": 401,
  "status_message": "Unauthorized",
  "success": false,
  "mensaje": "API Key inválida o no autorizada"
}
```

#### Error 404 - Not Found

```json
{
  "status_code": 404,
  "status_message": "Not Found",
  "success": false,
  "mensaje": "No se encontró información de cliente para el crédito 99999"
}
```

#### Error 422 - Unprocessable Entity

```json
{
  "status_code": 422,
  "status_message": "Unprocessable Entity",
  "success": false,
  "mensaje": "El campo 'id_credito' debe ser un número entero. Valor recibido: abc",
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "id_credito"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
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
  "mensaje": "Error al procesar la solicitud. Por favor, intente nuevamente."
}
```

---

## Prueba Técnica desde Postman

### Configuración de Postman

#### 1. Crear una Nueva Colección

1. Abrir **Postman**
2. Hacer clic en **"New"** → **"Collection"**
3. Nombre: `API Condonaciones Sparta Ledger`
4. Descripción: `Endpoints para consulta de condonaciones de gastos de cobranza`

#### 2. Crear una Nueva Request

1. Dentro de la colección, hacer clic en **"Add request"**
2. Nombre: `Obtener Condonaciones por ID`
3. Configurar los siguientes campos:

**Método y URL:**
```
GET http://localhost:8000/api/condonaciones/12345
```

#### 3. Configurar Headers

Ir a la pestaña **"Headers"** y agregar:

| Key | Value |
|-----|-------|
| `X-API-Key` | `sparta_ledger_2026_secure_key_v1` |
| `Content-Type` | `application/json` |

![Headers en Postman](https://via.placeholder.com/800x200.png?text=Headers+Configuration)

#### 4. Ejecutar la Solicitud

1. Hacer clic en el botón **"Send"**
2. Observar la respuesta en la sección inferior

### Resultado Esperado

**Código HTTP:** `200 OK`

**Tiempo de respuesta:** < 500ms (depende de la red y base de datos)

**Body:**
```json
{
  "status_code": 200,
  "status_message": "OK",
  "success": true,
  "mensaje": "Datos obtenidos correctamente",
  "datos_generales": { ... },
  "condonacion_cobranza": { ... }
}
```

### Casos de Prueba Recomendados

| # | Caso de Prueba | ID Crédito | Header API Key | Resultado Esperado |
|---|----------------|------------|----------------|--------------------|
| 1 | Crédito válido con condonaciones | `12345` | ✅ Válido | 200 - Respuesta con datos |
| 2 | Crédito válido sin condonaciones | `99999` | ✅ Válido | 200 - detalle vacío |
| 3 | Crédito inexistente | `1` | ✅ Válido | 404 - No encontrado |
| 4 | ID crédito inválido (negativo) | `-1` | ✅ Válido | 400 - Bad Request |
| 5 | ID crédito inválido (texto) | `abc` | ✅ Válido | 422 - Validation Error |
| 6 | Sin API Key | `12345` | ❌ Sin header | 401 - Unauthorized |
| 7 | API Key inválido | `12345` | ❌ Key incorrecto | 401 - Unauthorized |

### cURL Equivalente

```bash
curl --location 'http://localhost:8000/api/condonaciones/12345' \
--header 'X-API-Key: sparta_ledger_2026_secure_key_v1' \
--header 'Content-Type: application/json'
```

### Python Requests

```python
import requests

url = "http://localhost:8000/api/condonaciones/12345"
headers = {
    "X-API-Key": "sparta_ledger_2026_secure_key_v1",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())
```

### JavaScript (Fetch)

```javascript
const url = 'http://localhost:8000/api/condonaciones/12345';
const headers = {
    'X-API-Key': 'sparta_ledger_2026_secure_key_v1',
    'Content-Type': 'application/json'
};

fetch(url, {
    method: 'GET',
    headers: headers
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

---

## Consideraciones Técnicas

### 1. Seguridad

- ✅ **Autenticación obligatoria**: Todas las peticiones requieren API Key válido
- ✅ **Validación de entrada**: Los parámetros son validados automáticamente
- ✅ **Manejo seguro de errores**: No se exponen detalles internos de la base de datos
- ✅ **CORS configurado**: Se puede controlar qué dominios pueden consumir la API
- ⚠️ **En producción**: Usar HTTPS y configurar orígenes permitidos en CORS

### 2. Performance

- Base de datos: MySQL con conexiones pooling
- Tiempo de respuesta típico: < 300ms
- Las consultas usan índices optimizados
- Se recomienda implementar caché para consultas frecuentes

### 3. Límites y Restricciones

| Aspecto | Límite |
|---------|--------|
| Tamaño máximo de respuesta | ~5 MB (JSON) |
| Timeout de consulta | 30 segundos |
| Rate limiting | No implementado (considerar en producción) |
| Registros máximos por consulta | Sin límite explícito |

### 4. Datos Retornados

- **Solo se retornan gastos CONDONADOS** (`condonado = 1`)
- Si no hay gastos condonados, el array `detalle` estará vacío
- Los campos pueden ser `null` según disponibilidad en la base de datos
- Las fechas se retornan en formato ISO 8601

### 5. Base de Datos

**Tablas consultadas:**
- `db-mega-reporte.tbl_segundometro_semana` → Datos generales del cliente
- `db-mega-reporte.gastos_cobranza` → Gastos de cobranza condonados

**Relación:** Se usa `Id_credito` como clave de relación entre ambas tablas

### 6. Documentación Interactiva

La API incluye documentación automática en:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Estas interfaces permiten:
- Ver todos los endpoints disponibles
- Probar la API directamente desde el navegador
- Ver ejemplos de solicitudes y respuestas
- Descargar el esquema OpenAPI

### 7. Versionado

- **Versión actual**: 1.0.0
- El versionado sigue el estándar **Semantic Versioning** (SemVer)
- Cambios en la API se documentarán en un archivo `CHANGELOG.md`

### 8. Soporte y Contacto

Para solicitar:
- Nuevos campos en la respuesta
- Cambios en la estructura de datos
- Acceso a API Keys de producción
- Reportar errores o bugs

**Contactar a:** Equipo de Inteligencia de Negocios / Desarrollo de Software

---

## Anexo: Campos Adicionales

Si requieres campos adicionales que no están incluidos en la respuesta actual, por favor contacta al equipo de desarrollo con:

1. Nombre del campo solicitado
2. Tabla de origen (si la conoces)
3. Justificación del uso
4. Prioridad (alta, media, baja)

**Nota:** Los cambios en la estructura de la API se evaluarán para mantener retrocompatibilidad con integraciones existentes.

---

## Historial de Cambios

| Versión | Fecha | Cambios Realizados | Responsable |
|---------|-------|--------------------|-------------|
| 1.0.0 | 30/Enero/2026 | Versión inicial del manual técnico | Desarrollo de Software |

---

**Fin del Manual Técnico de Consumo - API de Condonaciones**

*Este documento es de uso interno y confidencial. No distribuir sin autorización.*
