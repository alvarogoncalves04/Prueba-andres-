import streamlit as st
import random

st.set_page_config(page_title="Juego de Andrés", page_icon="🎮")

st.title("🎮 ¡Bienvenido a mi juego!")
st.write("Prueba tu suerte adivinando el numero que estoy pensando. Cada vez que se reinicie el juego será un número diferente.")

# Usamos session_state para que el juego no se reinicie al tocar un botón
if 'numero_secreto' not in st.session_state:
    st.session_state.numero_secreto = random.randint(1, 100)
    st.session_state.intentos = 0

# Interfaz de usuario
st.info("He pensado un número entre 1 y 100. ¡Adivínalo!")

numero = st.number_input("Tu número:", min_value=1, max_value=100, key="input_juego")

if st.button("Probar suerte"):
    st.session_state.intentos += 1
    if numero < st.session_state.numero_secreto:
        st.warning("Más alto... ⬆️")
    elif numero > st.session_state.numero_secreto:
        st.warning("Más bajo... ⬇️")
    else:
        st.success(f"¡GANASTE! 🎉 Lo lograste en {st.session_state.intentos} intentos.")
        st.balloons()
        if st.button("Reiniciar"):
            st.session_state.numero_secreto = random.randint(1, 100)
            st.session_state.intentos = 0
            st.rerun()

# Barra lateral con info
st.sidebar.write(f"Intentos: {st.session_state.intentos}")
