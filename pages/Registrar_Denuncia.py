import streamlit as st
import streamlit.components.v1 as components
import src.utils as utils

st.set_page_config(page_title="Registrar Denúncia", layout="wide")

st.title("Canal de Denúncias")
st.markdown("### Envie seu relato de forma segura")

st.info("Este canal é seguro e pode ser utilizado para denúncias anônimas ou identificadas.")

# URL do formulário Google Forms (pode ser movido para config/secrets futuramente)
URL_DO_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeALRJNlUyGh4K7stmuRavAkDrYn8b4SpSqhhIyE681QxnPBA/viewform?embedded=true"

# Renderiza o formulário
components.iframe(URL_DO_FORM, height=1200, scrolling=True)

st.markdown(utils.footer(), unsafe_allow_html=True)
