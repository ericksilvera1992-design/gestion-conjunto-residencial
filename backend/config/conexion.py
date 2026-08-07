import mysql.connector
from mysql.connector import Error


def obtener_conexion():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gestion_conjunto_residencial",
            charset="utf8mb4"
        )
    except Error as error:
        raise ConnectionError(
            "No fue posible conectar con MySQL. "
            "Verifica que el servicio esté activo y la configuración sea correcta."
        ) from error
