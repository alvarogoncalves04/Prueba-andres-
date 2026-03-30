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
    st.session_state.vidas = 7
    st.session_state.mensaje = ("info", "Introduce un número y dale a ENTER")
    st.session_state.terminado = False

# --- LÓGICA DEL JUEGO ---
def procesar_jugada():
    if st.session_state.input_jugada and not st.session_state.terminado:
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
        
        if st.session_state.vidas == 0:
            st.session_state.terminado = True

# --- DISEÑO DE LA INTERFAZ ---
st.title("🎮 Adivinanza Estadística v2.0")
st.markdown("### Facultad de Ciencias - Universidad Central de Venezuela")
st.write("---")

col_juego, col_stats = st.columns([0.4, 0.6], gap="large")

with col_juego:
    st.subheader("🕹️ Panel de Control")
    
    dificultad = st.select_slider(
        "Selecciona el rango de búsqueda:", 
        options=["Fácil (1-50)", "Normal (1-100)", "Modo UCV (1-500)"]
    )
    max_val = 50 if "Fácil" in dificultad else 100 if "Normal" in dificultad else 500
    
    if isinstance(st.session_state.vidas, int):
        st.write(f"Vidas restantes: {'❤️' * st.session_state.vidas} ({st.session_state.vidas})")
    else:
        st.write("✨ **¡Felicidades, ganaste!** ✨")

    st.number_input(
        f"Adivina el número (1-{max_val}):", 
        min_value=1, 
        max_value=max_val, 
        key="input_jugada",
        on_change=procesar_jugada,
        disabled=st.session_state.terminado
    )
    
    tipo, texto = st.session_state.mensaje
    if tipo == "warning": st.warning(texto)
    elif tipo == "success": st.success(texto)
    elif tipo == "info": st.info(texto)

    if st.session_state.vidas == 0:
        st.error(f"¡GAME OVER! El número secreto era {st.session_state.secreto}. 💀")

    if st.button("🔄 Reiniciar Partida"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

with col_stats:
    st.subheader("📈 Análisis de Datos")
    
    if st.session_state.historial:
        m1, m2 = st.columns(2)
        m1.metric("Total de Intentos", st.session_state.intentos)
        
        # OCULTAR LA RESPUESTA: Solo se muestra si el juego terminó
        if st.session_state.terminado:
            error_val = abs(st.session_state.secreto - st.session_state.historial[-1])
            m2.metric("Distancia al objetivo", "¡Encontrado!" if error_val == 0 else "Fin del juego")
        else:
            m2.metric("Distancia al objetivo", "???") # <--- Secreto guardado

        df = pd.DataFrame({
            "Intento": range(1, len(st.session_state.historial) + 1), 
            "Valor": st.session_state.historial
        })
        
        fig = px.line(df, x="Intento", y="Valor", title="Convergencia de tus predicciones", markers=True)
        
        # La línea verde también se oculta hasta el final
        if st.session_state.terminado:
            fig.add_hline(y=st.session_state.secreto, line_dash="dash", line_color="green", annotation_text="Objetivo")
        
        fig.update_yaxes(range=[0, max_val + 20])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aquí aparecerá el análisis cuando hagas tu primer intento.")

st.sidebar.markdown("---")
st.sidebar.write("🏫 **UCV - Estadística**")
