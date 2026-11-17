# Plan de Mejora del Proyecto

Este documento recoge las mejoras propuestas para el proyecto. Hay dos objetivos principales:

1. **Que el proyecto se pueda instalar y ejecutar sin pasos manuales.**
2. **Agregar una interfaz gráfica sencilla (UI)** para que cualquier persona pueda pedir una recomendación de cultivo sin tocar el notebook.

---

## Problemas actuales

| # | Problema | Impacto |
|---|----------|---------|
| 1 | No hay `requirements.txt`. Las dependencias se instalaron a mano porque había problemas de compatibilidad con las versiones más recientes de Python. | Cada integrante tiene que adivinar qué versiones instalar. |
| 2 | No está documentada la versión de Python. TensorFlow no siempre sale a tiempo para la versión más nueva de Python. | Al instalar en un Python nuevo, `pip install tensorflow` falla. |
| 3 | El modelo se vuelve a entrenar en cada ejecución y no se guarda. | No se puede usar el modelo sin correr todo el notebook. |
| 4 | El conjunto de prueba se usa también como `validation_data`. | Las métricas reportadas (~95 %) salen optimistas, porque no hay un conjunto de prueba realmente independiente. |
| 5 | No hay semillas fijas en TensorFlow ni en NumPy. | Los resultados cambian ligeramente entre ejecuciones. |
| 6 | Hay detalles menores en el notebook: `df.info` sin paréntesis; `crosstab` sobre variables continuas (temperatura, pH), que genera tablas enormes sin utilidad; y un comentario de la celda de predicción que no coincide con los valores usados. | Confunden al lector y alargan la salida. |
| 7 | No se muestran métricas por clase (matriz de confusión, reporte de clasificación) ni curvas de entrenamiento. | La evaluación del modelo es incompleta para el PIA. |

---

## Fase 1: Instalación reproducible (prioridad alta)

- [x] Fijar la versión de Python soportada (actualmente **3.12**, probada con TensorFlow 2.21) y documentarla en un `README.md`.
- [x] Crear `requirements.txt` con versiones fijadas. Versiones que funcionan hoy en el `.venv`:
  ```
  tensorflow==2.21.0
  keras==3.15.1
  numpy==2.5.3
  pandas==3.0.6
  scikit-learn==1.9.1
  seaborn==0.13.2
  matplotlib==3.11.2
  ```
- [x] Escribir un `README.md` con los pasos de instalación:
  ```
  py -3.12 -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  ```
- [x] Instalación automática multiplataforma: celda «Instalación de dependencias» al inicio del notebook (reemplazó a un `setup.bat`, que solo servía en Windows).

## Fase 2: Limpieza del notebook (prioridad alta)

- [x] Fijar las semillas (`tf.keras.utils.set_random_seed(42)`).
- [x] Dividir los datos en **entrenamiento / validación / prueba** (p. ej. 70/15/15) y evaluar con `modelo.evaluate()` sobre la prueba al final.
- [x] Agregar las gráficas de `accuracy` y `loss` por época, la matriz de confusión y el `classification_report`.
- [x] Añadir `EarlyStopping` para no depender de un número fijo de épocas.
- [x] Corregir `df.info()`, eliminar o reemplazar los `crosstab` de variables continuas y arreglar el comentario de la predicción.
- [x] Usar `keras.Input(shape=...)` en lugar de `input_shape=` (este último está obsoleto en Keras 3).

## Fase 3: Separar el código del notebook (prioridad media)

Pasar la lógica a módulos reutilizables para que el notebook, la UI y cualquier script usen el mismo código:

```
src/
  datos.py        # carga y preprocesamiento
  modelo.py       # construcción y entrenamiento de la red
  predecir.py     # cargar el modelo guardado y recomendar cultivo
entrenar.py       # script: entrena y guarda el modelo
```

- [ ] Guardar el modelo entrenado (`modelo.keras`), el `scaler` y el `label_encoder` (`joblib`) en una carpeta `modelos/`.
- [ ] Hacer que la predicción cargue esos archivos en lugar de reentrenar.
- [ ] Decidir si el modelo entrenado se sube al repositorio. El `.gitignore` excluye ahora `*.keras`, `*.pkl` y `modelos/`; si se va a entregar, hay que ajustarlo o forzarlo con `git add -f`.

## Fase 4: Interfaz de uso sencillo (objetivo principal)

Una UI donde el usuario capture los 7 parámetros y vea el cultivo recomendado.

**Opción recomendada: Streamlit**
- Es una app web local hecha en Python puro, con poco código (unas 50 líneas).
- Se ejecuta con `streamlit run app.py`.
- Funciones:
  - Controles deslizantes o campos numéricos para N, P, K, temperatura, humedad, pH y lluvia, con rangos tomados del dataset.
  - Botón «Recomendar».
  - El cultivo recomendado y el **top 3 con su probabilidad**.
  - (Opcional) Gráfica de barras con las probabilidades.

**Alternativas:**
- **Gradio:** igual de sencilla y genera un enlace para compartir.
- **ipywidgets dentro del notebook:** no requiere instalar nada más, pero sigue dependiendo de Jupyter.
- **Tkinter:** app de escritorio sin dependencias extra, aunque con más código y una apariencia más básica.

## Fase 5: Extras (prioridad baja)

- [ ] Comparar con modelos clásicos (Random Forest, KNN) como referencia en el reporte.
- [ ] Validar las entradas de la UI (rangos físicos razonables) y avisar cuando los valores estén fuera de lo visto en el entrenamiento.
  - Hecho en el notebook: `recomendar_cultivo()` avisa cuando un valor está fuera del rango del dataset. Falta llevarlo a la UI.
- [ ] ~~Expandir el dataset~~: se descartó generar datos sintéticos, porque serían datos agronómicos inventados. Solo se ampliaría con un dataset real y citado.
- [ ] Actualizar `4_Uso_del_Modelo.md` con el uso de la UI (las nuevas métricas ya están documentadas).

---

## Orden sugerido

1. Fase 1 → 2. Fase 2 → 3. Fase 3 → 4. Fase 4 (UI) → 5. Fase 5

Las fases 1 y 2 son rápidas y mejoran la entrega de inmediato. La fase 3 es requisito para la UI.
