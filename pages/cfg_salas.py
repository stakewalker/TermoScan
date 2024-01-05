from dash import html, dcc, Input, Output, State, Dash, callback
import dash_bootstrap_components as dbc
import json
import pandas as pd


def carregar_salas():
    try:
        with open('assets/salas.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def salvar_salas(salas):
    with open('assets/salas.json', 'w') as file:
        json.dump(salas, file)

salas = carregar_salas()

# Gerar layout com dropdowns e campos de edição
layout = dbc.Container([
    html.H3("Configurações das Salas", className="header"),

    # Dropdowns e campos de edição para cada sala
    dbc.Row([
        dbc.Col([
        dcc.Dropdown(
            id='dropdown-salas',
            options=[{'label': sala['nome'], 'value': sala['nome']} for sala in salas.values()],
            placeholder="Selecione uma sala",
        ),
        html.Br()
            #html.Div(id='output-message', className='mt-3'),
        ], width=4 ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Label("Nome da Sala:"),
                    dcc.Input(id='input-nome-sala', type='text', size="40"),
                    html.Label("Modelo do CLP:"),
                    dcc.Input(id='input-modelo-clp', type='text', size="40"),
                    html.Label("Versão do Firmware do CLP:"),
                    dcc.Input(id='input-versao-firmware-clp', type='text', size="40"),
                    html.Label("Status do CLP:"),
                    dcc.Input(id='input-status-clp', type='text', size="40"),
                    html.Label("IP do CLP:"),
                    dcc.Input(id='input-ip-clp', type='text', size="40"),
                    html.Label("Seleção de Sensores:"),
                    dcc.Dropdown(id='dropdown-sensores', options=[], multi=True),
                    html.Br(),
                    dbc.Button("Salvar Alterações", id='save-button', style={'margin-right': '50px'}),
                    dbc.Button("Adicionar", color="success", id='add-button'),
                    dbc.Button("Remover", color="danger", id='remove-button'),
                    html.Div(id='output-message', className='mt-3')
                ])
            ),
            width=6
        )
    ], className="mb-3"),

    # Exibir Mensagens
    html.Div(id='output-message', className='mt-3')],
    className="mt-5"
)

# Callback para atualizar campos de edição quando sala é selecionada
@callback(
    [Output('input-nome-sala', 'value'),
     Output('input-modelo-clp', 'value'),
     Output('input-versao-firmware-clp', 'value'),
     Output('input-status-clp', 'value'),
     Output('input-ip-clp', 'value'),
     Output('dropdown-sensores', 'options')],
    [Input('dropdown-salas', 'value')],
    prevent_initial_call=True
)
def atualizar_campos_edicao(selected_sala_nome):
    if selected_sala_nome:
        selected_sala = next((sala for sala in salas.values() if sala['nome'] == selected_sala_nome), {})
        clp_info = selected_sala.get('clp', {})
        sensor_options = [{'label': sensor['sensor'], 'value': sensor['sensor']} for sensor in selected_sala.get('temperaturas', [])]
        return selected_sala.get('nome', ''), clp_info.get('modelo', ''), clp_info.get('versao_firmware', ''), clp_info.get('status', ''), clp_info.get('ip', ''), sensor_options
    else:
        return '', '', '', '', '', []

# Callback para salvar as mudanças quando clicar no botão
@callback(
    [Output('output-message', 'children'),
     Output('dropdown-salas', 'options')],
    [Input('save-button', 'n_clicks')],
    [State('dropdown-salas', 'value'),
     State('input-nome-sala', 'value'),
     State('input-modelo-clp', 'value'),
     State('input-versao-firmware-clp', 'value'),
     State('input-status-clp', 'value'),
     State('input-ip-clp', 'value')],
    prevent_initial_call=True
)
def salvar_alteracoes(n_clicks, selected_sala_nome, nome_sala, modelo_clp, versao_firmware_clp, status_clp, ip_clp):
    if selected_sala_nome:
        selected_sala = next((sala for sala in salas.values() if sala['nome'] == selected_sala_nome), {})
        clp_info = selected_sala.get('clp', {})
        selected_sala['nome'] = nome_sala
        clp_info['modelo'] = modelo_clp
        clp_info['versao_firmware'] = versao_firmware_clp
        clp_info['status'] = status_clp
        clp_info['ip'] = ip_clp
        salvar_salas(salas)
        return "Alterações salvas com sucesso!", [{'label': sala['nome'], 'value': sala['nome']} for sala in salas.values()]
    else:
        return "", []
