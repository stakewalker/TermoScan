from dash import dcc, html
import plotly.express as px
import json
import pandas as pd
import dash_bootstrap_components as dbc

def carregar_salas():
    try:
        with open('assets/salas_antigo.json', 'rb') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

salas = carregar_salas()
df = pd.read_csv('assets/temperaturas.csv')

# Lista para armazenar os gráficos
graficos = []

# Cria os gráficos baseados na qtde de salas e add na lista
for i in range(len(salas)):
    dados_sala = df[df['id_sala'] == i+1]
    fig = px.line(dados_sala, x='horario', y='temperatura')
    fig.update_layout(
            title=dict(  # Centraliza os títulos
                text=salas[str(i+1)],
                x=0.5),
            xaxis_title='',
            yaxis_title='')
    # Opções para remover features e deixar apenas o gráfico
    graficos.append(dcc.Graph(
        figure=fig, id=f'graph-{i+1}',
        config={
            'displayModeBar': False,
            'autosizable': True
        }))

# Organizar os gráficos em colunas
colunas = 3
graph_rows = [dbc.Row([dbc.Col(graph, width=0, style={'padding': '0px'}) for graph in graficos[i:i + colunas]]) for i in range(0, len(graficos), colunas)]

# Criar o layout final
layout = html.Div(graph_rows, style={"overflowY": "scroll", "height": "100vh"})