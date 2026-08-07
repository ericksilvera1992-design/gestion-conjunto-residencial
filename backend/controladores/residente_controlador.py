from backend.modelos.residente import Residente


class ResidenteControlador:

    @staticmethod
    def _validar_entero(valor, nombre_campo):
        try:
            numero = int(valor)
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"El campo {nombre_campo} debe ser un número entero."
            ) from error

        if numero <= 0:
            raise ValueError(
                f"El campo {nombre_campo} debe ser mayor que cero."
            )

        return numero

    @staticmethod
    def _validar_texto(valor, nombre_campo):
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            raise ValueError(f"El campo {nombre_campo} es obligatorio.")

        return texto

    @staticmethod
    def _validar_datos(
        nombres,
        apellidos,
        correo,
        telefono,
        tipo_residente,
        titular,
        documento,
        id_vivienda
    ):
        correo = ResidenteControlador._validar_texto(correo, "correo")

        if "@" not in correo:
            raise ValueError("El correo no tiene un formato válido.")

        return {
            "nombres": ResidenteControlador._validar_texto(
                nombres,
                "nombres"
            ),
            "apellidos": ResidenteControlador._validar_texto(
                apellidos,
                "apellidos"
            ),
            "correo": correo,
            "telefono": ResidenteControlador._validar_texto(
                telefono,
                "telefono"
            ),
            "tipo_residente": ResidenteControlador._validar_texto(
                tipo_residente,
                "tipo_residente"
            ),
            "titular": ResidenteControlador._validar_texto(
                titular,
                "titular"
            ),
            "documento": ResidenteControlador._validar_texto(
                documento,
                "documento"
            ),
            "id_vivienda": ResidenteControlador._validar_entero(
                id_vivienda,
                "id_vivienda"
            )
        }

    @staticmethod
    def listar():
        return Residente.listar()

    @staticmethod
    def buscar_por_documento(documento):
        documento = ResidenteControlador._validar_texto(
            documento,
            "documento"
        )
        return Residente.buscar_por_cedula(documento)

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
        datos = ResidenteControlador._validar_datos(
            nombres,
            apellidos,
            correo,
            telefono,
            tipo_residente,
            titular,
            documento,
            id_vivienda
        )
        return Residente.crear(**datos)

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
        id_residente = ResidenteControlador._validar_entero(
            id_residente,
            "id_residente"
        )
        datos = ResidenteControlador._validar_datos(
            nombres,
            apellidos,
            correo,
            telefono,
            tipo_residente,
            titular,
            documento,
            id_vivienda
        )
        return Residente.actualizar(id_residente, **datos)

    @staticmethod
    def eliminar(id_residente):
        id_residente = ResidenteControlador._validar_entero(
            id_residente,
            "id_residente"
        )
        return Residente.eliminar(id_residente)
