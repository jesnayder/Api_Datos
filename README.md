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
| `PROVEEDOR`            | Nombre del operador móvil (ej. Avantel, Uff Movil, Virgin Mobile, etc.).           |
| `LINEAS EN SERVICIO`   | Total de líneas móviles activas en ese trimestre.                              |
| `LINEAS PREPAGO`       | Número de líneas prepago activas.                                              |
| `LINEAS POSPAGO`       | Número de líneas pospago activas.                                              |
| `LÍNEAS ACTIVADAS`     | Cantidad de nuevas líneas activadas en ese periodo.                            |
| `LÍNEAS RETIRADAS`     | Número de líneas canceladas o retiradas durante el trimestre.                  |

Este conjunto de datos permite observar el comportamiento del mercado móvil a lo largo del tiempo, detectar cambios en la base de usuarios y comparar la evolución de diferentes tipos de línea y proveedores.

---

## Tecnologías Utilizadas

- **Lenguaje**: Python
- **Consumo de API**: `requests`
- **Almacenamiento**: Base de datos relacional (PostgreSQL)

---

## Avances y Entregables

Se irá documentando aquí el progreso del desarrollo, los resultados obtenidos y los dashboards o visualizaciones construidas para apoyar el análisis.

---

## Autores

- Jesnayder Pedrozo
- Carlos Ruiz
