import streamlit as st
import src.auth as auth
from src.data import load_data

st.set_page_config(page_title="Acompanhamento de denúncias", layout="wide")

auth.require_auth()
# auth._ensure_email_is_present()

st.title("Acompanhamento de denúncias")

df = load_data()

if not df.empty:
    from src.data import process_sla, process_user
    df = process_sla(df)
    
    user_email = st.session_state.get('user_info', {}).get('email')
    
    if user_email:
        dados_usuario = process_user(df, user_email)
        
        if not dados_usuario:
            st.info("Não foram encontradas denúncias registradas para o seu e-mail.")
        else:
            for item in dados_usuario:
                with st.container(border=True):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader(f"Processo SEI : {item['id_processo']}")
                        st.write(f"**Fase Atual:** {item['fase_atual']}")
                        st.write(f"**Unidade Responsável:** {item['unidade_responsavel']}")
                        st.caption(f"Última movimentação: {item['data_movimentacao']}")
                    
                    with col2:
                        st.write("**Próximas Etapas:**")
                        if item['proximas_fases']:
                            for fase in item['proximas_fases']:
                                st.text(f"• {fase}")
                        else:
                            st.success("Processo Concluído ou Fase Final")
    else:
        st.error("Erro ao identificar usuário logado.")
else:
    st.warning("O sistema de dados está temporariamente indisponível.")

