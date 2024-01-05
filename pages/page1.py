from dash import html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from datetime import datetime, date
import json

df = pd.read_csv('assets/temperaturas.csv')

def carregar_salas():
    try:
        with open('assets/salas_antigo.json', 'rb') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
salas = carregar_salas()

# 'horario' é armazenado como timestamp e convertido para objeto datetime
df['horario'] = pd.to_datetime(df['horario'], unit='s')

layout = html.Div([
    html.H1(children='Temperatura das Salas'),
    dcc.Dropdown(  # Menu das salas
        id='menu_salas',
        options=[{'label': salas[str(id_sala)], 'value': id_sala} for id_sala in df['id_sala'].unique()],
    ),
    dcc.DatePickerSingle(  # Componente do calendário
        id='selecionar_data',
        with_full_screen_portal=True,
        clearable=True,
        display_format="DD/MM/YYYY",
    ),
    dcc.Graph(
        id='conteudo_grafico',
        config={
            'displaylogo': False,
            'responsive': True
        }
    )
    ],
    style={"margin":20,"align":"center"})

@callback(
    [Output('conteudo_grafico', 'figure'),
     Output('selecionar_data', 'date')],
    [Input('menu_salas', 'value'),
     Input('selecionar_data', 'date')],
    suppress_callback_exceptions=True
)
def update_graph(value, data_selecionada):  
    # Extraíndo dados da sala selecionada
    dff = df[df['id_sala'] == value]
    
    # Atualizar o gráfico baseado na data selecionada
    if data_selecionada is not None:
        # Extrai apenas o conteúdo do dia
        dia_selecionado = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
        # Filtrar e plotar o DataFrame incluindo apenas dados do dia escolhido
        filtered_df = dff[dff['horario'].dt.date == dia_selecionado]
        fig = px.line(filtered_df, x='horario', y='temperatura')
        fig.update_layout(
            xaxis_title='Data e Hora',
            yaxis_title='Temperatura (ºC)')
        return fig, data_selecionada
    else: 
        # Se nenhuma data for escolhida, plotar todo o Dataframe
        fig = px.line(dff, x='horario', y='temperatura')
        fig.update_layout(
            xaxis_title='Data e Hora',
            yaxis_title='Temperatura (ºC)')
        return fig, None
