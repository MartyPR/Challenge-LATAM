
## Parte I: Ajustes y Mejoras en el Modelo

1. Definición del Modelo DelayModel
El modelo DelayModel fue diseñado para predecir los retrasos de vuelos a partir de un conjunto específico de características (features). Para ello, se utilizan los siguientes pasos:

Preprocesamiento de datos: Se aplicaron varias técnicas de transformación, entre ellas:
- Dummies para las columnas categóricas como OPERA (operadora aérea) y TIPOVUELO (tipo de vuelo).
- Creación de la columna min_diff que calcula la diferencia de minutos entre la fecha de salida y la fecha de llegada.
- Asignación de un valor binario a la columna objetivo (delay) que indica si el vuelo tuvo un retraso mayor a 15 minutos.
- Ajuste del modelo: Se utilizó la regresión logística con un ajuste de balance de clases para entrenar el modelo en un conjunto de datos desequilibrado, donde la mayoría de los vuelos no tienen retrasos. El archivo del modelo es guardado localmente con pickle para su reutilización.
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