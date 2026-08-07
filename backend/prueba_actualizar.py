from backend.controladores.residente_controlador import ResidenteControlador
from mysql.connector import Error


def solicitar_tipo_residente():
    opciones = ("Propietario", "Arrendatario", "Familiar")

    while True:
        tipo_residente = input(
            "Tipo de residente (Propietario, Arrendatario o Familiar): "
        ).strip().capitalize()

        if tipo_residente in opciones:
            return tipo_residente

        print("Valor no válido. Selecciona Propietario, Arrendatario o Familiar.")


def solicitar_titular():
    while True:
        titular = input("Titular (SI o NO): ").strip().upper()

        if titular in ("SI", "NO"):
            return titular

        print("Valor no válido. Escribe SI o NO.")


def solicitar_campo_obligatorio(nombre_campo):
    while True:
        valor = input(f"{nombre_campo}: ").strip()

        if valor:
            return valor

        print(f"El campo {nombre_campo.lower()} no puede quedar vacío.")


def main():
    print("===== ACTUALIZAR RESIDENTE =====")

    try:
        registros_actualizados = ResidenteControlador.actualizar(
            input("Id del residente: ").strip(),
            input("Nombres: ").strip(),
            input("Apellidos: ").strip(),
            solicitar_campo_obligatorio("Correo"),
            input("Teléfono: ").strip(),
            solicitar_tipo_residente(),
            solicitar_titular(),
            solicitar_campo_obligatorio("Documento"),
            input("Id de vivienda: ").strip()
        )

        if registros_actualizados == 1:
            print("\nResidente actualizado correctamente.")
        else:
            print("\nNo se encontró un residente con ese id.")
    except (ConnectionError, Error, ValueError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
