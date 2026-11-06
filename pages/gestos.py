
import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
#from PIL import Image
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

st.title("Gestos")

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)


broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("APP_CERR")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker,port)

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

   #To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer).convert("RGB")

    newsize = (224, 224)
    img = img.resize(newsize)

    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Normalize the image
    normalized_image_array = (img_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
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
            # ENVIAR GESTO A WOKWI MEDIANTE MQTT
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

        else:

            st.warning("No se pudo reconocer el gesto. Intenta nuevamente.")

