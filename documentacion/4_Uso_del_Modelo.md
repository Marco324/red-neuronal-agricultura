# Resultados y Uso del Modelo

Tras el entrenamiento de la arquitectura diseñada, la red neuronal ha demostrado una capacidad excepcional para modelar la relación biológica entre los requerimientos edafoclimáticos y los cultivos.

## Desempeño (Resultados)
* **Precisión en Entrenamiento (`accuracy`):** ~96%
* **Precisión en Validación (`val_accuracy`):** ~95%
La similitud entre estas métricas demuestra que el modelo ha generalizado bien, superando los problemas de sobreajuste presentados en pruebas tempranas con datos aleatorios.

## Implementación de la Función de Predicción

Para que el modelo tenga utilidad en el mundo real, se construyó una función programática (API interna) que simula la interacción de un usuario final (un agricultor o ingeniero agrónomo) con la Inteligencia Artificial.

### Flujo de la Función `recomendar_cultivo()`
1. **Recepción de Datos:** El usuario introduce los 7 parámetros de un análisis de suelo y las medias climáticas esperadas.
2. **Formato:** Los datos se agrupan en una matriz NumPy de 1 fila por 7 columnas.
3. **Escalamiento:** Crucialmente, los valores se normalizan utilizando el mismo objeto `StandardScaler` (`scaler.transform()`) empleado durante el entrenamiento. Sin este paso, la red recibiría datos en escalas que no comprende y arrojaría un resultado erróneo.
4. **Inferencia:** El modelo entrenado recibe los datos limpios y emite 22 porcentajes (probabilidades de éxito de cada cultivo).
5. **Decisión:** Usando `np.argmax`, se identifica el cultivo que obtuvo la mayor probabilidad.
6. **Decodificación:** Se utiliza `label_encoder.inverse_transform` para convertir el ID numérico ganador de vuelta a un texto humano comprensible (ej. de la clase `3` a `'chickpea'`).

### Simulación Regional
Como parte de las pruebas del PIA, se introdujeron datos regionales correspondientes al clima del **noreste de México (Monterrey, Nuevo León)**, caracterizado por suelos calcáreos, alta alcalinidad (pH 7.8), alto potasio y climas cálidos y semiáridos, validando la coherencia biológica de las predicciones arrojadas por la red.
