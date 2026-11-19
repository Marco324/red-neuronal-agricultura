# Red Neuronal: Predicción de Tipo de Cultivo

Producto Integrador de Aprendizaje (PIA) — Facultad de Ingeniería Mecánica y Eléctrica, UANL.

Red neuronal (TensorFlow/Keras) que recomienda el cultivo más adecuado a partir de 7 parámetros del suelo y el clima: nitrógeno (N), fósforo (P), potasio (K), temperatura, humedad, pH y lluvia. Se entrena con el dataset `Crop_recommendation.csv`.

## Requisitos

- **Python 3.12.** Las versiones más nuevas de Python pueden no ser compatibles todavía con TensorFlow, y `pip install` fallaría.
- Windows, macOS o Linux.

## Instalación

### Opción más sencilla: desde el notebook

1. Abre `redNeuronal.ipynb` en PyCharm, VS Code o Jupyter con cualquier intérprete de **Python 3.12**.
2. Ejecuta la celda **«Instalación de dependencias»**. Revisa la versión de Python e instala automáticamente lo que falte de `requirements.txt`.

> Se recomienda usar un entorno virtual (`.venv`) para no mezclar estas librerías con otros proyectos. Puedes crearlo con la opción de abajo o desde PyCharm (*Settings → Python Interpreter → Add Interpreter → Virtualenv*).

### Opción manual (terminal)

**Windows**
```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**macOS / Linux**
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

1. Abre `redNeuronal.ipynb` en PyCharm, VS Code o Jupyter.
2. Selecciona como intérprete o kernel el Python de `.venv`:
   - Windows: `.venv\Scripts\python.exe`
   - macOS/Linux: `.venv/bin/python`
3. Ejecuta todas las celdas en orden. La última celda usa la función `recomendar_cultivo(N, P, K, temperatura, humedad, ph, lluvia)` para hacer una predicción.

## Interfaz de escritorio

`interfaz.py` es una ventana de escritorio (Tkinter, incluido en Python) que usa la red ya
entrenada: se escriben los 7 datos del terreno y muestra los 3 cultivos más probables con su
probabilidad. No entrena nada, solo consume el modelo.

Necesita que el notebook se haya corrido completo al menos una vez, porque la última celda
(«Guardar el modelo para la interfaz») genera la carpeta `modelo_entrenado/` con:

- `modelo.keras` — la red entrenada.
- `preprocesadores.pkl` — el `StandardScaler`, el `LabelEncoder` y los rangos del dataset.

Esos archivos están en `.gitignore`: no se suben al repositorio, cada quien los genera corriendo
el notebook. Después, desde la carpeta del proyecto y con el entorno activado:

```bat
python interfaz.py
```

La ventana trae valores de ejemplo en el menú *Ejemplo* y avisa cuando un dato queda fuera del
rango que la red vio al entrenar, porque ahí la predicción no es confiable aunque muestre una
probabilidad alta.

## Estructura

```
├── Crop_recommendation.csv   # Dataset
├── redNeuronal.ipynb         # Análisis, entrenamiento y predicción
├── interfaz.py               # Interfaz de escritorio (usa el modelo entrenado)
├── requirements.txt          # Dependencias con versiones fijadas
└── documentacion/
    ├── 1_Variables_del_Dataset.md
    ├── 2_Preprocesamiento_de_Datos.md
    ├── 3_Arquitectura_Red_Neuronal.md
    ├── 4_Uso_del_Modelo.md
    └── 5_Plan_de_Mejora.md
```

## Integrantes

- Marco Antonio Méndez Sánchez — 2177912
- Alfonso Uriel Rodriguez Ruiz — 2177756
- Daniel Humberto Flores Martínez — 2177905
- Jared Nathan Hernandez Garibaldi — 2177817
- Gamaliel Cruz Feliciano — 2173901
