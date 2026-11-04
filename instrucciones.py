
import streamlit as st

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Instrucciones - Piedra, Papel o Tijera",
    page_icon="✊",
    layout="centered"
)

# ==========================================
# DISEÑO CSS
# ==========================================

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background: linear-gradient(135deg, #050505, #111111, #080808);
    color: white;
}

/* Ocultar menú y footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Título principal */
.main-title {
    text-align: center;
    color: #FFFFFF;
    font-size: 42px;
    font-weight: 900;
    margin-bottom: 5px;
}

/* Subtítulo */
.subtitle {
    text-align: center;
    color: #AAAAAA;
    font-size: 16px;
    margin-bottom: 35px;
}

/* Títulos de sección */
.section-title {
    color: #FFFFFF;
    font-size: 23px;
    font-weight: 900;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* Tarjetas */
.instruction-card {
    background: #181818;
    border: 1px solid #333333;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
}

/* Texto de tarjetas */
.card-text {
    color: #E5E5E5;
    font-size: 16px;
    line-height: 1.7;
}

/* Nombres de jugadas */
.move-title {
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 8px;
}

/* Separador */
hr {
    border-color: #333333;
}

/* Texto destacado */
.highlight {
    color: #FFFFFF;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# CONTENIDO
# ==========================================

st.markdown("""
<div class="main-title">
    ✊ PIEDRA, PAPEL O TIJERA
</div>

<div class="subtitle">
    Aprende las reglas y prepárate para desafiar a la computadora.
</div>
""", unsafe_allow_html=True)


# OBJETIVO
st.markdown("""
<div class="section-title">🎯 Objetivo del juego</div>

<div class="instruction-card">
    <div class="card-text">
        El objetivo es competir contra la computadora y conseguir
        la mayor cantidad de victorias posibles. En cada ronda,
        ambos deberán elegir entre piedra, papel o tijera.
    </div>
</div>
""", unsafe_allow_html=True)


# REGLAS
st.markdown("""
<div class="section-title">📖 ¿Cómo se juega?</div>

<div class="instruction-card">
    <div class="move-title">✊ Piedra</div>
    <div class="card-text">
        La piedra vence a la tijera porque la rompe,
        pero pierde contra el papel porque este la envuelve.
    </div>
</div>

<div class="instruction-card">
    <div class="move-title">✋ Papel</div>
    <div class="card-text">
        El papel vence a la piedra porque la envuelve,
        pero pierde contra la tijera porque esta lo corta.
    </div>
</div>

<div class="instruction-card">
    <div class="move-title">✌️ Tijera</div>
    <div class="card-text">
        La tijera vence al papel porque lo corta,
        pero pierde contra la piedra porque esta la rompe.
    </div>
</div>
""", unsafe_allow_html=True)


# DINÁMICA
st.markdown("""
<div class="section-title">⚡ Dinámica de cada ronda</div>

<div class="instruction-card">
    <div class="card-text">
        <b>1.</b> Selecciona una de las tres opciones: piedra, papel o tijera.<br><br>

        <b>2.</b> La computadora elegirá automáticamente una opción al azar.<br><br>

        <b>3.</b> El juego comparará ambas elecciones y determinará quién gana.<br><br>

        <b>4.</b> El resultado aparecerá en pantalla y se actualizará el marcador.
    </div>
</div>
""", unsafe_allow_html=True)


# CONDICIONES
st.markdown("""
<div class="section-title">🏆 ¿Cómo se determina el ganador?</div>

<div class="instruction-card">
    <div class="card-text">
        <b>Victoria:</b> Si tu elección vence a la de la computadora,
        ganas un punto.<br><br>

        <b>Derrota:</b> Si la computadora elige una opción que vence a la tuya,
        ella gana la ronda.<br><br>

        <b>Empate:</b> Si ambos seleccionan la misma opción,
        ninguno obtiene puntos.
    </div>
</div>
""", unsafe_allow_html=True)


# CONSEJO FINAL
st.markdown("""
<hr>

<div style="
    text-align: center;
    padding: 20px;
">
    <div style="
        color: white;
        font-size: 23px;
        font-weight: 900;
        margin-bottom: 10px;
    ">
        ¿Estás listo para jugar?
    </div>

    <div style="
        color: #AAAAAA;
        font-size: 15px;
    ">
        ¡Elige tu jugada, vence a la computadora y demuestra
        quién es el verdadero campeón!
    </div>
</div>
""", unsafe_allow_html=True)
