# DOCUMENTACIÓN TÉCNICA - API DE CONDONACIONES

**Versión:** 1.0.0 | **Fecha:** Enero 2026 | **Tecnología:** FastAPI (Python 3.x)

---

## INTRODUCCIÓN

API REST de solo lectura que permite consultar gastos de cobranza condonados asociados a créditos específicos. Retorna datos del cliente, estado del crédito y listado de gastos condonados en formato JSON estructurado.

**URL Base:** `https://TU_SERVIDOR/api/v1`

---

## 1. AUTENTICACIÓN

Todas las peticiones requieren un API Key en el header HTTP:

```http
X-API-Key: tu_api_key_de_32_caracteres_aqui
```

**Nota:** Contacta al equipo de desarrollo para obtener tu API Key. Si olvidas incluirla o es inválida, recibirás un error `401 Unauthorized`.

---

## 2. ENDPOINT Y PARÁMETROS

### GET /condonaciones/{id_credito}

Obtiene información completa de condonación para un crédito específico.

**Parámetros:**

| Parámetro | Ubicación | Tipo | Obligatorio | Descripción |
|-----------|-----------|------|-------------|-------------|
| `id_credito` | URL path | integer | Sí | ID del crédito a consultar (debe ser > 0) |
| `X-API-Key` | Header | string | Sí | API Key de autenticación |

**Ejemplo de petición:**
```http
GET https://TU_SERVIDOR/api/v1/condonaciones/12345
Headers:
  X-API-Key: tu_api_key_de_32_caracteres_aqui
  Content-Type: application/json
```

---

## 3. ESTRUCTURA DE LA RESPUESTA

### Respuesta Exitosa (200 OK)

```json
{
  "status_code": 200,
  "status_message": "OK",
  "success": true,
  "mensaje": "Se encontraron 2 gastos condonados",
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
      }
    ]
  }
}
```

### Campos Principales

**Objeto raíz:**
- `status_code`: Código HTTP (200, 400, 401, 404, 422, 500)
- `success`: `true` = éxito, `false` = error
- `mensaje`: Descripción en español del resultado
- `datos_generales`: Información del cliente y crédito
- `condonacion_cobranza`: Contenedor de gastos condonados

**datos_generales:**
- `id_credito`: ID único del crédito
- `nombre_cliente`: Nombre completo del cliente
- `bucket_morosidad`: Clasificación de morosidad (B1, B2, B3, etc.)
- `dias_mora`: Días que el crédito está en mora
- `saldo_vencido`: Monto total vencido

**condonacion_cobranza.detalle[]:**
- `periodoinicio/periodofin`: Rango de fechas del gasto (formato YYYY-MM-DD)
- `monto_valor`: Monto del gasto condonado
- `cuota`: Cuota pactada originalmente
- `condonado`: Siempre `1` (esta API solo retorna condonados)
- `fecha_condonacion`: Fecha/hora de la condonación (ISO 8601)

**Nota:** Si no hay gastos condonados, `detalle` será un arreglo vacío `[]`.

---

## 4. CÓDIGOS DE RESPUESTA HTTP

| Código | Significado | Causa Común |
|--------|-------------|-------------|
| **200** | OK | Consulta exitosa (con o sin gastos condonados) |
| **400** | Bad Request | ID inválido (negativo, cero, patrón sospechoso) |
| **401** | Unauthorized | API Key faltante, inválida o expirada |
| **404** | Not Found | Crédito no existe en la base de datos |
| **422** | Unprocessable Entity | ID no es un número entero válido |
| **500** | Internal Server Error | Error de servidor o base de datos |

### Ejemplos de Errores

**Error 401 - API Key inválida:**
```json
{
  "status_code": 401,
  "status_message": "Unauthorized",
  "success": false,
  "mensaje": "API Key inválida o no autorizada"
}
```

**Error 404 - Crédito no encontrado:**
```json
{
  "status_code": 404,
  "status_message": "Not Found",
  "success": false,
  "mensaje": "No se encontró información del crédito 99999. Verifica que el ID sea correcto."
}
```

**Error 422 - Validación fallida:**
```json
{
  "status_code": 422,
  "status_message": "Unprocessable Entity",
  "success": false,
  "mensaje": "No se pudo convertir 'abc' a un número entero válido"
}
```

---

## 5. EJEMPLOS DE USO

### cURL

```bash
curl -X GET "https://TU_SERVIDOR/api/v1/condonaciones/12345" \
     -H "X-API-Key: tu_api_key_de_32_caracteres_aqui" \
     -H "Content-Type: application/json"
```

### Python (requests)

```python
import requests

url = "https://TU_SERVIDOR/api/v1/condonaciones/12345"
headers = {
    "X-API-Key": "tu_api_key_de_32_caracteres_aqui",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
data = response.json()

if data["success"]:
    print(f"Cliente: {data['datos_generales']['nombre_cliente']}")
    print(f"Gastos condonados: {len(data['condonacion_cobranza']['detalle'])}")
    
    for gasto in data['condonacion_cobranza']['detalle']:
        print(f"  - Periodo: {gasto['periodoinicio']} | Monto: ${gasto['monto_valor']}")
else:
    print(f"Error {data['status_code']}: {data['mensaje']}")
```

### JavaScript (Fetch API)

