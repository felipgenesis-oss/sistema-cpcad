import streamlit as st

pages = [
    st.Page("src/home.py", title="Início", default=True),
    st.Page("pages/registrar-denuncia.py", title="Registrar Denúncia", url_path="registrar-denuncia"),
    st.Page("pages/operacional-cpcad.py", title="Operacional CPCAD", url_path="operacional-cpcad"),
    st.Page("pages/indicadores-gestao.py", title="Indicadores de Gestão", url_path="indicadores-gestao"),
]

pg = st.navigation(pages)
pg.run()