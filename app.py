import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import locale
import io

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

ARQUIVO_EXCEL = 'Controle de Insumos das Obras.xlsx'

# Nomes das colunas da sua planilha
COLUNAS = [
    'DATA', 'OBRA', 'CR RESPONSÁVEL', 'MATERIAL', 'N° TICKET', 'TAG', 
    'QUANTIDADE', 'CARRADAS', 'MOTORISTA', 'OBSERVAÇÃO', 
    'SERVIÇO', 'JAZIDA'
]

# Função para carregar ou criar o arquivo Excel
def carregar_dados():
    try:
        return pd.read_excel(ARQUIVO_EXCEL)
    except FileNotFoundError:
        df = pd.DataFrame(columns=COLUNAS)
        df.to_excel(ARQUIVO_EXCEL, index=False)
        return df

# Salva o dataframe no excel
def salvar_dados(df):
    df.to_excel(ARQUIVO_EXCEL, index=False)

st.image("Capa.jpg")
                 
def carregar_Crs():
    try:
        df_crs = pd.read_excel('listas_apoio.xlsx', sheet_name="CRs")
        return df_crs['Nome do CR'].tolist()
    except:
        st.warning("Arquivo 'listas_apoio.xlsx' não encontrado. Usando lista de CRs padrão.")

def carregar_Motorista():
    try:
        df_motorista = pd.read_excel('listas_apoio.xlsx', sheet_name="Motorista")
        return df_motorista['MOTORISTA'].tolist()
    except:
        st.warning("Arquivo 'listas_apoio.xlsx' não encontrado. Usando lista de CRs padrão.")

def validar_tag():
    if " " in tag:
        return False
    if len (tag) < 4:
        return False
    primeira_parte = tag[:2]
    if not primeira_parte.isalpha():
        return False
    return True

def formatar_numero_br(numero):
    #"""Formata um número para o padrão brasileiro (ex: 1.234,56)."""
    try:
        # Usa a formatação do locale
        return locale.format_string('%.2f', numero, grouping=True)
    except (ValueError, TypeError):
        # Se o número for inválido, retorna o próprio valor ou um padrão
        return numero

# Configuração da página
st.set_page_config(page_title="Controle de Obras", layout="wide")

st.title("Controle de Obra"
" - Logistica")

# Carrega os dados
df = carregar_dados()

if not df.empty:
    # Coloca todos os filtros dentro de um expander na sidebar para um visual "clean"
    with st.sidebar.expander("🔍 Abrir o Período"):
        
        st.subheader("Filtro por Período")
        
        # Define os valores padrão para os calendários
        data_minima = df['DATA'].min().date()
        data_maxima = df['DATA'].max().date()
        
        # CORREÇÃO: Parâmetros completos e sem 'sidebar.' pois já está no contexto
        data_inicio = st.date_input(
            "Data de Início", 
            value=data_minima, 
            min_value=data_minima, 
            max_value=data_maxima,
            format="DD/MM/YYYY"
        )
        data_fim = st.date_input(
            "Data de Fim", 
            value=data_maxima, 
            min_value=data_minima, 
            max_value=data_maxima,
            format="DD/MM/YYYY"
        )

lista_crs_unicos = df['CR RESPONSÁVEL'].unique().tolist()
opcoes_filtro_cr = ["Todos"] + lista_crs_unicos


CR_FILTRO = st.sidebar.multiselect(
    "Selecione um ou mais CRs", 
    options=opcoes_filtro_cr, 
    default="Todos"
)

if "Todos" in CR_FILTRO or not CR_FILTRO:
    # Se "Todos" estiver selecionado (ou se nada estiver), 
    # nossa lista para filtrar será a lista COMPLETA de todos os CRs.
    lista_final_para_filtrar = lista_crs_unicos
else:
    # Caso contrário, usamos apenas os CRs que o usuário selecionou.
    lista_final_para_filtrar = CR_FILTRO

df_filtrado = df[
    (df['CR RESPONSÁVEL'].isin(lista_final_para_filtrar)) &
    (df['DATA'].dt.date >= data_inicio) &
    (df['DATA'].dt.date <= data_fim)
    # Adicione outros filtros aqui com '&' se precisar
]

#BAIXAR A BASE FILTRADA POR CR 
st.sidebar.header("Exportar Dados")
buffer = io.BytesIO()
df_filtrado.to_excel(buffer, index=False)
st.sidebar.download_button(
    label="⬇️ Baixar Dados Filtrados",
    data=buffer.getvalue(),
    file_name="relatorio_filtrado.xlsx",
    mime="application/vnd.ms-excel" #CHAVE UNICA
)

#BAIXAR A BASECOMPLETA
buffer_completo = io.BytesIO()
df.to_excel(buffer_completo, index=False) 
st.sidebar.download_button(
    label="⬇️ Baixar Base Completa",
    data=buffer_completo.getvalue(),
    file_name="relatorio_completo.xlsx",
    mime="application/vnd.ms-excel",
    key='download_completo' #CHAVE UNICA
)

# --- Abas de navegação ---

tab1, tab2 = st.tabs(["Lançamentos", "Painel de Monitoramento"])