```javascript
const apiKey = 'tu_api_key_de_32_caracteres_aqui';
const idCredito = 12345;

fetch(`https://TU_SERVIDOR/api/v1/condonaciones/${idCredito}`, {
  method: 'GET',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('Cliente:', data.datos_generales.nombre_cliente);
    console.log('Gastos:', data.condonacion_cobranza.detalle.length);
    
    data.condonacion_cobranza.detalle.forEach(gasto => {
      console.log(`Gasto: $${gasto.monto_valor} (${gasto.periodoinicio})`);
    });
  } else {
    console.error('Error:', data.mensaje);
  }
})
.catch(error => console.error('Error de red:', error));
```

### Node.js (axios)

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
      console.error(`Error ${error.response.status}:`, error.response.data.mensaje);
    } else {
      console.error('Error:', error.message);
    }
    throw error;
  }
}

// Uso
obtenerCondonaciones(12345)
  .then(data => console.log('Datos obtenidos exitosamente'))
  .catch(error => console.error('Fallo en la consulta'));
```

---

## 6. MEJORES PRÁCTICAS

### Validación de Respuestas

Siempre valida el campo `success` antes de procesar los datos:

```python
if data["success"]:
    # Procesar datos
    procesar_respuesta(data)
else:
    # Manejar error
    print(f"Error: {data['mensaje']}")
```

### Manejo de Arreglo Vacío

El campo `detalle` puede estar vacío si no hay gastos condonados:

```javascript
const gastos = response.condonacion_cobranza.detalle;

if (gastos.length === 0) {
  console.log("No hay gastos condonados para este crédito");
} else {
  console.log(`Se encontraron ${gastos.length} gastos condonados`);
}
```

### Campos Nullable

Algunos campos pueden ser `null`, valida antes de usar:

```javascript
const nombreCliente = datos.nombre_cliente ?? "No disponible";
const diasMora = datos.dias_mora ?? 0;
```

### Implementar Timeouts

Siempre incluye timeouts en tus peticiones:

```python
response = requests.get(url, headers=headers, timeout=30)  # 30 segundos
```

### Manejo de Errores por Código

```python
if data['status_code'] == 401:
    # Re-autenticar o verificar API Key
    renovar_credenciales()
elif data['status_code'] == 404:
    # Registrar ID no encontrado
    log_id_no_encontrado(id_credito)
elif data['status_code'] >= 500:
    # Alertar equipo de operaciones
    notificar_error_servidor()
```

---

## 7. SEGURIDAD

La API implementa múltiples capas de seguridad:

1. **Autenticación API Key**: Solo clientes autorizados pueden acceder
2. **Validación de entrada**: Rechaza IDs inválidos o patrones sospechosos
3. **Consultas parametrizadas**: Previene SQL injection
4. **HTTPS obligatorio**: Todas las comunicaciones deben ser cifradas
5. **Rate limiting**: Límite de peticiones por minuto (contacta a desarrollo para detalles)

**Importante:** 
- Nunca expongas tu API Key en código público (repositorios, frontend)
- Almacena el API Key en variables de entorno o gestores de secretos
- Rota tu API Key periódicamente

---

## 8. DOCUMENTACIÓN INTERACTIVA

FastAPI genera automáticamente documentación interactiva donde puedes probar la API:

- **Swagger UI:** `https://TU_SERVIDOR/docs`
- **ReDoc:** `https://TU_SERVIDOR/redoc`

Desde Swagger UI puedes:
1. Ver todos los endpoints disponibles
2. Probar peticiones directamente desde el navegador
3. Ver esquemas de entrada/salida con ejemplos
4. Configurar tu API Key para pruebas

---

## 9. DEFINICIÓN DE TIPOS (TypeScript)

Para facilitar la integración en proyectos TypeScript:

```typescript
interface CondonacionResponse {
  status_code: number;
  status_message: string;
  success: boolean;
  mensaje: string;
  datos_generales: DatosGenerales | null;
  condonacion_cobranza: CondonacionCobranza | null;
}

interface DatosGenerales {
  id_credito: number | null;
  nombre_cliente: string | null;
  id_cliente: number | null;
  domicilio_completo: string | null;
  bucket_morosidad: string | null;
  dias_mora: number | null;
  saldo_vencido: number | null;
}

interface CondonacionCobranza {
  detalle: DetalleCondonacion[];
}

interface DetalleCondonacion {
  periodoinicio: string | null;
  periodofin: string | null;
  semana: string | number | null;
  parcialidad: string | number | null;
  monto_valor: number | null;
  cuota: number | null;
  condonado: number | null;
  fecha_condonacion: string | null;
}

// Ejemplo de uso
async function consultarAPI(idCredito: number): Promise<CondonacionResponse> {
  const response = await fetch(`https://API/condonaciones/${idCredito}`, {
    headers: { 'X-API-Key': process.env.API_KEY as string }
  });
  return await response.json();
}
```

---

## 10. SOPORTE Y CONTACTO

**Errores o dudas:** Contacta al equipo de desarrollo  
**Solicitud de API Key:** Envía correo a tu punto de contacto técnico  
**Reportar problemas:** Incluye el `id_credito` consultado y el mensaje de error recibido

---

**FIN DE DOCUMENTACIÓN**

---

*Última actualización: Enero 2026 | Versión 1.0.0*
