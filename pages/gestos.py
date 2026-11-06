
import paho.mqtt.client as paho
import time
import json
import random
import streamlit as st
import cv2
import numpy as np

#from PIL import Image
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

st.title("Gestos")


# ==========================================
# FUNCIONES MQTT
# ==========================================

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass


def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)


# ==========================================
# CONFIGURACIÓN MQTT
# ==========================================

broker = "broker.mqttdashboard.com"
port = 1883

client1 = paho.Client("APP_CERR")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

# Iniciar comunicación MQTT
client1.loop_start()


# ==========================================
# CARGAR MODELO DE PIEDRA, PAPEL Y TIJERA
# ==========================================

model = load_model('converted_kerasPTP/keras_model.h5')


# Cargar las etiquetas del modelo
with open('converted_kerasPTP/labels.txt', 'r') as f:
    clases = [
        linea.strip().split(maxsplit=1)[1]
        for linea in f.readlines()
        if linea.strip()
    ]


data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

st.title("Cerradura Inteligente")

img_file_buffer = st.camera_input("Toma una Foto")


if img_file_buffer is not None:

    # To read image file buffer with OpenCV:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer).convert("RGB")

    newsize = (224, 224)
    img = img.resize(newsize)

    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Normalize the image
    normalized_image_array = (img_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Run the inference
    prediction = model.predict(data, verbose=0)
    print(prediction)


    # ==========================================
    # IDENTIFICAR EL GESTO
    # ==========================================

    if len(clases) != 3:

        st.error("El modelo no contiene exactamente tres clases.")

    else:

        # Obtener la clase con mayor probabilidad
        indice = np.argmax(prediction[0])

        # Obtener el nivel de confianza
        confianza = prediction[0][indice]

        # Identificar el gesto
        gesto = clases[indice]


        if confianza > 0.3:

            st.header(gesto)

            st.write(
                "Confianza: {:.2f}%".format(confianza * 100)
            )


            # ==========================================
            # ENVIAR GESTO DEL JUGADOR POR MQTT
            # ==========================================

            mensaje = {
                "gesto": gesto
            }

            client1.publish(
                "tripletadeo",
                json.dumps(mensaje),
                qos=0,
                retain=False
            )

            time.sleep(0.2)


            # ==========================================
            # ELECCIÓN ALEATORIA DE LA COMPUTADORA
            # ==========================================

            maquina = random.choice(clases)

            st.subheader("🤖 Elección de la computadora")

            st.write("La computadora eligió:")

            st.header(maquina)


            # ==========================================
            # NORMALIZAR LOS NOMBRES DE LOS GESTOS
            # ==========================================

            jugador_normalizado = gesto.strip().lower()
            maquina_normalizada = maquina.strip().lower()

            # Unificar Tijera y Tijeras
            equivalencias = {
                "tijeras": "tijera",
                "tijera": "tijera",
                "piedra": "piedra",
                "papel": "papel"
            }

            jugador_normalizado = equivalencias.get(
                jugador_normalizado, jugador_normalizado
            )

            maquina_normalizada = equivalencias.get(
                maquina_normalizada, maquina_normalizada
            )


            # ==========================================
            # REGLAS DEL JUEGO
            # ==========================================

            # Piedra vence a Tijera
            # Tijera vence a Papel
            # Papel vence a Piedra

            reglas = {
                "piedra": "tijera",
                "tijera": "papel",
                "papel": "piedra"
            }


            # ==========================================
            # DETERMINAR GANADOR
            # ==========================================

            st.subheader("🏆 Resultado de la ronda")

            if jugador_normalizado not in reglas or maquina_normalizada not in reglas:

                st.error(
                    "No se reconocieron correctamente los nombres de los gestos. "
                    "Revisa el archivo labels.txt."
                )

            elif jugador_normalizado == maquina_normalizada:

                st.info(
                    "🤝 ¡EMPATE! Ambos eligieron " + gesto
                )

            elif reglas[jugador_normalizado] == maquina_normalizada:

                st.success(
                    "🎉 ¡GANASTE! Tu " + gesto + " vence a " + maquina
                )

            else:

                st.error(
                    "😢 ¡PERDISTE! La " + maquina +
                    " de la computadora vence a tu " + gesto
                )


        else:

            st.warning(
                "No se pudo reconocer el gesto. Intenta nuevamente."
            )


