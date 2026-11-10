
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


# ==========================================
# CONSEJOS, ESTRATEGIAS Y DATOS CURIOSOS
# ==========================================

consejos = [
    ("🧠 Estrategia", "Empieza jugando papel: algunos jugadores suelen comenzar con piedra."),
    ("🧠 Estrategia", "No repitas siempre la misma jugada. Cambiar evita que el rival identifique tus patrones."),
    ("🧠 Estrategia", "Analiza tus derrotas e intenta identificar qué decisiones te llevaron a perder."),
    ("🧠 Estrategia", "Si detectas que tu rival repite una jugada, utiliza la opción que la vence."),
    ("🧠 Estrategia", "Observa las jugadas anteriores de tu rival para encontrar posibles tendencias."),
    ("🧠 Estrategia", "Evita seguir patrones predecibles: variar tus elecciones puede dificultar que te anticipen."),
    ("🧠 Estrategia", "Después de un empate, considera cambiar tu jugada para no ser predecible."),
    ("🎭 Truco psicológico", "Juega con seguridad. Mostrar dudas puede hacer que tu rival intente anticiparse."),
    ("🎭 Truco psicológico", "Estudia el comportamiento de tu rival: sus hábitos pueden revelar tendencias."),
    ("🎭 Truco psicológico", "Aprovecha los hábitos de tu contrincante para elegir una jugada que los contrarreste."),
    ("🎭 Truco psicológico", "No juegues por impulso. Tómate un momento para pensar en las rondas anteriores."),
    ("🤯 Dato curioso", "La piedra suele ser una elección popular entre los jugadores."),
    ("🤯 Dato curioso", "Los seres humanos no somos completamente aleatorios: tendemos a repetir patrones."),
    ("🤯 Dato curioso", "Una estrategia aleatoria equilibrada consiste en elegir cada opción aproximadamente el 33,3 % de las veces."),
    ("🤯 Dato curioso", "Después de perder, algunas personas cambian su comportamiento y sus siguientes elecciones."),
    ("🤯 Dato curioso", "No existe una opción invencible: cada gesto tiene una opción que puede vencerlo."),
    ("🎯 Tip rápido", "Memoriza las reglas: piedra vence a tijera, tijera vence a papel y papel vence a piedra."),
    ("🎯 Tip rápido", "Lleva un registro de las jugadas de tu rival para detectar repeticiones."),
    ("🎯 Tip rápido", "No confundas una victoria por suerte con una estrategia que siempre funciona."),
    ("🎯 Tip rápido", "Sé impredecible: evita que tu rival pueda adivinar tu siguiente movimiento.")
]


def mostrar_consejo_aleatorio():

    categoria, consejo = random.choice(consejos)

    st.markdown("### 💡 Consejo para tu próxima ronda")
    st.markdown(f"**{categoria}**")
    st.info(consejo)


# ==========================================
# DISEÑO VISUAL NEGRO Y GRIS
# ==========================================

