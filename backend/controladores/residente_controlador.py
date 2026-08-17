"""
Controlador para la gestión de residentes.

Este módulo contiene las operaciones de validación y gestión
de los residentes del conjunto residencial.

Estándar de codificación utilizado:
- Clases: PascalCase.
- Funciones y métodos: snake_case.
- Variables y parámetros: snake_case.
- Constantes: MAYÚSCULAS.
- Docstrings: se utilizan para describir clases y métodos
  principales.
- Se utiliza manejo de excepciones para validar los datos
  recibidos.
"""

from backend.modelos.residente import Residente


class ResidenteControlador:
    """
    Controla las operaciones relacionadas con los residentes.

    Esta clase centraliza la validación de datos y las operaciones
    de creación, consulta, actualización y eliminación de residentes.
    """

    @staticmethod
    def _validar_entero(valor, nombre_campo):
        """
        Valida que un valor corresponda a un número entero positivo.

        Args:
            valor: Valor que se desea validar.
            nombre_campo: Nombre del campo que se está validando.

        Returns:
            int: Valor convertido a entero.

        Raises:
            ValueError: Si el valor no es un entero válido o
                es menor o igual que cero.
        """
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
        """
        Valida que un campo de texto no esté vacío.

        Args:
            valor: Valor que se desea validar.
            nombre_campo: Nombre del campo que se está validando.

        Returns:
            str: Texto limpio y sin espacios innecesarios.

        Raises:
            ValueError: Si el campo está vacío.
        """
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            raise ValueError(
                f"El campo {nombre_campo} es obligatorio."
            )

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
        """
        Valida y organiza los datos de un residente.

        Args:
            nombres: Nombres del residente.
            apellidos: Apellidos del residente.
            correo: Correo electrónico.
            telefono: Número de teléfono.
            tipo_residente: Tipo de residente.
            titular: Indica si es titular de la vivienda.
            documento: Documento de identidad.
            id_vivienda: Identificador de la vivienda.

        Returns:
            dict: Datos del residente validados.

        Raises:
            ValueError: Si alguno de los datos no cumple
                las validaciones establecidas.
        """
        correo = ResidenteControlador._validar_texto(
            correo,
            "correo"
        )

        if "@" not in correo:
            raise ValueError(
                "El correo no tiene un formato válido."
            )

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
        """
        Obtiene la lista de todos los residentes.

        Returns:
            Resultado obtenido desde el modelo Residente.
        """
        return Residente.listar()

    @staticmethod
    def buscar_por_documento(documento):
        """
        Busca un residente utilizando su documento.

        Args:
            documento: Documento del residente.

        Returns:
            Resultado de la búsqueda del residente.
        """
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
        """
        Crea un nuevo residente después de validar sus datos.

        Returns:
            Resultado de la creación del residente.
        """
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
        """
        Actualiza los datos de un residente existente.

        Args:
            id_residente: Identificador del residente.
            Los demás parámetros corresponden a los datos
            actualizados del residente.

        Returns:
            Resultado de la actualización del residente.
        """
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

        return Residente.actualizar(
            id_residente,
            **datos
        )

    @staticmethod
    def eliminar(id_residente):
        """
        Elimina un residente utilizando su identificador.

        Args:
            id_residente: Identificador del residente.

        Returns:
            Resultado de la eliminación del residente.
        """
        id_residente = ResidenteControlador._validar_entero(
            id_residente,
            "id_residente"
        )

        return Residente.eliminar(id_residente)