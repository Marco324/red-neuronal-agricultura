# Preprocesamiento de Datos

Antes de introducir los datos a la Red Neuronal, es indispensable limpiar y transformar matemáticamente los valores. Las redes neuronales requieren que toda la información esté en formato numérico y preferiblemente en la misma escala (normalizada) para asegurar que el algoritmo de descenso de gradiente converja correctamente.

En el archivo `redNeuronal.ipynb`, se realizaron los siguientes pasos:

## 1. Estandarización de Nombres de Columnas
Se convirtieron todos los nombres de las columnas a letras minúsculas para evitar errores de sintaxis y facilitar el acceso a las variables:
`df.columns = df.columns.str.lower()`

## 2. Limpieza de Datos (EDA)
Se verificó la existencia de valores nulos (datos faltantes) usando `df.isnull().sum()`. Al confirmar que el dataset estaba limpio, nos aseguramos de no tener que descartar filas ni aplicar técnicas de imputación (rellenado de datos).

## 3. Separación de Variables (X e y)
Se dividió el conjunto de datos en las variables independientes (características) y la variable dependiente (objetivo a predecir).
* **`X` (Características):** `n`, `p`, `k`, `temperature`, `humidity`, `ph`, `rainfall`.
* **`y` (Objetivo):** `label` (El tipo de cultivo).

## 4. Codificación de la Variable Objetivo (Label Encoding)
Como la red neuronal no puede predecir texto plano como "rice" o "coffee", se utilizó la herramienta `LabelEncoder` de la librería `scikit-learn` para convertir las 22 etiquetas de texto en números enteros del 0 al 21.

## 5. División en Set de Entrenamiento y Prueba (Train/Test Split)
Para validar que el modelo no estuviera "memorizando" (sobreajuste / overfitting), se dividieron los datos:
* **80% Entrenamiento (`X_train`, `y_train`):** Usados para que el modelo aprenda los patrones.
* **20% Prueba (`X_test`, `y_test`):** Datos ocultos al modelo, usados únicamente para evaluar su precisión final.

## 6. Escalamiento de Datos (StandardScaler)
Variables como `rainfall` tienen valores en cientos (ej. 200 mm), mientras que el `ph` tiene valores pequeños (ej. 6.5). Si se introducen así, la red podría darle más importancia artificial a la lluvia solo porque el número es más grande.
Se utilizó `StandardScaler` para normalizar todas las columnas numéricas de manera que tengan una media de 0 y una desviación estándar de 1. Es importante destacar que el escalador se ajustó (`fit`) solo con los datos de entrenamiento para evitar el sesgo de asomarse a los datos de prueba (Data Leakage).
