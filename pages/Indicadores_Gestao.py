import streamlit as st
import pandas as pd
import altair as alt
from src.auth import check_password
from src.data import load_data, process_sla
import src.utils as utils

st.set_page_config(page_title="Indicadores de Gestão", layout="wide")

# 1. Verificação de Segurança (Gestores também precisam de senha? Assumindo que sim)
if not check_password():
    st.stop()

st.title("Indicadores de Gestão - CPCAD")
st.markdown("### Visão Estratégica e Estatísticas")

# 2. Carregamento de Dados
df = load_data()
if df.empty:
    st.warning("Sem dados para exibir.")
    st.stop()
    
df = process_sla(df)

# 3. Métricas Globais
total = len(df)
resolvidos = len(df[df['Fase Atual'] == 'Arquivado'])
taxa_resolucao = (resolvidos / total * 100) if total > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Denúncias", total)
col2.metric("Casos Arquivados/Resolvidos", resolvidos)
col3.metric("Taxa de Resolução", f"{taxa_resolucao:.1f}%")

st.divider()

# 4. Gráficos
c1, c2 = st.columns(2)

with c1:
    st.subheader("Distribuição por Tipo de Denúncia")
    # Tenta achar a coluna de tipo
    col_tipo = next((c for c in df.columns if 'tipo' in c.lower() or 'notícia' in c.lower()), df.columns[1])
    
    tipo_counts = df[col_tipo].value_counts().reset_index()
    tipo_counts.columns = ['Tipo', 'Quantidade']
    
    chart_tipo = alt.Chart(tipo_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Quantidade", type="quantitative"),
        color=alt.Color(field="Tipo", type="nominal"),
        tooltip=["Tipo", "Quantidade"]
    )
    st.altair_chart(chart_tipo, use_container_width=True)

with c2:
    st.subheader("Volume por Unidade Responsável")
    unidade_counts = df['Unidade Responsável'].value_counts().reset_index()
    unidade_counts.columns = ['Unidade', 'Quantidade']
    
    chart_unidade = alt.Chart(unidade_counts).mark_bar().encode(
        x=alt.X('Unidade', sort='-y'),
        y='Quantidade',
        color='Unidade',
        tooltip=['Unidade', 'Quantidade']
    )
    st.altair_chart(chart_unidade, use_container_width=True)

# 5. Evolução Temporal
st.subheader("Evolução Mensal de Denúncias")
# Agrupamento por mês
df['Mes_Ano'] = pd.to_datetime(df.iloc[:, 0]).dt.to_period('M').astype(str)
evolucao = df.groupby('Mes_Ano').size().reset_index(name='Quantidade')

chart_evolucao = alt.Chart(evolucao).mark_line(point=True).encode(
    x='Mes_Ano',
    y='Quantidade',
    tooltip=['Mes_Ano', 'Quantidade']
)
st.altair_chart(chart_evolucao, use_container_width=True)

st.markdown(utils.footer(), unsafe_allow_html=True)