with tab1:
    st.header("Cadastrar Novo Lançamento")
    with st.form("lancamento_form"):
        # Organiza o formulário em colunas
        col1, col2, col3 = st.columns(3)
        with col1:
            obra = st.text_input("OBRA")
            Lista_de_Material = ["AREIA","PIÇARRA","BARRO"]
            material = st.selectbox("MATERIAL*", options=Lista_de_Material)
            tipo_documento = st.radio(
                "Tipo de Documento*",
                ["Ticket", "Nota Fiscal"],
                horizontal=True # Deixa as opções lado a lado
            )
            numero_documento = st.text_input("Número do Documento*")
            quantidade = st.number_input("QUANTIDADE*", step=1) 
        with col2:
            lista_de_crs = carregar_Crs()
            cr_responsavel = st.selectbox("CR RESPONSÁVEL*", options=lista_de_crs)

        with col2:
            lista_de_motoristas = carregar_Motorista()
            motorista = st.selectbox("MOTORISTA",options=lista_de_motoristas)
            carradas = st.number_input("CARRADAS*", min_value=1, step=1)
        with col3:
            tag = st.text_input("TAG*", help="Deve começar com 2 letras e não pode ter espaços.").strip()
            servico = st.text_input("SERVIÇO")
            jazida = st.text_input("JAZIDA*")
        
        observacao = st.text_area("OBSERVAÇÃO")
        
        submitted = st.form_submit_button("Salvar Lançamento")
    
        if submitted:
            n_ticket_final = f"{tipo_documento}: {numero_documento}"
            campos_obrigatorios = [
                 obra, material, numero_documento, tag, servico, jazida,quantidade,carradas]
            if any(campo == "" for campo in campos_obrigatorios):
                st.error("ERRO: Por favor, preencha todos os campos marcados com * antes de salvar.")

            else:
                nova_entrada = {
                    'DATA': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    'OBRA': obra, 'CR RESPONSÁVEL': cr_responsavel, 'MATERIAL': material,
                    'N° TICKET': n_ticket_final,'QUANTIDADE': quantidade,
                    'CARRADAS': carradas, 'MOTORISTA': motorista,
                    'OBSERVAÇÃO': observacao, 'SERVIÇO': servico, 'JAZIDA': jazida
                }
                df = pd.concat([df, pd.DataFrame([nova_entrada])], ignore_index=True)
                salvar_dados(df)
                st.success("Lançamento salvo com sucesso!")

    st.header("Últimos Lançamentos")
    st.dataframe(df.tail(50)) # Mostra os últimos 20 registros

# Segunda aba - graficos 
with tab2:
    st.header("Análise Gráfrica")

    if not df.empty:
        # --- INÍCIO DA SEÇÃO DE CARTÕES (KPIs) ---
        total_carradas = df_filtrado['CARRADAS'].sum()
        total_quantidade = df_filtrado['QUANTIDADE'].sum()
        num_registros = len(df_filtrado) # Conta o número de linhas na tabela filtrada

        #colunas dos cartões
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Total de Carradas", 
                value=total_carradas
            )
        
        with col2:
            st.metric(
                label="Toneladas Total",
                value=formatar_numero_br(total_quantidade)
            )

        with col3:
            st.metric(
                label="Nº de Registros",
                value=num_registros
            )

        st.divider() # Adiciona uma linha divisória

    if not df.empty:
        st.subheader("Carradas por CR")
        carradas_por_CR = df_filtrado.groupby('CR RESPONSÁVEL')['CARRADAS'].sum().reset_index()

        fig1 = px.bar(
        carradas_por_CR,
        x='CR RESPONSÁVEL',             
        y='CARRADAS',                 
        title='Total de Carradas por CR',
        labels={'CR': 'CR', 'Carradas': 'Total de Carradas'},
        color_discrete_sequence=["#000066"],
        text_auto=True )
        
        fig1.update_traces(
        textposition='auto',  #(pode ser 'inside' ou 'outside')
        textfont_size=14,        # Tamanho da fonte
        textfont_color='#FFD000',  # Cor da fonte
        textangle=0              # (0 = reto)
        )
        st.plotly_chart(fig1)
    else:
        st.write("Ainda não há dados para exibir.")


    col1,col2 = st.columns(2)

    with col1:
        if not df.empty:
            st.subheader("Carradas por Material")
            carradas_por_Material = df_filtrado.groupby('MATERIAL')['CARRADAS'].sum().reset_index()
            
            fig2 = px.pie(
                carradas_por_Material,
                names = "MATERIAL",
                values= "CARRADAS",
                title= 'Distribuição de Carradas por Material',
                 color_discrete_sequence=["#000066",'#FFD000',"#8C8CFF"]
            )
            st.plotly_chart(fig2)
        else:
            st.write("Ainda não há dados para exibir.")
    
    with col2:
        if not df.empty:
            st.subheader("TOP 10 - Carradas por Motorista")
            carradas_por_Motorista = df_filtrado.groupby('MOTORISTA')['CARRADAS'].sum().reset_index()
            top_10_motoristas = carradas_por_Motorista.sort_values(by="CARRADAS", ascending=False).head(10)
            top_10_motoristas_ordenado = top_10_motoristas.sort_values(by="CARRADAS", ascending=True)
        
            fig3= px.bar(
                top_10_motoristas_ordenado,
                x = "CARRADAS",
                y = 'MOTORISTA',
                title='Total de Carradas por Motorista',
                labels={'Motorista': 'Motorista', 'Carradas': 'Total de Carradas'},
                color_discrete_sequence=["#000066"],
                text_auto=True )
        
            fig3.update_traces(
                textposition='auto',  #(pode ser 'inside' ou 'outside')
                textfont_size=14,        # Tamanho da fonte
                textfont_color='#FFD000',  # Cor da fonte
                textangle=0              # (0 = reto)
            )
            st.plotly_chart(fig3)
        else:
         st.write("Ainda não há dados para exibir.")
