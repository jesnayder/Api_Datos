import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def graficar_retencion_por_trimestre(resumen):
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


def graficar_churnrate_por_trimestre(resumen):
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
