import mysql.connector


def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion de conjunto residencial"
    )
    return conexion