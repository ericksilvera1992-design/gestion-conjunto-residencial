from backend.config.conexion import obtener_conexion


class Residente:

    @staticmethod
    def _cerrar_recursos(conexion, cursor):
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()

    @staticmethod
    def listar():
        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    id_residente,
                    nombres,
                    apellidos,
                    correo,
                    telefono,
                    tipo_residente,
                    titular,
                    documento,
                    id_vivienda
                FROM residentes
                ORDER BY nombres, apellidos
            """

            cursor.execute(sql)
            return cursor.fetchall()

        finally:
            Residente._cerrar_recursos(conexion, cursor)

    @staticmethod
    def crear(
        nombres,
        apellidos,
        correo,
        telefono,
        tipo_residente,
        titular,
        documento,
        id_vivienda
    ):
        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            sql = """
                INSERT INTO residentes (
                    nombres,
                    apellidos,
                    correo,
                    telefono,
                    tipo_residente,
                    titular,
                    documento,
                    id_vivienda
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                nombres,
                apellidos,
                correo,
                telefono,
                tipo_residente,
                titular,
                documento,
                id_vivienda
            )

            cursor.execute(sql, valores)
            conexion.commit()

            return cursor.lastrowid

        finally:
            Residente._cerrar_recursos(conexion, cursor)

    @staticmethod
    def buscar_por_cedula(documento):
        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    id_residente,
                    nombres,
                    apellidos,
                    correo,
                    telefono,
                    tipo_residente,
                    titular,
                    documento,
                    id_vivienda
                FROM residentes
                WHERE documento = %s
            """

            cursor.execute(sql, (documento,))
            return cursor.fetchone()

        finally:
            Residente._cerrar_recursos(conexion, cursor)

    @staticmethod
    def actualizar(
        id_residente,
        nombres,
        apellidos,
        correo,
        telefono,
        tipo_residente,
        titular,
        documento,
        id_vivienda
    ):
        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            sql = """
                UPDATE residentes
                SET
                    nombres = %s,
                    apellidos = %s,
                    correo = %s,
                    telefono = %s,
                    tipo_residente = %s,
                    titular = %s,
                    documento = %s,
                    id_vivienda = %s
                WHERE id_residente = %s
            """

            valores = (
                nombres,
                apellidos,
                correo,
                telefono,
                tipo_residente,
                titular,
                documento,
                id_vivienda,
                id_residente
            )

            cursor.execute(sql, valores)
            conexion.commit()

            return cursor.rowcount

        finally:
            Residente._cerrar_recursos(conexion, cursor)

    @staticmethod
    def eliminar(id_residente):
        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            sql = """
                DELETE FROM residentes
                WHERE id_residente = %s
            """

            cursor.execute(sql, (id_residente,))
            conexion.commit()

            return cursor.rowcount

        finally:
            Residente._cerrar_recursos(conexion, cursor)
