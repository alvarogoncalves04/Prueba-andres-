import streamlit as st
import random
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(page_title="UCV Stats Game", page_icon="📊", layout="wide")

# 2. Inicializar variables de estado CON SEGURIDAD
if 'secreto' not in st.session_state:
    st.session_state.secreto = random.randint(1, 100)
    st.session_state.intentos = 0
    st.session_state.historial = []
    st.session_state.vidas = 7
    st.session_state.mensaje = ("info", "Introduce un número y dale a ENTER")
    st.session_state.terminado = False

# --- LÓGICA DEL JUEGO ---
def procesar_jugada():
    # Validación extra de que las variables existen
    if 'input_jugada' in st.session_state and not st.session_state.terminado:
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
            st.session_state.terminado = True
        
        if isinstance(st.session_state.vidas, int) and st.session_state.vidas <= 0:
            st.session_state.terminado = True

# --- DISEÑO DE LA INTERFAZ ---
st.title("🎮 Adivinanza Estadística v2.0")
st.markdown("### Facultad de Ciencias - Universidad Central de Venezuela")
st.write("---")

col_juego, col_stats = st.columns([0.4, 0.6], gap="large")

with col_juego:
    st.subheader("🕹️ Panel de Control")
    
    dificultad = st.select_slider(
        "Rango de búsqueda:", 
        options=["Fácil (1-50)", "Normal (1-100)", "Modo UCV (1-500)"],
        value="Normal (1-100)"
    )
    max_val = 50 if "Fácil" in dificultad else 100 if "Normal" in dificultad else 500
    
    # Mostrar Vidas
    if isinstance(st.session_state.vidas, int):
        st.write(f"Vidas: {'❤️' * st.session_state.vidas} ({st.session_state.vidas})")
    else:
        st.write("✨ **¡Victoria!** ✨")

    # Input con seguro para el error de la línea 66
    esta_terminado = st.session_state.get('terminado', False)
    
    st.number_input(
        f"Adivina (1-{max_val}):", 
        min_value=1, 
        max_value=max_val, 
        key="input_jugada",
        on_change=procesar_jugada,
        disabled=esta_terminado
    )
    
    tipo, texto = st.session_state.mensaje
    if tipo == "warning": st.warning(texto)
    elif tipo == "success": st.success(texto)
    elif tipo == "info": st.info(texto)

    if esta_terminado and st.session_state.vidas != "GANADOR":
        st.error(f"GAME OVER. El secreto era {st.session_state.secreto}. 💀")

    if st.button("🔄 Reiniciar Partida"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

with col_stats:
    st.subheader("📈 Análisis de Datos")
    
    if st.session_state.historial:
        m1, m2 = st.columns(2)
        m1.metric("Intentos", st.session_state.intentos)
        
        # Oculto hasta el final
        if st.session_state.get('terminado', False):
            m2.metric("Objetivo", st.session_state.secreto)
        else:
            m2.metric("Objetivo", "???")

        df = pd.DataFrame({
            "Intento": range(1, len(st.session_state.historial) + 1), 
            "Valor": st.session_state.historial
        })
        
        fig = px.line(df, x="Intento", y="Valor", markers=True, template="plotly_dark")
        
        if st.session_state.get('terminado', False):
            fig.add_hline(y=st.session_state.secreto, line_dash="dash", line_color="green")
        
        fig.update_yaxes(range=[0, max_val + 10])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Haz tu primer intento para ver los datos.")

st.sidebar.write("🏫 **UCV - Estadística**")
