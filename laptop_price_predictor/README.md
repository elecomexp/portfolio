# Predictor de precios de ordenadores portátiles

Este proyecto tiene como objetivo desarrollar un modelo de Machine Learning para predecir los precios de portátiles, basándose en diversas características de los productos, como especificaciones técnicas, marca, almacenamiento, entre otras. El modelo busca ayudar a Lucas, el dueño de una tienda de portátiles, a establecer precios más adecuados para sus productos, optimizando la venta y mejorando la rentabilidad.

## Objetivo

El objetivo principal es predecir el precio de los portátiles en euros mediante un modelo de regresión. Para ello, se entrenará un modelo utilizando diferentes características de los portátiles disponibles en el dataset.

## Métrica de Evaluación

La evaluación del modelo se realizará mediante el **Error de Raíz Cuadrada Media (RMSE)**, que es una métrica de regresión que mide la desviación estándar de los errores de predicción, proporcionando una medida de cuán cerca o lejos están las predicciones del valor real. Un menor valor de RMSE indica un modelo más preciso.

## Estructura del proyecto

```bash
laptop_price_predictor/
├── docs/                # Documentación adicional
│
├── src/                 # Directorio principal del código fuente
│   ├── data/            # Archivos de datos
│   ├── img/             # Imágenes generadas y usadas
│   ├── models/          # Modelos entrenados y guardados
│   ├── notebooks/       # Jupyter Notebooks con análisis de datos y modelos
│   ├── submissions/     # Archivos con los resultados finales
│   ├── utils/           # Funciones auxiliares y herramientas
│
├── README.md            # Archivo de documentación principal
└── requirements.txt     # Dependencias necesarias para el proyecto
```

## Versión de Python

Este proyecto ha sido desarrollado utilizando Python 3.12.4.