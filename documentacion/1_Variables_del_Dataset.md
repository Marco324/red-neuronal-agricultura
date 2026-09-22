# Variables del Dataset Agrícola (`Crop_recommendation.csv`)

Este documento describe las variables edafoclimáticas (del suelo y clima) que conforman el conjunto de datos utilizado para entrenar la red neuronal. El dataset original consta de 2,200 registros (100 muestras exactas para cada uno de los 22 tipos de cultivo), lo que garantiza un conjunto de datos perfectamente balanceado.

## Características de Entrada (Features - X)

Estas son las variables ambientales y químicas medidas antes de la siembra. Son los parámetros que el modelo utiliza para aprender y realizar su predicción.

1. **`n` (Nitrógeno):** 
   - **Descripción:** Proporción de Nitrógeno en el suelo.
   - **Importancia:** Esencial para el crecimiento de las hojas y el desarrollo general de la planta.
   - **Unidad/Formato:** Numérico entero (ratio).

2. **`p` (Fósforo):** 
   - **Descripción:** Proporción de Fósforo en el suelo.
   - **Importancia:** Crucial para el desarrollo de raíces, flores y frutos. En nuestro análisis exploratorio, descubrimos que tiene una correlación fuerte positiva (0.74) con el potasio en este dataset.
   - **Unidad/Formato:** Numérico entero (ratio).

3. **`k` (Potasio):** 
   - **Descripción:** Proporción de Potasio en el suelo.
   - **Importancia:** Ayuda a la resistencia a enfermedades y a la absorción de agua.
   - **Unidad/Formato:** Numérico entero (ratio).

4. **`temperature` (Temperatura):** 
   - **Descripción:** Temperatura promedio durante el ciclo de crecimiento del cultivo.
   - **Unidad:** Grados Celsius (°C). Decimal continuo.

5. **`humidity` (Humedad):** 
   - **Descripción:** Humedad relativa promedio del ambiente.
   - **Unidad:** Porcentaje (%). Decimal continuo.

6. **`ph` (Potencial de Hidrógeno):** 
   - **Descripción:** Nivel de acidez o alcalinidad del suelo.
   - **Importancia:** Valores menores a 7 indican acidez, y mayores a 7 indican alcalinidad. Diferentes cultivos tienen diferentes niveles de tolerancia al pH.
   - **Unidad:** Escala de pH (0 a 14). Decimal continuo.

7. **`rainfall` (Precipitación / Lluvia):** 
   - **Descripción:** Cantidad total de lluvia recibida durante el ciclo de vida del cultivo.
   - **Unidad:** Milímetros (mm). Decimal continuo.

---

## Variable Objetivo (Target - y)

1. **`label` (Tipo de Cultivo):** 
   - **Descripción:** El cultivo óptimo que fue sembrado y prosperó bajo las condiciones dadas en las variables de entrada.
   - **Valores posibles (22 clases):** 
     - rice (Arroz)
     - maize (Maíz)
     - chickpea (Garbanzo)
     - kidneybeans (Frijoles)
     - pigeonpeas (Gandules)
     - mothbeans (Frijol tepari/moth)
     - mungbean (Frijol mungo)
     - blackgram (Lenteja negra)
     - lentil (Lenteja)
     - pomegranate (Granada)
     - banana (Plátano)
     - mango (Mango)
     - grapes (Uvas)
     - watermelon (Sandía)
     - muskmelon (Melón)
     - apple (Manzana)
     - orange (Naranja)
     - papaya (Papaya)
     - coconut (Coco)
     - cotton (Algodón)
     - jute (Yute)
     - coffee (Café)
