import streamlit as st
import random
import pandas as pd
import plotly.express as px

# Configuración de página (Nivel 1: Look & Feel)
st.set_page_config(page_title="Juego de Andrés", page_icon="🎮📊")

st.title("🎮 ¡Bienvenido a mi juego!")
st.write("Prueba tu suerte adivinando el numero que estoy pensando. Cada vez que se reinicie el juego será un número diferente.")

# Estilo personalizado con CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_stdio=True)

# Inicializar variables de estado
if 'secreto' not in st.session_state:
    st.session_state.secreto = random.randint(1, 100)
    st.session_state.intentos = 0
    st.session_state.historial = []
    st.session_state.vidas = 5

# --- INTERFAZ PRINCIPAL ---
st.title("🎮 Adivinanza Estadística v2.0")
st.subheader("Proyecto: Computación para Estadística - UCV")

col1, col2 = st.columns([1, 1])

with col1:
    st.write("### 🕹️ ¡A jugar!")
    
    # Selector de Dificultad (Nivel 3: Lógica)
    dificultad = st.select_slider("Selecciona dificultad:", options=["Fácil (1-50)", "Normal (1-100)", "Modo UCV (1-500)"])
    max_val = 50 if "Fácil" in dificultad else 100 if "Normal" in dificultad else 500
    
    # Sistema de Vidas
    st.write(f"Vidas restantes: {'❤️' * st.session_state.vidas}")
    
    numero = st.number_input("Introduce tu apuesta:", min_value=1, max_value=max_val, key="input_jugada")
    
    if st.button("Lanzar"):
        if st.session_state.vidas > 0:
            st.session_state.intentos += 1
            st.session_state.historial.append(numero)
            
            if numero < st.session_state.secreto:
                st.warning("¡Más alto! ⬆️")
                st.session_state.vidas -= 1
            elif numero > st.session_state.secreto:
                st.warning("¡Más bajo! ⬇️")
                st.session_state.vidas -= 1
            else:
                st.success(f"¡LOGRADO! El número era {st.session_state.secreto}. 🎉")
                st.balloons()
        
        if st.session_state.vidas == 0 and numero != st.session_state.secreto:
            st.error(f"GAME OVER. El número era {st.session_state.secreto}. 💀")
            if st.button("Reiniciar Partida"):
                st.session_state.clear()
                st.rerun()

with col2:
    st.write("### 📈 Análisis de Datos (Real-time)")
    
    if st.session_state.historial:
        # Nivel 2: Estadística
        df = pd.DataFrame({"Intento": range(1, len(st.session_state.historial) + 1), 
                           "Valor": st.session_state.historial})
        
        # Gráfico de convergencia (Plotly)
        fig = px.line(df, x="Intento", y="Valor", title="Tu camino hacia el número real",
                      markers=True, line_shape="spline")
        fig.add_hline(y=st.session_state.secreto, line_dash="dash", line_color="green", annotation_text="Objetivo")
        st.plotly_chart(fig, use_container_width=True)
        
        # Cálculo de Probabilidad (Estadística básica)
        rango = max_val
        prob = (1/rango) * 100
        st.metric("Probabilidad de acierto (azar)", f"{prob:.2f}%")
    else:
        st.info("Haz tu primer intento para ver las estadísticas.")

# Pie de página
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Escudo_de_la_UCV.svg/1200px-Escudo_de_la_UCV.svg.png", width=100)
st.sidebar.write("Desarrollado por: Andrés")
