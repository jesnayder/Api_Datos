# Análisis de Cancelación de Líneas Móviles en Colombia

## Objetivo del Proyecto

Este proyecto tiene como finalidad desarrollar una aplicación de análisis de datos que consuma información desde una API pública, la almacene en una base de datos relacional y permita realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar). 

El enfoque principal del análisis está en el comportamiento de las líneas móviles en Colombia, con especial atención a las líneas **retiradas** por proveedor de servicios móviles a lo largo del tiempo (por año y trimestre). Este análisis busca responder preguntas clave como:

- ¿Qué proveedores presentan mayores volúmenes de líneas retiradas?
- ¿Existen periodos con un incremento significativo en la cancelación de líneas?
- ¿Cómo se comparan las líneas retiradas con las líneas activas en cada trimestre?

### Justificación

Comprender las tendencias de retiro de líneas móviles puede aportar información valiosa para:

- Evaluar la **competitividad** en el mercado móvil colombiano.
- Identificar posibles problemas de **fidelización** o **satisfacción del cliente**.
- Apoyar estudios sobre la **calidad del servicio** de los distintos operadores móviles.
- Detectar patrones estacionales o cambios relevantes en el comportamiento del usuario.

---

## Estructura del Dataset

El dataset contiene información histórica sobre el comportamiento de las líneas móviles en Colombia, clasificada por trimestre, año y proveedor. Cada registro representa los datos de un proveedor específico en un trimestre determinado.

| **Campo**              | **Descripción**                                                                 |
|------------------------|---------------------------------------------------------------------------------|
| `AÑO`                  | Año calendario del registro (por ejemplo, 2021, 2022).                         |
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
