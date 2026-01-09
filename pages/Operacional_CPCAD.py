import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.auth import check_password
from src.data import load_data, process_sla
import src.utils as utils

st.set_page_config(page_title="Operacional CPCAD", layout="wide")

if not check_password():
    st.stop()

st.title("Painel Operacional - CPCAD")
st.markdown("### Monitoramento de Prazos e Fluxo Processual")

df = load_data()

if df.empty:
    st.warning("Não foi possível carregar os dados ou a planilha está vazia.")
    st.stop()

df = process_sla(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Processos", len(df))
col2.metric("Críticos (> 2 dias)", len(df[df['Status Prazos'].str.contains('ATRASADO', na=False)]))
col3.metric("Novos (24h)", len(df[pd.to_datetime(df.iloc[:, 0]) > (datetime.now() - timedelta(days=1))]))
col4.metric("Em Triagem", len(df[df['Fase Atual'] == 'Triagem Inicial']))

st.divider()

# 5. Tabela de Monitoramento (Prioridade para Atrasados)
st.subheader("Fila de Prioridade (Prazos)")

# Filtros laterais
st.sidebar.header("Filtros Operacionais")
fase_filter = st.sidebar.multiselect("Filtrar por Fase", options=df['Fase Atual'].unique(), default=df['Fase Atual'].unique())
status_filter = st.sidebar.multiselect("Filtrar por Status", options=df['Status Prazos'].unique(), default=df['Status Prazos'].unique())

df_filtered = df[df['Fase Atual'].isin(fase_filter) & df['Status Prazos'].isin(status_filter)]

# Seleção de colunas para exibição
cols_to_show = ['ID Processo SEI', 'Data Ultima Movimentacao', 'Unidade Responsável', 'Fase Atual', 'Status Prazos']
# Adiciona colunas extras se existirem
cols_existentes = [c for c in cols_to_show if c in df_filtered.columns]

# Estilização Condicional
def color_status(val):
    if 'ATRASADO' in str(val): return 'background-color: #ffcccc; color: #990000; font-weight: bold' # Vermelho claro
    if 'ATENÇÃO' in str(val): return 'background-color: #fff4cc; color: #996600' # Amarelo claro
    return 'background-color: #ccffcc; color: #006600' # Verde claro

st.dataframe(
    df_filtered[cols_existentes].style.applymap(color_status, subset=['Status Prazos']),
    use_container_width=True,
    hide_index=True
)

# 6. Área de Ação (Simulação de Atualização)
with st.expander("🔧 Atualizar Status do Processo"):
    st.info("Selecione um processo para atualizar sua fase ou inserir o número SEI.")
    
    processo_selecionado = st.selectbox("Selecione o Processo (pela data/hora)", df_filtered.iloc[:, 0].astype(str))
    
    c1, c2 = st.columns(2)
    with c1:
        novo_sei = st.text_input("Novo ID SEI", placeholder="Ex: 0001234-56.2024.8.22.0000")
    with c2:
        nova_fase = st.selectbox("Nova Fase", ["Triagem Inicial", "Acolhimento Psicológico", "Junta de Apuração", "Presidência", "Arquivado"])
    
    if st.button("Salvar Alterações"):
        st.success(f"Alteração registrada! Fase: {nova_fase} | SEI: {novo_sei}")
        st.caption("Nota: A persistência real na planilha requer configuração de Service Account (Google Cloud).")

st.markdown(utils.footer(), unsafe_allow_html=True)
