import streamlit as st
from groq import Groq

# Configuración de la página de Streamlit
st.set_page_config(page_title="Mi chat de IA", page_icon="🤖", layout="centered")

# Lista de modelos disponibles
MODELOS = ['llama3-8b-8192', 'llama3-70b-32768', 'mixtral-8x7b-32768']

# Función para configurar la página y el modelo
def configurar_pagina():
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración de la IA")
    elegirModelo = st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    return elegirModelo

# Crear el cliente de Groq utilizando la clave API
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]  # La clave debe estar en .streamlit/secrets.toml
    return Groq(api_key=clave_secreta)

# Inicializar el cliente y el modelo seleccionado
cliente = crear_usuario_groq()
modelo = configurar_pagina()

# Entrada de chat del usuario
mensaje = st.chat_input("Escribí tu mensaje:")

# Función para actualizar el historial de mensajes
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

# Función para configurar y enviar el mensaje al modelo
def configurar_modelo(cliente, modelo, mensaje):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensaje}]
    )
    return respuesta.choices[0].message.content  # Devuelve el contenido de la respuesta

# Inicializar el estado de la sesión para almacenar mensajes
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# Función para mostrar el historial de mensajes
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

# Contenedor principal del área del chat
def area_chat():
    contenedorDelChat = st.container()
    with contenedorDelChat:
        mostrar_historial()

# Inicializa el estado y el área de chat
inicializar_estado()
area_chat()

# Procesa el mensaje enviado y actualiza el historial
if mensaje:
    # Muestra el mensaje del usuario en la terminal
    print(f"Mensaje del usuario: {mensaje}")
    
    # Almacena el mensaje del usuario en el historial
    actualizar_historial("user", mensaje, "🧑‍💻")
    
    # Obtiene la respuesta del modelo
    chat_completo = configurar_modelo(cliente, modelo, mensaje)
    
    # Muestra la respuesta del asistente en la terminal
    print(f"Respuesta del asistente: {chat_completo}")
    
    # Almacena la respuesta en el historial
    actualizar_historial("assistant", chat_completo, "🤖")
    
    # Recarga la aplicación para mostrar el nuevo mensaje
    st.rerun()
