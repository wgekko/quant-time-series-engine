import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Star Wars Dashboard", 
    page_icon="icons/icons8-la-guerra-de-las-galaxias-64.png", 
    layout="wide"
)

# Estilos CSS unificados (Sidebar oculto, fondo oscuro, color corregido y animación crawl)
st.markdown(
    """
    <style>
    /* Ocultar completamente la barra lateral y su espacio reservado */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Ocultar el botón flotante de colapsar/expandir sidebar */
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Fondo general de la aplicación */
    .stApp {
        background-color: #050505;
    }

    /* Estilo del título principal (Sintaxis de color corregida) */
    .titulo-init {
        text-align: center;
        font-family: 'Courier New', monospace;
        color: #ffe81f !important;
        letter-spacing: 4px;
        margin-top: 20px;
        margin-bottom: 20px;
        font-weight: bold;
    }

    /* Estilos para el texto Star Wars crawl */
    .starwars-crawl {
        display: flex;
        justify-content: center;
        height: 200px;
        perspective: 250px;
        color: #ffe81f;
        font-family: 'Century Gothic', sans-serif;
        font-weight: bold;
        overflow: hidden;
        margin-bottom: -10px;
    }
    .crawl-text {
        position: relative;
        top: 9999px;
        transform-origin: 50% 100%;
        animation: crawl 30s linear infinite;
        text-align: center;
    }
    .crawl-text h2 {
        font-size: 26px;
        color: #ffe81f;
        margin-bottom: 5px;
    }
    .crawl-text h3 {
        font-size: 22px;
        color: #ffe81f;
        margin-bottom: 5px;
    }
    .crawl-text p {
        font-size: 18px;
        color: #ffe81f;
    }
    @keyframes crawl {
        0% { top: 0; transform: rotateX(30deg) translateZ(0); }
        100% { top: -350px; transform: rotateX(40deg) translateZ(-100px); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h2 class='titulo-init'>Quant Time-Series Engine</h2>",
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="starwars-crawl">
        <div class="crawl-text">
            <h2>EPISODIO IV</h2>
            <h3>EN LOS MODELOS QUANT DE LA FUERZA</h3>
            <h3>Y LA AMENAZA DE LA VOLATILIDAD</h3>
            <p>Es un período de profunda incertidumbre analítica...</p>
            <p>Los mercados avanzan sin tregua, sembrando el caos en toda la galaxia financiera...</p>
            <p>Mientras el riesgo acecha en cada rincón... </p>
            <p>Un valiente arsenal de modelos cuantitativos se alza para resistir...</p>
            <p>Armados con herramientas de precisión y algoritmos estelares...</p>
            <p>Están listos para descifrar los escenarios venideros....</p>
            <p>Y restaurar el equilibrio en los mercados.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Contenedor para centrar el video y el botón
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
  # Inyectar el video en bucle, reproducción automática y silenciado
  st.video(
      "video/Luke Skywalker-Darth Vader.mp4",
      format="video/mp4",
      autoplay=True,
      loop=True,
      muted=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)

  # Botón de acceso que redirige directamente a la página en pages/app.py
  if st.button(
      "Presiona el botón para sincronizarte con la Fuerza.",
      use_container_width=True,
      type="primary",
  ):
    st.switch_page("pages/app.py")

