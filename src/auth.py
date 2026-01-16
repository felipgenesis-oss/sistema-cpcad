import streamlit as st
import src.utils as utils
from streamlit_google_auth import Authenticate
import os
import json
import tempfile
from streamlit_gsheets import GSheetsConnection

LOCAL_SECRET_PATH = '.streamlit/client_secret_100094970846-lsbpg08p65j87i4i0gvj66b1qnnlm155.apps.googleusercontent.com.json'

def _ensure_email_is_present():
    email = st.session_state.get("user_info").get("email")

    conn = st.connection(
        "gsheets",
        type=GSheetsConnection
    )

    df = conn.read()

    try:
        if df['6. E-mail institucional'] != email:
            raise ValueError
    
    except ValueError:
        st.error(f"Você não possui nenhuma entrada no sistema")

    return


#! WIP, not needed as google OAuth does it
def _ensure_login_is_trusted():
    email = st.session_state.get("user_info").get("email")

    conn = st.connection(
        "gsheets",
        type=GSheetsConnection
    )

    df = conn.read()

    try:
        if df['Email'] != email:
            raise ValueError
    
    except ValueError:
        st.error(f"Apenas e-mails institucionais são autorizados")

    return

def get_auth_config():

    if os.path.exists(LOCAL_SECRET_PATH):
        return LOCAL_SECRET_PATH, 'http://localhost:8501'
    
    if "web" in st.secrets:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            secret_dict = {"web": dict(st.secrets["web"])}
            json.dump(secret_dict, temp_file)
            
            redirect_uris = st.secrets["web"].get("redirect_uris", [])
            redirect_uri = redirect_uris[0] if redirect_uris else st.secrets["web"].get("redirect_uris_production", "")
            
            return temp_file.name, redirect_uri
            
    st.error("Credenciais de autenticação não encontradas (Local ou Secrets).")
    st.stop()
    return None, None

secret_path, redirect_uri_config = get_auth_config()

authenticator = Authenticate(
    secret_credentials_path=secret_path,
    cookie_name='cpcad_auth_cookie',
    cookie_key='digite_aqui_uma_frase_bem_longa_e_aleatoria_para_seguranca',
    redirect_uri=redirect_uri_config,
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

def require_auth():
    """
    Wrapper de compatibilidade para o sistema de senha simples.
    Interrompe a execução se não estiver logado.
    """
    if not check_password():
        st.stop()

def check_session():
    """
    Verifica sessão silenciosamente (compatibilidade).
    Apenas garante que o estado da senha esteja inicializado.
    """
    _ensure_session_state()

def show_user_sidebar():
    """
    Exibe informações do usuário na barra lateral se estiver logado.
    (Versão simplificada para autenticação por senha)
    """
    if st.session_state.get("password_correct"):
        with st.sidebar:
            st.write("**Usuário:** Administrador")
            st.caption("Acesso via Senha")
            
            if st.button("Sair", type="secondary"):
                logout()

def logout():
    authenticator.logout()
