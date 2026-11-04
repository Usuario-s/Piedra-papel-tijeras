

import streamlit as st

st.set_page_config(
    page_title="Piedra, Papel o Tijera | Instrucciones",
    page_icon="✊",
    layout="centered"
)

# ==========================================
# ESTILOS CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(145deg, #080808 0%, #141414 55%, #090909 100%);
    color: #FFFFFF;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

/* Contenedor principal */
.block-container {
    max-width: 850px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Título principal */
.main-title {
    color: #FFFFFF;
    text-align: center;
    font-size: 40px;
    font-weight: 900;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.subtitle {
    color: #999999;
    text-align: center;
    font-size: 16px;
    margin-bottom: 35px;
}

/* Separador */
.separator {
    height: 1px;
    background: linear-gradient(90deg, transparent, #505050, transparent);
    margin: 25px 0;
}

/* Títulos */
.section-title {
    color: #FFFFFF;
    font-size: 23px;
    font-weight: 850;
    margin-bottom: 15px;
    margin-top: 25px;
}

/* Tarjetas */
.card {
    background: linear-gradient(135deg, #202020, #181818);
    border: 1px solid #353535;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 14px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.20);
}

/* Texto */
.card-text {
    color: #D0D0D0;
    font-size: 15px;
    line-height: 1.8;
}

/* Texto destacado */
.card-text strong {
    color: #FFFFFF;
    font-weight: 800;
}

/* Títulos de jugadas */
.move-title {
    color: #FFFFFF;
    font-size: 19px;
    font-weight: 850;
    margin-bottom: 8px;
}

/* Iconos */
.move-icon {
    font-size: 27px;
    margin-right: 8px;
}

/* Pasos */
.step {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    margin-bottom: 17px;
}

.step:last-child {
    margin-bottom: 0;
}

.step-number {
    background: #353535;
    border: 1px solid #505050;
    color: #FFFFFF;
    min-width: 30px;
    height: 30px;
    border-radius: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: 800;
    font-size: 14px;
}

.step-description {
    color: #D0D0D0;
    font-size: 15px;
    line-height: 1.7;
    padding-top: 3px;
}

/* Resultados */
.result-row {
    padding: 12px 0;
    border-bottom: 1px solid #353535;
    color: #D0D0D0;
    font-size: 15px;
    line-height: 1.7;
}

.result-row:last-child {
    border-bottom: none;
}

.result-row strong {
    color: #FFFFFF;
    font-weight: 800;
}

/* Pie de página */
.final-message {
    text-align: center;
    padding: 25px 15px;
    background: linear-gradient(135deg, #242424, #171717);
    border: 1px solid #393939;
    border-radius: 15px;
    margin-top: 25px;
}

.final-title {
    color: #FFFFFF;
    font-size: 23px;
    font-weight: 900;
    margin-bottom: 10px;
}

.final-text {
    color: #AAAAAA;
    font-size: 14px;
    line-height: 1.7;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# ENCABEZADO
# ==========================================

st.markdown("""
<div class="main-title">
    ✊ PIEDRA, PAPEL O TIJERA
</div>

<div class="subtitle">
    Instrucciones del juego · Jugador vs Computadora
</div>

<div class="separator"></div>
""", unsafe_allow_html=True)


# ==========================================
# OBJETIVO
# ==========================================

st.markdown("""
<div class="section-title">🎯 Objetivo del juego</div>

<div class="card">
    <div class="card-text">
        Compite contra la computadora y consigue la mayor cantidad
        de victorias posibles. En cada ronda, ambos deberán elegir
        entre piedra, papel o tijera. ¡Demuestra quién tiene la mejor estrategia!
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# REGLAS
# ==========================================

st.markdown("""
<div class="section-title">📖 Las reglas</div>

<div class="card">
    <div class="move-title">✊ Piedra</div>
    <div class="card-text">
        Vence a la tijera porque la rompe, pero pierde contra el papel
        porque este la envuelve.
    </div>
</div>

<div class="card">
    <div class="move-title">✋ Papel</div>
    <div class="card-text">
        Vence a la piedra porque la envuelve, pero pierde contra la tijera
        porque esta lo corta.
    </div>
</div>

<div class="card">
    <div class="move-title">✌️ Tijera</div>
    <div class="card-text">
        Vence al papel porque lo corta, pero pierde contra la piedra
        porque esta la rompe.
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# DINÁMICA DEL JUEGO
# ==========================================

st.markdown("""
<div class="section-title">⚡ ¿Cómo jugar?</div>

<div class="card">

    <div class="step">
        <div class="step-number">1</div>
        <div class="step-description">
            <strong>Selecciona tu jugada.</strong><br>
            Elige entre piedra, papel o tijera.
        </div>
    </div>

    <div class="step">
        <div class="step-number">2</div>
        <div class="step-description">
            <strong>Turno de la computadora.</strong><br>
            La máquina elegirá automáticamente una opción al azar.
        </div>
    </div>

    <div class="step">
        <div class="step-number">3</div>
        <div class="step-description">
            <strong>Comparación de jugadas.</strong><br>
            El sistema comparará ambas elecciones para determinar el resultado.
        </div>
    </div>

    <div class="step">
        <div class="step-number">4</div>
        <div class="step-description">
            <strong>Resultado de la ronda.</strong><br>
            Descubre quién ganó y consulta la actualización del marcador.
        </div>
    </div>

</div>
""", unsafe_allow_html=True)


# ==========================================
# RESULTADOS
# ==========================================

st.markdown("""
<div class="section-title">🏆 Resultados de cada ronda</div>

<div class="card">

    <div class="result-row">
        <strong>VICTORIA</strong><br>
        Si tu elección vence a la de la computadora, ganas un punto.
    </div>

    <div class="result-row">
        <strong>DERROTA</strong><br>
        Si la computadora elige una opción que vence a la tuya,
        ella gana la ronda.
    </div>

    <div class="result-row">
        <strong>EMPATE</strong><br>
        Si ambos seleccionan la misma opción, ninguno obtiene puntos.
    </div>

</div>
""", unsafe_allow_html=True)


# ==========================================
# MENSAJE FINAL
# ==========================================

st.markdown("""
<div class="separator"></div>

<div class="final-message">

    <div class="final-title">
        ¿Estás listo para jugar?
    </div>

    <div class="final-text">
        Elige tu jugada, supera a la computadora y demuestra
        quién es el verdadero campeón.
        <br><br>
        <strong style="color: #FFFFFF;">
            ¡Que comience el desafío!
        </strong>
    </div>

</div>
""", unsafe_allow_html=True)

