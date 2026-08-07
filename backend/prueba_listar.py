from backend.modelos.residente import Residente

residentes = Residente.listar()

print("===== LISTA DE RESIDENTES =====")

for residente in residentes:
    print(residente)