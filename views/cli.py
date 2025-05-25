from controllers.main_controller import MainController
from models.dataset import Base
from db import engine

Base.metadata.create_all(engine)  # Crea las tablas si no existen

def menu():
    controller = MainController()
    while True:
        print("\n--- Menú Principal ---")
        print("1. Importar datos desde API")
        print("2. Listar estaciones")
        print("3. eliminar dato por id")
        print("4. eliminar tabla")
        print("5. listar por año")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            controller.importar_estaciones()
        elif opcion == "2":
            controller.listar_estaciones()
        elif opcion == "3":
            try:
                id_estacion = int(input("Ingresa el ID de la estación a eliminar: "))
                controller.eliminar_estacion_id(id_estacion)
            except ValueError:
                print("El ID debe ser un número entero.")
                  
        elif opcion == "4":
            controller.eliminar_tabla_estaciones()
        
        elif opcion == "5":

            ano = int(input("Ingresa el año que desea listar: "))
            controller.listar_estaciones_por_ano(ano)
            
        elif opcion == "6":
            print("Saliendo...")
            exit()
        else:
            print("Opción inválida")