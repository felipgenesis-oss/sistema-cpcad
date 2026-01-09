import streamlit as st
import assets.icons as icons

TJRO_BLUE = "#0c326f"
TJRO_IMAGE = "https://www.tjro.jus.br/templates/portal_tjro_helix_j5/images/presets/default/logo.png"

def render_svg_icon(svg_path):
    return f"""
    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="{TJRO_BLUE}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            {svg_path}
        </svg>
    </div>
    """

st.set_page_config(
    page_title="Portal CPCAD", 
    layout="centered", 
    page_icon="⚖️", 
    initial_sidebar_state="auto"
)

st.html("""
    <style>
        div[data-testid="stButton"] button {
            width: 100% !important;
        }
    </style>
""")

st.image(TJRO_IMAGE, width=215)
st.title("Sistema de Gestão - CPCAD")
st.info("Bem-vindo ao sistema de monitoramento da Comissão de Enfrentamento ao Assédio.")

Atendimento, Operacional, Gestao = st.columns(3, gap="medium", vertical_alignment="top")

with Atendimento:
    with st.container(border=True, gap='medium'):
        st.markdown(render_svg_icon(icons.ATENDIMENTO_DOC), unsafe_allow_html=True)
        st.subheader("Atendimento", text_alignment="center")
        st.caption("Registro de denúncias e links públicos.")
        if st.button("Acessar Registro", width="stretch", type="primary"):
            st.switch_page("pages/Registrar_Denuncia.py")

with Operacional:
    with st.container(border=True, gap='medium'):
        st.markdown(render_svg_icon(icons.OPERACIONAL_GEAR), unsafe_allow_html=True)
        st.subheader("Operacional", text_alignment="center" )
        st.caption("Triagem, prazos e fluxo da comissão.")
        if st.button("Painel Interno", width="stretch", type="primary"):
            st.switch_page("pages/Operacional_CPCAD.py")

with Gestao:
    with st.container(border=True, gap='medium'):
        st.markdown(render_svg_icon(icons.GESTAO_CHART), unsafe_allow_html=True)
        st.subheader("Gestão", text_alignment="center")
        st.caption("Indicadores e relatórios gerenciais.")
        if st.button("Ver Dashboard", width="stretch", type="primary"):
            st.switch_page("pages/Indicadores_Gestao.py")

st.markdown("---")
st.markdown(
    """
    <div style="position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; color: #666; font-size: 12px; padding: 10px; border-top: 1px solid #eee; z-index: 1000;">
       Desenvolvido pelo <strong>Laboratório de Inovação Gênesis</strong> - TJRO <br>© 2025 ViaJus. Todos os direitos reservados. 
    </div>
    """, 
    unsafe_allow_html=True
)
