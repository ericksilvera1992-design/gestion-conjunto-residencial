from backend.controladores.residente_controlador import ResidenteControlador
from mysql.connector import Error


def main():
    try:
        residentes = ResidenteControlador.listar()

        print("===== LISTA DE RESIDENTES =====")

        if not residentes:
            print("No hay residentes registrados.")
            return

        for residente in residentes:
            print(residente)
    except (ConnectionError, Error) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
