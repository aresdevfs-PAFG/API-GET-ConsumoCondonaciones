# Códigos de Estado HTTP - API Condonaciones

## 📋 Tabla de Códigos

| Código | Significado | Responsable | Cuándo se usa |
|--------|-------------|-------------|---------------|
| **200** | Todo bien | Nadie | Operación exitosa, datos retornados correctamente |
| **400** | Request mal formado | Cliente | ID inválido (0, negativos, patrones repetitivos) |
| **401** | No autenticado | Cliente | API Key inválida, faltante o no autorizada |
| **404** | No encontrado | Cliente | El crédito consultado no existe en la base de datos |
| **422** | Regla de negocio violada | Cliente | Validación de lógica de negocio (no usado actualmente) |
| **500** | Error del servidor | Backend | Error de base de datos, conexión o error interno |

## ✅ Respuestas Exitosas (200)

Todas las respuestas exitosas incluyen:
- `success: true`
- `mensaje`: Descripción de lo que se encontró
- `datos_generales`: Información del cliente
- `condonacion_cobranza`: Array de detalles (puede estar vacío)

```json
{
  "success": true,
  "mensaje": "Se encontraron 3 gastos condonados",
  "datos_generales": { ... },
  "condonacion_cobranza": {
    "detalle": [ ... ]
  }
}
```

## ❌ Errores del Cliente (4xx)

### 400 - Bad Request
**Causa**: ID de crédito inválido

Ejemplos:
- ID = 0 o negativo
- ID con patrón repetitivo (1111111, 22222222)
- ID con patrón alternante (12121212, 343434343)
- ID demasiado grande (> 999,999,999)

```json
{
  "detail": "El ID del crédito no puede tener todos los dígitos iguales (1111111)"
}
```

### 401 - Unauthorized
**Causa**: API Key inválida o faltante

```json
{
  "detail": "API Key inválida o no autorizada"
}
```

### 404 - Not Found
**Causa**: El crédito no existe

```json
{
  "detail": "No se encontró información del crédito 12345. Verifica que el ID sea correcto."
}
```

## 💥 Errores del Servidor (5xx)

### 500 - Internal Server Error
**Causa**: Error de base de datos o error interno

```json
{
  "detail": "Error de base de datos: (2003, \"Can't connect to MySQL server\")"
}
```

## 🔍 Flujo de Validación

```
Request → API Key válida? 
    NO → 401 Unauthorized
    SÍ ↓

ID válido? (formato, patrones)
    NO → 400 Bad Request
    SÍ ↓

Crédito existe?
    NO → 404 Not Found
    SÍ ↓

Consulta BD exitosa?
    NO → 500 Internal Server Error
    SÍ ↓

200 OK + Datos
```

## 📝 Notas Importantes

1. **success: true/false**
   - `true`: Solo en respuestas 200
   - No se incluye en errores 4xx/5xx (FastAPI usa `detail`)

2. **Mensajes descriptivos**
   - Los errores 4xx culpan al cliente (incluyen el valor inválido)
   - Los errores 5xx no revelan detalles sensibles del servidor

3. **Validaciones en capas**
   - Capa 1: FastAPI valida tipos (int, str)
   - Capa 2: Security valida API Key (401)
   - Capa 3: Utils valida formato y patrones (400)
   - Capa 4: Database valida existencia (404)
   - Capa 5: Manejo de excepciones (500)

4. **Array vacío ≠ Error**
   - Si no hay gastos condonados: 200 OK con `detalle: []`
   - Esto NO es un error, es un resultado válido
