"""Interfaz de escritorio para el recomendador de cultivos."""

import os
import pickle
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

CARPETA_MODELO = Path(__file__).resolve().parent / "modelo_entrenado"

CAMPOS = [
    ("n", "Nitrogeno (N)", "kg/ha"),
    ("p", "Fosforo (P)", "kg/ha"),
    ("k", "Potasio (K)", "kg/ha"),
    ("temperature", "Temperatura", "C"),
    ("humidity", "Humedad", "%"),
    ("ph", "pH del suelo", ""),
    ("rainfall", "Precipitacion", "mm"),
]

NOMBRES = {
    "apple": "Manzana", "banana": "Platano", "blackgram": "Frijol negro urd",
    "chickpea": "Garbanzo", "coconut": "Coco", "coffee": "Cafe",
    "cotton": "Algodon", "grapes": "Uva", "jute": "Yute",
    "kidneybeans": "Frijol rojo", "lentil": "Lenteja", "maize": "Maiz",
    "mango": "Mango", "mothbeans": "Frijol moth", "mungbean": "Frijol mungo",
    "muskmelon": "Melon", "orange": "Naranja", "papaya": "Papaya",
    "pigeonpeas": "Guandu", "pomegranate": "Granada", "rice": "Arroz",
    "watermelon": "Sandia",
}

EJEMPLOS = {
    "Maiz": {"n": 76, "p": 48, "k": 20, "temperature": 22.8,
             "humidity": 65.3, "ph": 6.3, "rainfall": 83.5},
    "Arroz": {"n": 80, "p": 47, "k": 40, "temperature": 23.7,
              "humidity": 82.2, "ph": 6.4, "rainfall": 233.1},
    "Yute": {"n": 78, "p": 46, "k": 40, "temperature": 25.0,
             "humidity": 79.5, "ph": 6.7, "rainfall": 175.6},
    "Cafe": {"n": 103, "p": 29, "k": 30, "temperature": 25.7,
             "humidity": 57.6, "ph": 6.8, "rainfall": 157.8},
    "Manzana": {"n": 24, "p": 136, "k": 200, "temperature": 22.6,
                "humidity": 92.4, "ph": 5.9, "rainfall": 113.0},
    "Garbanzo": {"n": 39, "p": 68, "k": 79, "temperature": 18.9,
                 "humidity": 16.7, "ph": 7.4, "rainfall": 79.7},
    "Platano": {"n": 100, "p": 81, "k": 50, "temperature": 27.4,
                "humidity": 80.2, "ph": 6.0, "rainfall": 105.0},
    "Algodon": {"n": 117, "p": 46, "k": 19, "temperature": 24.0,
                "humidity": 80.0, "ph": 6.8, "rainfall": 80.2},
}


class Recomendador:

    def __init__(self, carpeta):
        if not carpeta.is_dir():
            raise FileNotFoundError(
                f"No existe la carpeta '{carpeta.name}'.\n\n"
                "Primero abre redNeuronal.ipynb y corre todas las celdas: la ultima "
                "guarda el modelo entrenado que necesita esta interfaz."
            )

        archivo_modelo = carpeta / "modelo.keras"
        archivo_prep = carpeta / "preprocesadores.pkl"
        faltantes = [a.name for a in (archivo_modelo, archivo_prep) if not a.is_file()]
        if faltantes:
            raise FileNotFoundError(
                f"Falta(n) {', '.join(faltantes)} en '{carpeta.name}'.\n\n"
                "Corre todas las celdas de redNeuronal.ipynb para generarlos."
            )

        import pandas as pd
        from tensorflow import keras

        self.pd = pd
        self.modelo = keras.models.load_model(archivo_modelo)

        with open(archivo_prep, "rb") as f:
            prep = pickle.load(f)
        self.scaler = prep["scaler"]
        self.label_encoder = prep["label_encoder"]
        self.columnas = prep["columnas"]
        self.rangos = prep["rangos"]
        self.precision = prep.get("precision_prueba")

    def rango(self, columna):
        r = self.rangos[columna]
        return float(r["min"]), float(r["max"])

    def recomendar(self, valores, top=3):
        datos = self.pd.DataFrame([[valores[c] for c in self.columnas]],
                                  columns=self.columnas)

        avisos = []
        for columna in self.columnas:
            minimo, maximo = self.rango(columna)
            valor = datos[columna].iloc[0]
            if not (minimo <= valor <= maximo):
                etiqueta = next(e for c, e, _ in CAMPOS if c == columna)
                avisos.append(
                    f"{etiqueta} = {valor:g} esta fuera del rango visto en el "
                    f"entrenamiento [{minimo:.1f} - {maximo:.1f}]"
                )

        escalados = self.scaler.transform(datos)
        probabilidades = self.modelo.predict(escalados, verbose=0)[0]

        orden = probabilidades.argsort()[::-1][:top]
        resultados = [(self.label_encoder.classes_[i], float(probabilidades[i]))
                      for i in orden]
        return resultados, avisos


