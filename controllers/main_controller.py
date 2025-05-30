from api.api_client import APIClient
from models.dataset import Estacion
from db import engine
from db import Session
import matplotlib.pyplot as plt
import seaborn as sns

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
                abonados_prepago=int(item.get("abonados_prepago", 0)),
                abonados_pospago=int(item.get("abonados_pospago", 0)),
                lineas_activadas=int(item.get("l_neas_activas", 0)),
                lineas_retiradas=int(item.get("l_neas_retiradas", 0))
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

            Estacion.__table__.drop(engine)
            session.commit()
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

    
    def indices_de_fidelizacion(self):
        session = Session()
        try:
            proveedores = self._obtener_proveedores(session)
            periodos, trimestres_orden = self._obtener_periodos(session)
            resumen = self._construir_resumen(session, proveedores, periodos, trimestres_orden)
            self._mostrar_irt_por_proveedor(resumen)
            self._mostrar_top_irt(resumen)
            self._mostrar_top_irt(
                resumen,
                top=5,
                reverse=False,
                mensaje="Top 5 proveedores con menor IRT ponderado (mínimo 6 trimestres):"
            )
        except Exception as e:
            print(f"[ERROR] No se pudieron calcular los índices de fidelización: {e}")
        finally:
            session.close()

    def _obtener_proveedores(self, session):
        proveedores = session.query(Estacion.nombre).distinct().all()
        return [p[0] for p in proveedores]

    def _obtener_periodos(self, session):
        periodos = session.query(Estacion.año, Estacion.trimestre).distinct().order_by(Estacion.año, Estacion.trimestre).all()
        trimestres_orden = ['1', '2', '3', '4']
        return periodos, trimestres_orden

    def _construir_resumen(self, session, proveedores, periodos, trimestres_orden):
        resumen = {}
        estaciones = session.query(Estacion).all()
        index = {}
        for est in estaciones:
            index[(est.nombre, est.año, est.trimestre)] = est

        for proveedor in proveedores:
            resumen[proveedor] = []
            for año, trimestre in periodos:
                actual = index.get((proveedor, año, trimestre))
                if not actual:
                    continue
                idx_trim = trimestres_orden.index(trimestre)
                es_primer_periodo = (año == periodos[0][0] and trimestre == '1')
                if idx_trim == 0:
                    if es_primer_periodo:
                        clientes_inicio = actual.abonados_servicio
                        clientes_nuevos = 0
                        lineas_retiradas = 0
                    else:
                        año_ant = año - 1
                        anterior = index.get((proveedor, año_ant, '4'))
                        clientes_inicio = anterior.abonados_servicio if anterior else actual.abonados_servicio
                        clientes_nuevos = actual.lineas_activadas or 0
                        lineas_retiradas = actual.lineas_retiradas or 0
                else:
                    trimestre_ant = trimestres_orden[idx_trim - 1]
                    anterior = index.get((proveedor, año, trimestre_ant))
                    clientes_inicio = anterior.abonados_servicio if anterior else actual.abonados_servicio
                    clientes_nuevos = actual.lineas_activadas or 0
                    lineas_retiradas = actual.lineas_retiradas or 0

                clientes_finales = actual.abonados_servicio
                resumen[proveedor].append({
                    'año': año,
                    'trimestre': trimestre,
                    'clientes_inicio': clientes_inicio,
                    'clientes_finales': clientes_finales,
                    'clientes_nuevos': clientes_nuevos,
                    'lineas_retiradas': lineas_retiradas
                })
        return resumen
    
    def _calcular_irt_ponderado(self, resumen):
        resultados = {}
        for proveedor, datos in resumen.items():
            suma_numerador = 0
            suma_denominador = 0
            for d in datos:
                clientes_inicio = d['clientes_inicio']
                clientes_finales = d['clientes_finales']
                clientes_nuevos = d['clientes_nuevos']
                if clientes_inicio > 0:
                    suma_numerador += (clientes_finales - clientes_nuevos)
                    suma_denominador += clientes_inicio
            if suma_denominador > 0:
                resultados[proveedor] = {
                    'irt_ponderado': suma_numerador / suma_denominador,
                    'trimestres': len(datos)
                }
            else:
                resultados[proveedor] = {
                    'irt_ponderado': None,
                    'trimestres': len(datos)
                }
        return resultados
    
    def _mostrar_irt_por_proveedor(self, resumen):
        resultados = self._calcular_irt_ponderado(resumen)
        for proveedor, datos in resultados.items():
            irt = datos['irt_ponderado']
            if irt is not None:
                print(f"Proveedor: {proveedor} | Índice de retención total ponderado: {irt:.2%}")
            else:
                print(f"Proveedor: {proveedor} | No hay suficientes datos para calcular el índice ponderado.")

    def _mostrar_top_irt(self, resumen, top=5, reverse=True, mensaje="Top 5 proveedores con mayor IRT ponderado (mínimo 6 trimestres):"):
        resultados = self._calcular_irt_ponderado(resumen)
        lista = [
            {'proveedor': p, 'irt_ponderado': d['irt_ponderado'], 'trimestres': d['trimestres']}
            for p, d in resultados.items()
            if d['irt_ponderado'] is not None and d['trimestres'] >= 6
        ]
        topN = sorted(lista, key=lambda x: x['irt_ponderado'], reverse=reverse)[:top]
        print(f"\n{mensaje}")
        for r in topN:
            print(f"Proveedor: {r['proveedor']} | IRT ponderado: {r['irt_ponderado']:.2%} | Trimestres: {r['trimestres']}")

    def calcular_tasa_cancelacion(self, resumen):
        tasas = {}
        for proveedor, datos in resumen.items():
            suma_cancelacion = 0
            cuenta = 0
            for d in datos:
                clientes_inicio = d['clientes_inicio']
                lineas_retiradas = d.get('lineas_retiradas', 0)
                if clientes_inicio and clientes_inicio > 0:
                    tasa = (lineas_retiradas / clientes_inicio) * 100
                    suma_cancelacion += tasa
                    cuenta += 1
            if cuenta > 0:
                tasas[proveedor] = suma_cancelacion / cuenta
            else:
                tasas[proveedor] = None
        return tasas

    def calcular_relacion_retiradas_activadas(self, resumen):
        relaciones = {}
        for proveedor, datos in resumen.items():
            suma_relacion = 0
            cuenta = 0
            for d in datos:
                lineas_activadas = d.get('clientes_nuevos', 0)
                lineas_retiradas = d.get('lineas_retiradas', 0)
                if lineas_activadas and lineas_activadas > 0:
                    relacion = lineas_retiradas / lineas_activadas
                    suma_relacion += relacion
                    cuenta += 1
            if cuenta > 0:
                relaciones[proveedor] = suma_relacion / cuenta
            else:
                relaciones[proveedor] = None
        return relaciones

    def mostrar_resumen_cancelacion_y_relacion(self):
        session = Session()
        try:
            proveedores = self._obtener_proveedores(session)
            periodos, trimestres_orden = self._obtener_periodos(session)
            resumen = self._construir_resumen(session, proveedores, periodos, trimestres_orden)
            tasas = self.calcular_tasa_cancelacion(resumen)
            relaciones = self.calcular_relacion_retiradas_activadas(resumen)
            print("\nResumen por proveedor:")
            for proveedor in proveedores:
                tasa = tasas.get(proveedor)
                relacion = relaciones.get(proveedor)
                tasa_str = f"{tasa:.2f}%" if tasa is not None else "No disponible"
                relacion_str = f"{relacion:.2f}" if relacion is not None else "No disponible"
                print(f"Proveedor: {proveedor} | Tasa cancelación promedio: {tasa_str} | Relación retiradas/activadas: {relacion_str}")
        except Exception as e:
            print(f"[ERROR] No se pudo calcular el resumen: {e}")
        finally:
            session.close()

    def graficar_retencion_por_trimestre(self):
        session = Session()
        try:
            proveedores = self._obtener_proveedores(session)
            periodos, trimestres_orden = self._obtener_periodos(session)
            resumen = self._construir_resumen(session, proveedores, periodos, trimestres_orden)

            data = []
            for proveedor, datos in resumen.items():
                for d in datos:
                    clientes_inicio = d['clientes_inicio']
                    clientes_finales = d['clientes_finales']
                    clientes_nuevos = d['clientes_nuevos']
                    if clientes_inicio > 0:
                        retencion = (clientes_finales - clientes_nuevos) / clientes_inicio * 100
                        periodo = f"{d['año']}-Q{d['trimestre']}"
                        data.append({
                            'Proveedor': proveedor,
                            'Periodo': periodo,
                            'Retencion (%)': retencion
                        })

            if not data:
                print("No hay datos suficientes para graficar la retención.")
                return

            import pandas as pd
            df = pd.DataFrame(data)
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=df, x='Periodo', y='Retencion (%)', hue='Proveedor', marker='o')
            plt.title('Evolución del porcentaje de Retención por Trimestre y Proveedor')
            plt.xlabel('Trimestre')
            plt.ylabel('Retención (%)')
            plt.xticks(rotation=45)
            plt.legend(title='Proveedor')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"[ERROR] No se pudo generar el gráfico de retención: {e}")
        finally:
            session.close()

    def graficar_churnrate_por_trimestre(self):
        session = Session()
        try:
            proveedores = self._obtener_proveedores(session)
            periodos, trimestres_orden = self._obtener_periodos(session)
            resumen = self._construir_resumen(session, proveedores, periodos, trimestres_orden)

            data = []
            for proveedor, datos in resumen.items():
                for d in datos:
                    clientes_inicio = d['clientes_inicio']
                    lineas_retiradas = d.get('lineas_retiradas', 0)
                    if clientes_inicio and clientes_inicio > 0:
                        churn = (lineas_retiradas / clientes_inicio) * 100
                        periodo = f"{d['año']}-Q{d['trimestre']}"
                        data.append({
                            'Proveedor': proveedor,
                            'Periodo': periodo,
                            'ChurnRate (%)': churn
                        })

            if not data:
                print("No hay datos suficientes para graficar el churn rate.")
                return

            import pandas as pd
            df = pd.DataFrame(data)
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=df, x='Periodo', y='ChurnRate (%)', hue='Proveedor', marker='o')
            plt.title('Evolución del Churn Rate por Trimestre y Proveedor')
            plt.xlabel('Trimestre')
            plt.ylabel('Churn Rate (%)')
            plt.xticks(rotation=45)
            plt.legend(title='Proveedor')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"[ERROR] No se pudo generar el gráfico de churn rate: {e}")
        finally:
            session.close()










