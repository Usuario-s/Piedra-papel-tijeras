

import streamlit as st
import paho.mqtt.client as paho
import time
import json
import random
import cv2
import numpy as np

from PIL import Image, ImageOps
from keras.models import load_model


# =========================================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Piedra, Papel o Tijera",
    page_icon="✊",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #101010;
        color: white;
    }

    h1, h2, h3, p, label {
        color: white !important;
    }

    .titulo {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .subtitulo {
        text-align: center;
        color: #bdbdbd !important;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .resultado {
        text-align: center;
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
        background-color: #202020;
    }

    .victoria {
        color: #00e676 !important;
        font-size: 32px;
        font-weight: bold;
    }

    .derrota {
        color: #ff5252 !important;
        font-size: 32px;
        font-weight: bold;
    }

    .empate {
        color: #40c4ff !important;
        font-size: 32px;
        font-weight: bold;
    }

    .jugada {
        font-size: 20px;
        text-align: center;
        margin-top: 12px;
    }

    div.stButton > button {
        background-color: #292929;
        color: white;
        border: 1px solid #555;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #444;
        color: white;
        border: 1px solid white;
    }

    [data-testid="stCameraInput"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="titulo">PIEDRA, PAPEL O TIJERA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Realiza tu jugada frente a la cámara y reta a la máquina.</div>',
    unsafe_allow_html=True
)


# =========================================================
# CONSEJOS
# =========================================================

consejos = [
    "Observa los patrones de tus contrincantes.",
    "No repitas siempre la misma jugada.",
    "Intenta variar tus movimientos.",
    "Recuerda que la piedra vence a la tijera.",
    "El papel vence a la piedra.",
    "La tijera vence al papel.",
    "No existe una jugada que gane siempre.",
    "Evita actuar de manera demasiado predecible.",
    "Presta atención a las jugadas anteriores.",
    "Cambiar de estrategia puede ayudarte.",
    "No te apresures al elegir tu jugada.",
    "La aleatoriedad puede ser una buena estrategia.",
    "Intenta no dejarte llevar por la última ronda.",
    "A veces conviene romper tus propios patrones.",
    "Mantén la calma después de perder.",
    "Recuerda que cada ronda es independiente.",
    "No siempre el rival elegirá lo que esperas.",
    "Alternar entre piedra, papel y tijera dificulta anticiparte.",
    "Analiza tus decisiones después de cada partida.",
    "¡Sigue practicando para mejorar!"
]


def mostrar_consejo_aleatorio():
    consejo = random.choice(consejos)

    st.markdown(
        f"""
        <div class="resultado">
            <h3>💡 CONSEJO</h3>
            <p>{consejo}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CONFIGURACIÓN MQTT
# =========================================================

broker = "broker.mqttdashboard.com"
port = 1883

TOPIC_JUGADA = "tripletadeo"
TOPIC_RESULTADO = "IMIA"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Conexión MQTT establecida.")
    else:
        print(f"Error de conexión MQTT. Código: {rc}")


def on_publish(client, userdata, mid, *args):
    print(f"Mensaje MQTT publicado. ID: {mid}")


@st.cache_resource
def conectar_mqtt():
    # Cliente compatible con las versiones habituales de Paho MQTT.
    try:
        cliente = paho.Client(
            client_id="APP_GESTOS_PPT",
            protocol=paho.MQTTv311,
            callback_api_version=paho.CallbackAPIVersion.VERSION1
        )
    except (AttributeError, TypeError):
        cliente = paho.Client(
            client_id="APP_GESTOS_PPT",
            protocol=paho.MQTTv311
        )

    cliente.on_connect = on_connect
    cliente.on_publish = on_publish

    cliente.connect(broker, port, keepalive=60)
    cliente.loop_start()

    inicio = time.time()

    while not cliente.is_connected():
        if time.time() - inicio > 10:
            cliente.loop_stop()
            raise ConnectionError("No se pudo conectar con el broker MQTT.")

        time.sleep(0.1)

    return cliente


try:
    client1 = conectar_mqtt()
    st.success("Conexión MQTT establecida correctamente.")
except Exception as e:
    client1 = None
    st.error(f"No se pudo establecer la conexión MQTT: {e}")


# =========================================================
# ENVÍO DE MENSAJES A MQTT / WOKWI
# =========================================================

def publicar_mqtt(topic, mensaje):
    global client1

    if client1 is None:
        st.error("No hay conexión MQTT disponible.")
        return False

    try:
        if not client1.is_connected():
            client1.reconnect()

            inicio = time.time()

            while not client1.is_connected():
                if time.time() - inicio > 5:
                    st.error("No fue posible reconectar con MQTT.")
                    return False

                time.sleep(0.1)

        payload = json.dumps(mensaje)

        resultado = client1.publish(
            topic,
            payload,
            qos=1,
            retain=False
        )

        if resultado.rc != paho.MQTT_ERR_SUCCESS:
            st.error("No se pudo publicar el mensaje MQTT.")
            return False

        resultado.wait_for_publish(timeout=5)

        if resultado.is_published():
            print(f"Mensaje enviado | Tópico: {topic} | Datos: {payload}")
            return True

        st.warning("El mensaje fue enviado, pero no se confirmó su publicación.")
        return False

    except Exception as e:
        st.error(f"Error al enviar mensaje MQTT: {e}")
        return False


def enviar_resultado_wokwi(resultado):
    """
    Victoria  -> Abre
    Derrota   -> Cierra
    Empate    -> Empate
    """

    equivalencias_resultado = {
        "victoria": "Abre",
        "derrota": "Cierra",
        "empate": "Empate"
    }

    accion = equivalencias_resultado.get(resultado)

    if accion is None:
        st.error("Resultado no reconocido.")
        return

    mensaje = {
        "gesto": accion
    }

    publicar_mqtt(TOPIC_RESULTADO, mensaje)


# =========================================================
# CARGAR MODELO DE TEACHABLE MACHINE
# =========================================================

@st.cache_resource
def cargar_modelo():
    modelo = load_model(
        "converted_kerasPTP/keras_model.h5",
        compile=False
    )

    with open("converted_kerasPTP/labels.txt", "r") as archivo:
        clases_modelo = [
            linea.strip().split(maxsplit=1)[1]
            for linea in archivo.readlines()
            if linea.strip() and len(linea.strip().split(maxsplit=1)) > 1
        ]

    return modelo, clases_modelo


try:
    model, clases = cargar_modelo()
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")
    st.stop()


# =========================================================
# CÁMARA
# =========================================================

st.markdown("### 📸 Realiza tu jugada")

imagen_camara = st.camera_input("Muestra tu mano frente a la cámara")


# =========================================================
# LÓGICA DEL JUEGO
# =========================================================

if imagen_camara is not None:

    try:
        imagen = Image.open(imagen_camara).convert("RGB")

        # Redimensionar imagen al tamaño requerido por el modelo.
        imagen = ImageOps.fit(
            imagen,
            (224, 224),
            Image.Resampling.LANCZOS
        )

        imagen_array = np.asarray(imagen)

        # Normalización de los píxeles.
        imagen_array = (
            imagen_array.astype(np.float32) / 127.5
        ) - 1

        imagen_array = np.expand_dims(imagen_array, axis=0)

        # Predicción del modelo.
        prediccion = model.predict(imagen_array, verbose=0)

        indice = int(np.argmax(prediccion[0]))
        confianza = float(prediccion[0][indice])

        if indice >= len(clases):
            st.error("El modelo devolvió una clase no reconocida.")
            st.stop()

        gesto = clases[indice].strip()

        # Mostrar la confianza de la predicción.
        st.write(f"**Gesto detectado:** {gesto}")
        st.write(f"**Confianza:** {confianza * 100:.2f}%")

        # Enviar la jugada detectada al tópico original.
        publicar_mqtt(
            TOPIC_JUGADA,
            {"gesto": gesto}
        )

        # Elegir jugada aleatoria de la máquina.
        maquina = random.choice(clases).strip()

        # Normalizar nombres de las clases.
        equivalencias = {
            "tijeras": "tijera",
            "tijera": "tijera",
            "piedra": "piedra",
            "papel": "papel"
        }

        jugador_normalizado = equivalencias.get(gesto.lower())
        maquina_normalizada = equivalencias.get(maquina.lower())

        # Reglas del juego.
        reglas = {
            "piedra": "tijera",
            "tijera": "papel",
            "papel": "piedra"
        }

        if jugador_normalizado is None or maquina_normalizada is None:
            st.error(
                "No se reconoció correctamente una de las jugadas. "
                "Revisa los nombres de las clases en labels.txt."
            )
            st.stop()

        st.markdown("---")
        st.markdown("### 🎮 Resultado de la partida")

        st.markdown(
            f'<div class="jugada">🧑 Tu jugada: <b>{jugador_normalizado.upper()}</b></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="jugada">🤖 Jugada de la máquina: <b>{maquina_normalizada.upper()}</b></div>',
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # EMPATE
        # -------------------------------------------------

        if jugador_normalizado == maquina_normalizada:

            st.markdown(
                """
                <div class="resultado">
                    <div class="empate">🤝 ¡EMPATE!</div>
                    <p>Ambos eligieron la misma jugada.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Enviar comando de empate a Wokwi.
            enviar_resultado_wokwi("empate")

        # -------------------------------------------------
        # VICTORIA
        # -------------------------------------------------

        elif reglas.get(jugador_normalizado) == maquina_normalizada:

            st.markdown(
                """
                <div class="resultado">
                    <div class="victoria">🏆 ¡GANASTE!</div>
                    <p>¡Excelente jugada!</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Enviar comando de victoria a Wokwi.
            enviar_resultado_wokwi("victoria")

        # -------------------------------------------------
        # DERROTA
        # -------------------------------------------------

        else:

            st.markdown(
                """
                <div class="resultado">
                    <div class="derrota">💀 ¡PERDISTE!</div>
                    <p>La máquina ganó esta ronda.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Enviar comando de derrota a Wokwi.
            enviar_resultado_wokwi("derrota")

            mostrar_consejo_aleatorio()

    except Exception as e:
        st.error(f"Ocurrió un error al procesar la jugada: {e}")

