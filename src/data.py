import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

@st.cache_data(ttl=60)
def load_data():
    """
    Carrega os dados da planilha Google Sheets.
    Usa cache de 60 segundos para evitar requisições excessivas.
    """
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    try:
        # ttl=0 no read força a busca se o cache do st.cache_data expirar
        df = conn.read(ttl=0)
    except Exception as e:
        st.error(f"Erro ao conectar com o Google Sheets: {e}")
        return pd.DataFrame()

    df = df.dropna(how='all')
    
    # Normalização básica de colunas
    if not df.empty:
        # Tenta identificar colunas dinamicamente ou usa defaults
        col_data = df.columns[0] 
        # Garante que datas sejam datetime
        df[col_data] = pd.to_datetime(df[col_data], errors='coerce')
        
        # Garante existência de colunas críticas
        if 'ID Processo SEI' not in df.columns:
            df['ID Processo SEI'] = 'PENDENTE'
        if 'Fase Atual' not in df.columns:
            df['Fase Atual'] = 'Triagem Inicial'
        if 'Data Ultima Movimentacao' not in df.columns:
            df['Data Ultima Movimentacao'] = df[col_data]
            
        df['Data Ultima Movimentacao'] = pd.to_datetime(df['Data Ultima Movimentacao'], errors='coerce')
        
    return df

def process_sla(df):
    """
    Processa as regras de negócio de SLA (Prazos).
    """
    if df.empty:
        return df

    agora = datetime.now()
    col_cargo = next((c for c in df.columns if 'cargo' in c.lower()), df.columns[-1])
    
    def definir_responsavel(cargo):
        cargo = str(cargo).lower()
        if 'juiz' in cargo or 'magistrado' in cargo:
            return 'Corregedoria (1º Grau)'
        elif 'desembargador' in cargo:
            return 'Presidência (2º Grau)'
        else:
            return 'CPCAD (Comissão)'

    df['Unidade Responsável'] = df[col_cargo].apply(definir_responsavel)

    # Lógica de Dias Parado
    def calcular_dias_parado(row):
        if pd.isnull(row['Data Ultima Movimentacao']):
            return 0
        return (agora - row['Data Ultima Movimentacao']).days

    df['Dias Sem Movimentação'] = df.apply(calcular_dias_parado, axis=1)

    # Lógica de Status
    def calcular_status(row):
        dias_parado = row['Dias Sem Movimentação']
        if dias_parado >= 2: return '🔴 ATRASADO (> 2 dias)'
        elif dias_parado >= 1: return '🟡 ATENÇÃO'
        else: return '🟢 NO PRAZO'

    df['Status Prazos'] = df.apply(calcular_status, axis=1)
    
    return df
