from backend.controladores.residente_controlador import ResidenteControlador
from mysql.connector import Error


def main():
    documento = input("Ingrese el documento: ").strip()

    try:
        residente = ResidenteControlador.buscar_por_documento(documento)

        if residente:
            print("\n===== RESIDENTE ENCONTRADO =====")
            print(residente)
        else:
            print("\nNo se encontró ningún residente.")
    except (ConnectionError, Error, ValueError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