st.markdown("""
<style>

/* FONDO GENERAL */
.stApp {
    background: linear-gradient(135deg, #080808 0%, #151515 55%, #080808 100%);
    color: white;
}

/* CONTENEDOR PRINCIPAL */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* TEXTOS */
h1, h2, h3, p, label, span {
    color: #FFFFFF;
}

/* TITULOS */
h1 {
    text-align: center;
    font-weight: 800;
    letter-spacing: 2px;
    text-shadow: 0 0 12px rgba(255,255,255,0.18);
}

h2, h3 {
    font-weight: 700;
    letter-spacing: 1px;
}

/* TITULO PRINCIPAL */
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 4px;
    color: #FFFFFF;
    text-shadow: 0 0 15px rgba(255,255,255,0.25);
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    color: #999999;
    font-size: 14px;
    letter-spacing: 3px;
    margin-bottom: 35px;
}

/* SEPARADORES */
hr {
    border-color: #333333 !important;
}

/* CONTENEDOR DE LA CAMARA */
div[data-testid="stCameraInput"] {
    background: #171717;
    border: 1px solid #444444;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0 0 18px rgba(255,255,255,0.04);
}

/* BOTONES */
.stButton > button {
    background: linear-gradient(135deg, #333333, #151515);
    color: white;
    border: 1px solid #666666;
    border-radius: 10px;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    border-color: white;
    box-shadow: 0 0 12px rgba(255,255,255,0.25);
    color: white;
}

/* RESULTADOS */
.resultado {
    padding: 22px;
    border-radius: 15px;
    text-align: center;
    font-size: 21px;
    font-weight: 800;
    letter-spacing: 1px;
    margin: 20px 0;
    background: #151515;
    animation: aparecer 0.6s ease;
}

/* VICTORIA */
.resultado-win {
    color: #65FF91;
    border: 1px solid #00FF66;
    box-shadow:
        0 0 8px rgba(0,255,102,0.5),
        0 0 22px rgba(0,255,102,0.25),
        inset 0 0 12px rgba(0,255,102,0.08);
    text-shadow: 0 0 12px rgba(0,255,102,0.8);
}

/* DERROTA */
.resultado-lose {
    color: #FF6666;
    border: 1px solid #FF3030;
    box-shadow:
        0 0 8px rgba(255,48,48,0.5),
        0 0 22px rgba(255,48,48,0.25),
        inset 0 0 12px rgba(255,48,48,0.08);
    text-shadow: 0 0 12px rgba(255,48,48,0.8);
}

/* EMPATE */
.resultado-draw {
    color: #66BFFF;
    border: 1px solid #168BFF;
    box-shadow:
        0 0 8px rgba(22,139,255,0.5),
        0 0 22px rgba(22,139,255,0.25),
        inset 0 0 12px rgba(22,139,255,0.08);
    text-shadow: 0 0 12px rgba(22,139,255,0.8);
}

/* ERROR */
.resultado-error {
    color: #FF7777;
    border: 1px solid #FF3030;
    box-shadow: 0 0 15px rgba(255,48,48,0.2);
}

/* ANIMACION */
@keyframes aparecer {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ALERTAS */
div[data-testid="stAlert"] {
    background: #1B1B1B;
    border-radius: 12px;
    border: 1px solid #555555;
    color: white;
}

/* TEXTO DE CONFIANZA */
.confianza {
    text-align: center;
    color: #AAAAAA;
    font-size: 15px;
    background: #191919;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #333333;
}

/* ETIQUETAS DE LOS GESTOS */
.gesto-detectado {
    background: linear-gradient(135deg, #242424, #111111);
    border: 1px solid #555555;
    border-radius: 14px;
    padding: 15px;
    text-align: center;
    font-size: 25px;
    font-weight: 800;
    color: white;
    box-shadow: 0 0 15px rgba(255,255,255,0.05);
    margin: 15px 0;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# TITULO
# ==========================================

st.markdown(
    '<div class="main-title">PIEDRA · PAPEL · TIJERAS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">DESAFÍA A LA COMPUTADORA</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# FUNCIONES MQTT
# ==========================================

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")


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

client1 = paho.Client(client_id="APP_CERR")
client1.on_message = on_message
client1.on_publish = on_publish

client1.connect(broker, port, keepalive=60)

# Iniciar comunicación MQTT
client1.loop_start()


# ==========================================
# ENVIAR RESULTADO AL ESP32
# ==========================================

def enviar_resultado(resultado):

    mensaje = {
        "resultado": resultado
    }

    try:

        info = client1.publish(
            "IMIA",
            json.dumps(mensaje),
            qos=1,
            retain=False
        )

        info.wait_for_publish(timeout=5)

        if info.is_published():

            print(f"Resultado enviado al ESP32: {resultado}")

        else:

            print(f"No se pudo confirmar el envío: {resultado}")

    except Exception as e:

        print(f"Error al enviar resultado MQTT: {e}")


# ==========================================
# CARGAR MODELO DE PIEDRA, PAPEL Y TIJERA
# ==========================================

model = load_model('converted_kerasPTPF/keras_model.h5')


# Cargar las etiquetas del modelo
with open('converted_kerasPTPF/labels.txt', 'r') as f:

    clases = [
        linea.strip().split(maxsplit=1)[1]
        for linea in f.readlines()
        if linea.strip()
    ]


data = np.ndarray(
    shape=(1, 224, 224, 3),
    dtype=np.float32
)


st.markdown("### 📷 Reconocimiento del jugador")

img_file_buffer = st.camera_input("Toma una foto para jugar")


if img_file_buffer is not None:

    data = np.ndarray(
        shape=(1, 224, 224, 3),
        dtype=np.float32
    )

    img = Image.open(img_file_buffer).convert("RGB")

    newsize = (224, 224)
    img = img.resize(newsize)

    img_array = np.array(img)

    normalized_image_array = (
        img_array.astype(np.float32) / 127.5
    ) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data, verbose=0)

    print(prediction)


    # ==========================================
    # IDENTIFICAR EL GESTO
    # ==========================================

    if len(clases) != 3:

        st.error("El modelo no contiene exactamente tres clases.")

    else:

        indice = np.argmax(prediction[0])

        confianza = prediction[0][indice]

        gesto = clases[indice]


        if confianza > 0.3:

            st.markdown("### ✋ Tu jugada")

            st.markdown(
                f'<div class="gesto-detectado">{gesto.upper()}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="confianza">Confianza del reconocimiento: {confianza * 100:.2f}%</div>',
                unsafe_allow_html=True
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

            st.markdown("### 🤖 Jugada de la computadora")

            st.markdown(
                f'<div class="gesto-detectado">{maquina.upper()}</div>',
                unsafe_allow_html=True
            )


            # ==========================================
            # NORMALIZAR LOS NOMBRES DE LOS GESTOS
            # ==========================================

            jugador_normalizado = gesto.strip().lower()
            maquina_normalizada = maquina.strip().lower()

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

            reglas = {
                "piedra": "tijera",
                "tijera": "papel",
                "papel": "piedra"
            }


            # ==========================================
            # DETERMINAR GANADOR
            # ==========================================

            st.divider()

            st.markdown("### 🏆 Resultado de la ronda")


            if jugador_normalizado not in reglas or maquina_normalizada not in reglas:

                st.markdown(
                    '<div class="resultado resultado-error">No se reconocieron correctamente los nombres de los gestos. Revisa el archivo labels.txt.</div>',
                    unsafe_allow_html=True
                )


            elif jugador_normalizado == maquina_normalizada:

                st.markdown(
                    '<div class="resultado resultado-draw">🤝 ¡EMPATE! Ambos eligieron el mismo gesto.</div>',
                    unsafe_allow_html=True
                )

                # ENVIAR EMPATE AL ESP32
                enviar_resultado("Empate")


            elif reglas[jugador_normalizado] == maquina_normalizada:

                st.markdown(
                    f'<div class="resultado resultado-win">🏆 ¡GANASTE! Tu {gesto} vence a {maquina}.</div>',
                    unsafe_allow_html=True
                )

                # ENVIAR VICTORIA AL ESP32
                enviar_resultado("Gana")


            else:

                st.markdown(
                    f'<div class="resultado resultado-lose">😢 ¡PERDISTE! La {maquina} de la computadora vence a tu {gesto}.</div>',
                    unsafe_allow_html=True
                )

                # ENVIAR DERROTA AL ESP32
                enviar_resultado("Pierde")

                mostrar_consejo_aleatorio()


        else:

            st.warning(
                "No se pudo reconocer el gesto. Intenta nuevamente."
            )

