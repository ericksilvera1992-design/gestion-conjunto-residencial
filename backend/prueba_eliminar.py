from backend.controladores.residente_controlador import ResidenteControlador
from mysql.connector import Error


def main():
    print("===== ELIMINAR RESIDENTE =====")

    try:
        id_residente = input("Id del residente: ").strip()
        confirmacion = input("Escribe SI para confirmar la eliminación: ").strip()

        if confirmacion.upper() != "SI":
            print("\nEliminación cancelada.")
            return

        registros_eliminados = ResidenteControlador.eliminar(id_residente)

        if registros_eliminados == 1:
            print("\nResidente eliminado correctamente.")
        else:
            print("\nNo se encontró un residente con ese id.")
    except (ConnectionError, Error, ValueError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
