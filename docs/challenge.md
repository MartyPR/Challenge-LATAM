
## Parte I: Ajustes y Mejoras en el Modelo

1. Definición del Modelo DelayModel
El modelo DelayModel fue diseñado para predecir los retrasos de vuelos a partir de un conjunto específico de características (features). Para ello, se utilizan los siguientes pasos:

Preprocesamiento de datos: Se aplicaron varias técnicas de transformación, entre ellas:
- Dummies para las columnas categóricas como OPERA (operadora aérea) y TIPOVUELO (tipo de vuelo).
- Creación de la columna min_diff que calcula la diferencia de minutos entre la fecha de salida y la fecha de llegada.
- Asignación de un valor binario a la columna objetivo (delay) que indica si el vuelo tuvo un retraso mayor a 15 minutos.
- Ajuste del modelo: Se utilizó la regresión logística con un ajuste de balance de clases para entrenar el modelo en un conjunto de datos desequilibrado, donde la mayoría de los vuelos no tienen retrasos. El archivo del modelo es guardado localmente con pickle para su reutilización.

### Logistic Regression 
Logistic Regression es uno de los modelos más simples y fáciles de interpretar. Ofrece una probabilidad de que un evento ocurra (en este caso, un retraso), y  permite ver claramente cómo cada característica contribuye a la predicción.

Coeficientes claros: Con Logistic Regression, puedes interpretar directamente los coeficientes del modelo para saber qué características aumentan o disminuyen la probabilidad de retraso.
Relaciones lineales: El modelo asume una relación lineal entre las variables independientes y la log-odds (la probabilidad logarítmica de un evento), lo cual es más fácil de explicar.

- Logistic Regression es computacionalmente eficiente. Funciona bien con conjuntos de datos pequeños y medianamente grandes, lo que permite un entrenamiento rápido y eficiente, algo importante si estás haciendo iteraciones frecuentes en tu modelo.

- El uso de Class Weight: En el código se ha especificado class_weight='balanced', lo cual es útil en situaciones de clases desbalanceadas porque ajusta los pesos de cada clase para que el modelo preste más atención a la clase minoritaria.

- Dado que Logistic Regression es un modelo relativamente simple, tiene menos riesgo de overfitting comparado con modelos más complejos como los árboles de decisión o XGBoost, especialmente si tienes un número limitado de muestras o características.

*Nota*:  Logistic Regression es un buen punto de partida para este caso debido a que es simple, interpretable y eficiente.  especialmente en un entorno donde se priorizan las iteraciones rápidas

2. Características seleccionadas para el modelo
El modelo fue entrenado utilizando las siguientes columnas (features):

`OPERA_Latin American Wings`,
`OPERA_Grupo LATAM`,
`OPERA_Sky Airline`,
`OPERA_Copa Air`,
`TIPOVUELO_I`,
`MES_7`,
`MES_10`,
`MES_12`,
`MES_4`,
`MES_11`.
Estas características se seleccionaron tras analizar el impacto de cada una en la probabilidad de retraso.

3. Guardado y carga del modelo
El modelo se guarda utilizando pickle en un archivo delay_model.pkl, que es reutilizado posteriormente en el API para realizar predicciones.

4. Predicciones
Las predicciones se realizan utilizando la función predict, que carga el modelo si no está ya en memoria y realiza predicciones basadas en las características preprocesadas de nuevos datos de vuelos.

## Parte II: API para la predicción de retrasos en vuelos

1. Estructura de la API con FastAPI
Se implementó un API utilizando FastAPI para proporcionar predicciones de retrasos en vuelos a través de un endpoint /predict.

2. Definición del Endpoint /predict
El endpoint acepta datos de vuelos en formato JSON y devuelve una lista de predicciones que indica si un vuelo tendrá un retraso o no.

Estructura del Request:

Cada vuelo tiene los siguientes atributos:
`OPERA` (nombre de la aerolínea),
`TIPOVUELO` (tipo de vuelo: nacional o internacional),
`MES` (mes del vuelo),
`Fecha_I` (fecha de inicio del vuelo),
`Fecha_O` (fecha de término del vuelo).
Los campos `Fecha_I` y `Fecha_O` son opcionales, y se asigna un valor predeterminado en caso de que no sean proporcionados.

Estructura del Response:

Devuelve una lista con las predicciones de retraso, donde 1 indica que el vuelo se retrasará más de 15 minutos, y 0 indica que no lo hará.
3. Manejo de errores
Si el mes (MES) está fuera del rango permitido (1 a 12), se genera una excepción y la API devuelve un error con un código 400.
4. Endpoint de verificación /health
Además, se implementó un endpoint simple /health que devuelve el estado de salud del API, confirmando que el servicio está activo.


## Parte III: Mejoras y optimizaciones propuestas
1. Variables de entorno para mayor flexibilidad
Para mejorar la flexibilidad del código y permitir cambios más rápidos sin tocar el código fuente, se sugiere mover algunos parámetros importantes a variables de entorno, tales como:

`THRESHOLD_IN_MINUTES`: El umbral de minutos que define si un vuelo se considera retrasado.
`MODEL_FILE_NAME`: El nombre del archivo del modelo guardado.

2. Almacenamiento del modelo en la nube
Actualmente, el modelo se guarda localmente, pero una mejora sería almacenar el modelo entrenado en servicios de almacenamiento como Google Cloud Storage (GCS) para facilitar su distribución y acceso en un entorno de producción.

## Parte IV: Flujo de trabajo GitFlow y despliegue
1. Uso de GitFlow
Para organizar el desarrollo, se implementó GitFlow en el repositorio, utilizando las siguientes ramas:

Main: Para versiones oficiales y producción.
Develop: Para desarrollo continuo e integración.
Feature: Se crean ramas de características específicas (como la predicción de retrasos) y, una vez completadas, se fusionan en develop.
2. Flujo de CI/CD
CI: Se configura un flujo de integración continua que se ejecuta en cada push o pull request a las ramas develop o main. Este flujo se encarga de ejecutar los tests y verificar que todo funcione correctamente antes de integrar los cambios.
CD: Se implementa un flujo de despliegue continuo que se activa cuando hay cambios en la rama main, desplegando la nueva versión del API en un entorno de producción.
3. Despliegue en CloudRun
El contenedor que contiene la API se despliega en Google Cloud Platform usando CloudRun, un servicio que permite el despliegue de contenedores escalables de forma automática.