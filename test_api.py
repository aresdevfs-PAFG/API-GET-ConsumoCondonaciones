"""
Script de prueba para la API de Condonaciones
"""

import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener API Key del .env
API_KEY = os.getenv("API_KEYS", "").split(",")[0].strip()


def test_condonacion(id_credito: int, base_url: str = "http://localhost:8000"):
    """
    Prueba los endpoints de condonación
    
    Args:
        id_credito: ID del crédito a probar
        base_url: URL base de la API
    """
    
    # Headers con API Key
    headers = {
        "X-API-Key": API_KEY
    }
    
    print("=" * 60)
    print(f"PROBANDO API DE CONDONACIONES - Crédito: {id_credito}")
    print(f"API Key: {API_KEY[:20]}...")
    print("=" * 60)
    
    # Test 1: Obtener todos los gastos
    print("\n1. Obteniendo todos los gastos de cobranza...")
    print("-" * 60)
    
    try:
        response = requests.get(
            f"{base_url}/api/condonaciones/{id_credito}",
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Respuesta exitosa")
            print(f"Cliente: {data['datos_generales']['nombre_cliente']}")
            print(f"Total de gastos: {len(data['condonacion_cobranza']['detalle'])}")
            print("\nJSON completo:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif response.status_code == 401:
            print(f"\n✗ Error de autenticación: API Key inválida")
            print(response.text)
        else:
            print(f"\n✗ Error: {response.text}")
    except Exception as e:
        print(f"\n✗ Error de conexión: {e}")
    
    # Test 2: Obtener solo condonados
    print("\n" + "=" * 60)
    print("2. Obteniendo solo gastos condonados...")
    print("-" * 60)
    
    try:
        response = requests.get(
            f"{base_url}/api/condonaciones/{id_credito}/solo-condonados",
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Respuesta exitosa")
            print(f"Gastos condonados: {len(data['condonacion_cobranza']['detalle'])}")
            
            if data['condonacion_cobranza']['detalle']:
                print("\nPrimeros 3 registros condonados:")
                for i, detalle in enumerate(data['condonacion_cobranza']['detalle'][:3], 1):
                    print(f"  {i}. Semana: {detalle['semana']}, Monto: ${detalle['monto_valor']}")
        else:
            print(f"\n✗ Error: {response.text}")
    except Exception as e:
        print(f"\n✗ Error de conexión: {e}")
    
    # Test 3: Obtener pendientes
    print("\n" + "=" * 60)
    print("3. Obteniendo gastos pendientes de condonar...")
    print("-" * 60)
    
    try:
        response = requests.get(
            f"{base_url}/api/condonaciones/{id_credito}/pendientes",
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Respuesta exitosa")
            print(f"Gastos pendientes: {len(data['condonacion_cobranza']['detalle'])}")
            
            if data['condonacion_cobranza']['detalle']:
                print("\nPrimeros 3 registros pendientes:")
                for i, detalle in enumerate(data['condonacion_cobranza']['detalle'][:3], 1):
                    print(f"  {i}. Semana: {detalle['semana']}, Monto: ${detalle['monto_valor']}")
        else:
            print(f"\n✗ Error: {response.text}")
    except Exception as e:
        print(f"\n✗ Error de conexión: {e}")
    
    # Test 4: Probar sin API Key
    print("\n" + "=" * 60)
    print("4. Probando acceso sin API Key (debe fallar)...")
    print("-" * 60)
    
    try:
        response = requests.get(f"{base_url}/api/condonaciones/{id_credito}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print("\n✓ Seguridad funcionando correctamente - Acceso denegado")
            print(response.text)
        else:
            print(f"\n⚠️  La API permitió acceso sin API Key")
    except Exception as e:
        print(f"\n✗ Error de conexión: {e}")
    
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)


def test_health(base_url: str = "http://localhost:8000"):
    """Verifica el estado de la API"""
    print("\nVerificando estado de la API...")
    
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✓ API en línea")
            return True
        else:
            print("✗ API no responde correctamente")
            return False
    except Exception as e:
        print(f"✗ No se puede conectar a la API: {e}")
        return False


if __name__ == "__main__":
    # Configuración
    BASE_URL = "http://localhost:8000"
    ID_CREDITO = 1564499  # Cambia esto por un ID real de tu base de datos
    
    if not API_KEY:
        print("⚠️  Error: No se encontró API_KEY en el archivo .env")
        print("   Asegúrate de tener configurado API_KEYS en tu .env")
        exit(1)
    
    # Verificar estado de la API
    if test_health(BASE_URL):
        # Ejecutar pruebas
        test_condonacion(ID_CREDITO, BASE_URL)
    else:
        print("\n⚠️  Asegúrate de que la API esté corriendo:")
        print("   python main.py")
        print(f"   o")
        print("   uvicorn main:app --reload")
