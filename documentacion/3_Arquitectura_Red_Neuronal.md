# Arquitectura de la Red Neuronal

El modelo de predicción de cultivo se construyó utilizando la librería **TensorFlow / Keras**. Se diseñó una red neuronal profunda "Feed Forward" a través del API `Sequential`.

La arquitectura está diseñada específicamente para resolver un problema de **Clasificación Multiclase** (predecir entre 22 posibles cultivos basándose en parámetros ambientales).

## Estructura del Modelo

1. **Capa de Entrada (Implícita en Keras):**
   - Recibe 7 valores (las 7 características numéricas del suelo y clima: N, P, K, Temp, Humedad, pH, Lluvia).

2. **Capa Oculta 1:**
   - **Neuronas:** 64
   - **Función de Activación:** `ReLU` (Rectified Linear Unit). Permite al modelo aprender patrones no lineales, apagando las neuronas con resultados negativos.
   - **Capa de Regularización (Dropout):** 20% (`0.2`). Se apaga aleatoriamente el 20% de las neuronas en cada época para prevenir el sobreajuste (overfitting).

3. **Capa Oculta 2:**
   - **Neuronas:** 32
   - **Función de Activación:** `ReLU`. Extrae características más complejas a partir de los patrones descubiertos por la capa anterior.

4. **Capa de Salida:**
   - **Neuronas:** 22 (Una neurona para cada uno de los 22 tipos de cultivo).
   - **Función de Activación:** `Softmax`. Convierte los valores de salida en probabilidades matemáticas que suman 1 (o 100%). La neurona con el porcentaje más alto determina la decisión final del modelo.

---

## Compilación y Parámetros de Aprendizaje

- **Optimizador (`adam`):** Adaptative Moment Estimation. Es el algoritmo encargado de actualizar los pesos de las neuronas de manera eficiente, adaptando su tasa de aprendizaje sobre la marcha.
- **Función de Pérdida (`sparse_categorical_crossentropy`):** Mide la distancia matemática entre la predicción de la red y la respuesta real. Al ser "sparse", evita la necesidad de aplicar "One-Hot Encoding" manual a la variable objetivo (y).
- **Métricas (`accuracy`):** Permite visualizar el porcentaje de aciertos correctos de la red durante cada época de entrenamiento.

## Entrenamiento
El modelo se entrena durante múltiples iteraciones (`epochs`, típicamente entre 50 y 100) en lotes pequeños (`batch_size = 32`). Durante el proceso, se evalúa constantemente contra los datos de prueba (`val_accuracy`) para garantizar que la red esté generalizando los patrones biológicos y no memorizando.
