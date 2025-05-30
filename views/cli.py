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
        print("3. Eliminar dato por ID")
        print("4. Eliminar tabla")
        print("5. Listar por año")
        print("6. Indices de fidelización por proveedores")
        print("7. Resumen de cancelación y retención")
        print("8. Grafica de retención por trimestre")
        print("9. Grafica de cancelación por trimestre")
        print("10. Salir")
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
            controller.indices_de_fidelizacion()

        elif opcion == "7":
            controller.mostrar_resumen_cancelacion_y_relacion()
            
        elif opcion == "8":
            controller.graficar_retencion_por_trimestre()

        elif opcion == "9":
            controller.graficar_churnrate_por_trimestre()                        
            
        elif opcion == "10":
            print("Saliendo...")
            exit()
        else:
            print("Opción inválida")