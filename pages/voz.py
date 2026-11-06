

import os
import streamlit as st
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
import random
import re
from gtts import gTTS
from googletrans import Translator


# ==========================================
# DISEÑO VISUAL
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #080808 0%, #151515 55%, #080808 100%);
    color: white;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label, span {
    color: #FFFFFF;
}

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 4px;
    color: #FFFFFF;
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    color: #999999;
    font-size: 14px;
    letter-spacing: 3px;
    margin-bottom: 35px;
}

hr {
    border-color: #333333 !important;
}

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

.resultado {
    padding: 22px;
    border-radius: 15px;
    text-align: center;
    font-size: 21px;
    font-weight: 800;
    letter-spacing: 1px;
    margin: 20px 0;
    background: #151515;
}

.resultado-win {
    color: #65FF91;
    border: 1px solid #00FF66;
    box-shadow: 0 0 15px rgba(0,255,102,0.25);
}

.resultado-lose {
    color: #FF6666;
    border: 1px solid #FF3030;
    box-shadow: 0 0 15px rgba(255,48,48,0.25);
}

.resultado-draw {
    color: #66BFFF;
    border: 1px solid #168BFF;
    box-shadow: 0 0 15px rgba(22,139,255,0.25);
}

.resultado-error {
    color: #FF7777;
    border: 1px solid #FF3030;
}

.gesto-detectado {
    background: linear-gradient(135deg, #242424, #111111);
    border: 1px solid #555555;
    border-radius: 14px;
    padding: 15px;
    text-align: center;
    font-size: 25px;
    font-weight: 800;
    color: white;
    margin: 15px 0;
}

.confianza {
    text-align: center;
    color: #AAAAAA;
    font-size: 15px;
    background: #191919;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #333333;
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
    print("el dato ha sido publicado")
    pass


def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)


# ==========================================
# CONFIGURACION MQTT
# ==========================================

broker = "broker.mqttdashboard.com"
port = 1883

client1 = paho.Client("GIT-HUBC")
client1.on_message = on_message
client1.on_publish = on_publish


# ==========================================
# FUNCION PARA IDENTIFICAR LA JUGADA
# ==========================================

def detectar_jugada(transcripcion):

    texto = transcripcion.lower().strip()

    # Buscar las palabras dentro de la transcripcion
    patrones = {
        "piedra": r"\bpiedra\b",
        "papel": r"\bpapel\b",
        "tijera": r"\btijera(s)?\b"
    }

    for jugada, patron in patrones.items():

        if re.search(patron, texto):
            return jugada

    return None


# ==========================================
# FUNCION PARA DETERMINAR GANADOR
# ==========================================

def determinar_ganador(jugador, maquina):

    reglas = {
        "piedra": "tijera",
        "tijera": "papel",
        "papel": "piedra"
    }

    if jugador == maquina:
        return "empate"

    elif reglas[jugador] == maquina:
        return "jugador"

    else:
        return "maquina"


# ==========================================
# RECONOCIMIENTO DE VOZ
# ==========================================

st.markdown("### 🎤 Reconocimiento del jugador")

st.write("Presiona el botón y di piedra, papel o tijera.")

stt_button = Button(label=" Inicio ", width=200)

stt_button.js_on_event(
    "button_click",
    CustomJS(code="""
        var recognition = new webkitSpeechRecognition();

        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "es-CO";

        recognition.onresult = function (e) {

            var value = "";

            for (var i = e.resultIndex; i < e.results.length; ++i) {

                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }

            if (value != "") {

                document.dispatchEvent(
                    new CustomEvent("GET_TEXT", {detail: value})
                );

                recognition.stop();
            }
        }

        recognition.start();
    """)
)


result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)


# ==========================================
# PROCESAR TRANSCRIPCION
# ==========================================

if result and "GET_TEXT" in result:

    transcripcion = result.get("GET_TEXT")

    st.markdown("### 🗣️ Transcripción")

    st.markdown(
        f'<div class="confianza">{transcripcion.upper()}</div>',
        unsafe_allow_html=True
    )

    # Detectar jugada del jugador
    jugador = detectar_jugada(transcripcion)


    # ==========================================
    # VALIDAR JUGADA
    # ==========================================

    if jugador is None:

        st.markdown(
            '<div class="resultado resultado-error">'
            'No se reconoció ninguna jugada. '
            'Di piedra, papel o tijera.'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        # ==========================================
        # CONECTAR MQTT
        # ==========================================

        try:

            client1.connect(broker, port)

            mensaje = {
                "gesto": jugador
            }

            client1.publish(
                "voice_ctrl",
                json.dumps(mensaje),
                qos=0,
                retain=False
            )

            client1.disconnect()

        except Exception as e:

            st.warning("No se pudo conectar con MQTT: " + str(e))


        # ==========================================
        # ELECCION DEL JUGADOR
        # ==========================================

        st.divider()

        st.markdown("### ✋ Tu jugada")

        emojis = {
            "piedra": "✊",
            "papel": "✋",
            "tijera": "✌️"
        }

        st.markdown(
            f'<div class="gesto-detectado">'
            f'{emojis[jugador]} {jugador.upper()}'
            f'</div>',
            unsafe_allow_html=True
        )


        # ==========================================
        # ELECCION ALEATORIA DE LA MAQUINA
        # ==========================================

        maquina = random.choice([
            "piedra",
            "papel",
            "tijera"
        ])

        st.markdown("### 🤖 Jugada de la computadora")

        st.markdown(
            f'<div class="gesto-detectado">'
            f'{emojis[maquina]} {maquina.upper()}'
            f'</div>',
            unsafe_allow_html=True
        )


        # ==========================================
        # DETERMINAR GANADOR
        # ==========================================

        ganador = determinar_ganador(jugador, maquina)

        st.divider()

        st.markdown("### 🏆 Resultado de la ronda")


        if ganador == "empate":

            st.markdown(
                '<div class="resultado resultado-draw">'
                '🤝 ¡EMPATE! Ambos eligieron la misma jugada.'
                '</div>',
                unsafe_allow_html=True
            )

        elif ganador == "jugador":

            st.markdown(
                f'<div class="resultado resultado-win">'
                f'🏆 ¡GANASTE! {jugador.upper()} vence a {maquina.upper()}.'
                f'</div>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f'<div class="resultado resultado-lose">'
                f'😢 ¡PERDISTE! {maquina.upper()} vence a {jugador.upper()}.'
                f'</div>',
                unsafe_allow_html=True
            )
