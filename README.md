# Proyecto ETL: Data Warehouse de Fórmula 1

**Maestría de Ciencia de Datos - Universidad San Francisco de Quito**  
**Materia:** Ingeniería de Datos  
**Autor:** Nicolás Carrión  

Este repositorio contiene la implementación completa de un pipeline ETL (Extracción, Transformación y Carga) para datos históricos de la Fórmula 1. El proceso integra múltiples motores de bases de datos, centralizando la información dispersa en un modelo estrella (Star Schema) estructurado para el análisis analítico.

## Arquitectura y Prerrequisitos
* **Lenguaje:** Python 3.10
* **Herramienta ETL:** KNIME Analytics Platform (v5.12.0)
* **Infraestructura:** Docker y Docker Compose
* **Orígenes de Datos:** PostgreSQL, MySQL, MongoDB y archivos planos (CSV)
* **Destino (Data Warehouse):** PostgreSQL (`f1_dw`)

## Pasos del Proceso
El ciclo de vida del dato en este proyecto se divide en las siguientes fases:

1. **Despliegue de Infraestructura:** Los motores de bases de datos relacionales y NoSQL se levantan de forma aislada mediante contenedores de Docker.
2. **Obtención de Datos:** El script `descargar_datos.py` automatiza la conexión con Kaggle, descargando el dataset original y filtrando estrictamente los 6 archivos CSV necesarios para el modelo.
3. **Poblado de Orígenes:** El script `cargar_origenes.py` distribuye los datos crudos hacia los distintos motores simulando un entorno transaccional real.
4. **Modelado Dimensional:** El script `crear_dw.py` genera el esquema DDL del Data Warehouse, estableciendo 5 tablas de dimensiones (`drivers`, `constructors`, `circuits`, `races_time`, `status`) y 1 tabla de hechos (`fact_results`) con sus respectivas llaves foráneas.
5. **Pipeline en KNIME:** 
   * **Extracción:** Lectura simultánea desde los 4 orígenes de datos.
   * **Transformación:** Limpieza de valores nulos, estandarización de columnas y conversión rigurosa de tipos de datos.
   * **Carga:** Inserción en bloque hacia PostgreSQL, utilizando variables de flujo para orquestar la carga de dimensiones antes que la tabla de hechos.
6. **Validación:** Ejecución de consultas SQL analíticas a través de `validaciones_dw.ipynb` para comprobar la integridad del modelo.

## Guía de Reproducción

Para ejecutar este proyecto localmente, sigue estos comandos en orden:

**1. Levantar contenedores**
```bash
docker-compose up -d

```

**2. Obtener y preparar el entorno de datos**

```bash
python descargar_datos.py
python cargar_origenes.py
python crear_dw.py

```

**3. Ejecutar el ETL**

* Abre KNIME Analytics Platform.
* Ejecuta el flujo de trabajo del directorio `workflow/ETL_Formula1_DW` (exportado en el archivo `workflow/ETL_Formula1_DW.knwf`).

**4. Validar resultados**

* Abre y ejecuta las celdas del archivo `notebooks/validaciones_dw.ipynb`.

**5. Detener infraestructura**

```bash
docker-compose down

```