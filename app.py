import streamlit as st
import random
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(page_title="UCV Stats Game", page_icon="📊", layout="wide")

# 2. Inicializar variables de estado
if 'secreto' not in st.session_state:
    st.session_state.secreto = random.randint(1, 100)
    st.session_state.intentos = 0
    st.session_state.historial = []
    st.session_state.vidas = 7  # Te di un par de vidas extra

# --- INTERFAZ PRINCIPAL ---
st.title("🎮 Adivinanza Estadística v2.0")
st.markdown("### Proyecto: Computación para Estadística - UCV")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🕹️ ¡A jugar!")
    
    # Selector de Dificultad
    dificultad = st.select_slider(
        "Selecciona dificultad:", 
        options=["Fácil (1-50)", "Normal (1-100)", "Modo UCV (1-500)"]
    )
    
    # Ajustar rango según dificultad
    max_val = 50 if "Fácil" in dificultad else 100 if "Normal" in dificultad else 500
    
    st.write(f"Vidas restantes: {'❤️' * st.session_state.vidas}")
    
    # Input de número
    numero = st.number_input("Introduce tu número:", min_value=1, max_value=max_val, key="input_jugada")
    
    if st.button("Presiona aqui para ver el resultado"):
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
        
    if st.session_state.vidas <= 0:
        st.error(f"GAME OVER. El número era {st.session_state.secreto}. 💀")
        if st.button("Reiniciar Partida"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

with col2:
    st.subheader("📈 Análisis de Datos")
    
    if st.session_state.historial:
        # Mostrar tabla de datos
        df = pd.DataFrame({
            "Intento": range(1, len(st.session_state.historial) + 1), 
            "Valor": st.session_state.historial
        })
        
        # Gráfico con Plotly
        fig = px.line(df, x="Intento", y="Valor", title="Convergencia al Objetivo", markers=True)
        fig.add_hline(y=st.session_state.secreto, line_dash="dash", line_color="green")
        st.plotly_chart(fig, use_container_width=True)
        
        # Métrica estadística
        st.metric("Total de Intentos", st.session_state.intentos)
    else:
        st.info("Haz tu primer intento para ver las estadísticas.")

# Barra lateral
st.sidebar.markdown("---")
st.sidebar.write("🏫 **Universidad Central de Venezuela**")
st.sidebar.write("📊 Facultad de Ciencias - Estadística")
