
import streamlit as st

st.set_page_config(
    page_title="Piedra, Papel o Tijera",
    page_icon="✊",
    layout="centered"
)

# ==========================================
# DISEÑO GENERAL
# ==========================================

st.markdown("""
<style>

/* Fondo */
.stApp {
    background: linear-gradient(135deg, #080808, #151515, #090909);
    color: #FFFFFF;
}

/* Contenedor */
.block-container {
    max-width: 850px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Ocultar elementos */
#MainMenu, footer {
    visibility: hidden;
}

/* Textos generales */
.stMarkdown, .stMarkdown p {
    color: #D0D0D0;
}

/* Título principal */
h1 {
    color: #FFFFFF !important;
    font-size: 38px !important;
    font-weight: 900 !important;
    text-align: center;
    letter-spacing: 1px;
}

/* Subtítulos */
h2, h3 {
    color: #FFFFFF !important;
    font-weight: 850 !important;
}

/* Separadores */
hr {
    border-color: #393939;
}

/* Contenedores de tarjetas */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, #222222, #181818);
    border: 1px solid #383838;
    border-radius: 14px;
    padding: 15px;
}

/* Texto */
p {
    line-height: 1.8;
}

/* Texto secundario */
.caption {
    color: #999999;
    text-align: center;
}

/* Espaciado */
div[data-testid="stMarkdownContainer"] {
    color: #D0D0D0;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# ENCABEZADO
# ==========================================

st.title("✊ PIEDRA, PAPEL O TIJERA")

st.markdown(
    "<p style='text-align:center; color:#999999;'>"
    "INSTRUCCIONES DEL JUEGO · JUGADOR VS COMPUTADORA"
    "</p>",
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# OBJETIVO
# ==========================================

st.subheader("🎯 Objetivo del juego")

with st.container(border=True):
    st.write(
        "Compite contra la computadora y consigue la mayor cantidad "
        "de victorias posibles. En cada ronda, ambos deberán elegir "
        "entre piedra, papel o tijera."
    )

st.write("")


# ==========================================
# REGLAS
# ==========================================

st.subheader("📖 Las reglas")

with st.container(border=True):
    st.markdown("### ✊ Piedra")
    st.write(
        "Vence a la tijera porque la rompe, pero pierde contra "
        "el papel porque este la envuelve."
    )

with st.container(border=True):
    st.markdown("### ✋ Papel")
    st.write(
        "Vence a la piedra porque la envuelve, pero pierde contra "
        "la tijera porque esta lo corta."
    )

with st.container(border=True):
    st.markdown("### ✌️ Tijera")
    st.write(
        "Vence al papel porque lo corta, pero pierde contra "
        "la piedra porque esta la rompe."
    )

st.write("")


# ==========================================
# DINÁMICA DEL JUEGO
# ==========================================

st.subheader("⚡ ¿Cómo jugar?")

with st.container(border=True):

    st.markdown("**01 — Selecciona tu jugada**")
    st.write("Elige entre piedra, papel o tijera.")

    st.divider()

    st.markdown("**02 — Turno de la computadora**")
    st.write("La máquina elegirá automáticamente una opción al azar.")

    st.divider()

    st.markdown("**03 — Comparación de jugadas**")
    st.write(
        "El sistema comparará ambas elecciones para determinar "
        "el resultado de la ronda."
    )

    st.divider()

    st.markdown("**04 — Resultado**")
    st.write(
        "Descubre quién ganó y consulta la actualización del marcador."
    )

st.write("")


# ==========================================
# RESULTADOS
# ==========================================

st.subheader("🏆 Resultados de cada ronda")

with st.container(border=True):

    st.markdown("**<span style='color:#FFFFFF;'>VICTORIA</span>**", unsafe_allow_html=True)
    st.write(
        "Si tu elección vence a la de la computadora, ganas un punto."
    )

    st.divider()

    st.markdown("**DERROTA**")
    st.write(
        "Si la computadora elige una opción que vence a la tuya, "
        "ella gana la ronda."
    )

    st.divider()

    st.markdown("**EMPATE**")
    st.write(
        "Si ambos seleccionan la misma opción, ninguno obtiene puntos."
    )

st.write("")
st.divider()


# ==========================================
# MENSAJE FINAL
# ==========================================

with st.container(border=True):

    st.markdown(
        "<h3 style='text-align:center; color:white;'>"
        "¿Estás listo para jugar?"
        "</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; color:#AAAAAA;'>"
        "Elige tu jugada, supera a la computadora y demuestra "
        "quién es el verdadero campeón."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; color:white; font-weight:bold;'>"
        "Elige si quieres jugar con gestos o voz"
        "</p>",
        unsafe_allow_html=True
    )