class Ventana(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Recomendador de Cultivos - Red Neuronal (PIA)")
        self.minsize(640, 620)
        self.resizable(False, True)
        self.recomendador = None
        self.entradas = {}

        estilo = ttk.Style(self)
        if "vista" in estilo.theme_names():
            estilo.theme_use("vista")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 15, "bold"))
        estilo.configure("Sub.TLabel", font=("Segoe UI", 9), foreground="#555555")
        estilo.configure("Cultivo.TLabel", font=("Segoe UI", 11, "bold"))
        estilo.configure("Aviso.TLabel", font=("Segoe UI", 9), foreground="#B35C00")

        self._construir()
        threading.Thread(target=self._cargar_modelo, daemon=True).start()

    def _construir(self):
        marco = ttk.Frame(self, padding=18)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Recomendador de cultivos",
                  style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(marco, style="Sub.TLabel", text="Escribe las condiciones del "
                  "terreno y la red neuronal sugiere los 3 cultivos mas probables."
                  ).pack(anchor="w", pady=(2, 14))

        campos = ttk.LabelFrame(marco, text=" Datos del terreno ", padding=12)
        campos.pack(fill="x")
        campos.columnconfigure(1, weight=1)

        for fila, (clave, etiqueta, unidad) in enumerate(CAMPOS):
            texto = f"{etiqueta} ({unidad})" if unidad else etiqueta
            ttk.Label(campos, text=texto).grid(row=fila, column=0, sticky="w",
                                               pady=4, padx=(0, 10))
            entrada = ttk.Entry(campos, width=12, justify="right")
            entrada.grid(row=fila, column=1, sticky="w", pady=4)
            entrada.bind("<Return>", lambda _e: self._recomendar())
            self.entradas[clave] = entrada

            pista = ttk.Label(campos, text="", style="Sub.TLabel")
            pista.grid(row=fila, column=2, sticky="w", padx=(12, 0))
            setattr(self, f"_pista_{clave}", pista)

        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=(14, 4))

        self.boton = ttk.Button(botones, text="Recomendar cultivo",
                                command=self._recomendar, state="disabled")
        self.boton.pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self._limpiar).pack(
            side="left", padx=6)

        ttk.Label(botones, text="Ejemplo:", style="Sub.TLabel").pack(
            side="left", padx=(12, 4))
        self.combo = ttk.Combobox(botones, values=list(EJEMPLOS), width=10,
                                  state="readonly")
        self.combo.pack(side="left")
        self.combo.bind("<<ComboboxSelected>>", self._cargar_ejemplo)

        self.resultados = ttk.LabelFrame(marco, text=" Resultado ", padding=12)
        self.resultados.pack(fill="both", expand=True, pady=(12, 0))
        self.vacio = ttk.Label(self.resultados, style="Sub.TLabel",
                               text="Aun no hay una recomendacion.")
        self.vacio.pack(anchor="w")

        self.estado = ttk.Label(marco, style="Sub.TLabel",
                                text="Cargando el modelo entrenado...")
        self.estado.pack(anchor="w", pady=(12, 0))

    def _cargar_modelo(self):
        try:
            recomendador = Recomendador(CARPETA_MODELO)
        except Exception as error:
            self.after(0, self._fallo_carga, error)
            return
        self.after(0, self._modelo_listo, recomendador)

    def _modelo_listo(self, recomendador):
        self.recomendador = recomendador
        self.boton.config(state="normal")

        for clave, _etiqueta, _unidad in CAMPOS:
            minimo, maximo = recomendador.rango(clave)
            getattr(self, f"_pista_{clave}").config(
                text=f"dataset: {minimo:.1f} - {maximo:.1f}")

        cultivos = len(recomendador.label_encoder.classes_)
        mensaje = f"Modelo cargado - {cultivos} cultivos posibles"
        if recomendador.precision is not None:
            mensaje += f" - precision en prueba: {recomendador.precision:.2%}"
        self.estado.config(text=mensaje)

    def _fallo_carga(self, error):
        self.estado.config(text="No se pudo cargar el modelo.")
        messagebox.showerror("Falta el modelo entrenado", str(error))

    def _cargar_ejemplo(self, _evento=None):
        valores = EJEMPLOS.get(self.combo.get())
        if not valores:
            return
        for clave, valor in valores.items():
            self.entradas[clave].delete(0, "end")
            self.entradas[clave].insert(0, str(valor))
        self.combo.selection_clear()

    def _limpiar(self):
        for entrada in self.entradas.values():
            entrada.delete(0, "end")
        self.combo.set("")
        self._mostrar_vacio("Aun no hay una recomendacion.")

    def _leer_valores(self):
        valores = {}
        for clave, etiqueta, _unidad in CAMPOS:
            texto = self.entradas[clave].get().strip().replace(",", ".")
            if not texto:
                messagebox.showwarning("Falta un dato",
                                       f"Escribe un valor para {etiqueta}.")
                self.entradas[clave].focus_set()
                return None
            try:
                valores[clave] = float(texto)
            except ValueError:
                messagebox.showwarning(
                    "Dato invalido",
                    f"'{texto}' no es un numero valido para {etiqueta}.")
                self.entradas[clave].focus_set()
                return None
        return valores

    def _recomendar(self):
        if self.recomendador is None:
            return
        valores = self._leer_valores()
        if valores is None:
            return
        try:
            resultados, avisos = self.recomendador.recomendar(valores)
        except Exception as error:
            messagebox.showerror("Error al predecir", str(error))
            return
        self._mostrar(resultados, avisos)

    def _limpiar_resultados(self):
        for hijo in self.resultados.winfo_children():
            hijo.destroy()

    def _mostrar_vacio(self, texto):
        self._limpiar_resultados()
        ttk.Label(self.resultados, text=texto, style="Sub.TLabel").pack(anchor="w")

    def _mostrar(self, resultados, avisos):
        self._limpiar_resultados()

        cultivo, probabilidad = resultados[0]
        ttk.Label(self.resultados, style="Cultivo.TLabel",
                  text=f"Recomendacion: {NOMBRES.get(cultivo, cultivo)}  "
                       f"({probabilidad:.1%})").pack(anchor="w", pady=(0, 10))

        tabla = ttk.Frame(self.resultados)
        tabla.pack(fill="x")
        tabla.columnconfigure(2, weight=1)

        for fila, (cultivo, probabilidad) in enumerate(resultados):
            nombre = NOMBRES.get(cultivo, cultivo)
            ttk.Label(tabla, text=f"{fila + 1}.").grid(row=fila, column=0,
                                                       sticky="w", pady=3)
            ttk.Label(tabla, text=f"{nombre}  ({cultivo})").grid(
                row=fila, column=1, sticky="w", padx=(4, 12), pady=3)
            barra = ttk.Progressbar(tabla, length=180, maximum=100,
                                    value=probabilidad * 100)
            barra.grid(row=fila, column=2, sticky="w", pady=3)
            ttk.Label(tabla, text=f"{probabilidad:.2%}", width=9,
                      anchor="e").grid(row=fila, column=3, sticky="e",
                                       padx=(10, 0), pady=3)

        if avisos:
            marco = ttk.Frame(self.resultados)
            marco.pack(fill="x", pady=(12, 0))
            ttk.Label(marco, style="Aviso.TLabel",
                      text="Cuidado: la red esta extrapolando").pack(anchor="w")
            for aviso in avisos:
                ttk.Label(marco, text=f"  - {aviso}", style="Aviso.TLabel",
                          wraplength=560, justify="left").pack(anchor="w")
            ttk.Label(marco, style="Sub.TLabel", wraplength=560, justify="left",
                      text="Con datos fuera del rango del dataset la probabilidad "
                           "puede verse alta y aun asi estar equivocada.").pack(
                anchor="w", pady=(4, 0))


if __name__ == "__main__":
    Ventana().mainloop()
