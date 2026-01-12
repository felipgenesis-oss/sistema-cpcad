import streamlit as st
import src.utils as utils
from streamlit_google_auth import Authenticate
import os
import json
import tempfile

# Caminho local do arquivo
LOCAL_SECRET_PATH = '.streamlit/client_secret_100094970846-lsbpg08p65j87i4i0gvj66b1qnnlm155.apps.googleusercontent.com.json'

def get_secret_path():
    """
    Retorna o caminho do arquivo de credenciais.
    1. Se o arquivo local existir, usa ele.
    2. Se não, tenta ler do st.secrets e cria um arquivo temporário.
    """
    if os.path.exists(LOCAL_SECRET_PATH):
        return LOCAL_SECRET_PATH
    
    if "google_oauth" in st.secrets:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump(dict(st.secrets["google_oauth"]), temp_file)
            return temp_file.name
            
    st.error("Arquivo de credenciais não encontrado e 'google_oauth' não configurado nos Secrets.")
    st.stop()
    return None

authenticator = Authenticate(
    secret_credentials_path=get_secret_path(),
    cookie_name='cpcad_auth_cookie',
    cookie_key='digite_aqui_uma_frase_bem_longa_e_aleatoria_para_seguranca',
    redirect_uri='http://localhost:8501',
)

def _ensure_session_state():
    """Garante que as variáveis de estado essenciais existam na sessão atual."""
    if 'connected' not in st.session_state:
        st.session_state['connected'] = False
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = {}

def show_user_sidebar():
    """Exibe informações do usuário na barra lateral se estiver logado."""
    _ensure_session_state()
    
    if st.session_state.get('connected'):
        with st.sidebar:
            user_info = st.session_state.get('user_info', {})
            if user_info.get('picture'):
                st.image(user_info['picture'], width=60)
            
            st.write(f"**Usuário:** {user_info.get('name', 'Não identificado')}")
            st.caption(user_info.get('email', ''))
            
            if st.button("Sair", type="secondary"):
                logout()

def check_password():
    """
    Verifica a autenticação. Retorna True se logado, False se não.
    Renderiza a tela de login se não estiver logado.
    """
    _ensure_session_state()
    authenticator.check_authentification()

    if not st.session_state.get('connected'):
        st.image(utils.TJRO_IMAGE, width=200)
        st.title("Sistema de Gestão CPCAD")
        st.info("Por favor, faça login com seu e-mail institucional.")
        authenticator.login()
        return False
    
    show_user_sidebar()
    return True

def require_auth():
    """Interrompe a execução se não estiver logado."""
    if not check_password():
        st.stop()

def check_session():
    """Verifica se o usuário já está logado via cookie, sem forçar tela de login."""
    _ensure_session_state()
    authenticator.check_authentification()
    show_user_sidebar()

def logout():
    authenticator.logout()