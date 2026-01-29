"""
Configuración de base de datos
"""

import pymysql
from contextlib import contextmanager
from typing import Generator
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class DatabaseConfig:
    """Configuración de conexión a base de datos"""
    
    HOST = os.getenv("DB_HOST", "localhost")
    PORT = int(os.getenv("DB_PORT", "3306"))
    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD", "")
    DATABASE = os.getenv("DB_DATABASE", "db-mega-reporte")
    
    # Para tbl_segundometro_semana
    DATABASE_SEGUNDOMETRO = os.getenv("DB_SEGUNDOMETRO", "segundometro")


@contextmanager
def get_db_connection(database: str = None) -> Generator[pymysql.connections.Connection, None, None]:
    """
    Context manager para conexión a base de datos
    
    Args:
        database: Nombre de la base de datos (opcional)
    
    Yields:
        Conexión a la base de datos
    """
    db_name = database or DatabaseConfig.DATABASE
    
    connection = pymysql.connect(
        host=DatabaseConfig.HOST,
        port=DatabaseConfig.PORT,
        user=DatabaseConfig.USER,
        password=DatabaseConfig.PASSWORD,
        database=db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        yield connection
    finally:
        connection.close()


def get_db():
    """Dependency para FastAPI"""
    with get_db_connection() as conn:
        yield conn
