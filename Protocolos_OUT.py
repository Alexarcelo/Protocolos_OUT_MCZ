import pandas as pd
import mysql.connector
import decimal
import streamlit as st

def bd_phoenix(vw_name):
    # Parametros de Login AWS
    config = {
    'user': 'user_automation_jpa',
    'password': 'luck_jpa_2024',
    'host': 'comeia.cixat7j68g0n.us-east-1.rds.amazonaws.com',
    'database': 'test_phoenix_maceio'
    }
    # Conexão as Views
    conexao = mysql.connector.connect(**config)
    cursor = conexao.cursor()

    request_name = f'SELECT * FROM {vw_name}'

    # Script MySql para requests
    cursor.execute(
        request_name
    )
    # Coloca o request em uma variavel
    resultado = cursor.fetchall()
    # Busca apenas o cabecalhos do Banco
    cabecalho = [desc[0] for desc in cursor.description]

    # Fecha a conexão
    cursor.close()
    conexao.close()

    # Coloca em um dataframe e muda o tipo de decimal para float
    df = pd.DataFrame(resultado, columns=cabecalho)
    df = df.applymap(lambda x: float(x) if isinstance(x, decimal.Decimal) else x)
    return df

def definir_html(df_ref):

    valores = df_ref.values

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                text-align: center;  /* Centraliza o texto */
            }
            table {
                margin: 0 auto;  /* Centraliza a tabela */
                border-collapse: collapse;  /* Remove espaço entre as bordas da tabela */
            }
            th, td {
                padding: 8px;  /* Adiciona espaço ao redor do texto nas células */
                border: 1px solid black;  /* Adiciona bordas às células */
                text-align: center;
            }
        </style>
    </head>
    <body>
        <table>
    """

    for linha in valores:
        html += "<tr>"
        for valor in linha:
            html += f"<td>{valor}</td>"
        html += "</tr>"

    html += """
        </table>
    </body>
    </html>
    """
    
    return html

def criar_output_html(nome_html, html, hotel):

    with open(nome_html, "w", encoding="utf-8") as file:

        file.write(f'<p style="font-size:20px;">PROTOCOLO AVISA DE SAÍDA: ____/____/________</p>\n')

        file.write(f'<p style="font-size:20px;">ENTREGUE POR: _______________________________________</p>\n\n')

        file.write(f'<p style="font-size:20px;">Hotel: {hotel}</p>\n\n')
        
        file.write(html)

        file.write(f'\n\n<p style="font-size:20px;">RECEBIDO EM: ____/____/________</p>\n\n')

        file.write(f'<p style="font-size:20px;">______________________________________________________</p>\n')

        file.write(f'<p style="font-size:15px;">ASSINATURA</p>')

def inserir_roteiros_html(nome_html, html, hotel):

    with open(nome_html, "a", encoding="utf-8") as file:
        
        # Adiciona estilo para evitar quebras de página dentro do conteúdo
        file.write("""
        <style>
        @media print {
            .no-break {
                page-break-inside: avoid; /* Evita quebra de página dentro do elemento */
                break-inside: avoid; /* Compatível com navegadores mais modernos */
            }
        }
        </style>
        """)

        # Envolve o conteúdo em uma div com a classe "no-break"
        file.write(f'<div class="no-break">')

        file.write(f'<br><br><br><br><br><br>')

        file.write(f'<p style="font-size:20px;">Hotel: {hotel}</p>\n\n')
        
        file.write(html)

        file.write(f'\n\n<p style="font-size:20px;">RECEBIDO EM: ____/____/________</p>\n\n')

        file.write(f'<p style="font-size:20px;">______________________________________________________</p>\n')

        file.write(f'<p style="font-size:15px;">ASSINATURA</p>\n\n\n')

        file.write(f'</div>')  # Fecha a div

def inserir_roteiros_html_nova_pagina(nome_html, html, hotel):

    with open(nome_html, "a", encoding="utf-8") as file:
        
        # Estilo para quebra de página ao imprimir
        file.write("""
        <style>
        @media print {
            .page-break {
                page-break-before: always; /* Compatibilidade com navegadores antigos */
                break-before: page; /* Compatibilidade com navegadores mais recentes */
            }
        }
        </style>
        """)

        # Adiciona uma quebra de página antes do conteúdo
        file.write(f'<div class="page-break"></div>')

        file.write(f'<p style="font-size:20px;">PROTOCOLO AVISA DE SAÍDA: ____/____/________</p>\n')

        file.write(f'<p style="font-size:20px;">ENTREGUE POR: _______________________________________</p>\n\n')

        file.write(f'<p style="font-size:20px;">Hotel: {hotel}</p>\n\n')
        
        file.write(html)

        file.write(f'\n\n<p style="font-size:20px;">RECEBIDO EM: ____/____/________</p>\n\n')

        file.write(f'<p style="font-size:20px;">______________________________________________________</p>\n')

        file.write(f'<p style="font-size:15px;">ASSINATURA</p>\n\n\n')

st.set_page_config(layout='wide')

if 'mapa_router' not in st.session_state:

    with st.spinner('Carregando Dados do Phoenix...'):

        st.session_state.mapa_router = bd_phoenix('vw_out_protocolos')

        st.session_state.df_escalas = bd_phoenix('vw_escalas_protocolos')

st.title('Protocolo de Saídas - Maceió')

st.divider()

row0 = st.columns(2)

with row0[0]:

    data_protocolos = st.date_input(
        'Data Protocolos', 
        value=None,
        format='DD/MM/YYYY', 
        key='data_protocolos'
    )

with row0[1]:

    container_dados = st.container()

    atualizar_dados = container_dados.button(
        'Carregar Dados do Phoenix', 
        use_container_width=True
    )

if atualizar_dados:

    with st.spinner('Carregando Dados do Phoenix...'):

        st.session_state.mapa_router = bd_phoenix('vw_out_protocolos')

        st.session_state.df_escalas = bd_phoenix('vw_escalas_protocolos')

if data_protocolos:

    df_out = st.session_state.mapa_router[(st.session_state.mapa_router['Data Execucao']==data_protocolos)].sort_values(by='Est Origem').reset_index(drop=True)
    
    df_escalas = st.session_state.df_escalas[(st.session_state.df_escalas['Data Execucao']==data_protocolos)][['Reserva', 'Escala']].drop_duplicates().reset_index(drop=True)

    df_out = pd.merge(df_out, df_escalas, on='Reserva', how='left')

    df_out = df_out[pd.isna(df_out['Escala'])].reset_index(drop=True)

    with row0[0]:

        servico = st.selectbox('Serviço', sorted(df_out['Servico'].unique().tolist()), index=None)

    if servico=='OUT - ORLA DE MACEIÓ (OU PRÓXIMOS) ':

        df_out_servico = df_out[df_out['Servico']==servico].reset_index(drop=True)

        with row0[0]:

            hotel = st.selectbox('Hotel', df_out_servico['Est Origem'].unique().tolist(), index=None)

        if hotel is not None:

            df_out_servico = df_out_servico[df_out_servico['Est Origem']==hotel].reset_index(drop=True)

        contador=0

        nome_html = f"Protocolos {str(data_protocolos.strftime('%d-%m-%Y'))}.html"

        df_out_servico['Data Horario Apresentacao'] = df_out_servico['Data Horario Apresentacao'].apply(
            lambda x: x.strftime('%d/%m/%Y %H:%M:%S') if pd.notnull(x) and isinstance(x, pd.Timestamp) else x
        )

        for hotel in df_out_servico['Est Origem'].unique().tolist():

            df_ref = df_out_servico[df_out_servico['Est Origem']==hotel].reset_index(drop=True)

            html = definir_html(df_ref[['Reserva', 'Parceiro', 'Cliente', 'Voo', 'Data Horario Apresentacao']])

            if contador==0:

                criar_output_html(nome_html, html, hotel)

            else:

                inserir_roteiros_html(nome_html, html, hotel)

            contador+=1

        with open(nome_html, "r", encoding="utf-8") as file:

            html_content = file.read()

        st.download_button(
            label="Baixar Arquivo HTML",
            data=html_content,
            file_name=nome_html,
            mime="text/html"
        )

    elif servico:

        df_out_servico = df_out[df_out['Servico']==servico].reset_index(drop=True)

        with row0[0]:

            hotel = st.selectbox('Hotel', df_out_servico['Est Origem'].unique().tolist(), index=None)

        if hotel is not None:

            df_out_servico = df_out_servico[df_out_servico['Est Origem']==hotel].reset_index(drop=True)

        contador=0

        nome_html = f"Protocolos {str(data_protocolos.strftime('%d-%m-%Y'))}.html"

        df_out_servico['Data Horario Apresentacao'] = df_out_servico['Data Horario Apresentacao'].apply(
            lambda x: x.strftime('%d/%m/%Y %H:%M:%S') if pd.notnull(x) and isinstance(x, pd.Timestamp) else x
        )

        for hotel in df_out_servico['Est Origem'].unique().tolist():

            df_ref = df_out_servico[df_out_servico['Est Origem']==hotel].reset_index(drop=True)

            html = definir_html(df_ref[['Reserva', 'Parceiro', 'Cliente', 'Voo', 'Data Horario Apresentacao']])

            if contador==0:

                criar_output_html(nome_html, html, hotel)

            else:

                inserir_roteiros_html_nova_pagina(nome_html, html, hotel)

            contador+=1

        with open(nome_html, "r", encoding="utf-8") as file:

            html_content = file.read()

        st.download_button(
            label="Baixar Arquivo HTML",
            data=html_content,
            file_name=nome_html,
            mime="text/html"
        )
