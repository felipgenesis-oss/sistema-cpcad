import streamlit as st
import src.utils as utils

def _ensure_session_state():
    """Garante que as variáveis de estado essenciais existam na sessão atual."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

def check_password():
    """
    Verifica se o usuário inseriu a senha correta para acessar áreas restritas.
    Retorna True se autenticado, False caso contrário.
    Renderiza a tela de login se não estiver logado.
    """
    _ensure_session_state()

    if st.session_state["password_correct"]:
        return True

    st.image(utils.TJRO_IMAGE, width=200)
    st.title("Sistema de Gestão CPCAD")
    st.markdown("### 🔒 Acesso Restrito")
    
    password = st.text_input("Digite a senha de acesso:", type="password")
    
    if st.button("Entrar"):
        # Em produção, use st.secrets para a senha se possível, aqui hardcoded conforme original
        if password == "tjro123":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
            
    return False

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
    """Limpa a sessão de autenticação."""
    st.session_state["password_correct"] = False
    st.rerun()