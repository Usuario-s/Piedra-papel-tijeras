

import os
import streamlit as st
import random
import re
import json
import time
import paho.mqtt.client as paho

from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events


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
    animation: aparecer 0.6s ease;
}

.resultado-win {
    color: #65FF91;
    border: 1px solid #00FF66;
    box-shadow:
        0 0 8px rgba(0,255,102,0.5),
        0 0 22px rgba(0,255,102,0.25),
        inset 0 0 12px rgba(0,255,102,0.08);
    text-shadow: 0 0 12px rgba(0,255,102,0.8);
}

.resultado-lose {
    color: #FF6666;
    border: 1px solid #FF3030;
    box-shadow:
        0 0 8px rgba(255,48,48,0.5),
        0 0 22px rgba(255,48,48,0.25),
        inset 0 0 12px rgba(255,48,48,0.08);
    text-shadow: 0 0 12px rgba(255,48,48,0.8);
}

.resultado-draw {
    color: #66BFFF;
    border: 1px solid #168BFF;
    box-shadow:
        0 0 8px rgba(22,139,255,0.5),
        0 0 22px rgba(22,139,255,0.25),
        inset 0 0 12px rgba(22,139,255,0.08);
    text-shadow: 0 0 12px rgba(22,139,255,0.8);
}

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

div[data-testid="stAlert"] {
    background: #1B1B1B;
    border-radius: 12px;
    border: 1px solid #555555;
    color: white;
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
    print("El dato ha sido publicado")


# ==========================================
# CONFIGURACIÓN MQTT
# ==========================================

broker = "broker.mqttdashboard.com"
port = 1883

client1 = paho.Client(client_id="GIT-HUBC")
client1.on_publish = on_publish

client1.connect(broker, port, keepalive=60)

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
# FUNCIONES DEL JUEGO
# ==========================================

def detectar_jugada(transcripcion):

    patrones = {
        "piedra": r"\bpiedra\b",
        "papel": r"\bpapel\b",
        "tijera": r"\btijera(s)?\b"
    }

    texto = transcripcion.lower().strip()

    for gesto, patron in patrones.items():

        if re.search(patron, texto):
            return gesto

    return None


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
# RECONOCIMIENTO POR VOZ
# ==========================================

st.markdown("### 🎙️ Reconocimiento de voz")

st.write("Presiona el botón y di claramente: piedra, papel o tijera.")


boton = Button(
    label="🎙️ Hablar",
    button_type="primary",
    width=250
)


# ==========================================
# JAVASCRIPT PARA RECONOCIMIENTO DE VOZ
# ==========================================

boton.js_on_event(
    "button_click",
    CustomJS(code="""
        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {

            document.dispatchEvent(
                new CustomEvent("GET_TEXT", {
                    detail: "ERROR_NAVEGADOR"
                })
            );

        } else {

            const recognition = new SpeechRecognition();

            recognition.lang = "es-CO";
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.onresult = function(event) {

                const texto =
                    event.results[0][0].transcript;

                document.dispatchEvent(
                    new CustomEvent("GET_TEXT", {
                        detail: texto
                    })
                );
            };

            recognition.onerror = function(event) {

                document.dispatchEvent(
                    new CustomEvent("GET_TEXT", {
                        detail: "ERROR_MICROFONO"
                    })
                );
            };

            recognition.start();
        }
    """)
)


# ==========================================
# MOSTRAR BOTÓN Y RECIBIR TEXTO
# ==========================================

resultado_voz = streamlit_bokeh_events(
    boton,
    events="GET_TEXT",
    key="voz_piedra_papel_tijera",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)


# ==========================================
# PROCESAR JUGADA
# ==========================================

if resultado_voz and "GET_TEXT" in resultado_voz:

    transcripcion = resultado_voz["GET_TEXT"]


    if transcripcion == "ERROR_NAVEGADOR":

        st.error(
            "Tu navegador no permite el reconocimiento de voz. "
            "Prueba con Google Chrome."
        )


    elif transcripcion == "ERROR_MICROFONO":

        st.error(
            "No se pudo acceder al micrófono. "
            "Revisa los permisos del navegador."
        )


    else:

        st.markdown("### 🗣️ Lo que dijiste")

        st.markdown(
            f'<div class="gesto-detectado">{transcripcion.upper()}</div>',
            unsafe_allow_html=True
        )

        jugador = detectar_jugada(transcripcion)


        if jugador is None:

            st.warning(
                "No se reconoció una jugada válida. "
                "Di piedra, papel o tijera."
            )


        else:

            st.markdown("### ✋ Tu jugada")

            st.markdown(
                f'<div class="gesto-detectado">{jugador.upper()}</div>',
                unsafe_allow_html=True
            )


            # ==========================================
            # PUBLICAR JUGADA ORIGINAL POR MQTT
            # ==========================================

            mensaje = {
                "gesto": jugador
            }

            client1.publish(
                "voice_ctrl",
                json.dumps(mensaje),
                qos=0,
                retain=False
            )

            time.sleep(0.2)


            # ==========================================
            # ELECCIÓN DE LA COMPUTADORA
            # ==========================================

            opciones = [
                "piedra",
                "papel",
                "tijera"
            ]

            maquina = random.choice(opciones)

            st.markdown("### 🤖 Jugada de la computadora")

            st.markdown(
                f'<div class="gesto-detectado">{maquina.upper()}</div>',
                unsafe_allow_html=True
            )


            # ==========================================
            # DETERMINAR GANADOR
            # ==========================================

            st.divider()

            st.markdown("### 🏆 Resultado de la ronda")

            ganador = determinar_ganador(
                jugador,
                maquina
            )


            if ganador == "empate":

                st.markdown(
                    '<div class="resultado resultado-draw">🤝 ¡EMPATE! Ambos eligieron el mismo gesto.</div>',
                    unsafe_allow_html=True
                )

                # ENVIAR EMPATE AL ESP32
                enviar_resultado("Empate")


            elif ganador == "jugador":

                st.markdown(
                    f'<div class="resultado resultado-win">🏆 ¡GANASTE! Tu {jugador} vence a {maquina}.</div>',
                    unsafe_allow_html=True
                )

                # ENVIAR VICTORIA AL ESP32
                enviar_resultado("Gana")


            else:

                st.markdown(
                    f'<div class="resultado resultado-lose">😢 ¡PERDISTE! La {maquina} de la computadora vence a tu {jugador}.</div>',
                    unsafe_allow_html=True
                )

                # ENVIAR DERROTA AL ESP32
                enviar_resultado("Pierde")

                mostrar_consejo_aleatorio()

