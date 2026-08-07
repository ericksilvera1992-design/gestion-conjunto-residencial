from backend.modelos.residente import Residente

cedula = int(input("Ingrese la cédula: "))

residente = Residente.buscar_por_cedula(cedula)

if residente:
    print("\n===== RESIDENTE ENCONTRADO =====")
    print(residente)
else:
    print("\nNo se encontró ningún residente.")