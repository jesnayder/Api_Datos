from api.api_client import APIClient
from models.dataset import Estacion
from db import engine
from db import Session

class MainController:
    def __init__(self):
        self.api_client = APIClient()

    def importar_estaciones(self):
        datos = self.api_client.obtener_datos()
        session = Session()

        for item in datos:
            estacion = Estacion(
                año=item.get("a_o", ""),
                trimestre=item.get("trimestre", ""),
                nombre=item.get("proveedor", "Desconocido"),
                abonados_servicio=int(item.get("abonados_en_servicio", 0)),
                abonados_pospago=int(item.get("abonados_pospago", 0)),
                lineas_activas=int(item.get("l_neas_activas", 0)),
                lineas_retiradas=int(item.get("l_neas_retiradas", 0)),
                abonados_prepago=int(item.get("abonados_prepago", 0))
            )
            session.add(estacion)

        session.commit()
        session.close()
        print("Datos guardados correctamente en la base de datos.")

    def listar_estaciones(self):
        session = Session()
        try:
            estaciones = session.query(Estacion).all()
            if not estaciones:
                print("La tabla datos no existe. Primero debes importar los datos.")
            
            else:
                for estacion in estaciones:
                    print(f"ID: {estacion.id} | Año: {estacion.año} | Trimestre: {estacion.trimestre} | "
                        f"Nombre: {estacion.nombre} | Abonados en servicio: {estacion.abonados_servicio}")
        except Exception as e:
            print(f"[ERROR] No se pudieron obtener las estaciones: {e}")
        finally:
            session.close()

    def eliminar_tabla_estaciones(self):
        try:
            session = Session()

            # Eliminar la tabla
            Estacion.__table__.drop(engine)
            session.commit()
             # Volver a crear la tabla vacía
            Estacion.metadata.create_all(engine)
            print("[OK] Tabla 'datos' esta fue limpiada correctamente.")

        except Exception as e:
            print(f"[ERROR] Error al eliminar y recrear la tabla 'estaciones': {e}")
            session.rollback()

        finally:
            session.close()

    def eliminar_estacion_id(self, estacion_id):
        session = Session()
        try:
            estacion = session.query(Estacion).filter(Estacion.id == estacion_id).first()

            if estacion is None:
                print(f"[INFO] No se encontró una estación con ID {estacion_id} o no se ha importado la base de datos.") 
                print ("Verifique que el ID sea correcto .")
                return False

            session.delete(estacion)
            session.commit()
            print(f"[OK] dato con ID {estacion_id} eliminada correctamente.")
            return True

        except Exception as e:
            session.rollback()
            print(f"[ERROR] Error al eliminar la estación con ID {estacion_id}: {e}")
            return False

        finally:
            session.close()
            
    #listar por año
    def listar_estaciones_por_ano(self, ano_buscar):
        session = Session()
        try:
            estaciones = session.query(Estacion).filter(Estacion.año == ano_buscar).all()

            if not estaciones:
                print(f"No se encontraron estaciones para el año {ano_buscar}.")
                return

            for estacion in estaciones:
                print(f"ID: {estacion.id} | Año: {estacion.año} | Trimestre: {estacion.trimestre} | "
                    f"Nombre: {estacion.nombre} | Abonados en servicio: {estacion.abonados_servicio}")

        except Exception as e:
            print(f"[ERROR] No se pudieron obtener las estaciones del año {ano_buscar}: {e}")
        finally:
            session.close()

        



