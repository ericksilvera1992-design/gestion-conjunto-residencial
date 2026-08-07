from backend.config.conexion import obtener_conexion


class Residente:

    @staticmethod
    def listar():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM residentes
            ORDER BY NOMBRES
        """)

        datos = cursor.fetchall()

        cursor.close()
        conexion.close()

        return datos

    @staticmethod
    def crear(id_residente, nombres, apellidos, correo, telefono, torre, id_casa, titular):

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO residentes
        (ID_RESIDENTES, NOMBRES, APELLIDOS, CORREO, TELEFONO, TORRE, ID_CASA, TITULAR)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        valores = (
            id_residente,
            nombres,
            apellidos,
            correo,
            telefono,
            torre,
            id_casa,
            titular
        )

        cursor.execute(sql, valores)

        conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def buscar_por_cedula(id_residente):

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql = """
        SELECT *
        FROM residentes
        WHERE ID_RESIDENTES = %s
        """

        cursor.execute(sql, (id_residente,))

        residente = cursor.fetchone()

        cursor.close()
        conexion.close()

        return residente

    @staticmethod
    def actualizar(id_residente, nombres, apellidos, correo, telefono, torre, id_casa, titular):

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE residentes
        SET
            NOMBRES=%s,
            APELLIDOS=%s,
            CORREO=%s,
            TELEFONO=%s,
            TORRE=%s,
            ID_CASA=%s,
            TITULAR=%s
        WHERE ID_RESIDENTES=%s
        """

        valores = (
            nombres,
            apellidos,
            correo,
            telefono,
            torre,
            id_casa,
            titular,
            id_residente
        )

        cursor.execute(sql, valores)

        conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar(id_residente):

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        DELETE FROM residentes
        WHERE ID_RESIDENTES=%s
        """

        cursor.execute(sql, (id_residente,))

        conexion.commit()

        cursor.close()
        conexion.close()