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

## Estructura

```
├── Crop_recommendation.csv   # Dataset
├── redNeuronal.ipynb         # Análisis, entrenamiento y predicción
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
