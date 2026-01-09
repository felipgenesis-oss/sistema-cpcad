import streamlit as st
import assets.icons as icons
import src.utils as utils

TJRO_IMAGE = "https://www.tjro.jus.br/templates/portal_tjro_helix_j5/images/presets/default/logo.png"


st.set_page_config(
    page_title="Portal CPCAD", 
    layout="centered", 
    page_icon="⚖️", 
    initial_sidebar_state="auto"
)

st.image(TJRO_IMAGE, width=215)
st.title("Sistema de Gestão - CPCAD")
st.info("Bem-vindo ao sistema de monitoramento da Comissão de Enfrentamento ao Assédio.")

Atendimento, Operacional, Gestao = st.columns(3, gap="medium", vertical_alignment="top")

with Atendimento:
    with st.container(border=True, gap='medium'):
        st.markdown(
            utils.render_svg_icon(icons.ATENDIMENTO_DOC), 
            unsafe_allow_html=True
        )
        st.subheader("Atendimento", text_alignment="center")
        st.caption("Registro de denúncias e links públicos.")
        if st.button("Acessar Registro", width="stretch", type="primary"):
            st.switch_page("pages/Registrar_Denuncia.py")

with Operacional:
    with st.container(border=True, gap='medium'):
        st.markdown(
            utils.render_svg_icon(icons.OPERACIONAL_GEAR), 
            unsafe_allow_html=True
        )
        st.subheader("Operacional", text_alignment="center" )
        st.caption("Triagem, prazos e fluxo da comissão.")
        if st.button("Painel Interno", width="stretch", type="primary"):
            st.switch_page("pages/Operacional_CPCAD.py")

with Gestao:
    with st.container(border=True, gap='medium'):
        st.markdown(
            utils.render_svg_icon(icons.GESTAO_CHART), 
            unsafe_allow_html=True
        )
        st.subheader("Gestão", text_alignment="center")
        st.caption("Indicadores e relatórios gerenciais.")
        if st.button("Ver Dashboard", width="stretch", type="primary"):
            st.switch_page("pages/Indicadores_Gestao.py")

st.markdown(
    utils.footer(), 
    unsafe_allow_html=True
)
