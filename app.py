import streamlit as st
import random
import pandas as pd
import plotly.express as px

# 1. Configuración de página - Modo Wide para aprovechar toda la pantalla
st.set_page_config(page_title="UCV Stats Game", page_icon="📊", layout="wide")

# 2. Inicializar variables de estado (Session State)
if 'secreto' not in st.session_state:
    st.session_state.secreto = random.randint(1, 100)
    st.session_state.intentos = 0
    st.session_state.historial = []
    st.session_state.vidas = 7
    st.session_state.mensaje = ("info", "Introduce un número y dale a ENTER")

# --- LÓGICA DEL JUEGO (Función para el Enter automático) ---
def procesar_jugada():
    # Solo procesa si hay un número y le quedan vidas
    if st.session_state.input_jugada and isinstance(st.session_state.vidas, int) and st.session_state.vidas > 0:
        val = st.session_state.input_jugada
        st.session_state.intentos += 1
        st.session_state.historial.append(val)
        
        if val < st.session_state.secreto:
            st.session_state.mensaje = ("warning", f"¡Más alto que {val}! ⬆️")
            st.session_state.vidas -= 1
        elif val > st.session_state.secreto:
            st.session_state.mensaje = ("warning", f"¡Más bajo que {val}! ⬇️")
            st.session_state.vidas -= 1
        else:
            st.session_state.mensaje = ("success", f"¡LOGRADO! Era el {val}. 🎉")
            st.session_state.vidas = "GANADOR"

# --- DISEÑO DE LA INTERFAZ ---
st.title("🎮 Adivinanza Estadística v2.0")
st.markdown("### Facultad de Ciencias - Universidad Central de Venezuela")
st.write("---")

# Separación en Columnas: 40% Juego, 60% Análisis
col_juego, col_stats = st.columns([0.4, 0.6], gap="large")

# --- COLUMNA IZQUIERDA: EL JUEGO ---
with col_juego:
    st.subheader("🕹️ Panel de Control")
    
    # Selector de Dificultad (Nivel 3)
    dificultad = st.select_slider(
        "Selecciona el rango de búsqueda:", 
        options=["Fácil (1-50)", "Normal (1-100
