# Análisis de Fidelización y Comparación de Proveedores de Servicios Móviles en Colombia (Desde 2022)

## Objetivo del Proyecto

Este proyecto busca analizar el comportamiento de los proveedores de servicios móviles en Colombia a partir del año 2022, con un enfoque en la fidelización de clientes y la comparación entre operadores.

Utilizando datos trimestrales sobre líneas móviles activadas, retiradas y en servicio, el análisis se centra en responder preguntas clave como:

- ¿Qué proveedores presentan mejores o peores índices de fidelización?
- ¿Cómo se compara el volumen de líneas retiradas respecto a las líneas activadas y en servicio?
- ¿Qué tendencias se observan en la retención y abandono de clientes a lo largo del tiempo?

Este análisis es útil para evaluar la estabilidad y competitividad del mercado móvil, ayudando a entender la capacidad de los operadores para mantener su base de clientes y detectar posibles periodos críticos.

---

## Estructura del Dataset

El dataset contiene información histórica sobre el comportamiento de las líneas móviles en Colombia, clasificada por trimestre, año y proveedor. Cada registro representa los datos de un proveedor específico en un trimestre determinado.

| **Campo**              | **Descripción**                                                                 |
|------------------------|---------------------------------------------------------------------------------|
| `AÑO`                  | Año calendario del registro (por ejemplo, 2022, 2023).                         |
| `TRIMESTRE`            | Trimestre del año (1, 2, 3 o 4).                                                |
| `PROVEEDOR`            | Nombre del operador móvil (ej. Avantel, Uff Movil, Virgin Mobile, etc.).        |
| `LINEAS EN SERVICIO`   | Total de líneas móviles activas en ese trimestre.                               |
| `LINEAS PREPAGO`       | Número de líneas prepago activas.                                               |
| `LINEAS POSPAGO`       | Número de líneas pospago activas.                                               |
| `LÍNEAS ACTIVADAS`     | Cantidad de nuevas líneas activadas en ese periodo.                             |
| `LÍNEAS RETIRADAS`     | Número de líneas canceladas o retiradas durante el trimestre.                   |

Este conjunto de datos permite observar el comportamiento del mercado móvil a lo largo del tiempo, detectar cambios en la base de usuarios y comparar la evolución de diferentes tipos de línea y proveedores.

---

## Tecnologías Utilizadas

- **Lenguaje**: Python
- **Consumo de API**: `requests`
- **Almacenamiento**: Base de datos relacional (PostgreSQL o SQLite)
- **ORM**: SQLAlchemy
- **Visualización**: matplotlib, seaborn, pandas
- **Interfaz de usuario**: Menú CLI (línea de comandos)

---

## Instalación y Ejecución

1. **Clona el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Api_Datos-main

2. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    
Si tienes el archivo `requirements.txt`, simplemente ejecuta:

    pip install sqlalchemy matplotlib seaborn pandas requests

3. **Configura la base de datos:**

El proyecto utiliza SQLAlchemy. Asegúrate de tener configurado el archivo de conexión en la carpeta `db`/.

4. **Ejecuta el menú principal:**
    ```bash
    python main.py

---

## Funcionalidades principales

- Importación de datos desde una API externa.
- Listado de estaciones por año.
- Cálculo de índices de retención total ponderado (IRT) por proveedor.
- Top 5 de proveedores con mayor y menor IRT.
- Cálculo y resumen de tasa de cancelación y relación líneas retiradas/activadas.
- Gráficos de evolución de retención y churn rate por trimestre y proveedor.
- Menú CLI para una interacción sencilla e intuitiva.

---

## Visualización

- Los gráficos de retención y churn rate se generan utilizando `matplotlib` y `seaborn`.
- El eje X representa los trimestres (por ejemplo, `2022-Q1`), y el eje Y muestra el porcentaje de retención o churn.
- Cada línea del gráfico representa un proveedor distinto.
- Los gráficos incluyen leyenda, título y etiquetas rotadas para una mejor visualización.

---

## Autores

- Jesnayder Pedrozo
- Carlos Ruiz
