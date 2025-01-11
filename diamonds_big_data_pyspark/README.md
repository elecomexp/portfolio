# Clasificador de diamantes con PySpark en DataBricks

Este proyecto tiene como objetivo realizar la **clasificación de diamantes** según su **categoría** utilizando **PySpark** en un entorno de **Big Data**. A través de este análisis, entrenamos y evaluamos clasificadores para predecir la categoría de los diamantes en base a sus características. El proyecto incluye la implementación de técnicas de **feature selection**, **entrenamiento de clasificadores Random Forest y Gradient Boosting Trees (GBT)**, así como la aplicación de **OneHotEncoder** y **OrdinalEncoder**.

## Requisitos

Este proyecto está diseñado para ejecutarse en [DataBricks](https://www.databricks.com/), utilizando **DataFrames de PySpark** para procesar y analizar grandes volúmenes de datos. La plataforma **Databricks** permite ejecutar el código de manera distribuida y optimizada, aprovechando el poder de [Apache Spark](https://spark.apache.org/). La versión gratuita de **Databricks Community Edition** es suficiente para ejecutar este proyecto.

## Descripción del Proyecto

El **dataset de diamantes** contiene información sobre características como el corte, color, claridad, tamaño o precio de los diamantes. El objetivo del proyecto es construir un clasificador que prediga la **categoría** del diamante basada en estas características.

Este proyecto no está enfocado en un análisis profundo del dataset o en la optimización de los modelos, sino en hacer uso de herramientas y técnicas comunes en el procesamiento de Big Data. El objetivo principal es familiarizarse con el uso de Databricks y PySpark en un entorno de Big Data para proyectos de Machine Learning.

## Configuración de DataBricks

- Versión de Databricks Runtime: 12.2 LTS (incluye Apache Spark 3.3.2, Scala 2.12)
- Tipo de Driver: "Community Optimized", 15.2 GB de memoria, 2 núcleos.
- Configuración de Spark: spark.databricks.rocksDB.fileManager.useCommitService false
- Variables de entorno: PYSPARK_PYTHON=/databricks/python3/bin/python3

## Uso del Notebook

Este notebook está diseñado para ejecutarse dentro de un entorno **Databricks**. Para ejecutar los pasos:

1. Importar el Notebook: Carga este notebook en Databricks desde el repositorio.
2. Configurar el Entorno de Spark: Asegúrate de que tu clúster de Databricks tenga Spark configurado correctamente con la información anterior.
3. Ejecutar las Celdas: Sigue las instrucciones en cada celda para cargar los datos, realizar el análisis, entrenar los modelos y evaluarlos.
