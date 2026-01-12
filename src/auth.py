import streamlit as st
import src.utils as utils
from streamlit_google_auth import Authenticate

if 'connected' not in st.session_state:
    st.session_state['connected'] = False

SECRET_PATH = '.streamlit/client_secret_100094970846-lsbpg08p65j87i4i0gvj66b1qnnlm155.apps.googleusercontent.com.json'

authenticator = Authenticate(
    secret_credentials_path=SECRET_PATH,
    cookie_name='cpcad_auth_cookie',
    cookie_key='digite_aqui_uma_frase_bem_longa_e_aleatoria_para_seguranca',
    redirect_uri='http://localhost:8501',
)

def show_user_sidebar():
    if st.session_state.get('connected'):
        with st.sidebar:
            user_info = st.session_state.get('user_info', {})
            if user_info.get('picture'):
                st.image(user_info['picture'], width=60)
            
            st.write(f"**Usuário:** {user_info.get('name', 'Não identificado')}")
            st.caption(user_info.get('email', ''))
            
            if st.button("Sair", type="secondary"):
                authenticator.logout()

def check_password():
    authenticator.check_authentification()

    if not st.session_state.get('connected'):
        st.image(utils.TJRO_IMAGE, width=200)
        st.title("Sistema de Gestão CPCAD")
        st.info("Por favor, faça login com seu e-mail institucional.")
        authenticator.login()
        return False
    
    show_user_sidebar()
            
    return True

def logout():
    authenticator.logout()