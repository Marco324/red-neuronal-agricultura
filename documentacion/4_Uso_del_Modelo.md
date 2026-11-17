# Resultados y Uso del Modelo

Tras el entrenamiento de la arquitectura diseñada, la red neuronal ha demostrado una capacidad excepcional para modelar la relación biológica entre los requerimientos edafoclimáticos y los cultivos.

## Desempeño (Resultados)
* **Precisión en Prueba:** **98.5%** (330 muestras que el modelo nunca vio durante el entrenamiento)
* **Pérdida en Prueba:** 0.037

En el notebook la evaluación incluye:
* **Curvas de aprendizaje:** precisión y pérdida por época en entrenamiento y en validación. Que ambas curvas avancen juntas indica que el modelo generaliza y no sobreajusta.
* **Reporte de clasificación:** precisión, *recall* y F1 por cada cultivo.
* **Matriz de confusión:** muestra qué cultivos se confunden entre sí.

Los valores pueden variar ligeramente según el hardware, pero con la semilla fija la ejecución es reproducible en la misma máquina.

## Implementación de la Función de Predicción

Para que el modelo tenga utilidad en el mundo real, se construyó una función programática (API interna) que simula la interacción de un usuario final (un agricultor o ingeniero agrónomo) con la Inteligencia Artificial.

### Flujo de la Función `recomendar_cultivo()`
1. **Recepción de Datos:** El usuario introduce los 7 parámetros de un análisis de suelo y las medias climáticas esperadas.
2. **Formato:** Los datos se agrupan en un `DataFrame` de 1 fila por 7 columnas, con los mismos nombres de columna que en el entrenamiento.
3. **Escalamiento:** Crucialmente, los valores se normalizan utilizando el mismo objeto `StandardScaler` (`scaler.transform()`) empleado durante el entrenamiento. Sin este paso, la red recibiría datos en escalas que no comprende y arrojaría un resultado erróneo.
4. **Inferencia:** El modelo entrenado recibe los datos limpios y emite 22 porcentajes (probabilidades de éxito de cada cultivo).
5. **Decisión:** Con `np.argsort` se ordenan los cultivos por probabilidad y se toman los mejores (por defecto, el top 3).
6. **Decodificación:** Se utiliza `label_encoder.inverse_transform` para convertir cada ID numérico de vuelta a un texto humano comprensible (ej. de la clase `3` a `'chickpea'`). La función devuelve una lista de pares `(cultivo, probabilidad)`.

### Simulación Regional
Como parte de las pruebas del PIA, se introdujeron datos regionales correspondientes al clima del **noreste de México (Monterrey, Nuevo León)**, caracterizado por suelos calcáreos, alta alcalinidad (pH 7.8), alto potasio y climas cálidos y semiáridos, validando la coherencia biológica de las predicciones arrojadas por la red.
